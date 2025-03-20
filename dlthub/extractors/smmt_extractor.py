"""
Module for extracting vehicle registration data from the SMMT website using Scrapy with dlt integration.
"""
import os
from typing import Dict, List, Optional, Any, Iterator
from datetime import datetime
import dlt
from scrapy import Spider
from scrapy.http import Response

from dlthub.config import RAW_DATA_DIR
from .scrapy_helpers import run_spider
from prefect import task


class SMMTSpider(Spider):
    """
    Spider for extracting vehicle registration data from the SMMT website.
    """
    name = "smmt"
    # The start_urls will be set in __init__ from the config
    start_urls = []
    
    def __init__(self, *args, save_html=False, start_url=None, **kwargs):
        """
        Initialize the spider.
        
        Args:
            save_html: Whether to save the HTML response to a file
            start_url: The URL to start crawling from
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.save_html = save_html
        
        # Set the start URL if provided
        if start_url:
            self.start_urls = [start_url]
    
    @task
    def parse(self, response: Response) -> Iterator[Dict[str, Any]]:
        """
        Parse the SMMT website to extract vehicle registration data.
        
        Args:
            response: The response from the request
            
        Yields:
            Dict[str, Any]: Dictionary containing the extracted data
        """
        # Find the table with the monthly data
        tables = response.css('table')
        
        if not tables:
            self.logger.error("No tables found on the SMMT website")
            return
        
        # Assuming the first table contains the monthly data
        table = tables[0]
        
        # Get the current month from the first row
        current_month = "February"  # Default to February as specified by the user
        
        # Try to extract the month from the table
        month_text = table.css('tr:first-child td::text').get()
        if month_text and month_text.strip():
            current_month = month_text.strip()
            self.logger.info(f"Current month detected: {current_month}")
        else:
            self.logger.warning(f"Could not detect current month from the table, using default: {current_month}")
        
        # Define proper column mappings
        column_mappings = {
            "column_0": "fuel",
            "column_1": f"monthly_registrations_{current_month}_2025",
            "column_2": f"monthly_registrations_{current_month}_2024",
            "column_3": "yoy_pct_change",
            "column_4": "market_share_2025",
            "column_5": "market_share_2024"
        }
        
        # Get all rows from the table
        rows = table.css('tr')
        
        # Skip the first two rows (month name and year headers)
        # Start from the third row which contains actual data
        for row_index, row in enumerate(rows):
            # Skip the header rows (first two rows)
            if row_index < 2:
                continue
                
            cells = row.css('td, th')
            if cells:
                data = {}
                for i, cell in enumerate(cells):
                    column_key = f"column_{i}"
                    text = cell.css('::text').get()
                    value = text.strip() if text else ""
                    
                    # Use the proper column name if available
                    if column_key in column_mappings:
                        data[column_mappings[column_key]] = value
                    else:
                        data[column_key] = value
                
                # Skip rows that don't have a proper fuel type (like header rows)
                if data.get("fuel") in ["", None]:
                    continue
                
                # Add metadata
                data['data_source'] = 'SMMT'
                data['extraction_date'] = datetime.now().date().isoformat()
                data['month'] = current_month
                
                yield data
        
        # Save the raw HTML for debugging purposes only if explicitly requested
        if self.save_html:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_file_path = os.path.join(RAW_DATA_DIR, f"smmt_data_{timestamp}.html")
            with open(raw_file_path, 'wb') as f:
                f.write(response.body)
            self.logger.info(f"Saved raw HTML to {raw_file_path}")


@task
@dlt.resource(name="smmt_vehicle_data")
def smmt_vehicle_data(save_html=None) -> Iterator[Dict[str, Any]]:
    """
    DLT resource for extracting vehicle registration data from the SMMT website using Scrapy.
    
    Args:
        save_html: Whether to save the HTML response to a file. If None, uses the value from config.
        
    Yields:
        Dict[str, Any]: Dictionary containing vehicle registration data
    """
    # Get configuration from DLT
    smmt_config = dlt.config["sources.smmt_vehicle_data"]
    scraping_config = dlt.config["sources.scraping"]
    
    # Get the SMMT data URL from the config
    smmt_data_url = smmt_config.get("SMMT_DATA_URL")
    
    if not smmt_data_url:
        raise ValueError("SMMT_DATA_URL not found in config.toml. Please add it to the [sources.smmt_vehicle_data] section.")
    
    # Use the save_html parameter from the function call if provided,
    # otherwise use the value from the config
    save_html_value = save_html if save_html is not None else smmt_config.get('save_html', False)
    
    # Get Scrapy settings from config
    scrapy_settings = smmt_config.get('scrapy_settings', {})
    
    # If scrapy_settings is empty, use the common scraping settings
    if not scrapy_settings:
        scrapy_settings = {
            "ROBOTSTXT_OBEY": scraping_config.get("robotstxt_obey", True),
            "DOWNLOAD_DELAY": scraping_config.get("download_delay", 3),
            "CONCURRENT_REQUESTS": scraping_config.get("concurrent_requests", 1),
            "USER_AGENT": scraping_config.get("user_agent", "Mozilla/5.0"),
            "AUTOTHROTTLE_ENABLED": scraping_config.get("autothrottle_enabled", True),
        }
    
    # Create a spider instance with the save_html parameter and start URL
    spider = SMMTSpider(save_html=save_html_value, start_url=smmt_data_url)
    
    # Run the spider and collect the items
    items = run_spider(spider, scrapy_settings)
    
    # Yield the collected items
    for item in items:
        yield item 
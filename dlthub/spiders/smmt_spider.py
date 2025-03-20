"""
Scrapy spider for extracting vehicle registration data from the SMMT website.
"""
import scrapy
from datetime import datetime
import os
from typing import Dict, Any, List, Iterator

from ..config import SMMT_DATA_URL, RAW_DATA_DIR


class SMMTSpider(scrapy.Spider):
    """
    Spider for extracting vehicle registration data from the SMMT website.
    """
    name = "smmt"
    start_urls = [SMMT_DATA_URL]
    
    def parse(self, response):
        # Find the table with the monthly data
        tables = response.css('table')
        
        if not tables:
            self.logger.error("No tables found on the SMMT website")
            return
        
        # Assuming the first table contains the monthly data
        table = tables[0]
        
        # Extract table headers
        headers = []
        header_row = table.css('tr:first-child')
        if header_row:
            headers = []
            for th in header_row.css('th, td'):
                text = th.css('::text').get()
                if text:
                    headers.append(text.strip())
                else:
                    headers.append(f"column_{len(headers)}")
        
        if not headers:
            self.logger.error("No headers found in the table")
            return
        
        # Extract table data
        for row in table.css('tr')[1:]:  # Skip header row
            cells = row.css('td, th')
            if cells:
                data = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        text = cell.css('::text').get()
                        data[headers[i]] = text.strip() if text else ""
                
                # Add metadata
                data['data_source'] = 'SMMT'
                data['extraction_date'] = datetime.now().date().isoformat()
                
                yield data
        
        # Save the raw HTML for debugging purposes
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_file_path = os.path.join(RAW_DATA_DIR, f"smmt_data_{timestamp}.html")
        with open(raw_file_path, 'wb') as f:
            f.write(response.body) 
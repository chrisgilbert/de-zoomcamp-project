"""
Helper functions for Scrapy integration.
"""
from typing import Dict, Any, List, Type, Optional, Union
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import tempfile
import os
from prefect import task

@task
def run_spider(spider: Union[Type[Spider], Spider], settings: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Run a Scrapy spider and collect the items.
    
    Args:
        spider: The spider class or instance to run
        settings: Optional settings for the spider
        
    Returns:
        List[Dict[str, Any]]: The collected items
    """
    # Create a temporary file to store the items
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    # Configure Scrapy settings
    scrapy_settings = get_project_settings()
    if settings:
        for key, value in settings.items():
            scrapy_settings.set(key, value)
    
    # Configure the feed exporter to write to the temporary file
    scrapy_settings.set('FEEDS', {
        tmp_path: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
        }
    })
    
    # Create and run the crawler process
    process = CrawlerProcess(scrapy_settings)
    
    # Check if spider is a class or an instance
    if isinstance(spider, type):
        # It's a class, so use crawl with the class
        process.crawl(spider)
    else:
        # It's an instance, so use crawl with the instance's class and pass the instance
        process.crawl(spider.__class__, **vars(spider))
    
    process.start()  # This will block until the crawling is finished
    
    # Read the items from the temporary file
    import json
    try:
        with open(tmp_path, 'r') as f:
            items = json.load(f)
        
        # Clean up the temporary file
        os.unlink(tmp_path)
        
        return items
    except Exception as e:
        print(f"Error reading items from temporary file: {e}")
        return [] 
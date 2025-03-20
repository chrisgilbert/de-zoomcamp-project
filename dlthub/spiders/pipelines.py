"""
Scrapy pipelines for processing extracted data.
"""
import pandas as pd
from datetime import datetime
import os
from typing import Dict, Any, List
import dlt

from ..config import RAW_DATA_DIR


class SMMTProcessingPipeline:
    """
    Pipeline for processing SMMT data.
    """
    def __init__(self):
        """Initialize the pipeline."""
        self.items = []
    
    def process_item(self, item, spider):
        """
        Process an item extracted by the spider.
        
        Args:
            item: The item extracted by the spider
            spider: The spider that extracted the item
            
        Returns:
            Dict[str, Any]: The processed item
        """
        # Store the item for later processing
        self.items.append(item)
        return item
    
    def close_spider(self, spider):
        """
        Process all items when the spider is closed.
        
        Args:
            spider: The spider that is being closed
        """
        if not self.items:
            return
        
        # Create a temporary pipeline to use dlt's type inference
        pipeline = dlt.pipeline(
            pipeline_name="temp_smmt_pipeline",
            destination="duckdb",
            dataset_name="temp_smmt_data"
        )
        
        # Use dlt to infer and normalize the data types
        info = pipeline.run(
            self.items,
            table_name="smmt_data",
            write_disposition="replace"
        )
        
        # Get the processed data with inferred types
        with pipeline.sql_client() as client:
            query = "SELECT * FROM temp_smmt_data.smmt_data"
            df = client.query(query).df()
        
        # Save processed data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_file_path = os.path.join(RAW_DATA_DIR, f"smmt_data_processed_{timestamp}.csv")
        df.to_csv(processed_file_path, index=False)
        
        spider.logger.info(f"Processed {len(df)} items with dlt type inference and saved to {processed_file_path}") 
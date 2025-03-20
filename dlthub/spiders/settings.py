"""
Scrapy settings for the SMMT spider.
"""

BOT_NAME = 'smmt_spider'

SPIDER_MODULES = ['dlthub.spiders']
NEWSPIDER_MODULE = 'dlthub.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'dlthub.spiders.pipelines.SMMTProcessingPipeline': 300,
}

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure user agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False 
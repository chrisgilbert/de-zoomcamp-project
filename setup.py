from setuptools import setup, find_packages

setup(
    name="de-zoomcamp-project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "prefect>=2.0.0",
        "dbt-core==1.9.2",
        "dbt-bigquery",
        "python-dotenv",
        "pandas",
        "requests",
        "scrapy>=2.12.0",
        "google-cloud-bigquery",
        "google-cloud-storage",
        "google-cloud-bigquery-storage",
        "dlt[bigquery]",
        "dlt[duckdb]",
        "pytest",
        "pytest-cov",
        "prefect-dbt",
        "sqlfmt",
        "pyarrow>=12.0.0",
    ],
) 
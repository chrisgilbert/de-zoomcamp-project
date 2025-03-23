.PHONY: all tofu transform clean prefect-server

# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

test-env: 
	@echo "BQ_DATASET: $${BQ_DATASET}"
	@echo "GCP_PROJECT_ID: $${GCP_PROJECT_ID}"
	@echo "GCS_BUCKET: $${GCS_BUCKET}"
	@echo "GCS_LOCATION: $${GCS_LOCATION}"
	@echo "GOOGLE_CLOUD_PROJECT: $${GOOGLE_CLOUD_PROJECT}"
	@echo "SOURCES__GOV_UK_EXTRACTOR__GB_REGISTRATIONS_URL: $${SOURCES__GOV_UK_EXTRACTOR__GB_REGISTRATIONS_URL}"
	@echo "SOURCES__GOV_UK_EXTRACTOR__UK_REGISTRATIONS_URL: $${SOURCES__GOV_UK_EXTRACTOR__UK_REGISTRATIONS_URL}"

# Default target
all: tofu load transform

# OpenTofu tasks
tofu:
	@echo "☁️ Running tofu init"
	@echo "☁️ Running OpenTofu apply..."
	cd opentofu && tofu init
	cd opentofu && tofu apply

# dbt tasks
transform: dbt-deps dbt-build

dbt-deps:
	$(MAKE) test-env
	@echo "📦 Installing dbt dependencies..."
	cd dbt && dbt deps

dbt-build:
	$(MAKE) test-env
	@echo "🏗️  Building dbt models..."
	python load_and_transform.py --transform-only

load:
	$(MAKE) test-env
	@echo "🔄 Running load flows..."
	python load_and_transform.py --load-only

prefect-server:
	$(MAKE) test-env
	@echo "🔍 Checking if Prefect server is running..."
	@if ! python -c "import requests; exit(0 if requests.get('http://127.0.0.1:4200', timeout=2).status_code == 200 else 1)" 2>/dev/null; then \
		echo "🚀 Starting Prefect server in background..."; \
		prefect server start --background; \
		echo "⏳ Waiting for Prefect server to start..."; \
		sleep 5; \
	else \
		echo "✅ Prefect server is already running"; \
	fi

setup:
	@echo "⚙️ Setting up python environment..."
	if [ ! -d ".venv" ]; then \
		python -m venv .venv; \
		source .venv/bin/activate; \
	fi
	@echo "⚙️ Installing requirements..."
	pip install -U -r requirements.txt
	@echo "⚙️ Installing prefect-dbt..."
	pip install -U --pre prefect-dbt
	@echo "⚙️ Setting up Prefect server..."
	$(MAKE) prefect-server
	@echo "⚙️ Registering Prefect blocks..."
	prefect block register -m prefect_dbt

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	prefect server stop 

test:
	@echo "🧪 Running tests..."
	python run_tests.py

# Help
help:
	@echo "Available targets:"
	@echo "  test          - Run all tests"
	@echo "  all           - Run all tasks (tofu, load, transform)"
	@echo "  tofu          - Run OpenTofu init and apply"
	@echo "  transform     - Run dbt deps and build"
	@echo "  dbt-deps      - Install dbt dependencies"
	@echo "  dbt-build     - Build dbt models"
	@echo "  prefect-server - Start Prefect server"
	@echo "  load          - Run data loading flows"
	@echo "  setup         - Set up python, prefect server and register blocks"
	@echo "  clean         - Stop Prefect server and cleanup"
	@echo "  help          - Show this help message"
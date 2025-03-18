terraform {
  backend "gcs" {
    bucket = "de-zoomcamp-project-tfstate"
    prefix = "tofu/state"
  }
} 
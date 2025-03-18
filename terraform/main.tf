provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "vehicle_data" {
  dataset_id                  = var.dataset_id
  friendly_name               = "Vehicle Data"
  description                 = "Dataset for UK vehicle registrations"
  location                    = "EU"
  default_table_expiration_ms = null
}

resource "google_storage_bucket" "data_bucket" {
  name     = var.bucket_name
  location = "europe-west2"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_service_account" "pipeline_service_account" {
  account_id   = "vehicle-data-pipeline"
  display_name = "Vehicle Data Pipeline Service Account"
  description  = "Service account for the vehicle data pipeline"
}

resource "google_project_iam_member" "bigquery_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.pipeline_service_account.email}"
}

resource "google_project_iam_member" "storage_object_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.pipeline_service_account.email}"
}

resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.pipeline_service_account.email}"
} 
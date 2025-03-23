variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west2"
}

variable "dataset_id" {
  description = "The BigQuery dataset ID"
  type        = string
  default     = "vehicle_data"
}

variable "bucket_name" {
  description = "The GCS bucket name"
  type        = string
} 
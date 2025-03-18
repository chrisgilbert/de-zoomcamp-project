resource "google_storage_bucket" "tofu_state" {
  name          = "de-zoomcamp-project-tfstate"
  location      = "US"
  force_destroy = false

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30  # days
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  # Optional: Add labels
  labels = {
    environment = "production"
    managed-by  = "opentofu"
    purpose     = "state-storage"
  }
} 
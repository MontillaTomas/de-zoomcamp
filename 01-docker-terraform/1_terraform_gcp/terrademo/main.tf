terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  project = "de-zoomcamp-448414"
  region  = "us-central1"
}


resource "google_storage_bucket" "demo-bucket" {
  name          = "de-zoomcamp-448414" # bucket name should be globally unique
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

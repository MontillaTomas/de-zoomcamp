variable "credentials_file" {
  description = "My Credentials File"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "de-zoomcamp-448414"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "de-zoomcamp-448414"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "asia-southeast1"
}

variable "zone" {
  description = "The GCP zone for resources"
  type        = string
  default     = "asia-southeast1-a"
}

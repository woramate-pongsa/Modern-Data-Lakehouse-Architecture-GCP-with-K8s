# Medallion Architecture GCS Buckets
resource "google_storage_bucket" "bronze" {
  name                        = "${var.project_id}-lake-bronze"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "silver" {
  name                        = "${var.project_id}-lake-silver"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "gold" {
  name                        = "${var.project_id}-lake-gold"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# --- IAM & Service Accounts ---

# Dedicated Service Account for Spark Jobs
resource "google_service_account" "spark_sa" {
  account_id   = "spark-job-sa"
  display_name = "Service Account for Spark Jobs on GKE"
}

# Grant Spark SA access to Bronze, Silver, and Gold buckets
resource "google_storage_bucket_iam_member" "spark_bronze_admin" {
  bucket = google_storage_bucket.bronze.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.spark_sa.email}"
}

resource "google_storage_bucket_iam_member" "spark_silver_admin" {
  bucket = google_storage_bucket.silver.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.spark_sa.email}"
}

resource "google_storage_bucket_iam_member" "spark_gold_admin" {
  bucket = google_storage_bucket.gold.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.spark_sa.email}"
}

# Workload Identity Binding for Spark
resource "google_service_account_iam_member" "spark_workload_identity" {
  service_account_id = google_service_account.spark_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/spark-sa]"
}

# Dedicated Service Account for Ingestion API
resource "google_service_account" "api_sa" {
  account_id   = "ingestion-api-sa"
  display_name = "Service Account for Ingestion API"
}

resource "google_storage_bucket_iam_member" "api_bronze_admin" {
  bucket = google_storage_bucket.bronze.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.api_sa.email}"
}

resource "google_storage_bucket_iam_member" "api_silver_admin" {
  bucket = google_storage_bucket.silver.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.api_sa.email}"
}

resource "google_storage_bucket_iam_member" "api_gold_admin" {
  bucket = google_storage_bucket.gold.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.api_sa.email}"
}

# Workload Identity Binding for Ingestion API
resource "google_service_account_iam_member" "api_workload_identity" {
  service_account_id = google_service_account.api_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/ingestion-api-sa]"
}

# --- Infrastructure ---

# Artifact Registry for Docker Images
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "data-platform-repo"
  description   = "Docker repository for data platform components"
  format        = "DOCKER"
}

# GKE Autopilot Cluster
resource "google_container_cluster" "primary" {
  name     = "data-platform-cluster"
  location = var.region

  # Enabling Autopilot mode
  enable_autopilot = true

  # Deletion protection disabled for learning/dev environment
  deletion_protection = false
}


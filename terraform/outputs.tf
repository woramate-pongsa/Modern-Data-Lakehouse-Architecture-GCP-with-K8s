output "gcs_bucket_names" {
  description = "Names of the GCS buckets"
  value = [
    google_storage_bucket.bronze.name,
    google_storage_bucket.silver.name,
    google_storage_bucket.gold.name
  ]
}

output "artifact_registry_repo_id" {
  description = "The ID of the Artifact Registry repository"
  value       = google_artifact_registry_repository.repo.id
}

output "gke_cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

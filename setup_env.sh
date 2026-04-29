#!/bin/bash

# Phase 0: GCP Environment Configuration Script
# Usage: Update PROJECT_ID and run: bash setup_env.sh

# 1. Configuration - Set your Project ID here
PROJECT_ID="my-project-lakehouse-k8s"
SA_NAME="terraform-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Configuring environment for project: ${PROJECT_ID}..."

# 1. Set the active GCP project
gcloud config set project "${PROJECT_ID}"

# 2. Enable the required APIs
echo "Enabling GCP Services..."
gcloud services enable \
    compute.googleapis.com \
    container.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    bigquery.googleapis.com

# 3. Create a new Service Account
echo "Creating Service Account: ${SA_NAME}..."
gcloud iam service-accounts create "${SA_NAME}" \
    --display-name="Terraform Service Account"

# 4. Bind necessary roles to this Service Account
echo "Binding IAM roles..."
# roles/editor: For general resource management
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/editor"

# roles/resourcemanager.projectIamAdmin: To allow Terraform to manage IAM policies
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/resourcemanager.projectIamAdmin"

# 5. Create and download a JSON key file
echo "Generating Service Account key..."
gcloud iam service-accounts keys create terraform-key.json \
    --iam-account="${SA_EMAIL}"

# 6. Instructions for exporting credentials
echo "----------------------------------------------------------------"
echo "Setup Complete."
echo "To set your credentials for the current session, run:"
echo "export GOOGLE_APPLICATION_CREDENTIALS=\"\$(pwd)/terraform-key.json\""
echo "----------------------------------------------------------------"

# 📖 Modern Data Lakehouse: Step-by-Step Execution Guide

This guide documents every command used to provision, deploy, and run the Modern Data Lakehouse system on GCP. Follow these steps to reproduce the entire pipeline.

---

## 🏗 Phase 0: Environment Setup
Before starting, ensure your GCP project is set and APIs are enabled.

### 1. Configure GCloud Project
```bash
gcloud config set project "my-project-lakehouse-k8s"
```
*Sets the active project context for all subsequent `gcloud` and `bq` commands.*

### 2. Enable Required APIs
```bash
gcloud services enable \
    compute.googleapis.com \
    container.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    bigquery.googleapis.com
```
*Enables the necessary GCP services for GKE, Artifact Registry, Cloud Storage, and BigQuery.*

---

## 🛠 Phase 1: Infrastructure as Code (Terraform)
Provisioning the GCS buckets, GKE cluster, and Artifact Registry.

### 3. Initialize & Apply Terraform
```bash
cd terraform
terraform init
GOOGLE_APPLICATION_CREDENTIALS=../terraform-key.json terraform apply -auto-approve
```
*   `terraform init`: Downloads the Google provider plugins.
*   `terraform apply`: Creates the resources defined in `main.tf`. We pass `GOOGLE_APPLICATION_CREDENTIALS` to ensure Terraform has the permissions granted to our Service Account.

---

## 📥 Phase 2: Ingestion Layer (API)
Building and deploying the FastAPI service that collects data.

### 4. Authenticate Docker with GCP
```bash
gcloud auth configure-docker asia-southeast1-docker.pkg.dev --quiet
```
*Configures Docker to use `gcloud` as a credential helper for pushing images to the Artifact Registry.*

### 5. Build & Push Ingestion Image
```bash
cd ingestion-api
docker build -t asia-southeast1-docker.pkg.dev/my-project-lakehouse-k8s/data-platform-repo/ingestion-api:latest .
docker push asia-southeast1-docker.pkg.dev/my-project-lakehouse-k8s/data-platform-repo/ingestion-api:latest
```
*Packages the Python code into a Docker image and uploads it to the cloud.*

### 6. Connect to GKE Cluster
```bash
gcloud container clusters get-credentials data-platform-cluster --region asia-southeast1
```
*Updates your `kubeconfig` so `kubectl` can communicate with your new GKE cluster.*

### 7. Deploy Ingestion API
```bash
kubectl apply -f ingestion-api/k8s/service-account.yaml
kubectl apply -f ingestion-api/k8s/k8s-manifest.yaml
```
*   `service-account.yaml`: Creates a K8s Service Account linked to GCP (Workload Identity).
*   `k8s-manifest.yaml`: Creates the Deployment (Pods) and the LoadBalancer (Public IP).

---

## 🤖 Phase 3: Data Simulation
Generating traffic to test the pipeline.

### 8. Run Simulator (Background)
```bash
python3 data-simulation/data_simulator.py > simulation.log 2>&1 &
```
*Starts the Python script in the background. It sends JSON events to the API's LoadBalancer IP. Logs are saved to `simulation.log`.*

---

## ⚙️ Phase 4: Data Processing (Spark on K8s)
Transforming data from Bronze to Silver to Gold.

### 9. Install Spark Operator (via Helm)
```bash
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install my-spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --set webhook.enable=true
```
*Installs the operator that allows Kubernetes to manage Spark jobs as native objects.*

### 10. Build & Push Spark Job Image
```bash
cd spark-jobs
docker build -t asia-southeast1-docker.pkg.dev/my-project-lakehouse-k8s/data-platform-repo/spark-jobs:latest .
docker push asia-southeast1-docker.pkg.dev/my-project-lakehouse-k8s/data-platform-repo/spark-jobs:latest
```
*Creates an image containing the PySpark scripts and the Delta Lake dependencies.*

### 11. Run Bronze ➔ Silver Job
```bash
kubectl apply -f spark-jobs/k8s/spark-rbac.yaml
kubectl apply -f spark-jobs/k8s/service-account.yaml
kubectl apply -f spark-jobs/k8s/spark-app-bronze-silver.yaml
```
*Starts the transformation. Spark reads raw JSON from Bronze and writes cleaned Delta Tables to Silver.*

### 12. Run Silver ➔ Gold Job
```bash
kubectl apply -f spark-jobs/k8s/spark-app-silver-gold.yaml
```
*Reads the cleaned Silver data, calculates aggregates (event counts), and writes the final results to Gold.*

---

## 📊 Phase 5: Analytics (BigQuery)
Linking the data for SQL access.

### 13. Create BigQuery External Table
```bash
bq query --use_legacy_sql=false \
"CREATE SCHEMA IF NOT EXISTS \`my-project-lakehouse-k8s.analytics\` OPTIONS(location='asia-southeast1');
CREATE OR REPLACE EXTERNAL TABLE \`my-project-lakehouse-k8s.analytics.user_event_summary\`
OPTIONS (format = 'DELTA_LAKE', uris = ['gs://my-project-lakehouse-k8s-lake-gold/user_event_summary/']);"
```
*Creates a dataset and a "virtual table" that points directly to the files in GCS.*

### 14. Query the Results
```bash
bq query --use_legacy_sql=false "SELECT * FROM \`my-project-lakehouse-k8s.analytics.user_event_summary\` LIMIT 10;"
```
*Fetches the final processed data using SQL.*

---

## 🧹 Cleanup (Optional)
To avoid ongoing costs, destroy the resources when finished.

```bash
cd terraform
terraform destroy -auto-approve
```

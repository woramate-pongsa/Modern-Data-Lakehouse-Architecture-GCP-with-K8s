# Modern-Data-Lakehouse-Architecture-GCP-with-K8s

## 🛠 Tech Stack Overview
- **Infrastructure:** Terraform, Google Kubernetes Engine (GKE Autopilot)
- **Ingestion:** FastAPI (Python), Docker, Artifact Registry, Load Balancer
- **Storage:** Google Cloud Storage (GCS), Delta Lake (Medallion Architecture)
- **Orchestration:** Apache Airflow (Cloud Composer or GKE)
- **Processing:** Apache Spark on Kubernetes (PySpark)
- **Analytics & BI:** BigQuery, Looker Studio

---

## 📅 Phase 0: Foundation & Environment Setup
*Goal: Prepare the environment for running commands and managing permissions.*

- [x] Create GCP Project and enable Billing.
- [x] Install Google Cloud CLI and Terraform in Codespaces.
- [x] Create Service Account (terraform-sa) and JSON Key.
- [x] Enable APIs: Compute, GKE, Artifact Registry, GCS, BigQuery.

**Gemini CLI Prompt:** > "Provide a bash script to enable GCP APIs (GKE, GCS, BigQuery, Artifact Registry) and create a Service Account with Editor roles for Terraform."

---

## 🏗 Phase 1: Infrastructure as Code (IaC)
*Goal: Provision all resources via Terraform.*

- [x] Write `main.tf` to create GCS Buckets (Bronze, Silver, Gold).
- [x] Create Artifact Registry (Docker Repository).
- [x] Create GKE Autopilot Cluster.
- [x] Run `terraform init`, `plan`, and `apply`.

**Gemini CLI Prompt:** > "Write Terraform code to create 3 GCS buckets for a medallion architecture, a GKE Autopilot cluster, and a Docker Artifact Registry in the asia-southeast1 region."

---

## 📥 Phase 2: Ingestion Layer (API & Docker)
*Goal: Create a data entry point and package it into a Container.*

- [x] Write FastAPI (Python) to receive JSON Events and save to GCS Bronze.
- [x] Write Dockerfile and Build Image to Artifact Registry.
- [x] Write Kubernetes Manifests (`deployment.yaml`, `service.yaml`).
- [x] Deploy to GKE and get External IP from Load Balancer. (IP: 136.110.6.1).

**Gemini CLI Prompt:** > "Create a FastAPI application that receives JSON events and saves them to a GCS bucket. Also, provide a Dockerfile and Kubernetes deployment manifest with a LoadBalancer service."

---

## 🤖 Phase 3: Data Simulation (The Generator)
*Goal: Simulate user behavior data.*

- [x] Design Data Schema (user_id, event_type, item_id, timestamp).
- [x] Write a Python Script to generate random data and send HTTP POST to API.

**Gemini CLI Prompt:** > "Write a Python script to simulate user behavior (view_item, add_to_cart, purchase) and send these events as JSON via HTTP POST to a specific URL at a rate of 5 requests per second."

---

## ⚙️ Phase 4: Orchestration & Processing
*Goal: Process data using Spark and orchestrate with Airflow.*

- [ ] Install Airflow and Configure Spark on K8s.
- [x] Write PySpark Job to transform data from Bronze -> Silver (Clean/Join).
- [x] Write PySpark Job to aggregate data from Silver -> Gold (Delta Table Format).
- [x] Create Airflow DAG to orchestrate the pipeline.

**Gemini CLI Prompt:** > "Write a PySpark script to read JSON files from GCS, perform data cleaning, and save the output as a Delta Table. Then, write an Airflow DAG to trigger this Spark job daily."

---

## 📊 Phase 5: Data Warehouse & BI
*Goal: Connect data for analysis and visualization.*

- [x] Create BigQuery External Table linked to GCS Gold Layer (Delta/Parquet).
- [ ] Create Dashboard in Looker Studio to display KPIs.

**Gemini CLI Prompt:** > "Provide the SQL command to create a BigQuery External Table that points to a Parquet/Delta dataset in GCS. Suggest 3 key visualizations for an e-commerce event dashboard."

---

## 💡 Tips for using Gemini CLI / Copilot
- **Context is King:** When starting a new Phase, copy the Phase heading from this Roadmap and paste into the AI chat to provide context.
- **Error Debugging:** If you encounter issues, copy the entire Error Log and ask, "I got this error while running X, how to fix it?"
- **Incremental Progress:** Don't ask to build the whole project at once. Do it file by file or sub-task by sub-task.
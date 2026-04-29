import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage

app = FastAPI(title="Data Ingestion API")

# Configuration from environment variables
BRONZE_BUCKET_NAME = os.getenv("BRONZE_BUCKET_NAME")

class EventData(BaseModel):
    user_id: str
    event_type: str
    item_id: str
    timestamp: str

@app.post("/collect", status_code=200)
async def collect_event(event: EventData):
    if not BRONZE_BUCKET_NAME:
        raise HTTPException(status_code=500, detail="BRONZE_BUCKET_NAME environment variable not set")

    try:
        # Initialize GCS client inside the handler
        storage_client = storage.Client()
        
        # Prepare data for storage (using model_dump for Pydantic v2)
        event_dict = event.model_dump()
        payload = json.dumps(event_dict)

        # Generate unique filename: event_YYYYMMDD_HHMMSS_<uuid>.json
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"event_{now}_{unique_id}.json"

        # Upload to GCS
        bucket = storage_client.bucket(BRONZE_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(payload, content_type='application/json')

        return {
            "status": "success",
            "message": f"Event stored successfully as {filename}",
            "bucket": BRONZE_BUCKET_NAME
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store event: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

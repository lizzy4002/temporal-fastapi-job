from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import asyncio

app = FastAPI(title="Mock Temporal Jobs API")

# In-memory store for jobs
jobs_store: Dict[str, Dict] = {}

# Pydantic models
class JobInput(BaseModel):
    numbers: List[int]

class JobOptions(BaseModel):
    fail_first_attempt: bool = True

class JobRequest(BaseModel):
    input: JobInput
    options: JobOptions

# Mock workflow function
async def run_job(job_id: str, numbers: List[int], fail_first_attempt: bool):
    attempt = 1
    max_attempts = 3
    while attempt <= max_attempts:
        jobs_store[job_id]["progress"]["attempt"] = attempt
        jobs_store[job_id]["progress"]["stage"] = "compute"

        if fail_first_attempt and attempt == 1:
            jobs_store[job_id]["status"] = "RUNNING"
            jobs_store[job_id]["error"] = "Intentional first attempt failure"
            await asyncio.sleep(1)  # simulate work
            attempt += 1
            continue

        # Compute sum of numbers
        result = sum(numbers)
        jobs_store[job_id]["status"] = "SUCCEEDED"
        jobs_store[job_id]["result"] = result
        jobs_store[job_id]["error"] = None
        break

# POST /jobs endpoint
@app.post("/jobs")
async def start_job(request: JobRequest):
    job_id = str(uuid.uuid4())
    jobs_store[job_id] = {
        "job_id": job_id,
        "status": "STARTED",
        "progress": {"stage": "pending", "attempt": 0},
        "result": None,
        "error": None
    }

    # Start job asynchronously
    asyncio.create_task(run_job(job_id, request.input.numbers, request.options.fail_first_attempt))
    return {"job_id": job_id, "status": "STARTED"}

# GET /jobs/{job_id} endpoint
@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = jobs_store.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return job

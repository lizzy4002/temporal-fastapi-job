import asyncio

# In-memory storage for jobs
jobs_store = {}

async def start_job(job_id: str, job_data: dict):
    # Store initial job state
    jobs_store[job_id] = {
        "status": "RUNNING",
        "progress": {"stage": "compute", "attempt": 1},
        "result": None,
        "error": None,
    }
    
    # Simulate job execution asynchronously
    asyncio.create_task(run_job(job_id, job_data))

async def run_job(job_id: str, job_data: dict):
    numbers = job_data["input"]["numbers"]
    fail_first = job_data["options"].get("fail_first_attempt", False)
    
    attempt = 1
    while attempt <= 3:
        try:
            # Fail the first attempt if requested
            if fail_first and attempt == 1:
                raise Exception("Intentional first attempt failure")
            
            result = sum(numbers)  # simple computation
            jobs_store[job_id]["status"] = "SUCCEEDED"
            jobs_store[job_id]["result"] = result
            jobs_store[job_id]["progress"]["attempt"] = attempt
            break
        except Exception as e:
            jobs_store[job_id]["status"] = "RUNNING"
            jobs_store[job_id]["progress"]["attempt"] = attempt
            jobs_store[job_id]["error"] = str(e)
            attempt += 1
            await asyncio.sleep(1)  # simulate retry delay
    else:
        jobs_store[job_id]["status"] = "FAILED"

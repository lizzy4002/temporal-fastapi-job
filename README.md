Temporal-FastAPI Job Demo (Mock Version)

This project demonstrates a **FastAPI server** with **Temporal-style workflow simulation** for jobs.  
Since Docker/WSL2 is not available, the Temporal server and worker are **mocked using in-memory Python logic**.

Project Structure

temporal-fastapi-job/
│
├─ api/
│ ├─ init.py
│ ├─ main.py # FastAPI API
│ └─ mock_temporal.py # Mocked Temporal worker
│
├─ worker/
│ ├─ init.py
│ └─ worker.py # Real Temporal worker template (optional)
│
├─ workflows/
│ ├─ init.py
│ └─ jobs_workflow.py # Workflow definition (optional)
│
├─ requirements.txt
└─ README.md


Local Setup Instructions

1. **Create and activate virtual environment**

```cmd
python -m venv venv
venv\Scripts\activate

2.Install dependencies
pip install -r requirements.txt

3.Start FastAPI server
python -m uvicorn api.main:app --reload

. API runs at http://127.0.0.1:8000
. Swagger UI: http://127.0.0.1:8000/docs


How Jobs Work (Mock)
Jobs stored in memory (jobs_store).
Workflow simulation uses asyncio.create_task.
Retry logic:
fail_first_attempt=true fails first attempt.
Automatic retry up to 3 attempts.
Status: RUNNING, SUCCEEDED, or FAILED.
Deterministic: sums numbers in input array.

API Endpoints
1. Start a Job
POST /jobs
Request Example:{
  "input": {"numbers": [1, 2, 3, 4]},
  "options": {"fail_first_attempt": true}
}

Response Example:
{
  "job_id": "c3f1f6b8-1234-4abc-8d9f-6b7e8a9d0c12",
  "status": "STARTED"
}

2.Query Job Status
GET /jobs/{job_id}
Example During Retry:
{
  "status": "RUNNING",
  "progress": {"stage": "compute", "attempt": 1},
  "result": null,
  "error": "Intentional first attempt failure"
}

Example After Success:
{
  "status": "SUCCEEDED",
  "progress": {"stage": "compute", "attempt": 2},
  "result": 10,
  "error": null
}


Verification Steps
Start FastAPI server.
POST a job with fail_first_attempt=true.
Poll GET /jobs/{job_id} to observe:
Retry attempt increments
Error appears on first attempt
Final status=SUCCEEDED and correct result

Key Design Decisions
Mock Temporal: Simulated using asyncio in Python.
Deterministic: Jobs compute sum(numbers) only.
In-Memory Storage: No database needed.
Extensibility: Real worker template included in worker/worker.py.\

AI Usage Disclosure
ChatGPT used to scaffold project, provide mock workflow logic, and draft README.
All code is explainable manually; AI was used for guidance and scaffolding.

Instructions to add this in Notepad:
1. Open CMD in your project folder:
```cmd
cd C:\Users\User\temporal-fastapi-job
notepad README.md


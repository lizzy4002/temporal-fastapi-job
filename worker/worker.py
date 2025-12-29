import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.jobs_workflow import JobWorkflow
from worker.activities import compute_activity

async def main():
    
    client = await Client.connect("localhost:7233")

    
    worker = Worker(
        client,
        task_queue="jobs-task-queue",
        workflows=[JobWorkflow],
        activities=[compute_activity],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

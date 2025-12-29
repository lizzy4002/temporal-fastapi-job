import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.jobs_workflow import JobWorkflow
from worker.activities import compute_activity

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Start a worker listening to "jobs-task-queue"
    worker = Worker(
        client,
        task_queue="jobs-task-queue",
        workflows=[JobWorkflow],
        activities=[compute_activity],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

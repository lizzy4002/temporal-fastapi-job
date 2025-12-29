from temporalio import workflow
from worker.activities import compute_activity

@workflow.defn
class JobWorkflow:
    @workflow.run
    async def run(self, input: dict, options: dict):
        attempt = 1
        while True:
            try:
                result = await workflow.execute_activity(
                    compute_activity,
                    input["numbers"],
                    fail_first_attempt=options.get("fail_first_attempt", False),
                    schedule_to_close_timeout=10,
                    retry_policy={"maximum_attempts": 3},
                )
                return {"status": "SUCCEEDED", "result": result, "attempt": attempt}
            except Exception:
                attempt += 1
                if attempt > 3:
                    return {"status": "FAILED", "result": None, "attempt": attempt}

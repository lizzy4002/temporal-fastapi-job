from temporalio import activity


first_fail_registry = {}

@activity.defn
async def compute_activity(numbers: list, fail_first_attempt: bool = False):
    job_key = "-".join(map(str, numbers))
    if fail_first_attempt and job_key not in first_fail_registry:
        first_fail_registry[job_key] = True
        raise Exception("Intentional first attempt failure")
    return sum(numbers)

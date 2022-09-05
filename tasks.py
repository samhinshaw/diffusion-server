import random
import time
from celery import Celery, current_task

broker_url = "pyamqp://guest:guest@diffusion_rabbitmq:5672"
backend_url = "rpc://guest:guest@diffusion_rabbitmq:5672"

celery = Celery(
    "tasks",
    backend="rpc://guest:guest@diffusion_rabbitmq:5672",
    broker="pyamqp://guest:guest@diffusion_rabbitmq:5672",
)


@celery.task()
def async_task():
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
    message = ""
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = "{0} {1} {2}...".format(
                random.choice(verb), random.choice(adjective), random.choice(noun)
            )
        current_task.update_state(
            state="PROGRESS", meta={"current": i, "total": total, "status": message}
        )
        time.sleep(1)
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}

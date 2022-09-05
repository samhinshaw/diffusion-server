from celery import Celery

broker_url = "pyamqp://guest:guest@diffusion_rabbitmq:5672"
backend_url = "rpc://guest:guest@diffusion_rabbitmq:5672"

task_manager = Celery("tasks", broker=broker_url)
task_manager.conf.update(app.config)

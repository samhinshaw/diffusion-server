from os import path, getcwd
import random
import time
from flask import (
    Flask,
    request,
    render_template,
    session,
    send_from_directory,
    jsonify,
    url_for,
)
from celery import Celery, current_task
from flask import Flask

app = Flask(__name__, static_folder=path.join(getcwd(), "ui"), static_url_path="/")
app.config["CELERY_BROKER_URL"] = "pyamqp://guest:guest@diffusion_rabbitmq:5672"
app.config["CELERY_RESULT_BACKEND"] = "rpc://guest:guest@diffusion_rabbitmq:5672"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task()
def long_task():
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


@app.route("/longtask", methods=["POST"])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {"Location": url_for("taskstatus", task_id=task.id)}


@app.route("/status/<task_id>")
def taskstatus(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == "PENDING":
        # job did not start yet
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# serve index
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# Serve static app
# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
# def serve(path):
#     if path != "" and path.exists(app.static_folder + "/" + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", use_reloader=True, port=9022, threaded=True)

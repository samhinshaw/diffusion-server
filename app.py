from os import path, getcwd
from flask import (
    Flask,
    send_from_directory,
    jsonify,
    url_for,
)
from tasks import async_task


app = Flask(__name__, static_folder=path.join(getcwd(), "ui"), static_url_path="/")


@app.route("/longtask", methods=["POST"])
def longtask():
    task = async_task.delay()
    return jsonify({}), 202, {"Location": url_for("taskstatus", task_id=task.id)}


@app.route("/status/<task_id>")
def taskstatus(task_id):
    print("goooooo")
    task = async_task.AsyncResult(task_id)
    print(task)
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


# if __name__ == "__main__":
#     app.run("0.0.0.0", use_reloader=True, port=9022, threaded=True)

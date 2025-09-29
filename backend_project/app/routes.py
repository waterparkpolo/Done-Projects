from flask import Blueprint, request, jsonify
from datetime import datetime
from . import db
from .models import User, Task, Note

api = Blueprint("api", __name__, url_prefix="/api")

# --- helpers ---
def task_to_dict(t: Task):
    return {
        "id": t.id,
        "user_id": t.user_id,
        "title": t.title,
        "is_done": t.is_done,
        "created_at": t.created_at.isoformat(),
    }

# =======================
#        TASKS
# =======================

# GET /api/tasks  (list)
@api.get("/tasks")
def list_tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([task_to_dict(t) for t in tasks]), 200

# POST /api/tasks  (create)
@api.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    user_id = data.get("user_id")

    if not title or not user_id:
        return {"error": "title and user_id required"}, 400

    # optional: verify user exists
    if not User.query.get(user_id):
        return {"error": f"user_id {user_id} not found"}, 404

    t = Task(title=title, user_id=user_id, created_at=datetime.utcnow())
    db.session.add(t)
    db.session.commit()
    return task_to_dict(t), 201

# GET /api/tasks/<id>  (read one)
@api.get("/tasks/<int:task_id>")
def get_task(task_id):
    t = Task.query.get(task_id)
    if not t:
        return {"error": "task not found"}, 404
    return task_to_dict(t), 200

# PUT /api/tasks/<id>  (replace all fields)
@api.put("/tasks/<int:task_id>")
def put_task(task_id):
    t = Task.query.get(task_id)
    if not t:
        return {"error": "task not found"}, 404

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    user_id = data.get("user_id")
    is_done = data.get("is_done")

    if title is None or user_id is None or is_done is None:
        return {"error": "title, user_id, is_done required"}, 400

    if not User.query.get(user_id):
        return {"error": f"user_id {user_id} not found"}, 404

    t.title = title
    t.user_id = user_id
    t.is_done = bool(is_done)
    db.session.commit()
    return task_to_dict(t), 200

# PATCH /api/tasks/<id>  (partial update)
@api.patch("/tasks/<int:task_id>")
def patch_task(task_id):
    t = Task.query.get(task_id)
    if not t:
        return {"error": "task not found"}, 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        t.title = data["title"]
    if "is_done" in data:
        t.is_done = bool(data["is_done"])
    if "user_id" in data:
        if not User.query.get(data["user_id"]):
            return {"error": f"user_id {data['user_id']} not found"}, 404
        t.user_id = data["user_id"]

    db.session.commit()
    return task_to_dict(t), 200

# DELETE /api/tasks/<id>
@api.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    t = Task.query.get(task_id)
    if not t:
        return {"error": "task not found"}, 404
    db.session.delete(t)
    db.session.commit()
    return {"status": "deleted", "id": task_id}, 200

# =======================
#        NOTES
# =======================

@api.get("/notes")
def list_notes():
    notes = Note.query.all()
    data = [
        {
            "id": n.id,
            "user_id": n.user_id,
            "body": n.body,
            "created_at": n.created_at.isoformat(),
        }
        for n in notes
    ]
    return jsonify(data), 200

@api.post("/notes")
def create_note():
    payload = request.get_json(force=True)
    body = payload.get("body")
    user_id = payload.get("user_id")
    if not body or not user_id:
        return {"error": "body and user_id required"}, 400
    n = Note(body=body, user_id=user_id)
    db.session.add(n)
    db.session.commit()
    return {"id": n.id, "user_id": n.user_id, "body": n.body}, 201

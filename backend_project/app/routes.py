from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import User, Task, Note

api = Blueprint("api", __name__, url_prefix="/api")

# -------- helpers --------
def task_to_dict(t: Task):
    return {
        "id": t.id,
        "user_id": t.user_id,
        "title": t.title,
        "is_done": t.is_done,
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }

def note_to_dict(n: Note):
    return {
        "id": n.id,
        "user_id": n.user_id,
        "body": n.body,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }

# =======================
#         TASKS
# =======================


@api.post("/tasks")
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return {"error": "title required"}, 400

    # Enforce ownership: always use token's user id
    t = Task(title=title, user_id=user_id)  # let DB default set created_at
    db.session.add(t)
    db.session.commit()
    return task_to_dict(t), 201

@api.get("/tasks")
@jwt_required()
def list_tasks():
    uid = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=uid).order_by(Task.created_at.desc()).all()
    return [task_to_dict(t) for t in tasks], 200


@api.get("/tasks/<int:task_id>")
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())
    t = db.session.get(Task, task_id)
    if not t or t.user_id != user_id:
        return {"error": "task not found"}, 404
    return task_to_dict(t), 200

@api.put("/tasks/<int:task_id>")
@jwt_required()
def put_task(task_id):
    user_id = int(get_jwt_identity())
    t = db.session.get(Task, task_id)
    if not t or t.user_id != user_id:
        return {"error": "task not found"}, 404

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    is_done = data.get("is_done")

    if title is None or is_done is None:
        return {"error": "title and is_done required"}, 400

    t.title = title
    t.is_done = bool(is_done)
    db.session.commit()
    return task_to_dict(t), 200

@api.patch("/tasks/<int:task_id>")
@jwt_required()
def patch_task(task_id):
    user_id = int(get_jwt_identity())
    t = db.session.get(Task, task_id)
    if not t or t.user_id != user_id:
        return {"error": "task not found"}, 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        t.title = data["title"]
    if "is_done" in data:
        t.is_done = bool(data["is_done"])
    db.session.commit()
    return task_to_dict(t), 200

@api.delete("/tasks/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    t = db.session.get(Task, task_id)
    if not t or t.user_id != user_id:
        return {"error": "task not found"}, 404
    db.session.delete(t)
    db.session.commit()
    return {"status": "deleted", "id": task_id}, 200

# =======================
#         NOTES
# =======================

@api.get("/notes")
@jwt_required()
def list_notes():
    user_id = int(get_jwt_identity())
    notes = db.session.query(Note).filter(Note.user_id == user_id).order_by(Note.id.asc()).all()
    return jsonify([note_to_dict(n) for n in notes]), 200

@api.post("/notes")
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    body = data.get("body")
    if not body:
        return {"error": "body required"}, 400

    n = Note(body=body, user_id=user_id)
    db.session.add(n)
    db.session.commit()
    return {"id": n.id, "user_id": n.user_id, "body": n.body}, 201

@api.get("/notes/<int:note_id>")
@jwt_required()
def get_note(note_id):
    user_id = int(get_jwt_identity())
    n = db.session.get(Note, note_id)
    if not n or n.user_id != user_id:
        return {"error": "note not found"}, 404
    return note_to_dict(n), 200

@api.patch("/notes/<int:note_id>")
@jwt_required()
def patch_note(note_id):
    user_id = int(get_jwt_identity())
    n = db.session.get(Note, note_id)
    if not n or n.user_id != user_id:
        return {"error": "note not found"}, 404

    data = request.get_json(silent=True) or {}
    if "body" in data:
        n.body = data["body"]
    db.session.commit()
    return note_to_dict(n), 200

@api.delete("/notes/<int:note_id>")
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())
    n = db.session.get(Note, note_id)
    if not n or n.user_id != user_id:
        return {"error": "note not found"}, 404
    db.session.delete(n)
    db.session.commit()
    return {"status": "deleted", "id": note_id}, 200

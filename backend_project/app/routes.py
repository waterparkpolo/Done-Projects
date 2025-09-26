from flask import Blueprint, request, jsonify
from . import db
from .models import User, Task, Note

api = Blueprint("api", __name__, url_prefix="/api")

@api.get("/tasks")
def list_tasks():
    tasks = Task.query.all()
    data = [
        {"id": t.id, "user_id": t.user_id, "title": t.title, "is_done": t.is_done, "created_at": t.created_at.isoformat()}
        for t in tasks
    ]
    return jsonify(data), 200

@api.post("/tasks")
def create_task():
    payload = request.get_json(force=True)
    title = payload.get("title")
    user_id = payload.get("user_id")
    if not title or not user_id:
        return {"error": "title and user_id required"}, 400
    t = Task(title=title, user_id=user_id)
    db.session.add(t)
    db.session.commit()
    return {"id": t.id, "title": t.title, "user_id": t.user_id, "is_done": t.is_done}, 201

@api.get("/notes")
def list_notes():
    notes = Note.query.all()
    data = [
        {"id": n.id, "user_id": n.user_id, "body": n.body, "created_at": n.created_at.isoformat()}
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

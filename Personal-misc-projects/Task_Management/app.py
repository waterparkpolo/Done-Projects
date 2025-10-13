import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, abort, g
)
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from dotenv import load_dotenv

# load .env if present
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-to-a-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return bcrypt.verify(password, self.password_hash)
        except Exception:
            return False

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", back_populates="tasks")

# UTIL: create DB if not exists
with app.app_context():
    db.create_all()

# Simple login_required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        # load user into g
        user = User.query.get(session["user_id"])
        if not user:
            session.pop("user_id", None)
            return redirect(url_for("login"))
        g.user = user
        return f(*args, **kwargs)
    return decorated

# ROUTES - Frontend
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("register"))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful — please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid credentials.", "error")
            return redirect(url_for("login"))
        session["user_id"] = user.id
        flash("Logged in successfully.", "success")
        next_url = request.args.get("next") or url_for("tasks")
        return redirect(next_url)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/tasks")
@login_required
def tasks():
    user = g.user
    tasks = Task.query.filter_by(owner_id=user.id).order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=tasks, user=user)

@app.route("/tasks/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip() or None
    due_date_raw = request.form.get("due_date", "").strip()
    if not title:
        flash("Title is required.", "error")
        return redirect(url_for("tasks"))

    due_date = None
    if due_date_raw:
        try:
            # accept YYYY-MM-DD or YYYY-MM-DDTHH:MM if provided
            if "T" in due_date_raw:
                due_date = datetime.fromisoformat(due_date_raw)
            else:
                due_date = datetime.strptime(due_date_raw, "%Y-%m-%d")
        except ValueError:
            flash("Invalid due date format. Use YYYY-MM-DD.", "error")
            return redirect(url_for("tasks"))

    task = Task(title=title, description=description, due_date=due_date, owner_id=g.user.id)
    db.session.add(task)
    db.session.commit()
    flash("Task added.", "success")
    return redirect(url_for("tasks"))

@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=g.user.id).first_or_404()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip() or None
        due_date_raw = request.form.get("due_date", "").strip()
        if not title:
            flash("Title cannot be empty.", "error")
            return redirect(url_for("edit_task", task_id=task_id))
        due_date = None
        if due_date_raw:
            try:
                if "T" in due_date_raw:
                    due_date = datetime.fromisoformat(due_date_raw)
                else:
                    due_date = datetime.strptime(due_date_raw, "%Y-%m-%d")
            except ValueError:
                flash("Invalid due date format. Use YYYY-MM-DD.", "error")
                return redirect(url_for("edit_task", task_id=task_id))

        task.title = title
        task.description = description
        task.due_date = due_date
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("tasks"))

    return render_template("edit_task.html", task=task)

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=g.user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks"))

@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=g.user.id).first_or_404()
    task.completed = True
    task.updated_at = datetime.utcnow()
    db.session.commit()
    flash("Task marked complete.", "success")
    return redirect(url_for("tasks"))

# Optional: small API endpoints (JSON) if you want to call from JS or external tools
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid credentials"}, 401
    return {"user_id": user.id, "email": user.email}, 200

@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

# TEMPLATES are expected in the ./templates folder
if __name__ == "__main__":
    # Development server
    app.run(debug=True)

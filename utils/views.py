from flask import (request, Blueprint, redirect, render_template, url_for, 
                  session, flash)
from utils.storage import Storage
import utils.logger as logger
from utils.auth import AuthenticationManager
import uuid
from functools import wraps

views = Blueprint('views', __name__)

# Decorator for login required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("views.login"))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to get user data
def get_user_data():
    username = session.get("username")
    return Storage.load_data(username), username

@views.route('/')
def home():
    if session.get("user_id"):
        data, _ = get_user_data()
        tasks = data.get("tasks", [])
        return render_template("home.html", tasks=tasks)
    return render_template("index.html")
    
@views.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user_id"):
        return redirect(url_for("views.get_tasks"))
        
    if request.method == "GET":
        return render_template("register.html")
    
    # POST method handling
    form = request.form
    username = form.get("username")
    
    if Storage.user_exists(username):
        logger.Error_logger.error(f"Registration failed: Username {username} already exists.")
        return render_template("register.html", error="Username already exists, please choose another")

    # Create new user
    password_hash = AuthenticationManager.hash_pass(password=form.get("password"))
    user_data = Storage.load_data(username)
    
    new_data = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "name": form.get("name"),
        "email": form.get("email"),
        "password_hash": password_hash,
        "tasks": user_data.get("tasks", [])
    }
    
    Storage.save_data(new_data, username)
    logger.Info_logger.info(f"User {username} has registered successfully")
    return redirect(url_for("views.login"))

@views.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for("views.home"))
    
    if request.method == 'GET':
        return render_template("login.html")
    
    # POST method handling
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not Storage.user_exists(username):
        return render_template("login.html", error="Username does not exist")
        
    data = Storage.load_data(username)
    if not AuthenticationManager.compare_pass(password, data["password_hash"]):
        logger.Info_logger.warning(f"Failed login attempt for user: {username}")
        return render_template("login.html", error="Invalid password, try again")
    
    # Set session data
    session["user_id"] = data["user_id"]
    session["username"] = username
    session.permanent = bool(request.form.get("remember", False))
    
    logger.Info_logger.info(f"User {username} has logged in")
    return redirect(url_for("views.get_tasks"))

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    data, username = get_user_data()
    
    if request.method == 'POST':
        # Handle profile updates
        form = request.form
        data["name"] = form.get("name", data.get("name"))
        data["email"] = form.get("email", data.get("email"))
        
        # Handle password change if provided
        if form.get("new_password"):
            if AuthenticationManager.compare_pass(form.get("current_password"), data["password_hash"]):
                data["password_hash"] = AuthenticationManager.hash_pass(form.get("new_password"))
                flash("Password updated successfully")
            else:
                return render_template("profile.html", user=data, error="Current password is incorrect")
        
        Storage.save_data(data, username)
        flash("Profile updated successfully")
        
    return render_template("profile.html", user=data)

@views.route('/logout', methods=['POST'])
def logout():
    if session.get("user_id"):
        username = session.get("username")
        logger.Info_logger.info(f"User {username} has logged out")
        session.clear()
    return redirect(url_for("views.login"))

@views.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    data, _ = get_user_data()
    tasks = data.get("tasks", [])
    return render_template("tasks.html", tasks=tasks)

@views.route('/tasks/add_task', methods=['POST'])
@login_required
def add_task():
    data, username = get_user_data()
    tasks = data.get("tasks", [])
    
    task_name = request.form.get('task_name', '').strip()
    if not task_name:
        return render_template("tasks.html", tasks=tasks, error="Task name cannot be empty")
    
    # Check if task already exists
    if any((task.get("task_name") or "").strip() == task_name for task in tasks):
        return render_template("tasks.html", tasks=tasks, error="Task already exists!")
    
    # Generate a unique task ID
    task_id = max([task.get("id", 0) for task in tasks], default=0) + 1
    
    # Add new task
    new_task = {
        "id": task_id,
        "task_name": task_name,
        "description": request.form.get("description", ""),
        "completed": False
    }
    
    tasks.append(new_task)
    data["tasks"] = tasks
    Storage.save_data(data, username)
    
    logger.Info_logger.info(f"User {username} added task: {task_name}")
    return redirect(url_for("views.get_tasks"))

@views.route("/tasks/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    data, username = get_user_data()
    tasks = data.get("tasks", [])
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    
    data["tasks"] = tasks
    Storage.save_data(data, username)
    logger.Info_logger.info(f"User {username} completed task ID: {task_id}")
    
    return redirect(url_for('views.get_tasks'))

@views.route("/tasks/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    data, username = get_user_data()
    tasks = data.get("tasks", [])
    
    # Find and remove the task
    tasks = [task for task in tasks if task["id"] != task_id]
    
    data["tasks"] = tasks
    Storage.save_data(data, username)
    logger.Info_logger.info(f"User {username} deleted task ID: {task_id}")
    
    return redirect(url_for("views.get_tasks"))
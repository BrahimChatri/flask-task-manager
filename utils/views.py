from flask import(request, Blueprint, redirect, render_template, url_for, session)
from utils.storage import Storage
import utils.logger as logger
from utils.auth import AuthenticationManager
import uuid

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if session.get("user_id"):
        data = Storage.load_data(session["username"])
        
        # Ensure tasks is a list
        tasks = data.get("tasks", [])
        return render_template("home.html", tasks=tasks)  # Render home overview page if logged in
    else:
        return render_template("index.html")
    
@views.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user_id") == None:
        if request.method == "GET":
            return render_template("register.html")
        
        elif request.method == "POST" :
            form= request.form
            user_data =Storage.load_data(form.get("username"))

            if Storage.user_exists(form.get("username")):
                logger.Error_logger.error("Username already exists.")
                return render_template("register.html", error="Username already exists chose other one")

            else :
                password_hash = AuthenticationManager.hash_pass(password=form.get("password"))
                if user_data.get("tasks"):
                    tasks=user_data["tasks"]
                else :
                    tasks=[]
                new_data = {
                    "user_id": str(uuid.uuid4()),
                    "username" : form.get("username"),
                    "name" : form.get("name"),
                    "email": form.get("email"),
                    "password_hash" : password_hash,
                    "tasks" : tasks
                }
                Storage.save_data(new_data, form.get("username"))
                return redirect(url_for("views.login"))
    else:
        return redirect(url_for("views.get_tasks"))
    

@views.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for("views.home"))  # Add return here
    
    elif request.method == 'GET':
        return render_template("login.html")
    
    elif request.method == 'POST':
        username = request.form.get("username")
        
        if Storage.user_exists(username):
            data = Storage.load_data(username)
            
            if AuthenticationManager.compare_pass(request.form.get("password"), data["password_hash"]):
                session["user_id"] = data["user_id"]
                session["username"] = username
                print(f"Logged in as: {session['username']}")  # Debug print to check session

                return redirect(url_for("views.get_tasks"))
            else:
                return render_template("login.html", error="Invalid password, try again")
        else:
            return render_template("login.html", error="Username does not exist")

@views.route('/logout', methods=['POST'])
def logout():
    if session.get("user_id") :
        session.clear()
        return redirect(url_for("views.login"))
    return redirect(url_for("views.login"))

@views.route('/tasks', methods=['GET'])
def get_tasks():
    if session.get("user_id") == None:
        return redirect(url_for("views.login"))
    
    # Fetch user data
    username = session.get("username")
    data = Storage.load_data(username)
    
    # Ensure tasks is a list
    tasks = data.get("tasks")
    
    return render_template("tasks.html", tasks=tasks)



@views.route('/tasks/add_task', methods=['POST'])
def add_task():
    username = session.get("username")
    data = Storage.load_data(username)
    
    # Ensure tasks is a list
    tasks = data.get("tasks", [])
    
    # Check if task already exists
    for task in tasks:
        if task.get("task_name").strip() == request.form.get('task_name'):
            return render_template("tasks.html", error="Task already exists!")
    
    # Add new task
    new_task = {
        "id": len(tasks)+1,
        "task_name": request.form.get('task_name'),
        "description": request.form.get("description"),
        "completed": False
    }
    tasks.append(new_task)
    data["tasks"] = tasks  # Update tasks in the data
    
    # Save the data back
    Storage.save_data(user_data=data, filename=username)
    return redirect(url_for("views.get_tasks"))


@views.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    if session.get("user_id") == None:
        return redirect(url_for("views.login"))
     
    username = session.get("username")
    data =Storage.load_data(username)
    tasks=data["tasks"]
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    data["tasks"] = tasks
    Storage.save_data(data, username)
    return redirect(url_for('views.get_tasks'))

@views.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    username = session.get("username")
    if not username:
        return redirect(url_for("views.login"))

    data = Storage.load_data(username)
    tasks = data.get("tasks", [])

    # Find and remove the task
    tasks = [task for task in tasks if task["id"] != task_id]
    
    # Save updated data
    data["tasks"] = tasks
    Storage.save_data(data, username)

    return redirect(url_for("views.get_tasks"))

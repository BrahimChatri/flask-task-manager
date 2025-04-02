# 📝 Task Manager - Flask (GUI Version)  

A simple **Task Manager** built with **Flask** and **TailwindCSS** that allows users to **register, log in, and manage their tasks** efficiently.  

## 🚀 Features  

✅ **User Authentication** (Register/Login)  
✅ **Add Tasks** with descriptions  
✅ **Mark Tasks as Completed** (removes "Complete" button)  
✅ **Delete Tasks**  
✅ **Session-Based User Management**  
✅ **Beautiful UI** with **TailwindCSS**  

---

## 🛠 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/BrahimChatri/flask-task-manager.git
cd flask-task-manager
```

### 2️⃣ Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask Server  
```bash
python app.py
```
Then, open **http://127.0.0.1:5000** in your browser.

---

## 📂 Project Structure  

```
📂 flask-task-manager
│── 📂 data               # Data storage as json files
│── 📂 templates          # HTML templates (register, login, tasks)
│── 📂 static             # CSS/JS/PNG ... (if needed)
│── 📂 utils              # Storage, Authentication, Logging utilities
│── app.py                # Main Flask application
│── requirements.txt       # Required dependencies
│── README.md              # Documentation (You are here!)
```

---

## 🔑 Authentication System  

- Users **register** with a **username, name, email, and password**.  
- Passwords are **hashed** for security.  
- Users **log in** and can access **their tasks**.  
- Sessions are used to keep users logged in.  

---

## 🖥️ Screenshots

| Login Page           | Register Page        |
|----------------------|----------------------|
| ![Login](./static/login.png) | ![Register](./static/register.png) |

| Home Page            | Task Dashboard       |
|----------------------|----------------------|
| ![Home](./static/home.png)   | ![Tasks](./static/tasks.png)   |

## 🛠 Tech Stack  

🔹 **Flask** (Backend)  
🔹 **TailwindCSS** (Frontend)  
🔹 **Session-based Authentication**  
🔹 **Local Storage (JSON-based)**  

---

## 📌 Future Improvements  

- ✅ Add Due Dates  
- ✅ User Profiles  
- ✅ Task Priorities  

---

## 💡 Contributing  

Feel free to **fork this repo** and submit a **pull request** if you'd like to improve the project! 🚀  

---

## 📜 License  

This project is licensed under the **MIT License**.  

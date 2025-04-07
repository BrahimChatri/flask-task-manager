from flask import Flask, render_template
from utils.views import views
from dotenv import load_dotenv
import os
from datetime import timedelta


load_dotenv()

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
KEY = os.getenv("KEY")

app.config['SECRET_KEY'] = KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Auto-expire after 1 day

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__=='__main__':
    app.run(port="5000", debug=True, host="0.0.0.0")
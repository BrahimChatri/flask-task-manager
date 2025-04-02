from flask import Flask
from utils.views import views
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
KEY = os.getenv("KEY")

app.config['SECRET_KEY'] = KEY

if __name__=='__main__':
    app.run(port="5000", host="0.0.0.0")
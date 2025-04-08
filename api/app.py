# from flask import Flask, render_template
# from dotenv import load_dotenv
# import os, sys
# from datetime import timedelta
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from utils.views import views

# load_dotenv()

# app = Flask(__name__, template_folder='templates', static_folder='static')
# app.register_blueprint(views, url_prefix='/')

# app.config['SECRET_KEY'] = os.getenv("KEY")
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("404.html"), 404

# # Vercel requires this as handler
# handler = app

# # if __name__ == "__main__":
# #     app.run(debug=True)
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Vercel!"

# Add your other routes and application logic here

# This is the Vercel serverless function handler
app.debug = True

# Important: This makes the app compatible with Vercel
def app_handler(request):
    return app(request['headers'], request.get('body', ''))

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
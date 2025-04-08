from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os, sys
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.views import views

load_dotenv()

# Check if templates directory exists and is accessible
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

app.register_blueprint(views, url_prefix='/')

app.config['SECRET_KEY'] = os.getenv("KEY", "fallback-secret-key")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

@app.errorhandler(404)
def not_found(e):
    # Fallback to a simple JSON response if template isn't found
    try:
        return render_template("404.html"), 404
    except:
        return jsonify({"error": "Not found", "status": 404}), 404

app.debug = True

# For Vercel - don't modify this part
def app_handler(request):
    return app

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
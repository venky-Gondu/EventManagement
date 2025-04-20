import sys
import os
from flask_cors import CORS  # type: ignore # Correct import for Flask-CORS
from flask import Flask
from flask_session import Session  # type: ignore # Correct import for Flask sessions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Management import Management_blueprint
from src.auth import auth
from src.event import event_blueprint

app = Flask(__name__)
CORS(app,supports_credentials=True)  # Enable CORS for all routes
app.secret_key = "987##"  # Used for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
app.config['SESSION_PERMANENT'] = False  # Optional: Make sessions non-permanent
Session(app)  # Initialize Flask-SessionSession(app)  # Initialize Flask-Session

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(event_blueprint, url_prefix='/event')
app.register_blueprint(Management_blueprint, url_prefix='/management')  

if __name__ == "__main__":
    app.run( host="0.0.0.0",port=5000,debug=True)  # Run the Flask app in debug mode

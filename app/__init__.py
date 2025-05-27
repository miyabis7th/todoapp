import os
from flask import Flask
from google.cloud import firestore

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    
    # Ensure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize Firestore client
    db = firestore.Client()
    
    # Make db accessible to other modules
    app.db = db
    
    # Register routes
    from app import routes
    
    return app
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
    
    # Initialize Firestore client (only in production/Cloud Run)
    try:
        from google.cloud import firestore
        db = firestore.Client()
        print("Firestore client initialized successfully")
    except Exception as e:
        print(f"Firestore initialization failed: {e}")
        # Use a mock database for local development
        db = None
    
    # Make db accessible to other modules
    app.db = db
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    return app
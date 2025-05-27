# Todo Application

A modern Todo management application with Instagram-like UI, built with Flask and Google Cloud services.

[![Deploy Status](https://img.shields.io/badge/deploy-active-brightgreen)](https://todoapp-129496739028.asia-northeast1.run.app/)

## Features

- Task management (Create, Read, Update, Delete)
- Task completion tracking
- Image upload functionality
- Modern, Instagram-like UI
- Cloud Firestore integration for data storage
- Deployed on Google Cloud Run

## Technology Stack

- **Backend**: Python with Flask
- **Database**: Google Cloud Firestore
- **Deployment**: Google Cloud Run
- **CI/CD**: GitHub Actions
- **Container Registry**: Google Artifact Registry

## Development Setup

1. Clone this repository
   ```
   git clone https://github.com/miyabis7th/todoapp.git
   cd todoapp
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up Google Cloud Firestore
   - Create a project in Google Cloud Console
   - Enable Firestore API
   - Create service account credentials
   - Download service account key JSON file

5. Set environment variables
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-account-key.json"
   ```

6. Run the application
   ```
   python main.py
   ```

7. Access the application at http://localhost:8080

## CI/CD Pipeline

The application includes a GitHub Actions workflow that automatically:
- Builds a Docker image
- Pushes the image to Google Artifact Registry
- Deploys the application to Google Cloud Run

### Required GitHub Secrets

- `GCP_SERVICE_ACCOUNT_KEY`: JSON key for GCP service account
- `GCP_PROJECT_ID`: Google Cloud project ID
- `GCP_SERVICE_NAME`: Name for the Cloud Run service
- `GCP_ARTIFACT_REGISTRY_REPO_NAME`: Name for the Artifact Registry repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.
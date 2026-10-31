from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml_service.models import (
    CHDIComputeRequest,
    CHDIComputeResponse,
    RetrainRequest,
    RetrainResponse
)
from ml_service.chdi import compute_chdi_pipeline
from ml_service.classifier import feedback_model

app = FastAPI(
    title="SmartCattle Python Machine Learning Microservice",
    description="Dedicated mathematical and machine learning analytics pipeline implementing the Three-Stage Composite Health Deviation Index (CHDI) for IEEE Conference Paper.",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SmartCattle-ML-Microservice",
        "version": "1.0.0",
        "engine": "SciPy + NumPy + Scikit-learn",
        "classifier_trained": feedback_model.is_trained
    }

@app.post("/api/v1/chdi/compute", response_model=CHDIComputeResponse)
def compute_chdi_endpoint(request: CHDIComputeRequest):
    """
    Computes Stage 1 Baseline, Stage 2 Mahalanobis Anomaly Distance, and Stage 3 LOCO Feature Attribution.
    """
    try:
        response = compute_chdi_pipeline(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CHDI calculation error: {str(e)}")

@app.post("/api/v1/classifier/retrain", response_model=RetrainResponse)
def retrain_classifier_endpoint(request: RetrainRequest):
    """
    Retrains the Stage 3 Scikit-learn RandomForestClassifier on verified VetFeedback records.
    """
    try:
        res = feedback_model.train(request.samples)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classifier training error: {str(e)}")

@app.get("/api/v1/classifier/metrics")
def get_classifier_metrics():
    """
    Returns current classification precision, recall, and F1-score for the admin dashboard.
    """
    return feedback_model.metrics

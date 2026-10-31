import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from typing import List, Dict, Any, Optional
from ml_service.models import VetFeedbackSample, RetrainResponse

class VetFeedbackModel:
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=6)
        self.is_trained = False
        self.classes: List[str] = []
        self.metrics = {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "sample_count": 0
        }

    def train(self, samples: List[VetFeedbackSample]) -> RetrainResponse:
        if len(samples) < 5:
            return RetrainResponse(
                status="insufficient_data",
                accuracy=0.0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                sample_count=len(samples),
                classes=[]
            )

        X = []
        y = []

        feature_keys = ["milkDeviation", "ruminationDeviation", "temperatureDeviation", "activityDeviation", "feedDeviation", "weightDeviation"]

        for s in samples:
            row = [s.score, s.confidence]
            for k in feature_keys:
                row.append(s.deviations.get(k, 0.0))
            X.append(row)
            y.append(s.confirmed_outcome)

        X_mat = np.array(X, dtype=float)
        y_vec = np.array(y, dtype=str)

        self.clf.fit(X_mat, y_vec)
        self.is_trained = True
        self.classes = list(self.clf.classes_)

        # Internal cross-prediction metrics
        y_pred = self.clf.predict(X_mat)
        acc = float(accuracy_score(y_vec, y_pred))
        p, r, f1, _ = precision_recall_fscore_support(y_vec, y_pred, average="weighted", zero_division=0)

        self.metrics = {
            "accuracy": round(acc, 4),
            "precision": round(float(p), 4),
            "recall": round(float(r), 4),
            "f1_score": round(float(f1), 4),
            "sample_count": len(samples)
        }

        return RetrainResponse(
            status="trained",
            accuracy=self.metrics["accuracy"],
            precision=self.metrics["precision"],
            recall=self.metrics["recall"],
            f1_score=self.metrics["f1_score"],
            sample_count=len(samples),
            classes=self.classes
        )

# Global singleton
feedback_model = VetFeedbackModel()

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class PerformancePredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'models/predictor_model.pkl')
        self.load_model()
    
    def load_model(self):
        """Load trained model or create new one"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            # Train with initial data
            self.train_initial_model()
    
    def train_initial_model(self):
        """Train initial model with synthetic data"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic features
        engagement = np.random.uniform(0.1, 1.0, n_samples)
        quiz_avg = np.random.uniform(40, 95, n_samples)
        topic_mastery = np.random.uniform(0.2, 1.0, n_samples)
        consistency = np.random.uniform(0.3, 0.9, n_samples)
        
        # Generate target scores
        final_score = (
            engagement * 30 +
            quiz_avg * 0.5 +
            topic_mastery * 20 +
            consistency * 10 +
            np.random.normal(0, 5, n_samples)
        )
        final_score = np.clip(final_score, 0, 100)
        
        # Prepare data
        X = np.column_stack([engagement, quiz_avg, topic_mastery, consistency])
        y = final_score
        
        # Train model
        self.model.fit(X, y)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
    
    def extract_features(self, student_data):
        """Extract features from student data"""
        # Mock feature extraction - replace with actual logic
        engagement = student_data.get('engagement_score', 0.5)
        quiz_avg = student_data.get('average_quiz_score', 70)
        topic_mastery = student_data.get('average_mastery', 0.6)
        consistency = student_data.get('consistency_score', 0.7)
        
        return np.array([[engagement, quiz_avg, topic_mastery, consistency]])
    
    def predict(self, student_data):
        """Predict student performance"""
        features = self.extract_features(student_data)
        prediction = self.model.predict(features)[0]
        
        # Calculate confidence
        confidence = 95 - abs(prediction - 50) * 0.5
        confidence = max(70, min(99, confidence))
        
        return {
            'predicted_score': round(prediction, 1),
            'confidence_interval': [
                round(prediction - 5, 1),
                round(prediction + 5, 1)
            ],
            'confidence': round(confidence, 1)
        }
    
    def assess_risk(self, predicted_score):
        """Assess risk level based on predicted score"""
        if predicted_score >= 80:
            return 'low'
        elif predicted_score >= 60:
            return 'medium'
        else:
            return 'high'
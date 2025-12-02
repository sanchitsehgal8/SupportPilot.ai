"""ML Predictor - sentiment analysis and priority prediction"""
from backend.ml.preprocessor import MLPreprocessor
from typing import Dict, Tuple
import os
import joblib


class SentimentAnalyzer:
    """Analyzes sentiment of ticket descriptions"""
    
    def __init__(self):
        self.preprocessor = MLPreprocessor()
        model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model.pkl')
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print("[SentimentAnalyzer] Loaded trained model")
            except Exception as e:
                print(f"[SentimentAnalyzer] Failed to load model: {e}")
        
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        Returns: {'score': 0.0-1.0, 'label': 'positive'|'neutral'|'negative'}
        """
        if not text:
            return {'score': 0.5, 'label': 'neutral'}
        
        # Use trained model if available
        if self.model:
            try:
                label = self.model.predict([text])[0]
                proba = self.model.predict_proba([text])[0]
                score = max(proba)
                return {'score': round(float(score), 3), 'label': str(label)}
            except Exception as e:
                print(f"[SentimentAnalyzer] Model prediction failed: {e}")
        
        # Fallback: Simple heuristic-based sentiment analysis
        cleaned_text = self.preprocessor.clean_text(text)
        tokens = self.preprocessor.tokenize(cleaned_text)
        
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'happy', 'satisfied', 'love', 'awesome', 'perfect', 'best',
            'thank', 'thanks', 'appreciate', 'helpful', 'fixed', 'solved'
        }
        
        negative_words = {
            'bad', 'poor', 'awful', 'terrible', 'horrible', 'hate', 'angry',
            'frustrated', 'disappointed', 'broken', 'crash', 'error', 'problem',
            'issue', 'trouble', 'worst', 'useless', 'waste', 'fail'
        }
        
        positive_count = sum(1 for token in tokens if token in positive_words)
        negative_count = sum(1 for token in tokens if token in negative_words)
        
        total = len(tokens)
        if total == 0:
            return {'score': 0.5, 'label': 'neutral'}
        
        # Calculate sentiment score (0-1)
        score = (positive_count - negative_count) / total
        score = max(0, min(1, (score + 1) / 2))  # Normalize to 0-1 range
        
        # Determine label
        if score > 0.6:
            label = 'positive'
        elif score < 0.4:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {'score': round(score, 3), 'label': label}


class PriorityPredictor:
    """Predicts ticket priority level"""
    
    def __init__(self):
        self.preprocessor = MLPreprocessor()
        model_path = os.path.join(os.path.dirname(__file__), 'priority_model.pkl')
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print("[PriorityPredictor] Loaded trained model")
            except Exception as e:
                print(f"[PriorityPredictor] Failed to load model: {e}")
        
    def predict_priority(self, ticket_text: str, sentiment_score: float = 0.5) -> str:
        """
        Predict priority: 'low', 'medium', 'high', 'urgent'
        Based on text content and sentiment
        """
        if not ticket_text:
            return 'medium'
        
        # Use trained model if available
        if self.model:
            try:
                priority = self.model.predict([ticket_text])[0]
                return str(priority).lower()
            except Exception as e:
                print(f"[PriorityPredictor] Model prediction failed: {e}")
        
        # Fallback: heuristic-based
        cleaned_text = self.preprocessor.clean_text(ticket_text).lower()
        
        # Urgent keywords
        urgent_keywords = {
            'urgent', 'critical', 'emergency', 'asap', 'immediately',
            'down', 'crash', 'broken', 'not working', 'severe',
            'error', 'failed', 'account locked', 'data loss'
        }
        
        # High priority keywords
        high_keywords = {
            'important', 'urgent', 'issue', 'problem', 'impact',
            'business', 'customer', 'revenue', 'significant'
        }
        
        # Check for urgent indicators
        for keyword in urgent_keywords:
            if keyword in cleaned_text:
                return 'urgent'
        
        # Check for high priority indicators
        for keyword in high_keywords:
            if keyword in cleaned_text:
                return 'high'
        
        # Use sentiment to adjust priority
        if sentiment_score < 0.3:  # Very negative
            return 'high'
        elif sentiment_score < 0.4:  # Negative
            return 'medium'
        else:
            return 'low'


class KeywordExtractor:
    """Extracts keywords from ticket descriptions"""
    
    def __init__(self):
        self.preprocessor = MLPreprocessor()
        
    def extract(self, text: str, num_keywords: int = 5) -> list:
        """Extract top keywords from text"""
        return self.preprocessor.extract_keywords(text, num_keywords)

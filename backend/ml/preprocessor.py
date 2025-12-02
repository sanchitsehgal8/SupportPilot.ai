"""ML Preprocessor - text preprocessing for ML models"""
import re
from typing import List
import string


class MLPreprocessor:
    """Handles text preprocessing for ML models"""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
        
    def _load_stopwords(self) -> set:
        """Load common English stopwords"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'it', 'its', 'this', 'that'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        text = self.clean_text(text)
        return text.split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from token list"""
        return [token for token in tokens if token not in self.stopwords]
    
    def preprocess(self, text: str) -> List[str]:
        """Full preprocessing pipeline"""
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        return tokens
    
    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """Extract top keywords using TF-IDF concept"""
        tokens = self.preprocess(text)
        
        if not tokens:
            return []
        
        # Simple frequency-based keyword extraction
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_freq[:num_keywords]]

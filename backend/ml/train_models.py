"""Train simple ML models and save them as pickles"""
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib


def train_and_save_models(data_path: str, out_dir: str):
    df = pd.read_csv(data_path)
    texts = df['text'].fillna('')
    labels = df['label'].fillna('neutral')
    priorities = df['priority'].fillna('medium')
    
    os.makedirs(out_dir, exist_ok=True)
    
    # Sentiment model (labels: positive/neutral/negative)
    sentiment_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=1000)),
        ('clf', MultinomialNB())
    ])
    sentiment_pipeline.fit(texts, labels)
    joblib.dump(sentiment_pipeline, os.path.join(out_dir, 'sentiment_model.pkl'))
    
    # Priority model (low/medium/high/urgent)
    priority_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=1000)),
        ('clf', MultinomialNB())
    ])
    priority_pipeline.fit(texts, priorities)
    joblib.dump(priority_pipeline, os.path.join(out_dir, 'priority_model.pkl'))
    
    print('Models trained and saved to', out_dir)


if __name__ == '__main__':
    train_and_save_models(os.path.join(os.path.dirname(__file__), 'sample_dataset.csv'), os.path.dirname(__file__))

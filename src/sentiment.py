from transformers import pipeline
import pandas as pd
from src.config import SENTIMENT_MODEL, NEUTRAL_THRESHOLD

# Global variable to load model once
_sentiment_model = None

def get_model():
    """Load model once and reuse"""
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
    return _sentiment_model

def classify_review(text):
    """Classify a single review"""
    model = get_model()
    result = model(text[:512])[0]
    label = result['label'].lower()
    confidence = result['score']
    
    # Add neutral category
    if confidence < NEUTRAL_THRESHOLD:
        return 'neutral', confidence
    return label, confidence

def add_sentiment_to_df(df, text_column='review'):
    """Add sentiment columns to dataframe"""
    sentiments = []
    confidences = []
    
    for text in df[text_column]:
        sent, conf = classify_review(text)
        sentiments.append(sent)
        confidences.append(conf)
    
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = confidences
    return df

def aggregate_by_bank(df):
    """Get sentiment distribution by bank"""
    return df.groupby('bank')['sentiment_label'].value_counts(normalize=True).unstack() * 100

def aggregate_by_rating(df):
    """Get sentiment distribution by rating"""
    results = {}
    for rating in [1,2,3,4,5]:
        rating_df = df[df['rating'] == rating]
        if len(rating_df) > 0:
            results[rating] = rating_df['sentiment_label'].value_counts(normalize=True).to_dict()
    return results
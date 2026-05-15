# Model settings
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
NEUTRAL_THRESHOLD = 0.70

# File paths
INPUT_PATH = "data/processed/reviews.csv"
OUTPUT_PATH = "data/processed/reviews_with_sentiment.csv"

# Batch size for processing
BATCH_SIZE = 100
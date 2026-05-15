import pandas as pd
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clean_reviews(df):
    """
    Clean and preprocess reviews DataFrame
    
    Parameters:
        df: DataFrame with raw reviews
    
    Returns:
        Cleaned DataFrame with 5 required columns
    """
    print(f"\n Starting preprocessing...")
    print(f"   Initial reviews: {len(df)}")
    
    # 1. Remove duplicates using review_id
    before = len(df)
    if 'review_id' in df.columns:
        df = df.drop_duplicates(subset=['review_id'])
        print(f"   1. Removed {before - len(df)} duplicate reviews")
    
    # 2. Remove missing values
    before = len(df)
    df = df.dropna(subset=['review', 'rating'])
    df = df[df['review'].str.strip() != '']
    print(f"   2. Removed {before - len(df)} rows with missing data")
    
    # 3. Validate ratings (1-5)
    before = len(df)
    df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
    df['rating'] = df['rating'].astype(int)
    print(f"   3. Removed {before - len(df)} invalid ratings")
    
    # 4. Normalize dates
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    print(f"   4. Normalized dates to YYYY-MM-DD")
    
    # 5. Select only required columns
    df = df[['review', 'rating', 'date', 'bank', 'source']]
    print(f"   5. Selected required columns")
    
    print(f"\n Preprocessing complete: {len(df)} clean reviews")
    print(f"   Retention rate: {len(df)/before*100:.1f}%")
    
    return df

def load_raw_data(input_path='data/raw/scraped_reviews.csv'):
    """Load raw scraped data"""
    if os.path.exists(input_path):
        print(f" Loading raw data from {input_path}")
        return pd.read_csv(input_path)
    else:
        print(f" Raw data file not found: {input_path}")
        print("   Please run scrape_reviews.py first")
        return None

def save_cleaned_data(df, output_path='data/processed/reviews.csv'):
    """Save cleaned data"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    file_size = os.path.getsize(output_path) / 1024
    print(f" Cleaned data saved to: {output_path}")
    print(f"   File size: {file_size:.1f} KB")
    print(f"   Reviews: {len(df)}")
    print(f"   Columns: {', '.join(df.columns)}")
    
    return output_path

def generate_report(df):
    """Generate preprocessing report"""
    print("\n" + "="*50)
    print("PREPROCESSING REPORT")
    print("="*50)
    
    print(f"\n Final Dataset Summary:")
    print(f"   Total reviews: {len(df)}")
    print(f"   Banks: {', '.join(df['bank'].unique())}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Rating range: {df['rating'].min()} to {df['rating'].max()}")
    
    print(f"\n Reviews per bank:")
    for bank in df['bank'].unique():
        count = len(df[df['bank'] == bank])
        print(f"   {bank}: {count} reviews")
    
    print(f"\n Rating distribution:")
    for rating in sorted(df['rating'].unique(), reverse=True):
        count = len(df[df['rating'] == rating])
        pct = count / len(df) * 100
        bar = '█' * int(pct / 2)
        print(f"   {rating}★: {count:4} ({pct:5.1f}%) {bar}")
    
    return df

def main():
    """Main preprocessing workflow"""
    print("="*50)
    print("TASK 1: DATA PREPROCESSING")
    print("="*50)
    
    # Load raw data
    df = load_raw_data()
    if df is None:
        return None
    
    # Clean data
    df_cleaned = clean_reviews(df)
    
    # Generate report
    generate_report(df_cleaned)
    
    # Save cleaned data
    save_cleaned_data(df_cleaned)
    
    print("\n Task 1 preprocessing complete!")
    return df_cleaned

if __name__ == "__main__":
    result = main()
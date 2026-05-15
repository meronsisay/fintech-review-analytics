
from google_play_scraper import reviews, Sort
import pandas as pd
import time
from datetime import datetime
import os
import sys

# Add parent directory to path (for when running as script)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Bank app IDs (verified working)
BANK_APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

def scrape_bank_reviews(app_id, bank_name, target_count=450):
    """
    Scrape reviews for a single bank
    
    Args:
        app_id: Google Play app ID
        bank_name: Name of the bank
        target_count: Number of reviews to scrape
    
    Returns:
        DataFrame with scraped reviews
    """
    print(f"\n Scraping {bank_name}...")
    print(f"   App ID: {app_id}")
    print(f"   Target: {target_count} reviews")
    
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=target_count
        )
        
        print(f"  Got {len(result)} raw reviews")
        
        reviews_data = []
        for review in result:
            reviews_data.append({
                'review_id': review['reviewId'],
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            })
        
        return pd.DataFrame(reviews_data)
        
    except Exception as e:
        print(f"  Error: {e}")
        return pd.DataFrame()

def scrape_all_banks():
    """Scrape all three banks and return combined DataFrame"""
    print("="*60)
    print("SCRAPING ALL BANKS")
    print("="*60)
    
    all_reviews = []
    
    for i, (bank_name, app_id) in enumerate(BANK_APPS.items(), 1):
        df = scrape_bank_reviews(app_id, bank_name, target_count=450)
        
        if not df.empty:
            all_reviews.append(df)
            print(f"    Added {len(df)} reviews from {bank_name}")
        else:
            print(f"   Failed to get reviews from {bank_name}")
        
        # Wait between requests (except after last)
        if i < len(BANK_APPS):
            print("   Waiting 3 seconds...")
            time.sleep(3)
    
    if not all_reviews:
        print("\nNo reviews collected!")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_reviews, ignore_index=True)
    print(f"\n Total collected: {len(combined_df)} reviews")
    print(f"   Per bank:\n{combined_df['bank'].value_counts()}")
    
    return combined_df

def save_raw_data(df, output_path='data/raw/scraped_reviews.csv'):
    """Save raw scraped data"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f" Raw data saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Starting scraping process...")
    df = scrape_all_banks()
    
    if not df.empty:
        save_raw_data(df)
        print(f"\n Scraping complete! {len(df)} total reviews")
    else:
        print("\n Scraping failed!")
## Scraping Methodology

### Data Collection
- **Tool**: google-play-scraper Python library
- **Approach**: Jupyter notebook for iterative development and data exploration
- **Target Banks**: CBE, Bank of Abyssinia (BOA), Dashen Bank
- **App IDs Used**:
  - CBE: `com.combanketh.mobilebanking`
  - BOA: `com.boa.boaMobileBanking`
  - Dashen: `com.dashen.dashensuperapp`
- **Parameters**:
  - Language: English (`lang='en'`)
  - Country/Region: Ethiopia (`country='et'`)
  - Sort order: Newest first (`sort=Sort.NEWEST`)
  - Rate limiting: 3-second delay between requests

### Date Range
- **Scraping Date**: May 15, 2025
- **Reviews Date Range**: 2025-04-04 to 2026-05-14
- **Time Period Covered**:  405 days (approximately 13.5 months)

### Data Collected
- **Total Reviews**: 1,350 (450 per bank)
- **Fields**: review text, rating (1-5), date, bank name, source

### Limitations
1. **Language**: Only English-language reviews were collected
2. **Region**: Limited to Ethiopian Google Play store
3. **Review Limit**: Only reviews available through Google Play API (no pagination beyond ~450)
4. **App ID Validation**: App IDs were verified manually through Google Play Store
5. **Rate Limits**: Delays added to prevent API throttling

### Preprocessing Steps
1. Removed technical duplicates using `review_id`
2. Dropped rows with missing review text or rating
3. Filtered invalid ratings (outside 1-5 range)
4. Normalized dates to YYYY-MM-DD format
5. Cleaned review text (removed extra spaces, newlines)
6. Final dataset: 1,350 reviews, 5 columns

### Output
- **File**: `data/processed/reviews.csv`
- **Format**: CSV with columns: `review`, `rating`, `date`, `bank`, `source`
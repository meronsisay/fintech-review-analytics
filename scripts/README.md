## Scraping Methodology

**Tool**: google-play-scraper  
**Date**: May 15, 2026  
**Reviews Range**: April 4, 2025 - May 14, 2026 (405 days)  

**App IDs:**
- CBE: `com.combanketh.mobilebanking`
- BOA: `com.boa.boaMobileBanking`
- Dashen: `com.dashen.dashensuperapp`

**Parameters:**
- Language: English (`lang='en'`)
- Region: Ethiopia (`country='et'`)
- Sort: Newest first
- Delay: 3 seconds between requests

**Results:**
- Total: 1,350 reviews (450 per bank)
- Fields: review, rating, date, bank, source
- Missing data: 0%

**Limitations:**
- English reviews only
- Ethiopian store only
- Max ~450 reviews per app

## How to Run Task 1

```bash
pip install -r requirements.txt
python scripts/scrape_reviews.py
python scripts/preprocess.py
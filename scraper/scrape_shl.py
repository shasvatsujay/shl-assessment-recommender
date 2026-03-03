import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import json

print("Loading initial catalog...")
df = pd.read_csv("scraper/shl_catalog.csv")

detailed_data = []
headers = {"User-Agent": "Mozilla/5.0"}

print(f"Starting deep scrape of {len(df)} products. This will take a few minutes...")

# The exact categories specified in the assignment document
valid_test_types = [
    "Ability & Aptitude", "Biodata & Situational Judgement", "Competencies", 
    "Development & 360", "Assessment Exercises", "Knowledge & Skills", 
    "Personality & Behavior", "Simulations"
]

for index, row in df.iterrows():
    url = row['url']
    name = row['name']
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=' ', strip=True)
        
        # 1. Description: Grab from meta tag, fallback to name
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"].strip() if meta_desc else name
        
        # 2. Duration (Integer): Look for numbers near "minutes" or "max"
        duration_match = re.search(r'max\s*(\d+)|(\d+)\s*minutes?', text, re.IGNORECASE)
        duration = int(duration_match.group(1) or duration_match.group(2)) if duration_match else 15
        
        # 3. Test Type (List of Strings): Check page text against the 8 valid SHL categories
        test_types = [t for t in valid_test_types if t.lower() in text.lower()]
        if not test_types:
            test_types = ["Knowledge & Skills"] # Safe default if missing
            
        # 4. Remote & Adaptive Support (Yes/No String)
        remote_support = "Yes" if "remote" in text.lower() else "No"
        adaptive_support = "Yes" if "adaptive" in text.lower() else "No"
        
        detailed_data.append({
            "name": name,
            "url": url,
            "description": description,
            "duration": duration,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "test_type": json.dumps(test_types) # Store as JSON string for the API
        })
        
    except Exception as e:
        # Fallback to keep the pipeline moving if a single URL times out
        detailed_data.append({
            "name": name,
            "url": url,
            "description": name,
            "duration": 15,
            "remote_support": "Yes",
            "adaptive_support": "No",
            "test_type": json.dumps(["Knowledge & Skills"])
        })
        
    if (index + 1) % 50 == 0:
        print(f"Processed {index + 1}/{len(df)}...")
        
    time.sleep(0.2) # Polite delay to avoid getting blocked

detailed_df = pd.DataFrame(detailed_data)
detailed_df.to_csv("scraper/shl_catalog_detailed.csv", index=False)
print("\n✅ Deep scraping complete! Saved as scraper/shl_catalog_detailed.csv")
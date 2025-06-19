import requests
import time
import datetime
import pandas as pd
from states import aus_state_dict, us_state_dict, state_subreddits

flu_keywords = ["flu"]

# dates should be YYYY-MM-DD

def reddit(country, state, start, end):
    if country == "aus":
        states = aus_state_dict()
    else:
        states = us_state_dict()

    sub = state_subreddits[state]

    base_url = "https://arctic-shift.photon-reddit.com/api/posts/search"

    for keyword in flu_keywords:
        url = base_url + "&subreddit=" + sub + "&after=" + start + "&before=" + end + "&query=" + keyword + "&limit=50"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", [])
            print(f"{len(data)} posts found for {sub} - {keyword}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from {sub} with keyword {keyword}: {e}")

        


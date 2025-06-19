import requests
import time
import datetime
import pandas as pd
import os, sys
import random

path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)

from states import aus_state_dict, us_state_dict, state_subreddits


flu_keywords = ["flu"]

# dates should be YYYY-MM-DD

def reddit(country, state, start, end):
    # if country == "aus":
    #     states = aus_state_dict()
    # else:
    #     states = us_state_dict()

    sub = state_subreddits[state]

    base_url = "https://arctic-shift.photon-reddit.com/api/posts/search"

    for keyword in flu_keywords:
        url = base_url + "?subreddit=" + sub + "&after=" + start + "&before=" + end + "&query=" + keyword + "&limit=50"
        posts = []
        post_count = 0

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", [])
            post_count = len(data)

            for post in data:
                text = post.get("selftext", "").strip()[:100]
                if text and text != "[removed]":
                    posts.append(text)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from {sub} with keyword {keyword}: {e}")

        print(state + " " + start + " " + end)
        print("Num of Posts: " + str(post_count) + "\nPost Samples:")

        if len(posts) < 3:
            for post in posts:
                print(post)
        else:
            for i in range (0,3):
                print(posts[i])

# REMOVE testing
reddit("us", "California", "2024-01-01", "2025-01-01")
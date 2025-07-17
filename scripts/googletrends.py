from pytrends.request import TrendReq
import pandas
import sys, os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from serpapi import GoogleSearch

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import add_trend, get_state, add_many_trend
from states import aus_state_dict, us_state_dict, trends_aus_states, trends_us_states, aus_states, us_states

load_dotenv()
api_key = os.getenv("SERPAPIKEY")

def convert_trend_to_text(num):
    if num == 0:
        return "Not searched for"
    elif num >= 1 and num < 25:
        return "Low frequency"
    elif num >= 25 and num < 50:
        return "Moderate frequency"
    elif num >= 50 and num < 75:
        return "High frequency"
    else:
        return "Very high frequency"

def trends(country, state, start, end):
    if country == "aus":
        states = aus_state_dict()
        code = trends_aus_states[state]
    else:
        states = us_state_dict()
        code = trends_us_states[state]

    # date is in the formate yyyy-mm-dd
    date = start + " " + end

    params = {
        "api_key": api_key,
        "engine": "google_trends",
        "q": "flu",
        "geo": code,
        "date": date,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    data = results.get("interest_over_time", [])
    data = data["timeline_data"]

    records = []

    for week in data:
        end_date = datetime.fromtimestamp(int(week["timestamp"])) + timedelta(weeks=1)
        trend_num = week["values"][0]["extracted_value"]
        trend_text = convert_trend_to_text(trend_num)

        records.append({
            "StateID": states[state],
            "EndDate": end_date,
            "Trend": trend_text
        })

    records_df = pandas.DataFrame(records)
    add_many_trend(records_df)
    print("done " + state)

us = ["Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
for state in us:
    trends("us", state, "2016-01-01", "2024-12-01")
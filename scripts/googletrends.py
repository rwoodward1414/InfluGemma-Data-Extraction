from pytrends.request import TrendReq
import pandas
import sys, os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()
api_key = os.getenv("SERPAPIKEY")

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)
from datebase_update import add_trend, get_state, add_many_trend
from states import aus_state_dict, us_state_dict, trends_aus_states, trends_us_states

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

    params = {
        "api_key": api_key,
        "engine": "google_trends",
        "q": "flu",
        "geo": code,
        "date": "2013-01-01 2016-01-01",
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



trends("aus", "VIC", "test", "test")



# pytrends = TrendReq(hl='en-US', tz=360)

# def get_new_trends(country, state, end_date):

#     start_date = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(14)
#     start = start_date.strftime('%Y-%m-%d')
#     timeframe = start + " " + end_date
#     location = country + "-" + state

#     kw_list = ["flu", "influenza"]
#     pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=location, gprop='')
#     data = pytrends.interest_over_time()

#     df = data
#     del df["isPartial"]
#     one_end_date = df.iloc[7, 0]
#     print(one_end_date)
#     week_one = df.iloc[0:7, :]
#     week_one_mean = week_one.values.mean()
#     week_two = df.iloc[7:14, :]
#     week_two_mean = week_two.values.mean()

#     week_one_trend = convert_trend_to_text(week_one_mean)
#     week_two_trend = convert_trend_to_text(week_two_mean)

#     print(week_one_trend)
#     print(week_two_trend)
    
#     # state_id = get_state(state)
#     # add_trend(state_id, one_end_date, week_one_trend)
#     # add_trend(state_id, end_date, week_two_trend)




# get_new_trends("AU", "VIC", "2023-02-22")
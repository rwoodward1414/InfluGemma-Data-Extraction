from datetime import datetime, timedelta
import os, sys
import random
import pandas


path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../../sick-post-classifier/classify/posts.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../../sick-post-classifier/classify_posts.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import get_fortnight_surv, get_trend, get_post_perc, add_post_perc, get_region, get_state_demo
from states import aus_state_dict, us_state_dict, aus_states, us_states
from sarima import sarima_forecast
from posts import gather_posts
from classify_posts import classify_flu_posts
        

# Country : us or aus
# State : Full US name, Initals Aus
# Start date : yyyy-mm-dd
def generate_prompt(country, state, date, output_path):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=15)

    state_id = 0

    if country == "aus":
        states = aus_state_dict()
        state_id = states[state]
        region = "aus"
        region_id = 0
    elif country == "us":
        states = us_state_dict()
        state_id = states[state]
        region_id = get_region(state_id)
    else:
        print("Invalid country")
        return None
    
    demo = get_state_demo(state_id)[0]

    print("Getting info from DB")
    four_weeks_ago = start - timedelta(days=29)
    two_weeks_ago = start - timedelta(days=15)
    four_weeks = get_fortnight_surv(state_id, four_weeks_ago)[0]
    two_weeks = get_fortnight_surv(state_id, two_weeks_ago)[0]
    current = get_fortnight_surv(state_id, start)[0]
    trend = get_trend(state_id, start)[0]
    print("Classifying posts")
    flu_post_percent = get_post_perc(region_id, start)
    if flu_post_percent == None:
        posts = gather_posts(country, region_id, date)
        flu_post_percent = classify_flu_posts(posts)
        flu_post_percent = round(flu_post_percent, 3)
        add_post_perc(region_id, start, flu_post_percent)
    else:
        flu_post_percent = flu_post_percent[0]
    
    print("Calculating SARIMA")
    sarima_output = sarima_forecast(state_id, date)

    print("Creating prompt")

    actual_cases = get_fortnight_surv(state_id, end)[0]
    actual_trend = ""

    curr_per_hundthou = (current / float(demo[0])) * 100000
    actual_per_hundthou = (actual_cases / float(demo[0])) * 100000

    change_per_hundthou = actual_per_hundthou - curr_per_hundthou

    if change_per_hundthou >= 8:
        actual_trend = "Substantial Increase"
    elif change_per_hundthou >= 0.2 and change_per_hundthou < 8:
        actual_trend = "Increase"
    elif change_per_hundthou >= -0.2 and change_per_hundthou < 0.2:
        actual_trend = "Stable"
    elif change_per_hundthou >= -8 and change_per_hundthou < -0.2:
        actual_trend = "Decrease"
    else:
        actual_trend = "Substantial Decrease"

    prompt = f"State: {state}\nCountry: {country}\n\nCurrent case numers: {current}\n\nTwo-week ARIMA Case Prediction: {sarima_output}\n\nGoogle Trends Search Frequency: {trend}.\n\nDemographic Data:\nPopulation: {demo[0]}\nMedian age: {demo[1]}\nMedian yearly salary: {demo[2]}\n\nReddit Activity:\n{flu_post_percent}% of posts relate to influenza infection" 

    data = [[state, country, date, prompt, actual_cases, actual_trend, sarima_output]]
    df = pandas.DataFrame(data, columns=['state', 'country', 'date', 'prompt', 'actual_cases', 'actual_trend', 'sarima_forecast'])
    df.to_csv(output_path, mode='a', index=False, sep="|", header=False)


def generate_random():
    start = datetime(2018, 1, 1)
    end = datetime(2023, 12, 30)
    days_between = (end - start).days
    random_days = random.randint(1, days_between)
    random_date = datetime.strftime((start + timedelta(days=random_days)), "%Y-%m-%d")

    random_country =  random.choice(["us", "aus"])
    if random_country == "aus":
        states_list = aus_states
    else:
        states_list = us_states

    random_state = random.choice(states_list)
    print(random_date)
    print(random_state)

    generate_prompt(random_country, random_state, random_date, "/srv/scratch/z5397970/v2_temp_two.csv")
    
def generate_seq(country, date, num, start_state = 0):
    if country == "aus":
        states = aus_states[start_state:]
    else:
        states = us_states[start_state:]

    start = datetime.strptime(date, "%Y-%m-%d")
    for state in states:
        for i in range(0,(num*14),14):
            gen_date = datetime.strftime((start + timedelta(days=i)), "%Y-%m-%d")
            print("Generating:" + state + ", " + gen_date)
            generate_prompt(country, state, gen_date, "/srv/scratch/z5397970/v2_training/influgemma_v2_training.csv")


generate_seq(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

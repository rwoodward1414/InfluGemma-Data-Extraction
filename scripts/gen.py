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
path = os.path.dirname(os.path.abspath('../demographic-data/demo.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../../sick-post-classifier/classify/posts.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../../sick-post-classifier/classify_posts.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import get_fortnight_surv, get_trend, get_post_perc, add_post_perc, get_region
from states import aus_state_dict, us_state_dict, aus_states, us_states
from demo import get_aus_census_data, get_us_census_data
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
    demo = []

    if country == "aus":
        states = aus_state_dict()
        state_id = states[state]
        demo = get_aus_census_data(state)
        region = "aus"
        region_id = 0
    elif country == "us":
        states = us_state_dict()
        state_id = states[state]
        demo = get_us_census_data(state)
        region_id = get_region(state_id)
    else:
        print("Invalid country")
        return None
    
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
    forecast = sarima_forecast(state_id, start.strftime("%Y-%m-%d"))

    print("Creating prompt")
    indication = "increase"
    if forecast < two_weeks:
        indication = "decline"

    actual_cases = get_fortnight_surv(state_id, end)[0]
    actual_trend = ""

    curr_per_hundthou = (current / float(demo[0])) * 100000
    actual_per_hundthou = (actual_cases / float(demo[0])) * 100000

    change_per_hundthou = actual_per_hundthou - curr_per_hundthou

    if change_per_hundthou >= 10:
        actual_trend = "Substantial Increase"
    elif change_per_hundthou >= 0.2 and change_per_hundthou < 10:
        actual_trend = "Increase"
    elif change_per_hundthou >= -0.2 and change_per_hundthou < 0.2:
        actual_trend = "Stable"
    elif change_per_hundthou >= -10 and change_per_hundthou < -0.2:
        actual_trend = "Decrease"
    else:
        actual_trend = "Substantial Decrease"


    templates = []
    facts = []

    if actual_trend == "Stable":
        templates = [
            f"Flu cases appear to be stable currently.",
            f"The number of flu cases is expected to be around {actual_cases}, showing stablilty in the trend."
            f"Case numbers show only very small change, indicating a stable number over the next two weeks."
        ]

        if trend == "Very high frequency" or trend == "High frequency" or trend == "Moderate frequency":
            trend_text = [f"Flu related search terms are being searched at a {trend.lower()}, indicating a continuing worry around the flu.", f"The current search trend is {trend.lower()}, showing a current interest in the flu. "]
            facts.append(random.choice(trend_text))
        else:
            trend_text = [f"{trend.lower()} online search trend indicates low interest in the flu. ", f"The current search trend is {trend.lower()}, showing people continue to have low interest in the flu."]
            facts.append(random.choice(trend_text))

        if two_weeks > four_weeks:
            cases_text = [f"This follows a rise from {four_weeks} cases four weeks ago to {two_weeks} recently. ", f"While in the past weeks cases went from {four_weeks} to {two_weeks} cases, the trend has now stabilised. "]
            facts.append(random.choice(cases_text))
        else:
            cases_text = [f"This follows a decrease from {four_weeks} cases four weeks ago to {two_weeks}. ", f"In the past weeks cases did decrease from {four_weeks} to {two_weeks} cases, however, cases are now stabilising."]
            facts.append(random.choice(cases_text))

        if flu_post_percent >= 1.5:
            facts.append(f"A higher than average number of reddit posts relate to flu, suggesting more spread throughout the community.")
        elif flu_post_percent <= 0.3:
            facts.append("Very few reddit posts relate to flu, suggesting fewer people are currently discussing it.")


    elif actual_cases > current:
        templates = [
            f"Flu cases are expected to increase to {actual_cases} over the next two weeks. ",
            f"The number of flu cases is projected to rise to {actual_cases}, continuing the upward trend observed in recent weeks. ",
            f"An upward trend in flu activity is expected, with new cases forecasted to reach {actual_cases}. ",
        ]

        if trend == "Very high frequency" or trend == "High frequency" or trend == "Moderate frequency":
            trend_text = [f"Online interest in flu topics is {trend.lower()}, indicating possible increased symptom awareness or spread. ", f"The current search trend is {trend.lower()}, suggesting growing public concern. "]
            facts.append(random.choice(trend_text))
        else:
            trend_text = [f"Despite the current search trend being {trend.lower()}, cases are likely to increase. ", f"The current search trend is {trend.lower()}, however, this search volume may not reflect the increasing case numbers. "]
            facts.append(random.choice(trend_text))

        if two_weeks > four_weeks:
            cases_text = [f"This follows a rise from {four_weeks} cases four weeks ago to {two_weeks} recently. ", f"This increase aligns with the jump from {four_weeks} to {two_weeks} cases. "]
            facts.append(random.choice(cases_text))

        if float(demo[1]) >= 35:
            facts.append(f"The state has an older median age of {str(demo[1])}, suggesting people are more likely to be infected. ")
        else:
            age_text = [f"The relatively young and mobile population may contribute to sustained transmission. ", f"Demographics, including a median age of {str(demo[1])}, suggest the population is active enough to drive further spread."]
            facts.append(random.choice(age_text))

        if flu_post_percent >= 1.5:
            facts.append(f"A higher than average number of reddit posts relate to flu, suggesting more spread throughout the community")
        
    else:
        templates = [
            f"Flu cases are expected to decline to {actual_cases} in the next two weeks, down from {two_weeks} in the previous fortnight. ",
            f"The forecast indicates a downward trend in flu cases, with expected numbers falling to {actual_cases}. ",
            f"Flu activity appears to be declining. Projections show only {actual_cases} new cases over the next two weeks. ",
            f"New flu cases are forecasted to drop to {actual_cases}, indicating reduced transmission. ",
        ]

        if trend == "Very high frequency" or trend == "High frequency" or trend == "Moderate frequency":
            trend_text = [f"Despite {trend.lower()} online activity, the decrease may reflect a tapering of the current wave. ", f"The current search trend is {trend.lower()}, this may be due to lingering concerns. "]
            facts.append(random.choice(trend_text))
        else:
            trend_text = [f"{trend.lower()} online serach trend indicates that cases are liklely to decrease. ", f"The current search trend is {trend.lower()}, showing a decrease in flu related concerns. "]
            facts.append(random.choice(trend_text))

        if two_weeks > four_weeks:
            cases_text = [f"Despite a rise from {four_weeks} cases four weeks ago to {two_weeks}, other factors indicate cases are to decrease. ", f"This drop follows an earlier increase from {four_weeks} to {two_weeks}. "]
            facts.append(random.choice(cases_text))
        else:
            cases_text = [f"Cases decreased over the past month from {four_weeks} cases four weeks ago to {two_weeks} cases two weeks ago, showing a decreasing trend. ", f"Following a drop in cases over the path month, cases are likely to continue decreasing"]
            facts.append(random.choice(cases_text))

        if float(demo[1]) >= 35:
            facts.append(f"The state has an older median age of {str(demo[1])}, suggesting people are more likely to be infected. ")
        else:
            age_text = [f"The relatively young and mobile population may contribute to sustained transmission. ", f"Demographics, including a median age of {str(demo[1])}, suggest the population is active enough to drive further spread."]
            facts.append(random.choice(age_text))
        if flu_post_percent <= 0.3:
            facts.append("Very few reddit posts relate to flu, suggesting fewer people are currently discussing it.")

    summary = random.sample(facts, k=2)

    prompt = f"In the state of {state}, case numbers last fortnight ago were {two_weeks}\nCase number four weeks ago were {four_weeks}\nPredictions indicate that cases will {indication} over the next two weeks to {(int(forecast))}\nThe current google search volume for flu related terms is {trend}\nThis state has a population of {demo[0]}, a median age of {demo[1]}, and a median yearly salary of {demo[2]}\nCurrent reddit activity shows {flu_post_percent}% of posts in the region related to influenza infection."

    explanation = f"{random.choice(templates)}{summary[0]}{summary[1]}"

    data = [[state, country, date, prompt, explanation, actual_cases, actual_trend]]
    df = pandas.DataFrame(data, columns=['state', 'country', 'date', 'prompt', 'explanation', 'actual_cases', 'actual_trend'])
    df.to_csv(output_path, mode='a', index=False, sep="|", header=False)
    print(df)


def generate_random():
    start = datetime(2016, 1, 1)
    end = datetime(2024, 12, 30)
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

    generate_prompt(random_country, random_state, random_date)
    
def generate_seq(country, date, num):
    if country == "aus":
        states = aus_states
    else:
        states = us_states

    start = datetime.strptime(date, "%Y-%m-%d")
    for state in states:
        for i in range(0,(num*14),14):
            gen_date = datetime.strftime((start + timedelta(days=i)), "%Y-%m-%d")
            print("Generating:" + state + ", " + gen_date)
            generate_prompt(country, state, gen_date, "/srv/scratch/z5397970/v1_training/influgemma_v1_training.csv")


generate_seq(sys.argv[1], sys.argv[2], int(sys.argv[3]))


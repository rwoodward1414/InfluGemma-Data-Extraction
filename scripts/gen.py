from datetime import datetime, timedelta
import os, sys
import random
import json


path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../demographic-data/demo.py'))
if path not in sys.path:
    sys.path.append(path)


from datebase_update import get_fortnight_surv, get_trend
from states import aus_state_dict, us_state_dict, aus_states, us_states
from demo import get_aus_census_data, get_us_census_data
from sarima import sarima_forecast

# Country : us or aus
# State : Full US name, Initals Aus
# Start date : yyyy-mm-dd
def generate_prompt(country, state, date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=15)

    state_id = 0
    demo = []

    if country == "aus":
        states = aus_state_dict()
        state_id = states[state]
        demo = get_aus_census_data(state)
    elif country == "us":
        states = us_state_dict()
        state_id = states[state]
        demo = get_us_census_data(state)
    else:
        print("Invalid country")
        return None
    
    four_weeks_ago = start - timedelta(days=29)
    two_weeks_ago = start - timedelta(days=15)
    four_weeks = get_fortnight_surv(state_id, four_weeks_ago)[0]
    two_weeks = get_fortnight_surv(state_id, two_weeks_ago)[0]
    current = get_fortnight_surv(state_id, start)[0]
    trend = get_trend(state_id, start)[0]

    forecast = sarima_forecast(state_id, start.strftime("%Y-%m-%d"))

    indication = "increase"
    if forecast < two_weeks:
        indication = "decline"

    actual_cases = get_fortnight_surv(state_id, end)[0]
    actual_trend = ""

    templates = []
    facts = []

    if actual_cases > current:
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
        
        actual_trend = "Increasing"
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
        actual_trend = "Decreasing"

    summary = random.sample(facts, k=2)

    data = [{
        "prompt": f"You are a flu forecasting model. Based on the data below, generate a case number prediction and trend for new cases over the next two weeks for the state, and provide a short summary explaining the prediction.\nIn the state of {state}, Case numbers last fortnight ago were {two_weeks}\nCase number four weeks ago were {four_weeks}\nPredictions indicate that cases will {indication} over the next two weeks to {(int(forecast))}\nThe current google search volume for flu related terms is {trend}\nThis state has a population of {demo[0]}, a median age of {demo[1]}, and a median yearly salary of {demo[2]}",
        "output": f"Predicted cases: {actual_cases}\nTrend: {actual_trend}\nSummary:\n {random.choice(templates)}{summary[0]}{summary[1]}"

    },]

    print(data)

    with open("../training/flu_forecast_train.json", "w") as f:
        for item in data:
            json.dump(item, f)
            f.write("\n")

generate_prompt("aus", "QLD", "2022-05-01")

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
    
generate_random()
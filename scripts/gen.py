from datetime import datetime, timedelta
import os, sys
import random


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
from states import aus_state_dict, us_state_dict
from demo import get_aus_census_data
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

    if actual_cases > current:
        templates = [
            f"Flu cases are expected to increase to {actual_cases} over the next two weeks. "
            f"This follows a rise from {four_weeks} cases four weeks ago to {two_weeks} recently. "
            f"The current search trend is {trend.lower()}, suggesting growing public concern. "
            f"With a population of {str(demo[0])}, median age {str(demo[1])}, and moderate income levels, further spread is likely.",

            f"The number of flu cases is projected to rise to {actual_cases}, continuing the upward trend observed in recent weeks. "
            f"Online interest in flu topics is {trend.lower()}, indicating possible increased symptom awareness or spread. "
            f"The relatively young and mobile population may contribute to sustained transmission.",

            f"An upward trend in flu activity is expected, with new cases forecasted to reach {actual_cases}. "
            f"This increase aligns with the jump from {four_weeks} to {two_weeks} cases and the {trend.lower()} search volume.",

            f"Case counts are likely to climb to {actual_cases}, given the recent surge and strong flu-related online interest. "
            f"Demographics, including a median age of {str(demo[1])}, suggest the population is active enough to drive further spread."
        ]
        actual_trend = "Increasing"
    else:
        templates = [
            f"Flu cases are expected to decline to {actual_cases} in the next two weeks, down from {two_weeks} in the previous fortnight. "
            f"This drop follows an earlier increase from {four_weeks} to {two_weeks}. "
            f"Despite {trend.lower()} online activity, the decrease may reflect a tapering of the current wave.",

            f"The forecast indicates a downward trend in flu cases, with expected numbers falling to {actual_cases}. "
            f"After peaking at {two_weeks}, the decline suggests successful public awareness or seasonal slowdown.",

            f"Flu activity appears to be declining. Projections show only {actual_cases} new cases over the next two weeks. "

            f"New flu cases are forecasted to drop to {actual_cases}, indicating reduced transmission. "
        ]
        actual_trend = "Decreasing"


    data = [{
        "prompt": f"You are a flu forecasting model. Based on the data below, generate a case number prediction and trend for new cases over the next two weeks, and provide a short summary explaining the prediction.\nCase numbers last fortnight ago were {two_weeks}\nCase number four weeks ago were {four_weeks}\nPredictions indicate that cases will {indication} over the next two weeks to {(int(forecast))}\nThe current google search volume for flu related terms is {trend}\nThis state has a population of {demo[0]}, a median age of {demo[1]}, and a median yearly salary of {demo[2]}",
        "output": f"Predicted cases: {actual_cases}\nTrend: {actual_trend}\nSummary:\n {random.choice(templates)}"

    },]

    print(data)





generate_prompt("aus", "QLD", "2022-05-01")
# generate_output("aus", "QLD", "2022-05-01")
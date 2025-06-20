from datetime import datetime, timedelta
import os, sys


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

# Country : us or aus
# State : Full US name, Initals Aus
# Start date : yyyy-mm-dd
def generate(country, state, date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=15)

    state_id = 0
    demo = []

    if country == "aus":
        states = aus_state_dict()
        state_id = aus_state_dict[state]
        demo = get_aus_census_data(state)
    elif country == "us":
        states = us_state_dict()
        state_id = us_state_dict[state]
        demo = get_us_census_data(state)
    else:
        print("Invalid country")
        return None
    
    four_weeks_ago = start - timedelta(days=29)
    two_weeks_ago = start - timedelta(days=15)
    four_weeks = get_fortnight_surv(state_id, four_weeks_ago)
    two_weeks = get_fortnight_surv(state_id, two_weeks_ago)
    trend = get_trend(state_id, end)

    print("In " + state)
    print("Case number four weeks ago were " + str(four_weeks))
    print("Case number two weeks ago were " + str(two_weeks))
    print("The current google search trend shows people searching flu related terms at a " + trend)
    print("This state has a population of " + str(demo[0]) + ", a median age of " + str(demo[1]) + ", and a median yearly salary of " + str(demo[2]))
    print("Based on this information, generate a prediction for the trend of new cases over the next two weeks")

generate("aus", "QLD", "2022-05-01")
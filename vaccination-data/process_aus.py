import pandas as pd
from datetime import datetime
import os, sys

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)

path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import add_vaccination
from states import aus_state_dict

state_dict = aus_state_dict()

def get_date(year, month):
    date_string = str(year) + "-" + str(month) + "-1"
    date_date = datetime.strptime(date_string, "%Y-%m-%d")
    return date_date

df = pd.read_csv("/srv/scratch/z5397970/Aus_Vacc2025.csv")
print(df.head())
for state, group in df.groupby("State"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group)):
        month = group.loc[i, "Month"]
        year = group.loc[i, "Year"]
        end_date = get_date(year, month)
        vacc_perc = group.loc[i, "Percent"][:-1]
        add_vaccination(state_dict[state], end_date, vacc_perc)

    print(f"Done {state}")

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
from states import us_state_dict

state_dict = us_state_dict()

df = pd.read_csv('/srv/scratch/z5397970/usvacc2025.csv')

df = df[df['Geographic Level'] == "State"]
df = df[df['indicator_label'] == "Up-to-date"]
non_states = ["District of Columbia", "Guam", "IL-City of Chicago", "NY-City of New York", "Puerto Rico", "U.S. Virgin Islands", "Rhode Island"]

mask = ~df["Geographic Name"].isin(non_states)
df = df[mask]

df = df.sort_values(by=["Geographic Name", "Week_ending"]).reset_index(drop=True)
start = datetime(2025, 3, 29)

for state, group in df.groupby("Geographic Name"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group)):
        year_month = group.loc[i, "Week_ending"][:-12]
        end_date = datetime.strptime(year_month, "%Y %b %d")
        vacc_perc = str(group.loc[i, "Estimates"])
        if end_date > start:
            add_vaccination(state_dict[state], end_date, vacc_perc)
    print(f"Done {state}")


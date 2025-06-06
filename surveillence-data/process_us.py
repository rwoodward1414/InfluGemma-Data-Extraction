from datetime import datetime

def get_week_date(year, week):
    date_string = str(year) + "-" + str(week) + "-1"
    start_date = datetime.strptime(date_string, "%Y-%W-%w")
    return start_date

import os, sys
import pandas

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import add_many_surv
from states import us_state_dict

state_dict = us_state_dict()

file_path = "/home/ren/thesis/InfluGemma-Data-Extraction/data/us_2016-2025.csv"
df = pandas.DataFrame(pandas.read_csv(file_path, skiprows=1, usecols=["REGION", "YEAR", "WEEK", "TOTAL A", "TOTAL B"]))

# Convert X values to 0s and remove non-states
non_states = ["District of Columbia", "Puerto Rico", "Virgin Islands", "New York City"]
mask = ~df["REGION"].isin(non_states)
df = df[mask]
df.replace({"TOTAL A": "X", "TOTAL B": "X"}, 0, inplace=True)

# Add A and B strains together
df["TOTAL A"] =  df["TOTAL A"].astype(int)
df["TOTAL B"] =  df["TOTAL B"].astype(int)
df["TOTAL"] = df[["TOTAL A", "TOTAL B"]].sum(axis=1)

df = df.sort_values(by=["REGION", "YEAR", "WEEK"]).reset_index(drop=True)

combined = []
for state, group in df.groupby("REGION"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group) - 2, 2):
        end_year = group.loc[i + 2, "YEAR"]
        end_week = group.loc[i + 2, "WEEK"]
        end_date = get_week_date(end_year, end_week)
        total_cases = group.loc[i, "TOTAL"] + group.loc[i + 1, "TOTAL"]

        combined.append({
            "StateID": state_dict[state],
            "EndDate": end_date,
            "CaseNumber": total_cases
        })

combined_df = pandas.DataFrame(combined)

add_many_surv(combined_df)
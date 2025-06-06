# This script extracts data from a pre-compiled spreadsheet containing case numbers for australian states from 2010-2023
import pandas
import sys
import os
import psycopg2

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.abspath('../helper/states.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import add_many_surv
from states import aus_state_dict

states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
state_dict = aus_state_dict()

file_path = "/home/ren/thesis/InfluGemma-Data-Extraction/data/aus_2013-2023.xlsx"
df = pandas.DataFrame(pandas.read_excel(file_path))

df_long = df.melt(id_vars=["Start Date"], var_name="state", value_name="cases")
df_long["Start Date"] = pandas.to_datetime(df_long["Start Date"])
df_long = df_long.sort_values(by=["state", "Start Date"]).reset_index(drop=True)

combined = []
for state, group in df_long.groupby("state"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group) - 2, 2):
        # start_date = group.loc[i, "Start Date"]
        end_date = group.loc[i + 2, "Start Date"]
        total_cases = group.loc[i, "cases"] + group.loc[i + 1, "cases"]

        combined.append({
            "StateID": state_dict[state],
            "EndDate": end_date,
            "CaseNumber": total_cases
        })

combined_df = pandas.DataFrame(combined)

add_many_surv(combined_df)
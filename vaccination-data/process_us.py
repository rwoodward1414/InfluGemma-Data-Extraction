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

def get_date(year, month):
    if month > 12:
        month = month - 12
        year = year + 1
    date_string = str(year) + "-" + str(month) + "-1"
    date_date = datetime.strptime(date_string, "%Y-%m-%d")
    return date_date

df = pd.read_csv('../data/Influenza_Vaccination_Coverage_for_All_Ages_(6+_Months)_20251104(1).csv')

df = df[df["Vaccine"] == "Seasonal Influenza"]
df = df[df['Geography Type'] == "States/Local Areas"]
df = df[df['Dimension Type'] == "Age"]
df = df[df['Dimension'] == ">=18 Years"]

non_states = ["District of Columbia", "Guam", "IL-City of Chicago", "NY-City of New York", "Puerto Rico", "PA-Philadelphia", "TX-Bexar County", "TX-City of Houston", "U.S. Virgin Islands"]
mask = ~df["Geography"].isin(non_states)
df = df[mask]

df["Season/Survey Year"] = df["Season/Survey Year"].str.slice(0,4).astype(int)
df = df[df["Season/Survey Year"] >= 2017]
df = df.replace(to_replace="NR †", value="0")

print(df.head())
print(df["Season/Survey Year"].head())
df = df.sort_values(by=["Geography", "Season/Survey Year", "Month"]).reset_index(drop=True)

for state, group in df.groupby("Geography"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group)):
        month = group.loc[i, "Month"]
        year = group.loc[i, "Season/Survey Year"]
        end_date = get_date(year, month+1)
        vacc_perc = group.loc[i, "Estimate (%)"]
        add_vaccination(state_dict[state], end_date, vacc_perc)
    print(f"Done {state}")

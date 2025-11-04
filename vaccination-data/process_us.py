import pandas as pd
from datebase_update import add_vaccination
from states import us_state_dict
from datetime import datetime

state_dict = us_state_dict()

def get_date(year, month):
    date_string = str(year) + "-" + str(month) + "-1"
    date_date = datetime.strptime(date_string, "%Y-%m-%d")
    return date_date

df = pd.read_csv()

df = df[df["Vaccine"] == "Seasonal Influenza"]
df = df[df['Geography Type'] == "States/Local Areas"]
df = df[df['Dimension Type'] == "Age"]
df = df[df['Dimension'] == ">=18 Years"]

df = df.sort_values(by=["Geography", "Season/Survey Year", "Month"]).reset_index(drop=True)

for state, group in df.groupby("Geography"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group)):
        month = group.loc[i, "Month"]
        year = group.loc[i, "Season/Survey Year"]
        end_date = get_date(year, month+1)
        vacc_perc = group.loc[i, "Estimate (%)"]

        add_vaccination(state_dict[state], end_date, vacc_perc)
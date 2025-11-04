import pandas as pd
from datebase_update import add_vaccination
from states import aus_state_dict
from datetime import datetime

state_dict = aus_state_dict()

def get_date(year, month):
    date_string = str(year) + "-" + str(month) + "-1"
    date_date = datetime.strptime(date_string, "%Y-%m-%d")
    return date_date

df = pd.read_csv()
for state, group in df.groupby("State"):
    group = group.reset_index(drop=True)
    for i in range(0, len(group)):
        month = group.loc[i, "Month"]
        year = group.loc[i, "Year"]
        end_date = get_date(year, month+1)
        vacc_perc = group.loc[i, "Percent"]

        add_vaccination(state_dict[state], end_date, vacc_perc)
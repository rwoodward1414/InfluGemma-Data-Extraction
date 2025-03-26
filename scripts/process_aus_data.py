import pandas
import sys
from datebase_update import get_state, add_fortnight_surv

states = ['ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA']

def extract_data(file_path):
    df = pandas.DataFrame(pandas.read_excel(file_path, skiprows=2, usecols=['Disease name', 'ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA', 'This reporting period'], index_col=0))
    flu_cases = df.loc['Influenza (laboratory confirmed)']

    extract_date = df.iloc[1]['This reporting period']
    date = str(extract_date).removesuffix(' 00:00:00')

    for state in states:
        state_id = get_state(state)
        case_num = int(flu_cases[state])
        add_fortnight_surv(state_id, date, case_num)

for i in range(1, len(sys.argv)):
    extract_data(sys.argv[i])
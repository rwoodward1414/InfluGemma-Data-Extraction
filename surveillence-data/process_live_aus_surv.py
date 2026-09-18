import pandas
import sys
import os
import requests
from bs4 import BeautifulSoup
import datetime


path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)

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
        print(state, case_num)

        add_fortnight_surv(state_id, date, case_num)

#for i in range(1, len(sys.argv)):
 #    extract_data(sys.argv[i])

def download_new_sheet():
    base_url = "https://www.health.gov.au/resources/collections/nndss-fortnightly-reports"
    r = requests.get(base_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    page = soup.find("div", attrs={"class":"au-callout"})
    link_to_download = page.find("a")
    link_url = link_to_download["href"]
    download_page = "https://www.health.gov.au/" + link_url

    r = requests.get(download_page)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    excel = soup.find("a", href=lambda href: href and href.lower().endswith(".xlsx"))
    excel_url = excel["href"]
    excel_url = "https://www.health.gov.au/" + excel_url

    r = requests.get(excel_url)
    r.raise_for_status()

    filename = os.path.join("./data", os.path.basename(excel_url))
    with open(filename, "wb") as f:
        f.write(r.content)
        f.close()

    return filename


def download_one(path):
    r = requests.get(path)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    excel = soup.find("a", href=lambda href: href and href.lower().endswith(".xlsx"))
    excel_url = excel["href"]
    excel_url = "https://www.health.gov.au/" + excel_url

    r = requests.get(excel_url)
    r.raise_for_status()

    filename = os.path.join("./data", os.path.basename(excel_url))
    with open(filename, "wb") as f:
        f.write(r.content)
        f.close()

    return filename

for i in range(1, len(sys.argv)):
    file = download_one(sys.argv[i])
    extract_data(file)

#cases = [102, 2723, 408, 1443, 302, 62, 1032, 258]
#date = datetime.datetime(2024, 4, 28)
#for i in range(0, 1):
#    state_id = get_state(states[i])
#    case_num = int(cases[i])
#    print(state_id, case_num)

#    add_fortnight_surv(state_id, date, case_num)

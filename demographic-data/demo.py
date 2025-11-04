import requests
import sys
import re

def get_us_census_data(state):
    demo = []
    # Population
    pop_url = 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B01003_001E&for=state:*'
    response = requests.get(pop_url)
    print(response.status_code)
    data = response.text
    match = re.search(rf'{state}.*?([0-9]{{3,}})', data)
    demo.append(match.group(1))

    # Median Age
    age_url = 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B01002_001E&for=state:*'
    response = requests.get(age_url)
    print(response.status_code)
    data = response.text
    match = re.search(rf'{state}.*?([0-9]{{2}}\.[0-9])', data)
    demo.append(match.group(1))

    # Median Annual Wage
    wage_url = 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B06011_001E&for=state:*'
    response = requests.get(wage_url)
    data = response.text
    print(response.status_code)
    match = re.search(rf'{state}.*?([0-9]{{3,}})', data)
    demo.append(match.group(1))
    print(demo)

    return demo
    
get_us_census_data("California")


def get_aus_census_data(state):
    demo = []

    match state:
        case "ACT":
            stats = [481700, 35, 62556]
            demo.extend(stats)
        case "NSW":
            stats = [8545100, 39, 42276]
            demo.extend(stats)
        case "NT":
            stats = [262200, 33, 48672]
            demo.extend(stats)
        case "QLD":
            stats = [5618800, 38, 40924]
            demo.extend(stats)
        case "SA":
            stats = [1891700, 41, 38168]
            demo.extend(stats)
        case "TAS":
            stats = [575800, 42, 36452]
            demo.extend(stats)
        case "VIC":
            stats = [7011100, 38, 41756]
            demo.extend(stats)
        case "WA":
            stats = [3008700, 38, 44096]
            demo.extend(stats)

    return demo

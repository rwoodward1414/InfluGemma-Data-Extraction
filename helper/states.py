import os, sys

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import add_state, get_state

aus_states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
us_states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

trends_aus_states = {
    "NSW": "AU-NSW",
    "VIC": "AU-VIC",
    "QLD": "AU-QLD",
    "WA":  "AU-WA",
    "SA":  "AU-SA",
    "TAS": "AU-TAS",
    "ACT": "AU-ACT",
    "NT":  "AU-NT"
}

trends_us_states = {
    "Alabama": "US-AL",
    "Alaska": "US-AK",
    "Arizona": "US-AZ",
    "Arkansas": "US-AR",
    "California": "US-CA",
    "Colorado": "US-CO",
    "Connecticut": "US-CT",
    "Delaware": "US-DE",
    "Florida": "US-FL",
    "Georgia": "US-GA",
    "Hawaii": "US-HI",
    "Idaho": "US-ID",
    "Illinois": "US-IL",
    "Indiana": "US-IN",
    "Iowa": "US-IA",
    "Kansas": "US-KS",
    "Kentucky": "US-KY",
    "Louisiana": "US-LA",
    "Maine": "US-ME",
    "Maryland": "US-MD",
    "Massachusetts": "US-MA",
    "Michigan": "US-MI",
    "Minnesota": "US-MN",
    "Mississippi": "US-MS",
    "Missouri": "US-MO",
    "Montana": "US-MT",
    "Nebraska": "US-NE",
    "Nevada": "US-NV",
    "New Hampshire": "US-NH",
    "New Jersey": "US-NJ",
    "New Mexico": "US-NM",
    "New York": "US-NY",
    "North Carolina": "US-NC",
    "North Dakota": "US-ND",
    "Ohio": "US-OH",
    "Oklahoma": "US-OK",
    "Oregon": "US-OR",
    "Pennsylvania": "US-PA",
    "Rhode Island": "US-RI",
    "South Carolina": "US-SC",
    "South Dakota": "US-SD",
    "Tennessee": "US-TN",
    "Texas": "US-TX",
    "Utah": "US-UT",
    "Vermont": "US-VT",
    "Virginia": "US-VA",
    "Washington": "US-WA",
    "West Virginia": "US-WV",
    "Wisconsin": "US-WI",
    "Wyoming": "US-WY"
}

state_subreddits = {
    "ACT": "canberra",
    "TAS": "tasmania",
    "NSW": "sydney",
    "NT": "darwin",
    "QLD": "brisbane",
    "VIC": "melbourne",
    "Washington": "seattle",
    "Alabama": "HuntsvilleAlabama",
    "Alaska": "Alaska",
    "Arizona": "phoenix",
    "Arkansas": "arkansas",
    "California": "LosAngeles",
    "Colorado": "Denver",
    "Connecticut": "Connecticut",
    "Delaware": "Delaware",
    "Florida": "Florida",
    "Georgia": "Georgia",
    "Hawaii": "Hawaii",
    "Idaho": "Boise",
    "Illinois": "Chicago",
    "Indiana": "Indianapolis",
    "Iowa": "Iowa",
    "Kansas": "Wichita",
    "Kentucky": "Louisville",
    "Louisiana": "NewOrleans",
    "Maine": "Maine",
    "Maryland": "Maryland",
    "Massachusetts": "Boston",
    "Michigan": "Michigan",
    "Minnesota": "Minnesota",
    "Mississippi": "Mississippi",
    "Missouri": "KansasCity",
    "Montana": "Montana",
    "Nebraska": "Omaha",
    "Nevada": "LasVegas",
    "New Hampshire": "NewHampshire",
    "New Jersey": "NewJersey",
    "New Mexico": "Alburquerque",
    "New York": "NewYorkCity",
    "North Carolina": "NorthCarolina",
    "North Dakota": "NorthDakota",
    "Ohio": "Ohio",
    "Oklahoma": "Oklahoma",
    "Oregon": "Portland",
    "Pennsylvania": "Philadelphia",
    "Rhode Island": "RhodeIsland",
    "South Carolina": "SouthCarolina",
    "South Dakota": "SouthDakota",
    "Tennessee": "Tennessee",
    "Texas": "texas",
    "Utah": "Utah",
    "Vermont": "Vermont",
    "Virginia": "Virginia",
    "West Virginia": "WestVirginia",
    "Wisconsin": "wisconsin",
    "Wyoming": "wyoming"
}


def add_aus_states():
    for state in aus_states:
        add_state(state, 1)

def aus_state_dict():
    dict = {}
    for state in aus_states:
        dict[state] = get_state(state)
    return dict

def add_us_states():
    for state in us_states:
        add_state(state, 2)

def us_state_dict():
    dict = {}
    for state in us_states:
        dict[state] = get_state(state)
    return dict
import psycopg2
from database_connect import connect

def add_country(country_name, region):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT count(CountryID) FROM countries")
    result = cur.fetchone()
    country_id = result[0] + 1

    cur.execute("""
        INSERT INTO countries (CountryID, CountryName, Region)
        VALUES (%s, %s, %s)
    """, (country_id, country_name, region))

    conn.commit()

def add_state(state_name, country_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT count(StateID) FROM states")
    result = cur.fetchone()
    state_id = result[0] + 1

    cur.execute("""
        INSERT INTO states (StateID, StateName, CountryID)
        VALUES (%s, %s, %s)
    """, (state_id, state_name, country_id))

    conn.commit()

def get_state(state_name):
    conn = connect()
    cur = conn.cursor()

    low_state_name = state_name.lower()

    cur.execute("""
                SELECT StateID FROM states
                WHERE LOWER(StateName) ilike %s
                """, (low_state_name,))
    result = cur.fetchone()
    state_id = result[0]
    return state_id

def add_fortnight_surv(state_id, end_date, case_num):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO fornight_surv_data (StateID, EndDate, CaseNumber)
        VALUES (%s, %s, %s)
    """, (state_id, end_date, case_num))

    conn.commit()
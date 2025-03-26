import psycopg2
from database_connect import connect

def add_country(country_name, region):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT count(CounryID) FROM countries")
    result = cur.fetchone()
    print['count']
    country_id = result.count + 1

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
    print['count']
    state_id = result.count + 1

    cur.execute("""
        INSERT INTO states (StateID, StateName, CountryID)
        VALUES (%s, %s, %s)
    """, (state_id, state_name, country_id))

    conn.commit()

def add_fortnight_surv(state_id, end_date, case_num):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO fortnight_surv_data (StateID, EndDate, CaseNumber)
        VALUES (%s, %s, %s)
    """, (state_id, end_date, case_num))

    conn.commit()
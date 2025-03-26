import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="fludata",
            user="user",
            password="pass",
            host="localhost",
            port="5432"
        )
        print("connected")
        return conn
    except Exception as e:
        print("rip")
        print(e)
        return None
    
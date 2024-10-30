import psycopg2

def connect():
    conn = psycopg2.connect(
        host="postgres",
        database="mydatabase",
        user="user",
        password="password"
    )
    return conn

def fetch_data():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mytable")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

if __name__ == "__main__":
    fetch_data()

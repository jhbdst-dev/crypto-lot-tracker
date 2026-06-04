import psycopg2

conn = psycopg2.connect(
    dbname="crypto_lot_tracker",
    user="hs",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("SELECT * FROM trades")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
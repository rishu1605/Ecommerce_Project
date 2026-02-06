import sqlite3
conn = sqlite3.connect('sic_mart.db')
cursor = conn.execute("PRAGMA table_info(products)")
columns = [row[1] for row in cursor.fetchall()]
print(f"Your database columns are: {columns}")
conn.close()
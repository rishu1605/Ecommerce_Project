import sqlite3

# Connect to your database
conn = sqlite3.connect('sic_mart.db')
cursor = conn.cursor()

# Force the "SG bat" order to belong to your current ID (2)
cursor.execute("UPDATE orders SET seller_id = 2 WHERE product_name = 'SG bat'")

conn.commit()
print("Database updated! Refresh your Shop Orders page now.")
conn.close()
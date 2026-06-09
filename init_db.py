import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect('data.db')

# run schema.sql to create the tables
with open('schema.sql') as f:
    conn.executescript(f.read())

# read CSV file
df = pd.read_csv('victorian_road_crash_data.csv')

# clean column names
df.columns = [c.lower() for c in df.columns]

# rite data to your 'crash_data' table
df.to_sql('crash_data', conn, if_exists='replace', index=False)

# insert mission statement
cur = conn.cursor()
cur.execute("INSERT INTO site_content (section_name, content_body) VALUES (?, ?)",
            ('mission', 'The mission of this platform is to democratize access to Victorian road incident data...'))

conn.commit()
conn.close()
print("database populated")
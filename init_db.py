import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('data.db')
cur = conn.cursor()

# 1. Create the personas table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        filter_query TEXT NOT NULL
    )
''')

# 2. Insert the data for Marcus and Elena
# We use REPLACE or check existence to avoid unique constraint errors if run multiple times
cur.execute("DELETE FROM personas") # Optional: Clears old data to ensure a fresh state

cur.execute("INSERT INTO personas (name, description, filter_query) VALUES (?, ?, ?)",
            ('marcus', 'Long-distance commuter', 'SELECT speed_zone, severity, COUNT(*) as count FROM crash_data GROUP BY speed_zone, severity ORDER BY count DESC LIMIT 5'))

cur.execute("INSERT INTO personas (name, description, filter_query) VALUES (?, ?, ?)",
            ('elena', 'Cyclist', 'SELECT light_condition, road_geometry, COUNT(*) as count FROM crash_data WHERE bicyclist > 0 GROUP BY light_condition, road_geometry LIMIT 5'))
conn.commit()
conn.close()
print("database populated")
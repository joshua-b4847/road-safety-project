from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/mission')
def mission():
    conn = get_db_connection()
    content = conn.execute('SELECT content_body FROM site_content WHERE section_name = "mission"').fetchone()
    conn.close()
    return render_template('mission.html', mission=content['content_body'])

@app.route('/summary')
def summary():
    conn = get_db_connection()
    
    # default Summary
    general = conn.execute('SELECT severity, SUM("seriousinjury") as serious, SUM("otherinjury") as other FROM crash_data GROUP BY severity').fetchall()
    
    # marcus (Long-distance commuter)
    marcus = conn.execute('SELECT speed_zone, severity, COUNT(*) as count FROM crash_data GROUP BY speed_zone, severity ORDER BY count DESC LIMIT 5').fetchall()
    
    # elena (Cyclist)
    elena = conn.execute('SELECT light_condition, road_geometry, COUNT(*) as count FROM crash_data WHERE bicyclist > 0 GROUP BY light_condition, road_geometry LIMIT 5').fetchall()
    
    conn.close()
    return render_template('summary.html', general=general, marcus=marcus, elena=elena)
if __name__ == '__main__':
    app.run(debug=True)
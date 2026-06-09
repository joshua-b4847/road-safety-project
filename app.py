from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mission')
def mission():
    conn = get_db_connection()
    content = conn.execute('SELECT content_body FROM site_content WHERE section_name = "mission"').fetchone()
    conn.close()
    return render_template('mission.html', mission=content['content_body'])

@app.route('/discover')
def discover():
    conn = get_db_connection()
    
    # 1. Road Geometry in Dark (Existing)
    dark_accidents = conn.execute('''
        SELECT road_geometry, COUNT(*) as incident_count
        FROM crash_data
        WHERE light_condition LIKE '%Dark%'
        GROUP BY road_geometry
        ORDER BY incident_count DESC LIMIT 5
    ''').fetchall()
    
    # 2. NEW: Accidents by Day of Week
    day_accidents = conn.execute('''
        SELECT day_of_week, COUNT(*) as incident_count
        FROM crash_data
        GROUP BY day_of_week
        ORDER BY incident_count DESC
    ''').fetchall()
    
    # 3. NEW: Severity by Speed Zone (Focus on Serious/Fatal)
    severity_speed = conn.execute('''
        SELECT speed_zone, severity, COUNT(*) as count
        FROM crash_data
        WHERE severity IN ('Fatal accident', 'Serious injury accident')
        GROUP BY speed_zone, severity
        ORDER BY count DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    return render_template('discover.html', 
                           dark_accidents=dark_accidents, 
                           day_accidents=day_accidents, 
                           severity_speed=severity_speed)

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



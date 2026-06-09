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

# FIXED: Added <name> to the route so the function receives it
@app.route('/persona/<name>')
def show_persona(name):
    conn = get_db_connection()
    # Fetch the query directly from the database based on the persona name!
    persona = conn.execute('SELECT * FROM personas WHERE name = ?', (name,)).fetchone()
    # Ensure a result was found to prevent errors
    if persona:
        data = conn.execute(persona['filter_query']).fetchall()
    else:
        data = []
    conn.close()
    return render_template('persona_view.html', persona=persona, data=data)

@app.route('/discover')
def discover():
    conn = get_db_connection()
    
    dark_accidents = conn.execute('''
        SELECT road_geometry, COUNT(*) as incident_count
        FROM crash_data
        WHERE light_condition LIKE '%Dark%'
        GROUP BY road_geometry
        ORDER BY incident_count DESC LIMIT 5
    ''').fetchall()
    
    day_accidents = conn.execute('''
        SELECT day_of_week, COUNT(*) as incident_count
        FROM crash_data
        GROUP BY day_of_week
        ORDER BY incident_count DESC
    ''').fetchall()
    
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
    
    general = conn.execute('SELECT severity, SUM("seriousinjury") as serious, SUM("otherinjury") as other FROM crash_data GROUP BY severity').fetchall()
    marcus = conn.execute('SELECT speed_zone, severity, COUNT(*) as count FROM crash_data GROUP BY speed_zone, severity ORDER BY count DESC LIMIT 5').fetchall()
    elena = conn.execute('SELECT light_condition, road_geometry, COUNT(*) as count FROM crash_data WHERE bicyclist > 0 GROUP BY light_condition, road_geometry LIMIT 5').fetchall()
    
    conn.close()
    return render_template('summary.html', general=general, marcus=marcus, elena=elena)

if __name__ == '__main__':
    app.run(debug=True)



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
    # Fetch Sub-Task B content
    content = conn.execute('SELECT content_body FROM site_content WHERE section_name = "mission"').fetchone()
    conn.close()
    return render_template('mission.html', mission=content['content_body'])

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/summary')
def summary():
    conn = get_db_connection()
    # SQL query
    data = conn.execute('''
        SELECT severity, SUM(serious_injury) as total_serious, SUM(other_injury) as total_other
        FROM crash_data
        GROUP BY severity
    ''').fetchall()
    conn.close()
    return render_template('summary.html', data=data)
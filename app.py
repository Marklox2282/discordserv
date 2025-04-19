from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'complaints.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            server TEXT,
            moderator TEXT,
            message_link TEXT,
            complaint TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.before_first_request
 def setup():
    init_db()

@app.route('/', methods=['GET', 'POST'])
 def submit_complaint():
    if request.method == 'POST':
        username     = request.form['username']
        server       = request.form['server']
        moderator    = request.form['moderator']
        message_link = request.form['message_link']
        complaint    = request.form['complaint']
        timestamp    = datetime.utcnow().isoformat()

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''
            INSERT INTO complaints (username, server, moderator, message_link, complaint, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, server, moderator, message_link, complaint, timestamp))
        conn.commit()
        conn.close()

        return redirect(url_for('success'))

    return render_template('form.html')

@app.route('/success')
 def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)

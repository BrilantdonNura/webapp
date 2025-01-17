from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT,
                   last_name TEXT,
                   age INTEGER
                   )
""")

    cursor.connection.commit()
    cursor.connection.close()
    db.close()


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods = ['POST'])
def submit():
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = int(request.form['age'])

    db = sqlite3.connect('data.sqlite')
    cur = db.cursor()
    cur.execute("INSERT INTO users(first_name, last_name, age) VALUES(?,?,?)",(first_name, last_name,age))
    cur.connection.commit()
    
    cur.connection.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/users')
def list_users():
    db = sqlite3.connect('data.sqlite')
    cur = db.cursor()
    
    cur.execute('SELECT * FROM users')
    users_list = cur.fetchall()

    return render_template('users.html', users=users_list)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5200, debug=True)
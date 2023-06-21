from flask import Flask
from flask import templating, redirect
import hashlib
import sqlite3

secret = "today"

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/<hash>/')
@app.route('/<hash>')
def preroute(hash):
    sql = 'SELECT id FROM urls WHERE hash = ?'
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    cur.execute(sql, (hash,))
    data = cur.fetchall()
    if len(data) < 1:
        return 'Not found'
    else:
        return templating.render_template('forwarder.html', hash=str(hash))


@app.route('/<hash>/<id>/')
@app.route('/<hash>/<id>')
def route(hash, id):
    sql = 'SELECT id FROM urls WHERE hash = ?'
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    cur.execute(sql, (hash,))
    data = cur.fetchall()
    if len(data) < 1:
        return 'Not found'
    else:
        if data[0][0] == int(id):
            # redifrect to url
            sql = 'SELECT url FROM urls WHERE id = ?'
            cur.execute(sql, (id,))
            data = cur.fetchall()
            return redirect(data[0][0])


        else:
            return 'Not found'

if __name__ == '__main__':
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS urls (url TEXT UNIQUE, hash TEXT UNIQUE, id INT UNIQUE)')
    cur.close()
    db.commit()
    db.close()
    print('Database initialized')
    app.run()

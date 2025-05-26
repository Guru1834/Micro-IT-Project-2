from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 original_url TEXT NOT NULL,
                 short_code TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

# Generate a random short code
def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()
        
        conn = sqlite3.connect('url_shortener.db')
        c = conn.cursor()
        c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                 (original_url, short_code))
        conn.commit()
        conn.close()
        
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
#app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
# app.secret_key = "caircocoders-ednalan"
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'testingdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        password="postgres")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = conn.cursor()
    if request.method == 'POST':    
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
                query = "SELECT * from employee ORDER BY id"
                cur.execute(query)
                employee = cur.fetchall()
        else:
            query = "SELECT * from employee WHERE name LIKE '%{}%' OR email LIKE '%{}%' OR phone LIKE '%{}%' ORDER BY id DESC LIMIT 20".format(search_word,search_word,search_word)
            cur.execute(query)
            numrows = int(cur.rowcount)
            employee = cur.fetchall()
            print(numrows,employee)
    return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})
if __name__ == "__main__":
    app.run(debug=True)
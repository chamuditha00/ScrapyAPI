from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/app', methods=['GET'])
def get_data():
    conn = sqlite3.connect('amazon_rank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM amazon_ranked")
    columns = [description[0] for description in cursor.description]  # Get column names
    data = cursor.fetchall()
    result = []
    for row in data:
        result.append(dict(zip(columns, row)))  # Convert each row to a dictionary with column names
    return jsonify({'data': result, 'columns': columns})


@app.route('/app/<string:title>', methods=['GET'])

def get_data_by_title(title):
    conn = sqlite3.connect('amazon_rank.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE title=? ORDER BY rank LIMIT 10", (title,)).fetchall()
    return jsonify({'data':data})

@app.route('/app/<string:price>', methods=['GET'])

def get_data_by_price(price):
    conn = sqlite3.connect('amazon_rank.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE price=? ORDER BY rank LIMIT 10",(price,)).fetchall()
    return jsonify({'data':data})

@app.route('/app/<int:id>', methods=['GET'])

def get_data_by_id(id):
    conn = sqlite3.connect('amazon_rank.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE id=? ORDER BY rank LIMIT 10",(id,)).fetchall()
    return jsonify({'data':data})



if  __name__ == '__main__':
    app.run(debug=True)
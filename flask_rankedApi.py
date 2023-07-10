from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/app', methods=['GET'])
def get_data():
    conn = sqlite3.connect('ranked_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ranked_data")
    columns = [description[0] for description in cursor.description]  # Get column names
    data = cursor.fetchall()
    result = []
    for row in data:
        result.append(dict(zip(columns, row)))  # Convert each row to a dictionary with column names
    return jsonify({'data': result, 'columns': columns})
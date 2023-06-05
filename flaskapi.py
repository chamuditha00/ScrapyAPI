from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/app', methods=['GET'])

def get_data():
    conn = sqlite3.connect('amazon_data.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data").fetchall()
    return jsonify({'data':data})

@app.route('/app/<string:title>', methods=['GET'])

def get_data_by_title(title):
    conn = sqlite3.connect('amazon_data.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE title=?",(title,)).fetchall()
    return jsonify({'data':data})

@app.route('/app/<string:price>', methods=['GET'])

def get_data_by_price(price):
    conn = sqlite3.connect('amazon_data.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE price=?",(price,)).fetchall()
    return jsonify({'data':data})

@app.route('/app/<int:id>', methods=['GET'])

def get_data_by_id(id):
    conn = sqlite3.connect('amazon_data.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM amazon_data WHERE id=?",(id,)).fetchall()
    return jsonify({'data':data})
    

if  __name__ == '__main__':
    app.run(debug=True)
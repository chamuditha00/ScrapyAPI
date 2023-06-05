import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sqlite3

# Read the datasets.csv file for training the model
data_train = pd.read_csv("datasets.csv")

# Select the relevant columns for training the model
train = data_train.drop(['index','merchantid',
                        'meanproductprices', 'meanretailprices', 'averagediscount',
                        'meandiscount', 'totalurgencycount',
                        'urgencytextrate'], axis=1)

# Split the data into features (X) and target (Y)
X_train = train.drop(['rank'], axis=1)
Y_train = train['rank']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, test_size=0.3, random_state=2)

# Train the linear regression model
regr = LinearRegression()
regr.fit(X_train, Y_train)

# Read the amazon.csv file for ranking
data_amazon = pd.read_csv("amazon.csv")

# Select the relevant columns for ranking
test = data_amazon.drop(['index','merchantid',
                        'meanproductprices', 'meanretailprices', 'averagediscount',
                        'meandiscount', 'totalurgencycount',
                        'urgencytextrate'], axis=1)

# Get the predicted rankings for the test data
ranked_data = data_amazon.copy()
ranked_data['rank'] = regr.predict(test)

# Sort the data by rank in descending order
ranked_data.sort_values(by='rank', ascending=False, inplace=True)

# Reset the index of the ranked data
ranked_data.reset_index(drop=True, inplace=True)

# Create a SQLite connection and cursor
conn = sqlite3.connect('ranked_data.db')
cursor = conn.cursor()

# Create a table for the ranked data
cursor.execute('''CREATE TABLE IF NOT EXISTS ranked_data (
                    title TEXT,
                    price REAL,
                    rating REAL,
                    reviews INTEGER,
                    availability TEXT,
                    rank REAL)''')

# Insert the ranked data into the SQLite table
for _, row in ranked_data.iterrows():
    cursor.execute("INSERT INTO ranked_data VALUES (?, ?, ?, ?, ?, ?)",
                (row['title'], row['price'], row['rating'], row['reviews'], row['availability'], row['rank']))

# Commit the changes and close the connection
conn.commit()
conn.close()

# Start the Flask API to serve the ranked data
import subprocess

subprocess.Popen(["python", "flask.py"])

import sqlite3
import pandas as pd


def rank_item_category():
    conn = sqlite3.connect('amazon_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM amazon_data")
    categories = cursor.fetchall()
    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], "link":[], "image_url":[], "category":[], "rank":[]}

    for category in categories:
        category = category[0]  # Extract the category from the tuple
        print(f"Ranking items for category: {category}")

    # Retrieve data for the specified category
        query = f"SELECT * FROM amazon_data WHERE category = '{category}'"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(dict(zip(columns, row)))
        for row in data:
            print("title : " + row[1])
            print("category : " + row[8])
            print("imageUrl : " + row[7])
            print("url : " + row[6])
            price = convert_price(row[2])
            print("price : " + str(price))
            rating = convert_review_count(row[4])
            print("ratings : "+ str(rating))
            rate = convert_review_rate(row[3])
            print("rate : "+ str(rate))
            availability = row[5]
            print("availability : "+ str(check_availability(availability)))
            rank_score = ((-0.1*price)+ (0.5 * rating) +(0.1 * rate) )* check_availability(availability)
            if(rank_score > 0):
                d["title"].append(row[1])
                d["price"].append(row[2])
                d["rating"].append(row[3])
                d["reviews"].append(row[4])
                d["availability"].append(row[5])
                d["link"].append(row[6])
                d["image_url"].append(row[7])
                d["category"].append(row[8])
                d["rank"].append(rank_score)
            print("rank_score : "+ str(rank_score))
    #create dataframe
    amazon_df = pd.DataFrame.from_dict(d)
    #save to csv
    amazon_df.to_csv("amazon_ranked.csv", header=True, index=False)

    conn_ranks =  sqlite3.connect("amazon_rank.db")
    #save to db
    amazon_df.to_sql('amazon_ranked', conn_ranks, if_exists='replace', index=False)
    conn_ranks.close()
    print("Done")
    conn.close()


def convert_price(price):
    # Assuming price is in the format "$xx.xx"
    price_value = float(price.replace('$', ''))
    return price_value
def convert_review_rate(rate):
    # Assuming rate is in the format "x out of y"
    try:
        value = float(rate.split()[0])
    except(ValueError, TypeError, AttributeError):
        value = 0.0000001

    converted_rate = value
    return converted_rate

def convert_review_count(ratings):
    # Assuming rating count is in the format "x ratings"
    try:
        print("ratings : "+ str(ratings))
        value = int(ratings.replace(',', '').split()[0])
    except(ValueError, TypeError, AttributeError):
        value = 1
    
    converted_ratings = value
    return converted_ratings

#cehck availability
def check_availability(availability):
    try:
        if "In Stock" in availability:
            return 1
        elif "in stock" in availability:
            return 1
        else:
            return 0
    except(ValueError, TypeError, AttributeError):
        return 0

rank_item_category()


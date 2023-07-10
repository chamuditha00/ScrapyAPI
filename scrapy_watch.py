from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3

#function to get the title of the product
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

# Function to extract product image URL
def get_image_url(soup):
    try:
        image = soup.find("div", attrs={'id': 'imgTagWrapperId'})
        image_url = image.find("img")["src"]
    except AttributeError:
        image_url = ""
    return image_url

if __name__ == '__main__':

    # add your user agent  put your agent when use it
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37', 'Accept-Language': 'en-US, en;q=0.5'})

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], "link":[], "image_url":[],"category":"watch"}

    # The webpage URL
    for i in range(1,3):
        print("done done watch")
        URL = f"https://us.amazon.com/s?k=watch&crid=3D72CH8G1PIYQ&qid=1686149044&sprefix=watc%2Caps%2C427&ref=sr_pg_{i}"
        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
        
        # Store the links
        links_list = []
        # Loop for extracting links from Tag Objects
        for link in links:
                links_list.append(link.get('href'))
                
                

        
        
        # Loop for extracting product details from each link 
        for link in links_list:
        
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            print("done")
            d['price'].append(get_price(new_soup))
            print("done")
            d['rating'].append(get_rating(new_soup))
            print("done")
            d['reviews'].append(get_review_count(new_soup))
            print("done")
            d['availability'].append(get_availability(new_soup))
            print("done")
            d['link'].append("https://www.amazon.com" + link)
            print("done")
            d['image_url'].append(get_image_url(new_soup))
            print("done")
            print("watch" + str(i) + "done")
            i+=1
            if i>6:
                print(d)
                i = 0
                break



    #create dataframe
    amazon_df = pd.DataFrame.from_dict(d)
    #drop empty rows
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    #save to csv
    amazon_df.to_csv("amazon_watch.csv", header=True, index=False)
    if(amazon_df.empty):
        print("empty")
    else:
        #READ CSV
        df = pd.read_csv('amazon_watch.csv')
        #remove white space from column names
        df.columns = df.columns.str.strip()
        #create database
        conn =  sqlite3.connect("amazon_data.db")
        #create table
        df.to_sql("amazon_data", conn, if_exists='append')
        #close connection
        conn.close()
        

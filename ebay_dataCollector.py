import requests
import csv

# eBay API endpoint and parameters
url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json',
}
params = {
    'q': 'your_search_query',
    'limit': 100,  # Number of items to fetch
    'sort': 'price'  # Sort by price in ascending order
}

# Send GET request to eBay API
response = requests.get(url, headers=headers, params=params)
data = response.json()

# Extract relevant data from the response
items = data['itemSummaries']

# Create CSV file and write data
filename = 'ebay_data.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['Title', 'Price', 'Rating', 'Reviews', 'Image URL', 'Link'])

    # Write data rows
    for item in items:
        title = item['title']
        price = item['price']['value']
        rating = item['seller']['feedbackPercentage']
        reviews = item['seller']['feedbackScore']
        image_url = item['image']['imageUrl']
        link = item['itemWebUrl']
        writer.writerow([title, price, rating, reviews, image_url, link])

print(f'Data saved to {filename}.')

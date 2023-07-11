# Amazon Web Scraping and API

This project includes two main components: web scraping Amazon product data and providing an API to access the scraped data. The web scraping code collects product information from Amazon search results, while the Flask API serves as an interface to retrieve the scraped data from an SQLite database.

## Prerequisites

- Python 3.6 or higher
- Required Python packages: `Flask`, `BeautifulSoup`, `pandas`, `numpy`, `sqlite3`

## Installation

1. Clone the repository:

   
   git clone https://github.com/chamuditha00/ScrapyAPI.git


## project description
This project includes a scraping script and a Flask API.

The scraping script (scrapy.py) is responsible for scraping data from a website and storing it in a SQLite database.

The Flask API (flaskapi.py) provides endpoints to access the scraped data from the database.

### Running the Project

1. Run the main.py file to start the scraping script and Flask API.
2. The scraping script will run initially and then every 24 hours.
3. The Flask API will be available at http://localhost:5000/.
4. Use the provided endpoints to access the scraped data.

### API Endpoints

- GET /app: Get all data from the database.
- GET /app/{title}: Get data by product title.
- GET /app/{price}: Get data by product price.
- GET /app/{id}: Get data by product ID.

* Make requests to these endpoints using a tool like cURL or a web browser. The API will return the requested data in JSON format.

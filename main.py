import subprocess
import time

# Function to run the scraping script
def run_scraping_script():
    try:
        subprocess.run(["python", "scrapy_perfume.py"])
        subprocess.run(["python", "scrapy_sunCream.py"])
        subprocess.run(["python", "scrapy_watch.py"])
        subprocess.run(["python", "rank_data.py"])
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)

# Run the scraping script initially
run_scraping_script()

# Run the Flask application
subprocess.Popen(["python", "flaskapi.py"])

# Wait for 24 hours
time.sleep(60)
print("started")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import os
import sqlalchemy
from dotenv import load_dotenv
import datetime

load_dotenv()

def scrape_uk_urban_areas():
    url = "https://en.wikipedia.org/wiki/List_of_urban_areas_in_the_United_Kingdom"
    
    # Set up Chrome options (headless mode is recommended for scraping)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    
    # Initialize the driver. This assumes you have chromedriver installed and in your PATH.
    # You might need to specify the path: webdriver.Chrome(service=Service('/path/to/chromedriver'), options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # Locate the table using CSS selectors
        # Wikipedia tables typically use 'wikitable' and 'sortable' classes
        table = driver.find_element(By.CSS_SELECTOR, "table.wikitable.sortable")
        
        # Get headers to find the correct column index
        headers = table.find_elements(By.TAG_NAME, "th")
        
        target_column = "Primary subdivisions"
        col_index = -1
        
        for i, header in enumerate(headers):
            if target_column in header.text:
                col_index = i
                break
        
        if col_index == -1:
            print(f"Column '{target_column}' not found.")
            return []
            
        primary_subdivisions = []
        
        # Get all rows in the table body (skipping header if necessary, though wikitable usually separates thead/tbody)
        # We can find all rows and just filter those that have 'td' elements
        rows = table.find_elements(By.TAG_NAME, "tbody")
        # rows1 = table.find_elements(By.TAG_NAME, "tr")
        # rows2 = table.find_elements(By.TAG_NAME, "td")
        # print([row.text for row in rows2])
        seed = 4
        locs = ""
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            cells1 = [cell.text for cell in cells]
            # for cel in cells1:
            while seed + 6 <= len(cells1):
                locs += cells1[seed] + ", "
                seed += 6
            locs += cells1[seed]
            locs = locs.replace("[note 5]", "")
            locs = locs.replace('"', "")
        locs = locs.split(", ")
        # print(locs)
        print(f"Found {len(locs)} items:")
        print("-" * 30)
        print(locs)
        return locs

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        # Always close the browser
        driver.quit()

def create_urban_areas_table(database_name: str="postgres"):
    load_dotenv()
    sqlalchemy_engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{database_name}')
    metadata = sqlalchemy.MetaData()

    sqlalchemy.Table(
        'urban_areas',
        metadata,
        sqlalchemy.Column('city_town_name', sqlalchemy.String, primary_key=True),
        sqlalchemy.Column('last_updated', sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    )

    metadata.create_all(sqlalchemy_engine)

def update_urban_areas_table(database_name: str="postgres"):
    load_dotenv()
    sqlalchemy_engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{database_name}')
    connection = sqlalchemy_engine.connect()
    metadata = sqlalchemy.MetaData()

    urban_areas = sqlalchemy.Table('urban_areas', metadata, autoload_with=sqlalchemy_engine)

    scraped_areas = scrape_uk_urban_areas()

    for area in scraped_areas:
        query = sqlalchemy.select(urban_areas).where(urban_areas.c.city_town_name == area)
        # print(connection.execute(query).fetchone())
        if connection.execute(query).fetchone() is None:
            ins = urban_areas.insert().values(city_town_name=area, last_updated=datetime.datetime.now())
            connection.execute(ins)
    connection.commit()

if __name__ == "__main__":
    create_urban_areas_table()
    update_urban_areas_table()
    # results = scrape_uk_urban_areas()
    
    # print(f"Found {len(results)} items:")
    # print("-" * 30)
    # print(results)

# import requests
# from bs4 import BeautifulSoup
# import re

# def scrape_uk_urban_areas():
#     url = "https://en.wikipedia.org/wiki/List_of_urban_areas_in_the_United_Kingdom"
    
#     try:
#         # Fetch the page content
#         response = requests.get(url)
#         response.raise_for_status()  # Check for HTTP errors
        
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Find the specific table. 
#         # Wikipedia tables typically use 'wikitable' and 'sortable' classes.
#         table = soup.find('table', {'class': ['wikitable', 'sortable']})
        
#         if not table:
#             print("Could not find the table.")
#             return []

#         # Find the index of the "Primary subdivisions" column
#         headers = [th.get_text(strip=True) for th in table.find_all('th')]
        
#         target_column = "Primary subdivisions"
#         col_index = -1
        
#         # Handle cases where the header might contain footnotes or extra spaces
#         for i, header in enumerate(headers):
#             if target_column in header:
#                 col_index = i
#                 break
        
#         if col_index == -1:
#             print(f"Column '{target_column}' not found in table headers.")
#             return []

#         primary_subdivisions = []
        
#         # Iterate through table rows (skip the header row)
#         rows = table.find_all('tr')[1:]
        
#         for row in rows:
#             cells = row.find_all('td')
            
#             # Ensure the row has enough cells (some rows might be empty or formatting rows)
#             if len(cells) > col_index:
#                 cell_content = cells[col_index].get_text(strip=True)
                
#                 # specific cleanup: Wikipedia often adds reference links like [1]
#                 # We use regex to remove brackets and their content
#                 clean_name = re.sub(r'\[.*?\]', '', cell_content)
                
#                 if clean_name:
#                     primary_subdivisions.append(clean_name)

#         return primary_subdivisions

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching URL: {e}")
#         return []

# if __name__ == "__main__":
#     results = scrape_uk_urban_areas()
    
#     print(f"Found {len(results)} items:")
#     print("-" * 30)
#     print(results)
    
#     # Optional: Print them line by line for better readability
#     # for item in results:
#     #     print(item)
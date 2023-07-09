from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

def perform_search(query):
    print(f"Performing search for '{query}'...")
    driver.get("https://www.google.com")  # Open Google in the browser
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )  # Wait for the search box element to be located
        search_box.send_keys(query)  # Enter the search query
        search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search
        print("Waiting for search results to load...")
        time.sleep(2)  # Wait for the search results to load
    except Exception as e:
        print(f"Error performing search: {e}")

def extract_search_results():
    print("Extracting search results...")
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")  # Find the search result elements
    for i, result in enumerate(search_results, start=1):
        try:
            title = result.find_element(By.CSS_SELECTOR, "h3").text  # Extract the title
            link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")  # Extract the URL
            print(f"Result {i}: {title} ({link})")  # Process the search result as desired
        except Exception as e:
            print(f"Error extracting result {i}: {e}")

query = input("Enter your search query: ")
perform_search(query)
extract_search_results()

print("Closing browser...")
driver.quit()
print("Done.")

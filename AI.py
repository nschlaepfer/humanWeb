import os
from dotenv import load_dotenv
import openai
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()  # take environment variables from .env.

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

driver = webdriver.Chrome()

# Global variable for filename
filename = None

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

def extract_search_results(query):
    global filename
    print("Extracting search results...")
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")  # Find the search result elements
    os.makedirs("Searches", exist_ok=True)  # Create the "Searches" directory if it doesn't exist
    filename = os.path.join("Searches", f"{query}_{time.time()}.txt")  # Store the filename
    links = []
    with open(filename, "w") as f:  # Open the output file
        for i, result in enumerate(search_results, start=1):
            try:
                title = result.find_element(By.CSS_SELECTOR, "h3").text  # Extract the title
                link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")  # Extract the URL
                print(f"Result {i}: {title} ({link})")  # Process the search result as desired
                f.write(f"Result {i}: {title} ({link})\n")  # Write the result to the file
                links.append(link)
            except Exception as e:
                print(f"Error extracting result {i}: {e}")
        for link in links:
            print("Extracting page content...")
            driver.set_page_load_timeout(20)  # Set page load timeout
            try:
                driver.get(link)  # Navigate to the page
                page_content = driver.find_element(By.TAG_NAME, "body").text  # Extract the text from the body of the page
                print(page_content)  # Print the page content
                f.write(f"Page Content:\n{page_content}\n")  # Write the page content to the file
                print("\n---\n")  # Print a separator
                f.write("\n---\n")  # Write a separator to the file
            except Exception as e:
                print(f"Error loading page {link}: {e}")
            time.sleep(2)  # Wait for the search results to load again

def process_results_with_gpt3(query):
    global filename
    print("Processing results with GPT-3...")
    try:
        with open(filename, "r+") as f:  # Use the stored filename
            content = f.read()
            messages = [{'role': 'system', 'content': content}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            gpt_response = response.choices[0].message['content'].strip()
            print(f"GPT-3 Response: {gpt_response}")
            f.write(f"\nGPT-3 Response: {gpt_response}\n")  # Write the GPT-3 response to the file
    except FileNotFoundError:
        print(f"Could not find file: {filename}")

query = input("Enter your search query: ")
perform_search(query)
extract_search_results(query)
process_results_with_gpt3(query)

print("Closing browser...")
driver.quit()
print("Done.")




# import os
# from dotenv import load_dotenv
# import openai
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# load_dotenv()  # take environment variables from .env.

# # Get OpenAI API key from environment variable
# openai.api_key = os.getenv('OPENAI_API_KEY')

# driver = webdriver.Chrome()

# # Global variable for filename
# filename = None

# def perform_search(query):
#     print(f"Performing search for '{query}'...")
#     driver.get("https://www.google.com")  # Open Google in the browser
#     try:
#         search_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.NAME, "q"))
#         )  # Wait for the search box element to be located
#         search_box.send_keys(query)  # Enter the search query
#         search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search
#         print("Waiting for search results to load...")
#         time.sleep(2)  # Wait for the search results to load
#     except Exception as e:
#         print(f"Error performing search: {e}")

# def extract_search_results(query):
#     global filename
#     print("Extracting search results...")
#     search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")  # Find the search result elements
#     os.makedirs("Searches", exist_ok=True)  # Create the "Searches" directory if it doesn't exist
#     filename = os.path.join("Searches", f"{query}_{time.time()}.txt")  # Store the filename
#     with open(filename, "w") as f:  # Open the output file
#         for i, result in enumerate(search_results, start=1):
#             try:
#                 title = result.find_element(By.CSS_SELECTOR, "h3").text  # Extract the title
#                 link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")  # Extract the URL
#                 print(f"Result {i}: {title} ({link})")  # Process the search result as desired
#                 f.write(f"Result {i}: {title} ({link})\n")  # Write the result to the file
#                 print("Extracting page content...")
#                 driver.get(link)  # Navigate to the page
#                 page_content = driver.find_element(By.TAG_NAME, "body").text  # Extract the text from the body of the page
#                 print(page_content)  # Print the page content
#                 f.write(f"Page Content:\n{page_content}\n")  # Write the page content to the file
#                 print("\n---\n")  # Print a separator
#                 f.write("\n---\n")  # Write a separator to the file
#                 driver.back()  # Go back to the search results
#                 time.sleep(2)  # Wait for the search results to load again
#             except Exception as e:
#                 print(f"Error extracting result {i}: {e}")

# def process_results_with_gpt3(query):
#     global filename
#     print("Processing results with GPT-3...")
#     try:
#         with open(filename, "r+") as f:  # Use the stored filename
#             content = f.read()
#             messages = [{'role': 'system', 'content': content}]
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo-16k",
#                 messages=messages
#             )
#             gpt_response = response.choices[0].message['content'].strip()
#             print(f"GPT-3 Response: {gpt_response}")
#             f.write(f"\nGPT-3 Response: {gpt_response}\n")  # Write the GPT-3 response to the file
#     except FileNotFoundError:
#         print(f"Could not find file: {filename}")

# query = input("Enter your search query: ")
# perform_search(query)
# extract_search_results(query)
# process_results_with_gpt3(query)

# print("Closing browser...")
# driver.quit()
# print("Done.")


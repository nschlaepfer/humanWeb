import os
from dotenv import load_dotenv
import openai
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from QA import create_qa

load_dotenv()  # take environment variables from .env.

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ask user if they want to run headless
headless_option = input("Do you want to run the browser headlessly? (yes/no): ").lower()

options = webdriver.ChromeOptions()
if headless_option == 'yes':
    options.add_argument('headless')

driver = webdriver.Chrome(options=options)

# Global variable for filename
filename = None
summary_filename = None

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

def extract_search_results(query, num_results):
    global filename
    global summary_filename
    print("Extracting search results...")
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")[:num_results]  # Limit to user-specified number of results
    os.makedirs("Searches", exist_ok=True)  # Create the "Searches" directory if it doesn't exist
    filename = os.path.join("Searches", f"{query}_{time.time()}.txt")  # Store the filename
    summary_filename = os.path.join("Searches", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename
    links = []
    with open(filename, "w") as f:  # Open the output file
        for i, result in enumerate(search_results, start=1):
            try:
                title = result.find_element(By.CSS_SELECTOR, "h3").text  # Extract the title
                link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")  # Extract the URL
                print(f"Result {i}: {title} ({link})")  # Process the search result as desired
                f.write(f"Result {i}: {title} ({link})\n")  # Write the result to the file
                links.append((title, link))  # Store the title and link together
            except Exception as e:
                print(f"Error extracting result {i}: {e}")
        for title, link in links:
            print("Extracting page content...")
            driver.set_page_load_timeout(20)  # Set page load timeout
            try:
                driver.get(link)  # Navigate to the page
                page_content = driver.find_element(By.TAG_NAME, "body").text  # Extract the text from the body of the page
                print(page_content)  # Print the page content
                f.write(f"Page Content:\n{page_content}\n")  # Write the page content to the file
                print("\n---\n")  # Print a separator
                f.write("\n---\n")  # Write a separator to the file
                process_results_with_gpt3(title, link, page_content, summary_filename)  # Process the page content with GPT-3
            except Exception as e:
                print(f"Error loading page {link}: {e}")
            time.sleep(2)  # Wait for the search results to load again

def process_results_with_gpt3(title, link, content, summary_filename):
    print("Processing results with GPT-3...")
    try:
        system_prompt = "Given the following information, extract unique and interesting facts. If the information is already known in the content. Please do not repeat it.\n\nTitle: " + title + "\n\nLink: " + link + "\n\nContent:"
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': content}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        gpt_response = response.choices[0].message['content'].strip()
        print(f"GPT-3 Response: {gpt_response}")
        with open(summary_filename, "a") as sf:  # Open the summary file
            sf.write(f"\n## {title}\n\nSource: [{link}]({link})\n\nGPT-3 Summary: {gpt_response}\n")  # Write the GPT-3 summary to the summary file
    except FileNotFoundError:
        print(f"Could not find file: {summary_filename}")

def create_report(query):
    global summary_filename
    print("Creating report...")
    try:
        with open(summary_filename, "r") as sf:  # Open the summary file
            summaries = sf.read()
            messages = [{'role': 'system', 'content': summaries}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            gpt_report = response.choices[0].message['content'].strip()
            print(f"GPT-3 Report: {gpt_report}")
            os.makedirs("Reports", exist_ok=True)  # Create the "Reports" directory if it doesn't exist
            report_filename = os.path.join("Reports", f"Report_{query}_{time.time()}.md")  # Store the report filename
            with open(report_filename, "w") as rf:  # Open the report file
                rf.write(f"# GPT-3 Report:\n\n{gpt_report}\n\nReport generated by: Momo AI\n")  # Write the GPT-3 report to the report file
    except FileNotFoundError:
        print(f"Could not find file: {summary_filename}")

num_results = int(input("Enter the number of search results you want to process: "))
query = input("Enter your search query: ")

perform_search(query)
extract_search_results(query, num_results)
create_report(query)
create_qa(query, summary_filename)

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
# from QA import create_qa

# load_dotenv()  # take environment variables from .env.

# # Get OpenAI API key from environment variable
# openai.api_key = os.getenv('OPENAI_API_KEY')

# driver = webdriver.Chrome()

# # Global variable for filename
# filename = None
# summary_filename = None

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

# def extract_search_results(query, num_results):
#     global filename
#     global summary_filename
#     print("Extracting search results...")
#     search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")[:num_results]  # Limit to user-specified number of results
#     os.makedirs("Searches", exist_ok=True)  # Create the "Searches" directory if it doesn't exist
#     filename = os.path.join("Searches", f"{query}_{time.time()}.txt")  # Store the filename
#     summary_filename = os.path.join("Searches", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename
#     links = []
#     with open(filename, "w") as f:  # Open the output file
#         for i, result in enumerate(search_results, start=1):
#             try:
#                 title = result.find_element(By.CSS_SELECTOR, "h3").text  # Extract the title
#                 link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")  # Extract the URL
#                 print(f"Result {i}: {title} ({link})")  # Process the search result as desired
#                 f.write(f"Result {i}: {title} ({link})\n")  # Write the result to the file
#                 links.append(link)
#             except Exception as e:
#                 print(f"Error extracting result {i}: {e}")
#         for link in links:
#             print("Extracting page content...")
#             driver.set_page_load_timeout(20)  # Set page load timeout
#             try:
#                 driver.get(link)  # Navigate to the page
#                 page_content = driver.find_element(By.TAG_NAME, "body").text  # Extract the text from the body of the page
#                 print(page_content)  # Print the page content
#                 f.write(f"Page Content:\n{page_content}\n")  # Write the page content to the file
#                 print("\n---\n")  # Print a separator
#                 f.write("\n---\n")  # Write a separator to the file
#                 process_results_with_gpt3(page_content, summary_filename)  # Process the page content with GPT-3
#             except Exception as e:
#                 print(f"Error loading page {link}: {e}")
#             time.sleep(2)  # Wait for the search results to load again


# def process_results_with_gpt3(content, summary_filename):
#     print("Processing results with GPT-3...")
#     try:
#         messages = [{'role': 'system', 'content': content}]
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo-16k",
#             messages=messages
#         )
#         gpt_response = response.choices[0].message['content'].strip()
#         print(f"GPT-3 Response: {gpt_response}")
#         with open(summary_filename, "a") as sf:  # Open the summary file
#             sf.write(f"\nGPT-3 Summary: {gpt_response}\n")  # Write the GPT-3 summary to the summary file
#     except FileNotFoundError:
#         print(f"Could not find file: {summary_filename}")

# def create_report(query):
#     global summary_filename
#     print("Creating report...")
#     try:
#         with open(summary_filename, "r") as sf:  # Open the summary file
#             summaries = sf.read()
#             messages = [{'role': 'system', 'content': summaries}]
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo-16k",
#                 messages=messages
#             )
#             gpt_report = response.choices[0].message['content'].strip()
#             print(f"GPT-3 Report: {gpt_report}")
#             os.makedirs("Reports", exist_ok=True)  # Create the "Reports" directory if it doesn't exist
#             report_filename = os.path.join("Reports", f"Report_{query}_{time.time()}.txt")  # Store the report filename
#             with open(report_filename, "w") as rf:  # Open the report file
#                 rf.write(f"GPT-3 Report:\n{gpt_report}\n")  # Write the GPT-3 report to the report file
#     except FileNotFoundError:
#         print(f"Could not find file: {summary_filename}")

# num_results = int(input("Enter the number of search results you want to process: "))
# query = input("Enter your search query: ")

# perform_search(query)
# extract_search_results(query, num_results)
# create_report(query)
# create_qa(query, summary_filename)

# print("Closing browser...")
# driver.quit()
# print("Done.")





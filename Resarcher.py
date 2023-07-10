#Working well. Dont change it. for now.

import os
import json
import time

from dotenv import load_dotenv
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from QA import create_qa

load_dotenv()  # take environment variables from .env.

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

# Create a list to store all the summaries
all_summaries = []

# Create a debug log file
debug_log = open("debug_log.txt", "w")

def generate_additional_queries(query):
    print("Generating additional queries with GPT-3...")
    system_prompt = "Given this query, come up with 10 more queries that will help get the most information or complete a task in order."
    messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
    )
    additional_queries = response.choices[0].message['content'].strip().split('\n')
    # Write to debug log
    debug_log.write(f"Generated additional queries: {additional_queries}\n")
    return additional_queries

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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
        )  # Wait for the search results to load
    except Exception as e:
        print(f"Error performing search: {e}")
        return None
    return driver.find_elements(By.CSS_SELECTOR, "div.g")

def extract_search_results(query, num_results, filename, summary_filename):
    print("Extracting search results...")
    search_results = perform_search(query)[:num_results]  # Limit to user-specified number of results
    if search_results is None:
        print("No search results found.")
        return
    os.makedirs("Searches", exist_ok=True)  # Create the "Searches" directory if it doesn't exist
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
                gpt_response = process_results_with_gpt3(title, link, page_content, summary_filename)  # Process the page content with GPT-3
                if gpt_response is not None:
                    print(f"GPT-3 Response: {gpt_response}")
            except Exception as e:
                print(f"Error loading page {link}: {e}")

def process_results_with_gpt3(title, link, content, summary_filename):
    print("Processing results with GPT-3...")
    try:
        system_prompt = "Given the following information, extract unique and interesting facts. If the information is already known in the content. Please do not repeat it, look at the context given."
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': content}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        gpt_response = response.choices[0].message['content'].strip()
        summary = f"\n## {title}\n\nSource: [{link}]({link})\n\nGPT-3 Summary: {gpt_response}\n"
        all_summaries.append(summary)  # Add the summary to the list
        with open(summary_filename, "a") as sf:  # Open the summary file
            sf.write(summary)  # Write the GPT-3 summary to the summary file
    except FileNotFoundError:
        print(f"Could not find file: {summary_filename}")
        return None
    return gpt_response

def create_report(query, initial_query):
    print("Creating report...")
    summaries = "\n".join(all_summaries)  # Combine all the summaries into a single string
    system_prompt = "Given the following information, create a report with the information and be sure to cite sources. This a professional report."
    messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': summaries}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
    )
    gpt_report = response.choices[0].message['content'].strip()
    print(f"GPT-3 Report: {gpt_report}")
    os.makedirs(f"Reports/{initial_query}", exist_ok=True)  # Create the "Reports" directory if it doesn't exist
    report_filename = os.path.join("Reports", initial_query, f"Report_{query}_{time.time()}.md")  # Store the report filename
    with open(report_filename, "w") as rf:  # Open the report file
        rf.write(f"# GPT-3 Report:\n\n{gpt_report}\n\nReport generated by: Momo AI\n")  # Write the GPT-3 report to the report file
        print(f"Report saved to: {report_filename}")   

num_results = int(input("Enter the number of search results you want to process: "))
initial_query = input("Enter your initial search query: ")

# Create directories for the initial query
os.makedirs(f"Searches/{initial_query}", exist_ok=True)
os.makedirs(f"Reports/{initial_query}", exist_ok=True)

additional_queries = generate_additional_queries(initial_query)
all_queries = [initial_query] + additional_queries


# Set a limit for the number of additional queries
MAX_ADDITIONAL_QUERIES = 0
# Set a limit for the number of iterations
MAX_ITERATIONS = 5


# Keep track of the number of additional queries
num_additional_queries = 0
# Keep track of the number of iterations
num_iterations = 0

for query in all_queries:
    # Debug: print the current iteration and query
    print(f"Iteration {num_iterations + 1}, processing query: '{query}'")

    filename = os.path.join(f"Searches/{initial_query}", f"{query}_{time.time()}.txt")  # Store the filename
    summary_filename = os.path.join(f"Searches/{initial_query}", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename

    extract_search_results(query, num_results, filename, summary_filename)
    create_report(query, initial_query)
    qa_query = create_qa(query, summary_filename)

    if qa_query != query and num_additional_queries < MAX_ADDITIONAL_QUERIES:
        # If the result of create_qa is a new query and we haven't reached the limit, you can add it to all_queries and process it
        all_queries.append(qa_query)
        num_additional_queries += 1

        # Debug: print the new query and the updated total number of queries
        print(f"New query added: '{qa_query}', total queries: {len(all_queries)}")

        # Update the query variable
        query = qa_query

    num_iterations += 1
    if num_iterations >= MAX_ITERATIONS:
        # If the loop has run for more than MAX_ITERATIONS, break the loop
        print(f"Reached the maximum number of iterations ({MAX_ITERATIONS}), breaking the loop.")
        break

print("Closing browser...")
driver.quit()
print("Done.")

# Close the debug log file at the end
debug_log.close()

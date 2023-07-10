# This is the multi threaded version of the code

import os
import time

from dotenv import load_dotenv
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from QA import create_qa
from gpt3_functions import generate_additional_queries, create_report, extract_search_results

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

num_results = int(input("Enter the number of search results you want to process (rec. 2): "))
initial_query = input("Enter your request. Not a google. (gpt will decide what to google): ")

# Create directories for the initial query
os.makedirs(f"Searches/{initial_query}", exist_ok=True)
os.makedirs(f"Reports/{initial_query}", exist_ok=True)

num_queries = int(input("Enter the number of steps (number of queries) Default 3: "))
additional_queries = generate_additional_queries(initial_query, num_queries, debug_log, initial_query)

# Define all_queries here
all_queries = [initial_query] + additional_queries

# Set a limit for the number of additional queries
MAX_ADDITIONAL_QUERIES = 0
# Set a limit for the number of iterations
MAX_ITERATIONS = num_queries  # Set MAX_ITERATIONS to num_queries

# Keep track of the number of additional queries
num_additional_queries = 0
# Keep track of the number of iterations
num_iterations = 0

for query in all_queries:

    # Debug: print the current iteration and query
    print(f"Iteration {num_iterations + 1}, processing query: '{query}'")

    filename = os.path.join(f"Searches/{initial_query}", f"{query}_{time.time()}.txt")  # Store the filename
    summary_filename = os.path.join(f"Searches/{initial_query}", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename

    links = extract_search_results(query, num_results, filename, summary_filename, driver)

    summaries = []
    for title, link, snippet in links:
        summary = process_results_with_gpt3(title, link, snippet, summary_filename, initial_query)
        summaries.append(summary)
    
    report = create_report(query, initial_query, summaries)
    all_summaries.append(report)

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


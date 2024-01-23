
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
from retry_decorator import retry_on_service_unavailable


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



# Define available models
available_models = {
    'GPT-4 Vision (Preview)': 'gpt-4-vision-preview',
    'GPT-4 (Preview)': 'gpt-4-1106-preview',
    'GPT-3.5 Turbo (1106)': 'gpt-3.5-turbo-1106'
}

# Default model
default_model = 'gpt-4-vision-preview'

def select_model():
    print("Please select an AI model to use:")
    for i, model_name in enumerate(available_models, start=1):
        print(f"{i}. {model_name}")
    print(f"Press Enter for the default model: {list(available_models.keys())[0]}")
    
    choice = input("Enter the number of the model you want to use: ").strip()
    if choice.isdigit() and int(choice) in range(1, len(available_models) + 1):
        selected_model = list(available_models.values())[int(choice) - 1]
    else:
        selected_model = default_model
    print(f"You have selected: {selected_model}")
    return selected_model

# At the start of your main script
model_id = select_model()  # This will prompt the user to select a model


def generate_additional_queries(query, num_queries, model_id):
    print("Generating additional queries with {model_id}...")
    system_prompt = f"Given this query, come up with {num_queries} more queries that will help get the most information or complete a task in order. Come up with the most consise and clear queries for google."
    messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]
    response = openai.ChatCompletion.create(
        model=model_id, #changed since it is smaller
        messages=messages
    )
    additional_queries = response.choices[0].message['content'].strip().split('\n')[:num_queries]
    # Write to debug log
    debug_log.write(f"Generated additional queries: {additional_queries}\n")
    return additional_queries



# Ideas to update this function and project - then from that make new project about vision seeing computer and using mouse.:
# - Add more websitese to the list to use for like bing.com, duckduckgo.com, etc.
# - Add more error handling
# - Add more ways to process the search results (e.g. extract the title, link, and description)
# - Add more ways to process the page content (e.g. extract the text from the page)
# - Add more ways to search. Use GPT-4-vision-preview to search for image. By having a screen shot of tope 10 images and using GPT-4-vision-preview to help navigate and build a report.
# Use GPT-4-vision-preview to help navigate and build a report. for all the functions. I also want to eleminate the need for pre made actions  and use GPT-4-vision-preview to handle the web navigation.
# This needs to allow GPT-4-vision-preview to handle the web navigation by using the screen shot of where its at and assessing the page (having it select links and click on them).
# a nice mix of both where vision and text input are used with selenium to navigate the web.
# I possibly want to add in Tree of thouht (very hard to do).



def perform_search(query):
    print(f"Performing search for '{query}'...")
    driver.get("https://www.google.com")  # Open Google in the browser add more options

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )  # Wait for the search box element to be located
        search_box.send_keys(query)  # Enter the search query
        search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search
        print("Waiting for search results to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
        )  # Wait for the search results to load
    except Exception as e:
        print(f"Error performing search: {e}")
        import traceback
        traceback.print_exc()  # Add this line
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
                
                # Skip processing if the link points to a YouTube video
                if "youtube.com" in link:
                    print(f"Skipping Result {i}: {title} ({link}) - YouTube videos are not supported, well not yet..")
                    continue
                
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
                if "Sorry, you have been blocked" not in page_content:  # Check if the page content indicates you've been blocked
                    gpt_response = process_results_with_gpt3(title, link, page_content, summary_filename)  # Process the page content with GPT-3
                    if gpt_response is not None:
                        print(f"humanWeb's Response: {gpt_response}")
            except Exception as e:
                print(f"Error loading page {link}: {e}")


# Using the chain of thought from smartGPT project to process the results takes alot longer.
def process_results_with_gpt3(title, link, content, summary_filename, model_id):
    print("Processing results with humanWeb...")
    try:
        system_prompt = f"Given the following information, extract unique and interesting facts and analytical infromation. Do not just summarize it. This would will be used in a upcomiing report about {initial_query}. If the information is already known in the content, please do not repeat it. Look at the context given. MUST have sources at bottom."
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': content}]
        
        response = openai.ChatCompletion.create(
            model=model_id, #changed since it is smaller
            messages=messages
        )
        time.sleep(3)
        gpt_response = response.choices[0].message['content'].strip()

        # Use the GPT-3 response as the final summary
        summary = f"\n## {title}\n\nSource: [{link}]({link})\n\nhumanWeb Summary: {gpt_response}\n"
        all_summaries.append(summary)  # Add the summary to the list
        with open(summary_filename, "a") as sf:  # Open the summary file
            sf.write(summary)  # Write the GPT-3 summary to the summary file
    except FileNotFoundError:
        print(f"Could not find file: {summary_filename}")
        return None
    return gpt_response



# THis is smartGPT 
def create_report(query, initial_query, num_results, all_summaries,model_id):
    #global all_summaries  # Declare all_summaries as global so we can modify it
    print("Creating report...")
    summaries = "\n".join(all_summaries)  # Combine all the summaries into a single string
    system_prompt = f"Given the following information, create a report with the information and be sure to cite sources inline. This a professional analytical report. This is about: {query} and part of this: {initial_query}."
    messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': summaries}]

    best_report = None
    best_score = -1

    # Generate 3 reports
    for _ in range(3):
        response = openai.ChatCompletion.create(
            model=model_id, #changed since it is smaller
            messages=messages
        )
        gpt_report = response.choices[0].message['content'].strip()

        # Researcher step
        researcher_prompt = f"You are a researcher tasked with investigating the report. You are a peer-reviewer. List the flaws and faulty logic of the report. Here are all the summaries from each page of the search made: {all_summaries}. Make sure every response has sources and inline citations. Let's work this out in a step by step way to be sure we have all the errors:"
        researcher_messages = [{'role': 'system', 'content': researcher_prompt}, {'role': 'user', 'content': gpt_report}]
        researcher_response = openai.ChatCompletion.create(
            model=model_id, #changed since it is smaller
            messages=researcher_messages
        )
        time.sleep(5)
        researcher_output = researcher_response.choices[0].message['content'].strip()

        # Resolver step
        resolver_prompt = f"You are a resolver tasked with improving the report. Print the improved report in full. Let's work this out in a step by step way to be sure we have the right report use the goal: {initial_query} and data resarched {all_summaries} to provide the best report possible.:"
        resolver_messages = [{'role': 'system', 'content': resolver_prompt}, {'role': 'user', 'content': researcher_output}]
        resolver_response = openai.ChatCompletion.create(
            model=model_id, #changed since it is smaller
            messages=resolver_messages
        )
        time.sleep(5)
        resolver_output = resolver_response.choices[0].message['content'].strip()

        # Score the resolver output (you can replace this with your own scoring function)
        score = len(resolver_output)

        # If this output is better than the current best, update the best output and score
        if score > best_score:
            best_report = resolver_output
            best_score = score

    # If the best score is below a certain threshold, restart the entire search process
    THRESHOLD = 5000  # Set the threshold here
    if best_score < THRESHOLD:
        print("\n\nReport not satisfactory, restarting the search process...")
        all_summaries = []  # Clear the all_summaries list
        # Reset other variables as necessary here
        # Call your search function here to restart the search process
        # You might need to modify your search function to return the final report
        filename = os.path.join(f"Searches/{initial_query}", f"{query}_{time.time()}.txt")  # Store the filename
        summary_filename = os.path.join(f"Searches/{initial_query}", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename
        return extract_search_results(query, num_results, filename, summary_filename)

    print(f"\n\nhumanWeb Report: {best_report}")
    os.makedirs(f"Reports/{initial_query}", exist_ok=True)  # Create the "Reports" directory if it doesn't exist
    report_filename = os.path.join("Reports", initial_query, f"Report_{query}_{str(time.time())}.md")  # Store the report filename
    with open(report_filename, "w") as rf:  # Open the report file
        rf.write(f"# humanWeb Report:\n\n{best_report}\n\nReport generated by: Oraculum AI\n")
        rf.write(f"\n\nPrompt used to generate list: {initial_query}\nSearch made for this report: {query}")
        print(f"\n\nReport saved to: {report_filename}")   

    return best_report

print("\n\n\nWelcome to humanWeb! \nThis is a tool that uses OPEN AI or Local LMs to help you search the web and create a reports.\n Results may vary. BUGS ARE EXPECTED. \n\n\n")

num_results = int(input("Number of website to visit (Default 10) :"))
initial_query = input("Enter your request. Not a google. (gpt will decide what to google): ")

# Create directories for the initial query
os.makedirs(f"Searches/{initial_query}", exist_ok=True)
os.makedirs(f"Reports/{initial_query}", exist_ok=True)
#os.makedirs(f"Reports/{initial_query}", exist_ok=True)

num_queries = int(input("Number of reports (Default 5) : "))
additional_queries = generate_additional_queries(initial_query, num_queries, model_id)

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
    print(f"\n\n\nIteration {num_iterations + 1}, processing query: '{query}'")

    filename = os.path.join(f"Searches/{initial_query}", f"{query}_{time.time()}.txt")  # Store the filename
    summary_filename = os.path.join(f"Searches/{initial_query}", f"Summary_{query}_{time.time()}.txt")  # Store the summary filename

    extract_search_results(query, num_results, filename, summary_filename)
    create_report(query, initial_query, num_results,all_summaries)
    qa_query = create_qa(query, summary_filename)

    if qa_query != query and num_additional_queries < MAX_ADDITIONAL_QUERIES:
        # If the result of create_qa is a new query and we haven't reached the limit, you can add it to all_queries and process it
        all_queries.append(qa_query)
        num_additional_queries += 1

        # Debug: print the new query and the updated total number of queries
        print(f"\n\n\nNew query added: '{qa_query}', total queries: {len(all_queries)}")

        # Update the query variable
        query = qa_query

    num_iterations += 1
    if num_iterations >= MAX_ITERATIONS:
        # If the loop has run for more than MAX_ITERATIONS, break the loop
        print(f"\n\n\nReached the maximum number of iterations ({MAX_ITERATIONS}), breaking the loop.")
        break

print("\nClosing browser...")
driver.quit()
print("\nDone.")

# Close the debug log file at the end
debug_log.close()








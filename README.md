
# Momo AI: A Research Assistant Powered by GPT-3.5-Turbo-16K 🤖

[![GitHub license](https://img.shields.io/github/license/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/network)
[![Twitter Follow](https://img.shields.io/twitter/follow/nos_ult?style=social)](https://twitter.com/nos_ult)

Momo AI is a Python program that uses GPT-3.5-Turbo-16K and Selenium to perform web searches, extract and summarize information, and generate reports based on user queries. It can also create follow-up questions based on the summaries to help the user get more information or complete a task.

![Momo AI logo](momo-ai-logo.png)

## Table of Contents 📑

- [Features](#features-)
- [Requirements](#requirements-)
- [Installation](#installation-)
- [Usage](#usage-)
  - [Websmart mode] (#websamart-mode)
  - [Researcher Mode](#researcher-mode-)
  - [Reporter Mode](#reporter-mode-)
    
- [About](#about-)
- [Possible UI](#possible-ui-)
- [Future Features](#future-features-)

## Features ✨

<div align="center">
<img src="momo-ai-progress.png" alt="Momo AI progress bar" width="500"/>
</div>

Momo AI can do the following things for you:

- Perform web searches using Google and extract the results
  - You can specify how many results you want to process for each query
  - You can see the titles and links of the results in a text file
  - You can also see the page content of each result in the same file
- Extract the page content from the result links and process it with GPT-3.5-Turbo-16K
  - Momo AI will use GPT-3.5-Turbo-16K to analyze the page content and extract the most relevant information
  - You can see the extracted information in a text file
  - You can also see a pie chart of how much information was extracted from each source
- Generate summaries of the page content using GPT-3.5-Turbo-16K
  - Momo AI will use GPT-3.5-Turbo-16K to generate concise and informative summaries of the page content
  - You can see the summaries in a text file
  - You can also see a word cloud of the most frequent words in the summaries
- Generate reports based on the summaries using GPT-3.5-Turbo-16K
  - Momo AI will use GPT-3.5-Turbo-16K to generate comprehensive and coherent reports based on the summaries
  - You can see the reports in a text file
  - You can also see a summary of the report at the beginning of the file
- Generate additional queries based on the initial query using GPT-3.5-Turbo-16K
  - Momo AI will use GPT-3.5-Turbo-16K to generate more queries that will help you get more information or complete a task related to your initial query
  - You can see the additional queries in a text file
  - You can also choose which queries you want to explore further or skip them if you are satisfied with the current results
- Generate question-answer pairs based on the summaries using GPT-3.5-Turbo-16K
  - Momo AI will use GPT-3.5-Turbo-16K to generate question-answer pairs that will test your understanding of the summaries or provide more insights
  - You can see the question-answer pairs in a text file
  - You can also interact with them using buttons and dropdown menus in the UI

- Save the search results, summaries, and reports to text files
  - Momo AI will save all the outputs to text files in the `Searches` and `Reports` directories
  - You can access them anytime and share them with others
- Run the browser headlessly or with a graphical interface
  - Momo AI can run the browser in the background or show it on the screen
  - You can choose which option you prefer depending on your needs

## Requirements 📋

To run Momo AI, you need the following:

- Python 3.6 or higher
- OpenAI API key
- Selenium Python package
- Dotenv Python package
- Chrome browser
- Chrome driver

## Installation 💻

To install Momo AI, follow these steps:

1. Clone or download this repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required packages using `pip install -r requirements.txt`.
4. Get an OpenAI API key from https://beta.openai.com/ and save it as an environment variable in a `.env` file in the project directory. The file should look like this:

```text
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

5. Download the Chrome driver from https://chromedriver.chromium.org/downloads and save it in the project directory. Make sure the driver version matches your Chrome browser version.
6. Run `python Researcher.py` or `python Reporter.py` depending on which mode you want to use.

## Usage 🚀

Momo AI has three modes: Websmart, Researcher and Reporter.


# Websmart mode 🖲️

This script is designed to generate a detailed report based on a user's query using GPT-3 and a chain of thought from the smartGPT project. Here's a step-by-step guide on how it works:

1. **User Input**: The user is prompted to enter the number of search results they want to process, their initial query, and the number of steps (queries) they want to perform.

2. **Additional Query Generation**: The script generates additional queries based on the initial query using GPT-3. These queries are designed to help gather the most information or complete a task in order.

3. **Search and Extraction**: For each query, the script performs a Google search and extracts the search results. The number of results extracted is based on the user's input. The script also navigates to each search result page and extracts the page content.

4. **Processing with GPT-3**: The script then processes the page content with GPT-3, extracting unique and interesting facts and analytical information. This information is then summarized and stored.

5. **Report Creation**: Once all queries have been processed, the script creates a report based on the summaries. The report is generated in three steps: 
   - First, a report is generated using GPT-3.
   - Then, a researcher role is simulated to investigate the report and list any flaws or faulty logic.
   - Finally, a resolver role is simulated to improve the report based on the researcher's feedback. The best report is selected based on a scoring function.

6. **QA Creation**: The script also creates a QA (Question-Answer) pair based on the query and the generated report. If the QA pair results in a new query, it is added to the list of queries to be processed, provided the maximum number of additional queries has not been reached.

7. **Iteration**: The script iterates over the list of queries, performing the search, extraction, processing, report creation, and QA creation steps for each query. The iteration stops when all queries have been processed or when the maximum number of iterations (as specified by the user) has been reached.

8. **Completion**: Once all queries have been processed, the script closes the browser and ends.

The script also creates a debug log file to log the generated additional queries and any errors encountered during the process. The search results, summaries, and reports are saved in separate files in the "Searches" and "Reports" directories respectively.

Please note that this script uses the OpenAI API, and you will need to provide your OpenAI API key for it to work. Also, the script uses Selenium to perform the Google searches and extract the search results, so you will need to have the Selenium WebDriver installed and configured correctly.

### Researcher Mode 🔎

In Researcher mode, Momo AI will perform a series of web searches based on your initial query and generate additional queries using GPT-3.5-Turbo-16K. It will extract and summarize the search results, generate reports, and create question-answer pairs based on the summaries. It will save all the outputs to text files in the `Searches` and `Reports` directories.

To use Researcher mode, run `python Researcher.py` and follow these steps:

1. Enter the number of search results you want to process for each query. The default is 10.
2. Enter your initial search query. For example, “How to write a research paper”.
3. Wait for Momo AI to perform the search, extract and summarize the results, and generate a report.

![Momo AI performing search](momo-ai-search.gif)

4. Momo AI will also generate additional queries based on your initial query using GPT-3.5-Turbo-16K. For example, “How to choose a research topic”, “How to do literature review”, etc.
5. Momo AI will repeat steps 3 and 4 for each additional query until it reaches a limit or there are no more queries.

![Momo AI generating additional queries](momo-ai-additional.gif)

6. Momo AI will also create question-answer pairs based on the summaries using GPT-3.5-Turbo-16K. For example, “Q: What is a research paper? A: A research paper is a document that presents an original argument or analysis based on evidence from various sources.”
7. You can find all the outputs in the `Searches` and `Reports` directories.

![Momo AI creating question-answer pairs](momo-ai-question.gif)

### Reporter Mode 📰

In Reporter mode, Momo AI will perform a single web search based on your query and extract and summarize the results. It will generate a report based on the summaries using GPT-3.5-Turbo-16K and save it to a text file in the `Reports` directory.

To use Reporter mode, run `python Reporter.py` and follow these steps:

1. Enter whether you want to run the browser headlessly or not. If you choose “yes”, you will not see the browser window but Momo AI will still perform the search in the background. If you choose “no”, you will see the browser window and watch Momo AI perform the search.
2. Enter the number of search results you want to process for your query. The default is 10.
3. Enter your search query. For example, “Latest news on nuclear fusion”.
4. Wait for Momo AI to perform the search, extract and summarize the results, and generate a report.

![Momo AI generating report](momo-ai-report.gif)

5. You can find the report in the `Reports` directory.

## About 🙋‍♂️

Momo AI is an open-source project created by [Nico Schlaepfer](https://github.com/nschlaepfer) as a personal assistant for research purposes. It uses [OpenAI](https://openai.com/) as its natural language processing engine and [Selenium](https://www.selenium.dev/) as its web automation tool. It is not affiliated with or endorsed by any of these organizations.

Momo AI is still a work in progress and may have bugs or errors. If you find any issues or have any suggestions, please feel free to [open an issue](https://github.com/nschlaepfer/humanWeb/issues) or [submit a pull request](https://github.com/nschlaepfer/humanWeb/pulls).

You can also follow me on [Twitter](https://twitter.com/nos_ult) for updates and news about Momo AI.

## Possible UI 💻

A possible user interface for Momo AI could look something like this:

![Momo AI UI mockup](momo-ai-ui.png)

The UI would allow the user to enter their query, choose the mode, and see the outputs in a graphical way. It would also show the progress of the search, the summaries, and the reports using a progress bar and a pie chart. The user could also interact with the question-answer pairs and the additional queries generated by Momo AI using buttons and dropdown menus. The UI would be built using a web framework such as [Flask](https://flask.palletsprojects.com/) or [Django](https://www.djangoproject.com/).


## Future Features 🚧

Some of the future features that are planned for Momo AI are:

- Adding voice input and output using speech recognition and synthesis
  - ![Progress bar](https://progress-bar.dev/20/)
- Adding natural language understanding and dialogue management using GPT-3.5-Turbo-16K
  - ![Progress bar](https://progress-bar.dev/40/)
- Adding more sources of information such as Wikipedia, YouTube, etc.
  - ![Progress bar](https://progress-bar.dev/60/)
- Adding more modes of output such as slides, videos, etc.
  - ![Progress bar](https://progress-bar.dev/80/)
- Adding more customization options such as themes, fonts, etc.
  - ![Progress bar](https://progress-bar.dev/90/)
- Adding more languages support using translation APIs
  - ![Progress bar](https://progress-bar.dev/95/)

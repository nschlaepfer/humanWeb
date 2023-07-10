
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
  - [Researcher Mode](#researcher-mode-)
  - [Reporter Mode](#reporter-mode-)
- [About](#about-)
- [Possible UI](#possible-ui-)
- [Future Features](#future-features-)

## Features ✨

- Perform web searches using Google and extract the results
- Extract the page content from the result links and process it with GPT-3.5-Turbo-16K
- Generate summaries of the page content using GPT-3.5-Turbo-16K
- Generate reports based on the summaries using GPT-3.5-Turbo-16K
- Generate additional queries based on the initial query using GPT-3.5-Turbo-16K
- Generate question-answer pairs based on the summaries using GPT-3.5-Turbo-16K
- Save the search results, summaries, and reports to text files
- Run the browser headlessly or with a graphical interface

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

Momo AI has two modes: Researcher and Reporter.

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
- Adding natural language understanding and dialogue management using GPT-3.5-Turbo-16K
- Adding more sources of information such as Wikipedia, YouTube, etc.
- Adding more modes of output such as slides, videos, etc.
- Adding more customization options such as themes, fonts, etc.
- Adding more languages support using translation APIs
- Upgrading to GPT-4 when it becomes available
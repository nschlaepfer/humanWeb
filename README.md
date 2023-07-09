Sure, I can help you update the README and Tech Spec based on the code you provided. Here are the updated versions:

## README

### Web Searching Bot

The Web Searching Bot is a Python-based application designed to automate Google searches. It navigates to Google, enters a user-provided search query, and extracts the search results. It also visits each search result page and extracts the page content. The extracted information is saved to a text file in a directory named "Searches".

### Prerequisites

- Python 3.7 or higher
- Selenium Python library
- WebDriver for Google Chrome
- Google Chrome Browser

### Installation

1. Install Python and pip (Python package installer) on your system.
2. Install the Selenium library using pip:

```bash
pip install selenium
```

3. Download the ChromeDriver for Google Chrome and add it to your system's PATH.

### Usage

1. Run the Python script:

```bash
python web_search_bot.py
```

2. Input your search query when prompted.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)

---

## Tech Spec

### Overview

The Web Searching Bot is a program designed to automate Google searches. It uses Selenium to interact with Google Chrome, performing searches and extracting search results and page content.

### Technical Stack

1. **Programming Language:** Python
2. **Web Automation Library:** Selenium
3. **Browser:** Google Chrome

### Components

1. **Search Performer:** This component uses Selenium to navigate to Google, enter a search query, and perform the search.

2. **Search Result Extractor:** This component uses Selenium to find the search result elements on the Google search results page and extract the title and URL of each result.

3. **Page Content Extractor:** This component uses Selenium to navigate to each search result page and extract the text content of the page.

### Workflow

1. The user runs the script and inputs their search query when prompted.
2. The Search Performer navigates to Google and performs the search.
3. The Search Result Extractor finds the search result elements and extracts the title and URL of each result.
4. The Page Content Extractor navigates to each search result page and extracts the page content.
5. The extracted information is saved to a text file in the "Searches" directory.

### Error Handling

The script includes exception handling to print an error message if something goes wrong during the search or extraction process. If the script encounters an error while extracting a search result, it will skip that result and move on to the next one.


# README

## Web Searching Bot

The Web Searching Bot is a Python-based application designed to browse the internet as if it were a user. It navigates through web pages, follows links, and extracts relevant information based on user-defined criteria. The bot is designed to overcome common web crawling issues such as rate limits.

### Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)
- Google Chrome Browser (for Selenium WebDriver)

### Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Usage

1. Start the Flask server:

```bash
python app.py
```

2. (Optional) If you're using the frontend interface, navigate to the frontend directory and start the React app:

```bash
cd frontend
npm start
```

3. Use the application via the frontend interface or by sending requests to the Flask server.

### Components

- **Web Crawler:** Uses Selenium to simulate a real user's behavior, such as clicking on links and scrolling through pages.
- **Data Extractor:** Parses the HTML of the web pages visited by the crawler and extracts the relevant information using BeautifulSoup.
- **Backend Server:** Handles requests from the user, initiates the web crawler and data extractor, and returns the results. Built using Flask.
- **Frontend Interface:** (Optional) Allows users to input their search criteria and view the results in a user-friendly manner. Built using React.
- **Scheduler:** Automates the web searching process at regular intervals.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)

---

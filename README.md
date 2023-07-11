Certainly! Here's an improved layout for all the images in your GitHub README.md file:

```markdown
# humanWeb: Your Personal AI-Powered Research Assistant 🤖

[![GitHub license](https://img.shields.io/github/license/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/nschlaepfer/humanWeb)](https://github.com/nschlaepfer/humanWeb/network)
[![Twitter Follow](https://img.shields.io/twitter/follow/nos_ult?style=social)](https://twitter.com/nos_ult)

Welcome to humanWeb, a Python-based research assistant that harnesses the power of OpenAI's GPT-3.5-Turbo-16K model and Selenium WebDriver. This tool autonomously conducts web searches, extracts and summarizes relevant data, generates comprehensive reports, and formulates additional queries based on your initial input.

<div align="center">
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/a2a19a74-eb91-4512-ae02-ef1005866dfc" alt="logogif (1)" width="400"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/23b33a63-302c-4060-8232-f25f90978b75" alt="Screenshot 2023-07-10 at 2 06 03 PM" width="400"/>
</div>

## Table of Contents 📑

- [Features](#features-✨)
- [Requirements](#requirements-📋)
- [Installation](#installation-💻)
- [Usage](#usage-🚀)
  - [Websmart mode](#websamart-mode)
- [About](#about-🙋‍♂️)
- [Future Developments](#future-developments-🚧)

## Features ✨

<div align="center">
  <img src="humanWeb-progress.png" alt="humanWeb progress bar" width="500"/>
</div>

humanWeb is equipped with the following features:

- **Web Search & Information Extraction**: humanWeb autonomously performs web searches based on your queries using Selenium WebDriver. It then extracts and saves the search results for further analysis.

- **Data Summarization with GPT-3.5-Turbo-16K**: humanWeb leverages the GPT-3.5-Turbo-16K model to analyze the extracted web page content and pinpoint unique, relevant information. This information is then summarized and stored for future use.

- **Report Generation**: humanWeb generates detailed reports based on the summarized data using GPT-3.5-Turbo-16K. These reports provide synthesized insights on your initial query.

- **Additional Query Formulation**: To help you gather more information or complete a task, humanWeb formulates additional queries related to your initial one using the GPT-3.5-Turbo-16K model.

- **Debug Logging**: humanWeb maintains a debug log file that records the additional queries generated and any errors encountered during the process.

- **Data Storage**: All search results, summaries, and reports are stored in separate files within the `Searches` and `Reports` directories for convenient access and future use.

## Requirements 📋

To run humanWeb, you will need:

- Python 3.6 or higher
- An OpenAI API key
- Selenium Python package
- Dotenv Python package
- Google Chrome browser
- ChromeDriver

## Installation 💻

Here's how you can install humanWeb:

1. Clone or download this repository to your local machine.
2. Create and activate a virtual environment.
3. Install the required packages by running `pip install -r requirements.txt`.
4. Obtain an OpenAI API key from https://beta.openai.com/ and save it as an environment variable in a `.env` file in the project directory. The file should look like this:

```text
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

5. Download the ChromeDriver from https://chromedriver.chromium.org/downloads and save it in the project directory. Ensure that the driver version matches your Chrome browser version.

### macOS

1. Download the ChromeDriver from the [official website](https://chromedriver.chromium.org/downloads). Make sure to download the version that matches your installed version of Google Chrome.

2. Once downloaded, unzip the file. You'll get a file named `chromedriver`.

3. Open Terminal and navigate to the directory where `chromedriver` is located. For example, if it's in your Downloads folder, you'd use `cd ~/Downloads`.

4. Move the `chromedriver` to `/usr/local/bin` directory, which is in the PATH by default. Use the following command: `mv chromedriver /usr/local/bin`.

5. Now you should be able to use ChromeDriver from anywhere on your system.

### Linux

1. Download the ChromeDriver from the [official website](https://chromedriver.chromium.org/downloads). Make sure to download the version that matches your installed version of Google Chrome.

2. Once downloaded, unzip the file. You'll get a file named `chromedriver`.

3. Open Terminal and navigate to the directory where `chromedriver` is located. For example, if it's in your Downloads folder, you'd use `cd ~/Downloads`.

4. Move the `chromedriver` to `/usr/local/bin` directory, which is in the PATH by default. Use the following command: `sudo mv chromedriver /usr/local/bin`.

5. Now you should be able to use ChromeDriver from anywhere on your system.

### Windows

1. Download the ChromeDriver from the [official website](https://chromedriver.chromium.org/downloads). Make sure to download the version that matches your installed version of Google Chrome.

2. Once downloaded, unzip the file. You'll get a file named `chromedriver.exe`.

3. You need to add the directory containing `chromedriver.exe` to your system's PATH. Here's how:

   - Right-click on 'My Computer' or 'This PC' and go to Properties.

   - Click on 'Advanced system settings'.

   - Click on 'Environment Variables...'.

   - In the 'System variables' section, find the 'Path' variable, select it and click on 'Edit

   - In the 'Variable value' field, add the path to the directory containing `chromedriver.exe`. Make sure to separate it from existing paths with a semicolon (`;`).

4. Click OK on all windows to save the changes.

5. Now you should be able to use ChromeDriver from anywhere on your system.

Please note that you need to have administrative privileges to perform some of these steps. Also, remember to replace the paths in the commands with the actual paths where your `chromedriver` file is located.

## Usage 🚀

humanWeb operates in Websmart mode, which performs a comprehensive sequence of tasks,

 including web search, information extraction, data summarization, report generation, and additional query formulation. 

To run humanWeb, use the command `python humanWeb.py` and follow the prompts. You will be asked to input:

1. The number of search results you want to process.
2. Your initial query.
3. The number of steps (or queries) you wish to perform.

humanWeb will then autonomously perform a web search, extract and summarize results, generate additional queries, and formulate a comprehensive report based on the collected data. If the generated report doesn't meet a certain quality threshold, humanWeb restarts the search process to ensure satisfactory output.

<div align="center">
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/fec213c6-1b6f-48e2-9ed4-5d3ad4bdb346" alt="Screenshot 2023-07-10 at 2 05 06 PM" width="800"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/6f315981-e908-45b2-99f9-cdff6fe5855f" alt="Screenshot 2023-07-10 at 2 05 22 PM" width="800"/>
</div>

## About 🙋‍♂️

humanWeb is an open-source project developed by [Nico Schlaepfer](https://github.com/nschlaepfer). It was designed as a personal research assistant tool, utilizing [OpenAI](https://openai.com/) for natural language processing and [Selenium](https://www.selenium.dev/) for web automation. This project is not affiliated with or endorsed by any of these organizations.

Please note that humanWeb is a work in progress and may contain bugs or errors. If you find any issues or have any suggestions, feel free to [open an issue](https://github.com/nschlaepfer/humanWeb/issues) or [submit a pull request](https://github.com/nschlaepfer/humanWeb/pulls).

For updates and news about humanWeb, you can follow [Nico Schlaepfer](https://twitter.com/nos_ult) on Twitter.

<div align="center">
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/79f74d97-14b0-4739-a781-9978c803948c" alt="logo12" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/b400e1e4-471e-42bc-8817-96af67edc548" alt="logo11" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/9280f0e4-861c-4a57-828d-36cf59213394" alt="logo10" width="200"/>
  <br/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/2921eee3-c88d-43e7-bf72-81cf55285e07" alt="logo8" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/00cc6226-7660-4d97-b387-842aa7dfb849" alt="7" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/17ff9d73-1797-4414-9df9-b66feeb162b5" alt="6" width="200"/>
  <br/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/9a77b2ab-aa42-483a-82a4-9b6c34bf7d20" alt="_17439a69-fa52-41b2-b2e4-a52da7955c33" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/4c9f7983-74c3-4b89-9a19-74d338cddb30" alt="_4713be32-4b6b-41df-a163-11aa87a52c74" width="200"/>
  <img src="https://github.com/nschlaepfer/humanWeb/assets/44988633/c4d9928e-23b4-4eca-a829-bb4d6ddce6d2" alt="_8dad5291-e223-40bf-ab61-1bdc18eeceb7" width="200"/>
</div>

## Future Developments 🚧

We're continuously working on improving humanWeb. Here are some potential enhancements for future versions:

- Adding a user interface for intuitive interaction.
- Enhancing the report generation process with more dynamic and user-tailored outputs.
- Expanding the search functionality to include more sources of information.
- Implementing more customization options to adjust functionality according to user needs.
- Improving error handling and providing more detailed logs.
- proved layout with all the images nicely arranged in the README file on your GitHub repository.

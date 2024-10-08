# Shah-GPT
Shah GPT is an advanced chatbot built using the Google Gemini API and integrated with Telegram. This bot can answer any questions you ask in both English and Azerbaijani, leveraging the power of the Gemini API and the easygoogletranslate module for translation.. It’s designed to provide quick and informative responses to users via a Telegram chat interface. <br/>
<br/>

## Features
* Multilingual Support: Communicate in both English and Azerbaijani. You can select which language you want to communicate.
* Ask Anything: Get detailed responses to your questions by interacting with the bot on Telegram.
* Powered by Google Gemini API: Utilizes the Gemini API to generate high-quality answers.
* Telegram Integration: Easily communicate with the bot via Telegram using a token for secure messaging. <br/>
<br/>

## Project Structure
* configure.py: This file contains your Telegram bot token and Gemini API key for authentication and configuration. Make sure to replace the placeholders with your own credentials.
* bot.py: The main script where the bot logic is implemented. It handles incoming messages, sends them to the Gemini API, and returns responses to users.
* requirements.txt: Contains the list of dependencies required for running the chatbot, including the necessary Telegram and API libraries. <br/>
<br/>

# Getting Started
## Prerequisites
Before you begin, make sure you have the following: <br/>
* Telegram Bot Token: Create a new bot via BotFather on Telegram and get your bot token.
* Google Gemini API Key: Obtain an API key from Google Gemini to enable the chatbot's AI capabilities. <br/>
<br/>

## Installation
1. Clone the repository:
   
   ```bash
   git clone https://github.com/Shah114/Shah-GPT.git
   cd Shah-GPT
   ```
3. Install the required packages:
   
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your API keys in configure.py:
   
   ```python
   api_key = 'your-gemini-api-key'
   bot_token = 'your-telegram-token'
   ```
<br/>

## Running the Bot
To run the bot, simply execute: <br/>

```bash
python bot.py
```
Then write /start on Telegram. Your bot will now be live and ready to answer questions on Telegram. <br/>
<br/>

## Usage
Once your bot is running, users can interact with it by sending messages in a Telegram chat. The bot will forward the message to the Gemini API and return a response directly in the chat. <br/>
<br/>

## Future Enhancements
* Add support for additional languages.
* Integrate voice commands using a speech-to-text feature.


# Cryptocurrency Price Tracker

This Python script automates the process of collecting current cryptocurrency prices, 24-hour price changes, and trading volumes from the CoinMarketCap website. The data is saved to a local JSON file and sent as updates to a Telegram bot.

## Features

- Collects data on the top 10 cryptocurrencies by trading volume
- Updates the data every 3 hours
- Stores the data in a local JSON file with timestamp
- Sends price updates to a Telegram bot

## Requirements

- Python 3.7 or higher
- `playwright` library for web automation
- `aiogram 3x` library for Telegram bot integration
- `requests` library for making HTTP requests

## Installation

1. Clone the repository: ```git clone https://github.com/your-username/cryptocurrency-price-tracker.git```
2. Navigate to the project directory: ```cd cryptocurrency-price-tracker```
3. (Windows) Run the install script to set up the environment: ```install.bat```

(macOS/Linux) Install the required dependencies: ```pip install -r requirements.txt```


## Usage

1. (Windows) Run the start script to begin tracking prices and sending updates to Telegram: ```start.bat```

(macOS/Linux) Run the script directly: ```python3 main.py```

2. The script will automatically start collecting data and sending updates to your Telegram bot.

3. To stop the script, use the `/stop` command in your Telegram bot.

4. Additional commands:
- `/start`: Start the data collection process
- `/list`: Get the latest price update report
- `/currency <name>`: Get price data for a specific cryptocurrency (e.g., `/currency bitcoin`)

## Configuration

Before running the script, you'll need to set up your Telegram bot and configure the script with your bot token and chat ID. Update the `config.py` file with the necessary information.
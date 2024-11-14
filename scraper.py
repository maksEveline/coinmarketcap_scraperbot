import json
import logging
from datetime import datetime
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import asyncio

from apis.tg_api import send_crypto_data
from config import BACKUPS_DIR, BOT_TOKEN, ADMIN_ID, PARSE_SLEEP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("crypto_scraper.log"), logging.StreamHandler()],
)


async def fetch_top_cryptos(max_retries=3):
    """
    Fetches top 10 cryptocurrency data from CoinMarketCap and saves it to a JSON file.
    Retries page loading up to `max_retries` times if the page does not load correctly.

    :param max_retries: Maximum number of retries if the page fails to load
    """
    while True:
        retries = 0
        while retries < max_retries:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                page = await browser.new_page()

                try:
                    await page.goto("https://coinmarketcap.com/")
                    await page.wait_for_selector("tr", timeout=10000)

                    rows = await page.query_selector_all("tr")
                    crypto_data = []

                    for row in rows:
                        cells = await row.query_selector_all("td")
                        if len(cells) < 11:
                            continue

                        name = (await cells[2].inner_text()).strip().split("\n")[0]
                        price = (await cells[3].inner_text()).strip()
                        day_change = (await cells[5].inner_text()).strip()
                        volume_data = (await cells[8].inner_text()).strip()

                        volume_price, _, volume_crypto = volume_data.split("\n")
                        crypto_data.append(
                            {
                                "name": name.upper(),
                                "price": price,
                                "day_change": day_change,
                                "volume_price": volume_price,
                                "volume_crypto": volume_crypto,
                            }
                        )

                        if len(crypto_data) == 10:
                            break

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{BACKUPS_DIR}/crypto_data_{timestamp}.json"

                    await send_crypto_data(BOT_TOKEN, ADMIN_ID, crypto_data)

                    with open(filename, "w") as json_file:
                        json.dump(crypto_data, json_file, indent=4)

                    await browser.close()
                    logging.info(f"Top 10 cryptocurrency data saved to {filename}")
                    break

                except PlaywrightTimeoutError:
                    retries += 1
                    logging.warning(f"Attempt {retries} failed. Retrying...")
                    await browser.close()
                    await asyncio.sleep(2)

        await asyncio.sleep(PARSE_SLEEP)

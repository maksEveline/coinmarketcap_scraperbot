import aiohttp
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("crypto_bot.log"), logging.StreamHandler()],
)


async def send_crypto_data(bot_token, user_id, crypto_data):
    """
    generates and sends a message with cryptocurrency data to a user in Telegram

    :param bot_token: telegram bot token
    :param user_id: telegram user ID for message sending
    :param crypto_data: list of dictionaries with information about cryptocurrencies
    """
    message = "📈 Топ 10 криптовалют:\n\n"
    for crypto in crypto_data:
        message += (
            f"🔸 <b>{crypto['name']}</b>\n"
            f"Цена: {crypto['price']}\n"
            f"Изменение за день: {crypto['day_change']}\n"
            f"Объем торгов (цена): {crypto['volume_price']}\n"
            f"Объем торгов (кол-во): {crypto['volume_crypto']}\n\n"
        )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {"chat_id": user_id, "text": message, "parse_mode": "HTML"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                logging.info("Message sent successfully")
            else:
                logging.error(f"Failed to send message. Status code: {response.status}")

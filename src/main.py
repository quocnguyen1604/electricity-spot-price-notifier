from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import os

import api.electricity as electricity
import data.transform as transform
import notification.discordNotifier as discordNotifier
import analysis.ana as ana


def wait_until_next_hour():
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    sleep_seconds = (next_hour - now).total_seconds()
    time.sleep(sleep_seconds)


def run_once():
    date = datetime.now().strftime("%Y-%m-%d")

    spot_price = electricity_api.getSpotPrice(date)
    transformed_price = transform.transformPriceData(spot_price, float(margin))
    ana_result = ana.isCurrentHourPriceHigh(transformed_price)

    discordNotifier.sendDiscordNotification(
        discord_webhook_url, ana_result[0], ana_result[1], ana_result[2], ana_result[3]
    )

    print(transformed_price)


def main():
    global electricity_api, margin, discord_webhook_url

    print("Starting the electricity price monitoring application...")

    load_dotenv()
    base_url = os.getenv("BASE_URL")
    tulos = os.getenv("TULOS")
    margin = os.getenv("MARGIN")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    electricity_api = electricity.ElectricityAPI(base_url, tulos)

    while True:
        wait_until_next_hour()
        print(f"Running the price check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        run_once()


if __name__ == "__main__":
    main()
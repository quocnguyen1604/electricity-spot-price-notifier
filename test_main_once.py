"""
Test main.py by running once without waiting for next hour
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
from datetime import datetime
import api.electricity as electricity
import data.transform as transform
import notification.discordNotifier as discordNotifier
import analysis.ana as ana


def test_run_once():
    print("=" * 60)
    print("TESTING MAIN.PY - RUN ONCE MODE")
    print("=" * 60)
    
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    tulos = os.getenv("TULOS")
    margin = os.getenv("MARGIN")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    # Check if .env is configured
    if not all([base_url, tulos, margin, discord_webhook_url]):
        print("\n❌ ERROR: Missing environment variables in .env file")
        print("\nRequired .env variables:")
        print("  BASE_URL=...")
        print("  TULOS=...")
        print("  MARGIN=...")
        print("  DISCORD_WEBHOOK_URL=...")
        return False
    
    try:
        print("\n✅ Environment variables loaded")
        print(f"   BASE_URL: {base_url}")
        print(f"   MARGIN: {margin}")
        
        # Get electricity data
        print("\n🔄 Fetching electricity prices...")
        electricity_api = electricity.ElectricityAPI(base_url, tulos)
        date = datetime.now().strftime("%Y-%m-%d")
        spot_price = electricity_api.getSpotPrice(date)
        print(f"✅ Got prices for {date}")
        
        # Transform data
        print("\n🔄 Transforming price data...")
        transformed_price = transform.transformPriceData(spot_price, float(margin))
        print(f"✅ Transformed {len(transformed_price)} hours of data")
        
        # Analyze
        print("\n🔄 Analyzing prices...")
        ana_result = ana.isCurrentHourPriceHigh(transformed_price)
        print(f"✅ Analysis complete")
        
        # Send Discord notification
        print("\n🔄 Sending Discord notification...")
        discordNotifier.sendDiscordNotification(discord_webhook_url, ana_result)
        print(f"✅ Discord notification processed")
        
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_run_once()

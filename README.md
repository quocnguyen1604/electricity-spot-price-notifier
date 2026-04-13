# Electricity Spot Price Notifier ⚡

A smart Python application that monitors real-time electricity spot prices and sends intelligent notifications to Discord based on price trends and personalized usage patterns.

## Overview

This application fetches hourly electricity prices, analyzes them using percentile-based price bands, and sends automated alerts to your Discord channel when:

- 🟢 **Prices are cheap** - Best time to use electricity
- 🟡 **Prices are normal** - Regular hourly reports
- 🔴 **Prices are expensive** - Time to reduce consumption
- ⏸️ **Wait for cheaper** - Better prices coming soon

## Features

✨ **Smart Price Analysis**

- Percentile-based classification (cheap/normal/expensive) instead of simple averages
- Time-aware: Only analyzes your active usage hours (7am-11pm)
- Next-hour price comparison for context

🎯 **Intelligent Recommendations**

- Automatically suggests when to use electricity
- Warns when prices are expensive with wait times
- Adapts daily to actual price patterns

💬 **Rich Discord Notifications**

- Color-coded messages (🟢 Green/🟡 Yellow/🔴 Red)
- ANSI colored recommendation text for visibility
- Actionable insights with hourly breakdown
- Optional team mentions for urgent alerts

⏰ **Automated Scheduling**

- Runs every hour automatically
- Waits until the next hour to fetch fresh data
- Easy testing mode for immediate execution

## Project Structure

```
electricity-spot-price-notifier/
├── src/
│   ├── main.py                    # Main application entry point
│   ├── analysis/
│   │   └── ana.py                 # Price analysis & classification logic
│   ├── api/
│   │   └── electricity.py         # API client for fetching prices
│   ├── data/
│   │   └── transform.py           # Data transformation & margin calculation
│   ├── notification/
│   │   └── discordNotifier.py     # Discord message formatting & sending
│   └── test/
│       └── test_main_once.py      # Integration test
├── test_main_flow.py              # Mock data flow test (no API required)
├── requirements.txt               # Python dependencies
└── README.md                       # This file
```

## Installation

### Prerequisites

- Python 3.11+
- discord webhook URL
- Electricity API credentials

### Step 1: Clone & Setup

```bash
git clone <repository-url>
cd electricity-spot-price-notifier
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the project root:

```env
BASE_URL=https://api.example.com
TULOS=your_api_key_here
MARGIN=0.05
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook/url
```

**Configuration Details:**

- `BASE_URL`: Electricity price API endpoint
- `TULOS`: API authentication key
- `MARGIN`: Price margin to add (as decimal, e.g., 0.05 = 5%)
- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL for notifications

## Usage

### Run in Production (Waits for Next Hour)

```bash
python src/main.py
```

The application will:

1. Wait until the next full hour
2. Fetch electricity prices for today
3. Analyze current hour's price
4. Send Discord notification with recommendations
5. Loop and repeat

**Run in background:**

```bash
nohup python src/main.py > app.log 2>&1 &
```

### Test Mode (Run Once Immediately)

**With mock data (no API/Discord needed):**

```bash
python test_main_flow.py
```

**With real API (requires .env):**

```bash
python test/test_main_once.py
```

## How It Works

### 1️⃣ Price Fetching

- Fetches 24-hour electricity prices via API
- Applies margin multiplier
- Gets data for current day

### 2️⃣ Price Analysis (`ana.py`)

- Extracts only active usage hours (7am-11pm, configurable)
- Calculates percentiles:
  - **P25**: Bottom 25% threshold → Cheap prices
  - **P75**: Top 25% threshold → Expensive prices
- Classifies current + next hour into bands:
  - 🟢 `Giá rẻ` (Cheap) ≤ P25
  - 🟡 `Giá bình thường` (Normal) P25-P75
  - 🔴 `Đắt` (Expensive) ≥ P75

### 3️⃣ Recommendation Engine

```
IF Price is EXPENSIVE:
  └─ IF Next hour is cheaper/normal → "Wait for cheaper"
  └─ ELSE → "Use now, no better option"

IF Price is CHEAP:
  └─ "Use now!"

IF Price is NORMAL:
  └─ IF Next hour is expensive → "Use now before it rises"
  └─ ELSE → "Normal, no action needed"
```

### 4️⃣ Discord Notification

- Sends formatted message with:
  - Current hour & price band
  - Next hour comparison
  - Price thresholds (P25, P75)
  - ANSI-colored recommendation with emoji
  - Optional team mention for urgent alerts

## Example Discord Message

```
📊 BỐ MÀY BÁO CÁO ĐIỆN

Giờ hiện tại: 15:00

Giá: 0.40 c/kWh --- (ĐẮT)
Giá giờ sau: 0.26 c/kWh --- (GIÁ BÌNH THƯỜNG)

Price Thresholds (7am-11pm):
  • Cheap: ≤ 10.87 c/kWh
  • Expensive: ≥ 13.91 c/kWh

Recommendation:
⏸️ ĐỢI CHO RẺ HƠN ĐÊ
```

## Testing

### Test Classes

| Test                 | Command                         | Requires     |
| -------------------- | ------------------------------- | ------------ |
| **Mock Flow Test**   | `python test_main_flow.py`      | ❌ None      |
| **Integration Test** | `python test/test_main_once.py` | ✅ .env file |
| **Production Mode**  | `python src/main.py`            | ✅ .env file |

### Expected Output

```
============================================================
TESTING MAIN FLOW (WITHOUT API/DISCORD)
============================================================
✅ Analysis Result:
  Current Hour: 9
  Current Price: 0.25 c/kWh
  Current Band: Giá bình thường
  Next Hour Price: 0.18 c/kWh
  Next Band: Giá rẻ
  Recommendation: Bình thường
  P25 (Cheap threshold): 0.2
  P75 (Expensive threshold): 0.31
```

## Configuration Options

### Active Hours

Modify the usage window in `ana.py`:

```python
ana_result = ana.isCurrentHourPriceHigh(transformed_price, activeHourStart=7, activeHourEnd=23)
```

### Price Bands

Adjust classification logic in `ana.py` `classify_band()` function to use different thresholds.

### Notification Triggers

Edit `discordNotifier.py` `should_notify` condition to change when alerts are sent.

## Files Overview

### `src/main.py`

- Application entry point
- Orchestrates data flow
- Handles scheduling and looping

### `src/analysis/ana.py`

- Core price analysis algorithm
- Percentile-based classification
- Recommendation logic
- Returns detailed analysis results

### `src/api/electricity.py`

- API client for fetching prices
- Handles authentication
- Error handling

### `src/data/transform.py`

- Data transformation
- Margin calculation
- Prepares data for analysis

### `src/notification/discordNotifier.py`

- Formats Discord messages
- Adds color coding (hex for embed, ANSI for text)
- Sends notifications
- Handles webhook requests

## Troubleshooting

### Issue: ModuleNotFoundError for `rich`

**Solution:** Install dependencies

```bash
pip install -r requirements.txt
```

### Issue: Discord notification fails (Status 401)

**Solution:** Check `DISCORD_WEBHOOK_URL` in `.env` is correct

### Issue: API returns 404

**Solution:** Verify `BASE_URL` and `TULOS` credentials in `.env`

### Issue: Blue colored border instead of green/yellow/red

**Solution:** Ensure `current_band` in `ana.py` returns exact values:

- `'Giá rẻ'`
- `'Giá bình thường'`
- `'Đắt'`

## Requirements

```
requests>=2.32.5
python-dotenv>=1.2.2
rich>=15.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.

---

**Made with ⚡ for smarter electricity usage**

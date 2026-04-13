from src.analysis.ana import isCurrentHourPriceHigh
from datetime import datetime

# Sample price data for testing (24 hours)
sample_data = [
    {'hour': 0, 'price': 0.10},   # midnight
    {'hour': 1, 'price': 0.09},
    {'hour': 2, 'price': 0.08},
    {'hour': 3, 'price': 0.07},
    {'hour': 4, 'price': 0.08},
    {'hour': 5, 'price': 0.09},
    {'hour': 6, 'price': 0.10},
    {'hour': 7, 'price': 0.20},   # 7am - start of usage
    {'hour': 8, 'price': 0.22},
    {'hour': 9, 'price': 0.25},
    {'hour': 10, 'price': 0.18},
    {'hour': 11, 'price': 0.28},
    {'hour': 12, 'price': 0.35},
    {'hour': 13, 'price': 0.38},
    {'hour': 14, 'price': 0.32},
    {'hour': 15, 'price': 0.40},  # Peak hour
    {'hour': 16, 'price': 0.26},
    {'hour': 17, 'price': 0.24},
    {'hour': 18, 'price': 0.30},
    {'hour': 19, 'price': 0.27},
    {'hour': 20, 'price': 0.21},
    {'hour': 21, 'price': 0.19},
    {'hour': 22, 'price': 0.17},
    {'hour': 23, 'price': 0.16},  # 11pm - end of usage
]

# Test the new algorithm
result = isCurrentHourPriceHigh(sample_data)
print("\n=== RESULT ===")
print(f"Current Hour: {result['currentHour']}")
print(f"Current Price: {result['currentPrice']} → Band: {result['currentBand']}")
print(f"Next Hour Price: {result['nextHourPrice']} → Band: {result['nextBand']}")
print(f"\nPrice Thresholds (for active hours 7am-11pm):")
print(f"  Cheap (≤25th percentile): {result['p25']}")
print(f"  Expensive (≥75th percentile): {result['p75']}")
print(f"\n🔹 Recommendation: {result['recommendation'].upper()}")

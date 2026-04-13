from datetime import datetime
import statistics

def isCurrentHourPriceHigh(data, activeHourStart=7, activeHourEnd=23):
    """
    Improved pricing logic with percentile-based classification and next-hour recommendation.
    
    Args:
        data: List of hourly price data with 'price' key
        activeHourStart: Start of usage window (default: 7am)
        activeHourEnd: End of usage window (default: 11pm)
    
    Returns:
        {
            'currentHour': int,
            'currentPrice': float,
            'nextHourPrice': float,
            'currentBand': str ('cheap', 'normal', 'expensive'),
            'nextBand': str,
            'p25': float (25th percentile),
            'p75': float (75th percentile),
            'recommendation': str ('use_now', 'wait_for_cheaper', 'neutral')
        }
    """
    currentHour = datetime.now().hour
    currentPrice = data[currentHour]['price']
    nextHourPrice = data[(currentHour + 1) % 24]['price'] if currentHour < 23 else data[0]['price']
    
    # Extract prices from active usage hours only (7am-11pm)
    activeHourPrices = [
        data[hour]['price'] 
        for hour in range(activeHourStart, activeHourEnd + 1)
    ]
    
    # Calculate percentiles
    p25 = round(statistics.quantiles(activeHourPrices, n=4)[0], 2)  # 25th percentile
    p75 = round(statistics.quantiles(activeHourPrices, n=4)[2], 2)  # 75th percentile
    
    # Classify current hour into band
    def classify_band(price):
        if price <= p25:
            return 'Giá rẻ'
        elif price >= p75:
            return 'Đắt'
        else:
            return 'Giá bình thường'
    
    currentBand = classify_band(currentPrice)
    nextBand = classify_band(nextHourPrice)
    
    # Smart recommendation based on current and next hour comparison
    if currentBand == 'Đắt':
        recommendation = 'Đợi tí cho rẻ hơn'  # No cheaper option soon

    elif currentBand == 'Giá rẻ':
        recommendation = 'Tranh thủ đi th lồn'
        
    else:  # normal
        if nextBand == 'Đắt':
            recommendation = 'Tranh thủ đi th lồn'  # Prices going up
        elif nextBand == 'Giá rẻ':
            recommendation = 'Đợi tí cho rẻ hơn'  # Prices going down
        else:
            recommendation = 'Giá bình thường'  # No strong recommendation
    
    print(f"Current hour: {currentHour}")
    print(f"Current price: {currentPrice} ({currentBand}) | Next price: {nextHourPrice} ({nextBand})")
    print(f"Recommendation: {recommendation}")
    
    return {
        'currentHour': currentHour,
        'currentPrice': currentPrice,
        'nextHourPrice': nextHourPrice,
        'currentBand': currentBand,
        'nextBand': nextBand,
        'p25': p25,
        'p75': p75,
        'recommendation': recommendation
    }
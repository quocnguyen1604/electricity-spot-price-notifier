from datetime import datetime

def isCurrentHourPriceHigh(data):
    currentHour = datetime.now().hour
    currentPrice = 0
    print("Current hour: ", currentHour)
    averagePrice = round(sum(item['price'] for item in data) / len(data), 2)
    for item in data:
        if int(item['hour']) == currentHour:
            print("Current hour price: ", item['price'])
            currentPrice = item['price']
    return [currentPrice > averagePrice, currentPrice, averagePrice]
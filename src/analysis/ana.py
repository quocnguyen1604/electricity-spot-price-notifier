from datetime import datetime

def isCurrentHourPriceHigh(data):
    currentHour = datetime.now().hour
    currentPrice = data[currentHour]['price']
    nextHourPrice = data[(currentHour + 1) % 24]['price'] if currentHour < 23 else data[0]['price']
    print("Current hour: ", currentHour)
    averagePrice = round(sum(item['price'] for item in data) / len(data), 2)
    # for item in data:
    #     if int(item['hour']) == currentHour:
    #         print("Current hour price: ", item['price'])
    #         currentPrice = item['price']
    #         next

    return [currentPrice > averagePrice, currentPrice, nextHourPrice, averagePrice]
from datetime import datetime, timedelta


def transformPriceData(price_data, margin):
    transformed_data = []

    price_data = sorted(price_data, key=lambda x: x['aikaleima_suomi'])

    print("Price data: ", price_data)

    for i in range(0, 96, 4):
        hour = price_data[i]['aikaleima_suomi'][-5:-3]
        price = 0
        for j in range(4):
            price += price_data[i + j]['hinta']
            
        price = (price / 4 * 1.255) + margin

        transformed_data.append({
            "date": price_data[i]['aikaleima_suomi'][:10],
            "hour": hour,
            "price": round(price, 2)
        })
        
    return transformed_data
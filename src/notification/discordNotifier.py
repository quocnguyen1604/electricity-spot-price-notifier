import requests
import rich

def sendDiscordNotification(webhook_url, ana_result):
    """
    Send Discord notification with price analysis and recommendations.
    
    Args:
        webhook_url: Discord webhook URL
        ana_result: Dictionary from isCurrentHourPriceHigh() containing:
            - currentPrice, currentBand, nextHourPrice, nextBand
            - recommendation, p25, p75, currentHour
    """
    current_price = ana_result['currentPrice']
    current_band = ana_result['currentBand']
    next_hour_price = ana_result['nextHourPrice']
    next_band = ana_result['nextBand']
    recommendation = ana_result['recommendation']
    p25 = ana_result['p25']
    p75 = ana_result['p75']
    current_hour = ana_result['currentHour']
    
    # Determine color and message based on current band 
    band_colors = {
        'Giá rẻ': 0x00FF00,           # Green - Cheap
        'Giá bình thường': 0xFFFF00,  # Yellow - Normal
        'Đắt': 0xFF0000               # Red - Expensive
    }
    color = band_colors.get(current_band, 0x0000FF)
    
    # Recommendation emoji and message with ANSI color codes
    recommendation_map = {
        'Tranh thủ đi th lồn': '✅ DÙNG NGAY - Giá rẻ',
        'Đợi tí cho rẻ hơn': '⏸️ ĐỢI CHO RẺ HƠN ĐÊ',
        'Giá bình thường': '😐 BÌNH THƯỜNG - dùng ổn'
    }
    recommendation_msg = recommendation_map.get(recommendation, recommendation)
    
    # Define ANSI color codes for Discord based on current price band
    # \u001b[1;32m: Bold Green (Cheap)
    # \u001b[1;33m: Bold Yellow (Normal)
    # \u001b[1;31m: Bold Red (Expensive)
    # \u001b[0m: Reset color
    
    current_band_clean = current_band.strip() if current_band else ""
    
    if current_band_clean == "Giá rẻ":
        color_code = "\u001b[1;32m"  # Green - Cheap
    elif current_band_clean == "Giá bình thường":
        color_code = "\u001b[1;33m"  # Yellow - Normal
    elif current_band_clean == "Đắt":
        color_code = "\u001b[1;31m"  # Red - Expensive
    else:
        color_code = "\u001b[1;37m"  # White - Default
    
    # Create colored recommendation line
    colored_recommendation = f"```ansi\n{color_code}{recommendation_msg}\u001b[0m\n```"
    
    # Determine if should notify (only on expensive or waiting opportunities)
    should_notify = current_band == 'Đắt' or recommendation in ['Đợi tí cho rẻ hơn'] 
    
    if should_notify:
        mention = '<@&1490439901085171904>'
        title = "⚡ TẮT MẸ MÀY ĐIỆN NGAY - GIỜ ĐANG ĐẮT"
    else:
        mention = ""
        title = "📊 BỐ MÀY BÁO CÁO ĐIỆN"
    
    description = (
        f"**Giờ hiện tại:** {current_hour}:00\n\n"
        f"**Giá :** {current_price} c/kWh  ---      ({current_band.upper()})\n"
        f"**Giá giờ sau :** {next_hour_price} c/kWh  ---   ({next_band.upper()})\n\n"
        f"**Recommendation:**\n{colored_recommendation}"
    )
    
    embedded_message = {
        "content": mention,
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }
    
    response = requests.post(webhook_url, json=embedded_message)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
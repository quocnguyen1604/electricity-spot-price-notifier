import requests
import rich

def sendDiscordNotification(webhook_url, isHigh, currentPrice, averagePrice):
    if isHigh:
        embedded_message = {
            "content": f'<@&1490439901085171904>',
            "embeds": [
                {
                    "title": "TẮT ĐIỆN MẸ ĐI",
                    "description": f"Giá: {currentPrice} c/kWh\nTrung Bình: {averagePrice} c/kWh",
                    "color": 0xFF0000
                }
            ]
        }
    else:
        embedded_message = {
            "content": f'Báo cáo giá điện',
            "embeds": [
                {
                    "title": "TẸT GA ĐÊ",
                    "description": f"Giá: {currentPrice} c/kWh\nTrung Bình: {averagePrice} c/kWh",
                    "color": 0x00FF00
                }
            ]
        }
    response = requests.post(webhook_url, json=embedded_message)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
import os
import sys
import requests


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing")

if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID is missing")

def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as file:
        return file.read()


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Telegram report sent successfully.")
    else:
        print("Telegram send failed.")
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Report path is required.")
        sys.exit(1)

    report_path = sys.argv[1]

    report = load_report(report_path)

    send_telegram_message(report)






























# BOT_TOKEN = "https://api.telegram.org/bot8846040951:AAFxS4VxBF712wsYxK-9OFR0oJ9ICiUzYPM/getUpdates"
# CHAT_ID = "6761846723"
# REPORT_PATH = "outputs/reports/after_close_report.txt"

# def load_report():
#     with open(REPORT_PATH,"r",encoding="utf-8") as file:
#         return file.read()

# def send_telegram_message(message):
#     url = f"https://api.telegram.org/bot8846040951:AAFxS4VxBF712wsYxK-9OFR0oJ9ICiUzYPM/sendMessage"

#     payload = {
#         "chat_id": CHAT_ID,
#         "text": message
#     }

#     response = requests.post(url, data=payload)
#     print(response.json())

# if __name__ == "__main__":
#     report = load_report()
#     send_telegram_message(report)
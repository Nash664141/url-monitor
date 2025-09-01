import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN', "7515732152:AAGXQeYPuVNpWbi-T2KeoHVJC0zlB3L6oDo")
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "6402870424")

URLS = [
    "https://dchd.onrender.com/health",
    "https://dchd.onrender.com/ping"
]

def check_urls():
    messages = []
    for url in URLS:
        try:
            r = requests.get(url, timeout=10)
            status = r.status_code
            if 200 <= status < 300:
                alert_type = "✅ UP"
            elif 400 <= status < 500:
                alert_type = "⚠️ CLIENT ERROR"
            else:
                alert_type = "❌ SERVER ERROR"
            message = f"{url} → {alert_type} ({status})"
        except Exception as e:
            message = f"{url} → ❌ DOWN: {str(e)[:100]}"
        messages.append(message)
    return messages

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Erreur Telegram: {e}")

def main():
    print("Début du monitoring...")
    messages = check_urls()
    status_message = "📊 Rapport de statut:\n" + "\n".join(messages)
    print(status_message)
    send_telegram_message(status_message)

if __name__ == "__main__":
    main()

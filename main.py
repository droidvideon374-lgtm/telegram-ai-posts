import os
import requests

# ======================
# СЕКРЕТЫ ИЗ GITHUB
# ======================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ======================
# ПРОМТ
# ======================
PROMPT = """
Ты — опытный игровой журналист и автор Telegram-канала. Напиши пост на игровую тему объёмом ровно 550–650 символов (с пробелами). Тема любая: обзор механики, совет по прохождению, забавный баг, история разработки или игровая новость.

Требования:
- Без клише и шаблонов
- 2–3 абзаца
- В конце вопрос к читателю
- Максимум 2 эмодзи
- Живой разговорный стиль
"""

# ======================
# OPENROUTER ЗАПРОС
# ======================
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "messages": [
        {
            "role": "user",
            "content": PROMPT
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

print("OPENROUTER RESPONSE:")
print(data)

# проверка ошибки API
if "choices" not in data:
    raise Exception("OpenRouter error: " + str(data))

article = data["choices"][0]["message"]["content"]

# ======================
# TELEGRAM ОТПРАВКА
# ======================
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

tg_response = requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": article
    }
)

print("Telegram response:")
print(tg_response.text)

print("Статья опубликована")

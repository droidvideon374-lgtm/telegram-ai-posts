import os
import requests

# Получаем секреты из GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Тема статьи
PROMPT = """
Ты — опытный игровой журналист и автор Telegram-канала. Напиши пост на игровую тему объёмом ровно 550–650 символов (с пробелами). Тема любая: обзор механики, совет по прохождению, забавный баг, история разработки или игровая новость.

Требования:

Не используй клише, штампы и повторяющиеся фразы (избегай «стоит отметить», «как уже говорилось», «в заключение хочу сказать»).

Текст должен быть живым, динамичным, с элементами интриги или юмора.

Разбей текст на 2–3 коротких абзаца.

В конце напиши риторический вопрос или призыв к обсуждению (без эмодзи-спама, максимум 2 эмодзи).

Не используй маркированные списки и заголовки.

Язык — естественный, разговорный, без излишнего сленга (но лёгкий сленг допустим).
"""

# Запрос к OpenRouter
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [
            {
                "role": "user",
                "content": PROMPT
            }
        ]
    }
)

# Получаем текст статьи
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
            "content": "Напиши короткую статью про мобильные игры"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

print("OPENROUTER RESPONSE:")
print(data)

# Отправка в Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": article
    }
)

print("Статья опубликована")

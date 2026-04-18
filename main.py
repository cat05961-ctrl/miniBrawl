from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async
import asyncio

users = {}  # ник: пароль
chat_msgs = []

async def refresh(msg_box):
    while True:
        msg_box.clear()
        for m in chat_msgs:
            msg_box.append(put_text(m))
        await asyncio.sleep(1)

async def main():
    put_markdown("## 🔐 Вход / Регистрация")

    data = await input_group("Аккаунт", [
        input("Ник", name="user"),
        input("Пароль", type=PASSWORD, name="pass"),
        actions(name="act", buttons=[
            {"label": "Войти", "value": "login"},
            {"label": "Регистрация", "value": "register"}
        ])
    ])

    user = data["user"]
    password = data["pass"]

    # РЕГИСТРАЦИЯ
    if data["act"] == "register":
        if user in users:
            put_error("❌ Такой ник уже есть")
            return
        users[user] = password
        put_success("✅ Аккаунт создан!")

    # ВХОД
    elif data["act"] == "login":
        if user not in users or users[user] != password:
            put_error("❌ Неверный логин или пароль")
            return

    chat_msgs.append(f"🟢 {user} зашёл")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    run_async(refresh(msg_box))

    score = 0

    while True:
        data = await input_group("Чат / Игра", [
            input("Сообщение", name="msg"),
            actions(name="cmd", buttons=[
                {"label": "📨 Отправить", "value": "send"},
                {"label": "🎮 Клик", "value": "click"}
            ])
        ])

        if data["cmd"] == "send":
            chat_msgs.append(f"{user}: {data['msg']}")

        elif data["cmd"] == "click":
            score += 1
            chat_msgs.append(f"🎮 {user}: {score}")

# Render запуск
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    start_server(main, host="0.0.0.0", port=port)
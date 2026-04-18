from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async
import asyncio
import os
import random

# ===== ДАННЫЕ =====
users = {}
coins = {}
level = {}
hp = {}
chat_msgs = []

# ===== ЧАТ =====
async def chat(user):
    clear()
    put_markdown("## 💬 Чат")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    async def refresh():
        last = 0
        while True:
            await asyncio.sleep(1)
            if len(chat_msgs) > last:
                for m in chat_msgs[last:]:
                    msg_box.append(put_text(m))
                last = len(chat_msgs)

    run_async(refresh())

    while True:
        data = await input_group("Сообщение", [
            input(name="msg"),
            actions(name="cmd", buttons=["Отправить", "Назад"])
        ])

        if data["cmd"] == "Назад":
            break

        if data["msg"]:
            chat_msgs.append(f"{user}: {data['msg']}")

# ===== ИГРА =====
async def game(user):
    if user not in coins:
        coins[user] = 0
        level[user] = 1
        hp[user] = 100

    while True:
        clear()

        put_markdown(f"""
## 🎮 Mini Brawl

👤 {user}  
💰 {coins[user]}  
⭐ lvl {level[user]}  
❤️ HP {hp[user]}
""")

        data = await input_group("Меню", [
            actions(name="cmd", buttons=[
                "Клик",
                "Бой",
                "Чат",
                "Выход"
            ])
        ])

        if data["cmd"] == "Клик":
            coins[user] += 1

        elif data["cmd"] == "Бой":
            dmg = random.randint(5, 15)
            hp[user] -= random.randint(1, 10)

            if hp[user] <= 0:
                hp[user] = 50
                put_text("Ты проиграл")
            else:
                coins[user] += dmg
                put_text(f"+{dmg} монет")

        elif data["cmd"] == "Чат":
            await chat(user)

        elif data["cmd"] == "Выход":
            break

# ===== ЛОГИН =====
async def login():
    while True:
        data = await input_group("Вход", [
            input("Логин", name="user"),
            password("Пароль", name="pass"),
            actions(name="cmd", buttons=["Войти", "Регистрация"])
        ])

        user = data["user"]
        pas = data["pass"]

        if data["cmd"] == "Регистрация":
            users[user] = pas
            put_text("Аккаунт создан")

        else:
            if user in users and users[user] == pas:
                return user
            else:
                put_text("Ошибка входа")

# ===== MAIN =====
async def main():
    user = await login()
    await game(user)

# 🔥 ВАЖНО ДЛЯ RENDER
port = int(os.environ.get("PORT", 8080))

start_server(main, host="0.0.0.0", port=port)
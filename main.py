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

    put_html("""
    <style>
    body {background:#1e1e2f; color:white;}
    .msg {padding:8px; margin:5px; border-radius:10px; background:#2e2e4f;}
    .me {background:#4e8cff;}
    .sys {color:gray; font-size:12px;}
    input {font-size:18px;}
    button {font-size:18px;}
    </style>
    """)

    put_markdown("## 💬 Чат")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    chat_msgs.append(f"<span class='sys'>🟢 {user} вошёл</span>")

    async def refresh():
        last = 0
        while True:
            await asyncio.sleep(1)
            if len(chat_msgs) > last:
                for m in chat_msgs[last:]:
                    msg_box.append(put_html(m))
                last = len(chat_msgs)

    run_async(refresh())

    while True:
        data = await input_group("", [
            input(name="msg", placeholder="Напиши сообщение..."),
            actions(name="cmd", buttons=["📨", "🔙"])
        ])

        if data["cmd"] == "🔙":
            chat_msgs.append(f"<span class='sys'>🔴 {user} вышел</span>")
            break

        msg = data["msg"]

        if msg.strip():
            if msg.startswith("/"):
                if msg == "/clear":
                    chat_msgs.clear()
                elif msg == "/help":
                    chat_msgs.append("<span class='sys'>Команды: /clear /help</span>")
            else:
                chat_msgs.append(f"<div class='msg'><b>{user}:</b> {msg}</div>")

# ===== ТОП =====
def show_top():
    put_markdown("## 🏆 Топ игроков")

    top = sorted(coins.items(), key=lambda x: x[1], reverse=True)

    for i, (u, c) in enumerate(top[:10], 1):
        put_text(f"{i}. {u} — {c}💰 | lvl {level.get(u,1)}")

# ===== БОЙ =====
async def battle(user):
    enemy_hp = 50 + level[user]*10

    while True:
        clear()
        put_markdown(f"""
## ⚔️ Бой

❤️ Твоё HP: {hp[user]}  
👹 Враг HP: {enemy_hp}
""")

        data = await input_group("Действие", [
            actions(name="cmd", buttons=["💥 Атака", "🏃 Убежать"])
        ])

        if data["cmd"] == "🏃 Убежать":
            break

        dmg = random.randint(5, 15) + level[user]
        enemy_hp -= dmg

        enemy_dmg = random.randint(3, 10)
        hp[user] -= enemy_dmg

        if enemy_hp <= 0:
            coins[user] += 20
            level[user] += 1
            hp[user] = 100 + level[user]*10
            toast("🎉 Победа!")
            break

        if hp[user] <= 0:
            hp[user] = 50
            toast("💀 Поражение")
            break

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
💰 Монеты: {coins[user]}  
⭐ Уровень: {level[user]}  
❤️ HP: {hp[user]}
""")

        show_top()

        data = await input_group("Меню", [
            actions(name="cmd", buttons=[
                "💥 Клик (+1)",
                "⚔️ Бой",
                "💬 Чат",
                "🚪 Выйти"
            ])
        ])

        if data["cmd"] == "💥 Клик (+1)":
            coins[user] += 1

        elif data["cmd"] == "⚔️ Бой":
            await battle(user)

        elif data["cmd"] == "💬 Чат":
            await chat(user)

        elif data["cmd"] == "🚪 Выйти":
            break

# ===== ЛОГИН =====
async def login():
    while True:
        data = await input_group("🔐 Вход", [
            input("Логин", name="user"),
            password("Пароль", name="pass"),
            actions(name="cmd", buttons=["Войти", "Регистрация"])
        ])

        user = data["user"]
        pas = data["pass"]

        if data["cmd"] == "Регистрация":
            users[user] = pas
            coins[user] = 0
            level[user] = 1
            hp[user] = 100
            put_text("✅ Аккаунт создан")

        else:
            if user in users and users[user] == pas:
                return user
            else:
                toast("❌ Неверный пароль")

# ===== MAIN =====
async def main():
    put_html("""
    <style>
    body {background:#1e1e2f; color:white;}
    button {font-size:18px;}
    input {font-size:18px;}
    </style>
    """)

    user = await login()
    await game(user)

port = int(os.environ.get("PORT", 8080))
start_server(main, port=port)
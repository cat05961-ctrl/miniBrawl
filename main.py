from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async
import asyncio
import os

chat_msgs = []
online_users = set()

MAX_MSG = 50

async def refresh(msg_box):
    last_idx = 0
    while True:
        await asyncio.sleep(1)
        if len(chat_msgs) > last_idx:
            for m in chat_msgs[last_idx:]:
                msg_box.append(put_markdown(m))
            last_idx = len(chat_msgs)

async def main():
    global chat_msgs

    put_html("""
    <style>
    body {background:#1e1e2f; color:white;}
    .msg {padding:5px; margin:5px; border-radius:10px; background:#2e2e4f;}
    </style>
    """)

    put_markdown("## 💬 Онлайн чат")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    nickname = await input("👤 Твой ник")
    online_users.add(nickname)

    chat_msgs.append(f"**🟢 {nickname} зашел в чат**")

    run_async(refresh(msg_box))

    while True:
        data = await input_group("✏️ Сообщение", [
            input(name="msg", placeholder="Напиши что-нибудь..."),
            actions(name="cmd", buttons=["📨 Отправить", "🚪 Выйти"])
        ])

        if data["cmd"] == "🚪 Выйти":
            chat_msgs.append(f"**🔴 {nickname} вышел**")
            online_users.remove(nickname)
            break

        msg = data["msg"]

        if msg.strip() == "":
            continue

        chat_msgs.append(f"**{nickname}:** {msg}")

        if len(chat_msgs) > MAX_MSG:
            chat_msgs = chat_msgs[-MAX_MSG:]

port = int(os.environ.get("PORT", 8080))
start_server(main, port=port)
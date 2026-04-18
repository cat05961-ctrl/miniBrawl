from pywebio import start_server
from pywebio.input import input, input_group, actions
from pywebio.output import *
from pywebio.session import run_async
import asyncio

chat_msgs = []
online_users = set()

async def main():
    global chat_msgs

    put_markdown("## 📱 Mini Brawl Chat")

    # ВХОД
    nickname = await input("Введите ник:")
    password = await input("Введите пароль:", type="password")

    # простая проверка
    if password != "1234":
        put_error("❌ Неверный пароль")
        return

    online_users.add(nickname)

    put_success(f"✅ Ты вошёл как {nickname}")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    chat_msgs.append(("📢", f"{nickname} зашел в чат"))

    async def refresh():
        while True:
            msg_box.clear()
            for m in chat_msgs:
                msg_box.append(put_text(f"{m[0]} {m[1]}"))
            await asyncio.sleep(1)

    run_async(refresh())

    # ЧАТ
    while True:
        data = await input_group("💬 Сообщение", [
            input(name="msg", placeholder="Текст..."),
            actions(name="cmd", buttons=["Отправить", "Выйти"])
        ])

        if data is None or data["cmd"] == "Выйти":
            break

        chat_msgs.append((nickname, data["msg"]))

    online_users.remove(nickname)
    put_warning("Ты вышел")

# ОБЯЗАТЕЛЬНО!
if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
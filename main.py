from pywebio import start_server
from pywebio.input import input, input_group, actions, PASSWORD
from pywebio.output import *
from pywebio.session import run_async
import asyncio, os

users = {}
chat_rooms = {"global": []}
scores = {}

# ===== ОБНОВЛЕНИЕ =====
async def refresh(box, room):
    last = 0
    while True:
        msgs = chat_rooms.get(room, [])
        if len(msgs) != last:
            box.clear()
            for m in msgs[-50:]:
                box.append(put_text(m))
            last = len(msgs)
        await asyncio.sleep(1)

# ===== ЧАТ =====
async def chat(user):
    clear()

    room = "global"  # пока один чат (чтобы не ломалось)

    put_markdown("## 💬 Чат")
    box = output()
    put_scrollable(box, height=300)

    run_async(refresh(box, room))

    chat_rooms[room].append(f"🟢 {user} вошёл")

    while True:
        data = await input_group("", [
            input(name="msg", placeholder="Сообщение..."),
            actions(name="cmd", buttons=["Отправить", "Назад"])
        ])

        if not data:
            continue

        if data["cmd"] == "Назад":
            chat_rooms[room].append(f"🔴 {user} вышел")
            break

        msg = data.get("msg")

        if msg:
            chat_rooms[room].append(f"{user}: {msg}")

# ===== ИГРА =====
async def game(user):
    scores.setdefault(user, 0)

    while True:
        clear()

        put_markdown(f"""
## 🎮 Игра

👤 {user}  
💰 Очки: {scores[user]}
""")

        data = await input_group("Меню", [
            actions(name="cmd", buttons=[
                "Клик",
                "Чат",
                "Топ",
                "Выход"
            ])
        ])

        if not data:
            continue

        if data["cmd"] == "Клик":
            scores[user] += 1

        elif data["cmd"] == "Чат":
            await chat(user)

        elif data["cmd"] == "Топ":
            top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            popup("🏆 Топ", "\n".join(f"{u}: {s}" for u, s in top[:5]))

        elif data["cmd"] == "Выход":
            break

# ===== ВХОД =====
async def login():
    while True:
        clear()

        data = await input_group("🔐 Аккаунт", [
            input("Ник", name="user"),
            input("Пароль", type=PASSWORD, name="pass"),
            actions(name="cmd", buttons=["Войти", "Регистрация"])
        ])

        if not data:
            continue

        user = data["user"]
        pas = data["pass"]

        if data["cmd"] == "Регистрация":
            if not user or not pas:
                toast("❌ Пусто")
                continue

            if user in users:
                toast("❌ Уже есть")
            else:
                users[user] = pas
                toast("✅ Аккаунт создан")

        elif data["cmd"] == "Войти":
            if user in users and users[user] == pas:
                return user
            else:
                toast("❌ Неверно")

# ===== MAIN =====
async def main():
    user = await login()
    await game(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    start_server(main, host="0.0.0.0", port=port)
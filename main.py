from pywebio import start_server
from pywebio.input import input, input_group, actions, PASSWORD
from pywebio.output import put_text, put_markdown, output, put_scrollable, popup
from pywebio.session import run_async
import asyncio
import os

users = {}
chat_rooms = {"global": []}
scores = {}

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

async def choose_room():
    while True:
        rooms = list(chat_rooms.keys())
        choice = await input_group("Чаты", [
            actions(name="cmd", buttons=rooms + ["Создать"])
        ])

        cmd = choice["cmd"]

        if cmd == "Создать":
            name = await input("Название")
            if name and name not in chat_rooms:
                chat_rooms[name] = []
        else:
            return cmd

async def chat(user):
    room = await choose_room()

    put_markdown(f"## Чат: {room}")
    box = output()
    put_scrollable(box, height=300)

    run_async(refresh(box, room))

    chat_rooms[room].append(f"{user} вошёл")

    while True:
        data = await input_group("", [
            input(name="msg"),
            actions(name="cmd", buttons=["Отправить", "Назад"])
        ])

        if data["cmd"] == "Назад":
            chat_rooms[room].append(f"{user} вышел")
            break

        if data["msg"]:
            chat_rooms[room].append(f"{user}: {data['msg']}")

async def game(user):
    scores.setdefault(user, 0)

    while True:
        put_markdown(f"## Игрок: {user} | Очки: {scores[user]}")

        data = await input_group("Меню", [
            actions(name="cmd", buttons=[
                "Клик",
                "Чат",
                "Топ",
                "Выход"
            ])
        ])

        if data["cmd"] == "Клик":
            scores[user] += 1

        elif data["cmd"] == "Чат":
            await chat(user)

        elif data["cmd"] == "Топ":
            top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            text = "\n".join(f"{u}: {s}" for u, s in top[:5])
            popup("Топ", text)

        elif data["cmd"] == "Выход":
            break

async def login():
    while True:
        data = await input_group("Аккаунт", [
            input("Ник", name="user"),
            input("Пароль", type=PASSWORD, name="pass"),
            actions(name="cmd", buttons=["Войти", "Регистрация"])
        ])

        user = data["user"]
        pas = data["pass"]

        if data["cmd"] == "Регистрация":
            if user not in users:
                users[user] = pas
            else:
                put_text("Уже есть")

        elif data["cmd"] == "Войти":
            if user in users and users[user] == pas:
                return user
            else:
                put_text("Ошибка")

async def main():
    user = await login()
    await game(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    start_server(main, host="0.0.0.0", port=port)
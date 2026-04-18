from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async
import asyncio, json, os

CHAT_FILE = "chat.json"
SCORE_FILE = "score.json"

# ===== загрузка =====
def load(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

# ===== сохранение =====
def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# ===== чат обновление =====
async def refresh(msg_box, room):
    last = ""
    while True:
        data = load(CHAT_FILE)
        msgs = data.get("rooms", {}).get(room, [])
        text = "\n".join(msgs)

        if text != last:
            msg_box.clear()
            msg_box.append(put_text(text))
            last = text

        await asyncio.sleep(1)

# ===== выбор комнаты =====
async def choose_room():
    while True:
        data = load(CHAT_FILE)
        rooms = list(data.get("rooms", {}).keys())

        choice = await select("Выбери чат", rooms + ["➕ Создать"])

        if choice == "➕ Создать":
            name = await input("Название чата")
            if name:
                data["rooms"][name] = []
                save(CHAT_FILE, data)
        else:
            return choice

# ===== чат =====
async def chat(user):
    room = await choose_room()

    clear()
    put_markdown(f"## 💬 Чат: {room}")

    msg_box = output()
    put_scrollable(msg_box, height=300)

    run_async(refresh(msg_box, room))

    while True:
        data = await input_group("Сообщение", [
            input(name="msg"),
            actions(name="cmd", buttons=["📨", "🔙"])
        ])

        if data["cmd"] == "🔙":
            break

        if data["msg"]:
            chat = load(CHAT_FILE)
            chat["rooms"][room].append(f"{user}: {data['msg']}")
            save(CHAT_FILE, chat)

# ===== игра =====
async def game(user):
    scores = load(SCORE_FILE)
    scores.setdefault(user, 0)

    while True:
        clear()
        put_markdown(f"## 🎮 Игра\n👤 {user}\n💰 {scores[user]}")

        data = await input_group("Меню", [
            actions(name="cmd", buttons=[
                "💥 Клик",
                "💬 Чат",
                "🏆 Топ",
                "🚪 Выход"
            ])
        ])

        if data["cmd"] == "💥 Клик":
            scores[user] += 1

        elif data["cmd"] == "💬 Чат":
            await chat(user)

        elif data["cmd"] == "🏆 Топ":
            top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            text = "\n".join([f"{u}: {s}" for u, s in top[:5]])
            popup("🏆 Топ", text)

        elif data["cmd"] == "🚪 Выход":
            break

        save(SCORE_FILE, scores)

# ===== вход =====
async def main():
    put_markdown("## 🔐 Вход")
    user = await input("Ник")

    await game(user)

# ===== запуск =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    start_server(main, host="0.0.0.0", port=port)
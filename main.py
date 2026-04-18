from pywebio import start_server
from pywebio.input import input
from pywebio.output import put_text
import os

chat = []

def main():
    name = input("Твой ник")

    while True:
        msg = input("Сообщение")
        chat.append(f"{name}: {msg}")

        put_text("----- ЧАТ -----")
        for m in chat[-10:]:
            put_text(m)

port = int(os.environ.get("PORT", 8080))
start_server(main, port=port)
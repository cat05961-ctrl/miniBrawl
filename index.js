const { Telegraf } = require("telegraf");
const axios = require("axios");
const sqlite3 = require("sqlite3").verbose();

const PANEL_BOT_TOKEN = "ТВОЙ_ТОКЕН_ПАНЕЛИ";

const bot = new Telegraf(PANEL_BOT_TOKEN);

const db = new sqlite3.Database("database.db");

db.run(`
CREATE TABLE IF NOT EXISTS bots (
    user_id INTEGER,
    token TEXT,
    username TEXT
)
`);

bot.start((ctx) => {
    ctx.reply(
        "Отправь токен своего бота.\n\nПример:\n123456:ABCDEF..."
    );
});

bot.on("text", async (ctx) => {
    const token = ctx.message.text.trim();

    try {
        const res = await axios.get(
            `https://api.telegram.org/bot${token}/getMe`
        );

        if (!res.data.ok) {
            return ctx.reply("❌ Неверный токен");
        }

        const username = res.data.result.username;

        db.run(
            "INSERT INTO bots(user_id, token, username) VALUES(?,?,?)",
            [ctx.from.id, token, username]
        );

        ctx.reply(
            `✅ Бот подключен\n\n🤖 @${username}`
        );

    } catch {
        ctx.reply("❌ Токен не работает");
    }
});

bot.launch();

console.log("Bot started");
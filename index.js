const express = require("express");
const { Telegraf } = require("telegraf");

const app = express();
app.get("/", (req, res) => res.send("Bot is alive"));
app.listen(process.env.PORT || 3000);

const TOKEN = process.env.8810632130:AAHZWZtG8NiEhPf0Ef7mvqJNP5VqGkx3Fkk;

if (!TOKEN) {
    console.log("❌ BOT_TOKEN не найден в переменных Render");
    process.exit(1);
}

const bot = new Telegraf(TOKEN);

const CHANNEL = "@ReallTimeTG";
const PROMO = "SOSIVNKOQWOLNFIJ";
const IP = "ReallTime.kitpvp.su";

bot.start((ctx) => {
    ctx.reply(
        "🎁 Получите награду!\n\n" +
        "📢 Подпишитесь на канал: " + CHANNEL + "\n\n" +
        "🖥 IP сервера: " + IP,
        {
            reply_markup: {
                inline_keyboard: [
                    [{ text: "✅ Проверить подписку", callback_data: "check" }]
                ]
            }
        }
    );
});

bot.action("check", async (ctx) => {
    try {
        const member = await ctx.telegram.getChatMember(
            CHANNEL,
            ctx.from.id
        );

        if (["member", "administrator", "creator"].includes(member.status)) {
            return ctx.reply(
                "✅ Подписка подтверждена!\n\n" +
                "🎟 Промокод: " + PROMO + "\n" +
                "🖥 IP: " + IP
            );
        } else {
            return ctx.reply("❌ Ты не подписан на канал");
        }
    } catch (e) {
        console.log(e);
        return ctx.reply("⚠ Ошибка проверки (бот должен быть админом канала)");
    }
});

bot.launch();
console.log("Bot started");
const express = require("express");
const { Telegraf } = require("telegraf");

const app = express();
app.get("/", (req, res) => res.send("Bot is alive"));
app.listen(process.env.PORT || 3000);

const bot = new Telegraf(process.env.8810632130:AAHZWZtG8NiEhPf0Ef7mvqJNP5VqGkx3Fkk);

const CHANNEL = "@ReallTimeTG";
const PROMO = "SOSIVNKOQWOLNFIJ";
const IP = "ReallTime.kitpvp.su";

bot.start((ctx) => {
    return ctx.reply(
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
        return ctx.reply("⚠ Ошибка. Добавь бота в админы канала.");
    }
});

bot.launch();

console.log("Bot started");
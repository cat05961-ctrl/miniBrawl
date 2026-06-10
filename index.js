const { Telegraf } = require("telegraf");

const bot = new Telegraf("8810632130:AAHZWZtG8NiEhPf0Ef7mvqJNP5VqGkx3Fkk");

const CHANNEL = "@ReallTimeTG";
const PROMO = "SOSIVNKOQWOLNFIJ";
const IP = "ReallTime.kitpvp.su";

bot.start(async (ctx) => {
    return ctx.reply(
        "🎁 Получите награду!\n\n" +
        "📢 Подпишитесь на канал: " + CHANNEL + "\n\n" +
        "Нажмите кнопку ниже для проверки.\n\n" +
        "🖥 IP: " + IP,
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
                "🎟 Промокод:\n" + PROMO + "\n\n" +
                "🖥 IP: " + IP
            );
        } else {
            return ctx.reply("❌ Вы не подписаны на канал " + CHANNEL);
        }
    } catch (e) {
        return ctx.reply(
            "⚠ Ошибка проверки.\nУбедись что бот добавлен в админы канала."
        );
    }
});

bot.launch();
console.log("Bot started");
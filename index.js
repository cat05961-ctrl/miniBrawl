const { Telegraf } = require("telegraf");

const bot = new Telegraf("8810632130:AAHZWZtG8NiEhPf0Ef7mvqJNP5VqGkx3Fkk");

const CHANNEL = "@ReallTimeTG";
const PROMO = "/SISONDEKWORDWRSL";
const IP = "ReallTime.kitpvp.su";

bot.start(async (ctx) => {
    return ctx.reply(
        "🎁 Получите награду!\n\n" +
        "Подпишитесь на канал и нажмите проверку.\n\n" +
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
    const chatId = ctx.from.id;

    try {
        const member = await ctx.telegram.getChatMember(CHANNEL, chatId);

        if (["member", "administrator", "creator"].includes(member.status)) {
            return ctx.reply(
                "✅ Подписка подтверждена!\n\n" +
                "🎟 Промокод: " + PROMO + "\n" +
                "🖥 IP: " + IP
            );
        } else {
            return ctx.reply("❌ Вы не подписаны на канал.");
        }
    } catch (e) {
        return ctx.reply("⚠ Ошибка проверки подписки. Добавь бота в админы канала.");
    }
});

bot.launch();
console.log("Bot started");
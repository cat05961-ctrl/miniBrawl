const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mineflayer = require('mineflayer');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
app.use(express.static('public'));

const bots = new Map(); // имя бота -> объект бота

io.on('connection', (socket) => {
    console.log('Клиент подключён');

    // Запуск ботов
    socket.on('start', (cfg) => {
        const { host, port, count, prefix, regPass, loginPass, spamCmd, spamDelay, autoRejoin } = cfg;
        for (let i = 1; i <= count; i++) {
            const name = `${prefix}${i}`;
            let spamInterval = null;

            const bot = mineflayer.createBot({
                host, port,
                username: name,
                version: '1.20.4'
            });

            bot.on('spawn', () => {
                bots.set(name, bot);
                socket.emit('status', { name, status: 'connected' });

                setTimeout(() => {
                    if (regPass) bot.chat(`/register ${regPass}`);
                    setTimeout(() => {
                        if (loginPass) bot.chat(`/login ${loginPass}`);
                        socket.emit('status', { name, status: 'registered' });
                        if (spamCmd && spamDelay > 0) {
                            spamInterval = setInterval(() => bot.chat(spamCmd), spamDelay);
                        }
                    }, 500);
                }, 2000);
            });

            bot.on('end', () => {
                if (spamInterval) clearInterval(spamInterval);
                bots.delete(name);
                socket.emit('status', { name, status: 'disconnected' });
                if (autoRejoin) {
                    setTimeout(() => {
                        socket.emit('rejoin', { name, cfg });
                    }, 5000);
                }
            });

            bot.on('error', (err) => {
                socket.emit('status', { name, status: `error: ${err.message}` });
            });
        }
    });

    // Остановка всех ботов
    socket.on('stop', () => {
        for (let bot of bots.values()) bot.end();
        bots.clear();
        socket.emit('allStopped');
    });

    // Отправить команду всем ботам
    socket.on('command', (cmd) => {
        for (let bot of bots.values()) bot.chat(cmd);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`Сервер запущен на порту ${PORT}`);
});
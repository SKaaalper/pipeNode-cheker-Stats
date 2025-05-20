# 📡 Pipe Node Checker

## Скрипт на Python для мониторинга PoP-нод в тестовой сети Pipe Network.

🧾 Чтение списка Node ID из файла

📊 Вывод метрик в виде таблицы в консоли

📬 Уведомления в Telegram в Markdown-формате

### 📦 Установка и настройка

создайде и войдите в сессию tmux или screen (без разницы) что вам больше нравится
```bash
git clone https://github.com/noderguru/pipeNode-cheker-Stats.git
cd pipeNode-cheker-Stats
```
```bash
python3 -m venv venv
source venv/bin/activate
```
```bash
pip install requests beautifulsoup4 tabulate python-dotenv
```
```bash
nano .env
```
BOT_TOKEN — токен Telegram-бота. Создайте бота через @BotFather затем зайдите в него и нажмите start

CHAT_ID — Получите ваш CHAT_ID через @userinfobot

SEND_TELEGRAM — true или false  если false то данные будут выводится только в консоль

TELEGRAM_INTERVAL — интервал между циклами отправки сообщений (в секундах)

REQUEST_DELAY_MIN/MAX — задержки между запросами к разным нодам
```bash
nano node_ids.txt
```
вставьте pop_id каждый с новой строки. Можно получить в логах при старте ноды или из файла ```.pop_state.json``` или ```curl -sk https://localhost/state && echo -e "\n"``` (по желанию через пробел можете написать коментарий
```bash
python3 pipe_cheker.py
```
![image](https://github.com/user-attachments/assets/91f35ebb-0090-44d5-a374-e3285c168b31)

![image](https://github.com/user-attachments/assets/f5c85d0c-ef84-4376-89ec-d1bbb193e913)










# 📡 Pipe Node Checker

## Python script for monitoring PoP nodes in the Pipe Network testnet.

🧾 Reads a list of Node IDs from a file

📊 Outputs key performance metrics in a formatted table in the terminal

📬 Sends notifications to Telegram in Markdown format

---

**First Check your `PoP ID` Go to your terminal and run**:
```
curl -sk https://localhost/state && echo -e "\n"
```
- If your PoP ID is `0`, [Go HERE](https://github.com/SKaaalper/Pipe-Network-Testnet?tab=readme-ov-file#pop-id-error-guide) to configure your `PoP ID`

## 📦 Installation and Setup

First, create and enter a session using either `tmux` or `screen` (choose whichever you prefer) to keep the script running in the background even after disconnecting from your terminal:

### 1. Clone the Repo:
```
git clone https://github.com/SKaaalper/pipeNode-cheker-Stats.git
cd pipeNode-cheker-Stats
```

### 2. Create and activate a virtual environment (recommended for dependency isolation):
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required Python dependencies:
```
pip install requests beautifulsoup4 tabulate python-dotenv
```

### 4. Now configure your environment variables:
```
nano .env
```

- **Add the following variables**:

- `BOT_TOKEN` — Telegram bot token.
You can create a new bot via [@BotFather](https://t.me/BotFather)). After creating the bot, open the bot in Telegram and press Start to activate it.

- `CHAT_ID` — Your Telegram Chat ID.
You can retrieve this using [@userinfobot](https://t.me/userinfobot). Just message the bot and it will return your numeric Chat ID.

- `SEND_TELEGRAM` — true or false.
If set to true, the script will send status updates to Telegram. If set to false, updates will only be printed to the terminal.

- `TELEGRAM_INTERVAL` — Interval between Telegram notifications, in seconds (e.g. 300 for 5 minutes).

- `REQUEST_DELAY_MIN` / `REQUEST_DELAY_MAX` — Randomized delay range (in seconds) between checking each node, to avoid overloading the server.

- Example `.env`:
```
BOT_TOKEN=123456789:ABCdEfGhIJklMnopQRsTuvwxYZ
CHAT_ID=987654321
SEND_TELEGRAM=true
TELEGRAM_INTERVAL=300
REQUEST_DELAY_MIN=5
REQUEST_DELAY_MAX=10
```

### 5. Create your list of node IDs:
```
nano node_ids.txt
```
- Inside this file, paste each node’s `pop_id`, one per line.
- You can obtain these IDs in one of the following ways:
- From the logs printed when your node starts.
- From the `.pop_state.json` file in your node directory.

By running:
```
curl -sk https://localhost/state && echo -e "\n"
```
![image](https://github.com/user-attachments/assets/fef2feca-1f2a-4854-be52-fd201069742b)


### 6. (Optional) To keep the monitor running 24/7, keep it inside `tmux` or `screen`:

- Using `screen`:
```
screen -S pipe-checker
```

- using `tmux`:
```
tmux new -s pipe-checker
```

- You can detach from the session anytime by pressing:
  - **screen** detach: Press `Ctrl + A, Then Press `D`
  - **tmux** detach: Press `Ctrl + B, Then Press `D`
 
### 7. Start the script:
```
python3 pipe_cheker.py
```

![image](https://github.com/user-attachments/assets/f58e076f-621c-4e95-a7e0-a30632bae902)

### 8. Go to your telegram bot, check the result:

![image](https://github.com/user-attachments/assets/ddfaac78-96d4-4904-a9f4-e5d947e0204f)

Guide to run [Pipe Network Testnet](https://github.com/SKaaalper/Pipe-Network-Testnet)

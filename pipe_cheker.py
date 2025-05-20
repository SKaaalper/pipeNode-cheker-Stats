import os
import time
import random
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SEND_TELEGRAM = os.getenv("SEND_TELEGRAM", "false").lower() == "true"
TELEGRAM_INTERVAL = int(os.getenv("TELEGRAM_INTERVAL", 300))
REQUEST_DELAY = (
    float(os.getenv("REQUEST_DELAY_MIN", 5)),
    float(os.getenv("REQUEST_DELAY_MAX", 10))
)

NODE_IDS_FILE = "node_ids.txt"
URL_TEMPLATE = "https://dashboard.testnet.pipe.network/node/pop-{}"


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"[Telegram ❌] {response.status_code}: {response.text}")
        else:
            print("[Telegram ✅] Notification sent.")
    except Exception as e:
        print(f"[Telegram ❌] Error: {e}")


def check_all_nodes():
    node_list = []
    with open(NODE_IDS_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(maxsplit=1)
            node_id = parts[0]
            comment = parts[1] if len(parts) > 1 else ""
            node_list.append((node_id, comment))

    results = []
    telegram_lines = []

    for idx, (node_id, comment) in enumerate(node_list, 1):
        label = f"pop-{node_id}" + (f" ({comment})" if comment else "")
        print(f"[{idx}/{len(node_list)}] 🔍 Checking {label}...")

        try:
            url = URL_TEMPLATE.format(node_id)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Status
            status = "-"
            identity_labels = soup.select("div.identity-label")
            for lbl in identity_labels:
                if lbl.text.strip() == "Status:":
                    status = lbl.find_next_sibling().text.strip()
                    break

            def get_metric(title):
                card = soup.find("h3", string=title)
                if card:
                    value_div = card.find_next("div", class_="metric-value")
                    rank_span = card.find_next("span", class_="metric-rank")
                    value = value_div.text.strip() if value_div else "-"
                    rank = rank_span.text.strip() if rank_span else "-"
                    return value, rank
                return "-", "-"

            cache_eff, cache_rank = get_metric("Cache Efficiency")
            bandwidth, bandwidth_rank = get_metric("Bandwidth Served")
            req_volume, req_rank = get_metric("Request Volume")
            node_score, score_rank = get_metric("Node Score")

            last_audit = "-"
            audit_table = soup.find("table", class_="audit-table")
            if audit_table:
                row = audit_table.find("tr")
                if row:
                    data_row = row.find_next_sibling("tr")
                    if data_row:
                        cols = [td.text.strip() for td in data_row.find_all("td")]
                        last_audit = " | ".join(cols) if cols else "-"

            results.append([
                label, status,
                f"{cache_eff} ({cache_rank})",
                f"{bandwidth} ({bandwidth_rank})",
                f"{req_volume} ({req_rank})",
                f"{node_score} ({score_rank})",
                last_audit
            ])

            emoji_status = "✅" if status == "active" else "❌"
            emoji_score = "🔥" if score_rank and "1" in score_rank else "📉"
            telegram_lines.append(
                f"*{label}* {emoji_status}\n"
                f"📦 Status: `{status}`\n"
                f"🧠 Cache: `{cache_eff} ({cache_rank})`\n"
                f"📡 Bandwidth: `{bandwidth} ({bandwidth_rank})`\n"
                f"📊 Requests: `{req_volume} ({req_rank})`\n"
                f"💯 Score: `{node_score} ({score_rank})` {emoji_score}\n"
                f"🕵️ Last Audit: `{last_audit}`\n"
            )

        except Exception as e:
            results.append([label, "Error", "-", "-", "-", "-", f"Err: {e}"])
            telegram_lines.append(f"*{label}* ❌\nError during check: `{e}`\n")

        time.sleep(random.uniform(*REQUEST_DELAY))

    headers = [
        "Node ID", "Status", "Cache % (Rank)",
        "Bandwidth (Rank)", "Requests (Rank)",
        "Score (Rank)", "Last Audit"
    ]
    print(tabulate(results, headers=headers, tablefmt="grid"))

    if SEND_TELEGRAM:
        full_message = "📡 *Pipe Node Check Report*\n\n" + "\n\n".join(telegram_lines)
        send_telegram_message(full_message)

print("🚀 Starting node monitoring. Press Ctrl+C to stop.")
try:
    while True:
        check_all_nodes()
        print(f"⏳ Next check in {TELEGRAM_INTERVAL} sec...\n")
        time.sleep(TELEGRAM_INTERVAL)
except KeyboardInterrupt:
    print("🛑 Monitoring stopped")

import requests
from datetime import datetime, timedelta
import os
# =========================
# SLACK CONFIG
# =========================

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_MEMBER_ID = os.getenv("SLACK_MEMBER_ID")

# =========================
# JOB
# =========================
def check_nse_orders():
    try:
        # NSE often requires a warm-up request to obtain cookies
        session = requests.Session()
        session.trust_env = False

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/",
        }

        today = datetime.now()
        yesterday = today - timedelta(days=1)

        from_date = yesterday.strftime("%d-%m-%Y")
        to_date = today.strftime("%d-%m-%Y")

        # Warm-up request
        session.get(
            "https://www.nseindia.com",
            headers=headers,
            timeout=30,
        )

        url = (
            "https://www.nseindia.com/api/corporate-announcements"
            f"?index=equities"
            f"&from_date={from_date}"
            f"&to_date={to_date}"
            f"&reqXbrl=false"
        )

        response = session.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        data_required = []

        for i in data:
            if i.get("desc") == "Bagging/Receiving of orders/contracts":
                data_required.append(
                    f"{i['sm_name']} : {i['attchmntFile']}"
                )

        if data_required:
            message = "\n\n".join(data_required)

            slack_headers = {
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json",
            }

            payload = {
                "channel": SLACK_MEMBER_ID,
                "text": message,
            }

            slack_response = requests.post(
                "https://slack.com/api/chat.postMessage",
                headers=slack_headers,
                json=payload,
                timeout=30,
            )

            print(slack_response.json())

        print(f"Checked at {datetime.now()}")

    except Exception as e:
        print(f"Error: {e}")


# =========================
# SCHEDULER
# =========================



# Run every 5 minutes

# Run once immediately
check_nse_orders()

print("NSE Order Monitor Started...")

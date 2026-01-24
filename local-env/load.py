import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime

BASE_URL = "http://muffin-wallet.ru"
THREADS = 5
DURATION_SECONDS = 45 * 60 
CREATE_RATIO = 0.2
LIST_RATIO = 0.3
GET_RATIO = 0.2
TX_RATIO = 0.3

wallet_ids = []
wallet_ids_lock = Lock()
operations_count = 0
ops_lock = Lock()

WALLET_TYPES = ["CHOKOLATE", "CARAMEL", "PLAIN"]


def random_name():
    return "Ivan_" + "".join(random.choices(string.ascii_lowercase, k=5))


def inc_ops():
    global operations_count
    with ops_lock:
        operations_count += 1


def create_wallet():
    payload = {
        "type": random.choice(WALLET_TYPES),
        "owner_name": random_name()
    }
    try:
        r = requests.post(f"{BASE_URL}/v1/muffin-wallets", json=payload, timeout=5)
        if r.status_code == 200 or r.status_code == 201:
            wallet_id = r.json()["id"]
            with wallet_ids_lock:
                wallet_ids.append(wallet_id)
        inc_ops()
    except Exception:
        pass


def list_wallets():
    params = {
        "owner_name": "Ivan",
        "page": random.randint(0, 2),
        "size": 10
    }
    try:
        requests.get(f"{BASE_URL}/v1/muffin-wallets", params=params, timeout=5)
        inc_ops()
    except Exception:
        pass


def get_wallet():
    with wallet_ids_lock:
        if not wallet_ids:
            return
        wallet_id = random.choice(wallet_ids)

    try:
        requests.get(f"{BASE_URL}/v1/muffin-wallets/{wallet_id}", timeout=5)
        inc_ops()
    except Exception:
        pass


def make_transaction():
    with wallet_ids_lock:
        if len(wallet_ids) < 2:
            return
        from_id, to_id = random.sample(wallet_ids, 2)

    payload = {
        "to_muffin_wallet_id": to_id,
        "amount": random.randint(1, 500)
    }

    try:
        requests.post(
            f"{BASE_URL}/v1/muffin-wallet/{from_id}/transaction",
            json=payload,
            timeout=5
        )
        inc_ops()
    except Exception:
        pass


def worker(end_time):
    while time.time() < end_time:
        r = random.random()
        if r < CREATE_RATIO:
            create_wallet()
        elif r < CREATE_RATIO + LIST_RATIO:
            list_wallets()
        elif r < CREATE_RATIO + LIST_RATIO + GET_RATIO:
            get_wallet()
        else:
            make_transaction()


def main():
    start_time = datetime.now()
    print(f"🚀 Load test started at {start_time}")
    end_time = time.time() + DURATION_SECONDS

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(worker, end_time) for _ in range(THREADS)]
        for _ in as_completed(futures):
            pass

    finish_time = datetime.now()
    print(f"✅ Load test finished at {finish_time}")
    print(f"📊 Total operations executed: {operations_count}")


if __name__ == "__main__":
    main()

import requests
import time

def send_payment(key, amount):
    url = "http://127.0.0.1:8080/payment"
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": key
    }
    data = {"amount": amount}
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"[{key}] Status {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"Error with key {key}: {e}")

def test_get_simulate():
    url = "http://127.0.0.1:8080/simulate"
    for i in range(5):
        response = requests.get(url)
        print(f"[GET try {i+1}] Status: {response.status_code}, Text: {response.text}")
        if response.status_code == 200:
            break
        time.sleep(1)

if __name__ == "__main__":
    send_payment("test-key-abc", 500)
    send_payment("test-key-def", 999)
    send_payment("test-key-abc", 777)
    test_get_simulate()

from flask import Flask, request, jsonify
from random import randint
import os

app = Flask(__name__)

idempotency_store = {}

@app.route("/simulate", methods=["GET"])
def simulate_failure():
    """Симуляція GET-запиту з імовірністю помилки 50%"""
    chance = randint(1, 10)
    if chance <= 5:
        return "Oops! Temporary server issue (simulated)", 500
    return "All good! Request successful", 200

@app.route("/payment", methods=["POST"])
def process_payment():
    """POST-запит з підтримкою ідемпотентності та симульованою нестабільністю"""
    key = request.headers.get("Idempotency-Key")
    data = request.get_json()
    amount = data.get("amount") if data else None

    # 30% шанс збоїв
    if randint(1, 10) <= 3:
        return "Temporary failure during processing", 500

    if not key:
        return "Missing Idempotency-Key in headers", 400

    # Якщо ключ вже існує — повертаємо попередній результат
    if key in idempotency_store:
        print(f"[INFO] Reusing existing transaction for key {key}")
        return jsonify(idempotency_store[key]), 200

    # Створення нової транзакції
    new_txn = {
        "status": "processed",
        "amount": amount,
        "tx_id": os.urandom(6).hex()
    }

    # Зберігаємо результат
    idempotency_store[key] = new_txn
    print(f"[INFO] New transaction processed for key {key}")
    return jsonify(new_txn), 200

if __name__ == "__main__":
    app.run(port=8080)

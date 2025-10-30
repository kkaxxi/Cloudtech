from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def hello():
    # Отримуємо ім'я користувача (з параметрів або з JSON)
    name = None
    if request.method == "GET":
        name = request.args.get("name", "world")
    elif request.is_json:
        data = request.get_json(silent=True)
        name = data.get("name", "world") if data else "world"
    else:
        name = "world"

    # Формуємо відповідь
    response = jsonify({
        "hello": name,
        "runtime": "python",
        "region": "render"
    })

    # Додаємо CORS-заголовки
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    # Якщо це запит OPTIONS — повертаємо порожню відповідь
    if request.method == "OPTIONS":
        return ("", 204)

    return response


if __name__ == "__main__":
    # Обов’язково: Render призначає PORT через змінну середовища
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def hello():
    name = request.args.get("name") or request.json.get("name") if request.is_json else "world"
    response = jsonify({
        "hello": name,
        "runtime": "python",
        "region": "render"
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    if request.method == "OPTIONS":
        return ('', 204)
    return response

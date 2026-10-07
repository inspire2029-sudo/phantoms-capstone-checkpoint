from flask import Flask, jsonify, request

from src.database import init_database, store_webhook_data

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if data is None:
        return (
            jsonify({"status": "error", "message": "Invalid or missing JSON"}),
            400,
        )

    store_webhook_data(data)
    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5000, debug=False)

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    body = request.get_json(silent=True) or {}

    sku = body.get("sku")
    quantity = body.get("quantity")

    # Validate SKU
    if not sku:
        return jsonify({
            "status": "rejected",
            "reason": "Missing SKU"
        }), 400

    # Validate quantity
    if quantity is None:
        return jsonify({
            "status": "rejected",
            "reason": "Missing quantity"
        }), 400

    # Validate quantity type
    if not isinstance(quantity, (int, float)):
        return jsonify({
            "status": "rejected",
            "reason": "Quantity must be a number"
        }), 400

    # Validate quantity value
    if quantity < 0:
        return jsonify({
            "status": "rejected",
            "reason": "Quantity cannot be negative"
        }), 400

    # Meridian Pivot decision
    if quantity == 0:
        decision = "out_of_stock"
        action = "Flag item as out of stock"
    elif quantity <= 5:
        decision = "low_stock"
        action = "Flag item for restocking"
    else:
        decision = "in_stock"
        action = "Inventory level is healthy"

    return jsonify({
        "status": "success",
        "decision": decision,
        "action": action,
        "data": {
            "sku": sku,
            "quantity": quantity
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

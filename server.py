from flask import Flask, request, jsonify
import uuid
from helpers import calculate_points

app = Flask(__name__)

receipts = {}


@app.route("/receipts/process", methods=['POST'])
def process_receipts():
    receipt = request.get_json()
    needed_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for field in needed_fields:
        if field not in receipt:
            return jsonify({"error": "The receipt is invalid."}), 400
    generated_id = str(uuid.uuid4())
    points = calculate_points(receipt)

    receipts[generated_id] = points

    return jsonify({"id": generated_id}), 200

@app.route("/receipts/<id>/points", methods=['GET'])
def get_points(id):
    if id in receipts:
        return jsonify({"points": receipts.get(id)})
    else:
        return jsonify({"error": "No receipt found for that ID."})

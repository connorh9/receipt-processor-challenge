from flask import Flask, request, jsonify
import uuid
from helpers import calculate_points

app = Flask(__name__)

receipts = {} #not using a database


@app.route("/receipts/process", methods=['POST'])
def process_receipts():
    """
    This function will accept a jsonified receipt and validate the receipt.
    It will then generate a unique uuid for it, calculate the points
    for the receipt, and store it in our local variable receipts where the key
    is the id and the value is the points total.

    Returns: JSON: the receipt id along with a 200 status code or an error if the 
    receipt is invalid
    """
    receipt = request.get_json()
    needed_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total'] #list of required fields for a valid receipt
    for field in needed_fields:
        if field not in receipt:
            return jsonify({"error": "The receipt is invalid."}), 400
        
    generated_id = str(uuid.uuid4()) #use the uuid module to generate a unique id
    points = calculate_points(receipt)

    receipts[generated_id] = points

    return jsonify({"id": generated_id}), 200

@app.route("/receipts/<id>/points", methods=['GET'])
def get_points(id):
    """
    Handles requests for retrieving the point total of a receipt.
    It uses the id passed in and sends back the points total of the receipt,
    if it exists.

    Returns: JSON: the points total and a 200 code if the receipt is found, otherwise
    a 404 error.
    """
    #check to see if the id exists
    if id in receipts:
        return jsonify({"points": receipts.get(id)}), 200
    else:
        return jsonify({"error": "No receipt found for that ID."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
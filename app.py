from flask import Flask, request, jsonify
from ai_core import generate_contract_code
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        solidity_code = generate_contract_code(prompt)
        return jsonify({"contract_code": solidity_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

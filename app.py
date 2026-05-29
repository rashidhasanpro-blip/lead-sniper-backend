from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import find_leads

app = Flask(__name__)

CORS(app)

@app.route("/search", methods=["POST"])

def search():

    data = request.json

    service = data.get("service")
    location = data.get("location")
    keyword = data.get("keyword")
    amount = data.get("amount")

    results = find_leads(
        service,
        location,
        keyword,
        amount
    )

    return jsonify({
        "status":"success",
        "data":results
    })

if __name__ == "__main__":
    app.run(debug=True)
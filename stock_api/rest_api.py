# rest_api.py
from datetime import datetime
from math import isnan

import yaml
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from pymongo import ASCENDING, DESCENDING, MongoClient

rest_api = Blueprint("rest_api", __name__)

with open("secret.yml", "r") as file:
    config = yaml.safe_load(file)
MongoURI = config["MONGO_URI"]

# Connect to MongoDB
client = MongoClient(MongoURI)
db = client["StockInfoDB"]
collection = db["company_overview"]
cash_flow_collection = db["cash_flow"]
quarterly_earnings_collection = db["quarterly_earnings"]
stock_weekly_data_collection = db["stock_weekly_data"]
news_sentiment_collection = db["news_sentiment"]

def process_data(data):
    if isinstance(data, dict):
        return {k: process_data(v) for k, v in data.items() if k != '_id'}
    elif isinstance(data, list):
        return [process_data(item) for item in data]
    elif isinstance(data, float) and isnan(data):
        # Convert NaN values to the string "NaN"
        return "NaN"
    else:
        return data

@rest_api.route("/company_overview", methods=["GET"])
def get_company_overview():
    symbol = request.args.get("symbol")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="asc")
    limit = request.args.get("limit", default=10, type=int)
    if symbol:
        company_data = collection.find_one({"Symbol": symbol}, {"_id": 0})
        if company_data:
            return jsonify({"response": process_data(company_data)})
        else:
            return jsonify({"error": "Company not found"}), 404
    elif sort_field:
        if sort_field not in [
            "Name",
            "Symbol",
            "PEGRatio",
            "MarketCapitalization",
            "Beta",
        ]:
            return jsonify({"error": "Invalid sort_field"}), 400
        if sort_order not in ["asc", "desc"]:
            return jsonify({"error": "Invalid sort_order"}), 400
        pymongo_sort_order = ASCENDING if sort_order == "asc" else DESCENDING
        companies = list(
            collection.find({}, {"_id": 0})
            .sort(sort_field, pymongo_sort_order)
            .limit(limit)
        )
        if companies:
            return {"response": dumps(companies)}
        else:
            return jsonify({"error": "No companies found"}), 404
    else:
        return jsonify({"error": "Symbol or sort_field parameter is required"}), 400


@rest_api.route("/cash_flow", methods=["GET"])
def get_cash_flow():
    symbol = request.args.get("symbol")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="asc")
    pymongo_sort_order = ASCENDING if sort_order == "asc" else DESCENDING
    documents = list(
        cash_flow_collection.find({"symbol": symbol}).sort(
            sort_field, pymongo_sort_order
        )
    )
    if documents:
        for document in documents:
            document["_id"] = str(document["_id"])
            for key, value in document.items():
                if isinstance(value, float) and isnan(value):
                    document[key] = None
        return jsonify(documents)
    else:
        return jsonify({"error": "Data not found"}), 404


@rest_api.route("/quarterly_earnings", methods=["GET"])
def get_quarterly_earnings():
    symbol = request.args.get("symbol")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="asc")
    pymongo_sort_order = ASCENDING if sort_order == "asc" else DESCENDING
    documents = list(
        quarterly_earnings_collection.find({"symbol": symbol}).sort(
            sort_field, pymongo_sort_order
        )
    )
    if documents:
        for document in documents:
            document["_id"] = str(document["_id"])
        return jsonify(documents)
    else:
        return jsonify({"error": "Data not found"}), 404


@rest_api.route("/stock_weekly_data", methods=["GET"])
def get_weekly_data():
    symbol = request.args.get("symbol")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="asc")
    pymongo_sort_order = ASCENDING if sort_order == "asc" else DESCENDING
    documents = list(
        stock_weekly_data_collection.find({"symbol": symbol}).sort(
            sort_field, pymongo_sort_order
        )
    )
    if documents:
        for document in documents:
            document["_id"] = str(document["_id"])
        return jsonify(documents), 200
    else:
        return jsonify({"error": "Data not found"}), 404


@rest_api.route("/news_sentiment", methods=["GET"])
def get_news_sentiment():
    symbol = request.args.get("symbol")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="asc")
    pymongo_sort_order = ASCENDING if sort_order == "asc" else DESCENDING
    documents = list(
        news_sentiment_collection.find({"ticket_number": symbol}).sort(
            sort_field, pymongo_sort_order
        )
    )
    if documents:
        for document in documents:
            document["_id"] = str(document["_id"])
            dt = datetime.strptime(document["time_published"], "%Y%m%dT%H%M%S")
            document["time_published"] = dt.strftime("%Y/%m/%d %H:%M")
        return jsonify(documents)
    else:
        return jsonify({"error": "Data not found"}), 404

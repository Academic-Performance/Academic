from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def overview():
    return render_template("overview.html")

@views_bp.route("/predict", methods=["GET"])
def predict():
    return render_template("predict.html")

import json

@views_bp.route("/model", methods=["GET"])
def model_info():
    try:
        with open("artifacts/model/metadata.json", "r") as f:
            metadata = json.load(f)
    except Exception:
        metadata = None
    return render_template("model.html", metadata=metadata)

@views_bp.route("/insights", methods=["GET"])
def insights():
    return render_template("insights.html")

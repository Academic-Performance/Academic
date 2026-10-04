from flask import Blueprint, request, jsonify
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData
from src.exception import CustomError
from src.logger import logging

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "model_available": True})

@api_bp.route("/predict", methods=["POST"])
def predict():
    try:
        # Expected either JSON or Form data
        data = request.json if request.is_json else request.form

        # Validation mapping
        custom_data = CustomData(
            gender=data.get("gender"),
            race_ethnicity=data.get("race_ethnicity"),
            parental_level_of_education=data.get("parental_level_of_education"),
            lunch=data.get("lunch"),
            test_preparation_course=data.get("test_preparation_course"),
            reading_score=data.get("reading_score"),
            writing_score=data.get("writing_score"),
        )

        pred_df = custom_data.get_data_as_data_frame()
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        return jsonify({
            "success": True, 
            "prediction": round(results[0], 2),
            "model": "BestModel",
            "model_version": "1.0.0"
        })
    except CustomError as ce:
        logging.error(f"Prediction CustomError: {str(ce)}")
        return jsonify({"success": False, "error": str(ce)}), 400
    except Exception as e:
        logging.error(f"Prediction Exception: {str(e)}")
        return jsonify({"success": False, "error": "Invalid input or processing failed."}), 400

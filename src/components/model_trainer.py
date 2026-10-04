import sys
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from datetime import datetime

from src.exception import CustomError
from src.logger import logging
from src.utils import evaluate_models, save_object, save_json

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = Path("artifacts/model/model.pkl")
    model_metadata_file_path = Path("artifacts/model/metadata.json")

MIN_MODEL_SCORE = 0.6

class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array: np.ndarray, test_array: np.ndarray) -> dict:
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            models = {
                "Random Forest": RandomForestRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "Linear Regression": LinearRegression(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False, random_seed=42),
                "AdaBoost Regressor": AdaBoostRegressor(random_state=42),
                "K-Neighbors Regressor": KNeighborsRegressor(),
            }
            params = {
                "Decision Tree": {
                    "criterion": ["squared_error", "friedman_mse"],
                },
                "Random Forest": {
                    "n_estimators": [8, 16, 32, 64],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.05, 0.01],
                    "n_estimators": [32, 64, 128],
                },
                "Linear Regression": {},
                "CatBoosting Regressor": {
                    "depth": [6, 8],
                    "learning_rate": [0.01, 0.05, 0.1],
                    "iterations": [30, 50, 100],
                },
                "AdaBoost Regressor": {
                    "learning_rate": [0.1, 0.01, 0.5],
                    "n_estimators": [32, 64, 128],
                },
                "K-Neighbors Regressor": {
                    "n_neighbors": [5, 7, 9],
                },
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            # Get best model score based on r2_score
            best_model_name = max(model_report, key=lambda k: model_report[k]["r2_score"])
            best_model_metrics = model_report[best_model_name]
            best_model_score = best_model_metrics["r2_score"]

            best_model = models[best_model_name]

            if best_model_score < MIN_MODEL_SCORE:
                raise CustomError("No best model found")
                
            logging.info(f"Best model found: {best_model_name} with R2: {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )
            
            # Save metadata
            metadata = {
                "model_name": best_model_name,
                "training_timestamp": datetime.now().isoformat(),
                "metrics": {
                    "r2_score": best_model_metrics["r2_score"],
                    "mae": best_model_metrics["mae"],
                    "rmse": best_model_metrics["rmse"]
                },
                "hyperparameters": best_model_metrics["best_params"],
                "random_seed": 42
            }
            save_json(self.model_trainer_config.model_metadata_file_path, metadata)

            return metadata
        except Exception as e:
            raise CustomError(e, sys)

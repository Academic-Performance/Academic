import pickle
import sys
import json
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV
from src.exception import CustomError

def save_object(file_path: str | Path, obj: object) -> None:
    try:
        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomError(e, sys)
        
def save_json(file_path: str | Path, data: dict) -> None:
    try:
        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise CustomError(e, sys)

def evaluate_models(X_train: object, y_train: object, X_test: object, y_test: object, models: dict, param: dict) -> dict:
    try:
        report = {}
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)

            r2 = r2_score(y_test, y_test_pred)
            mae = mean_absolute_error(y_test, y_test_pred)
            from sklearn.metrics import root_mean_squared_error
            rmse = root_mean_squared_error(y_test, y_test_pred)

            report[model_name] = {
                "r2_score": r2,
                "mae": mae,
                "rmse": rmse,
                "best_params": gs.best_params_
            }
        return report
    except Exception as e:
        raise CustomError(e, sys)

def load_object(file_path: str | Path) -> object:
    try:
        with Path(file_path).open("rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomError(e, sys)

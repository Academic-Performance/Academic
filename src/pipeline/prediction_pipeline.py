import sys
from pathlib import Path
import pandas as pd
from src.exception import CustomError
from src.utils import load_object

class PredictPipeline:
    def __init__(self) -> None:
        self.model_path = Path("artifacts/model/model.pkl")
        self.preprocessor_path = Path("artifacts/preprocessing/preprocessor.pkl")

    def predict(self, features: pd.DataFrame) -> object:
        try:
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)
            
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomError(e, sys)

class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: str | int | float,
        writing_score: str | int | float,
    ) -> None:
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        
        # Validation
        try:
            self.reading_score = float(reading_score)
            self.writing_score = float(writing_score)
        except (ValueError, TypeError):
            raise CustomError("Scores must be valid numbers.", sys)
            
        if not (0 <= self.reading_score <= 100) or not (0 <= self.writing_score <= 100):
            raise CustomError("Scores must be between 0 and 100.", sys)
            
        valid_genders = ["male", "female"]
        if self.gender not in valid_genders:
            raise CustomError(f"Gender must be one of {valid_genders}", sys)

    def get_data_as_data_frame(self) -> pd.DataFrame:
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomError(e, sys)

import pytest
from unittest.mock import patch
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.exception import CustomError

def test_custom_data_valid():
    data = CustomData(
        gender="female",
        race_ethnicity="group B",
        parental_level_of_education="bachelor's degree",
        lunch="standard",
        test_preparation_course="none",
        reading_score=72,
        writing_score=74
    )
    df = data.get_data_as_data_frame()
    assert len(df) == 1
    assert df["reading_score"].iloc[0] == 72.0

def test_custom_data_negative_score():
    with pytest.raises(CustomError, match="between 0 and 100"):
        CustomData(
            gender="female",
            race_ethnicity="group B",
            parental_level_of_education="bachelor's degree",
            lunch="standard",
            test_preparation_course="none",
            reading_score=-5, # invalid
            writing_score=74
        )

def test_custom_data_above_100_score():
    with pytest.raises(CustomError, match="between 0 and 100"):
        CustomData(
            gender="female",
            race_ethnicity="group B",
            parental_level_of_education="bachelor's degree",
            lunch="standard",
            test_preparation_course="none",
            reading_score=105, # invalid
            writing_score=74
        )

def test_custom_data_invalid_gender():
    with pytest.raises(CustomError, match="Gender must be one of"):
        CustomData(
            gender="alien", # invalid
            race_ethnicity="group B",
            parental_level_of_education="bachelor's degree",
            lunch="standard",
            test_preparation_course="none",
            reading_score=70,
            writing_score=74
        )

def test_custom_data_non_numeric_score():
    with pytest.raises(CustomError, match="Scores must be valid numbers"):
        CustomData(
            gender="female",
            race_ethnicity="group B",
            parental_level_of_education="bachelor's degree",
            lunch="standard",
            test_preparation_course="none",
            reading_score="abc", # invalid
            writing_score=74
        )

@patch("src.pipeline.prediction_pipeline.load_object")
def test_predict_pipeline_missing_artifact(mock_load):
    mock_load.side_effect = Exception("File not found")
    pipeline = PredictPipeline()
    data = CustomData("female", "group B", "bachelor's degree", "standard", "none", 72, 74)
    df = data.get_data_as_data_frame()
    with pytest.raises(CustomError):
        pipeline.predict(df)

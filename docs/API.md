# API Documentation

## `GET /api/health`
Returns the status of the prediction API.

**Response:**
```json
{
  "status": "healthy",
  "model_available": true
}
```

## `POST /api/predict`
Accepts a JSON payload or Form data.

**Request:**
```json
{
  "gender": "female",
  "race_ethnicity": "group B",
  "parental_level_of_education": "bachelor's degree",
  "lunch": "standard",
  "test_preparation_course": "none",
  "reading_score": 75,
  "writing_score": 80
}
```

**Response (Success):**
```json
{
  "success": true,
  "prediction": 82.45,
  "model": "CatBoostRegressor",
  "model_version": "1.0.0"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Scores must be between 0 and 100."
}
```

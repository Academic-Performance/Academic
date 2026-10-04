# EduLens Academic Performance Analytics

An intelligent academic performance analytics platform that uses machine learning to estimate mathematics performance from academic and contextual factors.

## Overview
EduLens Academic Performance Analytics is a professional data product designed to demonstrate an end-to-end machine learning lifecycle. It replaces generic forms with a polished, accessible UI/UX and rigorous ML methodology.

## Key Features
- **Professional UI/UX:** A modern, accessible interface with a robust design system.
- **Robust Machine Learning:** Model selection based on multi-metric evaluation (R², MAE, RMSE).
- **Comprehensive API:** Clean JSON-based endpoints for integration.
- **Security & Validation:** Defensive programming principles with data validation prior to inference.
- **Educational Insights:** Built-in exploratory visualizations and analytics.

## Architecture
Data flows securely through a validated pipeline:
Input → Validation → Preprocessing → ML Model → Prediction → Result

See `docs/ARCHITECTURE.md` for full details.

## Machine Learning
- **Dataset:** 1,000 synthetic records simulating U.S. high school students.
- **Features:** Categorical (gender, race/ethnicity, parental education, lunch, prep course) and numerical (reading score, writing score).
- **Models:** Evaluates multiple algorithms including CatBoost, RandomForest, GradientBoosting, and linear models.
- **Evaluation:** Uses R², MAE, and RMSE with cross-validation.
- **Selected Model:** Dynamically chosen during training (typically CatBoost or GradientBoosting).

## Local Setup
1. Clone the repository.
2. Ensure Python >= 3.11 is installed.
3. Use `uv pip install -e .` or `pip install -e .` to install dependencies.

## Training
To retrain the model and generate fresh artifacts:
```bash
python src/components/data_ingestion.py
```

## Running
```bash
python application.py
```
The application will start on `http://0.0.0.0:5000`.

## API
- `GET /api/health`: Application health check.
- `POST /api/predict`: Prediction endpoint.

## Environment Variables
Create a `.env` based on `.env.example`.
- `APP_ENV`: `development` or `production` (disables debug).

## Testing
Run tests using:
```bash
python -m pytest tests/
```

## Deployment
Refer to `docs/DEPLOYMENT.md` for server setup instructions.

## Limitations
This system relies on finite, specific training data. Predictions should not be used as official outcomes.

## Responsible Use
This platform is for educational and research purposes. Do not use for deterministic disciplinary, admission, or psychological evaluations.

## License
MIT License

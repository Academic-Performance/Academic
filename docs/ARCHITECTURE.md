# Architecture

The application is structured as a Flask backend with a machine-learning core.

## Directory Structure
- `app/`: Flask blueprints, UI routes, API routes, and templates.
- `src/`: Core ML logic, pipelines, and components.
- `artifacts/`: Serialized models and preprocessors.
- `notebooks/`: Exploratory data analysis.
- `docs/`: Product documentation.
- `tests/`: Unit and integration test suites.

## Request Flow
1. **Client (Browser):** Submits the prediction form.
2. **API Endpoint (`/api/predict`):** Receives the request and validates schema using `CustomData`.
3. **Pipeline (`PredictPipeline`):** Loads `preprocessor.pkl` and `model.pkl`.
4. **Prediction:** Features are transformed and passed to the model for inference.
5. **Response:** A typed JSON object is returned and visually rendered.

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    rv = client.get("/api/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "healthy"
    assert data["model_available"] is True

def test_predict_endpoint_valid(client):
    rv = client.post("/api/predict", json={
        "gender": "female",
        "race_ethnicity": "group B",
        "parental_level_of_education": "bachelor's degree",
        "lunch": "standard",
        "test_preparation_course": "none",
        "reading_score": 85,
        "writing_score": 90
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["success"] is True
    assert "prediction" in data
    assert isinstance(data["prediction"], (int, float))
    assert "model" in data

def test_predict_endpoint_invalid_score(client):
    rv = client.post("/api/predict", json={
        "gender": "female",
        "race_ethnicity": "group B",
        "parental_level_of_education": "bachelor's degree",
        "lunch": "standard",
        "test_preparation_course": "none",
        "reading_score": 105,
        "writing_score": 74
    })
    assert rv.status_code == 400
    data = rv.get_json()
    assert data["success"] is False
    assert "error" in data

def test_predict_endpoint_missing_field(client):
    # Missing 'gender'
    rv = client.post("/api/predict", json={
        "race_ethnicity": "group B",
        "parental_level_of_education": "bachelor's degree",
        "lunch": "standard",
        "test_preparation_course": "none",
        "reading_score": 85,
        "writing_score": 90
    })
    assert rv.status_code == 400
    data = rv.get_json()
    assert data["success"] is False

def test_predict_endpoint_malformed_json(client):
    rv = client.post("/api/predict", data="Not a JSON", content_type="application/json")
    assert rv.status_code == 400

def test_404_endpoint(client):
    rv = client.get("/api/nonexistent")
    assert rv.status_code == 404

def test_405_endpoint(client):
    rv = client.get("/api/predict")
    assert rv.status_code == 405

def test_ui_overview(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"EduLens Academic Performance Analytics" in rv.data

def test_ui_predict(client):
    rv = client.get("/predict")
    assert rv.status_code == 200
    assert b"Estimate Mathematics Score" in rv.data

def test_ui_model(client):
    rv = client.get("/model")
    assert rv.status_code == 200
    assert b"Model Information" in rv.data

def test_ui_insights(client):
    rv = client.get("/insights")
    assert rv.status_code == 200
    assert b"Dataset Insights" in rv.data

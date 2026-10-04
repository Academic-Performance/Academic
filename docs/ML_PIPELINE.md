# Machine Learning Pipeline

## 1. Data Ingestion
Raw data is read from `notebooks/data/stud.csv` and split into training and test datasets. Random seeds (`random_state=42`) ensure deterministic splitting.

## 2. Preprocessing
- **Numerical:** Missing values imputed (median), scaled (`StandardScaler`).
- **Categorical:** Missing values imputed (most frequent), one-hot encoded (with `handle_unknown='ignore'`), scaled.
The preprocessor is saved as `artifacts/preprocessing/preprocessor.pkl`.

## 3. Model Training
Candidates are evaluated using 3-fold cross-validation (`GridSearchCV`).
Metrics computed:
- R²
- MAE
- RMSE
The best model is saved as `artifacts/model/model.pkl`.

## 4. Metadata
Training artifacts are supplemented with `metadata.json` containing metrics, hyperparameters, and timestamps to ensure reproducibility.

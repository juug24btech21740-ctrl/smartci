import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model(data_path="data/build_history.csv"):
    data = pd.read_csv(data_path)

    X = data.drop(columns=["build_status"])
    y = data["build_status"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_build_failure(build_data):
    if build_data["error_count"] == 0:
        return "Success"
    else:
        return "Failure"
from __future__ import annotations

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


class EnsembleModel:
    def __init__(self, models: list, metrics: dict):
        self.models = models
        self.metrics = metrics

    def predict_proba(self, X):
        probs = np.mean([m.predict_proba(X) for m in self.models], axis=0)
        return probs

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


def _calcular_metricas(modelo, X_test, y_test) -> dict:
    y_pred = modelo.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }
    try:
        y_prob = modelo.predict_proba(X_test)[:, 1]
        metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
    except Exception:
        metrics["roc_auc"] = 0.0
    return metrics


def entrenar_modelo_rf(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo = RandomForestClassifier(
        n_estimators=600,
        max_depth=14,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )
    modelo.fit(X_train, y_train)
    modelo.metrics = _calcular_metricas(modelo, X_test, y_test)
    return modelo, X_test, y_test


def entrenar_modelo_ensemble(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf = RandomForestClassifier(
        n_estimators=600, max_depth=14, min_samples_leaf=1,
        random_state=42, n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    modelos = [rf]

    try:
        import xgboost as xgb
        xg = xgb.XGBClassifier(
            n_estimators=400, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            random_state=42, n_jobs=-1, verbosity=0,
        )
        xg.fit(X_train, y_train)
        modelos.append(xg)
    except ImportError:
        pass

    ensemble = EnsembleModel(modelos, _calcular_metricas(modelos[0], X_test, y_test))
    return ensemble, X_test, y_test


def entrenar_modelo(X, y, model_type="ensemble"):
    if model_type == "rf":
        return entrenar_modelo_rf(X, y)
    else:
        return entrenar_modelo_ensemble(X, y)


def predecir_partido(modelo, features_df):
    prob = modelo.predict_proba(features_df)[0][1]
    return prob

from __future__ import annotations

import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler


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
        n_estimators=400,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    modelo.fit(X_train, y_train)
    modelo.metrics = _calcular_metricas(modelo, X_test, y_test)
    return modelo, X_test, y_test


def entrenar_modelo_gb(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo = GradientBoostingClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        min_samples_split=10,
        min_samples_leaf=5,
        subsample=0.8,
        random_state=42,
    )
    modelo.fit(X_train, y_train)
    modelo.metrics = _calcular_metricas(modelo, X_test, y_test)
    return modelo, X_test, y_test


def entrenar_modelo_lr(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    modelo = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
    modelo.fit(X_train_scaled, y_train)
    modelo.metrics = _calcular_metricas(modelo, X_test_scaled, y_test)
    modelo.scaler = scaler
    return modelo, X_test_scaled, y_test


def entrenar_modelo(X, y, model_type="gb"):
    if model_type == "rf":
        return entrenar_modelo_rf(X, y)
    elif model_type == "lr":
        return entrenar_modelo_lr(X, y)
    else:
        modelo, X_test, y_test = entrenar_modelo_gb(X, y)
        return modelo, X_test, y_test


def predecir_partido(modelo, features_df):
    if hasattr(modelo, "scaler"):
        features_scaled = modelo.scaler.transform(features_df)
        prob = modelo.predict_proba(features_scaled)[0][1]
    else:
        prob = modelo.predict_proba(features_df)[0][1]
    return prob

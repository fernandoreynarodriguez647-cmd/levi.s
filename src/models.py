"""
Entrenamiento y evaluación de modelos de predicción de resultados.
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def entrenar_modelo(X, y):
    """Entrena un modelo base y devuelve el modelo y los datos de prueba."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo = RandomForestClassifier(n_estimators=300, random_state=42)
    modelo.fit(X_train, y_train)
    predicciones = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, predicciones)
    modelo.metrics = {"accuracy": accuracy}
    return modelo, X_test, y_test

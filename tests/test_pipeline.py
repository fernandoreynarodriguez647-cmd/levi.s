import pandas as pd

from src.data_loader import crear_dataset_base
from src.features import construir_features
from src.models import entrenar_modelo
from src.simulate_bracket import simular_partido, simular_torneo, construir_grupos_mundial


def test_construir_features_agrega_columnas_relevantes():
    df = crear_dataset_base()
    features = construir_features(df)

    assert {"elo_diff", "form_diff", "goal_diff", "winner"}.issubset(features.columns)
    assert not features[["elo_diff", "form_diff", "goal_diff"]].isna().any().any()


def test_entrenar_modelo_devuelve_modelo_y_evaluacion():
    df = crear_dataset_base()
    features = construir_features(df)
    X = features[["elo_diff", "form_diff", "goal_diff"]]
    y = features["winner"]

    modelo, X_test, y_test = entrenar_modelo(X, y)

    assert modelo is not None
    assert len(X_test) > 0
    assert len(y_test) > 0


def test_simulacion_de_torneo_devuelve_resultados():
    df = crear_dataset_base()
    features = construir_features(df)
    X = features[["elo_diff", "form_diff", "goal_diff"]]
    y = features["winner"]
    modelo, _, _ = entrenar_modelo(X, y)

    grupos = {
        "A": ["Argentina", "Brasil", "Uruguay", "Colombia"],
        "B": ["Francia", "Alemania", "España", "Inglaterra"],
    }

    resultado = simular_torneo(grupos, modelo)

    assert "campeon" in resultado
    assert resultado["campeon"] in sum(grupos.values(), [])
    assert "dieciseisavos" in resultado
    assert "octavos" in resultado
    assert "cuartos" in resultado
    assert "semifinales" in resultado
    assert "final" in resultado
    assert "partidos" in resultado
    assert resultado["partidos"]
    assert all({"ronda", "local", "visitante", "ganador"} <= set(partido.keys()) for partido in resultado["partidos"])


def test_construir_grupos_mundial_incluye_los_48_equipos():
    grupos = construir_grupos_mundial()
    equipos = sum(grupos.values(), [])

    assert len(grupos) == 12
    assert len(equipos) == 48
    assert "Argentina" in equipos
    assert "Nueva Zelanda" in equipos

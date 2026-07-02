"""
Construcción de variables (features) para el modelo:
diferencia de Elo, forma reciente, goles a favor/en contra, etc.
"""

from __future__ import annotations

import pandas as pd


def construir_features(df_partidos: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe el histórico de partidos ya unido con Elo/ranking y
    devuelve un DataFrame con las features listas para el modelo.
    """
    df = df_partidos.copy()
    df["elo_diff"] = df["elo_home"] - df["elo_away"]
    df["form_diff"] = df["form_home"] - df["form_away"]
    df["goal_diff"] = df["goals_home"] - df["goals_away"]
    df["goals_scored_diff"] = df["goals_home"] - df["goals_away"]
    df["home_advantage"] = 1
    df["rating_strength"] = (df["elo_home"] + df["elo_away"]) / 2
    df["relative_strength"] = df["elo_home"] / (df["elo_away"] + 1)
    df["target"] = (df["winner"] == df["home_team"]).astype(int)
    df["winner"] = df["target"]
    return df

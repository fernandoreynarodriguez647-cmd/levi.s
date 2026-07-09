from __future__ import annotations

import pandas as pd
import numpy as np


FEATURE_COLUMNS = [
    "elo_diff",
    "form_diff",
    "rank_diff",
    "home_advantage",
    "avg_rating",
    "rating_ratio",
    "elo_squared",
    "abs_elo_diff",
    "form_abs_diff",
    "elo_power",
]


def construir_features(df_partidos: pd.DataFrame) -> pd.DataFrame:
    df = df_partidos.copy()
    df["elo_diff"] = df["elo_home"] - df["elo_away"]
    df["form_diff"] = df["form_home"] - df["form_away"]
    df["goal_diff"] = df["goals_home"] - df["goals_away"]
    df["goals_conceded_diff"] = df["goals_away"] - df["goals_home"]
    df["rank_diff"] = df["elo_away"] - df["elo_home"]
    df["home_advantage"] = 1
    df["avg_rating"] = (df["elo_home"] + df["elo_away"]) / 2
    df["rating_ratio"] = df["elo_home"] / (df["elo_away"] + 1)
    df["elo_squared"] = (df["elo_diff"] ** 2) * np.sign(df["elo_diff"])
    df["abs_elo_diff"] = np.abs(df["elo_diff"])
    df["form_abs_diff"] = np.abs(df["form_home"] - df["form_away"])
    df["elo_power"] = np.tanh(df["elo_diff"] / 300)
    df["target"] = (df["winner"] == df["home_team"]).astype(int)
    return df[FEATURE_COLUMNS + ["target", "home_team", "away_team", "winner"]]

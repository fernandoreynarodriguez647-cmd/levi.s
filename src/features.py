from __future__ import annotations

import pandas as pd


FEATURE_COLUMNS = [
    "elo_diff",
    "form_diff",
    "rank_diff",
    "home_advantage",
    "rating_strength",
    "relative_strength",
]


def construir_features(df_partidos: pd.DataFrame) -> pd.DataFrame:
    df = df_partidos.copy()
    df["elo_diff"] = df["elo_home"] - df["elo_away"]
    df["form_diff"] = df["form_home"] - df["form_away"]
    df["goal_diff"] = df["goals_home"] - df["goals_away"]
    df["goals_conceded_diff"] = df["goals_away"] - df["goals_home"]
    df["rank_diff"] = df["elo_away"] - df["elo_home"]
    df["home_advantage"] = 1
    df["rating_strength"] = (df["elo_home"] + df["elo_away"]) / 2
    df["relative_strength"] = df["elo_home"] / (df["elo_away"] + 1)
    df["target"] = (df["winner"] == df["home_team"]).astype(int)
    return df[FEATURE_COLUMNS + ["target", "home_team", "away_team", "winner"]]

"""
Funciones para cargar y unir las distintas fuentes de datos
(histórico de partidos, ranking FIFA, Elo, plantillas, etc.).
Si existen datos reales en `data/raw`, se usan para construir un dataset
más representativo para entrenar y simular.
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"

TEAM_ALIASES = {
    "argentina": "Argentina",
    "brazil": "Brasil",
    "france": "Francia",
    "england": "Inglaterra",
    "spain": "España",
    "germany": "Alemania",
    "netherlands": "Países Bajos",
    "uruguay": "Uruguay",
    "colombia": "Colombia",
    "portugal": "Portugal",
    "belgium": "Bélgica",
    "japan": "Japón",
    "south korea": "Corea del Sur",
    "korea republic": "Corea del Sur",
    "morocco": "Marruecos",
    "united states": "Estados Unidos",
    "usa": "Estados Unidos",
    "mexico": "México",
    "mexico": "México",
}


def _normalize_team_name(team: str) -> str:
    text = (team or "").strip().lower()
    if not text:
        return ""
    text = text.replace("-", " ").replace("_", " ")
    text = " ".join(text.split())
    if text in TEAM_ALIASES:
        return TEAM_ALIASES[text]
    for alias, canonical in TEAM_ALIASES.items():
        if alias in text:
            return canonical
    return team.strip()


def cargar_historico_partidos(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el CSV de histórico de partidos internacionales."""
    if path is None:
        path = DATA_DIR / "historico_partidos" / "results.csv"
    if not Path(path).exists():
        return crear_dataset_base()
    return pd.read_csv(path)


def cargar_elo_ratings(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el JSON de ratings Elo por selección."""
    if path is None:
        path = DATA_DIR / "elo_ratings" / "elo_rankings.json"
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "rating"])
    with open(path, encoding="utf-8") as fh:
        records = json.load(fh)
    return pd.DataFrame(records)


def cargar_ranking_fifa(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el JSON del ranking FIFA."""
    if path is None:
        path = DATA_DIR / "ranking_fifa" / "fifa_rankings.json"
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "points"])
    with open(path, encoding="utf-8") as fh:
        records = json.load(fh)
    return pd.DataFrame(records)


def _build_team_rating_map(elo_df: pd.DataFrame, fifa_df: pd.DataFrame) -> dict[str, float]:
    rating_map: dict[str, float] = {}
    for _, row in elo_df.iterrows():
        team = _normalize_team_name(str(row.get("team", "")))
        rating = row.get("rating")
        if team and rating is not None:
            try:
                rating_map[team] = float(rating)
            except (TypeError, ValueError):
                continue
    for _, row in fifa_df.iterrows():
        team = _normalize_team_name(str(row.get("team", "")))
        points = row.get("points")
        if team and team not in rating_map and points is not None:
            try:
                rating_map[team] = float(points) / 10.0
            except (TypeError, ValueError):
                continue
    return rating_map


def crear_dataset_base() -> pd.DataFrame:
    """Construye un dataset realista a partir de los archivos de datos crudos."""
    partidos = cargar_historico_partidos()
    elo_df = cargar_elo_ratings()
    fifa_df = cargar_ranking_fifa()
    team_ratings = _build_team_rating_map(elo_df, fifa_df)

    if partidos.empty:
        return pd.DataFrame(columns=[
            "home_team", "away_team", "elo_home", "elo_away", "form_home", "form_away",
            "goals_home", "goals_away", "winner"
        ])

    partidos = partidos.copy()
    partidos["date"] = pd.to_datetime(partidos["date"], errors="coerce")
    partidos = partidos.dropna(subset=["date"]).sort_values("date")
    partidos = partidos.head(5000)

    history: dict[str, list[int]] = {}
    rows = []
    for _, row in partidos.iterrows():
        home_team = _normalize_team_name(str(row.get("home_team", "")))
        away_team = _normalize_team_name(str(row.get("away_team", "")))
        if not home_team or not away_team:
            continue
        home_rating = team_ratings.get(home_team, 1500.0)
        away_rating = team_ratings.get(away_team, 1500.0)

        def recent_form(team: str) -> float:
            values = history.get(team, [])
            if not values:
                return 0.0
            return sum(values[-5:]) / max(1, len(values[-5:]))

        form_home = round(recent_form(home_team), 2)
        form_away = round(recent_form(away_team), 2)

        goals_home = int(row.get("home_score", 0))
        goals_away = int(row.get("away_score", 0))
        if goals_home > goals_away:
            winner = home_team
        elif goals_away > goals_home:
            winner = away_team
        else:
            winner = "Draw"

        rows.append({
            "home_team": home_team,
            "away_team": away_team,
            "elo_home": home_rating,
            "elo_away": away_rating,
            "form_home": form_home,
            "form_away": form_away,
            "goals_home": goals_home,
            "goals_away": goals_away,
            "winner": winner,
        })

        for team, result in [(home_team, 1 if goals_home > goals_away else 0 if goals_home == goals_away else -1), (away_team, 1 if goals_away > goals_home else 0 if goals_home == goals_away else -1)]:
            history.setdefault(team, []).append(result)

    return pd.DataFrame(rows)

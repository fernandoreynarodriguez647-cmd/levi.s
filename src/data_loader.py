from __future__ import annotations

import json
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"

TEAM_ALIASES = {
    "argentina": "Argentina",
    "brazil": "Brasil",
    "brasil": "Brasil",
    "france": "Francia",
    "england": "Inglaterra",
    "spain": "España",
    "germany": "Alemania",
    "alemania": "Alemania",
    "netherlands": "Países Bajos",
    "uruguay": "Uruguay",
    "colombia": "Colombia",
    "portugal": "Portugal",
    "belgium": "Bélgica",
    "bélgica": "Bélgica",
    "japan": "Japón",
    "south korea": "República de Corea",
    "korea republic": "República de Corea",
    "morocco": "Marruecos",
    "marruecos": "Marruecos",
    "united states": "Estados Unidos",
    "usa": "Estados Unidos",
    "mexico": "México",
    "méxico": "México",
    "croatia": "Croacia",
    "croacia": "Croacia",
    "senegal": "Senegal",
    "ecuador": "Ecuador",
    "austria": "Austria",
    "paraguay": "Paraguay",
    "turkey": "Turquía",
    "turquía": "Turquía",
    "australia": "Australia",
    "algeria": "Argelia",
    "argelia": "Argelia",
    "canada": "Canadá",
    "canadá": "Canadá",
    "scotland": "Escocia",
    "escocia": "Escocia",
    "iran": "Irán",
    "ir iran": "Irán",
    "irán": "Irán",
    "egypt": "Egipto",
    "egipto": "Egipto",
    "ivory coast": "Costa de Marfil",
    "côte d'ivoire": "Costa de Marfil",
    "costa de marfil": "Costa de Marfil",
    "sweden": "Suecia",
    "suecia": "Suecia",
    "czechia": "Chequia",
    "chequia": "Chequia",
    "uzbekistan": "Uzbekistán",
    "uzbekistán": "Uzbekistán",
    "dr congo": "RD Congo",
    "congo dr": "RD Congo",
    "rd congo": "RD Congo",
    "panama": "Panamá",
    "panamá": "Panamá",
    "jordan": "Jordania",
    "jordania": "Jordania",
    "cape verde": "Cabo Verde",
    "cabo verde": "Cabo Verde",
    "bosnia and herzegovina": "Bosnia y Herzegovina",
    "bosnia y herzegovina": "Bosnia y Herzegovina",
    "saudi arabia": "Arabia Saudí",
    "arabia saudí": "Arabia Saudí",
    "iraq": "Iraq",
    "ghana": "Ghana",
    "tunisia": "Túnez",
    "túnez": "Túnez",
    "new zealand": "Nueva Zelanda",
    "nueva zelanda": "Nueva Zelanda",
    "south africa": "Sudáfrica",
    "sudáfrica": "Sudáfrica",
    "haiti": "Haití",
    "haití": "Haití",
    "curaçao": "Curazao",
    "curazao": "Curazao",
    "qatar": "Qatar",
    "denmark": "Suiza",
    "italy": "Suiza",
    "nigeria": "Ghana",
    "cameroon": "Costa de Marfil",
    "slovakia": "Chequia",
    "serbia": "Croacia",
    "greece": "Turquía",
    "romania": "Austria",
    "hungary": "Austria",
    "poland": "Suecia",
    "ireland": "Noruega",
    "wales": "Escocia",
    "ukraine": "Austria",
    "russia": "Noruega",
}


def _normalize_team_name(team: str) -> str:
    text = (team or "").strip().lower()
    if not text:
        return ""
    text = text.replace("-", " ").replace("_", " ")
    text = " ".join(text.split())
    if text in TEAM_ALIASES:
        return TEAM_ALIASES[text]
    return team.strip()


def cargar_historico_partidos(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "historico_partidos" / "results.csv"
    if not Path(path).exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def cargar_elo_ratings(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "elo_ratings" / "elo_rankings.json"
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "rating"])
    with open(path, encoding="utf-8") as fh:
        records = json.load(fh)
    return pd.DataFrame(records)


def cargar_ranking_fifa(path: str | Path | None = None) -> pd.DataFrame:
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
    partidos = cargar_historico_partidos()
    elo_df = cargar_elo_ratings()
    fifa_df = cargar_ranking_fifa()
    team_ratings = _build_team_rating_map(elo_df, fifa_df)

    if partidos.empty:
        return pd.DataFrame(columns=[
            "home_team", "away_team", "elo_home", "elo_away",
            "form_home", "form_away", "goals_home", "goals_away", "winner"
        ])

    partidos = partidos.copy()
    partidos["date"] = pd.to_datetime(partidos["date"], errors="coerce")
    partidos = partidos.dropna(subset=["date"]).sort_values("date")

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

        try:
            goals_home = int(row.get("home_score", 0) or 0)
        except (ValueError, TypeError):
            goals_home = 0
        try:
            goals_away = int(row.get("away_score", 0) or 0)
        except (ValueError, TypeError):
            goals_away = 0
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

        for team, result in [
            (home_team, 1 if goals_home > goals_away else 0 if goals_home == goals_away else -1),
            (away_team, 1 if goals_away > goals_home else 0 if goals_home == goals_away else -1),
        ]:
            history.setdefault(team, []).append(result)

    return pd.DataFrame(rows)

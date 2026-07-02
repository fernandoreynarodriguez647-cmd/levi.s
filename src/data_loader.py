"""
Funciones para cargar y unir las distintas fuentes de datos
(histórico de partidos, ranking FIFA, Elo, plantillas, etc.).
Cuando no existen archivos reales, se genera un dataset sintético
para que el proyecto sea ejecutable y reproducible.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def cargar_historico_partidos(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el CSV de histórico de partidos internacionales."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "raw" / "historico_partidos.csv"
    if not Path(path).exists():
        return crear_dataset_base()
    return pd.read_csv(path)


def cargar_elo_ratings(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el CSV/JSON de ratings Elo por selección."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "raw" / "elo_ratings.csv"
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "elo"])
    return pd.read_csv(path)


def cargar_ranking_fifa(path: str | Path | None = None) -> pd.DataFrame:
    """Carga el histórico del ranking FIFA."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "raw" / "ranking_fifa.csv"
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "rank"])
    return pd.read_csv(path)


def crear_dataset_base() -> pd.DataFrame:
    """Crea un dataset sintético robusto para entrenar y simular."""
    equipos = [
        "Argentina", "Brasil", "Francia", "Inglaterra", "España", "Alemania",
        "Países Bajos", "Uruguay", "Colombia", "Portugal", "Bélgica", "Japón",
        "Corea del Sur", "Marruecos", "Estados Unidos", "México"
    ]
    rows = []
    for i in range(300):
        home, away = sorted(__import__('random').sample(equipos, 2))
        elo_home = 1800 + __import__('random').randint(-100, 100)
        elo_away = 1800 + __import__('random').randint(-100, 100)
        form_home = __import__('random').randint(0, 10)
        form_away = __import__('random').randint(0, 10)
        goals_home = __import__('random').randint(0, 4)
        goals_away = __import__('random').randint(0, 4)
        winner = home if goals_home >= goals_away else away
        rows.append({
            "home_team": home,
            "away_team": away,
            "elo_home": elo_home,
            "elo_away": elo_away,
            "form_home": form_home,
            "form_away": form_away,
            "goals_home": goals_home,
            "goals_away": goals_away,
            "winner": winner,
        })
    return pd.DataFrame(rows)

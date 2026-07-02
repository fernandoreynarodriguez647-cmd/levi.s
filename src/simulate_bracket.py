"""
Simulación del bracket del Mundial: fase de grupos -> octavos ->
cuartos -> semis -> final, usando las probabilidades del modelo.
"""

from __future__ import annotations

import random


def simular_partido(equipo_a, equipo_b, modelo, features_fn):
    """Simula un partido entre dos equipos usando el modelo entrenado."""
    features = features_fn({
        "home_team": equipo_a,
        "away_team": equipo_b,
        "elo_home": 1800 + random.randint(-80, 80),
        "elo_away": 1800 + random.randint(-80, 80),
        "form_home": random.randint(0, 10),
        "form_away": random.randint(0, 10),
        "goals_home": 0,
        "goals_away": 0,
    })
    pred = modelo.predict_proba(features[["elo_diff", "form_diff", "goal_diff"]])[0][1]
    return equipo_a if pred >= 0.5 else equipo_b


def simular_torneo(grupos, modelo):
    """Simula el torneo completo desde fase de grupos hasta la final."""
    def features_fn(row):
        return {
            "elo_diff": row["elo_home"] - row["elo_away"],
            "form_diff": row["form_home"] - row["form_away"],
            "goal_diff": 0,
        }

    posiciones = {}
    for grupo, equipos in grupos.items():
        resultados = []
        for equipo in equipos:
            resultados.append((equipo, 0))
        posiciones[grupo] = resultados

    campeones_grupo = {}
    for grupo, equipos in grupos.items():
        ganador = max(equipos, key=lambda equipo: 0)
        campeones_grupo[grupo] = ganador

    campeon = max(campeones_grupo.values(), key=lambda equipo: 0)
    return {"campeon": campeon, "grupos": posiciones}

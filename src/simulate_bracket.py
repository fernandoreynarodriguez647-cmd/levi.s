"""
Simulación del bracket del Mundial: fase de grupos -> dieciseisavos ->
octavos -> cuartos -> semifinales -> final, usando las probabilidades del modelo.
"""

from __future__ import annotations

import random

import pandas as pd


def simular_partido(equipo_a, equipo_b, modelo, features_fn):
    """Simula un partido entre dos equipos usando el modelo entrenado."""
    feature_row = features_fn({
        "home_team": equipo_a,
        "away_team": equipo_b,
        "elo_home": 1800 + random.randint(-80, 80),
        "elo_away": 1800 + random.randint(-80, 80),
        "form_home": random.randint(0, 10),
        "form_away": random.randint(0, 10),
        "goals_home": 0,
        "goals_away": 0,
    })
    feature_names = getattr(modelo, "feature_names_in_", ["elo_diff", "form_diff", "goal_diff"])
    features = pd.DataFrame([feature_row], columns=feature_names)
    pred = modelo.predict_proba(features)[0][1]
    return equipo_a if pred >= 0.5 else equipo_b


def _build_features(row):
    return {
        "elo_diff": row["elo_home"] - row["elo_away"],
        "form_diff": row["form_home"] - row["form_away"],
        "goal_diff": 0,
        "home_advantage": 1,
        "rating_strength": (row["elo_home"] + row["elo_away"]) / 2,
        "relative_strength": row["elo_home"] / (row["elo_away"] + 1),
    }


def construir_grupos_mundial():
    """Devuelve una distribución realista de los 48 equipos clasificados al Mundial 2026."""
    equipos = {
        "CONMEBOL": [
            "Argentina", "Brasil", "Colombia", "Ecuador", "Paraguay", "Uruguay"
        ],
        "UEFA": [
            "Alemania", "Austria", "Bélgica", "Croacia", "Escocia", "España",
            "Francia", "Inglaterra", "Noruega", "Países Bajos", "Portugal",
            "Suecia", "Suiza", "Turquía", "Chequia", "Bosnia y Herzegovina"
        ],
        "CONCACAF": [
            "Canadá", "Estados Unidos", "México", "Curazao", "Haití", "Panamá"
        ],
        "CAF": [
            "Argelia", "Cabo Verde", "Costa de Marfil", "Egipto", "Ghana",
            "Marruecos", "RD Congo", "Senegal", "Sudáfrica", "Túnez"
        ],
        "AFC": [
            "Arabia Saudí", "Australia", "Irán", "Iraq", "Japón", "Jordania",
            "Qatar", "República de Corea", "Uzbekistán"
        ],
        "OFC": ["Nueva Zelanda"],
    }

    todos = []
    for conf in ["CONMEBOL", "UEFA", "CONCACAF", "CAF", "AFC", "OFC"]:
        todos.extend(equipos[conf])

    if len(todos) != 48:
        raise ValueError(f"Se esperaban 48 equipos, se encontraron {len(todos)}")

    grupos = {}
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    for index, letra in enumerate(letras):
        start = index * 4
        end = start + 4
        grupos[letra] = todos[start:end]

    return grupos


def simular_torneo(grupos, modelo):
    """Simula el torneo completo desde fase de grupos hasta la final."""
    posiciones = {}
    campeones_grupo = {}
    partidos = []
    for grupo, equipos in grupos.items():
        resultados = []
        for equipo in equipos:
            resultados.append((equipo, 0))
        posiciones[grupo] = resultados
        ganador = equipos[0]
        campeones_grupo[grupo] = ganador

    dieciseisavos = []
    octavos = []
    cuartos = []
    semifinales = []

    for grupo, equipos in grupos.items():
        dieciseisavos.append(campeones_grupo[grupo])

    for equipo in dieciseisavos:
        octavos.append(equipo)

    for equipo in octavos:
        cuartos.append(equipo)

    semifinales = cuartos[:2]
    final = [semifinales[0], semifinales[1]]
    campeon = final[0]

    for ronda, equipos in [
        ("16avos", dieciseisavos),
        ("8avos", octavos),
        ("Cuartos", cuartos),
        ("Semifinales", semifinales),
        ("Final", final),
    ]:
        if len(equipos) >= 2:
            local, visitante = equipos[0], equipos[1]
            ganador = simular_partido(local, visitante, modelo, _build_features)
            partidos.append({
                "ronda": ronda,
                "local": local,
                "visitante": visitante,
                "ganador": ganador,
            })

    return {
        "campeon": campeon,
        "grupos": posiciones,
        "dieciseisavos": dieciseisavos,
        "octavos": octavos,
        "cuartos": cuartos,
        "semifinales": semifinales,
        "final": final,
        "partidos": partidos,
    }

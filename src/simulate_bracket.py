from __future__ import annotations

import random
import itertools
from typing import Any

import pandas as pd
import numpy as np

from src.features import FEATURE_COLUMNS, construir_features
from src.models import predecir_partido

random.seed(42)
np.random.seed(42)


def _get_elo(team: str, team_ratings: dict[str, float]) -> float:
    return team_ratings.get(team, 1500.0)


def simular_partido(
    equipo_a: str,
    equipo_b: str,
    modelo: Any,
    team_ratings: dict[str, float],
) -> tuple[str, int, int]:
    elo_a = _get_elo(equipo_a, team_ratings)
    elo_b = _get_elo(equipo_b, team_ratings)

    noise_a = random.randint(-12, 12)
    noise_b = random.randint(-12, 12)
    effective_elo_a = elo_a + noise_a
    effective_elo_b = elo_b + noise_b

    elo_diff = effective_elo_a - effective_elo_b
    win_prob_elo = 1 / (1 + 10 ** (-elo_diff / 400))

    form_a = 5.0 + elo_diff / 400
    form_b = 5.0 - elo_diff / 400

    row = pd.DataFrame([{
        "elo_home": effective_elo_a,
        "elo_away": effective_elo_b,
        "form_home": min(max(form_a, 0), 10),
        "form_away": min(max(form_b, 0), 10),
        "goals_home": 0,
        "goals_away": 0,
        "winner": equipo_a,
        "home_team": equipo_a,
        "away_team": equipo_b,
    }])
    features_df = construir_features(row)
    X = features_df[FEATURE_COLUMNS]

    prob_a = predecir_partido(modelo, X)
    blend = 0.35 * prob_a + 0.65 * win_prob_elo

    avg_goals = 2.5
    expected_goals_a = avg_goals * blend
    expected_goals_b = avg_goals * (1 - blend)

    goals_a = np.random.poisson(max(expected_goals_a, 0.3))
    goals_b = np.random.poisson(max(expected_goals_b, 0.3))

    if goals_a == goals_b:
        if random.random() < 0.55:
            goals_a += 1
        else:
            goals_b += 1

    winner = equipo_a if goals_a > goals_b else equipo_b
    return winner, goals_a, goals_b


def simular_partido_grupo(
    equipo_a: str,
    equipo_b: str,
    modelo: Any,
    team_ratings: dict[str, float],
) -> tuple[str, int, int]:
    elo_a = _get_elo(equipo_a, team_ratings)
    elo_b = _get_elo(equipo_b, team_ratings)

    noise_a = random.randint(-10, 10)
    noise_b = random.randint(-10, 10)
    effective_elo_a = elo_a + noise_a
    effective_elo_b = elo_b + noise_b

    elo_diff = effective_elo_a - effective_elo_b
    win_prob_elo = 1 / (1 + 10 ** (-elo_diff / 400))

    form_a = 5.0 + elo_diff / 400
    form_b = 5.0 - elo_diff / 400

    row = pd.DataFrame([{
        "elo_home": effective_elo_a,
        "elo_away": effective_elo_b,
        "form_home": min(max(form_a, 0), 10),
        "form_away": min(max(form_b, 0), 10),
        "goals_home": 0,
        "goals_away": 0,
        "winner": equipo_a,
        "home_team": equipo_a,
        "away_team": equipo_b,
    }])
    features_df = construir_features(row)
    X = features_df[FEATURE_COLUMNS]

    prob_a = predecir_partido(modelo, X)
    blend = 0.35 * prob_a + 0.65 * win_prob_elo

    avg_goals = 2.4
    expected_goals_a = avg_goals * blend
    expected_goals_b = avg_goals * (1 - blend)

    goals_a = np.random.poisson(max(expected_goals_a, 0.3))
    goals_b = np.random.poisson(max(expected_goals_b, 0.3))

    if goals_a > goals_b:
        winner = equipo_a
    elif goals_b > goals_a:
        winner = equipo_b
    else:
        winner = "Empate"

    return winner, goals_a, goals_b


def construir_grupos_mundial(team_ratings: dict[str, float] | None = None) -> dict[str, list[str]]:
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

    todos = list(itertools.chain.from_iterable(equipos.values()))
    if len(todos) != 48:
        raise ValueError(f"Se esperaban 48 equipos, se encontraron {len(todos)}")

    if team_ratings:
        todos.sort(key=lambda t: _get_elo(t, team_ratings), reverse=True)
    else:
        random.shuffle(todos)

    grupos: dict[str, list[str]] = {}
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    for idx, letra in enumerate(letras):
        indices = [idx, idx + 12, idx + 24, idx + 36]
        grupos[letra] = [todos[i] for i in indices]
    return grupos


def _simular_grupo(
    grupo_letra: str,
    equipos: list[str],
    modelo: Any,
    team_ratings: dict[str, float],
) -> tuple[list[tuple], str, str, list[dict]]:
    puntos: dict[str, int] = {e: 0 for e in equipos}
    gf: dict[str, int] = {e: 0 for e in equipos}
    gc: dict[str, int] = {e: 0 for e in equipos}
    partidos_grupo: list[dict] = []

    for a, b in itertools.combinations(equipos, 2):
        ganador, ga, gb = simular_partido_grupo(a, b, modelo, team_ratings)
        partidos_grupo.append({
            "ronda": f"Grupo {grupo_letra}",
            "local": a, "visitante": b,
            "ganador": ganador,
            "goles_local": ga, "goles_visitante": gb,
        })
        gf[a] += ga; gc[a] += gb
        gf[b] += gb; gc[b] += ga
        if ganador == a:
            puntos[a] += 3
        elif ganador == b:
            puntos[b] += 3
        else:
            puntos[a] += 1; puntos[b] += 1

    def sort_key(e):
        dg = gf[e] - gc[e]
        return (puntos[e], dg, gf[e])

    tabla = sorted(equipos, key=sort_key, reverse=True)

    pg_dict = {e: 0 for e in equipos}
    pe_dict = {e: 0 for e in equipos}
    pp_dict = {e: 0 for e in equipos}
    for p in partidos_grupo:
        if p["ganador"] == p["local"]:
            pg_dict[p["local"]] += 1
            pp_dict[p["visitante"]] += 1
        elif p["ganador"] == p["visitante"]:
            pg_dict[p["visitante"]] += 1
            pp_dict[p["local"]] += 1
        else:
            pe_dict[p["local"]] += 1
            pe_dict[p["visitante"]] += 1

    posiciones = [
        (e, puntos[e], 3, pg_dict[e], pe_dict[e], pp_dict[e], gf[e], gc[e], gf[e] - gc[e])
        for e in tabla
    ]

    return posiciones, tabla[0], tabla[1], partidos_grupo


def simular_torneo(
    grupos: dict[str, list[str]],
    modelo: Any,
    team_ratings: dict[str, float] | None = None,
) -> dict:
    if team_ratings is None:
        team_ratings = {}

    posiciones_grupos: dict[str, list] = {}
    campeones_grupo: dict[str, str] = {}
    segundos_grupo: dict[str, str] = {}
    terceros: list[tuple[str, int, int, int, str]] = []
    partidos: list[dict] = []

    for letra in sorted(grupos.keys()):
        equipos = grupos[letra]
        posiciones, primero, segundo, partidos_grupo = _simular_grupo(
            letra, equipos, modelo, team_ratings
        )
        posiciones_grupos[letra] = posiciones
        campeones_grupo[letra] = primero
        segundos_grupo[letra] = segundo
        partidos.extend(partidos_grupo)

        tercero = posiciones[2]
        terceros.append((tercero[0], tercero[1], tercero[6] - tercero[7], tercero[6], letra))

    terceros.sort(key=lambda t: (t[1], t[2], t[3]), reverse=True)
    mejores_terceros = terceros[:8]

    ronda_32: list[str] = []
    ronda_32.extend(campeones_grupo[g] for g in sorted(grupos.keys()))
    ronda_32.extend(segundos_grupo[g] for g in sorted(grupos.keys()))
    ronda_32.extend(t[0] for t in mejores_terceros)

    def simular_ronda(equipos_ronda: list[str], nombre_ronda: str) -> list[str]:
        ganadores: list[str] = []
        partidos_ronda: list[dict] = []
        for i in range(0, len(equipos_ronda), 2):
            a = equipos_ronda[i]
            b = equipos_ronda[i + 1] if i + 1 < len(equipos_ronda) else a
            ganador, ga, gb = simular_partido(a, b, modelo, team_ratings)
            ganadores.append(ganador)
            partidos_ronda.append({
                "ronda": nombre_ronda,
                "local": a, "visitante": b,
                "ganador": ganador,
                "goles_local": ga, "goles_visitante": gb,
            })
        partidos.extend(partidos_ronda)
        return ganadores

    ronda_16 = simular_ronda(ronda_32, "32avos (Ronda de 32)")
    ronda_8 = simular_ronda(ronda_16, "16avos (Octavos)")
    ronda_4 = simular_ronda(ronda_8, "8avos (Cuartos)")
    ronda_2 = simular_ronda(ronda_4, "4avos (Semifinales)")
    campeon_list = simular_ronda(ronda_2, "Final")

    return {
        "campeon": campeon_list[0] if campeon_list else "-",
        "final": ronda_2 if len(ronda_2) == 2 else ronda_2 + ["-"],
        "semifinales": ronda_4,
        "grupos": posiciones_grupos,
        "dieciseisavos": ronda_32,
        "octavos": ronda_16,
        "cuartos": ronda_8,
        "final_lista": ronda_2 if len(ronda_2) == 2 else ronda_2 + ["-"],
        "partidos": partidos,
        "campeones_grupo": campeones_grupo,
        "segundos_grupo": segundos_grupo,
        "mejores_terceros": [t[0] for t in mejores_terceros],
    }

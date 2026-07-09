from pathlib import Path
import json
import pandas as pd

from src.data_loader import crear_dataset_base, cargar_elo_ratings, cargar_ranking_fifa, _build_team_rating_map
from src.features import construir_features, FEATURE_COLUMNS
from src.models import entrenar_modelo
from src.simulate_bracket import construir_grupos_mundial, simular_torneo


def _generar_readme(resultado: dict, output_path: Path) -> None:
    campeon = resultado.get("campeon", "—")
    final = resultado.get("final", ["—", "—"])
    semis = resultado.get("semifinales", [])
    cuartos = resultado.get("cuartos", [])
    octavos = resultado.get("octavos", [])
    ronda_32 = resultado.get("dieciseisavos", [])
    grupos = resultado.get("grupos", {})
    campeones_grupo = resultado.get("campeones_grupo", {})
    segundos_grupo = resultado.get("segundos_grupo", {})
    mejores_terceros = resultado.get("mejores_terceros", [])
    partidos = resultado.get("partidos", [])
    metrics = resultado.get("modelo_metrics", {})

    def _match_block(local, visitante, gl, gv, ganador):
        return f"| {local} | **{gl} - {gv}** | {visitante} | ✅ {ganador} |"

    lines = []
    lines.append("# ⚽ Predicción Mundial 2026")
    lines.append("")
    lines.append("## 📊 Métricas del Modelo")
    lines.append("")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---------|-------|")
    lines.append(f"| Accuracy | **{metrics.get('accuracy', 0):.1%}** |")
    lines.append(f"| Precision | {metrics.get('precision', 0):.1%} |")
    lines.append(f"| Recall | {metrics.get('recall', 0):.1%} |")
    lines.append(f"| F1 | {metrics.get('f1', 0):.3f} |")
    lines.append(f"| ROC-AUC | {metrics.get('roc_auc', 0):.3f} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🏆 Resultado Final")
    lines.append("")
    lines.append(f"### 🥇 Campeón: **{campeon}**")
    lines.append("")
    lines.append(f"### 🥈 Final: **{final[0]}** vs **{final[1]}**")
    lines.append("")
    lines.append(f"### 🥉 Semifinalistas: {', '.join(semis)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 📋 Fase de Grupos")
    lines.append("")
    for letra in sorted(grupos.keys()):
        posiciones = grupos[letra]
        lines.append(f"### Grupo {letra}")
        lines.append("")
        lines.append("| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |")
        lines.append("|-----|--------|----|----|----|----|----|----|----|-----|")
        for i, item in enumerate(posiciones):
            eq, pts = item[0], item[1]
            pj, pg, pe, pp = item[2], item[3], item[4], item[5]
            gf, gc, dg = item[6], item[7], item[8]
            marker = " 🥇" if i == 0 else " 🥈" if i == 1 else ""
            lines.append(f"| {i+1} | **{eq}**{marker} | {pj} | {pg} | {pe} | {pp} | {gf} | {gc} | {dg} | **{pts}** |")
        lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 🏟️ Ronda de 32 (Dieciseisavos)")
    lines.append("")
    lines.append("| # | Enfrentamiento | Resultado | Ganador |")
    lines.append("|---|----------------|-----------|---------|")
    ronda_32_partidos = [p for p in partidos if p.get("ronda", "") == "32avos (Ronda de 32)"]
    for i, p in enumerate(ronda_32_partidos):
        lines.append(_match_block(p["local"], p["visitante"], p["goles_local"], p["goles_visitante"], p["ganador"]))
    lines.append("")
    lines.append(f"**Clasificados a Octavos:** {', '.join(octavos)}")
    lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 🏟️ Octavos de Final")
    lines.append("")
    lines.append("| # | Enfrentamiento | Resultado | Ganador |")
    lines.append("|---|----------------|-----------|---------|")
    octavos_partidos = [p for p in partidos if p.get("ronda", "") == "16avos (Octavos)"]
    for i, p in enumerate(octavos_partidos):
        lines.append(_match_block(p["local"], p["visitante"], p["goles_local"], p["goles_visitante"], p["ganador"]))
    lines.append("")
    lines.append(f"**Clasificados a Cuartos:** {', '.join(cuartos)}")
    lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 🏟️ Cuartos de Final")
    lines.append("")
    lines.append("| # | Enfrentamiento | Resultado | Ganador |")
    lines.append("|---|----------------|-----------|---------|")
    cuartos_partidos = [p for p in partidos if p.get("ronda", "") == "8avos (Cuartos)"]
    for i, p in enumerate(cuartos_partidos):
        lines.append(_match_block(p["local"], p["visitante"], p["goles_local"], p["goles_visitante"], p["ganador"]))
    lines.append("")
    lines.append(f"**Clasificados a Semifinales:** {', '.join(semis)}")
    lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 🏟️ Semifinales")
    lines.append("")
    lines.append("| # | Enfrentamiento | Resultado | Ganador |")
    lines.append("|---|----------------|-----------|---------|")
    semis_partidos = [p for p in partidos if p.get("ronda", "") == "4avos (Semifinales)"]
    for i, p in enumerate(semis_partidos):
        lines.append(_match_block(p["local"], p["visitante"], p["goles_local"], p["goles_visitante"], p["ganador"]))
    lines.append("")
    lines.append(f"**Finalistas:** {final[0]} vs {final[1]}")
    lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 🏟️ FINAL")
    lines.append("")
    final_partidos = [p for p in partidos if p.get("ronda", "") == "Final"]
    if final_partidos:
        p = final_partidos[0]
        lines.append(f"### {p['local']} **{p['goles_local']}** - **{p['goles_visitante']}** {p['visitante']}")
        lines.append("")
        lines.append(f"### 🏆 Campeón del Mundo 2026: **{campeon}** 🏆")
    lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 📈 Bracket Resumen")
    lines.append("")
    lines.append("```")
    lines.append(f"Ronda de 32:    {len(ronda_32)} equipos")
    lines.append(f"Octavos:        {len(octavos)} equipos → {', '.join(octavos)}")
    lines.append(f"Cuartos:        {len(cuartos)} equipos → {', '.join(cuartos)}")
    lines.append(f"Semifinales:    {len(semis)} equipos → {', '.join(semis)}")
    lines.append(f"Final:          {final[0]} vs {final[1]}")
    lines.append(f"Campeón:        {campeon}")
    lines.append("```")
    lines.append("")

    with output_path.open("w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    df = crear_dataset_base()
    df_features = construir_features(df)

    feature_cols = [c for c in FEATURE_COLUMNS if c in df_features.columns]
    target = df_features["target"]

    modelo, X_test, y_test = entrenar_modelo(df_features[feature_cols], target)
    accuracy = modelo.metrics.get("accuracy", 0.0)

    elo_df = cargar_elo_ratings()
    fifa_df = cargar_ranking_fifa()
    team_ratings = _build_team_rating_map(elo_df, fifa_df)

    grupos = construir_grupos_mundial()

    resultado = simular_torneo(grupos, modelo, team_ratings)
    resultado["modelo_accuracy"] = accuracy
    resultado["modelo_metrics"] = modelo.metrics

    result_path = output_dir / "prediccion_mundial_2026.json"
    with result_path.open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=2)

    readme_path = output_dir / "PREDICCION_MUNDIAL_2026.md"
    _generar_readme(resultado, readme_path)

    print("=" * 55)
    print("          PREDICCIÓN MUNDIAL 2026")
    print("=" * 55)
    print(f"  Precisión del modelo:       {accuracy:.3f}")
    print(f"  Campeón previsto:           {resultado['campeon']}")
    print(f"  Final prevista:             {resultado['final'][0]} vs {resultado['final'][1]}")
    print(f"  Semifinalistas:             {', '.join(resultado['semifinales'])}")
    print(f"  Archivo JSON:               outputs/prediccion_mundial_2026.json")
    print(f"  Archivo README:             outputs/PREDICCION_MUNDIAL_2026.md")
    print("=" * 55)


if __name__ == "__main__":
    main()

from pathlib import Path
import json
import pandas as pd

from src.data_loader import crear_dataset_base, cargar_elo_ratings, cargar_ranking_fifa, _build_team_rating_map
from src.features import construir_features, FEATURE_COLUMNS
from src.models import entrenar_modelo
from src.simulate_bracket import construir_grupos_mundial, simular_torneo


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

    print("=" * 55)
    print("          PREDICCIÓN MUNDIAL 2026")
    print("=" * 55)
    print(f"  Precisión del modelo:       {accuracy:.3f}")
    print(f"  Campeón previsto:           {resultado['campeon']}")
    print(f"  Final prevista:             {resultado['final'][0]} vs {resultado['final'][1]}")
    print(f"  Semifinalistas:             {', '.join(resultado['semifinales'])}")
    print(f"  Archivo generado:           outputs/prediccion_mundial_2026.json")
    print("=" * 55)


if __name__ == "__main__":
    main()

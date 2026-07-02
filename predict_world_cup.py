from pathlib import Path
import json
import pandas as pd

from src.data_loader import crear_dataset_base
from src.features import construir_features
from src.models import entrenar_modelo
from src.simulate_bracket import simular_torneo


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    df = crear_dataset_base()
    df_features = construir_features(df)

    features = df_features[["elo_diff", "form_diff", "goal_diff", "home_advantage"]]
    target = df_features["winner"]

    modelo, _, _ = entrenar_modelo(features, target)

    grupos = {
        "A": ["Argentina", "Brasil", "Uruguay", "Colombia"],
        "B": ["Francia", "Alemania", "España", "Inglaterra"],
        "C": ["Países Bajos", "Portugal", "Bélgica", "Japón"],
        "D": ["Corea del Sur", "Marruecos", "Estados Unidos", "México"],
    }

    resultado = simular_torneo(grupos, modelo)

    with (output_dir / "prediccion_mundial_2026.json").open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=2)

    print("Predicción generada en outputs/prediccion_mundial_2026.json")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

# Predictor Mundial 2026

Este proyecto implementa un pipeline de predicción para el Mundial 2026 usando modelos estadísticos y aprendizaje automático. Está pensado para ser reproducible, modular y fácil de ejecutar desde cualquier entorno local.

## ¿Qué hace?
- Genera un dataset base para entrenar un modelo de clasificación.
- Construye variables como diferencia de Elo, forma reciente y diferencia de goles.
- Entrena un modelo de Random Forest para estimar la probabilidad de victoria de un equipo.
- Produce una predicción de torneo y la guarda en formato JSON en la carpeta de outputs.

## Estructura del proyecto
- `data/raw/` – datos crudos o archivos base.
- `data/processed/` – datos limpios listos para modelado.
- `data/external/` – datasets de referencia como Elo o ranking FIFA.
- `src/` – módulos de Python para carga, features, modelos y simulación.
- `models/` – modelos entrenados.
- `outputs/` – predicciones y resultados generados.
- `reports/` – documentación y análisis.
- `tests/` – pruebas de validación.

## Requisitos
- Python 3.10 o superior.
- Dependencias listadas en `requirements.txt`.

## Cómo ejecutar
1. Crear un entorno virtual:
   `python -m venv venv`
2. Activar el entorno:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Instalar dependencias:
   `pip install -r requirements.txt`
4. Ejecutar pruebas:
   `pytest -q`
5. Ejecutar la predicción:
   `python predict_world_cup.py`
6. Abrir el dashboard:
   `streamlit run app.py`

## Despliegue
- El dashboard puede ejecutarse en Streamlit Cloud o en un entorno con Python y Streamlit instalado.
- El archivo principal de salida se genera automáticamente en `outputs/prediccion_mundial_2026.json`.

## Resultados
El script principal genera el archivo:
- `outputs/prediccion_mundial_2026.json`

## Nota importante
El proyecto ya funciona y genera resultados, aunque por ahora usa un dataset base sintético para asegurar que el pipeline sea ejecutable. Si agregas datos reales de partidos, Elo, ranking FIFA o plantillas, la predicción puede volverse mucho más precisa.

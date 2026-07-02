# Predictor Mundial 2026

Sistema de predicción del Mundial 2026 basado en modelos estadísticos
con un pipeline reproducible y ejecutable desde este repositorio.

## Qué hace el proyecto
- Genera un dataset base sintético para entrenar un modelo de clasificación.
- Construye features como diferencia de Elo, forma reciente y diferencia de goles.
- Entrena un Random Forest para estimar la probabilidad de victoria de un equipo local.
- Produce una predicción de torneo en formato JSON y la guarda en outputs.

## Estructura del proyecto
- `data/raw/` – datos descargados sin procesar o archivos base.
- `data/processed/` – datos limpios listos para modelar.
- `data/external/` – datasets de referencia (Elo, ranking FIFA, etc.).
- `src/` – módulos de Python (carga de datos, features, modelos, simulación).
- `models/` – modelos entrenados guardados.
- `outputs/` – predicciones y resultados generados.
- `reports/` – documentación de metodología y resultados.
- `tests/` – pruebas de validación del pipeline.

## Requisitos
- Python 3.10+.
- Dependencias de `requirements.txt`.

## Cómo correr
1. Crear entorno virtual: `python -m venv venv`
2. Activar entorno: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Mac/Linux)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar pruebas: `pytest -q`
5. Ejecutar predicción: `python predict_world_cup.py`

## Resultados
El script principal genera:
- `outputs/prediccion_mundial_2026.json`

## Notas
El proyecto ya está preparado para ejecutarse aunque los datos reales aún no estén descargados; usa los archivos de datos reales en `data/raw/` si quieres reemplazar el dataset sintético por uno más preciso.

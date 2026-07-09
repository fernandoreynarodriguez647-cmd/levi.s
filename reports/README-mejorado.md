# PREDICCIÓN MUNDIAL 2026 - Documentación Completa

## VISIÓN GENERAL

Sistema de predicción del Mundial 2026 que combina datos históricos reales,
modelos de Machine Learning y simulación de torneo para estimar el campeón,
los finalistas y el desarrollo completo del torneo (48 equipos, 12 grupos,
eliminatorias directas).

### Resultado actual de la predicción
- Campeón: España
- Final: España vs Senegal
- Semifinalistas: España, Portugal, Senegal
- Precisión del modelo: ~65%

---

## ARQUITECTURA DEL PROYECTO

```
predictor_mundial/
├── predict_world_cup.py      # Punto de entrada: ejecuta todo el pipeline
├── app.py                    # Dashboard interactivo (Streamlit)
├── src/                      # Módulos fuente
│   ├── data_loader.py        # Carga y preparación de datos
│   ├── features.py           # Ingeniería de características
│   ├── models.py             # Modelos de Machine Learning
│   └── simulate_bracket.py   # Simulación del torneo
├── data/raw/                 # Datos crudos
│   ├── historico_partidos/   # 49,477 partidos internacionales (1872-presente)
│   ├── elo_ratings/          # Ratings Elo de 244 selecciones
│   └── ranking_fifa/         # Ranking FIFA de 211 selecciones
├── outputs/                  # Resultados generados
│   └── prediccion_mundial_2026.json
├── tests/                    # Pruebas unitarias
└── reports/                  # Documentación e informes
```

---

## FLUJO DEL PIPELINE

### 1. CARGA DE DATOS (data_loader.py)

**Fuentes de datos:**
- `results.csv`: 49,477 partidos internacionales desde 1872
  - Columnas: fecha, equipo_local, equipo_visitante, goles_local, goles_visitante, torneo, ciudad, país, neutral
- `elo_rankings.json`: Ratings Elo de 244 selecciones
  - Sistema Elo: puntuación basada en resultados históricos (mayor = mejor)
  - Escala típica: 1400-2200 puntos
- `fifa_rankings.json`: Ranking FIFA de 211 selecciones
  - Puntuación compuesta por resultados, importancia del partido, fuerza del rival

**Procesamiento:**
- Normalización de nombres de equipos (ej: "brazil" → "Brasil", "south korea" → "Corea del Sur")
- Unificación de ratings: se usa Elo como primario, FIFA (dividido entre 10) como respaldo
- Cálculo de forma reciente: media de resultados de los últimos 5 partidos por equipo
- Los partidos con goles NaN se manejan con valor predeterminado 0

### 2. INGENIERÍA DE CARACTERÍSTICAS (features.py)

Se construyen 6 características predictivas (pre-partido):

| Característica | Fórmula | Descripción |
|---|---|---|
| `elo_diff` | elo_home - elo_away | Diferencia de calidad entre equipos |
| `form_diff` | form_home - form_away | Diferencia de forma reciente |
| `rank_diff` | elo_away - elo_home | Inverso de elo_diff (redundancia controlada) |
| `home_advantage` | 1 (constante) | Ventaja de localía |
| `rating_strength` | (elo_home + elo_away) / 2 | Nivel absoluto del partido |
| `relative_strength` | elo_home / (elo_away + 1) | Ventaja relativa del local |

**Target:** 1 si gana el local, 0 si no (incluye empates como 0).

**Nota importante:** NO se usan características post-partido (goal_diff, goles)
como features de entrenamiento para evitar data leakage.

### 3. ENTRENAMIENTO DEL MODELO (models.py)

**Modelo principal:** Random Forest Classifier

**Parámetros:**
- 400 árboles (n_estimators)
- Sin límite de profundidad (max_depth=None)
- Mínimo 2 muestras por hoja (min_samples_leaf=2)
- random_state=42 para reproducibilidad

**División de datos:** 80% entrenamiento, 20% prueba

**Métricas calculadas:**
- Accuracy (precisión global)
- Precision (precisión positiva)
- Recall (sensibilidad)
- F1-Score (media armónica)
- ROC-AUC (área bajo la curva)

**Modelos adicionales disponibles:**
- Gradient Boosting (n_estimators=200, max_depth=4)
- Regresión Logística (con escalado StandardScaler)

### 4. SIMULACIÓN DEL TORNEO (simulate_bracket.py)

#### Fase de grupos
- 48 equipos distribuidos en 12 grupos (A-L) de 4 equipos
- Cada equipo juega contra los otros 3 de su grupo (6 partidos por grupo)
- Puntuación: victoria=3pts, empate=1pt, derrota=0pts
- Clasifican: 1° y 2° de cada grupo (24 equipos a eliminatorias)

#### Eliminatorias (formato oficial Mundial 2026)
- **32avos de final (Ronda de 32):** 32 equipos → 16 ganadores
  - Clasifican: 12 campeones de grupo + 12 segundos + 8 mejores terceros
- **16avos de final (Octavos):** 16 → 8
- **8avos de final (Cuartos):** 8 → 4
- **Semifinales:** 4 → 2
- **Final:** 2 → 1 campeón

#### Simulación de cada partido
1. Se obtienen los ratings Elo reales de ambos equipos
2. Se añade ruido aleatorio (±40 puntos) para variabilidad
3. Se calcula probabilidad Elo: 1 / (1 + 10^(-elo_diff/400))
4. Se construyen features y se obtiene probabilidad del modelo ML
5. Blend: 60% modelo ML + 40% probabilidad Elo
6. Se generan goles con distribución Poisson:
   - Goles_local ~ Poisson(1.2 * probabilidad_blend)
   - Goles_visitante ~ Poisson(1.2 * (1-probabilidad_blend))
7. Si hay empate, se añade 1 gol al local

### 5. DASHBOARD (app.py)

Interfaz interactiva construida con Streamlit que muestra:

- **Métricas principales:** Campeón, Final, Semifinalistas, Total equipos
- **Favoritos:** Tarjetas visuales del campeón, finalistas y semifinalistas
- **Mapa del torneo:** Progresión visual desde fase de grupos hasta final
- **Fase de grupos:** Tablas expandibles con PJ, PG, PE, PP, GF, GC, DG, Pts
- **Eliminatorias:** Visualización de cada ronda knockout
- **Partidos simulados:** Lista completa con filtro por ronda y marcadores
- **Panel comparativo:** Gráfico de barras del avance de equipos destacados
- **Distribución por confederación:** Equipos por confederación (CONMEBOL, UEFA, etc.)
- **Recálculo:** Botón en sidebar para re-ejecutar el pipeline

### 6. PRUEBAS (tests/)

4 tests unitarios con pytest:
1. `test_construir_features_agrega_columnas_relevantes`: Verifica que el feature engineering genera las columnas correctas sin NaN
2. `test_entrenar_modelo_devuelve_modelo_y_evaluacion`: Verifica que el modelo entrena y retorna datos de prueba
3. `test_simulacion_de_torneo_devuelve_resultados`: Verifica que la simulación produce todas las claves esperadas
4. `test_construir_grupos_mundial_incluye_los_48_equipos`: Verifica 12 grupos × 4 = 48 equipos

---

## MEJORAS REALIZADAS

### Código
| Archivo | Mejora |
|---|---|
| `features.py` | Eliminadas features redundantes (goal_diff duplicado, form_diff duplicado). Solo 6 features predictivas + target |
| `data_loader.py` | Eliminado alias duplicado de México. Corregido bug de llamada recursiva. Manejo de NaN en goles con try/except |
| `models.py` | Agregados Gradient Boosting y Logistic Regression. Métricas extendidas (precisión, recall, F1, ROC-AUC). Función unificada `predecir_partido()` con soporte para scaler |
| `simulate_bracket.py` | Simulación real de grupos (round-robin con puntuación). Eliminatorias bracket real (24→12→6→3→2→1). Distribución Poisson para marcadores. Blend de probabilidades ML + Elo |
| `predict_world_cup.py` | Pipeline robusto con paso de team_ratings a simulación. Output más informativo |
| `app.py` | Dashboard completamentamente rediseñado con grupo expandibles, tabla de posiciones real, filtro de partidos por ronda, gráficos de barras, distribución por confederación, marcadores con goles |
| `tests/test_pipeline.py` | Tests actualizados para reflejar cambios en features y API |

### Datos
- Uso completo de los 49,477 partidos históricos (sin limitar a 5000)
- Ratings Elo como fuente principal, FIFA como respaldo
- Forma reciente calculada dinámicamente sobre últimos 5 partidos

---

## CÓMO EJECUTAR

```bash
# 1. Activar entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar pipeline de predicción
python predict_world_cup.py

# 4. Iniciar dashboard
streamlit run app.py

# 5. Ejecutar pruebas
pytest tests/ -v
```

---

## DEPENDENCIAS

- **pandas, numpy**: Manipulación de datos
- **scikit-learn**: Random Forest, Gradient Boosting, Logistic Regression, métricas
- **streamlit**: Dashboard interactivo
- **matplotlib, seaborn**: Visualización (base)
- **pytest**: Pruebas unitarias

---

## POSIBLES MEJORAS FUTURAS

1. **Datos de plantillas**: Incorporar valor de mercado de jugadores para mejorar features
2. **Modelos avanzados**: XGBoost, LightGBM, redes neuronales
3. **Hiperparámetros**: GridSearchCV para optimización automática
4. **Más simulaciones**: Monte Carlo (1000+ simulaciones) para estimar probabilidades
5. **Predicción de marcadores exactos**: Modelo Poisson bivariado
6. **Actualización automática**: Scraping de últimos resultados antes de simular
7. **Dashboard extendido**: Heatmaps de probabilidades, tabla de enfrentamientos directos

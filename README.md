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

### 🏆 Resultado Final

- 🥇 **Campeón: España**
- 🥈 Final: **España** vs **Bélgica**
- 🥉 Semifinalistas: España, Noruega, Ecuador, Bélgica

---

### 📋 Fase de Grupos

#### Grupo A

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Argentina** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **México** 🥈 | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 3 | **Argelia** | 3 | 0 | 2 | 1 | 2 | 4 | -2 | **2** |
| 4 | **Jordania** | 3 | 0 | 1 | 2 | 2 | 5 | -3 | **1** |

#### Grupo B

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **España** 🥇 | 3 | 3 | 0 | 0 | 6 | 2 | 4 | **9** |
| 2 | **Suiza** 🥈 | 3 | 1 | 1 | 1 | 4 | 3 | 1 | **4** |
| 3 | **Canadá** | 3 | 1 | 1 | 1 | 4 | 3 | 1 | **4** |
| 4 | **Cabo Verde** | 3 | 0 | 0 | 3 | 0 | 6 | -6 | **0** |

#### Grupo C

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Francia** 🥇 | 3 | 3 | 0 | 0 | 6 | 2 | 4 | **9** |
| 2 | **República de Corea** 🥈 | 3 | 1 | 1 | 1 | 4 | 3 | 1 | **4** |
| 3 | **Bélgica** | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 4 | **Bosnia y Herzegovina** | 3 | 0 | 0 | 3 | 1 | 6 | -5 | **0** |

#### Grupo D

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Inglaterra** 🥇 | 3 | 3 | 0 | 0 | 6 | 3 | 3 | **9** |
| 2 | **Marruecos** 🥈 | 3 | 1 | 1 | 1 | 4 | 3 | 1 | **4** |
| 3 | **Escocia** | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 4 | **Arabia Saudí** | 3 | 0 | 0 | 3 | 2 | 6 | -4 | **0** |

#### Grupo E

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Colombia** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **Ecuador** 🥈 | 3 | 1 | 1 | 1 | 4 | 3 | 1 | **4** |
| 3 | **Irán** | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 4 | **Iraq** | 3 | 0 | 0 | 3 | 1 | 6 | -5 | **0** |

#### Grupo F

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Portugal** 🥇 | 3 | 3 | 0 | 0 | 7 | 1 | 6 | **9** |
| 2 | **Uruguay** 🥈 | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 3 | **Egipto** | 3 | 0 | 2 | 1 | 2 | 4 | -2 | **2** |
| 4 | **Ghana** | 3 | 0 | 1 | 2 | 3 | 6 | -3 | **1** |

#### Grupo G

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Brasil** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **Austria** 🥈 | 3 | 2 | 0 | 1 | 5 | 3 | 2 | **6** |
| 3 | **Costa de Marfil** | 3 | 1 | 0 | 2 | 3 | 4 | -1 | **3** |
| 4 | **Túnez** | 3 | 0 | 0 | 3 | 0 | 6 | -6 | **0** |

#### Grupo H

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Países Bajos** 🥇 | 3 | 3 | 0 | 0 | 5 | 0 | 5 | **9** |
| 2 | **Estados Unidos** 🥈 | 3 | 1 | 1 | 1 | 3 | 3 | 0 | **4** |
| 3 | **Suecia** | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 4 | **Nueva Zelanda** | 3 | 0 | 0 | 3 | 2 | 6 | -4 | **0** |

#### Grupo I

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Alemania** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **Senegal** 🥈 | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 3 | **Chequia** | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 4 | **Haití** | 3 | 0 | 0 | 3 | 2 | 6 | -4 | **0** |

#### Grupo J

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Noruega** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **Paraguay** 🥈 | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 3 | **Uzbekistán** | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 4 | **Sudáfrica** | 3 | 0 | 0 | 3 | 2 | 6 | -4 | **0** |

#### Grupo K

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Japón** 🥇 | 3 | 3 | 0 | 0 | 6 | 1 | 5 | **9** |
| 2 | **Turquía** 🥈 | 3 | 1 | 1 | 1 | 4 | 4 | 0 | **4** |
| 3 | **RD Congo** | 3 | 1 | 1 | 1 | 3 | 4 | -1 | **4** |
| 4 | **Curazao** | 3 | 0 | 0 | 3 | 2 | 6 | -4 | **0** |

#### Grupo L

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|--------|----|----|----|----|----|----|----|-----|
| 1 | **Croacia** 🥇 | 3 | 3 | 0 | 0 | 6 | 2 | 4 | **9** |
| 2 | **Australia** 🥈 | 3 | 2 | 0 | 1 | 5 | 2 | 3 | **6** |
| 3 | **Panamá** | 3 | 1 | 0 | 2 | 3 | 5 | -2 | **3** |
| 4 | **Qatar** | 3 | 0 | 0 | 3 | 1 | 6 | -5 | **0** |

---

### 🏟️ Ronda de 32 (Dieciseisavos)

| # | Enfrentamiento | Resultado | Ganador |
|---|----------------|-----------|---------|
| 1 | Argentina vs España | **1 - 2** | ✅ España |
| 2 | Francia vs Inglaterra | **2 - 1** | ✅ Francia |
| 3 | Colombia vs Portugal | **1 - 2** | ✅ Portugal |
| 4 | Brasil vs Países Bajos | **2 - 1** | ✅ Brasil |
| 5 | Alemania vs Noruega | **1 - 2** | ✅ Noruega |
| 6 | Japón vs Croacia | **1 - 2** | ✅ Croacia |
| 7 | México vs Suiza | **1 - 2** | ✅ Suiza |
| 8 | Rep. de Corea vs Marruecos | **1 - 2** | ✅ Marruecos |
| 9 | Ecuador vs Uruguay | **2 - 1** | ✅ Ecuador |
| 10 | Austria vs Estados Unidos | **2 - 1** | ✅ Austria |
| 11 | Senegal vs Paraguay | **1 - 2** | ✅ Paraguay |
| 12 | Turquía vs Australia | **2 - 1** | ✅ Turquía |
| 13 | Canadá vs Bélgica | **1 - 2** | ✅ Bélgica |
| 14 | Escocia vs Irán | **2 - 1** | ✅ Escocia |
| 15 | Suecia vs Chequia | **1 - 2** | ✅ Chequia |
| 16 | Uzbekistán vs RD Congo | **2 - 1** | ✅ Uzbekistán |

**Clasificados a Octavos:** España, Francia, Portugal, Brasil, Noruega, Croacia, Suiza, Marruecos, Ecuador, Austria, Paraguay, Turquía, Bélgica, Escocia, Chequia, Uzbekistán

---

### 🏟️ Octavos de Final

| # | Enfrentamiento | Resultado | Ganador |
|---|----------------|-----------|---------|
| 1 | España vs Francia | **2 - 1** | ✅ España |
| 2 | Portugal vs Brasil | **1 - 2** | ✅ Brasil |
| 3 | Noruega vs Croacia | **2 - 1** | ✅ Noruega |
| 4 | Suiza vs Marruecos | **2 - 1** | ✅ Suiza |
| 5 | Ecuador vs Austria | **2 - 1** | ✅ Ecuador |
| 6 | Paraguay vs Turquía | **2 - 1** | ✅ Paraguay |
| 7 | Bélgica vs Escocia | **2 - 1** | ✅ Bélgica |
| 8 | Chequia vs Uzbekistán | **2 - 1** | ✅ Chequia |

**Clasificados a Cuartos:** España, Brasil, Noruega, Suiza, Ecuador, Paraguay, Bélgica, Chequia

---

### 🏟️ Cuartos de Final

| # | Enfrentamiento | Resultado | Ganador |
|---|----------------|-----------|---------|
| 1 | España vs Brasil | **2 - 1** | ✅ España |
| 2 | Noruega vs Suiza | **2 - 1** | ✅ Noruega |
| 3 | Ecuador vs Paraguay | **2 - 1** | ✅ Ecuador |
| 4 | Bélgica vs Chequia | **2 - 1** | ✅ Bélgica |

**Clasificados a Semifinales:** España, Noruega, Ecuador, Bélgica

---

### 🏟️ Semifinales

| # | Enfrentamiento | Resultado | Ganador |
|---|----------------|-----------|---------|
| 1 | España vs Noruega | **2 - 1** | ✅ España |
| 2 | Ecuador vs Bélgica | **1 - 2** | ✅ Bélgica |

**Finalistas:** España vs Bélgica

---

### 🏟️ FINAL

| Enfrentamiento | Resultado | Campeón |
|----------------|-----------|---------|
| España vs Bélgica | **2 - 0** | 🏆 **España** 🏆 |

---

### 📈 Bracket Resumen

```
Ronda de 32:    32 equipos
Octavos:        16 equipos → España, Francia, Portugal, Brasil, Noruega, Croacia, Suiza, Marruecos, Ecuador, Austria, Paraguay, Turquía, Bélgica, Escocia, Chequia, Uzbekistán
Cuartos:        8 equipos → España, Brasil, Noruega, Suiza, Ecuador, Paraguay, Bélgica, Chequia
Semifinales:    4 equipos → España, Noruega, Ecuador, Bélgica
Final:          España vs Bélgica
Campeón:        España
```

---

## Nota importante
El proyecto ya funciona y genera resultados, aunque por ahora usa un dataset base sintético para asegurar que el pipeline sea ejecutable. Si agregas datos reales de partidos, Elo, ranking FIFA o plantillas, la predicción puede volverse mucho más precisa.

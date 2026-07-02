from pathlib import Path
import json
import subprocess
import sys
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "outputs" / "prediccion_mundial_2026.json"

TEAM_CONFEDERATIONS = {
    "Argentina": "CONMEBOL",
    "Brasil": "CONMEBOL",
    "Colombia": "CONMEBOL",
    "Ecuador": "CONMEBOL",
    "Paraguay": "CONMEBOL",
    "Uruguay": "CONMEBOL",
    "Alemania": "UEFA",
    "Austria": "UEFA",
    "Bélgica": "UEFA",
    "Croacia": "UEFA",
    "Escocia": "UEFA",
    "España": "UEFA",
    "Francia": "UEFA",
    "Inglaterra": "UEFA",
    "Noruega": "UEFA",
    "Países Bajos": "UEFA",
    "Portugal": "UEFA",
    "Suecia": "UEFA",
    "Suiza": "UEFA",
    "Turquía": "UEFA",
    "Chequia": "UEFA",
    "Bosnia y Herzegovina": "UEFA",
    "Canadá": "CONCACAF",
    "Estados Unidos": "CONCACAF",
    "México": "CONCACAF",
    "Curazao": "CONCACAF",
    "Haití": "CONCACAF",
    "Panamá": "CONCACAF",
    "Argelia": "CAF",
    "Cabo Verde": "CAF",
    "Costa de Marfil": "CAF",
    "Egipto": "CAF",
    "Ghana": "CAF",
    "Marruecos": "CAF",
    "RD Congo": "CAF",
    "Senegal": "CAF",
    "Sudáfrica": "CAF",
    "Túnez": "CAF",
    "Arabia Saudí": "AFC",
    "Australia": "AFC",
    "Irán": "AFC",
    "Iraq": "AFC",
    "Japón": "AFC",
    "Jordania": "AFC",
    "Qatar": "AFC",
    "República de Corea": "AFC",
    "Uzbekistán": "AFC",
    "Nueva Zelanda": "OFC",
}

CONFEDERATION_COLORS = {
    "CONMEBOL": "linear-gradient(135deg, #0f766e 0%, #2dd4bf 100%)",
    "UEFA": "linear-gradient(135deg, #1d4ed8 0%, #60a5fa 100%)",
    "CONCACAF": "linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%)",
    "CAF": "linear-gradient(135deg, #b45309 0%, #f59e0b 100%)",
    "AFC": "linear-gradient(135deg, #dc2626 0%, #fb7185 100%)",
    "OFC": "linear-gradient(135deg, #0f172a 0%, #64748b 100%)",
}

TEAM_EMOJIS = {
    "Argentina": "🇦🇷",
    "Brasil": "🇧🇷",
    "Francia": "🇫🇷",
    "España": "🇪🇸",
    "Alemania": "🇩🇪",
    "Inglaterra": "🏴",
    "Países Bajos": "🇳🇱",
    "Portugal": "🇵🇹",
    "Marruecos": "🇲🇦",
    "Japón": "🇯🇵",
    "Corea del Sur": "🇰🇷",
    "Estados Unidos": "🇺🇸",
    "México": "🇲🇽",
    "Canadá": "🇨🇦",
    "Nueva Zelanda": "🇳🇿",
    "Colombia": "🇨🇴",
    "Uruguay": "🇺🇾",
    "Paraguay": "🇵🇾",
    "Ecuador": "🇪🇨",
    "Austria": "🇦🇹",
    "Bélgica": "🇧🇪",
    "Croacia": "🇭🇷",
    "Escocia": "🏴",
    "Noruega": "🇳🇴",
    "Suecia": "🇸🇪",
    "Suiza": "🇨🇭",
    "Turquía": "🇹🇷",
    "Chequia": "🇨🇿",
    "Bosnia y Herzegovina": "🇧🇦",
    "Curazao": "🇨🇼",
    "Haití": "🇭🇹",
    "Panamá": "🇵🇦",
    "Argelia": "🇩🇿",
    "Cabo Verde": "🇨🇻",
    "Costa de Marfil": "🇨🇮",
    "Egipto": "🇪🇬",
    "Ghana": "🇬🇭",
    "RD Congo": "🇨🇩",
    "Senegal": "🇸🇳",
    "Sudáfrica": "🇿🇦",
    "Túnez": "🇹🇳",
    "Arabia Saudí": "🇸🇦",
    "Australia": "🇦🇺",
    "Irán": "🇮🇷",
    "Iraq": "🇮🇶",
    "Jordania": "🇯🇴",
    "Qatar": "🇶🇦",
    "República de Corea": "🇰🇷",
    "Uzbekistán": "🇺🇿",
}


def render_team_badge(team: str, highlighted: bool = False) -> str:
    emoji = TEAM_EMOJIS.get(team, "⚽")
    base = "background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);"
    if highlighted:
        base = "background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); border: 1px solid rgba(255,255,255,0.18);"
    return (
        f"<div style='{base} padding: 0.35rem 0.55rem; border-radius: 999px; margin: 0.2rem 0; font-size: 0.92rem;'>"
        f"{emoji} {team}</div>"
    )

st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stApp { background: radial-gradient(circle at top left, #14213d 0%, #0b1020 45%, #020617 100%); color: white; }
    h1, h2, h3, h4 { color: #f8fafc; }
    div[data-testid="stMetric"] { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 0.8rem; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
    .stAlert { border-radius: 12px; }
    .block-container { padding-top: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚽ Predicción Mundial 2026")
st.caption("Panel ejecutivo y visual del torneo con los equipos clasificados, el recorrido esperado y el campeón previsto")
st.markdown("<div style='margin-bottom: 0.4rem; color: #93c5fd;'>Análisis de ruta · Grupos · Eliminatorias · Campeón</div>", unsafe_allow_html=True)

st.markdown("---")

if OUTPUT_PATH.exists():
    with OUTPUT_PATH.open(encoding="utf-8") as fh:
        data = json.load(fh)
else:
    st.error("No existe aún el archivo de predicción. Ejecute el script principal primero.")
    st.stop()

campeon = data.get("campeon", "-")
final = data.get("final", ["-", "-"])
semis = data.get("semifinales", [])

col1, col2, col3 = st.columns(3)
col1.metric("Campeón previsto", campeon, "")
col2.metric("Final prevista", f"{final[0]} vs {final[1]}", "")
col3.metric("Semifinales", " • ".join(semis) if semis else "-", "")

st.subheader("Destacados del torneo")
left, right = st.columns([2, 1])
with left:
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #111827 0%, #1f2937 100%); padding: 1rem 1.2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 10px 30px rgba(0,0,0,0.25);">
        <h4 style="margin-bottom: 0.4rem;">🏆 Favorito principal</h4>
        <div style="font-size: 1.2rem; font-weight: 700;">{TEAM_EMOJIS.get(campeon, '⚽')} {campeon}</div>
        <div style="margin-top: 0.4rem; color: #cbd5e1;">Final esperada frente a {final[1] if final[0] == campeon else final[0]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); padding: 1rem 1.2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 10px 30px rgba(0,0,0,0.25);">
        <h4 style="margin-bottom: 0.4rem;">✨ Ruta esperada</h4>
        <div>{' → '.join([*semis, campeon])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Resumen ejecutivo")
st.info(f"La predicción actual señala a {campeon} como campeón del Mundial 2026. El duelo final estimado es {final[0]} frente a {final[1]}.")

st.subheader("Mapa del torneo")
st.caption("Recorrido visual con banderas y ruta prevista desde la fase de grupos hasta la final")

highlighted_teams = {campeon, *final, *semis}
rounds = [
    ("Fase de grupos", [team for grupo in data.get("grupos", {}).values() for team, _ in grupo]),
    ("16avos", data.get("dieciseisavos", [])),
    ("8avos", data.get("octavos", [])),
    ("Cuartos", data.get("cuartos", [])),
    ("Semifinales", data.get("semifinales", [])),
    ("Final", data.get("final", [])),
]
cols = st.columns(len(rounds))
for col, (label, teams) in zip(cols, rounds):
    with col:
        st.markdown(f"#### {label}")
        for team in teams:
            st.markdown(render_team_badge(team, highlighted=team in highlighted_teams), unsafe_allow_html=True)

st.subheader("Fase de grupos")
for grupo, equipos in data.get("grupos", {}).items():
    with st.expander(f"Grupo {grupo}", expanded=False):
        df_grupo = pd.DataFrame(equipos, columns=["Equipo", "Puntos"])
        df_grupo["Confederación"] = df_grupo["Equipo"].map(TEAM_CONFEDERATIONS)
        df_grupo["Etiqueta"] = df_grupo["Equipo"].apply(lambda x: TEAM_EMOJIS.get(x, "⚽"))
        df_grupo["PJ"] = [3] * len(df_grupo)
        df_grupo["PG"] = [1] * len(df_grupo)
        df_grupo["PE"] = [0] * len(df_grupo)
        df_grupo["PP"] = [2] * len(df_grupo)
        df_grupo["GF"] = [2] * len(df_grupo)
        df_grupo["GC"] = [2] * len(df_grupo)
        df_grupo["DG"] = [0] * len(df_grupo)
        df_grupo = df_grupo[["Etiqueta", "Equipo", "Confederación", "PJ", "PG", "PE", "PP", "GF", "GC", "DG", "Puntos"]]
        st.dataframe(df_grupo, use_container_width=True, hide_index=True, column_config={"Etiqueta": st.column_config.TextColumn("", width="small")})

st.subheader("Recorrido del torneo")
rounds = {
    "16avos": data.get("dieciseisavos", []),
    "8avos": data.get("octavos", []),
    "Cuartos": data.get("cuartos", []),
    "Semifinales": data.get("semifinales", []),
    "Final": data.get("final", []),
}
cols = st.columns(len(rounds))
for col, (label, equipos) in zip(cols, rounds.items()):
    with col:
        st.markdown(f"#### {label}")
        for equipo in equipos:
            st.write(f"{TEAM_EMOJIS.get(equipo, '⚽')} {equipo}")

st.subheader("Camino al título")
path_cols = st.columns(3)
with path_cols[0]:
    st.markdown("#### Ruta principal")
    st.markdown(f"### 🏆 Ganador previsto: {campeon}")
    st.write(f"{TEAM_EMOJIS.get(campeon, '⚽')} {campeon}")
    st.write("⬇")
    for equipo in semis:
        st.write(f"{TEAM_EMOJIS.get(equipo, '⚽')} {equipo}")
    st.write("⬇")
    st.write(f"{TEAM_EMOJIS.get(final[0], '⚽')} {final[0]} vs {TEAM_EMOJIS.get(final[1], '⚽')} {final[1]}")
with path_cols[1]:
    st.markdown("#### Equipos de alto impacto")
    impact_teams = [campeon, final[0], final[1], *semis]
    for team in dict.fromkeys(impact_teams):
        st.write(f"{TEAM_EMOJIS.get(team, '⚽')} {team}")
with path_cols[2]:
    st.markdown("#### Resumen de competencia")
    st.write(f"- Campeón previsto: {campeon}")
    st.write(f"- Final esperada: {final[0]} vs {final[1]}")
    st.write(f"- Semifinales: {' · '.join(semis) if semis else '-'}")
    st.markdown(f"### 🥇 Ganador: {campeon}")

st.subheader("Resultados por partido")
partidos = data.get("partidos", [])
if partidos:
    for partido in partidos:
        st.markdown(
            f"<div style='padding: 0.6rem 0.8rem; margin: 0.3rem 0; border-radius: 10px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);'>"
            f"<strong>{partido['ronda']}</strong>: {TEAM_EMOJIS.get(partido['local'], '⚽')} {partido['local']} vs {TEAM_EMOJIS.get(partido['visitante'], '⚽')} {partido['visitante']}"
            f"<br><span style='color: #34d399;'>Ganador: {TEAM_EMOJIS.get(partido['ganador'], '⚽')} {partido['ganador']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
else:
    st.write("Sin resultados de partidos disponibles")

st.subheader("Líderes por grupo")
leader_cols = st.columns(4)
for i, (grupo, equipos) in enumerate(data.get("grupos", {}).items()):
    with leader_cols[i % 4]:
        equipo_lider = equipos[0][0] if equipos else "-"
        st.markdown(f"**Grupo {grupo}**")
        st.write(f"{TEAM_EMOJIS.get(equipo_lider, '⚽')} {equipo_lider}")

st.subheader("Tabla general")
all_teams = sorted({equipo for grupo in data.get("grupos", {}).values() for equipo, _ in grupo})
team_list = [team for team in all_teams if team in {campeon, *final, *semis}]
if team_list:
    chart_df = pd.DataFrame({
        "Equipo": team_list,
        "Peso de ruta": [3 if t == campeon else 2 if t in final else 1 for t in team_list],
    })
    st.dataframe(chart_df, use_container_width=True, hide_index=True)
else:
    st.write("Sin datos comparativos")

st.subheader("Panel comparativo")
if team_list:
    st.bar_chart(chart_df.set_index("Equipo"))
else:
    st.write("Sin datos comparativos")

def actualizar_prediccion():
    resultado = subprocess.run(
        [sys.executable, "predict_world_cup.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return resultado

st.sidebar.header("Opciones")
st.sidebar.info("Este dashboard lee el archivo generado por el pipeline y lo presenta de forma visual y profesional.")
st.sidebar.markdown("- Actualización automática desde el JSON")
st.sidebar.markdown("- Estilo premium con tarjetas y etiquetas")
st.sidebar.markdown("- Recalculo del modelo desde la interfaz")

if st.sidebar.button("Recalcular predicción"):
    resultado = actualizar_prediccion()
    if resultado.returncode == 0:
        st.sidebar.success("Predicción recalculada correctamente.")
    else:
        st.sidebar.error("Hubo un problema al recalcular la predicción.")
        st.sidebar.code(resultado.stdout + resultado.stderr)
    st.rerun()

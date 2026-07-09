from pathlib import Path
import json
import subprocess
import sys
from collections import defaultdict
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "outputs" / "prediccion_mundial_2026.json"

CONF_COLORS = {
    "CONMEBOL": "#0f766e", "UEFA": "#1d4ed8", "CONCACAF": "#7c3aed",
    "CAF": "#b45309", "AFC": "#dc2626", "OFC": "#64748b",
}
BANNER_GRADIENTS = {
    "CONMEBOL": "linear-gradient(135deg, #0f766e 0%, #2dd4bf 100%)",
    "UEFA": "linear-gradient(135deg, #1d4ed8 0%, #60a5fa 100%)",
    "CONCACAF": "linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%)",
    "CAF": "linear-gradient(135deg, #b45309 0%, #f59e0b 100%)",
    "AFC": "linear-gradient(135deg, #dc2626 0%, #fb7185 100%)",
    "OFC": "linear-gradient(135deg, #0f172a 0%, #64748b 100%)",
}
TEAM_CONF = {
    "Argentina":"CONMEBOL","Brasil":"CONMEBOL","Colombia":"CONMEBOL","Ecuador":"CONMEBOL",
    "Paraguay":"CONMEBOL","Uruguay":"CONMEBOL",
    "Alemania":"UEFA","Austria":"UEFA","Bélgica":"UEFA","Croacia":"UEFA","Escocia":"UEFA",
    "España":"UEFA","Francia":"UEFA","Inglaterra":"UEFA","Noruega":"UEFA","Países Bajos":"UEFA",
    "Portugal":"UEFA","Suecia":"UEFA","Suiza":"UEFA","Turquía":"UEFA","Chequia":"UEFA",
    "Bosnia y Herzegovina":"UEFA",
    "Canadá":"CONCACAF","Estados Unidos":"CONCACAF","México":"CONCACAF","Curazao":"CONCACAF",
    "Haití":"CONCACAF","Panamá":"CONCACAF",
    "Argelia":"CAF","Cabo Verde":"CAF","Costa de Marfil":"CAF","Egipto":"CAF","Ghana":"CAF",
    "Marruecos":"CAF","RD Congo":"CAF","Senegal":"CAF","Sudáfrica":"CAF","Túnez":"CAF",
    "Arabia Saudí":"AFC","Australia":"AFC","Irán":"AFC","Iraq":"AFC","Japón":"AFC",
    "Jordania":"AFC","Qatar":"AFC","República de Corea":"AFC","Uzbekistán":"AFC",
    "Nueva Zelanda":"OFC",
}
TEAM_EMOJIS = {
    "Argentina":"🇦🇷","Brasil":"🇧🇷","Francia":"🇫🇷","España":"🇪🇸","Alemania":"🇩🇪",
    "Inglaterra":"🇬🇧","Países Bajos":"🇳🇱","Portugal":"🇵🇹","Marruecos":"🇲🇦",
    "Japón":"🇯🇵","Corea del Sur":"🇰🇷","Estados Unidos":"🇺🇸","México":"🇲🇽",
    "Canadá":"🇨🇦","Nueva Zelanda":"🇳🇿","Colombia":"🇨🇴","Uruguay":"🇺🇾",
    "Paraguay":"🇵🇾","Ecuador":"🇪🇨","Austria":"🇦🇹","Bélgica":"🇧🇪","Croacia":"🇭🇷",
    "Escocia":"🇬🇧","Noruega":"🇳🇴","Suecia":"🇸🇪","Suiza":"🇨🇭","Turquía":"🇹🇷",
    "Chequia":"🇨🇿","Bosnia y Herzegovina":"🇧🇦","Curazao":"🇨🇼","Haití":"🇭🇹",
    "Panamá":"🇵🇦","Argelia":"🇩🇿","Cabo Verde":"🇨🇻","Costa de Marfil":"🇨🇮",
    "Egipto":"🇪🇬","Ghana":"🇬🇭","RD Congo":"🇨🇩","Senegal":"🇸🇳","Sudáfrica":"🇿🇦",
    "Túnez":"🇹🇳","Arabia Saudí":"🇸🇦","Australia":"🇦🇺","Irán":"🇮🇷","Iraq":"🇮🇶",
    "Jordania":"🇯🇴","Qatar":"🇶🇦","República de Corea":"🇰🇷","Uzbekistán":"🇺🇿",
}

st.set_page_config(page_title="Mundial 2026 - Predicción", page_icon="⚽", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
.stApp { background: radial-gradient(circle at top left, #0c1929 0%, #0a0f1a 50%, #020512 100%); color: #e2e8f0; }
h1, h2, h3, h4 { color: #f1f5f9; letter-spacing: -0.02em; }
div[data-testid="stMetric"] { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 0.8rem; }
.stAlert { border-radius: 12px; }
div[data-testid="stExpander"] { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; }
hr { border-color: rgba(255,255,255,0.08); }
.match-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 0.7rem 1rem; margin: 0.3rem 0; transition: 0.2s; }
.match-card:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); }
.bracket-cell { display: flex; flex-direction: column; align-items: center; text-align: center; }
.bracket-line { border-left: 2px solid rgba(255,255,255,0.15); height: 20px; margin: 0 auto; }
.team-flag { font-size: 1.3rem; line-height: 1; }
</style>
""", unsafe_allow_html=True)

if not OUTPUT_PATH.exists():
    st.error("Ejecute `python predict_world_cup.py` primero")
    st.stop()

with OUTPUT_PATH.open(encoding="utf-8") as fh:
    data = json.load(fh)

campeon = data.get("campeon", "—")
final = data.get("final", ["—", "—"])
partidos = data.get("partidos", [])
grupos_data = data.get("grupos", {})
ronda_32 = data.get("dieciseisavos", [])
octavos = data.get("octavos", [])
cuartos = data.get("cuartos", [])
semis = data.get("semifinales", [])
final_lista = data.get("final_lista", [])
campeones_grupo = data.get("campeones_grupo", {})
mejores_terceros = data.get("mejores_terceros", [])

by_round = defaultdict(list)
for p in partidos:
    by_round[p["ronda"]].append(p)

round_order = []
ko_rounds = ["32avos (Ronda de 32)", "16avos (Octavos)", "8avos (Cuartos)", "4avos (Semifinales)", "Final"]
for label in ["Grupo A","Grupo B","Grupo C","Grupo D","Grupo E","Grupo F","Grupo G","Grupo H","Grupo I","Grupo J","Grupo K","Grupo L"]:
    round_order.append(label)
round_order.extend(ko_rounds)

def team_html(team, size="0.9rem"):
    conf = TEAM_CONF.get(team, "")
    color = CONF_COLORS.get(conf, "#64748b")
    emoji = TEAM_EMOJIS.get(team, "⚽")
    return f'<span style="font-size:{size}">{emoji}</span> <span style="font-weight:600;color:#f1f5f9">{team}</span> <span style="background:{color}22;color:{color};border:1px solid {color}44;border-radius:999px;padding:0.05rem 0.4rem;font-size:0.6rem;font-weight:600">{conf}</span>'

def match_block(p):
    ga = p.get("goles_local", "?")
    gb = p.get("goles_visitante", "?")
    return f"""
    <div class="match-card">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:0.5rem">
            <div style="flex:1;text-align:right">{team_html(p["local"])}</div>
            <div style="background:#111827;border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:0.15rem 0.7rem;font-weight:800;font-size:1.1rem;color:#fbbf24;white-space:nowrap">{ga} - {gb}</div>
            <div style="flex:1;text-align:left">{team_html(p["visitante"])}</div>
        </div>
        <div style="margin-top:0.3rem;color:#34d399;font-size:0.8rem;text-align:center">✅ {team_html(p["ganador"], "0.8rem")}</div>
    </div>
    """

# ========== HEADER ==========
st.title("⚽ Predicción Mundial 2026")
st.caption("48 equipos · 12 grupos · 32 eliminatorias · 1 campeón")
st.markdown("---")

# ========== TOP METRICS ==========
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏆 Campeón", team_html(campeon), "")
col2.metric("🥇 Final", f"{TEAM_EMOJIS.get(final[0],'')} {final[0]} vs {TEAM_EMOJIS.get(final[1],'')} {final[1]}", "")
col3.metric("🏅 Semifinalistas", " • ".join(semis), "")
col4.metric("👥 Equipos", "48", "12 grupos")

# ========== BRACKET / PIRAMIDE ==========
st.subheader("🗺️ Recorrido completo (pirámide del torneo)")
st.caption("Cada columna es una ronda. Los ganadores avanzan hacia la derecha hasta la final.")

# Build bracket rounds data
bracket_rounds = [
    ("Fase Grupos", [
        {"teams": v, "label": f"Grupo {k}"}
        for k, v in sorted(grupos_data.items())
    ]),
    ("32avos", ronda_32),
    ("16avos", octavos),
    ("Cuartos", cuartos),
    ("Semifinales", semis),
    ("Final", final_lista),
]

# Show bracket as columns
cols = st.columns([2, 1.5, 1.2, 1, 1, 1])
for ci, (col, (label, data_round)) in enumerate(zip(cols, bracket_rounds)):
    with col:
        st.markdown(f"**{label}**")
        if label == "Fase Grupos":
            for g in data_round:
                st.markdown(f"<div style='font-size:0.7rem;color:#94a3b8;margin:0.1rem 0'>{g['label']}</div>", unsafe_allow_html=True)
                for team, *_ in g["teams"]:
                    hl = team == campeones_grupo.get(g["label"][-1], "")
                    bg = "background:#05966933;border-color:#34d399" if hl else ""
                    st.markdown(f'<div style="{bg};border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:0.1rem 0.4rem;margin:0.1rem 0;font-size:0.75rem">{TEAM_EMOJIS.get(team,"⚽")} {team}</div>', unsafe_allow_html=True)
        elif isinstance(data_round, list):
            for team in data_round:
                conf = TEAM_CONF.get(team, "")
                color = CONF_COLORS.get(conf, "#64748b")
                hl = team in {campeon, *final, *semis}
                bg = "background:#05966933;border-color:#34d399" if hl else ""
                st.markdown(f'<div style="{bg};border-left:3px solid {color};border-radius:4px;padding:0.15rem 0.4rem;margin:0.15rem 0;font-size:0.8rem">{TEAM_EMOJIS.get(team,"⚽")} {team}</div>', unsafe_allow_html=True)

st.markdown("---")

# ========== GRUPOS ==========
st.subheader("📊 Fase de grupos")
grp_tabs = st.tabs([f"Grupo {g}" for g in sorted(grupos_data.keys())])
for ti, letra in enumerate(sorted(grupos_data.keys())):
    with grp_tabs[ti]:
        posiciones = grupos_data[letra]
        records = []
        for item in posiciones:
            eq, pts, pj, pg, pe, pp, gf, gc, dg = item[:9] if len(item) >= 9 else (item[0], *[0]*8)
            is_1st = eq == campeones_grupo.get(letra, "")
            is_2nd = eq == [s[0] for s in posiciones][1] if len(posiciones) > 1 else False
            records.append({
                "": TEAM_EMOJIS.get(eq, "⚽"),
                "Equipo": eq,
                "Conf": TEAM_CONF.get(eq, ""),
                "PJ": pj, "PG": pg, "PE": pe, "PP": pp,
                "GF": gf, "GC": gc, "DG": dg, "Pts": pts,
                "": "🥇" if is_1st else "🥈" if is_2nd else "",
            })
        st.dataframe(pd.DataFrame(records), width='stretch', hide_index=True,
            column_config={"": st.column_config.TextColumn("", width="small")})

        group_matches = [p for p in partidos if f"Grupo {letra}" in p.get("ronda", "")]
        if group_matches:
            with st.expander(f"📋 Partidos del Grupo {letra}"):
                for p in group_matches:
                    st.markdown(match_block(p), unsafe_allow_html=True)

# ========== BUSCADOR DE PARTIDOS ==========
st.subheader("🔍 Buscador de partidos")
all_teams_list = sorted({p["local"] for p in partidos} | {p["visitante"] for p in partidos})
search_team = st.selectbox("Buscar por equipo", ["Todos"] + all_teams_list)
search_ronda = st.selectbox("Filtrar por ronda", ["Todas"] + [r for r in round_order if r in by_round])
filtered = partidos
if search_team != "Todos":
    filtered = [p for p in filtered if p["local"] == search_team or p["visitante"] == search_team]
if search_ronda != "Todas":
    filtered = [p for p in filtered if search_ronda in p.get("ronda", "")]
st.write(f"**{len(filtered)} partidos encontrados**")
for p in filtered:
    st.markdown(match_block(p), unsafe_allow_html=True)

# ========== MAPA DETALLADO POR RONDA ==========
st.subheader("📋 Todas las rondas - Partido por partido")
ronda_sel = st.selectbox("Seleccionar ronda", [""] + [r for r in round_order if r in by_round], index=0)
if ronda_sel and ronda_sel in by_round:
    for p in by_round[ronda_sel]:
        st.markdown(match_block(p), unsafe_allow_html=True)

# ========== PANEL COMPARATIVO ==========
st.subheader("📈 Panel de avance por equipo")
highlighted_set = {campeon, *final, *semis, *cuartos}
all_teams_set = {team for pos_list in grupos_data.values() for team, *_ in pos_list}
chart_data = []
for team in sorted(all_teams_set):
    weight = 0
    if team == campeon: weight = 6
    elif team in final: weight = 5
    elif team in semis: weight = 4
    elif team in cuartos: weight = 3
    elif team in octavos: weight = 2
    elif team in ronda_32: weight = 1
    if weight > 0:
        chart_data.append({"Equipo": team, "Avance": weight})
if chart_data:
    st.bar_chart(pd.DataFrame(chart_data).set_index("Equipo"), width='stretch')

# ========== SIDEBAR ==========
st.sidebar.header("⚙️ Panel de control")
acc = data.get("modelo_accuracy", data.get("modelo_metrics", {}).get("accuracy", "—"))
metrics = data.get("modelo_metrics", {})
st.sidebar.metric("🎯 Precisión", f"{acc:.1%}" if isinstance(acc, (int, float)) else acc)
if isinstance(metrics.get("roc_auc"), (int, float)):
    st.sidebar.metric("📊 ROC-AUC", f"{metrics['roc_auc']:.3f}")
if isinstance(metrics.get("f1"), (int, float)):
    st.sidebar.metric("📈 F1", f"{metrics['f1']:.3f}")
st.sidebar.markdown("---")
st.sidebar.markdown("### Clasificados a 32avos")
st.sidebar.markdown(f"🏆 **Campeones grupo:** {len(campeones_grupo)}")
st.sidebar.markdown(f"🥈 **Segundos:** {len(data.get('segundos_grupo',{}))}")
st.sidebar.markdown(f"⭐ **Mejores 3ros:** {len(mejores_terceros)}")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Recalcular"):
    with st.sidebar.status("Calculando...") as s:
        r = subprocess.run([sys.executable, "predict_world_cup.py"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            s.update(label="✅ Listo", state="complete")
        else:
            s.update(label="❌ Error", state="error")
            st.sidebar.code(r.stdout + r.stderr)
    st.rerun()

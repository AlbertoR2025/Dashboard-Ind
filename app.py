"""
Dashboard P109 V2.1 - ULTRA PREMIUM
Centro P109 | Inventario y Pallets FIFO
Sistema Modular + Efectos Premium
Autor: Alberto Reyes
Fecha: 16.10.2025
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# =============== CONFIGURACIÓN ===============
st.set_page_config(
    page_title="Supply Chain • P109 Ultra",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============== ESTILOS ULTRA PREMIUM ===============
PRIMARY = "#00E5FF"; ACCENT = "#FF6B6B"; SUCCESS = "#2EE59D"; WARNING = "#FFC861"
TEXT = "#E6F1FF"; BG_DARK = "#0E1117"; CARD_BG = "#151A22"; GRID = "#233041"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

.stApp {{
  background: radial-gradient(1200px 600px at 20% -10%, #0B1220 0%, {BG_DARK} 40%, #090C12 100%);
  color: {TEXT};
  font-family: 'Inter', system-ui, sans-serif;
}}

/* ========== TARJETAS KPI ULTRA PREMIUM ========== */
.kpi-card-ultra {{
    position: relative;
    padding: 22px 20px;
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(21,26,34,0.85), rgba(14,17,23,0.95));
    border: 2px solid;
    box-shadow: 
        0 15px 35px rgba(0,0,0,0.5),
        0 0 30px rgba(0,229,255,0.08),
        inset 0 1px 0 rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    overflow: hidden;
    min-height: 150px;
}}

.kpi-card-ultra::before {{
    content: "";
    position: absolute;
    inset: -3px;
    border-radius: 20px;
    background: radial-gradient(circle at 30% 30%, rgba(0,229,255,0.12), transparent 60%);
    filter: blur(18px);
    z-index: 0;
    transition: opacity 0.35s ease;
    opacity: 0.5;
}}

.kpi-card-ultra:hover::before {{ opacity: 1; }}

.kpi-card-ultra:hover {{
    transform: translateY(-6px) scale(1.015);
    box-shadow: 
        0 22px 50px rgba(0,0,0,0.65),
        0 0 50px rgba(0,229,255,0.15),
        inset 0 1px 0 rgba(255,255,255,0.1);
}}

.animated-border {{
    position: absolute;
    inset: -2px;
    border-radius: 18px;
    background: conic-gradient(
        from var(--angle, 0deg),
        var(--border-color),
        transparent 30%,
        transparent 70%,
        var(--border-color)
    );
    opacity: 0;
    transition: opacity 0.35s ease;
    z-index: -1;
    animation: rotate-border 3.5s linear infinite;
}}

.kpi-card-ultra:hover .animated-border {{ opacity: 0.6; }}

@keyframes rotate-border {{
    from {{ --angle: 0deg; transform: rotate(0deg); }}
    to {{ --angle: 360deg; transform: rotate(360deg); }}
}}

.kpi-icon {{
    font-size: 2.8rem;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 12px currentColor);
    animation: icon-float 3s ease-in-out infinite;
}}

@keyframes icon-float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-6px); }}
}}

.kpi-label {{
    color: rgba(230,241,255,0.7);
    font-size: 0.88rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 700;
    margin-bottom: 10px;
}}

.kpi-value {{
    font-size: 2.3rem;
    font-weight: 900;
    line-height: 1.1;
    text-shadow: 0 0 20px rgba(0,229,255,0.4);
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}}

.kpi-delta {{
    font-size: 0.92rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
}}

.delta-up {{ color: {SUCCESS}; text-shadow: 0 0 10px {SUCCESS}66; }}
.delta-down {{ color: {ACCENT}; text-shadow: 0 0 10px {ACCENT}66; }}
.delta-flat {{ color: {WARNING}; text-shadow: 0 0 10px {WARNING}66; }}

/* ========== HEADERS PREMIUM ========== */
.section-header {{
    font-weight: 900;
    font-size: 1.85rem;
    letter-spacing: 1.5px;
    margin: 2rem 0 1.5rem 0;
    padding-left: 18px;
    border-left: 6px solid;
    background: linear-gradient(90deg, rgba(46,229,157,0.12), transparent);
    padding: 14px 0 14px 18px;
    border-radius: 8px;
    color: {TEXT};
    text-shadow: 0 0 18px rgba(46,229,157,0.45);
    position: relative;
    overflow: hidden;
}}

.section-header::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(110deg, transparent 30%, rgba(46,229,157,0.15) 50%, transparent 70%);
    background-size: 200% 100%;
    animation: section-shimmer 3s linear infinite;
}}

@keyframes section-shimmer {{
    0% {{ background-position: -200% 0; }}
    100% {{ background-position: 200% 0; }}
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0F141E 0%, #0A0E14 100%);
    border-right: 1px solid rgba(0,229,255,0.2);
}}

.dataframe {{
    background-color: {BG_DARK} !important;
    color: {TEXT} !important;
    border-radius: 14px;
    font-size: 0.96rem;
}}

thead th {{
    background: linear-gradient(135deg, {CARD_BG}, #0F141C) !important;
    color: {PRIMARY} !important;
    font-weight: 800 !important;
    padding: 12px 14px !important;
    border-bottom: 2px solid {PRIMARY} !important;
    text-align: center !important;
    letter-spacing: 0.7px;
    text-shadow: 0 0 12px {PRIMARY}66;
}}

tbody tr:hover td {{
    background-color: #16213E !important;
    transition: all 0.28s ease;
}}
</style>
""", unsafe_allow_html=True)

# =============== FUNCIONES HELPER ===============
def format_number(num, decimals=0):
    try:
        if decimals == 0:
            return f"{int(num):,}".replace(",", ".")
        return f"{num:,.{decimals}f}".replace(",", ".")
    except:
        return "—"

def render_kpi_ultra(label, value, delta=None, delta_type="neutral", icon="📊", color="#00E5FF"):
    delta_html = ""
    if delta:
        delta_symbols = {"up": "↑", "down": "↓", "neutral": "•"}
        delta_html = f"""<div class='kpi-delta delta-{delta_type}'>
            <span style='font-size:1.1rem;'>{delta_symbols[delta_type]}</span>{delta}
        </div>"""
    
    st.markdown(f"""
    <div class='kpi-card-ultra' style='border-color: {color};'>
        <div class='kpi-icon' style='color:{color};'>{icon}</div>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value' style='
            background: linear-gradient(135deg, {color} 0%, rgba(255,255,255,0.9) 100%);
            -webkit-background-clip: text; background-clip: text; color: transparent;
        '>{value}</div>
        {delta_html}
        <div class='animated-border' style='--border-color: {color};'></div>
    </div>
    """, unsafe_allow_html=True)

def create_donut_ultra(data, names_col, values_col, title="", hole=0.62):
    colors = ["#00E5FF", "#2EE59D", "#FFC861", "#FF6B6B", "#A78BFA", "#64E9FF"]
    
    fig = px.pie(data, names=names_col, values=values_col, hole=hole,
                 color_discrete_sequence=colors, template="plotly_dark")
    
    fig.update_traces(
        textinfo="percent",
        textposition="outside",
        textfont=dict(size=15, family="Inter, sans-serif", color="#E6F1FF", weight=800),
        marker=dict(line=dict(color="#0A0E14", width=4)),
        pull=[0.12, 0.08, 0.04, 0.02, 0, 0],
        rotation=135,
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} u<br>%{percent}<extra></extra>"
    )
    
    fig.update_layout(
        height=480,
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color="#E6F1FF"),
        xaxis=dict(scaleanchor="y", scaleratio=1, visible=False),
        yaxis=dict(visible=False),
        showlegend=True,
        legend=dict(
            orientation="v", x=1.02, y=0.5,
            bgcolor="rgba(15,20,30,0.95)",
            bordercolor="rgba(0,229,255,0.4)",
            borderwidth=2,
            font=dict(size=12, color="#E6F1FF", weight=600)
        )
    )
    
    if title:
        total = data[values_col].sum()
        fig.add_annotation(
            text=f"<b style='font-size:32px; letter-spacing:1.5px; "
                 f"background: linear-gradient(135deg,#00E5FF,#2EE59D,#FFC861); "
                 f"-webkit-background-clip:text; background-clip:text; color:transparent; "
                 f"font-weight:900;'>{total:,.0f}</b><br>"
                 f"<span style='font-size:13px; color:#7B92A8; letter-spacing:0.8px; "
                 f"text-transform:uppercase; font-weight:700;'>{title}</span>",
            x=0.5, y=0.5, xref="paper", yref="paper",
            xanchor="center", yanchor="middle", showarrow=False
        )
    
    return fig

# =============== CARGA DE DATOS ===============
APP_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = APP_DIR / "dataframe_limpio.csv"
ALT_EXCEL = APP_DIR / "Base de Datos.XLSX"

@st.cache_data
def cargar_df(archivo_subido):
    if archivo_subido:
        return pd.read_csv(archivo_subido) if archivo_subido.name.endswith(".csv") else pd.read_excel(archivo_subido)
    if DEFAULT_CSV.exists(): return pd.read_csv(DEFAULT_CSV)
    if ALT_EXCEL.exists(): return pd.read_excel(ALT_EXCEL)
    return pd.DataFrame()

st.sidebar.title("⚙️ Configuración")
archivo = st.sidebar.file_uploader("📁 Subir archivo", type=["csv", "xlsx"])
df = cargar_df(archivo)
if df.empty:
    st.warning("⚠️ No se encontró archivo de datos")
    st.stop()

# Normalización
if "Fecha" in df.columns:
    df["Fecha_dt"] = pd.to_datetime(df["Fecha"], format="%d.%m.%y", errors="coerce")
if "Antiguedad_dias" in df.columns:
    df["Antiguedad_dias"] = pd.to_numeric(df["Antiguedad_dias"], errors="coerce").astype("Int64")

# =============== PARÁMETROS ===============
st.sidebar.markdown("### 📊 Parámetros")
unidades_por_caja = st.sidebar.number_input("Unidades por caja", 1, 10000, 12)
unidades_por_pallet = st.sidebar.number_input("Unidades por pallet", 100, 10000, 4180)
pallets_por_camion = st.sidebar.number_input("Pallets por camión", 1, 40, 28)
umbral_envejec = st.sidebar.slider("Umbral envejecimiento (días)", 15, 180, 90)

# =============== FILTROS ===============
st.sidebar.markdown("### 🔍 Filtros")
centros = sorted(df["Centro"].dropna().unique()) if "Centro" in df.columns else []
sel_centro = st.sidebar.multiselect("Centro", centros, centros[:1] if centros else [])

df_fil = df.copy()
if sel_centro: df_fil = df_fil[df_fil["Centro"].isin(sel_centro)]

from datetime import datetime

# =============== BANNER ULTRA PREMIUM - SOLUCIÓN DEFINITIVA ===============
fecha_actual = datetime.now().strftime('%d.%m.%y')

st.markdown(f"""
<div class="banner-ultra-wrapper">
    <div class="banner-ultra">
        <div class="banner-glow-pulse"></div>
        <div class="banner-shimmer"></div>
        <div class="banner-particles"></div>
        <div class="banner-content-ultra">
            <h1 class="banner-title-ultra">📦 ORIZON PT DASHBOARD ULTRA</h1>
            <p class="banner-subtitle-ultra">Centro P109 • Inventario en Tiempo Real • 
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.banner-ultra-wrapper {
    position: relative;
    margin-bottom: 2.5rem;
}

.banner-ultra {
    position: relative;
    padding: 3rem 2.5rem;
    border-radius: 20px;
    background: linear-gradient(-45deg, #0a1628, #16213e, #0f3460, #1a1a2e);
    background-size: 400% 400%;
    animation: gradient-shift 8s ease infinite;
    border: 2px solid rgba(0, 229, 255, 0.3);
    box-shadow: 
        0 25px 60px rgba(0, 0, 0, 0.7),
        0 0 100px rgba(0, 229, 255, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1),
        inset 0 -1px 0 rgba(0, 0, 0, 0.5);
    overflow: hidden;
}

.banner-glow-pulse {
    position: absolute;
    inset: -5px;
    border-radius: 22px;
    background: 
        radial-gradient(circle at 25% 25%, rgba(0, 229, 255, 0.4), transparent 50%),
        radial-gradient(circle at 75% 75%, rgba(46, 229, 157, 0.3), transparent 50%);
    filter: blur(25px);
    z-index: 0;
    animation: halo-pulse 4s ease-in-out infinite;
}

@keyframes halo-pulse {
    0%, 100% { opacity: 0.5; transform: scale(0.98); }
    50% { opacity: 1; transform: scale(1.08); }
}

.banner-shimmer {
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: linear-gradient(
        110deg,
        transparent 25%,
        rgba(255, 255, 255, 0.3) 45%,
        rgba(0, 229, 255, 0.5) 50%,
        rgba(255, 255, 255, 0.3) 55%,
        transparent 75%
    );
    background-size: 200% 100%;
    animation: shimmer-sweep 3.5s linear infinite;
    mix-blend-mode: screen;
    opacity: 0.7;
    pointer-events: none;
    z-index: 1;
}

@keyframes shimmer-sweep {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.banner-particles {
    position: absolute;
    inset: 0;
    background-image: 
        radial-gradient(2px 2px at 15% 25%, rgba(255, 255, 255, 0.5), transparent),
        radial-gradient(2px 2px at 65% 75%, rgba(0, 229, 255, 0.6), transparent),
        radial-gradient(1px 1px at 45% 45%, rgba(255, 255, 255, 0.4), transparent),
        radial-gradient(1px 1px at 85% 15%, rgba(46, 229, 157, 0.5), transparent),
        radial-gradient(2px 2px at 92% 65%, rgba(255, 255, 255, 0.4), transparent),
        radial-gradient(1px 1px at 28% 88%, rgba(0, 229, 255, 0.5), transparent);
    background-size: 200% 200%;
    background-position: 50% 50%;
    animation: particles-float 12s ease-in-out infinite;
    z-index: 1;
}

@keyframes particles-float {
    0%, 100% { background-position: 0% 0%; opacity: 0.5; }
    50% { background-position: 100% 100%; opacity: 1; }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.banner-content-ultra {
    position: relative;
    z-index: 10;
    text-align: center;
}

.banner-title-ultra {
    margin: 0 0 12px 0;
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #FFFFFF 0%, #00E5FF 35%, #2EE59D 70%, #FFC861 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 35px rgba(0, 229, 255, 0.7));
    animation: title-glow 3s ease-in-out infinite alternate;
    font-family: 'Inter', system-ui, sans-serif;
}

@keyframes title-glow {
    from { filter: drop-shadow(0 0 25px rgba(0, 229, 255, 0.5)) brightness(1); }
    to { filter: drop-shadow(0 0 50px rgba(0, 229, 255, 0.9)) brightness(1.2); }
}

.banner-subtitle-ultra {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: rgba(230, 249, 255, 0.9);
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    letter-spacing: 0.6px;
    font-family: 'Inter', system-ui, sans-serif;
}

@media (max-width: 768px) {
    .banner-ultra {
        padding: 2rem 1.5rem;
    }
    .banner-title-ultra {
        font-size: 2rem;
    }
    .banner-subtitle-ultra {
        font-size: 0.95rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =============== KPIs ULTRA PREMIUM ===============
stock_total = pd.to_numeric(df_fil.get("Stock"), errors="coerce").fillna(0).sum()
cajas_total = int(round(stock_total / unidades_por_caja))
pallet_total = round(stock_total / unidades_por_pallet, 2)
camiones_total = round(pallet_total / pallets_por_camion, 2)

c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1: render_kpi_ultra("Cajas Estimadas", format_number(cajas_total), "+2.1%", "up", "📦", "#00E5FF")
with c2: render_kpi_ultra("Stock Total", format_number(int(stock_total)), "Estable", "neutral", "📊", "#2EE59D")
with c3: render_kpi_ultra("Total Pallets", format_number(pallet_total), "-0.5%", "down", "🚛", "#FFC861")
with c4: render_kpi_ultra("Camiones", format_number(camiones_total), "Plan", "neutral", "🚚", "#FF6B6B")

# =============== GRÁFICO TOP MATERIALES CON GRADIENTE ===============
st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='section-header' style='border-left-color:#00E5FF;'>
    <span style='position:relative; z-index:1;'>📦 Top Materiales por Stock</span>
</div>
""", unsafe_allow_html=True)

if all(c in df_fil.columns for c in ["Material", "Stock"]):
    topN = st.slider("🎯 Top-N Materiales", 5, 30, 12, key="slider_top")
    mat = df_fil.groupby("Material")["Stock"].sum().reset_index().sort_values("Stock", ascending=False).head(topN)
    mat["Cajas"] = (mat["Stock"] / unidades_por_caja).round(1)
    
    fig_top = px.bar(mat, x="Material", y="Cajas", text="Cajas",
                     color="Cajas",
                     color_continuous_scale=["#0E3E52", "#1582A1", "#00C2FF", "#64E9FF", "#00E5FF"],
                     template="plotly_dark", height=450)
    
    fig_top.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside",
        textfont=dict(size=14, color="#E6F1FF", weight=800),
        cliponaxis=False,
        marker=dict(line=dict(color="#0E1117", width=2), opacity=0.95),
        hovertemplate="<b>%{x}</b><br>Stock: %{customdata[0]:,.0f} u<br>Cajas: %{y:.0f}<extra></extra>",
        customdata=mat[["Stock"]].values
    )
    
    fig_top.update_layout(
        margin=dict(t=40, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title=dict(text="<b>Material</b>", font=dict(size=13, color="#00E5FF")),
            gridcolor="#233041", tickangle=-35,
            tickfont=dict(size=11, color="#A7B9C9")
        ),
        yaxis=dict(
            title=dict(text="<b>Cajas</b>", font=dict(size=13, color="#00E5FF")),
            gridcolor="#233041",
            tickfont=dict(size=11, color="#A7B9C9")
        )
    )
    
    st.plotly_chart(fig_top, use_container_width=True, key="top_premium")

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============== DONUTS PERFECTOS — SOLUCIÓN DEFINITIVA ===============
import plotly.express as px

# =============== VISUAL ANALYTICS — SUNBURST PREMIUM ===============
st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='font-weight: 900; font-size: 1.85rem; letter-spacing: 1.5px;
    margin: 2rem 0 1.5rem 0; padding: 14px 0 14px 18px; border-radius: 8px;
    border-left: 6px solid #2EE59D; color: #E6F1FF;
    background: linear-gradient(90deg, rgba(46, 229, 157, 0.12), transparent);
    text-shadow: 0 0 18px rgba(46, 229, 157, 0.45);'>
    <span>📊 Visual Analytics</span>
</div>
""", unsafe_allow_html=True)

if all(c in df_fil.columns for c in ["Material", "Stock"]):
    
    col1, col2 = st.columns(2, gap="large")
    
    # ========== SUNBURST 1: CAJAS ==========
    with col1:
        st.markdown("""
        <div style='font-weight:800; font-size:1.25rem; margin-bottom:16px; color:#00E5FF; 
                    padding-left:12px; border-left:4px solid #00E5FF;'>
            📦 Cajas por Material (Sunburst)
        </div>
        """, unsafe_allow_html=True)
        
        tmp = df_fil.copy()
        tmp["Cajas"] = (tmp["Stock"] / max(1, unidades_por_caja)).astype(int)
        tmp["Categoria"] = "Total"  # Raíz para jerarquía
        top8_cajas = tmp.groupby("Material")["Cajas"].sum().reset_index().sort_values("Cajas", ascending=False).head(8)
        top8_cajas["Categoria"] = "Total"
        
        fig1 = px.sunburst(
            top8_cajas,
            path=["Categoria", "Material"],
            values="Cajas",
            color="Cajas",
            color_continuous_scale=["#0E3E52", "#00C2FF", "#00E5FF", "#2EE59D"],
            template="plotly_dark",
            height=480
        )
        
        fig1.update_traces(
            textinfo="label+value+percent parent",
            textfont=dict(size=13, color="#FFFFFF", family="Inter, sans-serif"),
            marker=dict(line=dict(color="#0A0E14", width=3)),
            hovertemplate='<b>%{label}</b><br>Cajas: %{value:,.0f}<br>%{percentParent}<extra></extra>'
        )
        
        fig1.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig1, use_container_width=True, key="sunburst_cajas")
    
    # ========== SUNBURST 2: UNIDADES ==========
    with col2:
        st.markdown("""
        <div style='font-weight:800; font-size:1.25rem; margin-bottom:16px; color:#2EE59D; 
                    padding-left:12px; border-left:4px solid #2EE59D;'>
            📊 Unidades por Material (Sunburst)
        </div>
        """, unsafe_allow_html=True)
        
        top8_units = df_fil.groupby("Material")["Stock"].sum().reset_index().sort_values("Stock", ascending=False).head(8)
        top8_units["Categoria"] = "Total"
        
        fig2 = px.sunburst(
            top8_units,
            path=["Categoria", "Material"],
            values="Stock",
            color="Stock",
            color_continuous_scale=["#0E4D3D", "#26A17B", "#2EE59D", "#88F8D1"],
            template="plotly_dark",
            height=480
        )
        
        fig2.update_traces(
            textinfo="label+value+percent parent",
            textfont=dict(size=13, color="#FFFFFF", family="Inter, sans-serif"),
            marker=dict(line=dict(color="#0A0E14", width=3)),
            hovertemplate='<b>%{label}</b><br>Stock: %{value:,.0f}<br>%{percentParent}<extra></extra>'
        )
        
        fig2.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig2, use_container_width=True, key="sunburst_units")

else:
    st.warning("⚠️ Faltan columnas necesarias")

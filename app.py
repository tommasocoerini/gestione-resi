import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS (ESTETICA E SEPARAZIONE LOGICA)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    .stAlert { background-color: #FBBD00 !important; border: 2px solid #0B1D45; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    
    /* Titoli e Testi Sidebar */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* RIQUADRO DI SEPARAZIONE BLOCCHI */
    .sidebar-block {
        border: 1px solid #0B1D45;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: rgba(11, 29, 69, 0.05); /* Un leggerissimo velo blu */
    }

    /* DROPDOWN MENU */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* RADIO BUTTONS (Cerca per...) */
    div[data-testid="stWidgetLabel"] { color: #0B1D45 !important; }
    
    /* TABELLA */
    .stDataFrame { background-color: #FFFFFF !important; border-radius: 10px; }
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td { color: #0B1D45 !important; }

    /* BOTTONE DOWNLOAD */
    .stDownloadButton button { 
        background-color: #FBBD00 !important; 
        color: #0B1D45 !important; 
        border: 2px solid #0B1D45 !important; 
        font-weight: bold; width: 100%;
    }
    .stDownloadButton button:hover { background-color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATI DI TEST
@st.cache_data
def load_data():
    data = {
        'Sales Representative': ['Mario Rossi', 'Mario Rossi', 'Luigi Bianchi', 'Luigi Bianchi'],
        'Codice Cliente': ['A105', 'B200', 'C001', 'A050'],
        'Nome Cliente': ['Zeta Tyres', 'Alpha Gomme', 'Beta Ruote', 'Delta Service'],
        'SKU': ['PNEU-001', 'PNEU-002', 'PNEU-003', 'PNEU-004'],
        'Qta_Iniziale': [10, 20, 15, 30]
    }
    return pd.DataFrame(data)

df = load_data()

# --- INTERFACCIA ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Benvenuto nel portale TEP. Seleziona il cliente per codice o ragione sociale.")

# --- SIDEBAR CON BLOCCHI SEPARATI ---

# BLOCCO 1: SALES REPRESENTATIVE
st.sidebar.markdown('<div class="sidebar-block">', unsafe_allow_html=True)
st.sidebar.subheader("👤 Sales Representative")
sales_reps = sorted(df['Sales Representative'].unique())
sales_rep = st.sidebar.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# BLOCCO 2: RICERCA CLIENTE
st.sidebar.markdown('<div class="sidebar-block">', unsafe_allow_html=True)
st.sidebar.subheader("🔍 Ricerca Cliente")

df_rep = df[df['Sales Representative'] == sales_rep]
nomi_lista = sorted(df_rep['Nome Cliente'].unique())
codici_lista = sorted(df_rep['Codice Cliente'].unique())

scelta_tipo = st.sidebar.radio("Modalità di ricerca:", ["Ragione Sociale", "Codice Cliente"])

if scelta_tipo == "Ragione Sociale":
    cliente_nome = st.sidebar.selectbox("Nome Cliente", nomi_lista)
    cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]
else:
    cliente_codice = st.sidebar.selectbox("Codice Cliente", codici_lista)
    cliente_nome = df_rep[df_rep['Codice Cliente'] == cliente_codice]['Nome Cliente'].iloc[0]
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# FILTRO DATI FINALI
df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice]

# --- VISUALIZZAZIONE ---
st.subheader(f"📋 Riepilogo Stock: {cliente_nome}")
st.write(f"**ID Cliente:** {cliente_codice} |

import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS AVANZATO
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    .stAlert { background-color: #FBBD00 !important; border: 2px solid #0B1D45; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    
    /* BOX CONTENITORI NELLA SIDEBAR */
    .sidebar-box {
        border: 2px solid #0B1D45 !important;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0px;
        background-color: transparent;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* FIX RADIO BUTTON (IL PALLINO) */
    /* Cerchio esterno */
    div[data-testid="stMarkdownContainer"] [role="radiogroup"] div div {
        border-color: #0B1D45 !important;
    }
    /* Pallino interno quando selezionato */
    div[role="radio"][aria-checked="true"] > div:first-child {
        background-color: #0B1D45 !important;
        border-color: #0B1D45 !important;
    }

    /* DROPDOWN MENU */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* TABELLA E ALLINEAMENTO */
    .stDataFrame { background-color: #FFFFFF !important; border-radius: 10px; }
    
    /* Centratura intestazioni e celle per le colonne quantità */
    [data-testid="stTable"] th, [data-testid="stDataFrame"] th {
        text-align: center !important;
        font-weight: bold !important;
        color: #0B1D45 !important;
    }

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
        'Size & Type': ['205/55 R16 Summer', '225/45 R17 Winter', '195/65 R15 AllSeason', '245/40 R18 Sport'],
        'Quantità Iniziale': [10, 20, 15, 30],
        'Quantità restituibile': [7, 14, 0, 21]
    }
    return pd.DataFrame(data)

df = load_data()

# --- INTERFACCIA SIDEBAR CON BOX ---

# CONTENITORE 1: SALES REPRESENTATIVE
with st.sidebar:
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.subheader("👤 Sales Representative")
    sales_reps = sorted(df['Sales Representative'].unique())
    sales_rep = st.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # CONTENITORE 2: RICERCA CLIENTE
    st.markdown('<div class="sidebar-box">', unsafe_allow_

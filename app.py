import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS PERSONALIZZATO
st.markdown("""
    <style>
    /* --- SFONDO E TESTI GENERALI --- */
    .main {
        background-color: #0B1D45; /* Sfondo Blu scuro */
    }
    
    /* --- TITOLO PRINCIPALE --- */
    h1 {
        color: #FBBD00 !important; /* Giallo */
        font-weight: bold;
    }

    /* --- BOX BENVENUTO --- */
    .stAlert {
        background-color: #FBBD00; 
        border: 2px solid #FBBD00;
    }
    .stAlert p {
        color: #0B1D45 !important; 
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* --- BARRA LATERALE (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #FBBD00; /* Sfondo Giallo */
    }
    
    [data-testid="stSidebar"] label {
        color: #0B1D45 !important; /* Testo Blu */
        font-weight: bold;
    }

    /* --- FIX BORDI E VISIBILITÀ DROPDOWN --- */
    /* Contenitore del menu a tendina */
    div[data-baseweb="select"] {
        border: 2px solid #0B1D45 !important; /* Bordo Blu scuro per staccare dal giallo */
        border-radius: 8px !important;
        background-color: #FBBD00 !important;
    }

    /* Testo dentro il menu selezionato */
    div[data-baseweb="select"] > div {
        color: #0B1D45 !important; 
    }

    /* Effetto Hover sul menu */
    div[data-baseweb="select"]:hover {
        border-color: #000000 !important; /* Diventa nero al passaggio del mouse */
    }

    /* --- TABELLE (Migliorata leggibilità) --- */
    .stDataFrame, [data-testid="stTable"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }
    
    /* Forza il testo della tabella a Blu per leggerlo su fondo bianco */
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td {
        color: #0B1D45 !important;
    }

    /* --- BOTTONE DOWNLOAD --- */
    .stDownloadButton button {
        background-color: #FBBD00 !important;
        color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: 0.3s;
    }
    .stDownloadButton button:hover {
        background-color: #0B1D45 !important;
        color: #FBBD00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA APPLICATIVA ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Benvenuto nel portale TEP. Seleziona l'agente e il cliente per calcolare lo stock restituibile.")

# Funzione dati (Esempio)
@st.cache_data
def load_data():
    data = {
        'Agente': ['Mario Rossi', 'Luigi Bianchi'],
        'Cliente': ['Gommista A', 'Gommista B'],
        'SKU': ['PNEU-001', 'PNEU-002'],
        'Qta_Iniziale': [10, 20]
    }
    return pd.DataFrame(data)

df = load_data()

# Filtri
agente = st.sidebar.selectbox("👤 Seleziona Agente", df['Agente'].unique())
cliente = st.sidebar.selectbox("🏢 Seleziona Cliente", df[df['Agente']==agente]['Cliente'].unique())

# Visualizzazione
st.subheader(f"Analisi per: {cliente}")
st.dataframe(df[df['Cliente']==cliente], use_container_width=True)

st.markdown("---")
st.download_button("📥 Scarica Modulo Reso TEP", "dati finti", "reso.csv")

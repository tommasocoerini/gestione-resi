import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS DEFINITIVO (FIX CONTRASTO E VISIBILITÀ)
st.markdown("""
    <style>
    /* Sfondo Blu Notte */
    .main { background-color: #0B1D45 !important; }
    
    /* Titolo Giallo */
    h1 { color: #FBBD00 !important; font-weight: bold; }
    
    /* Box Benvenuto: Sfondo Giallo, Testo Blu */
    .stAlert { background-color: #FBBD00 !important; border: 2px solid #FBBD00; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR GIALLA */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    
    /* Forza TUTTI i testi della sidebar (label, radio, scritte) in Blu Scuro */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* Testo dei pulsanti Radio (Cerca per...) in Blu */
    [data-testid="stWidgetLabel"] p { color: #0B1D45 !important; }
    div[data-testid="stMarkdownContainer"] p { color: #0B1D45 !important; }

    /* MENU A TENDINA (Dropdown) */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        border-radius: 8px !important; 
        background-color: #0B1D45 !important; /* Sfondo Blu scuro del box */
    }
    
    /* Testo selezionato dentro il Dropdown: Giallo su fondo Blu */
    div[data-baseweb="select"] div { 
        color: #FBBD00 !important; 
    }

    /* TABELLA: Sfondo Bianco, Testo Blu */
    .stDataFrame, [data-testid="stTable"] { 
        background-color: #FFFFFF !important; 
        border-radius: 10px; 
    }
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th { 
        color: #0B1D45 !important; 
    }

    /* BOTTONE DOWNLOAD */
    .stDownloadButton button { 
        background-color: #FBBD00 !important; 
        color: #0B1D45 !important; 
        border: 2px solid #0B1D45 !important; 
        font-weight: bold; 
        width: 100%;
    }
    .stDownloadButton button:hover { 
        background-color: #FFFFFF !important; 
        color: #0B1D45 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATI DI TEST (Popolamento)
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

# SIDEBAR
st.sidebar.subheader("👤 Sales Representative")
sales_reps = sorted(df['Sales Representative'].unique())
sales_rep = st.sidebar.selectbox("Scegli il tuo nome", sales_reps, label_visibility="collapsed")

df_rep = df[df['Sales Representative'] == sales_rep]

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Ricerca Cliente")

nomi_lista = sorted(df_rep['Nome Cliente'].unique())
codici_lista = sorted(df_rep['Codice Cliente'].unique())

# Selettore tipo ricerca
scelta_tipo = st.sidebar.radio("Cerca per:", ["Ragione Sociale", "Codice Cliente"])

if scelta_tipo == "Ragione Sociale":
    cliente_nome = st.sidebar.selectbox("

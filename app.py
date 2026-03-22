import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS PERSONALIZZATO (I TUOI COLORI ORIGINALI)
st.markdown("""
    <style>
    /* Sfondo Blu Notte che avevi scelto */
    .main { background-color: #0B1D45; }
    
    /* Titoli in Giallo */
    h1 { color: #FBBD00 !important; font-weight: bold; }

    /* Box Info Giallo con testo Blu */
    .stAlert { background-color: #FBBD00; border: 2px solid #FBBD00; }
    .stAlert p { color: #0B1D45 !important; font-weight: 500; }

    /* Sidebar Gialla con scritte Blu */
    [data-testid="stSidebar"] { background-color: #FBBD00; }
    [data-testid="stSidebar"] label { color: #0B1D45 !important; font-weight: bold; }

    /* Bordi dei menu a tendina per vederli sul fondo giallo */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        border-radius: 8px !important; 
        background-color: #FBBD00 !important; 
    }
    div[data-baseweb="select"] > div { color: #0B1D45 !important; }

    /* Tabella bianca con testo blu per non affaticare la vista */
    .stDataFrame, [data-testid="stTable"] { background-color: #FFFFFF; border-radius: 10px; }
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td { color: #0B1D45 !important; }

    /* Bottone Download */
    .stDownloadButton button { 
        background-color: #FBBD00 !important; 
        color: #0B1D45 !important; 
        border: 2px solid #0B1D45 !important; 
        font-weight: bold; 
        width: 100%; 
    }
    .stDownloadButton button:hover { background-color: #0B1D45 !important; color: #FBBD00 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARICAMENTO DATI (Simulazione con i nuovi campi)
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

# --- LOGICA DI NAVIGAZIONE ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Benvenuto nel portale TEP. Seleziona il cliente per codice o ragione sociale.")

# A. Selezione Sales Representative (Ordinato A-Z)
sales_reps = sorted(df['Sales Representative'].unique())
sales_rep = st.sidebar.selectbox("👤 Sales Representative", sales_reps)

# Filtriamo i dati per il Sales Rep scelto
df_rep = df[df['Sales Representative'] == sales_rep]

# Liste ordinate per i menu
nomi_ordinati = sorted(df_rep['Nome Cliente'].unique())
codici_ordinati = sorted(df_rep['Codice Cliente'].unique())

st.sidebar.markdown("---")
st.sidebar.write("🔍 **Cerca Cliente**")

# Sincronizzazione dei due menù
if 'nome_sel' not in st.session_state:
    st.session_state.nome_sel = nomi_ordinati[0]
if 'codice_sel' not in st.session_state:
    st.session_state.codice_sel = df_rep[df_rep['Nome Cliente'] == nomi_ordinati[0]]['Codice Cliente'].iloc[0]

def on_name_change():
    sel = st.session_state.nome_sel
    st.session_state.codice_sel = df_rep[df_rep['Nome Cliente'] == sel]['Codice Cliente'].iloc[0]

def on_code_change():
    sel = st.session_state.codice_sel
    st.session_state.nome_sel = df_rep[df_rep['Codice Cliente'] == sel]['Nome Cliente'].iloc

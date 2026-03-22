import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS PERSONALIZZATO (RIPRISTINO E FIX COLORI)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    
    /* Box Benvenuto */
    .stAlert { background-color: #FBBD00 !important; border: 2px solid #FBBD00; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    [data-testid="stSidebar"] label { color: #0B1D45 !important; font-weight: bold; font-size: 1.1rem; }

    /* DROPDOWN MENU (I selettori) */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        border-radius: 8px !important; 
        background-color: #0B1D45 !important; /* Sfondo Blu scuro dentro il menu */
    }
    
    /* TESTO DENTRO IL MENU (Quello che non si leggeva) */
    div[data-baseweb="select"] div { 
        color: #FBBD00 !important; /* Testo GIALLO su fondo blu */
    }

    /* TABELLE */
    .stDataFrame, [data-testid="stTable"] { 
        background-color: #FFFFFF !important; 
        border-radius: 10px; 
        padding: 10px;
    }
    
    /* Forza testo nero/blu nella tabella per leggibilità */
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
        margin-top: 20px;
    }
    .stDownloadButton button:hover { 
        background-color: #FFFFFF !important; 
        color: #0B1D45 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATI DI ESEMPIO (Assicuriamoci che siano popolati)
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

# SIDEBAR - SALES REP
sales_reps = sorted(df['Sales Representative'].unique())
sales_rep = st.sidebar.selectbox("👤 Sales Representative", sales_reps)

# Filtro immediato per il Sales Rep scelto
df_rep = df[df['Sales Representative'] == sales_rep]

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Ricerca Cliente")

# Liste per i menu
nomi_lista = sorted(df_rep['Nome Cliente'].unique())
codici_lista = sorted(df_rep['Codice Cliente'].unique())

# LOGICA SEMPLIFICATA DI SELEZIONE (senza session_state complesso che bloccava tutto)
scelta_tipo = st.sidebar.radio("Cerca per:", ["Ragione Sociale", "Codice Cliente"], horizontal=True)

if scelta_tipo == "Ragione Sociale":
    cliente_nome = st.sidebar.selectbox("Seleziona Nome", nomi_lista)
    # Troviamo il codice corrispondente
    cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]
else:
    cliente_codice = st.sidebar.selectbox("Seleziona Codice", codici_lista)
    # Troviamo il nome corrispondente
    cliente_nome = df_rep[df_rep['Codice Cliente'] == cliente_codice]['Nome Cliente'].iloc[0]

# FILTRO FINALE DEI DATI
df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice]

# --- VISUALIZZAZIONE ---
st.subheader(f"Dati per: {cliente_nome} (Cod: {cliente_codice})")

if not df_display.empty:
    st.dataframe(df_display[['SKU', 'Qta_Iniziale']], use_container_width=True)
    
    st.markdown("---")
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Scarica Modulo Reso per {cliente_nome}",
        data=csv,
        file_name=f"TEP_{cliente_codice}.csv",
        mime='text/csv'
    )
else:
    st.warning("Nessun dato trovato per questo cliente.")

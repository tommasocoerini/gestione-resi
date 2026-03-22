import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS (BOX CONTENITORI E STILE TABELLA)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    .stAlert { background-color: #FBBD00 !important; border: 2px solid #0B1D45; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    
    /* Box Contenitori nella Sidebar */
    .sidebar-box {
        border: 2px solid #0B1D45;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        background-color: rgba(11, 29, 69, 0.03);
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* DROPDOWN MENU */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* TABELLA */
    .stDataFrame { background-color: #FFFFFF !important; border-radius: 10px; }
    
    /* Stile per il grassetto nella colonna Quantità Restituibile */
    /* Nota: Streamlit renderizza i dataframe in modo standard, 
       useremo lo styling di Pandas per il grassetto */

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

# 3. DATI DI TEST (Aggiornati con le nuove colonne)
@st.cache_data
def load_data():
    data = {
        'Sales Representative': ['Mario Rossi', 'Mario Rossi', 'Luigi Bianchi', 'Luigi Bianchi'],
        'Codice Cliente': ['A105', 'B200', 'C001', 'A050'],
        'Nome Cliente': ['Zeta Tyres', 'Alpha Gomme', 'Beta Ruote', 'Delta Service'],
        'Size & Type': ['205/55 R16 Summer', '225/45 R17 Winter', '195/65 R15 AllSeason', '245/40 R18 Sport'],
        'Quantità Iniziale': [10, 20, 15, 30],
        'Quantità restituibile': [7, 14, 0, 21] # Valori di test che calcoleremo poi
    }
    return pd.DataFrame(data)

df = load_data()

# --- INTERFACCIA SIDEBAR ---

# BLOCCO 1: SALES REPRESENTATIVE
st.sidebar.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
st.sidebar.subheader("👤 Sales Representative")
sales_reps = sorted(df['Sales Representative'].unique())
sales_rep = st.sidebar.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# BLOCCO 2: RICERCA CLIENTE
st.sidebar.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
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
df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

# --- VISUALIZZAZIONE ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Benvenuto nel portale TEP. Gestione stock e resi stagionali.")

st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice Cliente:** {cliente_codice} | **Sales Representative:** {sales_rep}")

# Funzione per applicare il grassetto alla colonna specifica
def bold_column(val):
    return 'font-weight: bold'

if not df_display.empty:
    # Selezione e rinomina colonne per la visualizzazione
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']]
    
    # Applichiamo lo stile (Grassetto sulla colonna Quantità restituibile)
    styled_df = df_view.style.applymap(bold_column, subset=['Quantità restituibile'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(label=f"📥 SCARICA MODULO RESO PER {cliente_nome}", data=csv, file_name=f"TEP_{cliente_codice}.csv", mime='text/csv')

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

# 3. DATI DI TEST

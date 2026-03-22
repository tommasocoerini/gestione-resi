import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. CSS
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #0B1D45 !important;
        font-weight: bold !important;
    }

    /* Etichette sidebar */
    .sidebar-label {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        margin-top: 4px;
    }
    .sidebar-label-text {
        color: #0B1D45;
        font-weight: 900;
        font-size: 1rem;
    }

    /* --- RADIO come PILL BUTTONS --- */
    /* Contenitore orizzontale */
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
    }
    /* Nasconde il pallino radio originale */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    /* Ogni opzione radio diventa una pill */
    div[data-testid="stRadio"] label {
        background-color: #FBBD00 !important;
        color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
        font-weight: 900 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.08em !important;
        padding: 7px 22px !important;
        border-radius: 999px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        margin: 0 !important;
    }
    /* Pill ATTIVA: blu pieno + testo giallo */
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #0B1D45 !important;
        color: #FBBD00 !important;
        border: 2px solid #0B1D45 !important;
    }
    /* Hover sulla pill inattiva */
    div[data-testid="stRadio"] label:hover {
        background-color: #e6a800 !important;
    }
    /* Nasconde l'eventuale testo del label radio (lo sostituiamo con il testo della scelta) */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    /* DROPDOWN MENU */
    div[data-baseweb="select"] {
        border: 2px solid #0B1D45 !important;
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* BOTTONE DOWNLOAD */
    .stDownloadButton button {
        background-color: #FBBD00 !important;
        color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
        font-weight: bold; width: 100%;
    }

    /* --- TABELLA CUSTOM --- */
    .tep-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    .tep-table thead tr { background-color: #FBBD00; }
    .tep-table thead th {
        color: #0B1D45 !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 12px 16px;
        text-align: center;
    }
    .tep-table thead th:first-child,
    .tep-table tbody td:first-child {
        text-align: left;
        padding-left: 20px;
        width: 55%;
    }
    .tep-table thead th:not(:first-child),
    .tep-table tbody td:not(:first-child) {
        text-align: center;
        width: 22.5%;
    }
    .tep-table tbody tr:nth-child(odd)  { background-color: #112259; }
    .tep-table tbody tr:nth-child(even) { background-color: #0D1D48; }
    .tep-table tbody tr:hover {
        background-color: #1a3070;
        transition: background-color 0.2s ease;
    }
    .tep-table tbody td {
        color: #E8EDF8 !important;
        padding: 11px 16px;
        border-top: 1px solid rgba(255,255,255,0.07);
        vertical-align: middle;
    }
    .tep-table tbody td:last-child {
        color: #FBBD00 !important;
        font-weight: 800;
        font-size: 1.05rem;
    }
    .badge-zero {
        display: inline-block;
        background-color: rgba(255,255,255,0.1);
        color: #8899BB !important;
        font-weight: 600 !important;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.9rem;
    }
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

# --- SIDEBAR ---
with st.sidebar:

    # -- Sales Rep --
    st.markdown(
        '<div class="sidebar-label">'
        '<span style="font-size:1.4rem;">👤</span>'
        '<span class="sidebar-label-text">Seleziona Sales Representative</span>'
        '</div>',
        unsafe_allow_html=True
    )
    sales_reps = sorted(df['Sales Representative'].unique())
    sales_rep = st.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")

    st.markdown("---")

    # -- Ricerca Cliente --
    st.markdown(
        '<div class="sidebar-label">'
        '<span style="font-size:1.4rem;">🔍</span>'
        '<span class="sidebar-label-text">Seleziona Cliente</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # st.radio mascherato da pill buttons via CSS
    modalita = st.radio(
        "Modalità ricerca",
        options=["NOME", "CODICE"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    usa_codice = (modalita == "CODICE")

    df_rep = df[df['Sales Representative'] == sales_rep]

    if usa_codice:
        codici_lista = sorted(df_rep['Codice Cliente'].unique())
        cliente_codice = st.selectbox("Seleziona Codice Cliente", codici_lista)
        cliente_nome = df_rep[df_rep['Codice Cliente'] == cliente_codice]['Nome Cliente'].iloc[0]
    else:
        nomi_lista = sorted(df_rep['Nome Cliente'].unique())
        cliente_nome = st.selectbox("Seleziona Ragione Sociale", nomi_lista)
        cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]

# --- MAIN ---
st.title("🛞 TEP: Tire Exchange Program")

st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice:** {cliente_codice} | **Sales Rep:** {sales_rep}")

df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']].copy()

    rows = []
    for _, row in df_view.iterrows():
        qty_rest = row['Quantità restituibile']
        qty_cell = '<span class="badge-zero">0</span>' if qty_rest == 0 else str(int(qty_rest))
        rows.append(f"<tr><td>{row['Size & Type']}</td><td>{int(row['Quantità Iniziale'])}</td><td>{qty_cell}</td></tr>")

    rows_html = "".join(rows)
    table_html = (
        '<table class="tep-table">'
        "<thead><tr>"
        "<th>Pneumatico</th><th>Qtà Iniziale</th><th>Qtà Restituibile</th>"
        "</tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
    )

    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 SCARICA MODULO RESO TEP", data=csv, file_name=f"TEP_{cliente_codice}.csv")

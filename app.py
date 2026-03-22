import streamlit as st
import pandas as pd
import io

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. CSS PERSONALIZZATO (Stile Claude + Tabelle)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #0B1D45 !important;
        font-weight: bold !important;
    }
    .sidebar-label {
        display: flex; align-items: center;
        gap: 10px; margin-bottom: 8px; margin-top: 4px;
    }
    .sidebar-label-text { color: #0B1D45; font-weight: 900; font-size: 1rem; }
    div[data-baseweb="select"] {
        border: 2px solid #0B1D45 !important;
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }
    .stDownloadButton button {
        background-color: #FBBD00 !important;
        color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
        font-weight: bold; width: 100%;
        padding: 12px; border-radius: 8px;
    }
    .tep-table {
        width: 100%; border-collapse: separate; border-spacing: 0;
        border-radius: 12px; overflow: hidden;
        font-family: 'Segoe UI', sans-serif; font-size: 0.95rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4); margin-bottom: 25px;
    }
    .tep-table thead tr { background-color: #FBBD00; }
    .tep-table thead th {
        color: #0B1D45 !important; font-weight: 800;
        text-transform: uppercase; padding: 12px 16px; text-align: center;
    }
    .tep-table thead th:first-child, .tep-table tbody td:first-child {
        text-align: left; padding-left: 20px; width: 55%;
    }
    .tep-table thead th:not(:first-child), .tep-table tbody td:not(:first-child) {
        text-align: center; width: 22.5%;
    }
    .tep-table tbody tr:nth-child(odd)  { background-color: #112259; }
    .tep-table tbody tr:nth-child(even) { background-color: #0D1D48; }
    .tep-table tbody td {
        color: #E8EDF8 !important; padding: 11px 16px;
        border-top: 1px solid rgba(255,255,255,0.07); vertical-align: middle;
    }
    .tep-table tbody td:last-child { color: #FBBD00 !important; font-weight: 800; font-size: 1.05rem; }
    .badge-zero {
        display: inline-block; background-color: rgba(255,255,255,0.1);
        color: #8899BB !important; font-weight: 600 !important;
        padding: 2px 10px; border-radius: 20px; font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. FUNZIONE EXCEL PROFESSIONALE
def to_excel(df, codice, ragione_sociale):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # startrow=3 e header=False per evitare la doppia riga di titoli alla riga 4
        df.to_excel(writer, index=False, sheet_name='Reso_TEP', startrow=3, header=False)
        
        workbook  = writer.book
        worksheet = writer.sheets['Reso_TEP']

        # Formati
        fmt_grigio_bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        fmt_header = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        fmt_normal = workbook.add_format({'border': 1})
        
        # Intestazioni fisse (Righe 1 e 2)
        worksheet.write('A1', 'CODICE CLIENTE', fmt_grigio_bold)
        worksheet.write('B1', codice, fmt_normal) # B1 Normale
        
        worksheet.write('A2', 'RAGIONE SOCIALE', fmt_grigio_bold)
        worksheet.write('B2', ragione_sociale, fmt_normal) # B2 Normale (come richiesto)

        # Formattazione riga 3 (Manuale, per avere controllo totale)
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(2, col_num, value, fmt_header)

        # Auto-adattamento colonne
        for i, col in enumerate(df.columns):
            # Calcolo larghezza basato sui dati o sul titolo
            max_val = df[col].astype(str).map(len).max() if not df.empty else 0
            max_len = max(max_val, len(col)) + 5
            worksheet.set_column(i, i, max_len)

    return output.getvalue()

# 4. DATI DI TEST
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

df_all = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-label"><span style="font-size:1.4rem;">👤</span><span class="sidebar-label-text">Sales Representative</span></div>', unsafe_allow_html=True)
    sales_reps = sorted(df_all['Sales Representative'].unique())
    sales_rep = st.selectbox("Scegli", sales_reps, label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sidebar-label"><span style="font-size:1.4rem;">🔍</span><span class="sidebar-label-text">Cliente</span></div>', unsafe_allow_html=True)
    
    df_rep = df_all[df_all['Sales Representative'] == sales_rep]
    nomi_lista = sorted(df_rep['Nome Cliente'].unique())
    cliente_nome = st.selectbox("Scegli Cliente", nomi_lista, label_visibility="collapsed")
    
    cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]
    df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

# --- MAIN CONTENT ---
st.title("🛞 TEP: Tire Exchange Program")
st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice:** {cliente_codice} | **Sales Rep:** {sales_rep}")

if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']].copy()

    # Tabella HTML (Visione App)
    rows = []
    for _, row in df_view.iterrows():
        qty_rest = row['Quantità restituibile']
        qty_cell = '<span class="badge-zero">0</span>' if qty_rest == 0 else str(int(qty_rest))
        rows.append(f"<tr><td>{row['Size & Type']}</td><td>{int(row['Quantità Iniziale'])}</td><td>{qty_cell}</td></tr>")

    rows_html = "".join(rows)
    table_html = f'<table class="tep-table"><thead><tr><th>Pneumatico</th><th>Qtà Iniziale</th><th>Qtà Restituibile</th></tr></thead><tbody>{rows_html}</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download Excel con Nomenclatura Dinamica
    excel_file = to_excel(df_view, cliente_codice, cliente_nome)
    
    # Generazione nome file pulito (senza spazi eccessivi o caratteri strani)
    nome_file_download = f"Restituzione_TEP_{cliente_codice}_{cliente_nome.replace(' ', '_')}.xlsx"
    
    st.download_button(
        label="📥 SCARICA MODULO DI RESO",
        data=excel_file,
        file_name=nome_file_download,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

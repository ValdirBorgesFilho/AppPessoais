import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
from datetime import datetime

# 1. Configuração de página para ocupar toda a largura
st.set_page_config(layout="wide", page_title="Scanner NF-e Pro")

# 2. CSS para expandir a altura, centralizar e criar a borda de enquadramento
st.markdown(
    """
    <style>
    /* Estica o container da câmera */
    iframe {
        height: 500px !important; 
        width: 100% !important;
        border: 4px solid #00FF00 !important; /* Borda verde de scanner */
        border-radius: 15px;
        box-shadow: 0px 0px 15px rgba(0, 255, 0, 0.3);
    }
    /* Estilização dos botões para facilitar o toque no celular */
    .stButton > button {
        width: 100%;
        height: 50px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📲 Scanner de NF-e")
st.write("Enquadre o QR Code na área verde abaixo:")

# Inicializa a lista de links
if 'links' not in st.session_state:
    st.session_state.links = []

# 3. O componente do Scanner
# Ele tentará abrir a câmera traseira automaticamente
link_bruto = qrcode_scanner(key='scanner_nfe')

if link_bruto:
    # Limpeza de caracteres estranhos (Regex)
    match = re.search(r'https?://[^\s]+', link_bruto)
    if match:
        link_limpo = match.group(0)
        # Evita duplicados na lista
        if link_limpo not in st.session_state.links:
            st.session_state.links.append(link_limpo)
            st.toast(f"Nota {len(st.session_state.links)} adicionada!", icon="✅")
        else:
            st.toast("Nota já está na lista!", icon="⚠️")

# 4. Exibição e Gerenciamento
if st.session_state.links:
    st.divider()
    st.subheader(f"Notas na Fila: {len(st.session_state.links)}")
    
    # Tabela simplificada para celular
    df = pd.DataFrame(st.session_state.links, columns=["Link da Nota"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Botões de Ação
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"links_nfe_{datetime.now().strftime('%d%m_%H%M')}.csv",
            mime="text/csv",
        )
    with col2:
        if st.button("🗑️ Limpar Lista"):
            st.session_state.links = []
            st.rerun()

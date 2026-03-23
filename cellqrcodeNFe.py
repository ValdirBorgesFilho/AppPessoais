import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
from datetime import datetime

# 1. Mudamos para 'centered' (padrão) para evitar o esmagamento horizontal no mobile
st.set_page_config(layout="centered", page_title="Scanner NF-e Pro")

# 2. CSS agressivo para forçar a altura do container e do iframe
st.markdown(
    """
    <style>
    /* Alvo direto no container que o Streamlit cria para componentes externos */
    [data-testid="stHtmlBlock"] iframe {
        height: 600px !important; 
        min-height: 600px !important;
        width: 100% !important;
        border: 5px solid #00FF00 !important;
        border-radius: 20px;
    }
    
    /* Garante que o bloco pai não limite a altura */
    .element-container, .stMarkdown {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📲 Scanner Automático")
st.write("Aproxime o QR Code da moldura verde:")

if 'links' not in st.session_state:
    st.session_state.links = []

# 3. Scanner - A detecção é automática, ele adiciona assim que reconhece
link_bruto = qrcode_scanner(key='scanner_nfe')

if link_bruto:
    match = re.search(r'https?://[^\s]+', link_bruto)
    if match:
        link_limpo = match.group(0)
        if link_limpo not in st.session_state.links:
            st.session_state.links.append(link_limpo)
            st.toast(f"Capturado! Total: {len(st.session_state.links)}", icon="✅")

# 4. Área de Gerenciamento (aparece apenas se houver notas)
if st.session_state.links:
    st.divider()
    df = pd.DataFrame(st.session_state.links, columns=["Link da Nota"])
    
    # Botão de download grande para facilitar o clique
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 BAIXAR LISTA (CSV)",
        data=csv,
        file_name=f"notas_{datetime.now().strftime('%d%m_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    if st.button("🗑️ Limpar Lista"):
        st.session_state.links = []
        st.rerun()
        
    st.dataframe(df, use_container_width=True)

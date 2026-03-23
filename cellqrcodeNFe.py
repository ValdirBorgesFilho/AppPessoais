import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
from datetime import datetime

# 1. Configuração padrão (melhor para proporção de câmera no celular)
st.set_page_config(layout="centered", page_title="Scanner NF-e")

# 2. CSS para forçar a altura da janela da câmera no navegador do celular
st.markdown(
    """
    <style>
    /* Alvo no iframe do scanner para dar altura e borda */
    iframe {
        height: 650px !important; 
        min-height: 650px !important;
        width: 100% !important;
        border: 4px solid #00FF00 !important;
        border-radius: 15px;
    }
    /* Estilo para a tabela e botões */
    div.stButton > button {
        width: 100%;
        height: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📲 Scanner de NF-e")
st.write("Aponte a câmera. A leitura é automática.")

if 'links' not in st.session_state:
    st.session_state.links = []

# 3. O Componente de Scanner (Aquele que você confirmou que funciona)
link_bruto = qrcode_scanner(key='scanner_nfe_v2')

if link_bruto:
    # Limpeza do link via Regex
    match = re.search(r'https?://[^\s]+', link_bruto)
    if match:
        link_limpo = match.group(0)
        if link_limpo not in st.session_state.links:
            st.session_state.links.append(link_limpo)
            st.toast(f"Nota {len(st.session_state.links)} capturada!", icon="✅")

# 4. Exibição dos resultados e Download
if st.session_state.links:
    st.divider()
    st.subheader(f"Lista de Notas ({len(st.session_state.links)})")
    
    df = pd.DataFrame(st.session_state.links, columns=["Link da Nota"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 BAIXAR CSV PARA O PC",
        data=csv,
        file_name=f"notas_{datetime.now().strftime('%d%m_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("🗑️ Limpar Lista"):
        st.session_state.links = []
        st.rerun()

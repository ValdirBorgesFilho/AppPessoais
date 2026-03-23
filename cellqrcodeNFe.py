import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
from datetime import datetime

# 1. Configuração da página (Centrado é melhor para manter a proporção da câmera)
st.set_page_config(layout="centered", page_title="Scanner NF-e Pro")

# 2. CSS para criar a moldura externa e forçar a altura do Iframe
st.markdown(
    """
    <style>
    /* Estica o container onde o scanner mora */
    iframe {
        height: 700px !important; 
        min-height: 700px !important;
        width: 100% !important;
        border: 5px solid #00FF00 !important; /* Moldura verde */
        border-radius: 20px;
        box-shadow: 0px 0px 20px rgba(0, 255, 0, 0.2);
    }
    /* Melhora os botões para toque no celular */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📲 Scanner Automático")
st.write("Aponte para o QR Code. O quadrado interno agora deve ocupar toda a área verde.")

# Inicializa a lista de links na sessão
if 'links_nfe' not in st.session_state:
    st.session_state.links_nfe = []

# 3. O Componente de Scanner com ajuste de estilo INTERNO
# O segredo aqui é o video_style e o container_style estarem com a mesma altura do CSS
link_bruto = qrcode_scanner(
    key='scanner_nfe_final',
    video_style={
        'height': '700px', 
        'width': '100%', 
        'object-fit': 'cover' # 'cover' preenche tudo, 'contain' mantém a proporção original
    },
    container_style={
        'height': '700px',
        'width': '100%'
    }
)

# 4. Lógica de captura e limpeza
if link_bruto:
    # Regex para pegar apenas a URL limpa (ignora lixo antes do http)
    match = re.search(r'https?://[^\s]+', link_bruto)
    if match:
        link_limpo = match.group(0)
        if link_limpo not in st.session_state.links_nfe:
            st.session_state.links_nfe.append(link_limpo)
            st.toast(f"Nota {len(st.session_state.links_nfe)} capturada!", icon="✅")
        else:
            st.toast("Essa nota já foi lida.", icon="⚠️")

# 5. Exibição e Botões de Ação
if st.session_state.links_nfe:
    st.divider()
    st.subheader(f"Notas na Fila: {len(st.session_state.links_nfe)}")
    
    df = pd.DataFrame(st.session_state.links_nfe, columns=["Link da Nota"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 BAIXAR CSV",
            data=csv,
            file_name=f"notas_{datetime.now().strftime('%d%m_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        if st.button("🗑️ Limpar Lista"):
            st.session_state.links_nfe = []
            st.rerun()

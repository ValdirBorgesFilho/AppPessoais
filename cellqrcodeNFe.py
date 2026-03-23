import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
from datetime import datetime

# 1. Configuração da página
st.set_page_config(layout="centered", page_title="Scanner NF-e Pro")

# 2. CSS para criar a moldura externa e forçar a altura do Iframe
st.markdown(
    """
    <style>
    /* Estica o container onde o scanner mora */
    iframe {
        height: 500px !important; 
        min-height: 500px !important;
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
st.write("Aponte para o QR Code dentro da área verde.")

# Inicializa a lista de links na sessão
if 'links_nfe' not in st.session_state:
    st.session_state.links_nfe = []

# 3. O Componente de Scanner com Proteção contra Erros
# Removidos estilos internos complexos que podem causar o erro na linha 44
try:
    # Captura o retorno do scanner
    link_bruto = qrcode_scanner(key='scanner_nfe_v2')
except Exception as e:
    st.error(f"Erro ao carregar a câmera: {e}")
    link_bruto = None

# 4. Lógica de captura com validação de tipo (O SEGREDO PARA NÃO QUEBRAR)
if link_bruto and isinstance(link_bruto, str):
    
    # Regex para pegar apenas a URL limpa (ignora lixo antes do http)
    match = re.search(r'https?://[^\s]+', link_bruto)
    
    if match:
        link_limpo = match.group(0)
        
        # Só adiciona se o link for novo na sessão atual
        if link_limpo not in st.session_state.links_nfe:
            st.session_state.links_nfe.append(link_limpo)
            st.toast(f"Nota {len(st.session_state.links_nfe)} capturada!", icon="✅")
            # Força o recarregamento para limpar o buffer do scanner após leitura
            st.rerun()
        else:
            # Aviso temporário caso já tenha lido
            st.toast("Essa nota já foi lida.", icon="⚠️")

# 5. Exibição e Botões de Ação
if st.session_state.links_nfe:
    st.divider()
    st.subheader(f"Notas na Fila: {len(st.session_state.links_nfe)}")
    
    # Cria o DataFrame para exibição e download
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
else:
    st.info("Nenhuma nota lida ainda. Aponte a câmera para um QR Code de NF-e.")

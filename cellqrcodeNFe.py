import streamlit as st
from streamlit_camera_input_live import camera_input_live
import cv2
import numpy as np
import pandas as pd
import re
from datetime import datetime

# 1. Configuração da página
st.set_page_config(layout="centered", page_title="Scanner NF-e Live")

# 2. CSS para melhorar o visual da câmera no celular
st.markdown(
    """
    <style>
    /* Estiliza o container da câmera */
    [data-testid="stCameraInputLive"] {
        border: 5px solid #00FF00;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0px 0px 15px rgba(0, 255, 0, 0.3);
    }
    .stButton > button {
        width: 100%;
        height: 55px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📲 Scanner NF-e Live")
st.write("Aponte para o QR Code. A leitura é instantânea.")

# Inicializa a lista de links na sessão
if 'links_nfe' not in st.session_state:
    st.session_state.links_nfe = []

# 3. O Componente de Câmera Live
# debounce=100 significa que ele processa um frame a cada 100ms (rápido!)
imagem_capturada = camera_input_live(debounce=100)

if imagem_capturada:
    # Converter a imagem capturada (bytes) para o formato OpenCV
    file_bytes = np.asarray(bytearray(imagem_capturada.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Detector de QR Code do OpenCV
    detector = cv2.QRCodeDetector()
    link_bruto, pontos, _ = detector.detectAndDecode(opencv_image)

    # 4. Lógica de Processamento se encontrar um QR Code
    if link_bruto:
        # Regex para extrair apenas a URL limpa
        match = re.search(r'https?://[^\s]+', link_bruto)
        
        if match:
            link_limpo = match.group(0)
            
            if link_limpo not in st.session_state.links_nfe:
                st.session_state.links_nfe.append(link_limpo)
                st.toast(f"Nota {len(st.session_state.links_nfe)} capturada!", icon="✅")
                # Não usamos rerun aqui para não interromper o fluxo da câmera live
            else:
                st.toast("Nota já registrada.", icon="⚠️")

# 5. Exibição da Tabela e Download
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
else:
    st.info("Aguardando QR Code...")

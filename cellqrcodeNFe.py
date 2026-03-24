import streamlit as st
import cv2
import numpy as np
import pandas as pd
import re
from datetime import datetime

# 1. Configuração da página
st.set_page_config(layout="centered", page_title="Scanner NF-e Estável")

st.title("📲 Scanner NF-e")
st.write("Tire uma foto nítida do QR Code da nota.")

# Inicializa a lista na sessão
if 'links_nfe' not in st.session_state:
    st.session_state.links_nfe = []

# 2. Componente Nativo (Não depende de bibliotecas extras instáveis)
foto = st.camera_input("Aponte e clique em 'Take Photo'")

if foto:
    # Converter foto para formato OpenCV
    file_bytes = np.asarray(bytearray(foto.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Detector de QR Code
    detector = cv2.QRCodeDetector()
    link_bruto, _, _ = detector.detectAndDecode(opencv_image)

    if link_bruto:
        # Regex para extrair a URL
        match = re.search(r'https?://[^\s]+', link_bruto)
        if match:
            link_limpo = match.group(0)
            if link_limpo not in st.session_state.links_nfe:
                st.session_state.links_nfe.append(link_limpo)
                st.success(f"Nota capturada com sucesso!", icon="✅")
            else:
                st.warning("Esta nota já foi lida.", icon="⚠️")
    else:
        st.error("Não foi possível ler o QR Code. Tente aproximar mais ou melhorar a luz.")

# 3. Exibição e Download
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

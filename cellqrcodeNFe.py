import streamlit as st
import cv2
import numpy as np
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="Scanner NF-e Estável", page_icon="📷")

st.title("📷 Scanner de NF-e")
st.write("Tire uma foto nítida do QR Code da nota.")

if 'links' not in st.session_state:
    st.session_state.links = []

# 1. Componente nativo (usa a câmera do sistema com foco automático)
imagem_camera = st.camera_input("Alinhe o QR Code e clique em 'Take Photo'")

if imagem_camera is not None:
    # Converter imagem para formato OpenCV
    bytes_data = imagem_camera.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Detector de QR Code do OpenCV
    detector = cv2.QRCodeDetector()
    link_detectado, bbox, _ = detector.detectAndDecode(cv2_img)
    
    if link_detectado:
        # Limpeza do link (Regex)
        match = re.search(r'https?://[^\s]+', link_detectado)
        if match:
            link_limpo = match.group(0)
            if link_limpo not in st.session_state.links:
                st.session_state.links.append(link_limpo)
                st.success(f"Nota capturada! Total: {len(st.session_state.links)}")
            else:
                st.info("Esta nota já foi adicionada.")
    else:
        st.error("Não foi possível ler o QR Code. Tente aproximar mais ou melhorar a iluminação.")

# 2. Gerenciamento dos Links
if st.session_state.links:
    st.divider()
    df = pd.DataFrame(st.session_state.links, columns=["Link da Nota"])
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Lista (CSV)",
        data=csv,
        file_name=f"notas_{datetime.now().strftime('%d%m_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    if st.button("🗑️ Limpar Lista"):
        st.session_state.links = []
        st.rerun()

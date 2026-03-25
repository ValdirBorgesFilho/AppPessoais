import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Scanner de QR Code Contínuo")

# Inicializa o armazenamento no session state se não existir
if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Configuração da câmera - st.camera_input abre o digitalizador nativo do celular
img_file = st.camera_input("Aponte para o QR Code")

if img_file is not None:
    # Converte o arquivo da câmera para formato OpenCV
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Detetor de QR Code do OpenCV
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    if data:
        if data not in st.session_state['scanned_codes']:
            st.session_state['scanned_codes'].append(data)
            st.success(f"Lido: {data}")
    else:
        st.warning("QR Code não detectado. Tente novamente.")

# Exibe os códigos armazenados
st.subheader("Códigos Lidos")
for code in st.session_state['scanned_codes']:
    st.write(f"- {code}")

# Botão para limpar a lista
if st.button("Limpar Lista"):
    st.session_state['scanned_codes'] = []

import streamlit as st
import cv2
import numpy as np
import zxingcpp  # O nome correto oficial do módulo C++

st.title("Scanner Industrial - QR Code Denso")

if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Captura de alta resolução (Evita o borrão do navegador)
img_file = st.file_uploader("Capture a imagem em alta resolução", type=["jpg", "jpeg", "png"])

if img_file is not None:
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Tratamento de binarização adaptativa para destacar os mini-quadrados da NF-e
    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Varredura agressiva na imagem tratada em alta definição
    # O ZXing-C++ varre todas as extremidades e cantos da imagem
    results = zxingcpp.read_barcodes(processed_img)

    if results:
        for result in results:
            dados = result.text
            if dados not in st.session_state['scanned_codes']:
                st.session_state['scanned_codes'].append(dados)
                st.success(f"NF-e / Código Lido: {dados}")
    else:
        st.error("Falha na leitura. Se o código for muito denso, posicione a câmera um pouco mais perto.")

# Exibição dos dados salvos
st.subheader("Lista de Códigos")
for code in st.session_state['scanned_codes']:
    st.write(f"- {code}")

# Botão para resetar a lista
if st.button("Limpar Lista"):
    st.session_state['scanned_codes'] = []
    st.rerun()

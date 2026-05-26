import streamlit as st
import cv2
import numpy as np
import zxing  # O nome correto para importação é 'zxing'

st.title("Scanner Industrial - QR Code Denso")

if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Captura em alta definição para não borrar códigos densos
img_file = st.file_uploader("Capture a imagem em alta resolução", type=["jpg", "jpeg", "png"])

if img_file is not None:
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Tratamento de imagem para realçar os quadradinhos do QR Code denso
    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Salva temporariamente em memória para a engine C++ ler com eficiência
    _, encoded_img = cv2.imencode('.png', processed_img)
    img_bytes = encoded_img.tobytes()

    # Inicializa a engine estável do ZXing
    reader = zxing.BarCodeReader()
    
    # Executa a leitura forçando a busca por QR Codes complexos
    result = reader.decode_in_memory(img_bytes)

    if result and result.parsed:
        dados = result.parsed
        if dados not in st.session_state['scanned_codes']:
            st.session_state['scanned_codes'].append(dados)
            st.success(f"NF-e / Código Lido: {dados}")
    else:
        st.error("Falha na leitura. Se o código for muito denso, aproxime um pouco mais para dar resolução física aos pixels.")

# Exibição
st.subheader("Lista de Códigos")
for code in st.session_state['scanned_codes']:
    st.write(f"- {code}")

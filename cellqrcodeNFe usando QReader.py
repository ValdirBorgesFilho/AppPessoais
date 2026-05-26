import streamlit as st
import cv2
import numpy as np
import zxing  # Engine C++ atualizada de altíssimo desempenho

st.title("Scanner Industrial - QR Code Denso")

if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Forçamos o uso do uploader em alta definição
img_file = st.file_uploader("Capture a imagem em alta resolução", type=["jpg", "jpeg", "png"])

if img_file is not None:
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # --- TRATAMENTO INDUSTRIAL PARA CÓDIGOS DENSOS ---
    # Convertemos para escala de cinza
    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    
    # Aplica limiarização adaptativa para remover borrões e sombras (essencial para NF-e)
    # Isso reconstrói as bordas dos quadradinhos minúsculos do QR Code denso
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Configura o leitor ZXing-C++ para varredura agressiva de área total
    options = zxing_cpp.ReaderOptions()
    options.set_formats(zxing_cpp.BarcodeFormat.QRCode)
    options.set_try_harder(True)  # Força o algoritmo a procurar nos cantos mais difíceis
    options.set_try_rotate(True)  # Lê mesmo se o celular estiver torto

    # Executa a leitura na imagem tratada em alta definição
    results = zxing_cpp.read_barcodes(processed_img, options)

    if results:
        for result in results:
            dados = result.text
            if dados not in st.session_state['scanned_codes']:
                st.session_state['scanned_codes'].append(dados)
                st.success(f"NF-e / Código Lido: {dados}")
    else:
        st.error("Falha na leitura. Se o código for muito denso, aproxime um pouco mais para dar resolução física aos pixels.")

# Exibição
st.subheader("Lista de Códigos")
for code in st.session_state['scanned_codes']:
    st.write(f"- {code}")

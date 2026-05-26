import streamlit as st
import cv2
import numpy as np
import zxingcpp

st.title("Scanner Industrial - QR Code Denso")

if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Captura de alta resolução pelo aplicativo nativo do celular
img_file = st.file_uploader("Capture a imagem em alta resolução", type=["jpg", "jpeg", "png"])

if img_file is not None:
    # 1. Converte o arquivo recebido para o formato OpenCV
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # 2. Configura a busca agressiva diretamente na biblioteca C++
    # Isso ativa algoritmos internos de alta resiliência para códigos distantes ou densos
    options = zxingcpp.ReaderOptions()
    options.formats = zxingcpp.BarcodeFormat.QRCode  # Foco estrito em QR Codes
    options.try_harder = True   # Varre cada pixel milimetricamente (essencial para NF-e)
    options.try_rotate = True   # Consegue ler o código em qualquer ângulo ou de ponta-cabeça
    options.try_invert = True   # Lê mesmo se as cores estiverem invertidas

    # 3. Executa a leitura na imagem pura de alta definição
    results = zxingcpp.read_barcodes(cv2_img, options)

    if results:
        for result in results:
            dados = result.text
            if dados not in st.session_state['scanned_codes']:
                st.session_state['scanned_codes'].append(dados)
                st.success(f"Código Detectado: {dados}")
    else:
        st.error("Nenhum QR Code detectado. Certifique-se de que a foto não ficou tremida.")

# Exibição dos dados salvos
st.subheader("Lista de Códigos")
if st.session_state['scanned_codes']:
    for code in st.session_state['scanned_codes']:
        st.write(f"- {code}")
else:
    st.caption("Nenhum código na lista.")

# Botão para resetar a lista
if st.button("Limpar Lista"):
    st.session_state['scanned_codes'] = []
    st.rerun()

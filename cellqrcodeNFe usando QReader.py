import streamlit as st
import cv2
import numpy as np

st.title("Scanner de QR Code Contínuo")

# Inicializa o armazenamento no session state se não existir
if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Inicializa o detector do WeChat no session state para não recarregar a cada foto
if 'wechat_detector' not in st.session_state:
    try:
        # Tenta usar o modelo robusto do WeChat QR
        st.session_state['wechat_detector'] = cv2.wechat_qrcode_WeChatQRCode()
    except AttributeError:
        # Alerta caso o pacote opencv-contrib-python não esteja instalado
        st.error("Erro: Instale o 'opencv-contrib-python' para ativar a varredura de área total.")
        st.session_state['wechat_detector'] = None

# Configuração da câmera nativa
img_file = st.camera_input("Aponte para o QR Code (Pode ser de longe ou no canto)")

if img_file is not None and st.session_state['wechat_detector'] is not None:
    # Converte o arquivo da câmera para formato OpenCV
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Executa a varredura em 100% da área da imagem usando IA do WeChat
    detector = st.session_state['wechat_detector']
    dados, pontos = detector.detectAndDecode(cv2_img)

    # O WeChat retorna uma tupla de strings. Se leu algo, a primeira posição terá conteúdo.
    if dados and dados[0]:
        codigo_detectado = dados[0]
        
        if codigo_detectado not in st.session_state['scanned_codes']:
            st.session_state['scanned_codes'].append(codigo_detectado)
            st.success(f"Lido com sucesso: {codigo_detectado}")
        else:
            st.info(f"Este código já foi lido: {codigo_detectado}")
    else:
        st.warning("Nenhum QR Code detectado nesta área. Tente mudar o ângulo.")

# Exibe os códigos armazenados
st.subheader("Códigos Lidos")
if st.session_state['scanned_codes']:
    for code in st.session_state['scanned_codes']:
        st.write(f"- {code}")
else:
    st.caption("Nenhum código na lista.")

# Botão para limpar a lista
if st.button("Limpar Lista"):
    st.session_state['scanned_codes'] = []
    st.rerun()

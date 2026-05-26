import streamlit as st
import cv2
import numpy as np
import zxingcpp

st.title("Scanner Industrial - Resolução Otimizada")

if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

# Captura de arquivo em alta resolução
img_file = st.file_uploader("Capture a imagem da NF-e", type=["jpg", "jpeg", "png"])

if img_file is not None:
    # 1. Converte o arquivo recebido para o formato OpenCV
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # 2. REDIMENSIONAMENTO INTELIGENTE (Gargalo de Alta Resolução)
    # Se a imagem for gigantesca, reduzimos proporcionalmente para largura de 1920px (Full HD)
    # Isso junta os pixels espalhados e reconstrói o padrão denso do QR Code
    alt, larg = cv2_img.shape[:2]
    if larg > 1920:
        nova_larg = 1920
        nova_alt = int((alt / larg) * nova_larg)
        cv2_img = cv2.resize(cv2_img, (nova_larg, nova_alt), interpolation=cv2.INTER_AREA)

    # 3. CONFIGURAÇÃO AGRESSIVA DO MOTOR C++
    options = zxingcpp.ReaderOptions()
    options.formats = zxingcpp.BarcodeFormat.QRCode
    options.try_harder = True      # Ativa busca microscópica de quinas
    options.try_rotate = True      # Detecta mesmo se a foto estiver inclinada
    options.try_downscale = True    # Força sub-amostragem interna se necessário
    options.is_pure = False         # Avisa o motor que o código NÃO está sozinho no fundo branco

    # 4. Executa a leitura na imagem otimizada
    results = zxingcpp.read_barcodes(cv2_img, options)

    if results:
        for result in results:
            dados = result.text
            if dados not in st.session_state['scanned_codes']:
                st.session_state['scanned_codes'].append(dados)
                st.success(f"Código Identificado: {dados}")
    else:
        st.error("Código não reconhecido. Certifique-se de que o QR Code ocupa pelo menos 20% do enquadramento da foto.")

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

import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
import re
import time
from datetime import datetime

st.set_page_config(layout="centered", page_title="Scanner NF-e Pro")

# CSS Ajustado: Removemos o excesso de bordas no iframe que atrapalha o clique no mobile
st.markdown("""
    <style>
    iframe {
        height: 450px !important; 
        width: 100% !important;
        border: 4px solid #00FF00 !important;
        border-radius: 15px;
    }
    .stApp { background-color: #111; }
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Scanner NF-e")

if 'links_nfe' not in st.session_state:
    st.session_state.links_nfe = []
if 'last_qr' not in st.session_state:
    st.session_state.last_qr = None

# 3. Scanner com chave dinâmica para forçar reset após leitura
scanner_key = f"scanner_{len(st.session_state.links_nfe)}"
link_bruto = qrcode_scanner(key=scanner_key)

# 4. Lógica de Captura Refinada
if link_bruto:
    # Limpeza profunda da string (remove espaços e caracteres especiais de controle)
    link_limpo_bruto = str(link_bruto).strip()
    
    # Busca apenas a URL (padrão de NF-e geralmente contém 'nfe' ou 'fazenda')
    match = re.search(r'https?://[^\s|]+', link_limpo_bruto)
    
    if match:
        link_final = match.group(0)
        
        # Evita duplicidade imediata e processamento repetido do mesmo frame
        if link_final != st.session_state.last_qr:
            if link_final not in st.session_state.links_nfe:
                st.session_state.links_nfe.append(link_final)
                st.session_state.last_qr = link_final
                st.toast(f"Nota {len(st.session_state.links_nfe)} capturada!", icon="✅")
                
                # Delay crucial para o usuário ver o feedback antes do refresh
                time.sleep(0.5) 
                st.rerun()
            else:
                st.warning("Esta nota já está na lista!")
                time.sleep(1)
                st.rerun()

# 5. Interface de Resultados
if st.session_state.links_nfe:
    st.subheader(f"📋 Notas na Fila: {len(st.session_state.links_nfe)}")
    df = pd.DataFrame(st.session_state.links_nfe, columns=["URL da Nota"])
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV", csv, "notas.csv", "text/csv", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.links_nfe = []
            st.session_state.last_qr = None
            st.rerun()
else:
    st.info("Aguardando leitura de QR Code...")

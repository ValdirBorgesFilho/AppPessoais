import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Scanner NF-e", page_icon="📲")

st.title("📲 Scanner de NF-e")
st.write("Aponte para o QR Code da nota. O link aparecerá na lista abaixo.")

# Inicializa a lista se não existir
if 'lista_links' not in st.session_state:
    st.session_state.lista_links = []

# O componente de scanner (solicita câmera automaticamente no celular)
# Nota: Use uma 'key' para evitar que o componente reinicie a cada leitura
link_detectado = qrcode_scanner(key='leitor_nfe')

if link_detectado:
    # Verifica se o link já foi lido para evitar duplicados
    if link_detectado not in st.session_state.lista_links:
        st.session_state.lista_links.append(link_detectado)
        st.toast(f"Nota {len(st.session_state.lista_links)} lida!", icon="✅")
    else:
        st.toast("Essa nota já está na lista", icon="⚠️")

# Exibição dos resultados
if st.session_state.lista_links:
    st.divider()
    st.subheader(f"Notas Scaneadas: {len(st.session_state.lista_links)}")
    
    # Criar DataFrame para exibição e download
    df = pd.DataFrame(st.session_state.lista_links, columns=["Link da Nota"])
    st.table(df) # 'table' é melhor para visualizar no celular que 'dataframe'

    # Preparar o arquivo para baixar no PC depois
    csv = df.to_csv(index=False).encode('utf-8')
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"links_nfe_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    with col2:
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.lista_links = []
            st.rerun()

st.caption("Dica: Ao terminar, baixe o CSV, abra no seu PC e use os links para salvar os HTMLs na pasta do nosso script de extração.")

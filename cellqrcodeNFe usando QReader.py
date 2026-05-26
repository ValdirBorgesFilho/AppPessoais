import streamlit as st

st.title("Scanner Sincronizado - Xiaomi Nativo")

# Inicializa o armazenamento no session state se não existir
if 'scanned_codes' not in st.session_state:
    st.session_state['scanned_codes'] = []

st.info("💡 Como usar com máxima eficiência:\n"
        "1. Abra a câmera nativa ou o app 'Scanner' do seu Xiaomi.\n"
        "2. Foque no QR Code denso e clique no botão de 'Copiar Conteúdo'.\n"
        "3. Volte aqui e cole o resultado no campo abaixo.")

# Campo de texto para colar o conteúdo gerado pelo celular
conteudo_copiado = st.text_input("Cole o código copiado aqui (Pressione Enter):", key="qr_input")

# Se o usuário colou algo
if conteudo_copiado:
    # Limpa espaços em branco nas pontas
    codigo_limpo = conteudo_copiado.strip()
    
    if codigo_limpo:
        if codigo_limpo not in st.session_state['scanned_codes']:
            st.session_state['scanned_codes'].append(codigo_limpo)
            st.success(f"Adicionado com sucesso: {codigo_limpo[:30]}...")
        else:
            st.warning("Este código já foi adicionado anteriormente.")
        
        # Truque para limpar o campo de digitação automaticamente após a inserção
        st.session_state.qr_input = ""
        st.rerun()

# Exibe os códigos armazenados
st.subheader("Códigos Acumulados")
if st.session_state['scanned_codes']:
    for code in st.session_state['scanned_codes']:
        st.write(f"- `{code}`")
else:
    st.caption("Nenhum código na lista.")

# Botão para limpar a lista
if st.button("Limpar Lista"):
    st.session_state['scanned_codes'] = []
    st.rerun()

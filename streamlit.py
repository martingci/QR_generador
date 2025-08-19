import streamlit as st
import qr_code_creator as maker
import io

st.logo("logo.png", size="large")


st.title("Generador QR Sindicato")

link = st.text_input("Ingrese URL")
create = st.button("Crear QR", type="primary")
if (create == 1) and link != "":
    with st.spinner("Creando código QR..."):
        # Crea el código QR
        qr = maker.create_qrcode(link, "qr_code", "logo.png")
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        st.image(qr, caption=f'Código QR de "' + link+'"')

    st.success("Código QR creado exitosamente!")
    st.download_button(label="Descargar imagen", data=buf.getvalue(), file_name="qr_code.png")

    

    
    






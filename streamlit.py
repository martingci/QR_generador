import streamlit as st
import qr_code_creator as maker
import io

st.title("Generador QR Sindicato")

link = st.text_input("Ingrese URL")
create = st.button("Crear QR")
if (create == 1) and link != "":
    qr = maker.create_qrcode(link, "qr_code", "logo.png")
    st.image(qr, caption=f'Código QR de "' + link+'"')
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    st.download_button(label="Descargar imagen", data=buf.getvalue(), file_name="qr_code.png")
    
    






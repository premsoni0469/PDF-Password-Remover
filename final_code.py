import streamlit as st
import PyPDF2
from io import BytesIO

st.title("🔐 PDF Password Remover")

uploaded_file = st.file_uploader("Upload Encrypted PDF", type=["pdf"])
password = st.text_input("Enter PDF Password", type="password")

if uploaded_file and password:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 0:
                st.error("Incorrect password.")
                st.stop()

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_pdf = BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)

        st.success("✅ Password removed successfully.")
        decrypted_file_name = uploaded_file.name
        st.download_button("📥 Download Decrypted PDF", output_pdf, file_name=decrypted_file_name)

    except Exception as e:
        st.error(f"Error: {e}")
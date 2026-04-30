

import streamlit as st
from pdf2docx import Converter
import os
import streamlit as st




import streamlit as st

def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color:#f69966;
            color: white !important;
            border: 2px solid mediumslateblue !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_color()

#st.title("   ")
st.title("📄 PDF to Word Converter by SIRI")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    pdf_path = "uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF uploaded successfully!")

    if st.button("Convert to DOCX"):
        docx_path = "converted.docx"

        try:
            # Convert PDF to DOCX
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            st.success("Conversion completed!")
            st.write("Successfully converted by  :blue[SIRI] ")

            # Provide download button
             # Provide download button
            with open(docx_path, "rb") as file:
                st.download_button(
                    label="📥 Download DOCX",
                    data=file,
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        except Exception as e:
            st.error(f"Error: {e}")

    # Cleanup (optional)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
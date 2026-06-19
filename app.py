import streamlit as st
import tempfile
import subprocess
import os

st.set_page_config(page_title="JS to PPT Converter", layout="wide")

st.title("JavaScript → PPTX")

code = st.text_area(
    "Paste PptxGenJS code",
    height=500
)

uploaded = st.file_uploader(
    "Upload JS file",
    type=["js"]
)

if uploaded:
    code = uploaded.read().decode()

if st.button("Generate PPTX"):

    if not code.strip():
        st.error("Please provide JavaScript code")
        st.stop()

    with tempfile.TemporaryDirectory() as tmp:

        js_file = os.path.join(tmp, "input.js")
        ppt_file = os.path.join(tmp, "output.pptx")

        with open(js_file, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            [
                "node",
                "converter.js",
                js_file,
                ppt_file
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            st.error(result.stderr)

        elif os.path.exists(ppt_file):

            with open(ppt_file, "rb") as f:
                st.download_button(
                    "Download PPTX",
                    data=f.read(),
                    file_name="presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        else:
            st.error("PPT generation failed")

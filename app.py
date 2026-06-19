import streamlit as st
import subprocess
import tempfile
from pathlib import Path
import re

st.set_page_config(
    page_title="JavaScript → PowerPoint Converter",
    layout="wide"
)

st.title("JavaScript → PowerPoint Converter")

uploaded_file = st.file_uploader(
    "Upload JavaScript File",
    type=["js"]
)

js_code = ""

if uploaded_file:
    js_code = uploaded_file.read().decode("utf-8")

js_code = st.text_area(
    "JavaScript Code",
    value=js_code,
    height=500
)

filename = st.text_input(
    "Output Filename",
    value="presentation"
)

if st.button("🚀 Generate PPTX"):

    if not js_code.strip():
        st.error("Please enter JavaScript code.")
        st.stop()

    if not Path("converter.js").exists():
        st.error("converter.js not found.")
        st.stop()

    with tempfile.TemporaryDirectory() as tmp:

        js_file = Path(tmp) / "input.js"
        ppt_file = Path(tmp) / "output.pptx"

        # --------------------------------------------------
        # Auto-clean uploaded JS
        # Removes ONLY:
        # 1. const pptxgen = require("pptxgenjs");
        # 2. const pres = new pptxgen();
        # 3. pres.writeFile(...)
        # --------------------------------------------------

        cleaned_code = js_code

        cleaned_code = re.sub(
            r'const\s+pptxgen\s*=\s*require\s*\(\s*[\'"]pptxgenjs[\'"]\s*\)\s*;?',
            '',
            cleaned_code
        )

        cleaned_code = re.sub(
            r'const\s+pres\s*=\s*new\s+pptxgen\s*\(\s*\)\s*;?',
            'const pres = pptx;',
            cleaned_code
        )

        cleaned_code = re.sub(
            r'pres\.writeFile\s*\([\s\S]*$',
            '',
            cleaned_code
        )

        js_file.write_text(
            cleaned_code,
            encoding="utf-8"
        )

        result = subprocess.run(
            [
                "node",
                "converter.js",
                str(js_file),
                str(ppt_file)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            st.error("PowerPoint generation failed")

            if result.stderr:
                st.code(result.stderr)

            if result.stdout:
                st.code(result.stdout)

            st.stop()

        if not ppt_file.exists():

            st.error("PPT file was not generated")

            if result.stdout:
                st.code(result.stdout)

            if result.stderr:
                st.code(result.stderr)

            st.stop()

        st.success("PowerPoint generated successfully!")

        with open(ppt_file, "rb") as f:

            st.download_button(
                label="📥 Download PPTX",
                data=f.read(),
                file_name=f"{filename}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

        with st.expander("Execution Logs"):

            if result.stdout:
                st.code(result.stdout)

            if result.stderr:
                st.code(result.stderr)

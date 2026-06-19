import streamlit as st
import subprocess
import tempfile
from pathlib import Path

st.set_page_config(
    page_title="JavaScript → PowerPoint Converter",
    layout="wide"
)

@st.cache_resource
def install_dependencies():
    try:
        result = subprocess.run(
            ["npm", "list", "pptxgenjs"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            subprocess.run(
                ["npm", "install", "pptxgenjs"],
                check=True,
                capture_output=True,
                text=True
            )

        return True

    except Exception as e:
        st.error(f"Dependency installation failed:\n{e}")
        return False

install_dependencies()

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

    with tempfile.TemporaryDirectory() as tmp:

        js_file = Path(tmp) / "input.js"
        ppt_file = Path(tmp) / f"{filename}.pptx"
# remove start
import re

cleaned_code = js_code

# Remove import
cleaned_code = re.sub(
    r'const\s+pptxgen\s*=\s*require\s*\(\s*[\'"]pptxgenjs[\'"]\s*\)\s*;?',
    '',
    cleaned_code
)

# Replace presentation creation
cleaned_code = re.sub(
    r'const\s+pres\s*=\s*new\s+pptxgen\s*\(\s*\)\s*;?',
    'const pres = pptx;',
    cleaned_code
)

# Remove final writeFile block
cleaned_code = re.sub(
    r'pres\.writeFile\s*\([\s\S]*?$',
    '',
    cleaned_code,
    flags=re.MULTILINE
)

js_file.write_text(
    cleaned_code,
    encoding="utf-8"
)
# remove end
        js_file.write_text(
            js_code,
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
            st.code(result.stderr)
            st.stop()

        if not ppt_file.exists():
            st.error("PPT file was not generated")
            if result.stdout:
                st.code(result.stdout)
            st.stop()

        with open(ppt_file, "rb") as f:
            st.download_button(
                "📥 Download PPTX",
                data=f.read(),
                file_name=f"{filename}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

        if result.stdout:
            with st.expander("Logs"):
                st.code(result.stdout)

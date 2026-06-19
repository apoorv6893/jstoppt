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

st.markdown("""
Paste PptxGenJS code below.

Example:

```javascript
let slide = pptx.addSlide();

slide.addText("Hello World", {
    x: 1,
    y: 1,
    w: 4,
    h: 1,
    fontSize: 24
});
```
""")

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

if st.button("🚀 Generate PPTX", use_container_width=True):

    if not js_code.strip():
        st.error("Please enter JavaScript code.")
        st.stop()

    if not Path("converter.js").exists():
        st.error("converter.js not found in repository root.")
        st.stop()

    with tempfile.TemporaryDirectory() as tmp:

        js_file = Path(tmp) / "input.js"
        ppt_file = Path(tmp) / "output.pptx"

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

            if result.stderr:
                st.code(result.stderr)

            if result.stdout:
                st.code(result.stdout)

            st.stop()

        if not ppt_file.exists():

            st.error("PPT file was not generated.")

            if result.stdout:
                st.code(result.stdout)

            st.stop()

        st.success("PowerPoint generated successfully!")

        with open(ppt_file, "rb") as f:

            st.download_button(
                label="📥 Download PPTX",
                data=f.read(),
                file_name=f"{filename}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )

        with st.expander("Execution Logs"):
            if result.stdout:
                st.code(result.stdout)
            else:
                st.write("No logs generated.")

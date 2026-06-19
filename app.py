import streamlit as st
import subprocess
import tempfile
from pathlib import Path

@st.cache_resource
def install_dependencies():
    result = subprocess.run(
        ["npm", "install", "pptxgenjs"],
        capture_output=True,
        text=True
    )

    return result.returncode == 0

install_dependencies()

st.set_page_config(page_title="JS to PPTX", layout="wide")

@st.cache_resource
def install_deps():
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
    except Exception as e:
        st.warning(f"npm install issue: {e}")

install_deps()

st.title("JavaScript → PowerPoint Converter")

st.markdown("""
Paste PptxGenJS code such as:

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

js_code = st.text_area("JavaScript Code", height=500)

filename = st.text_input("Output Filename", "presentation")

if st.button("Generate PPTX"):

    if not js_code.strip():
        st.error("Please enter JavaScript code.")
        st.stop()

    converter_js = """
const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    const code = fs.readFileSync(inputFile, "utf8");

    const wrappedCode = `
        const pptx = new PptxGenJS();
        ${code}
        await pptx.writeFile({ fileName: "${outputFile}" });
    `;

    const fn = new Function("PptxGenJS", wrappedCode);
    await fn(PptxGenJS);
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});
"""

    Path("converter.js").write_text(converter_js, encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:

        js_file = Path(tmp) / "input.js"
        ppt_file = Path(tmp) / "output.pptx"

        js_file.write_text(js_code, encoding="utf-8")

        result = subprocess.run(
            ["node", "converter.js", str(js_file), str(ppt_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            st.error("Generation failed")
            st.code(result.stderr)
            st.stop()

        if not ppt_file.exists():
            st.error("PPT file was not generated.")
            st.stop()

        with open(ppt_file, "rb") as f:
            st.download_button(
                "Download PPTX",
                data=f.read(),
                file_name=f"{filename}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

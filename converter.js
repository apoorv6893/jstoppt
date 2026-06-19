const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    const code = fs.readFileSync(inputFile, "utf8");

    const wrappedCode = `
        const pptx = new PptxGenJS();
        ${code}
        pptx.writeFile({ fileName: "${outputFile}" });
    `;

    const fn = new Function("PptxGenJS", wrappedCode);
    await fn(PptxGenJS);
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

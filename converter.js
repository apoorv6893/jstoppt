console.log("=== NEW CONVERTER LOADED ===");

const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Remove common lines users paste from full examples
    code = code.replace(
        /const\s+pptx\s*=\s*new\s+PptxGenJS\s*\(\s*\)\s*;?/g,
        ""
    );

    code = code.replace(
        /let\s+pptx\s*=\s*new\s+PptxGenJS\s*\(\s*\)\s*;?/g,
        ""
    );

    code = code.replace(
        /await\s+pptx\.writeFile\s*\([^)]*\)\s*;?/g,
        ""
    );

    code = code.replace(
        /pptx\.writeFile\s*\([^)]*\)\s*;?/g,
        ""
    );

    const wrappedCode = `
        const pptx = new PptxGenJS();

        ${code}

        await pptx.writeFile({
            fileName: "${outputFile}"
        });
    `;

    console.log("===== EXECUTING CODE =====");
    console.log(wrappedCode);

    const AsyncFunction = Object.getPrototypeOf(
        async function () {}
    ).constructor;

    const fn = new AsyncFunction(
        "PptxGenJS",
        wrappedCode
    );

    await fn(PptxGenJS);

    console.log("PPT generated successfully");
}

run().catch(err => {
    console.error("===== ERROR =====");
    console.error(err);
    process.exit(1);
});

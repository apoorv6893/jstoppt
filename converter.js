const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Remove pptxgenjs import from uploaded JS
    code = code.replace(
        /const\s+.*?\s*=\s*require\s*\(\s*["']pptxgenjs["']\s*\)\s*;?/g,
        ""
    );

    // Replace ANY writeFile(...) call
    code = code.replace(
        /\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;?/g,
        ""
    );

    const wrappedCode = `
        const pptxgen = PptxGenJS;

        ${code}

        if (typeof pres !== "undefined") {
            await pres.writeFile({
                fileName: "${outputFile}"
            });
        } else if (typeof pptx !== "undefined") {
            await pptx.writeFile({
                fileName: "${outputFile}"
            });
        } else {
            throw new Error(
                "Could not find presentation object. Expected 'pres' or 'pptx'."
            );
        }
    `;

    const AsyncFunction =
        Object.getPrototypeOf(async function(){}).constructor;

    const fn = new AsyncFunction(
        "PptxGenJS",
        wrappedCode
    );

    await fn(PptxGenJS);
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

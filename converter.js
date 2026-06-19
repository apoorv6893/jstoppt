const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Remove any pptxgenjs imports
    code = code.replace(
        /const\s+.*?\s*=\s*require\s*\(\s*["']pptxgenjs["']\s*\)\s*;?/g,
        ""
    );

    // Replace hardcoded output file
    code = code.replace(
        /pres\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;?/g,
        `await pres.writeFile({ fileName: "${outputFile}" });`
    );

    const AsyncFunction =
        Object.getPrototypeOf(async function () {}).constructor;

    const fn = new AsyncFunction(
        "PptxGenJS",
        `
${code}
`
    );

    await fn(PptxGenJS);

    console.log("PPT generated successfully");
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

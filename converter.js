const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Remove imports
    code = code.replace(
        /const\s+pptxgen\s*=\s*require\(["']pptxgenjs["']\);?/g,
        ""
    );

    code = code.replace(
        /const\s+PptxGenJS\s*=\s*require\(["']pptxgenjs["']\);?/g,
        ""
    );

    // Remove presentation creation
    code = code.replace(
        /const\s+pres\s*=\s*new\s+pptxgen\s*\(\s*\)\s*;?/g,
        ""
    );

    code = code.replace(
        /const\s+pptx\s*=\s*new\s+PptxGenJS\s*\(\s*\)\s*;?/g,
        ""
    );

    // Remove writeFile calls
    code = code.replace(
        /await\s+.*?writeFile\s*\([^)]*\)\s*;?/gs,
        ""
    );

    code = code.replace(
        /.*?writeFile\s*\([^)]*\)\s*;?/gs,
        ""
    );

    const wrappedCode = `
        const pptx = new PptxGenJS();
        const pres = pptx;

        ${code}

        await pptx.writeFile({
            fileName: "${outputFile}"
        });
    `;

    const AsyncFunction =
        Object.getPrototypeOf(async function(){}).constructor;

    const fn = new AsyncFunction(
        "PptxGenJS",
        wrappedCode
    );

    await fn(PptxGenJS);

    console.log("PPT generated successfully");
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

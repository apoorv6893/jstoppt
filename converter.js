const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    const code = fs.readFileSync(inputFile, "utf8");

    const wrappedCode = `
        const pptx = new PptxGenJS();

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
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Remove ALL require(...) lines
    code = code.replace(
        /^.*require\s*\(.*\).*$/gm,
        ""
    );

    // Remove ALL writeFile(...) calls
    code = code.replace(
        /^.*writeFile\s*\(.*$/gm,
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
            throw new Error("No presentation object found");
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

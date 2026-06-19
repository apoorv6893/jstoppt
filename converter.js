const fs = require("fs");
const PptxGenJS = require("pptxgenjs");

async function run() {

    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    code = code.replace(
        /const\s+pptxgen\s*=\s*require\(["']pptxgenjs["']\);?/g,
        ""
    );

    code = code.replace(
        /const\s+pres\s*=\s*new\s+pptxgen\(\);?/g,
        "const pres = new PptxGenJS();"
    );

    code = code.replace(
        /pres\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;?/g,
        ""
    );

    const AsyncFunction =
        Object.getPrototypeOf(async function(){}).constructor;

    const wrapped = `
        ${code}

        await pres.writeFile({
            fileName: "${outputFile}"
        });
    `;

    const fn = new AsyncFunction(
        "PptxGenJS",
        wrapped
    );

    await fn(PptxGenJS);
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

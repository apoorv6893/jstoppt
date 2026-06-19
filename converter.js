const fs = require("fs");
const { spawnSync } = require("child_process");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    code = code.replace(
        /\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;?/g,
        `.writeFile({ fileName: "${outputFile}" });`
    );

    const generatedFile = "generated_runtime.js";

    fs.writeFileSync(
        generatedFile,
        code,
        "utf8"
    );

    const result = spawnSync(
        "node",
        [generatedFile],
        {
            encoding: "utf8"
        }
    );

    try {
        fs.unlinkSync(generatedFile);
    } catch {}

    if (result.stdout) {
        console.log(result.stdout);
    }

    if (result.stderr) {
        console.error(result.stderr);
    }

    process.exit(result.status || 0);
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});

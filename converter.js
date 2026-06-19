const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

async function run() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];

    let code = fs.readFileSync(inputFile, "utf8");

    // Replace any writeFile call with our output path
    code = code.replace(
        /\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;?/g,
        `.writeFile({ fileName: "${outputFile}" });`
    );

    const generatedScript = path.join(
        path.dirname(inputFile),
        "generated.js"
    );

    fs.writeFileSync(
        generatedScript,
        code,
        "utf8"
    );

    const result = spawnSync(
        "node",
        [generatedScript],
        {
            encoding: "utf8"
        }
    );

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

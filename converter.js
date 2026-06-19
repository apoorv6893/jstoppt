const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const inputFile = process.argv[2];
const outputFile = process.argv[3];

let code = fs.readFileSync(inputFile, "utf8");

// Replace the final writeFile path
code = code.replace(
    /pres\.writeFile\s*\(\s*\{[\s\S]*?\}\s*\)\s*;/,
    `pres.writeFile({ fileName: "${outputFile}" });`
);

const runtimeFile = path.join(
    path.dirname(inputFile),
    "runtime.js"
);

fs.writeFileSync(runtimeFile, code);

const result = spawnSync(
    "node",
    [runtimeFile],
    {
        encoding: "utf8",
        cwd: process.cwd()
    }
);

if (result.stdout) {
    console.log(result.stdout);
}

if (result.stderr) {
    console.error(result.stderr);
}

process.exit(result.status || 0);

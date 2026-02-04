#!/usr/bin/env node
const fs = require("fs");
const crypto = require("crypto");

function sha256(data) {
  return "sha256:" + crypto.createHash("sha256").update(data).digest("hex");
}

function hashFile(path) {
  const data = fs.readFileSync(path);
  return sha256(data);
}

const args = process.argv.slice(2);
const cmd = args[0];

if (cmd === "init") {
  const file = args[1];
  const hash = hashFile(file);
  console.log(hash);
}

/* ---------------- commit ---------------- */

if (cmd === "commit") {
  const file = args[1];
  const author = args[args.indexOf("--author") + 1] || "";
  const intent = args[args.indexOf("--intent") + 1] || "";

  const contentHash = hashFile(file);
  const medfPath = file + ".medf.json";

  let previous = null;
  if (fs.existsSync(medfPath)) {
    const old = fs.readFileSync(medfPath, "utf8");
    previous = sha256(old);
  }

  const medf = {
    medf_version: "0.1",
    document: {
      title: file,
      content_hash: contentHash,
      content_type: "text/plain",
      source: `local:${file}`
    },
    intent: {
      author,
      description: intent
    },
    timestamp: new Date().toISOString(),
    previous
  };

  fs.writeFileSync(medfPath, JSON.stringify(medf, null, 2));
  console.log(`MEDF committed: ${medfPath}`);
}

/* ---------------- verify ---------------- */

if (cmd === "verify") {
  const file = args[1];
  const medf = JSON.parse(fs.readFileSync(file, "utf8"));
  const sourceFile = medf.document.source.replace("local:", "");
  const currentHash = hashFile(sourceFile);

  if (currentHash === medf.document.content_hash) {
    console.log("✅ content hash OK");
  } else {
    console.log("❌ content hash MISMATCH");
  }
}

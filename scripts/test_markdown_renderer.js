#!/usr/bin/env node

"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const projectRoot = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(projectRoot, "plugin", "content", "main.js"), "utf8");
const context = vm.createContext({
    ZCC_TESTING: true,
    Zotero: {},
    Cc: {},
    Ci: {},
    katex: {},
    Services: {},
    console,
    setTimeout,
    clearTimeout,
});
vm.runInContext(source, context, { filename: "plugin/content/main.js" });

const { renderMarkdown, splitTableRow } = context.ZoteroCodexChatPlugin.__test;

assert.deepEqual(
    Array.from(splitTableRow("| Method | Solution | Scope |")),
    ["Method", "Solution", "Scope"]
);
assert.deepEqual(
    Array.from(splitTableRow(String.raw`| Least squares | $\min_x \|Ax-y\|_2^2$ | Linear |`)),
    ["Least squares", String.raw`$\min_x \|Ax-y\|_2^2$`, "Linear"]
);
assert.deepEqual(
    Array.from(splitTableRow("| Syntax | `left | right` | $a | b$ |")),
    ["Syntax", "`left | right`", "$a | b$"]
);

const table = renderMarkdown(String.raw`| Method | Solution | Scope |
| --- | --- | --- |
| Least squares | $\min_x \|Ax-y\|_2^2$ | Linear |`);
assert.equal((table.match(/<td>/g) || []).length, 3);
assert.match(table, /data-tex="\\min_x \\\|Ax-y\\\|_2\^2"/);

const looseList = renderMarkdown("1. First\n\nExplanation\n\n2. Second\n\n3. Third");
assert.equal(
    looseList,
    "<ol><li>First</li></ol><p>Explanation</p><ol start=\"2\"><li>Second</li></ol><ol start=\"3\"><li>Third</li></ol>"
);

const contiguousList = renderMarkdown("3. Third\n4. Fourth");
assert.equal(contiguousList, "<ol start=\"3\"><li>Third</li><li>Fourth</li></ol>");

console.log("Markdown renderer tests passed.");

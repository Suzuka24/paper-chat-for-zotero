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

const { renderMarkdown, splitTableRow, normalizedFontSize, createStreamingPreview } = context.ZoteroCodexChatPlugin.__test;

assert.equal(normalizedFontSize("16"), 16);
assert.equal(normalizedFontSize(8), 11);
assert.equal(normalizedFontSize(24), 20);
assert.equal(normalizedFontSize("invalid"), 13);

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

const timers = new Map();
let nextTimer = 0;
let updates = 0;
let finalRenders = 0;
const textNode = { data: "", appendData(value) { this.data += value; } };
const classes = new Set();
const element = {
    ownerDocument: { createTextNode: () => textNode },
    classList: { add: value => classes.add(value), remove: value => classes.delete(value) },
    append(node) { assert.equal(node, textNode); },
    textContent: "",
};
const view = {
    setTimeout(callback) { const id = ++nextTimer; timers.set(id, callback); return id; },
    clearTimeout(id) { timers.delete(id); },
};
const preview = createStreamingPreview(element, view, (target, source) => {
    finalRenders++;
    target.textContent = source;
}, () => { updates++; });
let streamed = "";
for (let index = 0; index < 5000; index++) {
    streamed += "x";
    preview.append("x", streamed);
}
assert.equal(timers.size, 1);
assert.equal(updates, 0);
assert.equal(element._zccMarkdown, streamed);
timers.get(1)();
timers.delete(1);
assert.equal(updates, 1);
assert.equal(textNode.data, streamed);
assert.equal(classes.has("zcc-streaming"), true);
preview.append("!", streamed + "!");
preview.finish(streamed + "!");
assert.equal(timers.size, 0);
assert.equal(finalRenders, 1);
assert.equal(element.textContent, streamed + "!");
assert.equal(classes.has("zcc-streaming"), false);
preview.cancel();

const abandoned = createStreamingPreview(element, view, () => { finalRenders++; }, () => { updates++; });
abandoned.append("ignored", "ignored");
assert.equal(timers.size, 1);
abandoned.cancel();
assert.equal(timers.size, 0);
assert.equal(finalRenders, 1);

console.log("Markdown renderer tests passed.");

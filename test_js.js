const fs = require("fs");
const pdfjsLib = require("pdfjs-dist/legacy/build/pdf.js");

async function test() {
  const data = new Uint8Array(fs.readFileSync("franca.pdf"));
  const doc = await pdfjsLib.getDocument(data).promise;

  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const textContent = await page.getTextContent();

    const items = textContent.items;
    const tolerance = 4;
    items.sort((a, b) => {
      if (Math.abs(a.transform[5] - b.transform[5]) > tolerance)
        return b.transform[5] - a.transform[5];
      return a.transform[4] - b.transform[4];
    });

    let lines = [];
    let currentLine = [];
    let currentY = null;
    items.forEach((item) => {
      if (
        currentY === null ||
        Math.abs(item.transform[5] - currentY) > tolerance
      ) {
        if (currentLine.length > 0) lines.push(currentLine);
        currentLine = [];
        currentY = item.transform[5];
      }
      currentLine.push(item.str);
    });
    if (currentLine.length > 0) lines.push(currentLine);

    console.log(`--- PAGE ${i} ---`);
    lines.forEach((l, idx) => {
      const lineStr = l.join(" ").trim();
      const rawValues = l.slice(1);
      const numericValues = rawValues.filter(
        (v) => /[\\d\\.,]+/.test(v) && v.trim().length > 0,
      );
      if (lineStr.includes("13º Salário") || lineStr.includes("13° Salário")) {
        console.log(`FOUND 13o on Line ${idx}: ${JSON.stringify(l)}`);
        console.log(`numericValues: ${JSON.stringify(numericValues)}`);
      }
    });
  }
}
test().catch(console.error);

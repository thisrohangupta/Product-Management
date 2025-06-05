"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
function scanDir(dir, root, files) {
    const entries = fs_1.default.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path_1.default.join(dir, entry.name);
        if (entry.isDirectory()) {
            scanDir(fullPath, root, files);
        }
        else if (entry.name.endsWith('.yaml') || entry.name.endsWith('.yml')) {
            const content = fs_1.default.readFileSync(fullPath, 'utf8');
            files.push({ relativePath: path_1.default.relative(root, fullPath), content });
        }
    }
}
function getAllYamlFiles() {
    // __dirname points to the compiled JS directory. Move two levels up to reach
    // the repository root so that all YAML files are discovered.
    const rootDir = path_1.default.resolve(__dirname, '..', '..');
    const files = [];
    scanDir(rootDir, rootDir, files);
    return files;
}
function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}
function generateHtml(files) {
    const items = files
        .map((file, index) => {
        const escaped = escapeHtml(file.content);
        const id = `modal-${index}`;
        return `\n      <div class="border rounded-lg p-4 bg-white shadow">
        <h2 class="font-semibold text-sm break-all">${file.relativePath}</h2>
        <button class="mt-2 text-sm text-blue-600 underline" data-modal="${id}">View</button>
        <dialog id="${id}" class="p-0 rounded-lg w-11/12 max-w-3xl">
          <div class="p-4 overflow-auto max-h-[80vh]">
            <button class="text-sm mb-2" data-close>Close</button>
            <pre class="whitespace-pre-wrap text-xs">${escaped}</pre>
          </div>
        </dialog>
      </div>`;
    })
        .join('\n');
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>YAML Gallery</title>
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.3.5/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50 text-gray-900">
  <main class="container mx-auto p-4 grid gap-4 grid-cols-1 md:grid-cols-2">
  ${items}
  </main>
<script>
  document.querySelectorAll('[data-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.getAttribute('data-modal');
      const dialog = document.getElementById(id);
      dialog.showModal();
    });
  });
  document.querySelectorAll('dialog [data-close]').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('dialog').close());
  });
</script>
</body>
</html>`;
}
const files = getAllYamlFiles();
const html = generateHtml(files);
const outDir = path_1.default.join(__dirname, 'dist');
fs_1.default.mkdirSync(outDir, { recursive: true });
fs_1.default.writeFileSync(path_1.default.join(outDir, 'index.html'), html);
console.log(`Generated ${files.length} YAML entries in dist/index.html`);

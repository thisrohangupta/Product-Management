import fs from 'fs';
import path from 'path';

interface YamlFile {
  relativePath: string;
  content: string;
}

function scanDir(dir: string, root: string, files: YamlFile[]) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(fullPath, root, files);
    } else if (entry.name.endsWith('.yaml') || entry.name.endsWith('.yml')) {
      const content = fs.readFileSync(fullPath, 'utf8');
      files.push({ relativePath: path.relative(root, fullPath), content });
    }
  }
}

function getAllYamlFiles(): YamlFile[] {
  // __dirname points to the compiled JS directory. Move two levels up to reach
  // the repository root so that all YAML files are discovered.
  const rootDir = path.resolve(__dirname, '..', '..');
  const files: YamlFile[] = [];
  scanDir(rootDir, rootDir, files);
  return files;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function generateHtml(files: YamlFile[]): string {
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
const outDir = path.join(__dirname, 'dist');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'index.html'), html);
console.log(`Generated ${files.length} YAML entries in dist/index.html`);

import fs from 'fs';
import path from 'path';

export interface YamlFile {
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

export function getAllYamlFiles(): YamlFile[] {
  const root = path.resolve(process.cwd(), '..');
  const files: YamlFile[] = [];
  scanDir(root, root, files);
  return files;
}

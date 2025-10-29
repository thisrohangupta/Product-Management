# YAML Gallery (Static)

This script generates a simple static HTML gallery of all YAML files in the repository.
It does not require any npm dependencies and can run in offline environments.

## Usage

Run the generator with `tsc` and `node`:

```bash
tsc -p yaml-gallery-static/tsconfig.json
node yaml-gallery-static/dist/generate-gallery.js
```

Open `yaml-gallery-static/dist/index.html` in your browser to view the gallery.

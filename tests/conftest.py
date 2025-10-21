import os
import sys
from pathlib import Path

# Ensure 'src' is importable without installing as a package
ROOT = Path(__file__).resolve().parents[1]
src_path = ROOT / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

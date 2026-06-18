#!/usr/bin/env python3
"""Auto-generated plot wrapper for civil-generic-property-comparison."""

from pathlib import Path
import sys

# Add figure scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts" / "figures4materials"))

from plot_grouped_bar import main

if __name__ == "__main__":
    raise SystemExit(main())

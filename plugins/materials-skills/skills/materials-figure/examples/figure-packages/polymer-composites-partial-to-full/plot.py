#!/usr/bin/env python3
from pathlib import Path
import sys

FIGURE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(FIGURE_ROOT / "scripts"))

from compose_multipanel_figure import compose  # noqa: E402

PACKAGE = Path(__file__).resolve().parent
compose(PACKAGE / "figure_storyboard.yaml", PACKAGE)

#!/usr/bin/env python3
"""Build editorial showcase proof boards from reader-package visual assets."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = SKILL_ROOT / "assets" / "showcase-proof"
SHOWCASE_MANIFEST = "showcase_manifest.json"

CANVAS_SIZE = (2000, 1280)
MARGIN = 72
TOP_START = 228
GAP = 26
CARD_RADIUS = 30
LABEL_HEIGHT = 126
NARRATIVE_LAYERS = ["overview", "deviation", "relationship"]

PALETTE = {
    "paper": "#F4EFE6",
    "paper_alt": "#EEE6DA",
    "card": "#FFFDFC",
    "border": "#D7CBB9",
    "ink": "#1F2624",
    "muted": "#5B6760",
    "shadow": "#D9D0C2",
    "line": "#C9BCA9",
    "overview": "#314A63",
    "deviation": "#A65A37",
    "relationship": "#6D7B45",
    "gold": "#B28B45",
}


@dataclass(frozen=True)
class Crop:
    left: float = 0.0
    top: float = 0.0
    right: float = 1.0
    bottom: float = 1.0

    def as_dict(self) -> dict[str, float]:
        return {
            "left": self.left,
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
        }


@dataclass(frozen=True)
class Tile:
    panel_id: str
    role: str
    label: str
    source_note: str
    path: Path
    crop: Crop = Crop()
    accent: str = "overview"
    framing: str = "fit"


@dataclass(frozen=True)
class Board:
    filename: str
    title: str
    subtitle: str
    eyebrow: str
    footer: str
    layout_family: str
    badges: tuple[str, ...]
    tiles: tuple[Tile, ...]


def crop_box(left: float, top: float, right: float, bottom: float) -> Crop:
    return Crop(left=left, top=top, right=right, bottom=bottom)


CONTACT_SHEET_015 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "contact_sheet.png"
CONTACT_SHEET_016 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "contact_sheet.png"
CONTACT_SHEET_017 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "contact_sheet.png"

FIG_015_01 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-01_fig-1-2.png"
FIG_015_02 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-02_fig-3.png"
FIG_015_03 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-03_fig-8.png"
FIG_015_08 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-08_fig-14.png"

FIG_016_02 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "figures" / "f016-02_table-5-fm-morphology.png"
FIG_016_03 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "figures" / "f016-03_fig-3-4.png"
FIG_016_05 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "figures" / "f016-05_fig-8-10-table-6.png"
TABLE_016_01 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "tables" / "t016-01_table-7.png"

FIG_017_01 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "figures" / "f017-01_fig-4-5-inclined-shear-fatigue-method.png"
FIG_017_02 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "figures" / "f017-02_fig-8-tack-coat-fatigue-results.png"
FIG_017_03 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "figures" / "f017-03_fig-9-s-n-fitting.png"
TABLE_017_01 = REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "tables" / "t017-01_table-8-tack-coat-fatigue-table.png"


BOARDS = (
    Board(
        filename="reader_package_proof_wall.png",
        title="Reader-Package Editorial Wall",
        subtitle="Three package overviews plus focused insets, preserving package scale and evidence lineage on the same surface",
        eyebrow="front-door proof / package scale",
        footer="Each panel stays linked to a real package page, extracted figure, or chart so the gallery proves workflow scale rather than promising it abstractly.",
        layout_family="editorial_triptych",
        badges=("Package scale", "Asset lineage", "Source-grounded"),
        tiles=(
            Tile("a", "overview", "015 curing-agent package", "contact_sheet.png", CONTACT_SHEET_015, accent="overview", framing="contain"),
            Tile("b", "overview", "016 SBR-WER binder package", "contact_sheet.png", CONTACT_SHEET_016, accent="deviation", framing="contain"),
            Tile("c", "overview", "017 AC-PCC fatigue package", "contact_sheet.png", CONTACT_SHEET_017, accent="relationship", framing="contain"),
            Tile("d", "deviation", "Rheology inset from WER-EA package", "f015-03_fig-8.png", FIG_015_03, crop_box(0.11, 0.20, 0.92, 0.68), accent="deviation"),
            Tile("e", "relationship", "FTIR + morphology evidence surface", "f016-03_fig-3-4.png", FIG_016_03, crop_box(0.02, 0.00, 0.95, 0.68), accent="overview"),
            Tile("f", "relationship", "Tack-coat fatigue result inset", "f017-02_fig-8-tack-coat-fatigue-results.png", FIG_017_02, crop_box(0.07, 0.01, 0.95, 0.53), accent="relationship"),
        ),
    ),
    Board(
        filename="wer_ea_figure_proof_board.png",
        title="WER-EA Review Evidence Board",
        subtitle="A dominant mechanism anchor, then dosage drift and spectral support arranged as overview, deviation, and relationship",
        eyebrow="front-door proof / review figure",
        footer="The large panel establishes the mechanism story, while the smaller panels keep dosage behavior and spectral support visible as separate evidence roles.",
        layout_family="editorial_mosaic",
        badges=("Mechanism anchor", "Dosage drift", "Spectral support"),
        tiles=(
            Tile("a", "overview", "Crosslinking overview crop", "f015-01_fig-1-2.png", FIG_015_01, crop_box(0.14, 0.34, 0.86, 0.89), accent="overview"),
            Tile("b", "deviation", "Chemical formula anchor", "f015-02_fig-3.png", FIG_015_02, crop_box(0.14, 0.02, 0.88, 0.62), accent="gold"),
            Tile("c", "deviation", "Rheology temperature-response window", "f015-03_fig-8.png", FIG_015_03, crop_box(0.09, 0.15, 0.94, 0.72), accent="deviation"),
            Tile("d", "relationship", "FTIR evidence anchor", "f015-08_fig-14.png", FIG_015_08, crop_box(0.03, 0.00, 0.45, 0.34), accent="relationship"),
            Tile("e", "relationship", "Second rheology view for comparison", "f015-03_fig-8.png", FIG_015_03, crop_box(0.52, 0.15, 0.95, 0.72), accent="overview"),
        ),
    ),
    Board(
        filename="sbr_wer_performance_proof_board.png",
        title="SBR-WER Performance Editorial Board",
        subtitle="Performance, fluorescence morphology, FTIR, adhesion photos, and SEM details sit on one surface without collapsing into a template card",
        eyebrow="front-door proof / performance + morphology",
        footer="This board compresses the strongest waterproof-binder evidence into one editorial surface while keeping charts, microscopy, FTIR, and adhesion photos legible as separate sources.",
        layout_family="editorial_mosaic",
        badges=("Behavior window", "Morphology density", "Adhesion photos"),
        tiles=(
            Tile("a", "overview", "Performance window with viscosity + low-temperature results", "f016-05_fig-8-10-table-6.png", FIG_016_05, crop_box(0.02, 0.00, 0.98, 0.57), accent="deviation"),
            Tile("b", "deviation", "Fluorescence morphology matrix", "f016-02_table-5-fm-morphology.png", FIG_016_02, crop_box(0.17, 0.10, 0.98, 0.90), accent="relationship"),
            Tile("c", "deviation", "FTIR modifier comparison", "f016-03_fig-3-4.png", FIG_016_03, crop_box(0.02, 0.00, 0.47, 0.35), accent="overview"),
            Tile("d", "relationship", "Aggregate adhesion photo table", "t016-01_table-7.png", TABLE_016_01, crop_box(0.52, 0.00, 0.99, 0.72), accent="gold"),
            Tile("e", "relationship", "SEM surface evidence sheet", "f016-03_fig-3-4.png", FIG_016_03, crop_box(0.04, 0.53, 0.94, 0.98), accent="deviation"),
        ),
    ),
    Board(
        filename="interlayer_fatigue_proof_board.png",
        title="Interlayer Fatigue Editorial Board",
        subtitle="Result charts dominate the page, while apparatus, fitting curves, and tabulated fatigue life stay visible as supporting relationships",
        eyebrow="front-door proof / method + results",
        footer="The front-door view leads with the fatigue result field, then keeps apparatus geometry, fitting curves, and table evidence close enough to audit the claim path.",
        layout_family="editorial_mosaic",
        badges=("Fatigue results", "Method fixture", "Table trace"),
        tiles=(
            Tile("a", "overview", "Tack-coat fatigue result field", "f017-02_fig-8-tack-coat-fatigue-results.png", FIG_017_02, crop_box(0.07, 0.00, 0.95, 0.52), accent="overview"),
            Tile("b", "deviation", "S-N fitting comparison", "f017-03_fig-9-s-n-fitting.png", FIG_017_03, crop_box(0.14, 0.00, 0.94, 0.56), accent="deviation"),
            Tile("c", "deviation", "Fatigue life table surface", "t017-01_table-8-tack-coat-fatigue-table.png", TABLE_017_01, crop_box(0.03, 0.04, 0.97, 0.59), accent="gold"),
            Tile("d", "relationship", "Method schematic", "f017-01_fig-4-5-inclined-shear-fatigue-method.png", FIG_017_01, crop_box(0.02, 0.00, 0.45, 0.44), accent="relationship"),
            Tile("e", "relationship", "Fixture photograph", "f017-01_fig-4-5-inclined-shear-fatigue-method.png", FIG_017_01, crop_box(0.50, 0.00, 0.90, 0.44), accent="overview"),
        ),
    ),
)


def load_font(size: int, *, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if serif:
        candidates = ["DejaVuSerif-Bold.ttf", "Georgia Bold.ttf", "timesbd.ttf"] if bold else ["DejaVuSerif.ttf", "Georgia.ttf", "times.ttf"]
    else:
        candidates = ["DejaVuSans-Bold.ttf", "arialbd.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = load_font(58, bold=True, serif=True)
SUBTITLE_FONT = load_font(24)
EYEBROW_FONT = load_font(18, bold=True)
BADGE_FONT = load_font(17, bold=True)
PANEL_FONT = load_font(26, bold=True, serif=True)
LABEL_FONT = load_font(25, bold=True)
NOTE_FONT = load_font(16)
FOOTER_FONT = load_font(18)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def crop_image(path: Path, crop: Crop) -> Image.Image:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        width, height = rgb.size
        left = int(width * crop.left)
        top = int(height * crop.top)
        right = int(width * crop.right)
        bottom = int(height * crop.bottom)
        return rgb.crop((left, top, max(left + 1, right), max(top + 1, bottom)))


def render_panel(tile: Tile, size: tuple[int, int]) -> Image.Image:
    image = crop_image(tile.path, tile.crop)
    if tile.framing == "contain":
        panel = Image.new("RGB", size, "#F8F4EC")
        contained = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
        offset = ((size[0] - contained.width) // 2, (size[1] - contained.height) // 2)
        panel.paste(contained, offset)
        return panel
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def paint_background(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    for y in range(CANVAS_SIZE[1]):
        blend = y / (CANVAS_SIZE[1] - 1)
        r0, g0, b0 = ImageColorTuple.from_hex(PALETTE["paper"])
        r1, g1, b1 = ImageColorTuple.from_hex(PALETTE["paper_alt"])
        color = (
            int(r0 + (r1 - r0) * blend),
            int(g0 + (g1 - g0) * blend),
            int(b0 + (b1 - b0) * blend),
        )
        draw.line((0, y, CANVAS_SIZE[0], y), fill=color)

    for x in range(MARGIN, CANVAS_SIZE[0] - MARGIN, 160):
        draw.line((x, 0, x, CANVAS_SIZE[1]), fill="#F1E8DB", width=1)
    for y in range(0, CANVAS_SIZE[1], 120):
        draw.line((0, y, CANVAS_SIZE[0], y), fill="#EFE5D7", width=1)


class ImageColorTuple:
    @staticmethod
    def from_hex(value: str) -> tuple[int, int, int]:
        value = value.lstrip("#")
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def draw_badges(draw: ImageDraw.ImageDraw, board: Board) -> None:
    x = CANVAS_SIZE[0] - MARGIN - 420
    y = 42
    for index, label in enumerate(board.badges):
        badge_width = 132
        x0 = x + index * (badge_width + 10)
        x1 = x0 + badge_width
        draw.rounded_rectangle((x0, y, x1, y + 34), radius=17, fill="#FFF8EE", outline=PALETTE["border"], width=1)
        draw.text((x0 + 14, y + 8), label, fill=PALETTE["ink"], font=BADGE_FONT)


def draw_header(draw: ImageDraw.ImageDraw, board: Board) -> None:
    eyebrow_width = int(draw.textlength(board.eyebrow.upper(), font=EYEBROW_FONT)) + 28
    draw.rounded_rectangle((MARGIN, 38, MARGIN + eyebrow_width, 72), radius=17, fill="#FFF7EB", outline=PALETTE["border"], width=1)
    draw.text((MARGIN + 14, 47), board.eyebrow.upper(), fill=PALETTE["muted"], font=EYEBROW_FONT)

    draw.text((MARGIN, 104), board.title, fill=PALETTE["ink"], font=TITLE_FONT)
    subtitle_lines = wrap_text(draw, board.subtitle, SUBTITLE_FONT, 1160)
    for index, line in enumerate(subtitle_lines[:2]):
        draw.text((MARGIN, 170 + index * 28), line, fill=PALETTE["muted"], font=SUBTITLE_FONT)

    draw_badges(draw, board)
    draw.line((MARGIN, TOP_START - 24, CANVAS_SIZE[0] - MARGIN, TOP_START - 24), fill=PALETTE["line"], width=3)

    for index, role in enumerate(NARRATIVE_LAYERS):
        chip_width = 134
        x0 = CANVAS_SIZE[0] - MARGIN - 3 * chip_width - 2 * 10 + index * (chip_width + 10)
        y0 = 96
        draw.rounded_rectangle((x0, y0, x0 + chip_width, y0 + 34), radius=17, fill=PALETTE[role], outline=PALETTE[role], width=1)
        draw.text((x0 + 18, y0 + 8), role.title(), fill="#FFF9F2", font=BADGE_FONT)


def draw_tile(canvas: Image.Image, draw: ImageDraw.ImageDraw, tile: Tile, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    shadow_offset = 10
    draw.rounded_rectangle((x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset), radius=CARD_RADIUS, fill=PALETTE["shadow"])
    draw.rounded_rectangle((x0, y0, x1, y1), radius=CARD_RADIUS, fill=PALETTE["card"], outline=PALETTE["border"], width=2)

    inset = 16
    image_height = (y1 - y0) - inset * 2 - LABEL_HEIGHT
    image_size = ((x1 - x0) - inset * 2, image_height)
    image = render_panel(tile, image_size)
    mask = rounded_mask(image_size, 22)
    image_pos = (x0 + inset, y0 + inset)
    canvas.paste(image, image_pos, mask)

    stripe_y = y0 + inset + image_height - 8
    draw.rectangle((x0 + inset, stripe_y, x1 - inset, stripe_y + 8), fill=PALETTE[tile.accent])

    letter_box = (x0 + inset + 14, y0 + inset + 14, x0 + inset + 64, y0 + inset + 64)
    draw.rounded_rectangle(letter_box, radius=18, fill="#FFF9F2", outline=PALETTE["border"], width=1)
    draw.text((letter_box[0] + 17, letter_box[1] + 11), tile.panel_id, fill=PALETTE["ink"], font=PANEL_FONT)

    role_label = tile.role.title()
    role_width = int(draw.textlength(role_label, font=BADGE_FONT)) + 30
    role_x1 = x1 - inset - 14
    role_x0 = role_x1 - role_width
    role_y0 = y0 + inset + 16
    draw.rounded_rectangle((role_x0, role_y0, role_x1, role_y0 + 30), radius=15, fill=PALETTE[tile.role], outline=PALETTE[tile.role], width=1)
    draw.text((role_x0 + 14, role_y0 + 6), role_label, fill="#FFF9F2", font=BADGE_FONT)

    label_top = y0 + inset + image_height + 16
    label_lines = wrap_text(draw, tile.label, LABEL_FONT, image_size[0] - 20)
    draw.text((x0 + inset + 4, label_top), label_lines[0], fill=PALETTE["ink"], font=LABEL_FONT)
    if len(label_lines) > 1:
        draw.text((x0 + inset + 4, label_top + 28), label_lines[1], fill=PALETTE["ink"], font=LABEL_FONT)
        note_y = label_top + 62
    else:
        note_y = label_top + 36

    note_text = f"{tile.source_note} | {relative_path(tile.path.parent.parent if tile.path.name == 'contact_sheet.png' else tile.path)}"
    note_lines = wrap_text(draw, note_text, NOTE_FONT, image_size[0] - 20)
    for index, line in enumerate(note_lines[:2]):
        draw.text((x0 + inset + 4, note_y + index * 18), line, fill=PALETTE["muted"], font=NOTE_FONT)


def render_editorial_mosaic(board: Board, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    hero_width = 1120
    hero_height = 520
    right_width = CANVAS_SIZE[0] - MARGIN * 2 - hero_width - GAP
    small_height = (hero_height - GAP) // 2
    bottom_width = (CANVAS_SIZE[0] - MARGIN * 2 - GAP) // 2
    bottom_height = 304

    boxes = [
        (MARGIN, TOP_START, MARGIN + hero_width, TOP_START + hero_height),
        (MARGIN + hero_width + GAP, TOP_START, CANVAS_SIZE[0] - MARGIN, TOP_START + small_height),
        (MARGIN + hero_width + GAP, TOP_START + small_height + GAP, CANVAS_SIZE[0] - MARGIN, TOP_START + hero_height),
        (MARGIN, TOP_START + hero_height + GAP, MARGIN + bottom_width, TOP_START + hero_height + GAP + bottom_height),
        (MARGIN + bottom_width + GAP, TOP_START + hero_height + GAP, CANVAS_SIZE[0] - MARGIN, TOP_START + hero_height + GAP + bottom_height),
    ]
    for tile, box in zip(board.tiles, boxes):
        draw_tile(canvas, draw, tile, box)


def render_editorial_triptych(board: Board, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    column_width = (CANVAS_SIZE[0] - MARGIN * 2 - GAP * 2) // 3
    top_height = 594
    bottom_height = 264

    boxes = []
    for index in range(3):
        x0 = MARGIN + index * (column_width + GAP)
        boxes.append((x0, TOP_START, x0 + column_width, TOP_START + top_height))
    bottom_top = TOP_START + top_height + GAP
    for index in range(3):
        x0 = MARGIN + index * (column_width + GAP)
        boxes.append((x0, bottom_top, x0 + column_width, bottom_top + bottom_height))

    for tile, box in zip(board.tiles, boxes):
        draw_tile(canvas, draw, tile, box)


def render_board(board: Board) -> Image.Image:
    canvas = Image.new("RGB", CANVAS_SIZE, PALETTE["paper"])
    paint_background(canvas)
    draw = ImageDraw.Draw(canvas)
    draw_header(draw, board)

    if board.layout_family == "editorial_triptych":
        render_editorial_triptych(board, canvas, draw)
    else:
        render_editorial_mosaic(board, canvas, draw)

    footer_y = CANVAS_SIZE[1] - 94
    draw.line((MARGIN, footer_y - 18, CANVAS_SIZE[0] - MARGIN, footer_y - 18), fill=PALETTE["line"], width=2)
    footer_lines = wrap_text(draw, board.footer, FOOTER_FONT, CANVAS_SIZE[0] - MARGIN * 2)
    for index, line in enumerate(footer_lines[:2]):
        draw.text((MARGIN, footer_y + index * 22), line, fill=PALETTE["muted"], font=FOOTER_FONT)
    return canvas


def build_manifest() -> dict:
    return {
        "visual_language": "editorial-proof-boards",
        "narrative_layers": NARRATIVE_LAYERS,
        "boards": [
            {
                "filename": board.filename,
                "title": board.title,
                "layout_family": board.layout_family,
                "eyebrow": board.eyebrow,
                "tiles": [
                    {
                        "panel_id": tile.panel_id,
                        "role": tile.role,
                        "label": tile.label,
                        "source_note": tile.source_note,
                        "source_path": relative_path(tile.path),
                        "crop": tile.crop.as_dict(),
                    }
                    for tile in board.tiles
                ],
            }
            for board in BOARDS
        ],
    }


def save_outputs(images: dict[str, Image.Image], manifest: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, image in images.items():
        image.save(output_dir / filename, format="PNG", optimize=True)
    (output_dir / SHOWCASE_MANIFEST).write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--mirror-output-dir", default="", help="Optional second output directory to mirror the same files into.")
    args = parser.parse_args()

    generated = {}
    skipped = []
    for board in BOARDS:
        missing = [tile.path for tile in board.tiles if not tile.path.is_file()]
        if missing:
            skipped.append((board.filename, missing))
            continue
        generated[board.filename] = render_board(board)

    if not generated:
        print(f"WARNING: all {len(BOARDS)} boards skipped due to missing source images", file=sys.stderr)
        for filename, paths in skipped:
            print(f"  skipped: {filename} ({len(paths)} missing images)", file=sys.stderr)
    manifest = build_manifest()
    output_dir = Path(args.output_dir)
    save_outputs(generated, manifest, output_dir)

    if args.mirror_output_dir:
        save_outputs(generated, manifest, Path(args.mirror_output_dir))

    for filename in generated:
        print(filename)
    print(SHOWCASE_MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

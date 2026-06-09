#!/usr/bin/env python3
"""Generate a dependency-light PPTX deck for civil materials research."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape


NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_OFFICE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


@dataclass
class SlideImage:
    path: Path
    alt: str = "Figure"
    x: int = 6_700_000
    y: int = 1_520_000
    cx: int = 4_550_000
    cy: int = 3_950_000
    crop_left: int = 0
    crop_top: int = 0
    crop_right: int = 0
    crop_bottom: int = 0


@dataclass
class Slide:
    title: str
    bullets: list[str]
    notes: list[str] = field(default_factory=list)
    images: list[SlideImage] = field(default_factory=list)


PROJECT_REPORT_ZH = [
    Slide("题目", ["{title}", "汇报人：{presenter}", "日期：{date}"], ["开场说明课题、汇报人和本次汇报目标。"]),
    Slide("工程问题", ["服役中最关键的失效或不足是什么？", "现有材料或工艺为什么还不够？"], ["先讲工程痛点，不急着讲材料配方。"]),
    Slide("材料设计", ["材料体系：[填写]", "关键变量：[填写]", "预期作用机制：[填写]"], ["说明每个组分为什么加入，以及变量如何服务研究问题。"]),
    Slide("试验矩阵", ["性能测试：[填写]", "机理测试：[填写]", "耐久/服役测试：[填写]"], ["强调试验链条如何覆盖性能、机理和服役边界。"]),
    Slide("关键结果 1", ["核心结论：[填写]", "证据来源：[图/表/数据]", "工程意义：[填写]"], ["只讲一个核心趋势，避免把所有数据塞进一页。"]),
    Slide("关键结果 2", ["核心结论：[填写]", "证据来源：[图/表/数据]", "边界条件：[填写]"], ["补充第二个关键证据，并说明适用边界。"]),
    Slide("机理解释", ["直接证据：[FTIR/SEM/荧光/流变等]", "解释链条：[填写]", "不可过度外推的部分：[填写]"], ["区分直接证据和推断机制，避免过度因果。"]),
    Slide("局限与下一步", ["当前局限：[填写]", "可补充实验：[填写]", "下一步论文或试验计划：[填写]"], ["收束到下一步可执行动作。"]),
]

JOURNAL_CLUB_ZH = [
    Slide("文献信息", ["{title}", "期刊/年份：[填写]", "为什么这篇文章值得读：[填写]"], ["用一句话说明这篇文章和自己课题的关系。"]),
    Slide("研究问题", ["研究空白：[填写]", "工程问题：[填写]", "可借鉴角度：[填写]"], ["把作者的研究问题转化成自己能借鉴的问题。"]),
    Slide("材料体系", ["基体材料：[填写]", "改性剂：[填写]", "关键变量：[填写]"], ["不要只罗列材料，要讲变量为何重要。"]),
    Slide("试验链条", ["制备：[填写]", "性能测试：[填写]", "机理测试：[填写]", "耐久测试：[填写]"], ["指出试验链条是否完整。"]),
    Slide("图表证据 1", ["图/表：[填写]", "支持的 claim：[填写]", "注意事项：[填写]"], ["逐图讲 evidence，不把 caption 当结论。"]),
    Slide("图表证据 2", ["图/表：[填写]", "支持的 claim：[填写]", "注意事项：[填写]"], ["继续说明第二个证据及其边界。"]),
    Slide("机理与边界", ["直接证据：[填写]", "推断链条：[填写]", "适用边界：[填写]"], ["明确哪些是作者直接测到的，哪些只是解释。"]),
    Slide("我能借鉴什么", ["写作逻辑：[填写]", "试验设计：[填写]", "审稿风险：[填写]"], ["最后落到自己的选题和下一步实验。"]),
]

REVIEW_TALK_ZH = [
    Slide("综述范围", ["{title}", "材料体系：[填写]", "应用边界：[填写]"], ["先把综述边界讲清楚。"]),
    Slide("研究背景", ["工程需求：[填写]", "服役失效：[填写]", "为什么需要综述：[填写]"], ["把综述必要性讲成工程问题。"]),
    Slide("材料分类", ["体系 1：[填写]", "体系 2：[填写]", "体系 3：[填写]"], ["分类要服务后续评价，不只是罗列。"]),
    Slide("性能证据", ["关键性能：[填写]", "对比逻辑：[填写]", "证据缺口：[填写]"], ["强调不同研究之间可比性。"]),
    Slide("机理证据", ["化学证据：[填写]", "微观证据：[填写]", "未解决问题：[填写]"], ["区分性能归纳和机制证据。"]),
    Slide("耐久与服役", ["水损害/老化：[填写]", "施工条件：[填写]", "现场相关性：[填写]"], ["把实验结果拉回服役场景。"]),
    Slide("研究缺口", ["缺口 1：[填写]", "缺口 2：[填写]", "缺口 3：[填写]"], ["缺口必须能导向自己的实验。"]),
    Slide("我的选题切入", ["拟切入角度：[填写]", "需要补的实验：[填写]", "目标期刊：[填写]"], ["把综述变成可执行课题。"]),
]

PROJECT_REPORT_EN = [
    Slide("Title", ["{title}", "Presenter: {presenter}", "Date: {date}"], ["Introduce the topic and the purpose of this presentation."]),
    Slide("Engineering Problem", ["What fails in service?", "Why are current solutions insufficient?"], ["Start from the engineering problem before discussing formulation."]),
    Slide("Material Design", ["Material system: [fill]", "Design variable: [fill]", "Expected mechanism: [fill]"], ["Explain why each component is included."]),
    Slide("Experiment Matrix", ["Preparation: [fill]", "Performance tests: [fill]", "Mechanism tests: [fill]", "Durability tests: [fill]"], ["Connect each test to a claim."]),
    Slide("Key Result 1", ["Claim: [fill]", "Evidence: [figure/table/data]", "Reviewer-safe takeaway: [fill]"], ["Use one figure and one claim."]),
    Slide("Key Result 2", ["Claim: [fill]", "Evidence: [figure/table/data]", "Boundary: [fill]"], ["State the evidence boundary."]),
    Slide("Mechanism", ["Direct evidence: [fill]", "Interpretation: [fill]", "Claim strength: direct / inferred / hypothesis"], ["Separate measured evidence from inferred mechanism."]),
    Slide("Limitations and Next Work", ["Limitation: [fill]", "Next experiment: [fill]", "Paper angle: [fill]"], ["End with the next concrete step."]),
]

PRESETS = {
    ("project-report", "zh"): PROJECT_REPORT_ZH,
    ("journal-club", "zh"): JOURNAL_CLUB_ZH,
    ("review-talk", "zh"): REVIEW_TALK_ZH,
    ("project-report", "en"): PROJECT_REPORT_EN,
    ("journal-club", "en"): PROJECT_REPORT_EN,
    ("review-talk", "en"): PROJECT_REPORT_EN,
}


def parse_crop(value: str | None) -> tuple[int, int, int, int]:
    if not value:
        return 0, 0, 0, 0
    parts = [int(float(part.strip()) * 1000) for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("--crop must be left,top,right,bottom percentages")
    return tuple(max(0, min(100000, part)) for part in parts)  # type: ignore[return-value]


def parse_markdown(path: Path) -> list[Slide]:
    slides: list[Slide] = []
    current: Slide | None = None
    mode = "bullets"
    heading = re.compile(r"^##\s+(?:Slide\s+\d+\s*[-–]\s*)?(.+?)\s*$", re.I)
    image = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        match = heading.match(line)
        if match:
            current = Slide(match.group(1), [])
            slides.append(current)
            mode = "bullets"
            continue
        if current is None:
            continue
        img = image.search(line)
        if img:
            image_path = (path.parent / img.group(2)).resolve()
            current.images.append(SlideImage(path=image_path, alt=img.group(1) or "Figure"))
            continue
        if line.lower().startswith("speaker note"):
            mode = "notes"
            note = line.split(":", 1)[1].strip() if ":" in line else ""
            if note:
                current.notes.append(note)
            continue
        if line.startswith("- "):
            target = current.notes if mode == "notes" else current.bullets
            target.append(line[2:].strip())
        elif mode == "notes" and line:
            current.notes.append(line)
    return slides


def slide_image_from_dict(item: dict, base_dir: Path) -> SlideImage:
    raw_path = Path(str(item.get("path", "")))
    if not raw_path:
        raise ValueError("Image item requires a path.")
    image_path = raw_path if raw_path.is_absolute() else (base_dir / raw_path)
    crop = item.get("crop")
    if isinstance(crop, dict):
        crop_values = (
            int(float(crop.get("left", 0)) * 1000),
            int(float(crop.get("top", 0)) * 1000),
            int(float(crop.get("right", 0)) * 1000),
            int(float(crop.get("bottom", 0)) * 1000),
        )
    elif isinstance(crop, str):
        crop_values = parse_crop(crop)
    else:
        crop_values = (0, 0, 0, 0)
    return SlideImage(
        path=image_path.resolve(),
        alt=str(item.get("alt", "Figure")),
        x=int(item.get("x", 6_700_000)),
        y=int(item.get("y", 1_520_000)),
        cx=int(item.get("cx", 4_550_000)),
        cy=int(item.get("cy", 3_950_000)),
        crop_left=crop_values[0],
        crop_top=crop_values[1],
        crop_right=crop_values[2],
        crop_bottom=crop_values[3],
    )


def parse_json(path: Path) -> list[Slide]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("slides", data if isinstance(data, list) else [])
    slides: list[Slide] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        notes = item.get("notes", [])
        if isinstance(notes, str):
            notes = [notes]
        images = [slide_image_from_dict(img, path.parent) for img in item.get("images", []) if isinstance(img, dict)]
        slides.append(
            Slide(
                title=str(item.get("title", "Untitled")),
                bullets=[str(x) for x in item.get("bullets", [])],
                notes=[str(x) for x in notes],
                images=images,
            )
        )
    return slides


def preset(deck_type: str, language: str) -> list[Slide]:
    return [Slide(s.title, list(s.bullets), list(s.notes), list(s.images)) for s in PRESETS.get((deck_type, language), PROJECT_REPORT_ZH)]


def substitute(slides: list[Slide], title: str, presenter: str) -> list[Slide]:
    today = dt.date.today().isoformat()
    values = {"title": title, "presenter": presenter, "date": today}

    def safe_format(text: str) -> str:
        try:
            return text.format(**values)
        except (KeyError, ValueError):
            return text

    return [
        Slide(
            safe_format(slide.title),
            [safe_format(bullet) for bullet in slide.bullets],
            [safe_format(note) for note in slide.notes],
            slide.images,
        )
        for slide in slides
    ]


def rels(items: list[tuple[str, str, str]]) -> str:
    body = "".join(
        f'<Relationship Id="{rid}" Type="{escape(kind)}" Target="{escape(target)}"/>'
        for rid, kind, target in items
    )
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{NS_REL}">{body}</Relationships>'


def text_body(lines: list[str], font_size: int = 2400, bullet_first: bool = False) -> str:
    if not lines:
        lines = ["[填写]"]
    paragraphs = []
    for idx, line in enumerate(lines):
        bullet = '<a:pPr lvl="0"><a:buChar char="•"/></a:pPr>' if bullet_first or idx else ""
        paragraphs.append(
            f"<a:p>{bullet}<a:r><a:rPr lang=\"zh-CN\" sz=\"{font_size}\"/><a:t>{escape(line)}</a:t></a:r></a:p>"
        )
    return "".join(paragraphs)


def shape(shape_id: int, name: str, x: int, y: int, cx: int, cy: int, lines: list[str], font_size: int) -> str:
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{shape_id}" name="{escape(name)}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    {text_body(lines, font_size)}
  </p:txBody>
</p:sp>"""


def image_shape(shape_id: int, rel_id: str, image: SlideImage) -> str:
    crop = ""
    if image.crop_left or image.crop_top or image.crop_right or image.crop_bottom:
        crop = f'<a:srcRect l="{image.crop_left}" t="{image.crop_top}" r="{image.crop_right}" b="{image.crop_bottom}"/>'
    return f"""
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="{shape_id}" name="{escape(image.alt)}" descr="{escape(image.alt)}"/>
    <p:cNvPicPr/>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="{rel_id}"/>
    {crop}
    <a:stretch><a:fillRect/></a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm><a:off x="{image.x}" y="{image.y}"/><a:ext cx="{image.cx}" cy="{image.cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
</p:pic>"""


def slide_xml(slide: Slide, slide_no: int, image_rels: list[str]) -> str:
    title = shape(2, "Title", 640000, 420000, 10800000, 760000, [slide.title], 3400)
    body_width = 5_650_000 if slide.images else 10_300_000
    body = shape(3, "Content", 900000, 1450000, body_width, 4500000, slide.bullets, 2350)
    footer = shape(4, "Footer", 900000, 6250000, 10300000, 300000, [f"Civil materials research · {slide_no}"], 1150)
    images = "".join(image_shape(10 + idx, rel_id, image) for idx, (rel_id, image) in enumerate(zip(image_rels, slide.images), 1))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="F7F4EC"/></a:solidFill></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {title}
      {body}
      {images}
      {footer}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def notes_slide_xml(slide: Slide, slide_no: int) -> str:
    notes = slide.notes or ["[Speaker notes]"]
    notes_shape = shape(2, "Speaker Notes", 685800, 914400, 5486400, 5486400, notes, 1800)
    title_shape = shape(3, "Slide Title", 685800, 260000, 5486400, 420000, [f"Slide {slide_no}: {slide.title}"], 1700)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {title_shape}
      {notes_shape}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>"""


def content_types(slide_count: int, image_exts: set[str]) -> str:
    defaults = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
    ]
    for ext in sorted(image_exts):
        ctype = "image/png" if ext == "png" else "image/jpeg" if ext in {"jpg", "jpeg"} else f"image/{ext}"
        defaults.append(f'<Default Extension="{ext}" ContentType="{ctype}"/>')
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
        '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    overrides.extend(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    overrides.extend(
        f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        + "".join(defaults)
        + "".join(overrides)
        + "</Types>"
    )


def presentation_xml(slide_count: int) -> str:
    ids = "".join(f'<p:sldId id="{256+i}" r:id="rId{2+i}"/>' for i in range(slide_count))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:notesMasterIdLst><p:notesMasterId r:id="rId{slide_count + 2}"/></p:notesMasterIdLst>
  <p:sldIdLst>{ids}</p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle><a:defPPr><a:defRPr lang="zh-CN"/></a:defPPr></p:defaultTextStyle>
</p:presentation>"""


def presentation_rels(slide_count: int) -> str:
    items = [("rId1", f"{NS_OFFICE_REL}/slideMaster", "slideMasters/slideMaster1.xml")]
    items.extend((f"rId{2+i}", f"{NS_OFFICE_REL}/slide", f"slides/slide{i+1}.xml") for i in range(slide_count))
    items.append((f"rId{slide_count+2}", f"{NS_OFFICE_REL}/notesMaster", "notesMasters/notesMaster1.xml"))
    items.append((f"rId{slide_count+3}", f"{NS_OFFICE_REL}/presProps", "presProps.xml"))
    items.append((f"rId{slide_count+4}", f"{NS_OFFICE_REL}/viewProps", "viewProps.xml"))
    return rels(items)


SLIDE_MASTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""

SLIDE_LAYOUT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="obj" preserve="1">
  <p:cSld name="Civil Materials Layout"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

NOTES_MASTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="{NS_OFFICE_REL}" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
</p:notesMaster>"""

THEME = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Civil Materials">
  <a:themeElements>
    <a:clrScheme name="Civil Materials">
      <a:dk1><a:srgbClr val="1F2933"/></a:dk1><a:lt1><a:srgbClr val="F7F4EC"/></a:lt1>
      <a:dk2><a:srgbClr val="374151"/></a:dk2><a:lt2><a:srgbClr val="E8E1D2"/></a:lt2>
      <a:accent1><a:srgbClr val="A16207"/></a:accent1><a:accent2><a:srgbClr val="3F6B5B"/></a:accent2>
      <a:accent3><a:srgbClr val="416788"/></a:accent3><a:accent4><a:srgbClr val="8B5E34"/></a:accent4>
      <a:accent5><a:srgbClr val="5B6C5D"/></a:accent5><a:accent6><a:srgbClr val="7C2D12"/></a:accent6>
      <a:hlink><a:srgbClr val="416788"/></a:hlink><a:folHlink><a:srgbClr val="7C2D12"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Civil Materials Fonts">
      <a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface="Microsoft YaHei"/></a:majorFont>
      <a:minorFont><a:latin typeface="Aptos"/><a:ea typeface="Microsoft YaHei"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Civil Materials Format"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def core_props(title: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{escape(title)}</dc:title>
  <dc:creator>civil-materials-pptx</dc:creator>
  <cp:lastModifiedBy>civil-materials-pptx</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""


def media_extension(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    if ext == "jpe":
        ext = "jpg"
    if ext not in {"png", "jpg", "jpeg"}:
        raise ValueError(f"Unsupported image extension for {path}; use PNG or JPEG.")
    return ext


def write_pptx(slides: list[Slide], output: Path, title: str) -> None:
    image_exts = {media_extension(image.path) for slide in slides for image in slide.images}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(len(slides), image_exts))
        zf.writestr("_rels/.rels", rels([
            ("rId1", f"{NS_OFFICE_REL}/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", f"{NS_OFFICE_REL}/extended-properties", "docProps/app.xml"),
        ]))
        zf.writestr("docProps/core.xml", core_props(title))
        zf.writestr("docProps/app.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>civil-materials-pptx</Application><Slides>{len(slides)}</Slides></Properties>')
        zf.writestr("ppt/presentation.xml", presentation_xml(len(slides)))
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(len(slides)))
        zf.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([
            ("rId1", f"{NS_OFFICE_REL}/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", f"{NS_OFFICE_REL}/theme", "../theme/theme1.xml"),
        ]))
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([
            ("rId1", f"{NS_OFFICE_REL}/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]))
        zf.writestr("ppt/notesMasters/notesMaster1.xml", NOTES_MASTER)
        zf.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([
            ("rId1", f"{NS_OFFICE_REL}/theme", "../theme/theme1.xml"),
        ]))
        zf.writestr("ppt/theme/theme1.xml", THEME)
        zf.writestr("ppt/presProps.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
        zf.writestr("ppt/viewProps.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')

        media_id = 1
        for idx, slide in enumerate(slides, 1):
            slide_rels = [("rId1", f"{NS_OFFICE_REL}/slideLayout", "../slideLayouts/slideLayout1.xml")]
            image_rel_ids = []
            for image in slide.images:
                if not image.path.exists():
                    raise FileNotFoundError(f"Image not found: {image.path}")
                ext = media_extension(image.path)
                media_name = f"image{media_id}.{ext}"
                zf.writestr(f"ppt/media/{media_name}", image.path.read_bytes())
                rel_id = f"rId{len(slide_rels) + 1}"
                slide_rels.append((rel_id, f"{NS_OFFICE_REL}/image", f"../media/{media_name}"))
                image_rel_ids.append(rel_id)
                media_id += 1
            slide_rels.append((f"rId{len(slide_rels) + 1}", f"{NS_OFFICE_REL}/notesSlide", f"../notesSlides/notesSlide{idx}.xml"))
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide_xml(slide, idx, image_rel_ids))
            zf.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", rels(slide_rels))
            zf.writestr(f"ppt/notesSlides/notesSlide{idx}.xml", notes_slide_xml(slide, idx))
            zf.writestr(f"ppt/notesSlides/_rels/notesSlide{idx}.xml.rels", rels([
                ("rId1", f"{NS_OFFICE_REL}/slide", f"../slides/slide{idx}.xml"),
                ("rId2", f"{NS_OFFICE_REL}/notesMaster", "../notesMasters/notesMaster1.xml"),
            ]))


def attach_cli_image(slides: list[Slide], image_path: str | None, slide_no: int, crop: str | None) -> None:
    if not image_path:
        return
    if slide_no < 1 or slide_no > len(slides):
        raise ValueError(f"--image-slide must be between 1 and {len(slides)}")
    left, top, right, bottom = parse_crop(crop)
    slides[slide_no - 1].images.append(
        SlideImage(
            path=Path(image_path).resolve(),
            alt="Inserted figure",
            crop_left=left,
            crop_top=top,
            crop_right=right,
            crop_bottom=bottom,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default="Civil materials research presentation")
    parser.add_argument("--presenter", default="")
    parser.add_argument("--input", help="Optional Markdown or JSON outline generated by civil-materials-paper2ppt.")
    parser.add_argument("--deck-type", choices=["project-report", "journal-club", "review-talk"], default="project-report")
    parser.add_argument("--language", choices=["zh", "en"], default="zh")
    parser.add_argument("--image", help="Optional PNG/JPEG figure to embed into one slide.")
    parser.add_argument("--image-slide", type=int, default=2, help="1-based slide number for --image.")
    parser.add_argument("--crop", help="Optional image crop as left,top,right,bottom percentages, e.g. 5,0,5,0.")
    parser.add_argument("--output", default="civil-materials-deck.pptx")
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        slides = parse_json(input_path) if input_path.suffix.lower() == ".json" else parse_markdown(input_path)
    else:
        slides = preset(args.deck_type, args.language)
    if not slides:
        raise SystemExit("No slides found in input outline.")
    slides = substitute(slides, args.title, args.presenter)
    attach_cli_image(slides, args.image, args.image_slide, args.crop)
    output = Path(args.output)
    write_pptx(slides, output, args.title)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Mechanical checks for edu-ppt's lesson-review or three-Word delivery phase.

Uses only the Python standard library. A successful exit means only that the
implemented automatic checks passed; it never means that the product is verified.
Run with --help for the CLI. JSON goes to stdout; exit codes are 0 (automatic
checks pass), 1 (document failure), and 2 (invalid CLI arguments).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path
import posixpath
import re
import struct
import sys
from urllib.parse import unquote
import zipfile
import xml.etree.ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WS = "http://purl.oclc.org/ooxml/wordprocessingml/main"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT = "http://schemas.openxmlformats.org/package/2006/content-types"
WORD_NAMESPACES = {W, WS}
OUTLINE_FIELDS = ("页面标题", "页面文字")
VISUAL_FIELDS = ("画面风格", "添加元素", "文字字体与重点标注", "布局排版", "镜头与光影", "画面去重与统一约束")
LESSON_SECTIONS = ("课程基本信息", "设计依据", "设计理念", "教学目标", "教学重点、难点与突破策略", "教学准备", "教-学-评一体化设计", "教学过程", "板书设计", "作业设计", "教学评价", "教学反思预设与课后改进")
METADATA_FIELDS = ("课题", "学科与学段/年级", "教材依据", "课时安排", "所属单元/主题及大概念", "课型", "授课对象", "设计者/日期")
SCRIPT_PAGE = re.compile(r"^P([0-9]+)\s+(.+)$", re.ASCII)
SECTION_PREFIX = re.compile(r"^(?:(?:第[一二三四五六七八九十百\d]+[部分章节])|(?:[（(]?[一二三四五六七八九十百\d]+[）).、．]))\s*")
PAGE = re.compile(r"^第\s*([0-9]+)\s*页\s*[:：]?$", re.ASCII)
PAGE_LIKE = re.compile(r"^第\s*[0-9一二三四五六七八九十]+\s*页")
EXTRA_OUTLINE_FIELDS = ("教师指导", "教师引导", "教学指导", "设计意图", "设计说明", "重点标注", "备注")
EXTRA_VISUAL_FIELDS = ("页面标题", "页面文字", "教师指导", "教师引导", "教学指导", "设计意图", "设计说明", "重点标注", "备注", "说明")
MANUAL_CHECKS = [
    {"id": "source_and_cross_file_semantics", "status": "not_assessed", "required": "逐项核对冻结教材、来源台账与三 Word 的课题、对象、目标、术语、事实、引文、活动、时间和来源覆盖；机械页序一致不代表语义一致。"},
    {"id": "teaching_and_field_quality", "status": "not_assessed", "required": "核实具体课标条款及政策来源，检查2—4条目标与活动/评价/量规对齐、重难点的依据和突破路径、段落式过程的学习推进、学生行动、评价证据及支架、时间估算与分配及反思预判；字符数、标签和时间加总不能证明真实或有效。"},
    {"id": "board_quality", "status": "not_assessed", "required": "检查文字板书的板书主线、副板书、生成时机及课题专属性，层级和关系可在黑板一屏呈现、随教学逐步生成；默认不以板书图片代替。"},
    {"id": "script_color_and_delivery", "status": "not_assessed", "required": "检查逐字稿实际DOCX口播黑色、提示红色且单独【】标记；P页标题对应页纲，问题后有合理回应空间，条件式应对不冒充实际学生发言，反馈和过渡连贯。结构脚本不验证字体颜色或真实讲授节奏。"},
    {"id": "rendered_word_pages", "status": "not_assessed", "required": "渲染三份 Word 并逐页检查空白/缺页、裁切、溢出、表格、字体、页序、对比度及正文重点强调；本脚本不渲染，也不验证 Office/WPS 打开效果。"},
    {"id": "full_verification_verdict", "status": "not_assessed", "required": "依照 deliverables.md 完成全部格式与跨文件矩阵判定后才能进入 verified；本 JSON 只提供部分机械检查结果。可选 PPTX 的 WPS 检查须另行执行。"},
]


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def attr(node: ET.Element, name: str, default=None):
    for key, value in node.attrib.items():
        if local(key) == name:
            return value
    return default


def child(node: ET.Element | None, name: str):
    if node is not None:
        return next((x for x in node if local(x.tag) == name), None)
    return None


def word_paragraph(node: ET.Element) -> bool:
    return local(node.tag) == "p" and node.tag.split("}")[0].lstrip("{") in WORD_NAMESPACES


@dataclass
class Line:
    text: str
    location: str
    numbered: bool = False
    table: str | None = None
    row: str | None = None
    cell: int | None = None
    row_cells: int = 0
    images: tuple = ()


class Report:
    def __init__(self, phase="final"):
        self.phase = phase
        self.errors = []
        self.documents = {}
        self.page_counts = {}

    def fail(self, doc, code, message, line=None):
        self.errors.append({"document": doc, "file": self.documents.get(doc, {}).get("path"), "code": code, "location": line.location if line else "package / document", "message": message})

    def output(self):
        manual = [dict(check) for check in MANUAL_CHECKS]
        if self.phase == "plan-review":
            manual = [check for check in manual if check["id"] != "script_color_and_delivery"]
            replacements = {
                "source_and_cross_file_semantics": "核对冻结教材、来源台账与待确认教学设计的理解、目标、事实、活动及来源覆盖；本阶段不检查或声称已生成 PPT 页纲和逐字稿。",
                "teaching_and_field_quality": "核实教案具体课标、课文专属性、重难点突破、目标与任务/活动/评价对齐、时间分配及反思预判真实性；字符数和时间相加不证明教学有效。",
                "rendered_word_pages": "渲染本阶段唯一教学设计Word，逐页检查十二模块模板分级标题、深红重点、连贯段落式过程、文字板书、量规、页序、裁切与溢出；脚本不渲染或验证 Office/WPS。",
                "full_verification_verdict": "仅判定教学设计待确认稿的适用检查；未制作的页纲、视觉蓝图和逐字稿不纳入此阶段，也不能声称全套交付完成。",
            }
            for check in manual:
                check["required"] = replacements.get(check["id"], check["required"])
        return {"automatic_checks_pass": not self.errors, "phase": self.phase, "scope": ("lesson-plan review only" if self.phase == "plan-review" else "final three-Word package") + ": OOXML integrity and mechanical text/table/image-header checks only; not a complete DOCX schema, rendering, semantic, or WPS verdict", "documents": self.documents, "page_counts": self.page_counts, "errors": self.errors, "manual_checks_required": manual}


def paragraph_text(p: ET.Element) -> str:
    """Join split runs, retaining breaks; nested text-box paragraphs are separate."""
    chunks = []

    def walk(node):
        for item in node:
            name = local(item.tag)
            if word_paragraph(item):
                continue
            if name in {"t", "delText"}:
                chunks.append(item.text or "")
            elif name in {"br", "cr"}:
                chunks.append("\n")
            elif name == "tab":
                chunks.append("\t")
            else:
                walk(item)

    walk(p)
    return "".join(chunks)


def numbering_resolver(styles_root):
    styles = {}
    default_style = None
    if styles_root is not None:
        for s in styles_root:
            if local(s.tag) == "style" and attr(s, "type") == "paragraph":
                styles[attr(s, "styleId")] = s
                if attr(s, "default") in {"1", "true", "on"}:
                    default_style = attr(s, "styleId")

    def num_value(ppr):
        num = child(child(ppr, "numPr"), "numId")
        return attr(num, "val") if num is not None else None

    def resolve(p):
        ppr = child(p, "pPr")
        value = num_value(ppr)
        if value is not None:
            return value != "0"
        pstyle = child(ppr, "pStyle")
        sid = attr(pstyle, "val") if pstyle is not None else default_style
        seen = set()
        while sid in styles and sid not in seen:
            seen.add(sid)
            s = styles[sid]
            value = num_value(child(s, "pPr"))
            if value is not None:
                return value != "0"
            base = child(s, "basedOn")
            sid = attr(base, "val") if base is not None else None
        return False

    return resolve


def extract_paragraphs(root, part, numbered):
    """XML order preserves paragraphs interleaved with table rows/cells.

    Text boxes are scanned but excluded from the linear contract, because their
    visual reading order cannot be inferred from their XML anchor position.
    """
    body, scan = [], []

    def walk(node, path, in_textbox=False, table=None, row=None, cell=None, row_cells=0):
        in_textbox = in_textbox or local(node.tag) == "txbxContent"
        if local(node.tag) == "tbl":
            table, row, cell, row_cells = f"{part} / {path}", None, None, 0
        if local(node.tag) == "tr":
            row, cell = f"{part} / {path}", None
            row_cells = sum(local(item.tag) == "tc" for item in node)
        if word_paragraph(node):
            value = paragraph_text(node)
            loc = f"{part} / {path}"
            scan.append(Line(value, loc, numbered(node)))
            if not in_textbox:
                images = tuple(attr(item, "embed") or attr(item, "id") or "unembedded-image"
                               for item in node.iter() if local(item.tag) in {"blip", "imagedata"})
                for n, text in enumerate(value.splitlines(), 1):
                    if text.strip():
                        body.append(Line(text.strip(), f"{loc} / line {n}", numbered(node), table, row, cell, row_cells, images))
                if images and not value.strip():
                    body.append(Line("", loc, numbered(node), table, row, cell, row_cells, images))
        counts = {}
        for item in node:
            tag = local(item.tag)
            counts[tag] = counts.get(tag, 0) + 1
            walk(item, f"{path}/{tag}[{counts[tag]}]", in_textbox, table, row,
                 counts[tag] if tag == "tc" else cell, row_cells)

    walk(root, local(root.tag))
    return body, scan


def image_header(data):
    """Check supported raster signature/dimensions; full decoding remains manual."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        if len(data) >= 33 and data[8:16] == b"\x00\x00\x00\rIHDR":
            width, height = struct.unpack(">II", data[16:24])
            if width and height:
                return {"format": "PNG", "width": width, "height": height}
        return None
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 4 <= len(data):
            if data[offset] != 255:
                return None
            while offset < len(data) and data[offset] == 255:
                offset += 1
            if offset >= len(data):
                return None
            marker = data[offset]
            offset += 1
            if marker in {0xD8, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if marker in {0xD9, 0xDA} or offset + 2 > len(data):
                return None
            length = int.from_bytes(data[offset:offset + 2], "big")
            if length < 2 or offset + length > len(data):
                return None
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                if length >= 8:
                    height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
                    if width and height:
                        return {"format": "JPEG", "width": width, "height": height}
                return None
            offset += length
    return None


def load_docx(path, key, report):
    report.documents[key] = {"path": str(Path(path).resolve()), "package_checks_pass": False}
    try:
        with zipfile.ZipFile(path) as package:
            names = package.namelist()
            if len(names) != len(set(names)):
                raise ValueError("ZIP contains duplicate part names")
            for required in ("[Content_Types].xml", "_rels/.rels", "word/document.xml"):
                if required not in names:
                    raise ValueError(f"required part is missing: {required}")
            damaged = package.testzip()
            if damaged:
                raise ValueError(f"ZIP CRC check failed: {damaged}")
            roots = {}
            for name in names:
                if name.endswith((".xml", ".rels")):
                    try:
                        roots[name] = ET.fromstring(package.read(name))
                    except ET.ParseError as exc:
                        raise ValueError(f"malformed XML in {name}: {exc}") from exc
            types = roots["[Content_Types].xml"]
            if types.tag != f"{{{CONTENT}}}Types":
                raise ValueError("invalid [Content_Types].xml root")
            main_types = [x.get("ContentType", "") for x in types if x.get("PartName") == "/word/document.xml"]
            if main_types != ["application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"]:
                raise ValueError("word/document.xml must have the DOCX document main content type")
            main_rel = [x for x in roots["_rels/.rels"] if x.get("Type", "").endswith("/officeDocument")]
            if len(main_rel) != 1 or main_rel[0].get("TargetMode") == "External" or posixpath.normpath(main_rel[0].get("Target", "").lstrip("/")) != "word/document.xml":
                raise ValueError("package must have one internal officeDocument relationship to word/document.xml")
            for name, root in roots.items():
                if not name.endswith(".rels"):
                    continue
                if root.tag != f"{{{PKG_REL}}}Relationships":
                    raise ValueError(f"invalid relationship root: {name}")
                source_dir = posixpath.dirname(posixpath.dirname(name)) if name != "_rels/.rels" else ""
                ids = set()
                for rel in root:
                    rid = rel.get("Id")
                    if not rid or rid in ids or not rel.get("Type") or not rel.get("Target"):
                        raise ValueError(f"invalid or duplicate relationship in {name}")
                    ids.add(rid)
                    if rel.get("TargetMode") == "External":
                        continue
                    target = unquote(rel.get("Target").split("#", 1)[0])
                    resolved = posixpath.normpath(target.lstrip("/") if target.startswith("/") else posixpath.join(source_dir, target))
                    if resolved not in names:
                        raise ValueError(f"missing relationship target: {name} -> {resolved}")
            root = roots["word/document.xml"]
            if local(root.tag) != "document" or root.tag.split("}")[0].lstrip("{") not in WORD_NAMESPACES or child(root, "body") is None:
                raise ValueError("word/document.xml has no Word document/body")
            if any(local(node.tag) == "altChunk" for node in root.iter()):
                raise ValueError("word/document.xml contains altChunk content; normalize it to native Word paragraphs/tables before text checks")
            resolver = numbering_resolver(roots.get("word/styles.xml"))
            body, scan = extract_paragraphs(root, "word/document.xml", resolver)
            image_rels = {}
            for rel in roots.get("word/_rels/document.xml.rels", []):
                if rel.get("Type", "").endswith("/image"):
                    info = None
                    if rel.get("TargetMode") != "External":
                        target = unquote(rel.get("Target").split("#", 1)[0])
                        resolved = posixpath.normpath(target.lstrip("/") if target.startswith("/") else posixpath.join("word", target))
                        info = image_header(package.read(resolved))
                    image_rels[rel.get("Id")] = info
            for name, root in roots.items():
                if name.startswith("word/") and name != "word/document.xml":
                    _, auxiliary = extract_paragraphs(root, name, resolver)
                    scan.extend(auxiliary)
            report.documents[key].update(package_checks_pass=True, body_lines=len(body), scanned_paragraphs=len(scan), embedded_image_headers=image_rels)
            return body, scan
    except (OSError, ValueError, KeyError, RuntimeError, zipfile.BadZipFile) as exc:
        report.fail(key, "docx_package", str(exc))
        return None


def banned_words(scan, key, report):
    patterns = [] if key == "lesson_plan" else [("banned_teaching_period", re.compile(r"课\s*时"), "出现禁用的教学时段词语（课时及其变体）")]
    if key == "lesson_plan":
        slide = r"(?:P\s*P\s*T(?:X)?|PowerPoint|幻灯片|课件)"
        page_number = r"[\d一二三四五六七八九十百XxNn]+\s*(?:[—–\-～~至]\s*[\d一二三四五六七八九十百XxNn]+\s*)?页"
        patterns.append(("production_note_in_plan", re.compile(
            slide + r"[^\n。；;]{0,24}?(?:" + page_number + r"|页数|页码|页序|对应页面)"
            + r"|对应\s*" + slide + r"\s*第|对应页(?:面|码)\s*[:：]|AI生成提示词", re.I),
            "教学设计不得出现PPT总页数、页码、页面对应或制作提示信息；映射只存内部记录"))
    for line in scan:
        for code, pattern, message in patterns:
            found = pattern.search(line.text)
            if found:
                report.fail(key, code, f"{message}：{found.group(0)!r}", line)


def heading_value(text, label):
    text = SECTION_PREFIX.sub("", text.strip())
    if text == label:
        return ""
    match = re.fullmatch(re.escape(label) + r"\s*[:：]\s*(.*)", text)
    return match.group(1) if match else None


def field_match(text, labels):
    for label in labels:
        match = re.fullmatch(r"(.*?)" + re.escape(label) + r"\s*(?:[:：]\s*(.*))?", text)
        if match:
            return label, match.group(1), match.group(2) or ""
    return None


def validate_fields(lines, fields, key, report, context, no_prefix=False, extra_fields=()):
    found, active, values = [], None, {}
    for line in lines:
        match = field_match(line.text, fields)
        if match:
            name, prefix, value = match
            found.append((name, line))
            values.setdefault(name, []).append(value)
            active = name
            if no_prefix and (prefix.strip() or line.numbered):
                report.fail(key, "field_list_prefix", f"{context}：{name} 前不得有数字、字母、项目符号或 Word 自动列表编号", line)
            elif prefix.strip():
                report.fail(key, "field_prefix", f"{context}：字段必须直接以 {name} 开始", line)
        else:
            extra = field_match(line.text, extra_fields)
            if extra:
                report.fail(key, "extra_field", f"{context}：出现合同外字段 {extra[0]}", line)
            if active:
                values[active][-1] += "\n" + line.text
            elif line.text.strip():
                report.fail(key, "unassigned_text", f"{context}：固定字段之前出现未归属文字：{line.text[:60]}", line)
    sequence = [name for name, _ in found]
    if sequence != list(fields):
        report.fail(key, "field_sequence", f"{context}：字段须各一次并依次为 {list(fields)}；实际为 {sequence}", found[0][1] if found else (lines[0] if lines else None))
    for name, line in found:
        if any(not value.strip() for value in values[name]):
            report.fail(key, "empty_field", f"{context}：{name} 为空", line)


def page_blocks(lines, key, report, context, pattern=PAGE):
    blocks = []
    for line in lines:
        match = pattern.fullmatch(line.text)
        if match:
            blocks.append((int(match.group(1)), line, []))
        elif PAGE_LIKE.match(line.text) or (key == "speaker_script" and re.match(r"^P[0-9]+(?:\s|$)", line.text)):
            report.fail(key, "page_heading", f"{context}：须用P1 页面标题" if key == "speaker_script" else f"{context}：页标题须单独使用 第X页（X 为阿拉伯数字）", line)
        elif blocks:
            blocks[-1][2].append(line)
        else:
            report.fail(key, "text_before_page", f"{context}：第一个页码之前有未归属文字：{line.text[:60]}", line)
    numbers = [number for number, _, _ in blocks]
    if not numbers:
        report.fail(key, "missing_pages", f"{context}：没有找到页块")
    for index, (number, line, _) in enumerate(blocks, 1):
        if number != index:
            report.fail(key, "page_sequence", f"{context}：第 {index} 个页块应为第{index}页，实际为第{number}页（重复、缺页或乱序）", line)
    return blocks


def outline_visual(lines, report, expected):
    key = "outline_visual"
    headings = [(i, name) for i, line in enumerate(lines) for name in ("PPT页纲", "视觉蓝图") if heading_value(line.text, name) == ""]
    if [name for _, name in headings] != ["PPT页纲", "视觉蓝图"]:
        report.fail(key, "combined_sections", "必须恰好有 PPT页纲、视觉蓝图 两个有标签的部分，且按此顺序出现", lines[headings[0][0]] if headings else None)
        return None
    outline_start, visual_start = headings[0][0], headings[1][0]
    outline = page_blocks(lines[outline_start + 1:visual_start], key, report, "PPT页纲")
    visual = page_blocks(lines[visual_start + 1:], key, report, "视觉蓝图")
    for number, _, content in outline:
        validate_fields(content, OUTLINE_FIELDS, key, report, f"PPT页纲/第{number}页", extra_fields=EXTRA_OUTLINE_FIELDS)
    for number, _, content in visual:
        validate_fields(content, VISUAL_FIELDS, key, report, f"视觉蓝图/第{number}页", no_prefix=True, extra_fields=EXTRA_VISUAL_FIELDS)
    first, second = [x[0] for x in outline], [x[0] for x in visual]
    report.page_counts.update(outline=len(first), visual_blueprint=len(second))
    if first != second:
        report.fail(key, "page_correspondence", f"页纲页序 {first} 与视觉蓝图页序 {second} 不一致", lines[visual_start])
    if expected is not None and len(first) != expected:
        report.fail(key, "expected_page_count", f"冻结页数为 {expected}，页纲实际有 {len(first)} 个页块", lines[outline_start])
    return first


def speaker_script(lines, report, approved, expected):
    # A cover/title before the first page is allowed in a standalone script.
    start = next((i for i, line in enumerate(lines) if re.match(r"^P[0-9]+(?:\s|$)", line.text) or PAGE_LIKE.match(line.text)), len(lines))
    blocks = page_blocks(lines[start:], "speaker_script", report, "逐字稿", SCRIPT_PAGE)
    for number, _, content in blocks:
        speech = []
        for line in content:
            if re.match(r"^师\s*[:：]\s*\S", line.text):
                speech.append(line)
            elif re.fullmatch(r"【\s*\S.*】", line.text):
                continue
            else:
                report.fail("speaker_script", "script_paragraph_type", "逐字稿用师：口播或【非口播提示】段落，不沿用旧五字段或无标记说明", line)
        if not speech:
            report.fail("speaker_script", "missing_teacher_speech", f"P{number}缺少可讲的师：口播", content[0] if content else None)
    sequence = [x[0] for x in blocks]
    report.page_counts["speaker_script"] = len(sequence)
    if approved is not None and sequence != approved:
        report.fail("speaker_script", "page_correspondence", f"逐字稿页序 {sequence} 与页纲页序 {approved} 不一致", blocks[0][1] if blocks else None)
    if expected is not None and len(sequence) != expected:
        report.fail("speaker_script", "expected_page_count", f"冻结页数为 {expected}，逐字稿实际有 {len(sequence)} 个页块", blocks[0][1] if blocks else None)


def chinese_count(text):
    return sum(1 for char in text if 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FA1F)


def lesson_heading(text):
    text = SECTION_PREFIX.sub("", text.strip())
    text = re.sub(r"教[—–－-]学[—–－-]评", "教-学-评", text)
    text = text.replace("教学重点与难点", "教学重点、难点与突破策略")
    if text.startswith("教学反思预设") and not text.startswith("教学反思预设与课后改进"):
        text = text.replace("教学反思预设", "教学反思预设与课后改进", 1)
    return next((label for label in LESSON_SECTIONS
                 if text == label or re.fullmatch(re.escape(label) + r"\s*[（(].*[）)]", text)), None)


def named_sections(lines, labels, report, context, optional=()):
    """Split native subsection labels without treating their body text as labels."""
    found = []
    for index, line in enumerate(lines):
        # The template annotates labels with parenthetical filling instructions.
        text = re.sub(r"[（(][^（）()]*[）)](?=\s*[:：]|$)", "", line.text)
        text = SECTION_PREFIX.sub("", text)
        if text.startswith("重点"):
            text = "教学" + text
        elif text.startswith("难点") and not text.startswith(("难点一", "难点二")):
            text = "教学" + text
        for label in labels:
            value = heading_value(text, label)
            if value is not None:
                found.append((index, label, value))
    if [label for _, label, _ in found if label not in optional] != [label for label in labels if label not in optional] or len({label for _, label, _ in found}) != len(found):
        report.fail("lesson_plan", "lesson_subsections", f"{context}须依次有 {[label for label in labels if label not in optional]}，可选{list(optional)}，各一次",
                    lines[0] if lines else None)
    result = {}
    for number, (index, label, value) in enumerate(found):
        stop = found[number + 1][0] if number + 1 < len(found) else len(lines)
        body = ([replace(lines[index], text=value)] if value else []) + lines[index + 1:stop]
        result[label] = (lines[index], body)
        if not any(line.text.strip() for line in body):
            report.fail("lesson_plan", "empty_lesson_subsection", f"{context}/{label}没有实质文字", lines[index])
    return result


def lesson_plan(lines, report, total):
    key = "lesson_plan"
    lines = [replace(line, text=line.text.replace("／", "/")) for line in lines]
    found = [(i, lesson_heading(line.text)) for i, line in enumerate(lines) if lesson_heading(line.text)]
    if [label for _, label in found] != list(LESSON_SECTIONS):
        report.fail(key, "lesson_sections", f"规定十二模块须各一次按序排列：{list(LESSON_SECTIONS)}",
                    lines[found[0][0]] if found else None)
    sections = {}
    for number, (index, label) in enumerate(found):
        stop = found[number + 1][0] if number + 1 < len(found) else len(lines)
        heading, body = lines[index], lines[index + 1:stop]
        sections.setdefault(label, (heading, body))
        if heading.table:
            report.fail(key, "lesson_heading_layout", f"{label}须是原生独立标题，不套整篇外表格", heading)
        if not any(line.text.strip() or line.images for line in body):
            report.fail(key, "empty_lesson_section", f"{label}没有内容", heading)

    if "课程基本信息" in sections:
        heading, body = sections["课程基本信息"]
        metadata = []
        aliases = {"学科与学段": "学科与学段/年级", "课时与时长": "课时安排", "所属单元/主题": "所属单元/主题及大概念"}
        for line in body:
            text = SECTION_PREFIX.sub("", line.text)
            for old_label, new_label in aliases.items():
                text = re.sub(r"^" + re.escape(old_label) + r"(?=\s*[:：])", new_label, text)
            metadata.append(replace(line, text=text))
        validate_fields(metadata, METADATA_FIELDS, key, report, "课程基本信息")

    if "设计依据" in sections:
        _, body = sections["设计依据"]
        body = [replace(line, text=line.text.replace("设计理论/教学模式", "设计理论与教学模式")) for line in body]
        basis = named_sections(body, ("课程标准依据", "教材分析", "学情分析", "设计理论与教学模式"), report, "设计依据", optional=("设计理论与教学模式",))
        if "课程标准依据" in basis:
            heading, content = basis["课程标准依据"]
            evidence = set()
            for line in content:
                text = line.text.replace("（水平）", "").replace("(水平)", "")
                match = field_match(text, ("内容要求", "学业要求/学业质量", "学业要求", "学业质量", "教学提示/评价建议"))
                if match and match[2].strip():
                    evidence.add(match[0])
            if len(evidence) < 2:
                report.fail(key, "curriculum_basis", "课程标准依据至少两项具体内容，不能只有通用说明或空字段", heading)

    if "教学目标" in sections:
        heading, body = sections["教学目标"]
        goals = [int(match.group(1)) for line in body
                 if (match := re.match(r"^目标\s*([0-9]+)\s*(?:【|\[|[:：])", line.text))]
        if not 2 <= len(goals) <= 4 or goals != list(range(1, len(goals) + 1)):
            report.fail(key, "lesson_objectives", "教学目标须有连续编号的2—4条可观察目标", heading)

    if "教学重点、难点与突破策略" in sections:
        _, body = sections["教学重点、难点与突破策略"]
        parts = named_sections(body, ("教学重点", "教学难点", "突破策略"), report, "教学重点与难点")
        for label in ("教学重点", "教学难点"):
            if label in parts:
                heading, content = parts[label]
                count = chinese_count("\n".join(line.text for line in content))
                report.documents[key][label + "_chinese_characters"] = count
                if count < 100:
                    report.fail(key, "insufficient_chinese_characters", f"{label}正文须至少100个中文字符，实际{count}", heading)

    if "板书设计" in sections:
        heading, body = sections["板书设计"]
        named_sections(body, ("板书主线", "副板书", "生成时机"), report, "文字板书")
        if any(line.images for line in body):
            report.fail(key, "board_text_only", "新标准板书默认文字描述结构，不以图片代替；图片须另行明确请求并按对应范围检查", heading)

    if "教学过程" not in sections:
        return
    heading, body = sections["教学过程"]
    meta = sections.get("课程基本信息", (None, []))[1]
    timing_text = "\n".join(line.text for line in meta)
    # Time may be declared in metadata or the process heading, not only one slot.
    declared = re.findall(r"总时长\s*[:：]?\s*([0-9]+(?:\.[0-9]+)?)\s*分钟", timing_text + "\n" + heading.text)
    totals = [float(value) for value in declared]
    if len(set(totals)) > 1:
        report.fail(key, "lesson_duration_consistency", "基本信息与教学过程的总时长不一致", heading)
    count_match = re.search(r"(?:建议|共)\s*([0-9]+)\s*课时", timing_text)
    if not count_match:
        count_match = re.search(r"(?<!第)([0-9]+)\s*课时", timing_text)
    session_count = int(count_match.group(1)) if count_match else 1
    each_match = re.search(r"(?:每课时|本课时)\s*[:：]?\s*([0-9]+(?:\.[0-9]+)?)\s*分钟", timing_text)
    if each_match and ("每课时" in each_match.group(0) or session_count == 1):
        inferred = session_count * float(each_match.group(1))
        if totals and abs(totals[0] - inferred) > 0.001:
            report.fail(key, "lesson_duration_consistency", "课时数乘每课时分钟数须等于总时长", heading)
        if not totals:
            totals = [inferred]
    if not totals and session_count == 1:
        single = re.search(r"课时\s*[,，;；：:]\s*([0-9]+(?:\.[0-9]+)?)\s*分钟", timing_text)
        if single:
            totals = [float(single.group(1))]
    if not totals or totals[0] <= 0:
        report.fail(key, "lesson_duration", "教案须写明正数总时长或可核算的课时数与每课时时间；建议/估算须明确标记", heading)

    blocks, sessions, session_ids = [], [], []
    active_session = None
    for line in body:
        session = re.fullmatch(r"第([0-9一二三四五六七八九十]+)课时(?:\s*[:：].+?)?\s*[（(]([0-9]+(?:\.[0-9]+)?)\s*分钟[）)]", line.text)
        block = re.fullmatch(r"(?:[（(][一二三四五六七八九十0-9]+[）)]|[0-9]+[.、．])\s*(.+?)\s*[（(]([0-9]+(?:\.[0-9]+)?)\s*分钟[）)]", line.text)
        if session:
            ordinal = session.group(1)
            numerals = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
            if ordinal.isascii():
                session_ids.append(int(ordinal))
            elif "十" in ordinal and ordinal != "十":
                tens, units = ordinal.split("十", 1)
                session_ids.append(numerals.get(tens, 1) * 10 + numerals.get(units, 0))
            else:
                session_ids.append(numerals.get(ordinal, -1))
            active_session = (line, float(session.group(2)), [])
            sessions.append(active_session)
        elif block:
            item = (line, float(block.group(2)), [])
            blocks.append(item)
            if active_session is not None:
                active_session[2].append(item)
        elif re.match(r"时间核对\s*[:：]", line.text):
            # The arithmetic line is not an extra teaching block or body content.
            continue
        elif re.match(r"(?:[（(][一二三四五六七八九十0-9]+[）)]|[0-9]+[.、．])", line.text) and ("分钟" in line.text or "待定" in line.text):
            report.fail(key, "process_block_heading", "环节标题须填具体正数分钟数", line)
        elif blocks and (active_session is None or active_session[2]):
            blocks[-1][2].append(line)
        elif line.text.strip():
            report.fail(key, "process_block_heading", "教学过程应从有具体分钟数的环节或课时标题开始", line)
    if not blocks:
        report.fail(key, "process_block_count", "教学过程须有实际学习环节及具体分钟数，不限定统一环节数量或名称", heading)
    if totals and abs(sum(minutes for _, minutes, _ in blocks) - totals[0]) > 0.001:
        report.fail(key, "process_time_total", "所有环节分钟数之和须等于教案总时长，含转换、思考与反馈时间", heading)
    if (session_count > 1 or sessions) and len(sessions) != session_count:
        report.fail(key, "lesson_sessions", "多课时教案须写全各课时安排和用时，不能只交其中一段", heading)
    if sessions:
        if session_ids != list(range(1, len(sessions) + 1)):
            report.fail(key, "lesson_sessions", "教案课时须连续编号，不能重复或缺段", heading)
        if totals and abs(sum(minutes for _, minutes, _ in sessions) - totals[0]) > 0.001:
            report.fail(key, "session_time_total", "各课时分钟数合计须等于教案总时长", heading)
        if sum(len(items) for _, _, items in sessions) != len(blocks):
            report.fail(key, "lesson_sessions", "多课时教案的所有环节须归入相应课时", heading)
        for session_heading, minutes, items in sessions:
            if minutes <= 0 or not items or abs(sum(item[1] for item in items) - minutes) > 0.001:
                report.fail(key, "session_time_total", "每课时环节时间之和须等于该课时时长且为正数", session_heading)
    for block_heading, minutes, content in blocks:
        if minutes <= 0:
            report.fail(key, "process_block_duration", "环节时间须为正数", block_heading)
        if not any(line.text.strip() for line in content):
            report.fail(key, "empty_process_block", "环节须有实质教学段落，不能只有标题和分钟数", block_heading)
    # Student actions, evidence, scaffolds, transitions and cross-file coverage
    # require semantic review; visible repeated labels/page ranges are not proof.


def validate(outline_path=None, lesson_path=None, script_path=None, expected_pages=None, *, phase="final"):
    if phase not in {"final", "plan-review"}:
        raise ValueError("phase must be final or plan-review")
    if not lesson_path or (phase == "final" and (not outline_path or not script_path)):
        raise ValueError("final requires all three documents; plan-review requires the lesson plan")
    if phase == "plan-review" and (outline_path is not None or script_path is not None or expected_pages is not None):
        raise ValueError("plan-review accepts only lesson_path, without outline, script, or expected page count")
    report = Report(phase)
    loaded = {}
    for key, path in (("outline_visual", outline_path), ("lesson_plan", lesson_path), ("speaker_script", script_path)):
        if path is None:
            continue
        document = load_docx(path, key, report)
        if document is not None:
            loaded[key] = document[0]
            banned_words(document[1], key, report)
    approved = outline_visual(loaded["outline_visual"], report, expected_pages) if "outline_visual" in loaded else None
    if "speaker_script" in loaded:
        speaker_script(loaded["speaker_script"], report, approved, expected_pages)
    if "lesson_plan" in loaded:
        lesson_plan(loaded["lesson_plan"], report, expected_pages if expected_pages is not None else (len(approved) if approved else None))
    return report.output()


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("plan-review", "final"), default="final", help="plan-review checks only the lesson plan; final checks the default three-Word package")
    parser.add_argument("--outline-visual", type=Path, help="combined PPT页纲 + 视觉蓝图 .docx; final only")
    parser.add_argument("--lesson-plan", required=True, type=Path, help="教学设计 .docx")
    parser.add_argument("--speaker-script", type=Path, help="教师逐字稿 .docx; final only")
    parser.add_argument("--expected-pages", type=positive_integer, help="frozen/approved slide count; otherwise check internal agreement only")
    args = parser.parse_args(argv)
    try:
        result = validate(args.outline_visual, args.lesson_plan, args.speaker_script, args.expected_pages, phase=args.phase)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["automatic_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

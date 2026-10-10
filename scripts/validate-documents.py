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
SCRIPT_FIELDS = ("教师逐字讲述", "课堂提问", "预设回答", "教师点拨", "过渡语")
PROCESS_FIELDS = ("教学目标", "教师组织", "学生学习", "关键问题", "评价要点", "承接推进")
LESSON_SECTIONS = ("课程信息", "教材与学情分析", "教学目标", "教学重难点", "教学过程", "板书设计", "作业设计")
SECTION_PREFIX = re.compile(r"^(?:(?:第[一二三四五六七八九十百\d]+[部分章节])|(?:[（(]?[一二三四五六七八九十百\d]+[）).、．]))\s*")
PAGE = re.compile(r"^第\s*([0-9]+)\s*页\s*[:：]?$", re.ASCII)
PAGE_LIKE = re.compile(r"^第\s*[0-9一二三四五六七八九十]+\s*页")
PAGE_RANGE = re.compile(r"^对应\s*PPT\s*第\s*([0-9]+)\s*(?:[—–\-～~至]\s*(?:第\s*)?([0-9]+)\s*)?页\s*[:：]?$", re.I)
EXTRA_OUTLINE_FIELDS = ("教师指导", "教师引导", "教学指导", "设计意图", "设计说明", "重点标注", "备注")
EXTRA_VISUAL_FIELDS = ("页面标题", "页面文字", "教师指导", "教师引导", "教学指导", "设计意图", "设计说明", "重点标注", "备注", "说明")
DURATION_NUMBER = r"(?:\d+(?:[.．]\d+)?|[零〇一二两三四五六七八九十百半]+)"
TOTAL_DURATION = re.compile(
    r"总\s*(?:时长|时间)|时长\s*(?:合计|总计)|"
    r"(?:全课|整课|本课|全程|课程|本节课)\s*"
    r"(?:共(?:计|需|用|安排)?|合计|总计|总共|历时|时长|用时)\s*[:：]?\s*"
    r"(?:约为|大约|约|预计|不超过|为)?\s*" + DURATION_NUMBER
    + r"(?:\s*[—–\-～~至]\s*" + DURATION_NUMBER + r")?\s*(?:分钟|小时)"
)
MANUAL_CHECKS = [
    {"id": "source_and_cross_file_semantics", "status": "not_assessed", "required": "逐项核对冻结教材、来源台账与三 Word 的课题、对象、目标、术语、事实、引文、活动、时间和来源覆盖；机械页序一致不代表语义一致。"},
    {"id": "teaching_and_field_quality", "status": "not_assessed", "required": "检查字段值的实质性、逐页专属性、额外字段的语义、逐字稿可讲授性，以及重点难点各自的依据、障碍与教学回应；字符数不能证明质量。"},
    {"id": "board_quality", "status": "not_assessed", "required": "实际查看板书图片，核对文字无误、至少三层、至少两条明确关系、课题专属性、至少三步生成及教学过程映射；确认缩放至 Word 可用宽高后清晰、无裁切/拉伸。图片头检查不证明能完整解码或内容正确。"},
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
            replacements = {
                "source_and_cross_file_semantics": "核对冻结教材、来源台账与待确认教学设计的理解、目标、事实、活动及来源覆盖；本阶段不检查或声称已生成 PPT 页纲和逐字稿。",
                "teaching_and_field_quality": "检查教学设计各栏的实质性、课文专属性、重点难点的依据与教学回应，以及模拟讲授可行性；字符数不能证明质量。",
                "rendered_word_pages": "渲染本阶段唯一的教学设计 Word，逐页检查表格、灰底栏目标题、重点强调、板书图片、页序、裁切和溢出；本脚本不渲染或验证 Office/WPS。",
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
    patterns = [("banned_teaching_period", re.compile(r"课\s*时"), "出现禁用的教学时段词语（课时及其变体）")]
    if key == "lesson_plan":
        patterns.extend([
            ("banned_outcome_evidence", re.compile(r"(?:成果|学习结果|学习成效|学习产出)\s*(?:的\s*)?证据"), "出现禁用的成果证据措辞"),
            ("banned_total_duration", TOTAL_DURATION, "出现禁用的总体时长说明"),
        ])
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


def page_blocks(lines, key, report, context):
    blocks = []
    for line in lines:
        match = PAGE.fullmatch(line.text)
        if match:
            blocks.append((int(match.group(1)), line, []))
        elif PAGE_LIKE.match(line.text):
            report.fail(key, "page_heading", f"{context}：页标题须单独使用 第X页（X 为阿拉伯数字）", line)
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
    start = next((i for i, line in enumerate(lines) if PAGE.fullmatch(line.text) or PAGE_LIKE.match(line.text)), len(lines))
    blocks = page_blocks(lines[start:], "speaker_script", report, "逐字稿")
    for number, _, content in blocks:
        validate_fields(content, SCRIPT_FIELDS, "speaker_script", report, f"逐字稿/第{number}页")
    sequence = [x[0] for x in blocks]
    report.page_counts["speaker_script"] = len(sequence)
    if approved is not None and sequence != approved:
        report.fail("speaker_script", "page_correspondence", f"逐字稿页序 {sequence} 与页纲页序 {approved} 不一致", blocks[0][1] if blocks else None)
    if expected is not None and len(sequence) != expected:
        report.fail("speaker_script", "expected_page_count", f"冻结页数为 {expected}，逐字稿实际有 {len(sequence)} 个页块", blocks[0][1] if blocks else None)


def chinese_count(text):
    return sum(1 for char in text if 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FA1F)


def lesson_plan(lines, report, total):
    key = "lesson_plan"
    process_start = next((i for i, line in enumerate(lines) if heading_value(line.text, "教学过程") is not None), len(lines))
    found = []
    for i, line in enumerate(lines):
        for label in LESSON_SECTIONS:
            # 教学目标 is also a required process field, not a repeated top section.
            if label == "教学目标" and i > process_start:
                continue
            value = heading_value(line.text, label)
            if value is not None:
                found.append((i, label, value))
    sequence = [label for _, label, _ in found]
    if sequence != list(LESSON_SECTIONS):
        report.fail(key, "lesson_sections", f"规定章节须各出现一次且按序排列；应为 {list(LESSON_SECTIONS)}，实际为 {sequence}", lines[found[0][0]] if found else None)
    sections = {}
    for n, (index, label, inline) in enumerate(found):
        stop = found[n + 1][0] if n + 1 < len(found) else len(lines)
        sections.setdefault(label, (lines[index], [replace(lines[index], text=inline)] if inline else []))
        sections[label][1].extend(lines[index + 1:stop])
    for label, (heading, content) in sections.items():
        for line in [heading] + content:
            if (line.text or line.images) and not line.table:
                report.fail(key, "lesson_table_layout", f"{label} 的栏目标题和内容须位于可编辑的原生 Word 表格内；其他位置存在表格不能代替本栏目表格排版", line)
        if not content:
            report.fail(key, "empty_lesson_section", f"{label} 没有内容", heading)
    if "教学重难点" in sections:
        heading, content = sections["教学重难点"]
        labels = ("教学重点", "教学难点")
        sub = [(i, label, heading_value(line.text, label))
               for i, line in enumerate(content) for label in labels
               if heading_value(line.text, label) is not None]
        if [label for _, label, _ in sub] != list(labels):
            report.fail(key, "lesson_difficulty_subsections", "教学重难点内须依次包含一次 教学重点、教学难点", heading)
        for n, (index, label, inline) in enumerate(sub):
            stop = sub[n + 1][0] if n + 1 < len(sub) else len(content)
            count = chinese_count((inline or "") + "\n" + "\n".join(x.text for x in content[index + 1:stop]))
            report.documents[key][label + "_chinese_characters"] = count
            if count < 100:
                report.fail(key, "insufficient_chinese_characters", f"{label}正文须至少 100 个中文字符；实际为 {count}（不计字段标题、标点、数字和拉丁字母）", content[index])
    if "板书设计" in sections:
        heading, content = sections["板书设计"]
        board_labels = ("板书成品示意", "板书生成顺序")
        board_headings = [(i, label, heading_value(line.text, label))
                          for i, line in enumerate(content) for label in board_labels
                          if heading_value(line.text, label) is not None]
        if [label for _, label, _ in board_headings] != list(board_labels):
            report.fail(key, "board_subsection_order", "板书设计须先为 板书成品示意，再为 板书生成顺序", heading)
        for label in board_labels:
            matches = [(i, value) for i, name, value in board_headings if name == label]
            if len(matches) != 1:
                report.fail(key, "board_subsection", f"板书设计须包含一次 {label}；实际为 {len(matches)} 次", heading)
                continue
            index, inline = matches[0]
            stop = next((i for i, _, _ in board_headings if i > index), len(content))
            if label == "板书成品示意":
                images = [rid for line in content[index:stop] for rid in line.images]
                if not images:
                    report.fail(key, "board_embedded_image", "板书成品示意中须实际嵌入 PNG/JPEG 图片，不能仅有文字、占位符或其他栏目中的图片", content[index])
                for rid in images:
                    if not report.documents[key].get("embedded_image_headers", {}).get(rid):
                        report.fail(key, "board_image_invalid", f"板书图片 {rid!r} 缺少有效的内部图片关系或 PNG/JPEG 签名与非零尺寸", content[index])
            elif not inline and not any(line.text.strip() for line in content[index + 1:stop]):
                report.fail(key, "empty_board_subsection", f"{label} 没有内容", content[index])
    if "教学过程" not in sections:
        return
    heading, content = sections["教学过程"]
    rows = []
    for line in content:
        if not line.row:
            report.fail(key, "process_table_layout", "教学过程必须为 教学环节 | 具体教学安排 两列表格", line)
            continue
        if not rows or rows[-1][0].row != line.row:
            rows.append([])
        rows[-1].append(line)
    if not rows:
        report.fail(key, "missing_process_blocks", "教学过程缺少两列表格和详细过程块", heading)
        return
    header = rows[0]
    if [line.text for line in header] != ["教学环节", "具体教学安排"] or [line.cell for line in header] != [1, 2] or any(line.row_cells != 2 for line in header):
        report.fail(key, "process_table_header", "教学过程表格的首行必须恰为 教学环节 | 具体教学安排 两列", header[0])
    if len(rows) < 2:
        report.fail(key, "missing_process_blocks", "教学过程表格没有具体教学安排", heading)
    covered = set()
    for n, row in enumerate(rows[1:], 1):
        if any(line.row_cells != 2 or line.table != header[0].table for line in row):
            report.fail(key, "process_table_layout", "每个教学过程块须在同一原生表格的独立两列行内，不得将多个块打散或合并", row[0])
        titles = [line for line in row if line.cell == 1 and line.text]
        body = [line for line in row if line.cell == 2]
        if len(titles) != 1 or field_match(titles[0].text, PROCESS_FIELDS) or PAGE_RANGE.fullmatch(titles[0].text):
            report.fail(key, "process_block_title", "教学环节列须有一个独立的内容性板块标题", row[0])
        ranges = [(i, PAGE_RANGE.fullmatch(line.text)) for i, line in enumerate(body) if PAGE_RANGE.fullmatch(line.text)]
        if report.phase == "plan-review":
            if ranges:
                report.fail(key, "premature_process_page_range", "教学设计待确认阶段尚未编排最终 PPT，过程块不得填写对应 PPT 页码", body[ranges[0][0]])
        elif len(ranges) != 1 or ranges[0][0] != 0:
            report.fail(key, "process_page_mapping", "最终教学过程每行的具体教学安排须先有一个 对应PPT第X—X页，再有六个过程字段", row[0])
        for index, match in ranges:
            start, end = int(match.group(1)), int(match.group(2) or match.group(1))
            if start < 1 or end < start or (total is not None and end > total):
                report.fail(key, "process_page_range", f"教学过程页范围 {start}—{end} 不在批准的 1—{total} 页内或范围倒置", body[index])
            else:
                covered.update(range(start, end + 1))
        body = [line for line in body if not PAGE_RANGE.fullmatch(line.text)]
        validate_fields(body, PROCESS_FIELDS, key, report, f"教学过程/第{n}个板块")
    if report.phase == "final" and total is not None and covered != set(range(1, total + 1)):
        report.fail(key, "process_page_coverage", f"教学过程尚未覆盖全部 PPT 页；缺少 {sorted(set(range(1, total + 1)) - covered)}", heading)


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

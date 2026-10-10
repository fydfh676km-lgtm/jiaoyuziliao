"""Behavioral tests using temporary, minimal but genuine OOXML DOCX packages."""

import importlib.util
import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.sax.saxutils import escape
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "validate-documents.py"
SPEC = importlib.util.spec_from_file_location("edu_ppt_validate_documents", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"


def p(*runs, properties=""):
    return "<w:p>" + ("<w:pPr>" + properties + "</w:pPr>" if properties else "") + "".join("<w:r><w:t xml:space='preserve'>" + escape(run) + "</w:t></w:r>" for run in runs) + "</w:p>"


def table(rows):
    return "<w:tbl><w:tblPr/><w:tblGrid/>" + "".join("<w:tr>" + "".join("<w:tc><w:tcPr/>" + (cell if cell.startswith("<w:") else p(cell)) + "</w:tc>" for cell in row) + "</w:tr>" for row in rows) + "</w:tbl>"


BOARD_PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aS8sAAAAASUVORK5CYII=")


def board_picture(rid="rIdBoard"):
    return '<w:p><w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="5486400" cy="3086100"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:blipFill><a:blip r:embed="' + rid + '"/></pic:blipFill></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'


def outline():
    # First page uses paragraphs; second uses table cells and split text runs.
    return "".join([
        p("材料示例"), p("PPT页纲"), p("第1页"),
        p("页面标题：材料阅读"), p("页面文字：请圈画证据。"),
        table([["第2页"], [p("页面", "标题："), "比较表达"], ["页面文字：", "说明两则材料的共同点。"]]),
        p("视觉蓝图"), p("第1页"),
        p("画面风格：清晰、沉静"), p("添加元素：两则材料的来源标签"),
        p("文字字体与重点标注：正文大字；突出证据"),
        p("布局排版：上方问题，下方材料"), p("镜头与光影：平视、均匀照明"),
        p("画面去重与统一约束：统一深色标题、浅色正文区"),
        p("第2页"),
        table([[p("画面", "风格："), "延续沉静风格，采用对照结构"],
               ["添加元素：", "并排材料框"],
               ["文字字体与重点标注：", "突出共同特征"],
               ["布局排版：", "对照后汇合为一句解释"],
               ["镜头与光影：", "俯视纸面、柔光"],
               ["画面去重与统一约束：", "沿用标题层级，改变内容结构"]]),
    ])


def script():
    return "".join([
        p("教师逐字稿"), p("第1页"), p("教师逐字讲述：请先读材料，再说出你的判断。"),
        p("课堂提问：你从哪里得出这个判断？"), p("预设回答：指出材料中的语句。"),
        p("教师点拨：将判断与证据连起来。"), p("过渡语：接下来比较第二则材料。"),
        p("第2页"),
        table([["教师逐字讲述：", "先比较，再解释共同点。"], ["课堂提问：", "哪些证据支持共同点？"],
               ["预设回答：", "列举相同特征与对应证据。"], ["教师点拨：", "共同点不是复述。"],
               ["过渡语：", "带着这一方法完成练习。"]]),
    ])


KEY_POINT = (
    "根据教材材料的阅读要求和学习任务，学生需要从具体语句中提取可支持判断的信息，并将证据与自己的解释对应。"
    "学习中可能把抄录原文误当成完成解释，因此教师先用同一材料中的不同答案组织比较，让学生指出证据与判断之间缺少的联系。"
    "随后通过圈画、同伴说明和修改表述，逐步形成先找依据再作解释的阅读习惯，课堂评价关注证据是否准确以及说明是否建立了联系。"
)
DIFFICULTY = (
    "根据学习任务中的比较要求，学生需要在两则不同材料之间辨认共同特征，同时保留各自语境的差异。"
    "主要障碍是学生容易只按表面相似的词语进行归类，忽略这些词语在材料中承担的具体作用。"
    "教学中先分别梳理每则材料，再让学生在对照表中标明相同与不同，并用完整语句说明归类的理由。"
    "教师利用同伴质疑与反例追问促使学生修正过度概括，最终检查结论能否同时得到两则材料的支持。"
)


def process_table(review=False):
    first = "".join([
        "" if review else p("对应PPT第1页"),
        p("教学目标：建立判断与依据的联系。"), p("教师组织：呈现两种答案，追问各自依据。"),
        p("学生学习：圈画、讨论并修改解释。"), p("关键问题：哪一句支持你的解释？"),
        p("评价要点：证据准确且与判断有关。"), p("承接推进：比较另一则材料。"),
    ])
    second = "".join([
        "" if review else p("对应PPT第2—2页"),
        p("教学目标：解释两则材料的共同特征。"), p("教师组织：出示对照表并组织质疑。"),
        p("学生学习：比较材料并修正结论。"), p("关键问题：共同点能得到两则材料支持吗？"),
        p("评价要点：归类准确，理由完整。"), p("承接推进：将方法用于新的材料。"),
    ])
    return table([["教学环节", "具体教学安排"], ["从材料寻找依据（5分钟）", first], ["跨材料比较（8分钟）", second]])


def lesson(review=False):
    # Editable native cells with section titles, nested process table, real image.
    return p("材料阅读教学设计") + table([
        ["课程信息"], [p("课题：材料阅读") + p("对象：学习者")],
        ["教材与学情分析"], [p("包含两则可比较材料；学习者需要从复述发展到解释。")],
        ["教学目标"], [p("能用材料证据解释判断。")],
        ["教学重难点"], [p("教学重点") + p(KEY_POINT) + p("教学难点") + p(DIFFICULTY)],
        ["教学过程"], [process_table(review) + p("")],
        ["板书设计"], [p("板书成品示意") + board_picture() + p("板书生成顺序") + p("阅读时写证据，讨论时连判断，比较时补共同点。")],
        ["作业设计"], [p("比较一组新材料。")],
    ])


def write_docx(path, body, *, header=None, footer=None, styles=None, invalid_xml=False,
               board_data=BOARD_PNG, board_relationship=True, external_board=False):
    overrides = [('/word/document.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml')]
    parts = {"word/document.xml": f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{body}<w:sectPr></w:sectPr></w:body></w:document>'}
    relationships = []
    if "rIdBoard" in body and board_relationship:
        target = "https://example.invalid/board.png" if external_board else "media/board.png"
        mode = ' TargetMode="External"' if external_board else ""
        relationships.append(f'<Relationship Id="rIdBoard" Type="{R}/image" Target="{target}"{mode}/>')
        if not external_board:
            parts["word/media/board.png"] = board_data
            overrides.append(("/word/media/board.png", "image/png"))
    for name, content in (("header1", header), ("footer1", footer), ("styles", styles)):
        if content is None:
            continue
        role = name.rstrip("1")
        root = {"header": "hdr", "footer": "ftr", "styles": "styles"}[role]
        parts[f"word/{name}.xml"] = f'<w:{root} xmlns:w="{W}">{content}</w:{root}>'
        overrides.append((f"/word/{name}.xml", f"application/vnd.openxmlformats-officedocument.wordprocessingml.{role}+xml"))
        relationships.append(f'<Relationship Id="rId{len(relationships)+1}" Type="{R}/{role}" Target="{name}.xml"/>')
        if role in ("header", "footer"):
            parts["word/document.xml"] = parts["word/document.xml"].replace("</w:sectPr>", f'<w:{role}Reference w:type="default" r:id="rId{len(relationships)}"/></w:sectPr>')
    if relationships:
        parts["word/_rels/document.xml.rels"] = f'<Relationships xmlns="{REL}">' + "".join(relationships) + "</Relationships>"
    parts["[Content_Types].xml"] = f'<Types xmlns="{CT}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>' + "".join(f'<Override PartName="{name}" ContentType="{typ}"/>' for name, typ in overrides) + "</Types>"
    parts["_rels/.rels"] = f'<Relationships xmlns="{REL}"><Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/></Relationships>'
    if invalid_xml:
        parts["word/document.xml"] = "<w:document"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        for name, content in parts.items():
            package.writestr(name, content)


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.paths = [Path(self.tmp.name) / name for name in ("outline.docx", "lesson.docx", "script.docx")]
        self.bodies = [outline(), lesson(), script()]
        self.options = [{}, {}, {}]

    def check(self, expected=2):
        for path, body, options in zip(self.paths, self.bodies, self.options):
            write_docx(path, body, **options)
        return CHECKER.validate(*self.paths, expected)

    def assert_failure(self, result, code, document=None, location=None):
        self.assertFalse(result["automatic_checks_pass"], result)
        matches = [x for x in result["errors"] if x["code"] == code and (document is None or x["document"] == document)]
        self.assertTrue(matches, result["errors"])
        if location:
            self.assertTrue(any(location in x["location"] for x in matches), matches)

    def test_valid_mixed_paragraph_table_and_split_runs(self):
        result = self.check()
        self.assertTrue(result["automatic_checks_pass"], result["errors"])
        self.assertEqual(result["page_counts"], {"outline": 2, "visual_blueprint": 2, "speaker_script": 2})
        self.assertTrue(all(x["status"] == "not_assessed" for x in result["manual_checks_required"]))
        self.assertNotIn("verified", result)

    def test_sections_can_have_ordinary_heading_numbers(self):
        self.bodies[1] = self.bodies[1].replace(p("教学重点"), p("六、教学重点："))
        self.bodies[1] = self.bodies[1].replace(p("教学难点"), p("7. 教学难点"))
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_inline_section_content_counts(self):
        self.bodies[1] = self.bodies[1].replace(p("教学重点") + p(KEY_POINT), p("教学重点：" + KEY_POINT))
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_forbidden_term_in_body_table_across_runs(self):
        self.bodies[0] += table([[p("第一课", "时总结")]])
        self.assert_failure(self.check(), "banned_teaching_period", "outline_visual", "/tbl[")

    def test_forbidden_term_across_header_runs(self):
        self.options[2]["header"] = p("课", "时一")
        self.assert_failure(self.check(), "banned_teaching_period", "speaker_script", "word/header1.xml")

    def test_forbidden_term_in_footer(self):
        self.options[1]["footer"] = p("第二课时")
        self.assert_failure(self.check(), "banned_teaching_period", "lesson_plan", "word/footer1.xml")

    def test_textbox_is_scanned_without_repeating_anchoring_paragraph(self):
        textbox = '<w:p><w:r><w:pict><v:shape xmlns:v="urn:schemas-microsoft-com:vml" id="TextBox1" style="width:180pt;height:40pt"><v:textbox><w:txbxContent>' + p("课", "时导入") + "</w:txbxContent></v:textbox></v:shape></w:pict></w:r></w:p>"
        self.bodies[0] += textbox
        result = self.check()
        self.assert_failure(result, "banned_teaching_period", "outline_visual", "txbxContent")
        self.assertEqual(len([x for x in result["errors"] if x["code"] == "banned_teaching_period"]), 1)

    def test_duplicate_page(self):
        self.bodies[0] = self.bodies[0].replace(p("第2页"), p("第1页"))
        self.assert_failure(self.check(), "page_sequence", "outline_visual")

    def test_missing_page_and_cross_file_disagreement(self):
        self.bodies[2] = self.bodies[2].split(p("第2页"))[0]
        result = self.check()
        self.assert_failure(result, "page_correspondence", "speaker_script")
        self.assert_failure(result, "expected_page_count", "speaker_script")

    def test_page_gap_even_when_documents_have_same_count(self):
        self.bodies = [body.replace("第2页", "第3页") for body in self.bodies]
        self.assert_failure(self.check(), "page_sequence")

    def test_expected_page_count_is_independent_of_internal_agreement(self):
        self.assert_failure(self.check(expected=3), "expected_page_count", "outline_visual")

    def test_no_expected_count_still_checks_internal_agreement(self):
        self.assertTrue(self.check(expected=None)["automatic_checks_pass"])
        self.bodies[2] = self.bodies[2].split(p("第2页"))[0]
        self.assert_failure(self.check(expected=None), "page_correspondence")

    def test_visual_section_order_and_duplicates(self):
        for replacement in (p("视觉蓝图") + p("PPT页纲"), p("PPT页纲") + p("PPT页纲")):
            with self.subTest(replacement=replacement):
                self.bodies[0] = outline().replace(p("PPT页纲"), replacement)
                self.assert_failure(self.check(), "combined_sections")

    def test_empty_split_table_field(self):
        self.bodies[0] = self.bodies[0].replace(p("延续沉静风格，采用对照结构"), p("  "))
        self.assert_failure(self.check(), "empty_field", "outline_visual", "/tc[")

    def test_missing_repeated_and_reordered_fixed_fields(self):
        changes = [
            (p("镜头与光影：平视、均匀照明"), ""),
            (p("镜头与光影：平视、均匀照明"), p("镜头与光影：平视、均匀照明") * 2),
            (p("画面风格：清晰、沉静") + p("添加元素：两则材料的来源标签"), p("添加元素：两则材料的来源标签") + p("画面风格：清晰、沉静")),
        ]
        for old, new in changes:
            with self.subTest(new=new):
                self.bodies[0] = outline().replace(old, new)
                self.assert_failure(self.check(), "field_sequence", "outline_visual")

    def test_visual_numeric_letter_bullet_and_circled_prefixes(self):
        for prefix in ("1. ", "一、", "（二）", "① ", "A. ", "• ", "- "):
            with self.subTest(prefix=prefix):
                self.bodies[0] = outline().replace("画面风格：清晰", prefix + "画面风格：清晰")
                self.assert_failure(self.check(), "field_list_prefix", "outline_visual")

    def test_visual_direct_word_numbering(self):
        self.bodies[0] = self.bodies[0].replace(p("画面风格：清晰、沉静"), p("画面风格：清晰、沉静", properties='<w:numPr><w:ilvl w:val="0"/><w:numId w:val="4"/></w:numPr>'))
        self.assert_failure(self.check(), "field_list_prefix", "outline_visual")

    def test_visual_inherited_word_numbering(self):
        self.options[0]["styles"] = '<w:style w:type="paragraph" w:styleId="Numbered"><w:pPr><w:numPr><w:numId w:val="7"/></w:numPr></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Derived"><w:basedOn w:val="Numbered"/></w:style>'
        self.bodies[0] = self.bodies[0].replace(p("画面风格：清晰、沉静"), p("画面风格：清晰、沉静", properties='<w:pStyle w:val="Derived"/>'))
        self.assert_failure(self.check(), "field_list_prefix", "outline_visual")

    def test_direct_zero_numbering_cancels_inherited_numbering(self):
        self.options[0]["styles"] = '<w:style w:type="paragraph" w:styleId="Numbered"><w:pPr><w:numPr><w:numId w:val="7"/></w:numPr></w:pPr></w:style>'
        self.bodies[0] = self.bodies[0].replace(p("画面风格：清晰、沉静"), p("画面风格：清晰、沉静", properties='<w:pStyle w:val="Numbered"/><w:numPr><w:numId w:val="0"/></w:numPr>'))
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_seventh_visual_field(self):
        self.bodies[0] += p("备注：制作时进一步修改。")
        self.assert_failure(self.check(), "extra_field", "outline_visual")

    def test_outline_rejects_explicit_extra_structural_fields(self):
        for label in ("教师引导", "教师指导", "设计意图", "备注"):
            with self.subTest(label=label):
                self.bodies[0] = outline().replace(p("视觉蓝图"), p(label + "：要求学生比较材料。") + p("视觉蓝图"))
                self.assert_failure(self.check(), "extra_field", "outline_visual")

    def test_outline_keeps_legitimate_colons_in_page_copy(self):
        self.bodies[0] = outline().replace(
            p("页面文字：请圈画证据。"),
            p("页面文字：请圈画证据。") + p("材料：两则材料中的共同点。")
            + p("问题：怎样用证据支持判断？") + p("活动：讨论并修改表述。"),
        )
        result = self.check()
        self.assertTrue(result["automatic_checks_pass"], result["errors"])

    def test_script_requires_five_ordered_nonempty_fields(self):
        self.bodies[2] = self.bodies[2].replace(p("教师点拨：将判断与证据连起来。"), p("教师点拨："))
        self.assert_failure(self.check(), "empty_field", "speaker_script")
        self.bodies[2] = script().replace(p("课堂提问：你从哪里得出这个判断？"), "")
        self.assert_failure(self.check(), "field_sequence", "speaker_script")

    def test_lesson_sections_missing_and_out_of_order(self):
        self.bodies[1] = self.bodies[1].replace(p("教材与学情分析"), p("课程信息")).replace(p("教学重难点"), "")
        self.assert_failure(self.check(), "lesson_sections", "lesson_plan")

    def test_chinese_minimum_does_not_count_latin_punctuation_or_section_label(self):
        self.bodies[1] = self.bodies[1].replace(p(KEY_POINT), p("汉" * 99 + " A lesson, 1234!" * 100))
        self.assert_failure(self.check(), "insufficient_chinese_characters", "lesson_plan")
        self.bodies[1] = self.bodies[1].replace(p("汉" * 99 + " A lesson, 1234!" * 100), p("汉" * 100))
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_both_key_point_and_difficulty_are_independently_counted(self):
        self.bodies[1] = self.bodies[1].replace(p(DIFFICULTY), p("只是简短描述。"))
        result = self.check()
        self.assert_failure(result, "insufficient_chinese_characters", "lesson_plan")
        self.assertTrue(any("教学难点" in e["message"] for e in result["errors"]))

    def test_outcome_evidence_and_total_duration_forbidden_in_auxiliary_parts(self):
        self.options[1]["header"] = p("学习成果", "证据")
        self.options[1]["footer"] = p("全课共", "40分钟")
        result = self.check()
        self.assert_failure(result, "banned_outcome_evidence", "lesson_plan", "word/header1.xml")
        self.assert_failure(result, "banned_total_duration", "lesson_plan", "word/footer1.xml")

    def test_total_duration_does_not_match_ordinary_joint_learning_sentences(self):
        for text in ("本课共同探究两则材料。", "本课共同探究，先阅读5分钟。", "本课共安排三个活动，每个活动5分钟。"):
            with self.subTest(text=text):
                self.bodies[1] = lesson().replace(p("比较一组新材料。"), p("比较一组新材料。") + p(text))
                result = self.check()
                self.assertTrue(result["automatic_checks_pass"], result["errors"])

    def test_total_duration_requires_quantity_and_unit_or_explicit_total_label(self):
        for text in ("总时长：", "课程总时长：四十分钟", "全课共40分钟", "本课共约四十分钟", "本课用时：1.5小时", "全程历时45—50分钟", "课程时长为四十五分钟"):
            with self.subTest(text=text):
                self.bodies[1] = lesson() + p(text)
                self.assert_failure(self.check(), "banned_total_duration", "lesson_plan")

    def test_board_subitems_are_required_and_nonempty(self):
        self.bodies[1] = self.bodies[1].replace(p("板书生成顺序"), p("操作提示"))
        self.assert_failure(self.check(), "board_subsection", "lesson_plan")
        self.bodies[1] = lesson().replace(p("阅读时写证据，讨论时连判断，比较时补共同点。"), "")
        self.assert_failure(self.check(), "empty_board_subsection", "lesson_plan")

    def test_process_fields_and_page_ranges(self):
        self.bodies[1] = self.bodies[1].replace(p("评价要点：证据准确且与判断有关。"), "")
        self.assert_failure(self.check(), "field_sequence", "lesson_plan")
        self.bodies[1] = lesson().replace(p("对应PPT第2—2页"), p("对应PPT第3—3页"))
        self.assert_failure(self.check(), "process_page_range", "lesson_plan")

    def test_exactly_seven_lesson_sections(self):
        self.assertEqual(CHECKER.LESSON_SECTIONS, ("课程信息", "教材与学情分析", "教学目标", "教学重难点", "教学过程", "板书设计", "作业设计"))
        self.bodies[1] = self.bodies[1].replace(p("作业设计"), p("作业设计") + p("课程信息"))
        self.assert_failure(self.check(), "lesson_sections", "lesson_plan")

    def test_lesson_not_accepted_as_prose_plus_unrelated_table(self):
        # Removing the table around all sections must not be hidden by process table.
        body = lesson()
        for tag in ('<w:tbl>', '</w:tbl>', '<w:tblPr/>', '<w:tblGrid/>', '<w:tr>', '</w:tr>', '<w:tc>', '</w:tc>', '<w:tcPr/>'):
            body = body.replace(tag, '')
        self.bodies[1] = body + table([["无关表格", "不能证明教案已表格排版"]])
        self.assert_failure(self.check(), "lesson_table_layout", "lesson_plan")

    def test_one_section_outside_native_table_is_not_accepted(self):
        original = '<w:tr><w:tc><w:tcPr/>' + p("作业设计") + '</w:tc></w:tr><w:tr><w:tc><w:tcPr/>' + p("比较一组新材料。") + '</w:tc></w:tr>'
        self.bodies[1] = self.bodies[1].replace(original, '') + p("作业设计") + p("比较一组新材料。")
        self.assert_failure(self.check(), "lesson_table_layout", "lesson_plan")

    def test_keypoint_and_difficulty_must_be_separate_subsections(self):
        self.bodies[1] = self.bodies[1].replace(p("教学难点"), p("合并说明"))
        self.assert_failure(self.check(), "lesson_difficulty_subsections", "lesson_plan")

    def test_process_requires_exact_two_column_header(self):
        self.bodies[1] = self.bodies[1].replace(p("教学环节"), p("教师活动"))
        self.assert_failure(self.check(), "process_table_header", "lesson_plan")

    def test_process_fields_cannot_be_recovered_across_different_rows(self):
        split = p("关键问题：哪一句支持你的解释？")
        self.bodies[1] = self.bodies[1].replace(split, '</w:tc></w:tr><w:tr><w:tc><w:tcPr/>' + p("拆开的其他环节") + '</w:tc><w:tc><w:tcPr/>' + split)
        self.assert_failure(self.check(), "field_sequence", "lesson_plan")

    def test_process_fields_cannot_be_in_title_column(self):
        field = p("教师组织：呈现两种答案，追问各自依据。")
        self.bodies[1] = self.bodies[1].replace(field, '').replace(p("从材料寻找依据（5分钟）"), p("从材料寻找依据（5分钟）") + field)
        result = self.check()
        self.assert_failure(result, "process_block_title", "lesson_plan")
        self.assert_failure(result, "field_sequence", "lesson_plan")

    def test_process_third_empty_cell_does_not_pass_two_column_check(self):
        ending = p("承接推进：比较另一则材料。") + '</w:tc></w:tr>'
        self.bodies[1] = self.bodies[1].replace(ending, p("承接推进：比较另一则材料。") + '</w:tc><w:tc><w:tcPr/>' + p("") + '</w:tc></w:tr>')
        self.assert_failure(self.check(), "process_table_layout", "lesson_plan")

    def test_final_requires_real_page_mapping_in_each_process_row(self):
        self.bodies[1] = lesson(review=True)
        self.assert_failure(self.check(), "process_page_mapping", "lesson_plan")

    def test_board_requires_picture_inside_correct_subsection(self):
        for replacement in ("", p("此处放板书图片")):
            with self.subTest(replacement=replacement):
                self.bodies[1] = lesson().replace(board_picture(), replacement)
                self.assert_failure(self.check(), "board_embedded_image", "lesson_plan")
        self.bodies[1] = lesson().replace(board_picture(), '').replace(p("比较一组新材料。"), board_picture() + p("比较一组新材料。"))
        self.assert_failure(self.check(), "board_embedded_image", "lesson_plan")

    def test_board_image_after_generation_order_is_not_example(self):
        self.bodies[1] = lesson().replace(board_picture(), '').replace(p("板书生成顺序"), p("板书生成顺序") + board_picture())
        self.assert_failure(self.check(), "board_embedded_image", "lesson_plan")

    def test_board_image_broken_reference(self):
        self.options[1]["board_relationship"] = False
        self.assert_failure(self.check(), "board_image_invalid", "lesson_plan")

    def test_board_external_image_link_is_not_embedded(self):
        self.options[1]["external_board"] = True
        self.assert_failure(self.check(), "board_image_invalid", "lesson_plan")

    def test_board_image_signature_and_nonzero_dimensions(self):
        for data in (b"not an image", BOARD_PNG[:24], BOARD_PNG[:16] + b'\0' * 8 + BOARD_PNG[24:]):
            with self.subTest(data=data):
                self.options[1]["board_data"] = data
                self.assert_failure(self.check(), "board_image_invalid", "lesson_plan")

    def test_board_image_relationship_must_be_image_type(self):
        self.check()
        with zipfile.ZipFile(self.paths[1]) as source:
            parts = {name: source.read(name) for name in source.namelist()}
        parts["word/_rels/document.xml.rels"] = parts["word/_rels/document.xml.rels"].replace((R + '/image').encode(), (R + '/hyperlink').encode())
        with zipfile.ZipFile(self.paths[1], "w") as package:
            for name, content in parts.items():
                package.writestr(name, content)
        self.assert_failure(CHECKER.validate(*self.paths, 2), "board_image_invalid", "lesson_plan")

    def test_jpeg_image_header_recognized_and_truncated_rejected(self):
        # Tiny SOF segment is only a header fixture; this script never claims decoding.
        header = b'\xff\xd8\xff\xc0\x00\x0b\x08\x01\x00\x02\x00\x01\x01\x11\x00\xff\xd9'
        self.assertEqual(CHECKER.image_header(header), {"format": "JPEG", "width": 512, "height": 256})
        self.assertIsNone(CHECKER.image_header(header[:10]))

    def test_plan_review_only_checks_lesson_without_page_numbers(self):
        write_docx(self.paths[1], lesson(review=True))
        result = CHECKER.validate(lesson_path=self.paths[1], phase="plan-review")
        self.assertTrue(result["automatic_checks_pass"], result["errors"])
        self.assertEqual(result["phase"], "plan-review")
        self.assertEqual(set(result["documents"]), {"lesson_plan"})
        self.assertEqual(result["page_counts"], {})
        self.assertIn("lesson-plan review only", result["scope"])
        self.assertNotIn("verified", result)
        self.assertTrue(all(x["status"] == "not_assessed" for x in result["manual_checks_required"]))

    def test_plan_review_rejects_premature_page_mapping(self):
        write_docx(self.paths[1], lesson())
        result = CHECKER.validate(lesson_path=self.paths[1], phase="plan-review")
        self.assert_failure(result, "premature_process_page_range", "lesson_plan")

    def test_invalid_phase_or_incomplete_scope_rejected_at_api_boundary(self):
        for arguments in ({"lesson_path": self.paths[1]}, {"phase": "other", "lesson_path": self.paths[1]},
                          {"phase": "plan-review", "lesson_path": self.paths[1], "outline_path": self.paths[0]},
                          {"phase": "plan-review", "lesson_path": self.paths[1], "script_path": self.paths[2]},
                          {"phase": "plan-review", "lesson_path": self.paths[1], "expected_pages": 2}):
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    CHECKER.validate(**arguments)

    def test_plan_review_cli_phase_and_invalid_extra_arguments(self):
        write_docx(self.paths[1], lesson(review=True))
        command = [sys.executable, str(SCRIPT), "--phase", "plan-review", "--lesson-plan", str(self.paths[1])]
        process = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        self.assertEqual(json.loads(process.stdout)["phase"], "plan-review")
        for extra in (["--expected-pages", "2"], ["--outline-visual", str(self.paths[0])], ["--speaker-script", str(self.paths[2])]):
            process = subprocess.run(command + extra, capture_output=True, text=True)
            self.assertEqual(process.returncode, 2, process.stdout)

    def test_docx_package_malformed_xml(self):
        self.options[1]["invalid_xml"] = True
        self.assert_failure(self.check(), "docx_package", "lesson_plan")

    def test_zip_without_docx_package_parts(self):
        self.check()
        with zipfile.ZipFile(self.paths[0], "w") as package:
            package.writestr("word/document.xml", "<document/>")
        self.assert_failure(CHECKER.validate(*self.paths), "docx_package", "outline_visual")

    def test_broken_relationship_target(self):
        self.check()
        with zipfile.ZipFile(self.paths[0]) as source:
            parts = {name: source.read(name) for name in source.namelist()}
        parts["_rels/.rels"] = parts["_rels/.rels"].replace(b'word/document.xml', b'word/missing.xml')
        with zipfile.ZipFile(self.paths[0], "w") as package:
            for name, content in parts.items():
                package.writestr(name, content)
        self.assert_failure(CHECKER.validate(*self.paths), "docx_package", "outline_visual")

    def test_cli_json_and_exit_codes(self):
        self.check()
        command = [sys.executable, str(SCRIPT), "--outline-visual", str(self.paths[0]), "--lesson-plan", str(self.paths[1]), "--speaker-script", str(self.paths[2]), "--expected-pages", "2"]
        process = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        self.assertTrue(json.loads(process.stdout)["automatic_checks_pass"])
        self.paths[1].unlink()
        process = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(process.returncode, 1)
        self.assert_failure(json.loads(process.stdout), "docx_package", "lesson_plan")
        process = subprocess.run(command[:-1] + ["0"], capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)


if __name__ == "__main__":
    unittest.main()

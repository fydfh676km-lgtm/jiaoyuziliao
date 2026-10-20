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
        p("教师逐字稿"), p("黑色为教师口播；红色为操作提示，不朗读。"),
        p("P1 材料阅读"), p("师：请先读材料，再说出你的判断。"),
        p("师：你从哪里得出这个判断？"), p("【留白5秒，听学生结合原文回答。】"),
        p("师：我们要把判断与证据连起来。接下来比较第二则材料。"),
        p("P2 比较表达"), p("师：先比较，再解释共同点。哪些证据支持共同点？"),
        p("【若学生只复述，追问两则材料的共同特征。】"),
        p("师：共同点不是复述。带着这一方法完成练习。"),
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


def process_blocks(review=False):
    blocks = []
    for name, minutes, page in (("导入：比较两种答案", 4, "1"), ("主体：依据核验", 30, "1—2"),
                                ("评价总结：回看解释", 4, "2—2"), ("课堂延伸：迁移方法", 2, "2—2")):
        blocks.extend([p(f"（{len(blocks)//2+1}）{name}（{minutes}分钟）"),
                       p("教师呈现两种答案，追问哪一句支持解释。学生圈画、讨论并修改判断，继而比较两则材料。教师观察所引语句是否支持判断；若只抄原文，则追问语句与判断的联系。")])
    return "".join(blocks)


def metadata():
    return "".join(p(text) for text in (
        "课题：材料阅读", "学科与学段：初中语文七年级", "教材依据：用户提供版本及阅读单元。",
        "课时安排：建议1课时，40分钟，总时长40分钟（非已确认）。", "所属单元/主题及大概念：阅读与解释。",
        "课型：新授", "授课对象：七年级，班级与人数未提供。", "设计者/日期：未提供。"))


def lesson(review=False):
    return p("材料阅读教学设计") + "".join([
        p("一、课程基本信息"), metadata(),
        p("二、设计依据"), p("（一）课程标准依据"),
        p("内容要求：课程内容中关于阅读材料、形成解释的要求。"),
        p("学业要求：能引用材料依据解释自己的判断。"),
        p("（二）教材分析"), p("包含两则可比较材料，训练依据与判断的联系。"),
        p("（三）学情分析"), p("经验判断：学生易将复述当解释，以对照表支架回应。"),
        p("（四）设计理论与教学模式"), p("任务驱动，以真实比较任务连接依据和解释。"),
        p("三、设计理念"), p("以依据和解释的联系贯穿材料比较和迁移。"),
        p("四、教学目标"),
        p("目标1【素养落点：思维能力】学生通过材料圈画，能引用一句语句说明判断，依据与判断相符。"),
        p("目标2【素养落点：思维能力】学生通过双栏比较，能解释两则材料的共同点，同时获得两则支持。"),
        p("五、教学重点、难点与突破策略"), p("教学重点"), p(KEY_POINT), p("教学难点"), p(DIFFICULTY),
        p("突破策略：难点一通过双栏比较与反例追问，在主体活动中核验。"),
        p("六、教学准备"), p("教材原文和两种答案的对照材料。"),
        p("七、教-学-评一体化设计（三线对齐）"),
        p("目标1—评价任务1：圈画依据；对应导入及主体，用语句与判断的关联判定。"),
        p("目标2—评价任务2：完成双栏比较；对应主体与总结，用两则材料同时支持判定。"),
        p("八、教学过程（总时长40分钟）"), process_blocks(review),
        p("九、板书设计（文字描述结构，不画图）"),
        p("板书主线：材料一、材料二并列，下连依据与解释，再汇聚共同特征。"),
        p("副板书：暂存两种待检验答案。"), p("生成时机：阅读时写证据，讨论时连判断，比较时补共同点。"),
        p("十、作业设计（分层）"), p("基础作业：比较一组新材料。拓展作业：口头解释一次修改；教师反馈。"),
        p("十一、教学评价（本课评价方案）"), p("评价方式：观察、自评、教师反馈。"),
        table([["维度", "待达标", "达标", "优秀"], ["依据关联", "有提示仍不对应", "独立对应", "可用反例检验"],
               ["比较准确", "只比词语", "比较材料关系", "能解释语境差别"], ["解释完整", "只有结论", "有结论和依据", "能回应不同判断"]]),
        p("评价结果的使用：即时反馈并用反例补救。"),
        p("十二、教学反思预设与课后改进"),
        p("预判问题1：可能只复述，追问判断依据。预判问题2：可能过度概括，增加反例核验。"),
        p("目标达成的证据形式：比较表与修改说明；未达标时增加成对示例支架。"),
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
        self.options[0]["footer"] = p("第二课时")
        self.assert_failure(self.check(), "banned_teaching_period", "outline_visual", "word/footer1.xml")

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
        self.bodies[2] = self.bodies[2].split(p("P2 比较表达"))[0]
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
        self.bodies[2] = self.bodies[2].split(p("P2 比较表达"))[0]
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

    def test_script_rejects_legacy_printed_fields(self):
        self.bodies[2] = script().replace(p("师：你从哪里得出这个判断？"), p("课堂提问：你从哪里得出这个判断？"))
        self.assert_failure(self.check(), "script_paragraph_type", "speaker_script")

    def test_script_requires_a_page_title_after_p_number(self):
        self.bodies[2] = script().replace(p("P1 材料阅读"), p("P1"))
        self.assert_failure(self.check(), "page_heading", "speaker_script")

    def test_script_page_must_contain_spoken_teacher_text(self):
        self.bodies[2] = script().split(p("P2 比较表达"))[0] + p("P2 比较表达") + p("【出示材料。】")
        self.assert_failure(self.check(), "missing_teacher_speech", "speaker_script")

    def test_script_numbering_cannot_duplicate_or_skip(self):
        for heading in ("P1 比较表达", "P3 比较表达"):
            with self.subTest(heading=heading):
                self.bodies[2] = script().replace(p("P2 比较表达"), p(heading))
                self.assert_failure(self.check(), "page_sequence", "speaker_script")

    def test_lesson_sections_missing_and_out_of_order(self):
        self.bodies[1] = lesson().replace(p("三、设计理念"), "")
        self.assert_failure(self.check(), "lesson_sections", "lesson_plan")

    def test_chinese_minimum_does_not_count_latin_or_labels(self):
        self.bodies[1] = lesson().replace(p(KEY_POINT), p("汉" * 99 + " 1234! A lesson" * 100))
        self.assert_failure(self.check(), "insufficient_chinese_characters", "lesson_plan")
        self.bodies[1] = lesson().replace(p(KEY_POINT), p("汉" * 100))
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_both_key_point_and_difficulty_are_independently_counted(self):
        self.bodies[1] = lesson().replace(p(DIFFICULTY), p("只是简短描述。"))
        self.assert_failure(self.check(), "insufficient_chinese_characters", "lesson_plan")

    def test_new_plan_allows_period_time_and_evaluation_evidence(self):
        self.options[1]["header"] = p("课时安排与建议总时长40分钟")
        result = self.check()
        self.assertTrue(result["automatic_checks_pass"], result["errors"])

    def test_new_template_allows_learning_output_evidence(self):
        self.options[1]["header"] = p("学习成果", "证据")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_duplicate_top_module_rejected(self):
        self.bodies[1] = lesson().replace(p("三、设计理念"), p("三、设计理念") * 2)
        self.assert_failure(self.check(), "lesson_sections", "lesson_plan")

    def test_metadata_value_must_not_be_empty(self):
        self.bodies[1] = lesson().replace(p("课型：新授"), p("课型："))
        self.assert_failure(self.check(), "empty_field", "lesson_plan")

    def test_metadata_missing_label_rejected(self):
        self.bodies[1] = lesson().replace(p("课型：新授"), "")
        self.assert_failure(self.check(), "field_sequence", "lesson_plan")

    def test_reference_headings_are_native_paragraphs_not_outer_table(self):
        self.bodies[1] = table([[lesson()]])
        self.assert_failure(self.check(), "lesson_heading_layout", "lesson_plan")

    def test_basis_requires_four_subsections(self):
        self.bodies[1] = lesson().replace(p("（三）学情分析"), p("其他说明"))
        self.assert_failure(self.check(), "lesson_subsections", "lesson_plan")

    def test_curriculum_basis_requires_two_nonempty_items(self):
        self.bodies[1] = lesson().replace(p("学业要求：能引用材料依据解释自己的判断。"), p("学业要求："))
        self.assert_failure(self.check(), "curriculum_basis", "lesson_plan")

    def test_curriculum_placeholder_paragraph_is_not_specific_basis(self):
        self.bodies[1] = lesson().replace(p("内容要求：课程内容中关于阅读材料、形成解释的要求。"), p("依据新课标要求。"))
        self.assert_failure(self.check(), "curriculum_basis", "lesson_plan")

    def test_two_to_four_objectives_required(self):
        self.bodies[1] = lesson().replace(p("目标2【素养落点：思维能力】学生通过双栏比较，能解释两则材料的共同点，同时获得两则支持。"), "")
        self.assert_failure(self.check(), "lesson_objectives", "lesson_plan")

    def test_objective_numbers_cannot_skip(self):
        self.bodies[1] = lesson().replace("目标2【", "目标3【")
        self.assert_failure(self.check(), "lesson_objectives", "lesson_plan")

    def test_breakthrough_strategy_required(self):
        self.bodies[1] = lesson().replace(p("突破策略：难点一通过双栏比较与反例追问，在主体活动中核验。"), "")
        self.assert_failure(self.check(), "lesson_subsections", "lesson_plan")

    def test_process_uses_connected_paragraphs_without_fixed_fields(self):
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_process_block_cannot_be_empty(self):
        self.bodies[1] = lesson().replace(p("教师呈现两种答案，追问哪一句支持解释。学生圈画、讨论并修改判断，继而比较两则材料。教师观察所引语句是否支持判断；若只抄原文，则追问语句与判断的联系。"), "", 1)
        self.assert_failure(self.check(), "empty_process_block", "lesson_plan")

    def test_process_time_sum_must_match_total(self):
        self.bodies[1] = lesson().replace("总时长40分钟", "总时长41分钟")
        self.assert_failure(self.check(), "process_time_total", "lesson_plan")

    def test_process_requires_numeric_positive_total(self):
        self.bodies[1] = lesson().replace("总时长40分钟", "总时长待定").replace("建议1课时，40分钟", "建议课时待定")
        self.assert_failure(self.check(), "lesson_duration", "lesson_plan")

    def test_more_than_five_process_blocks_can_fit_actual_logic(self):
        self.bodies[1] = lesson().replace(process_blocks(), process_blocks() * 2).replace("总时长40分钟", "总时长80分钟").replace("建议1课时，40分钟", "建议1课时，80分钟")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_content_titles_do_not_need_fixed_function_words(self):
        self.bodies[1] = lesson().replace("课堂延伸：迁移方法", "试用新方法")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_process_block_time_must_be_positive(self):
        self.bodies[1] = lesson().replace("比较两种答案（4分钟）", "比较两种答案（0分钟）")
        self.assert_failure(self.check(), "process_block_duration", "lesson_plan")

    def test_final_requires_no_visible_page_mapping(self):
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_mapping_does_not_replace_teaching_content(self):
        self.bodies[1] = lesson().replace(p("（1）导入：比较两种答案（4分钟）"), p("（1）导入：比较两种答案（4分钟）") + p("对应PPT第1—2页"))
        self.assert_failure(self.check(), "production_note_in_plan", "lesson_plan")

    def test_lesson_plan_bans_slide_count_and_mapping_in_all_parts(self):
        for note in ("全套PPT共30页", "ppt页码：P3—P5", "幻灯片第5页", "对应页面：P1—P3", "课件建议制作二十八页", "PowerPoint共30页", "P P T 页数：30", "本环节对应PPT第1—2页"):
            for part in ("body", "header", "footer"):
                with self.subTest(note=note, part=part):
                    self.bodies[1] = lesson()
                    self.options[1] = {}
                    if part == "body":
                        self.bodies[1] += p(note)
                    else:
                        self.options[1][part] = p(note)
                    self.assert_failure(self.check(), "production_note_in_plan", "lesson_plan")

    def test_teaching_preparation_can_name_ppt_without_page_production_notes(self):
        self.bodies[1] += p("教学资源：PPT展示教材材料，引导比较。教材依据可核查第12页原文。")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_text_board_has_three_required_subsections(self):
        self.bodies[1] = lesson().replace(p("副板书：暂存两种待检验答案。"), "")
        self.assert_failure(self.check(), "lesson_subsections", "lesson_plan")

    def test_text_board_cannot_be_an_empty_label(self):
        self.bodies[1] = lesson().replace(p("副板书：暂存两种待检验答案。"), p("副板书："))
        self.assert_failure(self.check(), "empty_lesson_subsection", "lesson_plan")

    def test_default_board_does_not_require_or_allow_an_image_instead(self):
        self.assertTrue(self.check()["automatic_checks_pass"])
        self.bodies[1] = lesson().replace(p("副板书：暂存两种待检验答案。"), p("副板书：暂存两种待检验答案。") + board_picture())
        self.assert_failure(self.check(), "board_text_only", "lesson_plan")

    def test_plan_review_only_checks_lesson_without_page_numbers(self):
        write_docx(self.paths[1], lesson(review=True))
        result = CHECKER.validate(lesson_path=self.paths[1], phase="plan-review")
        self.assertTrue(result["automatic_checks_pass"], result["errors"])
        self.assertEqual(result["phase"], "plan-review")
        self.assertEqual(set(result["documents"]), {"lesson_plan"})
        self.assertEqual(result["page_counts"], {})
        self.assertNotIn("script_color_and_delivery", {check["id"] for check in result["manual_checks_required"]})
        self.assertIn("lesson-plan review only", result["scope"])
        self.assertNotIn("verified", result)
        self.assertTrue(all(x["status"] == "not_assessed" for x in result["manual_checks_required"]))

    def test_plan_review_rejects_premature_page_mapping(self):
        write_docx(self.paths[1], lesson() + p("对应PPT第1—2页"))
        result = CHECKER.validate(lesson_path=self.paths[1], phase="plan-review")
        self.assert_failure(result, "production_note_in_plan", "lesson_plan")


    def test_theory_subsection_is_optional(self):
        self.bodies[1] = lesson().replace(p("（四）设计理论与教学模式") + p("任务驱动，以真实比较任务连接依据和解释。"), "")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_combined_curriculum_label_is_accepted(self):
        self.bodies[1] = lesson().replace("学业要求：能引用", "学业要求／学业质量：能引用")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_total_can_be_in_metadata_not_process_title(self):
        self.bodies[1] = lesson().replace("八、教学过程（总时长40分钟）", "八、教学过程")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_numbered_metadata_matches_supplied_template(self):
        self.bodies[1] = lesson().replace("课题：材料阅读", "1. 课题：材料阅读").replace("学科与学段：", "2. 学科与学段／年级：")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def multi_session(self, first=None, second=None):
        body = lesson().replace("建议1课时，40分钟，总时长40分钟", "建议2课时，每课时40分钟，总时长80分钟")
        body = body.replace("八、教学过程（总时长40分钟）", "八、教学过程（总时长80分钟）")
        return body.replace(process_blocks(), p("第1课时（40分钟）") + (first or process_blocks()) + p("第2课时（40分钟）") + (second or process_blocks()))

    def test_two_session_plan_does_not_split_or_shorten_outline(self):
        self.bodies[1] = self.multi_session()
        result = self.check()
        self.assertTrue(result["automatic_checks_pass"], result["errors"])
        self.assertEqual(result["page_counts"], {"outline": 2, "visual_blueprint": 2, "speaker_script": 2})

    def test_each_session_time_is_checked_not_only_overall_sum(self):
        self.bodies[1] = self.multi_session(
            process_blocks().replace("比较两种答案（4分钟）", "比较两种答案（5分钟）"),
            process_blocks().replace("比较两种答案（4分钟）", "比较两种答案（3分钟）"))
        self.assert_failure(self.check(), "session_time_total", "lesson_plan")

    def test_template_current_session_field_does_not_override_total_count(self):
        self.bodies[1] = self.multi_session().replace("建议2课时，每课时40分钟", "第1课时／共2课时；每课时40分钟")
        self.assertTrue(self.check()["automatic_checks_pass"])

    def test_session_count_must_match_declared_count(self):
        self.bodies[1] = self.multi_session().replace("建议2课时，每课时40分钟", "建议1课时，每课时80分钟")
        self.assert_failure(self.check(), "lesson_sessions", "lesson_plan")

    def test_session_ids_cannot_repeat_or_skip(self):
        for replacement in ("第1课时（40分钟）", "第3课时（40分钟）"):
            with self.subTest(replacement=replacement):
                self.bodies[1] = self.multi_session().replace("第2课时（40分钟）", replacement)
                self.assert_failure(self.check(), "lesson_sessions", "lesson_plan")

    def test_different_session_durations_are_supported(self):
        self.bodies[1] = self.multi_session().replace("建议2课时，每课时40分钟，总时长80分钟", "建议2课时，分别40和45分钟，总时长85分钟")
        self.bodies[1] = self.bodies[1].replace("八、教学过程（总时长80分钟）", "八、教学过程（总时长85分钟）")
        self.bodies[1] = self.bodies[1].replace(p("第2课时（40分钟）") + process_blocks(), p("第2课时（45分钟）") + process_blocks().replace("主体：依据核验（30分钟）", "主体：依据核验（35分钟）"))
        self.assertTrue(self.check()["automatic_checks_pass"])

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

# 生成《荒坂集团2077年度财报.pdf》——RAG 知识库测试数据（虚构内容，赛博朋克2077世界观）
# 用法：python src/20260912rag/make_report.py

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).parent / "荒坂集团2077年度财报.pdf"

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))  # 内置中文字体，无需外部字体文件
FONT = "STSong-Light"

TITLE = ParagraphStyle("title", fontName=FONT, fontSize=26, leading=36, alignment=1, spaceAfter=6)
SUBTITLE = ParagraphStyle("subtitle", fontName=FONT, fontSize=14, leading=22, alignment=1, textColor=colors.HexColor("#555555"))
H1 = ParagraphStyle("h1", fontName=FONT, fontSize=16, leading=24, spaceBefore=18, spaceAfter=8, textColor=colors.HexColor("#8B0000"))
H2 = ParagraphStyle("h2", fontName=FONT, fontSize=13, leading=20, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#333333"))
BODY = ParagraphStyle("body", fontName=FONT, fontSize=10.5, leading=17, firstLineIndent=21, spaceAfter=6)
NOTE = ParagraphStyle("note", fontName=FONT, fontSize=9, leading=14, textColor=colors.HexColor("#666666"), spaceBefore=4)


def table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, hAlign="CENTER")
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#8B0000")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F0F0")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    if doc.page > 1:
        canvas.drawString(20 * mm, 282 * mm, "荒坂集团 2077 年度报告")
        canvas.drawRightString(190 * mm, 282 * mm, "ARASAKA CORPORATION")
        canvas.setStrokeColor(colors.HexColor("#CCCCCC"))
        canvas.line(20 * mm, 280 * mm, 190 * mm, 280 * mm)
    canvas.drawCentredString(105 * mm, 12 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, topMargin=22 * mm, bottomMargin=20 * mm)
    story = []

    # ===== 封面 =====
    story.append(Spacer(1, 70 * mm))
    story.append(Paragraph("荒坂集团", TITLE))
    story.append(Paragraph("ARASAKA CORPORATION", SUBTITLE))
    story.append(Spacer(1, 12 * mm))
    story.append(Paragraph("2077 年度财务报告", TITLE))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("（虚构文本，仅供 RAG 系统测试使用）", SUBTITLE))
    story.append(Spacer(1, 50 * mm))
    story.append(Paragraph("总部：东京 · 夜之城荒坂塔", SUBTITLE))
    story.append(Paragraph("报告期间：2077年1月1日至2077年12月31日", SUBTITLE))
    story.append(PageBreak())

    # ===== 一、公司概况 =====
    story.append(Paragraph("一、公司概况", H1))
    story.append(
        Paragraph(
            "荒坂集团（Arasaka Corporation）创立于1915年，由荒坂笹井在东京创立，最初从事制造业。"
            "1960年荒坂三郎接任社长后，集团逐步转型为横跨安保、军工、金融与生物科技的全球性企业集团。"
            "历经第四次企业战争与2023年夜之城荒坂塔事件，集团于2074年完成夜之城荒坂塔的重建，"
            "重新确立了其在北美的核心地位。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "截至2077年底，集团在全球拥有雇员约595,000人，业务覆盖68个国家和地区。"
            "集团旗下主要子公司包括：荒坂安保、荒坂军工、荒坂银行、荒坂保险、荒坂生物科技，"
            "以及负责“灵魂守护（Secure Your Soul）”计划的荒坂数字遗产事业部。",
            BODY,
        )
    )
    story.append(Paragraph("关键人物", H2))
    story.append(
        Paragraph(
            "集团创始人兼最高领袖为荒坂三郎；荒坂赖宣、荒坂华子分别负责集团海外事务与内部监察。"
            "夜之城分部由荒坂美智子统筹，直接向东京总部汇报。",
            BODY,
        )
    )

    # ===== 二、财务摘要 =====
    story.append(Paragraph("二、2077年度财务摘要", H1))
    story.append(
        Paragraph(
            "2077财年，集团实现营业总收入9,860亿欧元（Eurodollar），较2076财年的9,210亿欧元增长7.1%；"
            "净利润1,520亿欧元，同比增长9.4%。业绩增长主要由“灵魂守护”计划订阅收入与安保服务合同续约驱动。",
            BODY,
        )
    )
    story.append(
        table(
            [
                ["指标（亿欧元）", "2077年", "2076年", "同比变动"],
                ["营业总收入", "9,860", "9,210", "+7.1%"],
                ["营业成本", "5,420", "5,180", "+4.6%"],
                ["毛利润", "4,440", "4,030", "+10.2%"],
                ["营业利润", "1,970", "1,800", "+9.4%"],
                ["净利润", "1,520", "1,390", "+9.4%"],
                ["经营活动现金流净额", "2,140", "1,960", "+9.2%"],
                ["总资产", "24,680", "22,850", "+8.0%"],
                ["股东权益合计", "10,730", "9,610", "+11.7%"],
            ],
            col_widths=[70 * mm, 32 * mm, 32 * mm, 32 * mm],
        )
    )

    # ===== 三、业务分部 =====
    story.append(Paragraph("三、业务分部收入", H1))
    story.append(Paragraph("集团收入按业务分部构成如下：", BODY))
    story.append(
        table(
            [
                ["业务分部", "收入（亿欧元）", "占比", "同比变动"],
                ["荒坂安保（企业安保与警务外包）", "3,250", "33.0%", "+5.8%"],
                ["荒坂军工（武器与防务装备）", "2,610", "26.5%", "+4.2%"],
                ["荒坂银行（金融与投资）", "1,580", "16.0%", "+6.0%"],
                ["荒坂保险", "1,120", "11.4%", "+3.1%"],
                ["荒坂生物科技（义体与制药）", "890", "9.0%", "+12.6%"],
                ["其他（含Relic数字遗产）", "410", "4.1%", "+78.3%"],
                ["合计", "9,860", "100.0%", "+7.1%"],
            ],
            col_widths=[74 * mm, 36 * mm, 26 * mm, 30 * mm],
        )
    )
    story.append(Paragraph("重点业务进展", H2))
    story.append(
        Paragraph(
            "1. Relic 2.0 生物芯片于2077年第三季度完成最终测试，“灵魂守护”计划付费用户突破12万人，"
            "主要为全球政要与企业高管。该项目本年度贡献收入约310亿欧元，计入“其他”分部。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "2. 荒坂安保与夜之城市政府续签为期五年的城市安全协议，合同总额约900亿欧元。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "3. 与军用科技（Militech）在防务装备市场的竞争加剧，导致军工分部毛利率下降1.8个百分点。",
            BODY,
        )
    )

    # ===== 四、合并利润表 =====
    story.append(Paragraph("四、合并利润表（2077年度）", H1))
    story.append(
        table(
            [
                ["项目（亿欧元）", "2077年", "2076年"],
                ["一、营业总收入", "9,860", "9,210"],
                ["减：营业成本", "5,420", "5,180"],
                ["销售及管理费用", "1,780", "1,690"],
                ["研发费用", "690", "540"],
                ["二、营业利润", "1,970", "1,800"],
                ["加：营业外收支净额", "-60", "-40"],
                ["三、利润总额", "1,910", "1,760"],
                ["减：所得税费用", "390", "370"],
                ["四、净利润", "1,520", "1,390"],
            ],
            col_widths=[90 * mm, 38 * mm, 38 * mm],
        )
    )
    story.append(Paragraph("注：研发费用同比增长27.8%，主要投向Relic生物芯片与义体神经接口项目。", NOTE))

    # ===== 五、合并资产负债表 =====
    story.append(Paragraph("五、合并资产负债表（2077年12月31日）", H1))
    story.append(
        table(
            [
                ["项目（亿欧元）", "期末余额", "期初余额"],
                ["货币资金", "1,980", "1,630"],
                ["应收款项", "3,120", "2,940"],
                ["存货（武器与义体库存）", "2,450", "2,300"],
                ["固定资产（含荒坂塔）", "9,860", "9,320"],
                ["无形资产（含Relic专利）", "4,270", "3,910"],
                ["其他资产", "3,000", "2,750"],
                ["资产总计", "24,680", "22,850"],
                ["负债合计", "13,950", "13,240"],
                ["股东权益合计", "10,730", "9,610"],
            ],
            col_widths=[90 * mm, 38 * mm, 38 * mm],
        )
    )

    # ===== 六、现金流量表 =====
    story.append(Paragraph("六、合并现金流量表（2077年度）", H1))
    story.append(
        table(
            [
                ["项目（亿欧元）", "2077年", "2076年"],
                ["经营活动产生的现金流量净额", "2,140", "1,960"],
                ["投资活动产生的现金流量净额", "-1,230", "-1,080"],
                ["筹资活动产生的现金流量净额", "-560", "-490"],
                ["现金及现金等价物净增加额", "350", "390"],
                ["期末现金及现金等价物余额", "1,980", "1,630"],
            ],
            col_widths=[90 * mm, 38 * mm, 38 * mm],
        )
    )

    # ===== 七、风险因素 =====
    story.append(Paragraph("七、风险因素", H1))
    story.append(
        Paragraph(
            "1. 地缘与竞争风险：与军用科技的军备竞争持续升温，若爆发第五次企业战争，"
            "集团海外资产与供应链将面临重大不确定性。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "2. 技术伦理风险：Relic生物芯片涉及人格数字化存储，部分国家已启动伦理审查，"
            "存在被要求限制销售的可能性。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "3. 安全事件风险：2023年夜之城荒坂塔事件的诉讼仍未全部了结，"
            "本年度已计提相关或有负债准备金85亿欧元。",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "4. 数据安全风险：集团数据中心多次遭受网络黑客（Netrunner）入侵尝试，"
            "本年度网络安全投入增加至210亿欧元。",
            BODY,
        )
    )

    # ===== 八、未来展望 =====
    story.append(Paragraph("八、2078年度展望", H1))
    story.append(
        Paragraph(
            "集团预计2078财年营业总收入突破10,500亿欧元。战略重点包括："
            "（1）推动“灵魂守护”计划向中端市场下沉；"
            "（2）扩大夜之城分部在北美的安保市场份额；"
            "（3）加速义体神经接口的民用化落地。"
            "荒坂集团将继续秉持“守护秩序，成就永恒”的理念，为股东创造长期价值。",
            BODY,
        )
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"已生成：{OUTPUT}")


if __name__ == "__main__":
    build()

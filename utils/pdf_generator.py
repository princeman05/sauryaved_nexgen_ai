from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

from reportlab.graphics.shapes import Drawing

from reportlab.graphics.charts.barcharts import VerticalBarChart

from reportlab.graphics import renderPDF

from reportlab.platypus.flowables import Flowable

from datetime import datetime

import os


# ==========================================
# CUSTOM CHART FLOWABLE
# ==========================================

class ChartDrawing(Flowable):

    def __init__(self, drawing):

        Flowable.__init__(self)

        self.drawing = drawing

    def wrap(self, availWidth, availHeight):

        return (400, 200)

    def draw(self):

        renderPDF.draw(
            self.drawing,
            self.canv,
            0,
            0
        )


# ==========================================
# PDF GENERATOR
# ==========================================

def generate_pdf_report(

    username,

    score,

    feedback,

    detected_skills
):

    # CREATE FOLDER
    os.makedirs(
        "static/reports",
        exist_ok=True
    )

    filename = f"report_{username}.pdf"

    filepath = f"static/reports/{filename}"

    # PDF DOCUMENT
    doc = SimpleDocTemplate(

        filepath,

        pagesize=letter,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    story = []

    # ==========================================
    # COMPANY HEADER
    # ==========================================

    company_title = """

    <font size=24 color='#06b6d4'>

    <b>AI Virtual Interviewer</b>

    </font>

    """

    story.append(

        Paragraph(
            company_title,
            styles['Title']
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(

        Paragraph(

            "<font size=12 color='gray'>Professional AI Hiring Analysis Platform</font>",

            styles['BodyText']
        )
    )

    story.append(
        Spacer(1, 25)
    )

    # ==========================================
    # REPORT TABLE
    # ==========================================

    table_data = [

        ["Candidate Name", username],

        ["Interview Score", f"{score}%"],

        ["Generated On", str(datetime.now())]
    ]

    table = Table(

        table_data,

        colWidths=[180, 300]
    )

    table.setStyle(

        TableStyle([

            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#06b6d4")),

            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),

            ('GRID', (0,0), (-1,-1), 1, colors.black),

            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0,0), (-1,-1), 12),

            ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#e2e8f0"))
        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 30)
    )

    # ==========================================
    # SKILLS SECTION
    # ==========================================

    story.append(

        Paragraph(

            "<font size=18 color='#06b6d4'><b>Detected Skills</b></font>",

            styles['Heading2']
        )
    )

    story.append(
        Spacer(1, 10)
    )

    skill_text = ", ".join(
        skill.title()
        for skill in detected_skills
    )

    story.append(

        Paragraph(

            skill_text,

            styles['BodyText']
        )
    )

    story.append(
        Spacer(1, 25)
    )

    # ==========================================
    # PERFORMANCE CHART
    # ==========================================

    story.append(

        Paragraph(

            "<font size=18 color='#06b6d4'><b>Performance Analytics</b></font>",

            styles['Heading2']
        )
    )

    story.append(
        Spacer(1, 15)
    )

    drawing = Drawing(400, 200)

    chart = VerticalBarChart()

    chart.x = 50

    chart.y = 50

    chart.height = 120

    chart.width = 300

    chart.data = [[

        score,
        max(score - 15, 0),
        min(score + 5, 100)
    ]]

    chart.categoryAxis.categoryNames = [

        'Interview',
        'Technical',
        'Confidence'
    ]

    chart.valueAxis.valueMin = 0

    chart.valueAxis.valueMax = 100

    chart.valueAxis.valueStep = 20

    chart.bars.strokeWidth = 0.5

    drawing.add(chart)

    story.append(
        ChartDrawing(drawing)
    )

    story.append(
        Spacer(1, 25)
    )

    # ==========================================
    # AI FEEDBACK
    # ==========================================

    story.append(

        Paragraph(

            "<font size=18 color='#06b6d4'><b>AI Feedback</b></font>",

            styles['Heading2']
        )
    )

    story.append(
        Spacer(1, 10)
    )

    feedback = feedback.replace(
        "\n",
        "<br/>"
    )

    story.append(

        Paragraph(

            feedback,

            styles['BodyText']
        )
    )

    story.append(
        Spacer(1, 30)
    )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    if score >= 80:

        result = """

        <font size=16 color='green'>

        <b>Excellent Performance 🚀</b>

        </font>

        """

    elif score >= 50:

        result = """

        <font size=16 color='orange'>

        <b>Good Performance 👍</b>

        </font>

        """

    else:

        result = """

        <font size=16 color='red'>

        <b>Needs Improvement 📘</b>

        </font>

        """

    story.append(

        Paragraph(

            result,

            styles['Heading2']
        )
    )

    story.append(
        Spacer(1, 40)
    )

    # ==========================================
    # FOOTER
    # ==========================================

    footer = """

    <font size=10 color='gray'>

    This report was automatically generated by
    AI Virtual Interviewer Platform.

    </font>

    """

    story.append(

        Paragraph(

            footer,

            styles['BodyText']
        )
    )

    # BUILD PDF
    doc.build(story)

    return filename
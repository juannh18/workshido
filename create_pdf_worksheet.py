"""
Workshido – PDF Worksheet Generator v2
Design: large title, sidebar, colored circle badges, rounded boxes, dashed lines
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Flowable, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT = r"C:\Users\juand\Downloads\PresentSimple_Writing_A2.pdf"

PW, PH = A4
ML = MR = 1.4*cm
MT = MB = 1.2*cm
W = PW - ML - MR

# ── COLORS ────────────────────────────────────────────────────────────────────
C_GREEN   = colors.HexColor("#2D6A4F")   # dark green (header, titles)
C_LGREEN  = colors.HexColor("#52B788")   # medium green (exercise A)
C_LLGREEN = colors.HexColor("#D8F3DC")   # light green bg
C_PURPLE  = colors.HexColor("#7B2D8B")   # exercise B
C_LPURPLE = colors.HexColor("#F3E5F5")   # light purple bg
C_ORANGE  = colors.HexColor("#E65100")   # exercise C
C_LORANGE = colors.HexColor("#FFF3E0")   # light orange bg
C_NAVY    = colors.HexColor("#1B2A4A")   # title dark navy
C_TEAL    = colors.HexColor("#00695C")   # sidebar accent
C_LTEAL   = colors.HexColor("#E0F2F1")   # light teal bg
C_YELLOW  = colors.HexColor("#FFFDE7")   # remember box
C_BORDER  = colors.HexColor("#BDBDBD")   # border gray
WHITE     = colors.white
DARK      = colors.HexColor("#1A1A1A")
GRAY      = colors.HexColor("#555555")

# ── CUSTOM FLOWABLES ──────────────────────────────────────────────────────────
class CircleBadge(Flowable):
    """Colored circle with a letter inside."""
    def __init__(self, letter, bg_color, size=0.6*cm):
        super().__init__()
        self.letter = letter
        self.bg = bg_color
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        r = self.size / 2
        c.setFillColor(self.bg)
        c.circle(r, r, r, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", self.size * 0.55)
        c.drawCentredString(r, r - self.size*0.18, self.letter)

class RoundedBox(Flowable):
    """Box with rounded corners, colored border and background."""
    def __init__(self, content_flowables, width, bg, border_color,
                 radius=6, pad=8, min_height=0):
        super().__init__()
        self.content = content_flowables
        self.width = width
        self.bg = bg
        self.border_color = border_color
        self.radius = radius
        self.pad = pad
        self.min_height = min_height
        self._content_height = None

    def wrap(self, aW, aH):
        # Measure content height
        total = self.pad * 2
        for f in self.content:
            w2, h2 = f.wrap(self.width - self.pad*2, aH)
            total += h2 + 3
        self._content_height = max(total, self.min_height)
        return self.width, self._content_height

    def draw(self):
        c = self.canv
        h = self._content_height
        w = self.width
        c.setFillColor(self.bg)
        c.setStrokeColor(self.border_color)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, w, h, self.radius, fill=1, stroke=1)
        # Draw content top-down
        y = h - self.pad
        for f in self.content:
            fw, fh = f.wrap(w - self.pad*2, h)
            y -= fh
            f.drawOn(c, self.pad, y)
            y -= 3

class DashedLines(Flowable):
    """Numbered dashed answer lines."""
    def __init__(self, n, width, line_height=0.7*cm, start=1):
        super().__init__()
        self.n = n
        self.width = width
        self.line_height = line_height
        self.start = start
        self.height = n * line_height

    def wrap(self, aW, aH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.6)
        for i in range(self.n):
            y = self.height - (i + 1) * self.line_height + 0.15*cm
            # Number
            c.setFillColor(DARK)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(0, y + 0.1*cm, f"{self.start + i}.")
            # Dashed line
            c.setDash(3, 3)
            c.line(0.5*cm, y, self.width, y)
            c.setDash()

class WritingLines(Flowable):
    """Plain dashed writing lines (no numbers)."""
    def __init__(self, n, width, line_height=0.75*cm):
        super().__init__()
        self.n = n; self.width = width
        self.line_height = line_height
        self.height = n * line_height

    def wrap(self, aW, aH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.5)
        c.setDash(3, 3)
        for i in range(self.n):
            y = self.height - (i + 1) * self.line_height + 0.2*cm
            c.line(0, y, self.width, y)
        c.setDash()

# ── STYLE HELPERS ─────────────────────────────────────────────────────────────
def S(name, font='Helvetica', size=10, color=DARK, align=TA_LEFT,
      leading=None, sb=0, sa=0, li=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          textColor=color, alignment=align,
                          leading=leading or size*1.4,
                          spaceBefore=sb, spaceAfter=sa, leftIndent=li)

def P(txt, **kw): return Paragraph(txt, S('_', **kw))
def SP(h): return Spacer(1, h)

def ex_header_row(letter, badge_color, title, title_color, subtitle=None):
    """Returns a list of flowables for an exercise header."""
    items = []
    badge_and_title = Table(
        [[CircleBadge(letter, badge_color, 0.65*cm),
          Paragraph(f'<b>{title}</b>',
                    S('_', font='Helvetica-Bold', size=11, color=title_color, leading=14))]],
        colWidths=[0.8*cm, None]
    )
    badge_and_title.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    items.append(badge_and_title)
    if subtitle:
        items.append(P(subtitle, size=9, color=GRAY, sb=2))
    return items

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)

MAIN_W   = W * 0.63
SIDE_W   = W * 0.34
GAP      = W * 0.03

story = []

# ══════════════════════════════════════════════════════════════════════════════
# TOP BAR: subject tag | name | date
# ══════════════════════════════════════════════════════════════════════════════
topbar = Table(
    [[Paragraph('<b>English Grammar in Writing  ✏</b>',
                S('_', font='Helvetica-Bold', size=9, color=WHITE)),
      Paragraph('<b>Name:</b>  ________________________  <b>Date:</b>  ______________',
                S('_', size=9, color=DARK, align=TA_RIGHT))]],
    colWidths=[7*cm, W - 7*cm], rowHeights=[0.6*cm]
)
topbar.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (0,0), C_GREEN),
    ('BACKGROUND',   (1,0), (1,0), WHITE),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING',  (0,0), (0,0), 10),
    ('RIGHTPADDING', (1,0), (1,0), 4),
    ('TOPPADDING',   (0,0), (-1,-1), 0),
    ('BOTTOMPADDING',(0,0), (-1,-1), 0),
    ('LINEBELOW',    (0,0), (-1,-1), 1, C_GREEN),
]))
story.append(topbar)
story.append(SP(0.35*cm))

# ══════════════════════════════════════════════════════════════════════════════
# TITLE BLOCK (left) + REMEMBER BOX (right)
# ══════════════════════════════════════════════════════════════════════════════
title_block = [
    Paragraph('<b>Present Simple</b>',
              S('_', font='Helvetica-Bold', size=32, color=C_NAVY, leading=36)),
    Paragraph('<i>Writing Practice</i>',
              S('_', font='Helvetica-Oblique', size=22, color=C_LGREEN, leading=26)),
    SP(0.25*cm),
    Paragraph('Write clear and simple sentences about yourself and the things you do every day.',
              S('_', size=9.5, color=GRAY, leading=13)),
]

remember_items = [
    P('<b><i>Remember!</i></b>', font='Helvetica-BoldOblique', size=11, color=C_GREEN),
    P('• Use the present simple for habits and routines.', size=8.5, color=DARK, li=4),
    P('• I/You/We/They + base verb', size=8.5, color=DARK, li=4),
    P('• He/She/It + base verb + <b>-s/-es</b>', size=8.5, color=DARK, li=4),
    P('• Example: <i>I play tennis.  She <b>plays</b> tennis.</i>', size=8.5, color=DARK, li=4),
]
remember_box = RoundedBox(remember_items, SIDE_W - 0.1*cm,
                          C_YELLOW, colors.HexColor("#F9A825"), radius=6, pad=8, min_height=3.5*cm)

title_table = Table(
    [[title_block, remember_box]],
    colWidths=[MAIN_W, SIDE_W]
)
title_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
story.append(title_table)
story.append(SP(0.4*cm))
story.append(HRFlowable(width=W, thickness=1.5, color=C_GREEN, spaceAfter=0.3*cm))

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT + SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
main = []
side = []

# ── EXERCISE A ────────────────────────────────────────────────────────────────
for fl in ex_header_row("A", C_LGREEN, "Write about your daily routine.", C_GREEN,
                        "Look at the pictures and write a sentence for each one using the <b>present simple</b>."):
    main.append(fl)
main.append(SP(0.2*cm))

# Picture boxes row (numbered 1-6)
pic_cells = []
for i in range(1, 7):
    emoji = ["⏰", "🥣", "🎒", "📚", "🎸", "💤"][i-1]
    cell_content = [
        [Paragraph(str(i), S('_', font='Helvetica-Bold', size=8, color=WHITE, align=TA_LEFT))],
        [Paragraph(emoji,  S('_', size=22, align=TA_CENTER, leading=26))],
    ]
    ct = Table(cell_content, colWidths=[2.1*cm])
    ct.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (0,0), C_LGREEN),
        ('BACKGROUND',   (0,1), (0,1), C_LLGREEN),
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ('LEFTPADDING',  (0,0), (-1,-1), 4),
        ('BOX',          (0,0), (-1,-1), 1, C_LGREEN),
    ]))
    pic_cells.append(ct)

pics_row = Table([pic_cells], colWidths=[2.15*cm]*6)
pics_row.setStyle(TableStyle([
    ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 0),  ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
main.append(pics_row)
main.append(SP(0.1*cm))
main.append(DashedLines(6, MAIN_W - 0.2*cm))
main.append(SP(0.3*cm))

# ── EXERCISE B ────────────────────────────────────────────────────────────────
for fl in ex_header_row("B", C_PURPLE, "Write a paragraph about yourself.", C_PURPLE,
                        "Use the ideas below to write 5–7 sentences about your daily life."):
    main.append(fl)
main.append(SP(0.2*cm))

# Prompt cards
prompts = ["What time do\nyou get up?", "Where do\nyou go?",
           "What do you\ndo in the\nafternoon?", "What do you\ndo in your\nfree time?",
           "What time do\nyou go to bed?"]
prompt_icons = ["⏰", "🏫", "✏️", "⚽", "🛏️"]
prompt_cells = []
for txt, icon in zip(prompts, prompt_icons):
    pc = Table([
        [Paragraph(txt.replace('\n','<br/>'), S('_', size=8, color=C_PURPLE, align=TA_CENTER, leading=11))],
        [Paragraph(icon, S('_', size=16, align=TA_CENTER, leading=20))],
    ], colWidths=[2.55*cm])
    pc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LPURPLE),
        ('BOX', (0,0), (-1,-1), 1, C_PURPLE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    prompt_cells.append(pc)

prompts_row = Table([prompt_cells], colWidths=[2.6*cm]*5)
prompts_row.setStyle(TableStyle([
    ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 0),  ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
main.append(prompts_row)
main.append(SP(0.15*cm))
main.append(WritingLines(5, MAIN_W - 0.2*cm))
main.append(SP(0.3*cm))

# ── EXERCISE C ────────────────────────────────────────────────────────────────
for fl in ex_header_row("C", C_ORANGE, "Answer the questions about your paragraph.", C_ORANGE,
                        "Write full sentences."):
    main.append(fl)
main.append(SP(0.15*cm))

c_questions = [
    "What time do you usually get up?",
    "What do you do in the afternoon?",
    "What is your favorite free-time activity?",
    "What time do you go to bed?",
]
for i, q in enumerate(c_questions):
    main.append(Paragraph(f'<b>{i+1}.</b>  {q}  ' + '_'*28,
                           S('_', size=9.5, color=DARK, leading=18)))

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

# Useful Words box
uw_items = [
    P('<b>USEFUL WORDS</b>', font='Helvetica-Bold', size=9, color=C_TEAL),
    SP(0.1*cm),
]
word_pairs = [("get up", "go to school"), ("study", "have lunch"),
              ("play", "listen to music"), ("do homework", "go to bed")]
for w1, w2 in word_pairs:
    row_p = Table([[P(w1, size=8.5, color=DARK), P(w2, size=8.5, color=DARK)]],
                  colWidths=[(SIDE_W-24)/2, (SIDE_W-24)/2])
    row_p.setStyle(TableStyle([
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ]))
    uw_items.append(row_p)

side.append(RoundedBox(uw_items, SIDE_W, C_LTEAL, C_TEAL, radius=6, pad=10))
side.append(SP(0.3*cm))

# About me example box
about_items = [
    P('<b>ABOUT ME – EXAMPLE</b>', font='Helvetica-Bold', size=8.5, color=C_TEAL),
    SP(0.05*cm),
    P('<i>I get up at 7 o\'clock every day. I go to school at 8. I have lunch at school. I study in the afternoon and I do my homework. I play the guitar and I listen to music. I go to bed at 10 o\'clock.</i>',
       font='Helvetica-Oblique', size=8.5, color=DARK, leading=13),
]
side.append(RoundedBox(about_items, SIDE_W, C_LTEAL, C_TEAL, radius=6, pad=10))
side.append(SP(0.3*cm))

# Teacher Tip box
tip_items = [
    P('⭐ <b>TEACHER TIP</b>', font='Helvetica-Bold', size=9, color=C_PURPLE),
    SP(0.05*cm),
    P('Encourage students to use time expressions in their writing.', size=8.5, color=DARK, leading=13),
    P('<b>Examples:</b> <i>every day, in the morning, on Mondays, in the evening, at night.</i>',
       size=8.5, color=DARK, leading=13),
]
side.append(RoundedBox(tip_items, SIDE_W, C_LPURPLE, C_PURPLE, radius=6, pad=10))
side.append(SP(0.3*cm))

# Challenge box
chal_items = [
    P('🏆 <b>CHALLENGE!</b>', font='Helvetica-Bold', size=9, color=C_ORANGE),
    SP(0.05*cm),
    P('Add one more sentence to your paragraph. What is your favorite day of the week and why?',
      size=8.5, color=DARK, leading=13),
]
side.append(RoundedBox(chal_items, SIDE_W, C_LORANGE, C_ORANGE, radius=6, pad=10))

# ── ASSEMBLE MAIN + SIDEBAR ───────────────────────────────────────────────────
body = Table(
    [[main, side]],
    colWidths=[MAIN_W + GAP, SIDE_W]
)
body.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING',  (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING',   (0,0), (-1,-1), 0),
    ('BOTTOMPADDING',(0,0), (-1,-1), 0),
    ('LINEAFTER', (0,0), (0,0), 0.5, colors.HexColor("#DDDDDD")),
    ('LEFTPADDING', (1,0), (1,0), 10),
]))
story.append(body)
story.append(SP(0.3*cm))

# ── FOOTER ────────────────────────────────────────────────────────────────────
footer = Table(
    [[Paragraph('workshido.com',
                S('_', font='Helvetica-Bold', size=10, color=WHITE, align=TA_CENTER))]],
    colWidths=[W], rowHeights=[0.55*cm]
)
footer.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,-1), C_GREEN),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',   (0,0), (-1,-1), 0),
    ('BOTTOMPADDING',(0,0), (-1,-1), 0),
]))
story.append(footer)

doc.build(story)
print(f"Saved: {OUTPUT}")

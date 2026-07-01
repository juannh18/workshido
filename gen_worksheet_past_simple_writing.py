from PIL import Image, ImageDraw, ImageFont
import os

W, H   = 2480, 3508
OUTPUT = r'C:\Users\juand\Downloads\PastSimple_Writing_B1.png'
FD     = 'C:/Windows/Fonts/'

# ── Palette ────────────────────────────────────────────────
BG       = '#FFFFFF'
GREEN    = '#1A5C3A'
GREEN_L  = '#E6F2EB'
AMBER    = '#C8860A'
AMBER_L  = '#FEF3DC'
BLUE     = '#1A5080'
BLUE_L   = '#E0EBF5'
ORANGE   = '#C94A1A'
ORANGE_L = '#FDEEE8'
GREY     = '#555555'
LGREY    = '#BBBBBB'
DARK     = '#1A1A2A'
WHITE    = '#FFFFFF'
LINE_CLR = '#AAAAAA'

def fnt(name, sz):
    try:    return ImageFont.truetype(FD + name, sz)
    except: return ImageFont.load_default()

img  = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Drawing helpers ────────────────────────────────────────
def box(x0, y0, x1, y1, fill=None, border=None, bw=3, r=0):
    if r: draw.rounded_rectangle([x0,y0,x1,y1], radius=r, fill=fill, outline=border, width=bw)
    else: draw.rectangle([x0,y0,x1,y1], fill=fill, outline=border, width=bw)

def t(s, x, y, f, fill=DARK, a='la', anchor=None):
    draw.text((x,y), s, font=f, fill=fill, anchor=anchor or a)

def wl(y, x0, x1, n, gap=80, clr=LINE_CLR, lw=3):
    for i in range(n):
        draw.line([(x0, y+i*gap),(x1, y+i*gap)], fill=clr, width=lw)
    return y + n*gap

def wrap(s, x, y, f, fill, maxw, lh, a='la'):
    words, lines, ln = s.split(), [], ''
    for w in words:
        test = ln+(' ' if ln else '')+w
        if draw.textlength(test,font=f) <= maxw: ln = test
        else:
            if ln: lines.append(ln)
            ln = w
    if ln: lines.append(ln)
    for i, ln in enumerate(lines):
        draw.text((x, y+i*lh), ln, font=f, fill=fill, anchor=a)
    return y+len(lines)*lh

def circle(cx, cy, r, color, letter, fsz):
    draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=color)
    draw.text((cx,cy), letter, font=fnt('calibrib.ttf',fsz), fill=WHITE, anchor='mm')

def ex_header(label, title, color, x0, y, badge='', time_str=''):
    """Draw a full-width exercise header bar and return y after it."""
    bar_h = 78
    box(x0, y, W-60, y+bar_h, fill=color, r=14)
    circle(x0+48, y+bar_h//2, 34, WHITE, label, 44)
    draw.text((x0+100, y+bar_h//2), title,
              font=fnt('calibrib.ttf', 50), fill=WHITE, anchor='lm')
    if time_str:
        draw.text((W-80, y+bar_h//2), time_str,
                  font=fnt('calibrii.ttf',38), fill='rgba(255,255,255,180)', anchor='rm')
    return y + bar_h + 24

# ── HEADER ────────────────────────────────────────────────
box(0, 0, W, 0+8, fill=AMBER)           # thin top stripe
box(0, 8, W, 290, fill=GREEN)

# Workshido brand
t('Work', 70, 32, fnt('calibrib.ttf',84), fill=WHITE)
bw = 70+draw.textlength('Work', font=fnt('calibrib.ttf',84))
t('shido', int(bw), 32, fnt('calibri.ttf',84), fill='#7EC8F0')

# Main title
t('Past Simple', 70, 138, fnt('calibrib.ttf',118), fill=WHITE)

# WRITING pill badge
pill_x, pill_y = W-380, 30
box(pill_x, pill_y, pill_x+300, pill_y+76, fill=AMBER, r=38)
t('WRITING', pill_x+150, pill_y+38, fnt('arialbd.ttf',46), fill=WHITE, anchor='mm')

# B1 badge
box(pill_x+40, pill_y+90, pill_x+260, pill_y+160, fill=WHITE, r=14)
t('B1  ·  45 min', pill_x+150, pill_y+125, fnt('calibrib.ttf',40), fill=GREEN, anchor='mm')

# ── GOAL STRIP ───────────────────────────────────────────
box(0, 290, W, 370, fill=GREEN_L)
t('✏   Write about past events using Past Simple verbs',
  70, 330, fnt('calibri.ttf',46), fill=GREEN, anchor='lm')

# ── NAME BAR ─────────────────────────────────────────────
y_bar = 396
fields = [('Name:',70,820),('Date:',850,1460),('Class:',1490,2170),('Score:',2200,2400)]
for label, x0, x1 in fields:
    box(x0, y_bar, x1, y_bar+66, fill='#F5F5F0', border=LGREY, bw=2, r=6)
    t(label, x0+14, y_bar+33, fnt('calibrib.ttf',36), fill=GREY, anchor='lm')
    lbl_w = int(draw.textlength(label+' ', font=fnt('calibrib.ttf',36)))
    draw.line([(x0+14+lbl_w, y_bar+60),(x1-14,y_bar+60)], fill=LGREY, width=2)

# ══════════════════════════════════════════════════════════
# EXERCISES  (all full-width, 70..2410)
# ══════════════════════════════════════════════════════════
X0, X1 = 70, 2410
y = 490

# ── EXERCISE A ───────────────────────────────────────────
y = ex_header('A','Read & React', GREEN, X0, y, time_str='5 min')

# Two columns: text left, questions right
col_mid = X0 + (X1-X0)//2 - 30
passage = ("Last Saturday, Maria decided to cook a special dinner for her family. "
           "She went to the market early in the morning and bought fresh vegetables and meat. "
           "When she came back home, she started cooking immediately. "
           "The meal took three hours to prepare, but her family absolutely loved it!")

box(X0, y, col_mid, y+202, fill=GREEN_L, r=12)
wrap(passage, X0+20, y+16, fnt('calibrii.ttf',38), DARK, col_mid-X0-40, 52)

# Instruction under passage
t('Underline all Past Simple verbs in the text.', X0, y+216,
  fnt('calibrib.ttf',36), fill=GREEN)

# Questions right column
qx = col_mid+40
t('Answer the questions:', qx, y, fnt('calibrib.ttf',40), fill=DARK)
qy = y+54
for q in ['1.  Where did Maria go in the morning?',
          '2.  How long did the cooking take?',
          '3.  What did the family do after dinner?']:
    t(q, qx, qy, fnt('calibri.ttf',38), fill=DARK)
    qy += 44
    draw.line([(qx, qy+4),(X1, qy+4)], fill=LINE_CLR, width=3)
    qy += 42

y = max(y+258, qy) + 40

# ── WORD BANK (between A and B) ──────────────────────────
box(X0, y, X1, y+120, fill=AMBER_L, r=14, border=AMBER, bw=3)
t('📚  Word Bank:', X0+22, y+60, fnt('calibrib.ttf',40), fill=AMBER, anchor='lm')
words = ['went · saw · had · made · met · talked · felt · thought · '
         'came · bought · gave · told · took · wrote · said · left']
t(words[0], X0+310, y+60, fnt('calibrii.ttf',40), fill=DARK, anchor='lm')
y += 140

# ── EXERCISE B ───────────────────────────────────────────
y = ex_header('B','Sentence Builder', BLUE, X0, y, time_str='10 min')
t('Write the past simple form of the verb in brackets to complete each sentence.',
  X0, y, fnt('calibri.ttf',38), fill=GREY)
y += 54

sents = [
    ('1.','She',         '(go)',          'to the cinema last Friday.'),
    ('2.','They',        '(not / finish)','their homework on time.'),
    ('3.','We',          '(have)',         'a wonderful trip to the mountains.'),
    ('4.','He',          '(see)',          'an interesting documentary yesterday.'),
    ('5.','I',           '(not / know)',   'the answer to the question.'),
    ('6.','The train',   '(arrive)',       'three hours late this morning.'),
]

# Two-column grid of sentences
col_w  = (X1-X0-40)//2
for idx, (num, subj, verb, rest) in enumerate(sents):
    col = idx % 2
    row = idx // 2
    sx  = X0 + col*(col_w+40)
    sy2 = y + row*72

    box(sx, sy2, sx+col_w, sy2+62, fill=BLUE_L if row%2==0 else WHITE, r=8, border='#D0DDF0', bw=2)
    t(num, sx+14, sy2+31, fnt('calibrib.ttf',38), fill=BLUE, anchor='lm')
    t(subj+' ', sx+58, sy2+31, fnt('calibri.ttf',38), fill=DARK, anchor='lm')
    sx2 = sx+58+int(draw.textlength(subj+' ', font=fnt('calibri.ttf',38)))
    draw.line([(sx2, sy2+54),(sx2+220, sy2+54)], fill=BLUE, width=4)
    t(' '+verb+' '+rest, sx2+228, sy2+31, fnt('calibri.ttf',36), fill=GREY, anchor='lm')

y += 3*72 + 40

# ── TIPS BOX ─────────────────────────────────────────────
box(X0, y, X1, y+96, fill='#F0F0F0', r=12, border=LGREY, bw=2)
tip_items = ['⏱ Time words: yesterday · last week · in 2023 · two days ago',
             '📝 Regular: walk→walked · talk→talked    |    ⚡ Irregular: go→went · see→saw · have→had · come→came']
t(tip_items[0], X0+22, y+22, fnt('calibri.ttf',35), fill=GREY)
t(tip_items[1], X0+22, y+62, fnt('calibri.ttf',35), fill=GREY)
y += 116

# ── EXERCISE C ───────────────────────────────────────────
y = ex_header('C','My Last Weekend', AMBER, X0, y, time_str='20 min')
t('Write a paragraph (80–100 words) about what you did last weekend.',
  X0, y, fnt('calibri.ttf',40), fill=GREY)
y += 46
t('Use at least 6 verbs from the Word Bank and include time expressions.',
  X0, y, fnt('calibrib.ttf',40), fill=AMBER)
y += 58
y = wl(y, X0, X1, 8, gap=76, clr='#AAAAAA', lw=3)
y += 36

# ── CHALLENGE ────────────────────────────────────────────
box(X0, y, X1, y+8, fill=ORANGE)
y += 18
y = ex_header('D','Challenge: The Great Escape!', ORANGE, X0, y, time_str='10 min')
t('You were a secret agent on a mission last weekend! Write a short story (100–120 words).',
  X0, y, fnt('calibri.ttf',40), fill=GREY)
y += 48

# Prompt pills
prompts = ['📍 Where?', '👤 Who?', '💥 What happened?', '🎯 How did it end?']
pw = (X1-X0-60)//4
for i,p in enumerate(prompts):
    px = X0+i*(pw+20)
    box(px, y, px+pw, y+66, fill=ORANGE_L, r=12, border=ORANGE, bw=3)
    t(p, px+pw//2, y+33, fnt('calibri.ttf',38), fill=ORANGE, anchor='mm')
y += 88

y = wl(y, X0, X1, 8, gap=76, clr='#AAAAAA', lw=3)
y += 40

# ── SELF-CHECK ───────────────────────────────────────────
box(X0, y, X1, y+80, fill=GREEN_L, r=12, border=GREEN, bw=2)
cx = X0+22
t('✅  Self-check:', cx, y+40, fnt('calibrib.ttf',38), fill=GREEN, anchor='lm')
cx += int(draw.textlength('✅  Self-check:  ', font=fnt('calibrib.ttf',38)))
for c in ['Past Simple verbs?', 'Time expressions?', 'Connectors?', 'Word count?']:
    box(cx, y+22, cx+34, y+58, fill=WHITE, r=4, border=GREEN, bw=3)
    t(c, cx+46, y+40, fnt('calibri.ttf',36), fill=DARK, anchor='lm')
    cx += 56+int(draw.textlength(c+'   ', font=fnt('calibri.ttf',36)))

# ── FOOTER ───────────────────────────────────────────────
fy = H-72
draw.line([(0, fy),(W, fy)], fill=GREEN, width=6)
box(0, fy+6, W, H, fill=GREEN)
t('workshido.com', W//2, fy+6+(H-fy-6)//2, fnt('calibri.ttf',52), fill=WHITE, anchor='mm')

# ── SAVE ─────────────────────────────────────────────────
img.save(OUTPUT, 'PNG', dpi=(300,300))
print(f'Saved: {OUTPUT}')

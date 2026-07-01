from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 2480, 3508
OUT  = r'C:\Users\juand\Downloads\PastSimple_Writing_B1_v4.png'
FD   = 'C:/Windows/Fonts/'

# ── Palette ─────────────────────────────────────────────
BG      = '#FAFAF8'
GREEN   = '#2D7A4F'
GREEN_L = '#E8F5EE'
GREEN_D = '#1A5233'
YELLOW  = '#FFFBE6'
YELLOW_B= '#F5C842'
BLUE    = '#1A5FA0'
BLUE_L  = '#E6F0FB'
ORANGE  = '#D95F1A'
ORANGE_L= '#FEF0E6'
PURPLE  = '#6B3FA0'
PURPLE_L= '#F0EAFB'
TEAL    = '#1A8080'
TEAL_L  = '#E6F5F5'
DARK    = '#1C1C2E'
GREY    = '#5A5A6A'
LGREY   = '#C8C8D0'
WHITE   = '#FFFFFF'
RED     = '#C0392B'

def f(name, sz):
    for n in [name, name.lower(), name.upper()]:
        try: return ImageFont.truetype(FD+n, sz)
        except: pass
    return ImageFont.load_default()

img = Image.new('RGB', (W,H), BG)
d   = ImageDraw.Draw(img)

# ── Core helpers ─────────────────────────────────────────
def bx(x0,y0,x1,y1,fill=None,border=None,bw=3,r=0):
    if r: d.rounded_rectangle([x0,y0,x1,y1],radius=r,fill=fill,outline=border,width=bw)
    else: d.rectangle([x0,y0,x1,y1],fill=fill,outline=border,width=bw)

def t(s,x,y,font,fill=DARK,a='la'):
    d.text((x,y),s,font=font,fill=fill,anchor=a)

def ln(x0,y0,x1,y1,fill=LGREY,lw=3):
    d.line([(x0,y0),(x1,y1)],fill=fill,width=lw)

def circle(cx,cy,r,fill=None,border=None,bw=2):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=fill,outline=border,width=bw)

def wrap(s,x,y,font,fill,maxw,lh,a='la'):
    words,lines,cur=s.split(),[],''
    for w in words:
        test=cur+(' ' if cur else '')+w
        if d.textlength(test,font=font)<=maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    for i,l in enumerate(lines): d.text((x,y+i*lh),l,font=font,fill=fill,anchor=a)
    return y+len(lines)*lh

def wlines(y,x0,x1,n,gap=82,clr='#B0B0B8',lw=3):
    for i in range(n): ln(x0,y+i*gap,x1,y+i*gap,fill=clr,lw=lw)
    return y+n*gap

# ── Icon drawers ─────────────────────────────────────────
def icon_alarm(cx,cy,sz,color):
    r=sz//2
    circle(cx,cy,r,fill=WHITE,border=color,bw=4)
    circle(cx,cy,r-14,fill=None,border=color,bw=2)
    ln(cx,cy,cx,cy-r+20,fill=color,lw=4)
    ln(cx,cy,cx+r//2,cy+r//4,fill=color,lw=4)
    d.arc([cx-r-14,cy-r-14,cx-r+6,cy-r+6],200,320,fill=color,width=4)
    d.arc([cx+r-6,cy-r-14,cx+r+14,cy-r+6],220,340,fill=color,width=4)

def icon_breakfast(cx,cy,sz,color):
    bh=sz//3
    d.ellipse([cx-sz//2,cy+bh//2,cx+sz//2,cy+sz//2+bh//2],fill=WHITE,outline=color,width=4)
    d.arc([cx-sz//2+8,cy+bh//2+8,cx+sz//2-8,cy+sz//2+bh//2-8],180,360,fill=color,width=3)
    ln(cx-4,cy+bh//4,cx-4,cy+bh//4+sz//2,fill=color,lw=4)
    d.arc([cx-4,cy+bh//4,cx+sz//3,cy+bh//4+sz//3],180,0,fill=color,width=4)
    ln(cx-sz//2-10,cy+sz//2+bh//2+4,cx+sz//2+10,cy+sz//2+bh//2+4,fill=color,lw=4)

def icon_school(cx,cy,sz,color):
    hw=sz*2//3
    bh=sz//2
    bx(cx-hw,cy,cx+hw,cy+bh,fill=WHITE,border=color,bw=4)
    d.polygon([(cx-hw-10,cy),(cx,cy-sz//3),(cx+hw+10,cy)],fill=color)
    bx(cx-12,cy+bh//3,cx+12,cy+bh,fill=color)
    for wx in [cx-hw+18,cx+hw-38]:
        bx(wx,cy+10,wx+24,cy+bh//2,fill=BLUE_L,border=color,bw=2)

def icon_study(cx,cy,sz,color):
    bw2=sz*2//3; bh=sz//2
    for i,c in enumerate([WHITE,'#F0F0F0',WHITE]):
        off=i*6
        bx(cx-bw2+off,cy-bh//2+off,cx+bw2+off,cy+bh//2+off,fill=c,border=color,bw=3,r=4)
    ln(cx-bw2+16,cy-6,cx+bw2-16,cy-6,fill=LGREY,lw=2)
    ln(cx-bw2+16,cy+16,cx+bw2-20,cy+16,fill=LGREY,lw=2)
    d.polygon([(cx+bw2-6,cy-bh//2+6),(cx+bw2+14,cy-bh//2-14),(cx+bw2+14,cy-bh//2+16)],fill=YELLOW_B)

def icon_friends(cx,cy,sz,color):
    for ox,col in [(-sz//4,color),( sz//4,'#A0C4A0')]:
        circle(cx+ox,cy-sz//3,sz//5,fill=WHITE,border=col,bw=4)
        d.arc([cx+ox-sz//4,cy-sz//8,cx+ox+sz//4,cy+sz//3],0,180,fill=col,width=4)

def icon_bed(cx,cy,sz,color):
    bw2=sz*3//4; bh=sz//2
    bx(cx-bw2,cy,cx+bw2,cy+bh,fill='#F0EBE0',border=color,bw=4,r=8)
    bx(cx-bw2,cy-bh//3,cx-bw2+sz//3,cy+bh//4,fill=color,r=6)
    bx(cx-sz//4,cy+4,cx+sz//4,cy+bh//2,fill=WHITE,border=LGREY,bw=2,r=6)
    ln(cx-bw2,cy,cx+bw2,cy,fill=color,lw=4)

ICONS = [icon_alarm, icon_breakfast, icon_school, icon_study, icon_friends, icon_bed]
LABELS= ['Woke up','Had breakfast','Went to school','Studied','Met friends','Went to bed']

# ═══════════════════════════════════════════════════════
# PAGE LAYOUT
# ═══════════════════════════════════════════════════════
PAD = 70   # left/right margin

# ── TOP BAR ──────────────────────────────────────────────
bx(0,0,W,12,fill=GREEN)
bx(0,12,W,94,fill='#F2F2EE')
t('English Grammar in Writing', PAD, 53, f('calibri.ttf',40), fill='#888888', a='lm')
# pencil simple
px=PAD+d.textlength('English Grammar in Writing  ',font=f('calibri.ttf',40))
d.polygon([(px,72),(px+10,44),(px+22,72)],fill='#888888')
bx(px+2,68,px+20,74,fill='#888888')

t('Name:', W-740, 53, f('calibri.ttf',40), fill=GREY, a='lm')
ln(W-660,82,W-380,82,fill=LGREY)
t('Date:', W-340, 53, f('calibri.ttf',40), fill=GREY, a='lm')
ln(W-265,82,W-PAD,82,fill=LGREY)

# ── TITLE BLOCK ───────────────────────────────────────────
t('Past Simple', PAD, 110, f('calibrib.ttf',148), fill=DARK)
t('Writing Practice', PAD+6, 256, f('MTCORSVA.TTF',100), fill=GREEN)
t('Write clear and simple sentences about past events.',
  PAD, 370, f('calibri.ttf',40), fill=GREY)

# ── STICKY NOTE ───────────────────────────────────────────
sn_x, sn_y, sn_w, sn_h = 1480, 100, 920, 390
# shadow
bx(sn_x+8,sn_y+8,sn_x+sn_w+8,sn_y+sn_h+8,fill='#CCCCCC',r=6)
# note body
bx(sn_x,sn_y,sn_x+sn_w,sn_y+sn_h,fill='#FFFDE7',border='#F5C842',bw=3,r=6)
# folded corner
d.polygon([(sn_x+sn_w-40,sn_y),(sn_x+sn_w,sn_y+40),(sn_x+sn_w,sn_y)],fill='#E8B800')
# tape
bx(sn_x+sn_w//2-50,sn_y-18,sn_x+sn_w//2+50,sn_y+16,fill='rgba(220,210,180,160)',r=4)
t('Remember!', sn_x+18, sn_y+22, f('calibrib.ttf',44), fill='#5C4A00')
note_lines=[
    '• Use past simple for completed actions',
    '• I/You/We/They + verb (past form)',
    '• Regular: walk → walked, play → played',
    '• Irregular: go → went, see → saw',
    '• Example:  She visited her friend.',
]
for i,nl in enumerate(note_lines):
    t(nl, sn_x+18, sn_y+82+i*54, f('calibri.ttf',33) if nl.startswith('•') else f('calibrib.ttf',33),
      fill='#4A3A00')
# lightbulb
lbx,lby=sn_x+sn_w+30,sn_y-10
circle(lbx+36,lby+46,38,fill=YELLOW,border=YELLOW_B,bw=4)
bx(lbx+18,lby+80,lbx+54,lby+100,fill='#C8A800',r=4)
bx(lbx+24,lby+100,lbx+48,lby+114,fill='#A08000',r=3)

# ── DIVIDER ───────────────────────────────────────────────
ln(PAD,438,W-PAD,438,fill=GREEN_L,lw=5)

# ═══════════════════════════════════════════════════════
# SECTION A
# ═══════════════════════════════════════════════════════
y = 460
# Badge
d.ellipse([PAD,y,PAD+72,y+72],fill=GREEN)
t('A', PAD+36, y+36, f('calibrib.ttf',52), fill=WHITE, a='mm')
t('Write about your last Saturday.', PAD+88, y+36, f('calibrib.ttf',54), fill=GREEN, a='lm')
y += 84
t('Look at the activities and write ONE sentence for each picture using the Past Simple.',
  PAD, y, f('calibri.ttf',38), fill=GREY)
y += 54

# ── 6 picture boxes 3×2 ──────────────────────────────────
MAIN_W  = W - PAD*2 - 360   # leave space for Useful Words
BOX_GAP = 24
BOX_W   = (MAIN_W - BOX_GAP*2) // 3
BOX_H   = 185

for idx in range(6):
    col = idx % 3
    row = idx // 3
    bx0 = PAD + col*(BOX_W+BOX_GAP)
    by0 = y + row*(BOX_H+BOX_GAP)
    bx1 = bx0 + BOX_W
    by1 = by0 + BOX_H
    bx(bx0,by0,bx1,by1,fill=WHITE,border=GREEN,bw=3,r=14)
    # number badge
    d.ellipse([bx0+12,by0+12,bx0+52,by0+52],fill=GREEN)
    t(str(idx+1),bx0+32,by0+32,f('calibrib.ttf',34),fill=WHITE,a='mm')
    # icon
    ICONS[idx]((bx0+bx1)//2,(by0+by1)//2-14,100,GREEN)
    # label
    t(LABELS[idx],(bx0+bx1)//2,by1-16,f('calibri.ttf',32),fill=GREY,a='mb')

# USEFUL WORDS box
uw_x = W - PAD - 330
uw_y = y
bx(uw_x,uw_y,uw_x+330,uw_y+BOX_H*2+BOX_GAP,fill=GREEN_L,border=GREEN,bw=3,r=14)
bx(uw_x,uw_y,uw_x+330,uw_y+54,fill=GREEN,r=10)
t('USEFUL WORDS',uw_x+165,uw_y+27,f('calibrib.ttf',32),fill=WHITE,a='mm')
uw_words=[('get up','study'),('eat breakfast','meet friends'),
          ('go to school','watch TV'),('do homework','go to bed'),
          ('play sport','listen to music')]
for i,(a,b) in enumerate(uw_words):
    uy=uw_y+68+i*56
    t('•  '+a, uw_x+14, uy, f('calibri.ttf',31), fill=GREEN_D)
    t('•  '+b, uw_x+170, uy, f('calibri.ttf',31), fill=GREEN_D)

y += 2*(BOX_H+BOX_GAP) + 20

# 6 writing lines
for i in range(6):
    t(f'{i+1}.',PAD,y+4,f('calibrib.ttf',38),fill=GREEN)
    ln(PAD+48,y+40,W-PAD,y+40,fill='#C0C0C8')
    y += 64

ln(PAD,y+10,W-PAD,y+10,fill=GREEN_L,lw=5)
y += 34

# ═══════════════════════════════════════════════════════
# SECTION B
# ═══════════════════════════════════════════════════════
d.ellipse([PAD,y,PAD+72,y+72],fill=BLUE)
t('B', PAD+36, y+36, f('calibrib.ttf',52), fill=WHITE, a='mm')
t('Write a paragraph about your last weekend.', PAD+88, y+36, f('calibrib.ttf',54), fill=BLUE, a='lm')
y += 84
t('Use the ideas below to write 5–7 sentences about what you did last weekend.',
  PAD, y, f('calibri.ttf',38), fill=GREY)
y += 56

# Prompt cards (5 across)
MAIN_W2 = W - PAD*2
CW = (MAIN_W2 - 60) // 5
CARD_COLORS = [
    (BLUE,   BLUE_L,   '🕐','What time\ndid you\nget up?'),
    (GREEN,  GREEN_L,  '📍','Where\ndid you\ngo?'),
    (ORANGE, ORANGE_L, '🍽','What did\nyou eat\nor cook?'),
    (PURPLE, PURPLE_L, '🎯','What did\nyou do\nfor fun?'),
    (TEAL,   TEAL_L,   '💤','What time\ndid you\ngo to bed?'),
]
for i,(col,col_l,icon,lbl) in enumerate(CARD_COLORS):
    cx0=PAD+i*(CW+15); cx1=cx0+CW
    bx(cx0,y,cx1,y+190,fill=col_l,border=col,bw=3,r=16)
    t(icon,(cx0+cx1)//2,y+58,f('seguiemj.ttf',58),fill=col,a='mm')
    for j,line in enumerate(lbl.split('\n')):
        t(line,(cx0+cx1)//2,y+106+j*36,f('calibrib.ttf',30),fill=col,a='mm')
y += 190

# Writing lines section B
for _ in range(5):
    ln(PAD,y+40,W-PAD,y+40,fill='#C0C0C8')
    y += 64
y += 12

# About Me example (full width, below writing lines)
am_x = PAD
am_y = y
bx(am_x,am_y,am_x+640,am_y+470,fill=PURPLE_L,border=PURPLE,bw=3,r=16)
bx(am_x,am_y,am_x+640,am_y+58,fill=PURPLE,r=12)
t('ABOUT ME — EXAMPLE',am_x+320,am_y+29,f('calibrib.ttf',32),fill=WHITE,a='mm')
# avatar circle
circle(am_x+60,am_y+126,38,fill='#D4A0D4',border=PURPLE,bw=3)
circle(am_x+60,am_y+102,22,fill='#EED0EE',border=PURPLE,bw=2)
d.arc([am_x+22,am_y+120,am_x+98,am_y+168],0,180,fill=PURPLE,width=3)
example=[
    "Last Saturday I got up at 8 o'clock.",
    "I had breakfast with my family. Then",
    "I went to the park and played football",
    "with my friends. In the afternoon,",
    "we had lunch together. At night",
    "I watched a film and went to bed late.",
]
am_w = W - PAD*2
bx(am_x,am_y,am_x+am_w,am_y+240,fill=PURPLE_L,border=PURPLE,bw=3,r=16)
bx(am_x,am_y,am_x+am_w,am_y+52,fill=PURPLE,r=12)
t('ABOUT ME — EXAMPLE',(am_x+am_x+am_w)//2,am_y+26,f('calibrib.ttf',34),fill=WHITE,a='mm')
# avatar
circle(am_x+52,am_y+140,36,fill='#D4A0D4',border=PURPLE,bw=3)
circle(am_x+52,am_y+118,20,fill='#EED0EE',border=PURPLE,bw=2)
d.arc([am_x+16,am_y+134,am_x+88,am_y+174],0,180,fill=PURPLE,width=3)
half_w = am_w//2 - 20
col1=["Last Saturday I got up at 8 o'clock.","I had breakfast with my family.","Then I went to the park and played football."]
col2=["In the afternoon, we had lunch together.","At night I watched a film and relaxed.","I went to bed late. It was a great day!"]
for i,el in enumerate(col1):
    t(el,am_x+106,am_y+66+i*54,f('calibrii.ttf',32),fill=DARK)
for i,el in enumerate(col2):
    t(el,am_x+am_w//2+14,am_y+66+i*54,f('calibrii.ttf',32),fill=DARK)

y = am_y+256
ln(PAD,y,W-PAD,y,fill=BLUE_L,lw=5)
y += 34

# ═══════════════════════════════════════════════════════
# SECTION C
# ═══════════════════════════════════════════════════════
d.ellipse([PAD,y,PAD+72,y+72],fill=TEAL)
t('C', PAD+36, y+36, f('calibrib.ttf',52), fill=WHITE, a='mm')
t('Answer the questions about your paragraph.', PAD+88, y+36, f('calibrib.ttf',54), fill=TEAL, a='lm')
y += 84
t('Write full sentences.', PAD, y, f('calibri.ttf',38), fill=GREY)
y += 54

questions=[
    '1.  What time did you usually get up last weekend?',
    '2.  Where did you go and who did you go with?',
    '3.  What was your favourite activity last weekend?',
    '4.  What time did you go to bed on Saturday night?',
]
for q in questions:
    t(q,PAD,y,f('calibri.ttf',40),fill=DARK)
    y+=44
    ln(PAD,y+4,W-PAD,y+4,fill='#C0C0C8')
    y+=56

ln(PAD,y+10,W-PAD,y+10,fill=TEAL_L,lw=5)
y += 30

# ═══════════════════════════════════════════════════════
# TEACHER TIP  +  CHALLENGE
# ═══════════════════════════════════════════════════════
half = (W - PAD*2 - 40) // 2
tip_h = 190

# Teacher Tip
bx(PAD,y,PAD+half,y+tip_h,fill=BLUE_L,border=BLUE,bw=3,r=16)
bx(PAD,y,PAD+half,y+60,fill=BLUE,r=12)
# star badge
d.ellipse([PAD+14,y+68,PAD+82,y+136],fill=YELLOW_B)
t('★',PAD+48,y+102,f('calibrib.ttf',52),fill=WHITE,a='mm')
t('TEACHER TIP',PAD+100,y+30,f('calibrib.ttf',40),fill=WHITE,a='lm')
wrap("Encourage students to use time expressions: last Saturday, in the morning, after that, then, finally, in the evening, at night.",
     PAD+96,y+72,f('calibri.ttf',34),DARK,half-110,46)

# Challenge
bx(PAD+half+40,y,W-PAD,y+tip_h,fill=ORANGE_L,border=ORANGE,bw=3,r=16)
bx(PAD+half+40,y,W-PAD,y+60,fill=ORANGE,r=12)
d.ellipse([PAD+half+54,y+68,PAD+half+122,y+136],fill=YELLOW_B)
t('🏆',PAD+half+88,y+102,f('seguiemj.ttf',44),fill=WHITE,a='mm')
t('CHALLENGE!',PAD+half+134,y+30,f('calibrib.ttf',40),fill=WHITE,a='lm')
wrap('Add TWO more sentences using a different time expression in each one. Try to use an irregular verb!',
     PAD+half+130,y+72,f('calibri.ttf',34),DARK,W-PAD-PAD-half-150,46)
y += tip_h + 24

# Extra writing lines for challenge
wlines(y,PAD,W-PAD,2,gap=66)

# ── FOOTER ───────────────────────────────────────────────
bx(0,H-76,W,H,fill=GREEN)
t('workshido.com',W//2,H-38,f('calibri.ttf',50),fill=WHITE,a='mm')

img.save(OUT,'PNG',dpi=(300,300))
print(f'Saved: {OUT}')

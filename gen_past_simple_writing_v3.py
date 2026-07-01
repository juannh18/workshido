from PIL import Image, ImageDraw, ImageFont
import os, math

W, H   = 2480, 3508
OUT    = r'C:\Users\juand\Downloads\PastSimple_Writing_B1_v3.png'
FD     = 'C:/Windows/Fonts/'

# ── Palette ───────────────────────────────────────────────
BG       = '#FFFFFF'
GREEN    = '#2E7D52'
GREEN_L  = '#EAF5EE'
GREEN_D  = '#1A5C3A'
YELLOW   = '#FFF176'
YELLOW_D = '#F9A825'
BLUE     = '#1565C0'
BLUE_L   = '#E3F0FF'
ORANGE   = '#E65100'
ORANGE_L = '#FFF3E0'
PURPLE   = '#6A1B9A'
PURPLE_L = '#F3E5F5'
GREY     = '#555555'
LGREY    = '#BBBBBB'
DARK     = '#1A1A2A'
WHITE    = '#FFFFFF'
TEAL     = '#00695C'
TEAL_L   = '#E0F2F1'

def fnt(name, sz):
    for n in [name, name.lower(), name.upper()]:
        try: return ImageFont.truetype(FD + n, sz)
        except: pass
    return ImageFont.load_default()

img  = Image.new('RGB', (W, H), BG)
d    = ImageDraw.Draw(img)

# ── Helpers ───────────────────────────────────────────────
def box(x0,y0,x1,y1,fill=None,border=None,bw=3,r=0):
    if r: d.rounded_rectangle([x0,y0,x1,y1],radius=r,fill=fill,outline=border,width=bw)
    else: d.rectangle([x0,y0,x1,y1],fill=fill,outline=border,width=bw)

def txt(s,x,y,f,fill=DARK,a='la'):
    d.text((x,y),s,font=f,fill=fill,anchor=a)

def wrap(s,x,y,f,fill,maxw,lh,a='la'):
    words,lines,ln=s.split(),[],''
    for w in words:
        test=ln+(' ' if ln else '')+w
        if d.textlength(test,font=f)<=maxw: ln=test
        else:
            if ln: lines.append(ln)
            ln=w
    if ln: lines.append(ln)
    for i,ln in enumerate(lines):
        d.text((x,y+i*lh),ln,font=f,fill=fill,anchor=a)
    return y+len(lines)*lh

def wline(y,x0,x1,color='#BBBBBB',lw=3):
    d.line([(x0,y),(x1,y)],fill=color,width=lw)

def wlines(y,x0,x1,n,gap=80):
    for i in range(n): wline(y+i*gap,x0,x1)
    return y+n*gap

def dash_box(x0,y0,x1,y1,color,dash=16):
    """Dashed border rectangle"""
    for side in [(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]:
        x_a,y_a,x_b,y_b=side
        length=math.hypot(x_b-x_a,y_b-y_a)
        steps=int(length//(dash*2))
        for s in range(steps):
            t0=s*2*dash/length; t1=min((s*2+1)*dash/length,1)
            d.line([(x_a+t0*(x_b-x_a),y_a+t0*(y_b-y_a)),
                    (x_a+t1*(x_b-x_a),y_a+t1*(y_b-y_a))],fill=color,width=3)

def img_box(x0,y0,x1,y1,num,label,color):
    """Numbered picture placeholder box"""
    box(x0,y0,x1,y1,fill='#F8F8F8',border=color,bw=3,r=12)
    # number circle
    cx,cy=x0+34,y0+34
    d.ellipse([cx-24,cy-24,cx+24,cy+24],fill=color)
    txt(str(num),cx,cy,fnt('calibrib.ttf',34),fill=WHITE,a='mm')
    # label at bottom
    txt(label,(x0+x1)//2,y1-20,fnt('calibri.ttf',30),fill=GREY,a='mb')
    # subtle image icon lines
    mx,my=(x0+x1)//2,(y0+y1)//2-10
    d.ellipse([mx-30,my-30,mx+30,my+30],outline=LGREY,width=2)
    d.rectangle([mx-40,my+10,mx+40,my+40],outline=LGREY,width=2)

def sticky_note(x0,y0,w,h,title,lines_txt,bg=YELLOW,border=YELLOW_D):
    """Sticky note style box"""
    # slight rotation effect with shadow
    box(x0+6,y0+6,x0+w+6,y0+h+6,fill='#CCCCCC',r=4)
    box(x0,y0,x0+w,y0+h,fill=bg,border=border,bw=2,r=4)
    # folded corner
    d.polygon([(x0+w-30,y0),(x0+w,y0+30),(x0+w,y0)],fill=border)
    txt(title,x0+14,y0+16,fnt('calibrib.ttf',36),fill='#333300')
    ty=y0+58
    for line in lines_txt:
        if line.startswith('•'):
            txt(line,x0+14,ty,fnt('calibri.ttf',31),fill='#333300')
        else:
            txt(line,x0+14,ty,fnt('calibrib.ttf',31),fill='#333300')
        ty+=40
    return ty

def section_label(letter,x,y,color,title,font_sz=52):
    """Colored circle + bold section title"""
    d.ellipse([x,y,x+70,y+70],fill=color)
    txt(letter,x+35,y+35,fnt('calibrib.ttf',46),fill=WHITE,a='mm')
    txt(title,x+86,y+35,fnt('calibrib.ttf',font_sz),fill=color,a='lm')

def prompt_card(x0,y0,x1,y1,icon,label,color):
    box(x0,y0,x1,y1,fill=color+'22',border=color,bw=3,r=14)
    txt(icon,(x0+x1)//2,y0+42,fnt('seguiemj.ttf',44),fill=color,a='mm')
    wrap(label,(x0+x1)//2,y0+68,fnt('calibri.ttf',30),DARK,(x1-x0-20),36,a='mm')

# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════
# Top thin stripe
box(0,0,W,10,fill=GREEN)

# Subject tag bar
box(0,10,W,90,fill='#F0F0F0')
txt('English Grammar in Writing',70,50,fnt('calibri.ttf',40),fill=GREY,a='lm')
# pencil icon (simple drawn)
px,py=640,28
for seg in [((px,py+44),(px+10,py+12),'#555555'),
            ((px+10,py+12),(px+22,py),'#888888'),
            ((px,py+44),(px+12,py+44),'#888888')]:
    d.line([seg[0],seg[1]],fill=seg[2],width=4)

# Name / Date
txt('Name:',W-700,50,fnt('calibri.ttf',38),fill=GREY,a='lm')
d.line([(W-620,78),(W-350,78)],fill=LGREY,width=2)
txt('Date:',W-320,50,fnt('calibri.ttf',38),fill=GREY,a='lm')
d.line([(W-250,78),(W-50,78)],fill=LGREY,width=2)

# ── TITLE ─────────────────────────────────────────────
txt('Past Simple',70,110,fnt('calibrib.ttf',140),fill=DARK)
txt('Writing Practice',70,248,fnt('MTCORSVA.TTF',96),fill=GREEN)

# ── Tagline ───────────────────────────────────────────
txt('Write clear and simple sentences about past events and experiences.',
    70,356,fnt('calibri.ttf',38),fill=GREY)

# ── STICKY NOTE (Remember!) ────────────────────────────
sn_x,sn_y=1560,100
sticky_note(sn_x,sn_y,840,360,'Remember!',[
    '• Use past simple for finished actions',
    '• I/You/He/She/We/They + verb (past)',
    '• Regular: walk → walked',
    '• Irregular: go → went, see → saw',
    '• Example: She visited her friend.',
],bg='#FFFDE7',border='#F9A825')

# ── Divider line ──────────────────────────────────────
wline(420,60,W-60,color=GREEN_L,lw=4)

# ═══════════════════════════════════════════════════════
# SECTION A  — Write about what you did
# ═══════════════════════════════════════════════════════
y=448
section_label('A',70,y,GREEN,'Write about your last Saturday.')
y+=92
txt('Look at the activities and write ONE sentence about each picture using the Past Simple.',
    70,y,fnt('calibri.ttf',38),fill=GREY)
y+=52

# 6 picture boxes (2 rows × 3)
activities=[('1','Woke up'),('2','Had breakfast'),('3','Went to school'),
            ('4','Studied'),('5','Met friends'),('6','Went to bed')]
bw2=(W-140-80)//3
bh=220
for idx,(num,lbl) in enumerate(activities):
    col=idx%3; row=idx//3
    bx=70+col*(bw2+40); by=y+row*(bh+50)
    img_box(bx,by,bx+bw2,by+bh,num,lbl,GREEN)

y+=2*(bh+50)+10

# 6 writing lines
for i in range(6):
    txt(f'{i+1}.',70,y+12,fnt('calibrib.ttf',38),fill=GREEN)
    wline(y+44,110,W-70)
    y+=74

wline(y,60,W-60,color=GREEN_L,lw=4)
y+=30

# ── USEFUL WORDS sidebar box (floated right, overlapping) ──
uw_x=W-520; uw_y=448+92+52
box(uw_x,uw_y,W-50,uw_y+310,fill=GREEN_L,border=GREEN,bw=3,r=14)
box(uw_x,uw_y,W-50,uw_y+52,fill=GREEN,r=10)
txt('USEFUL WORDS',(uw_x+W-50)//2,uw_y+26,fnt('calibrib.ttf',34),fill=WHITE,a='mm')
uw_pairs=[('get up','go to school'),('study','have lunch'),
          ('play sport','listen to music'),('do homework','go to bed')]
for i,(a,b) in enumerate(uw_pairs):
    ty2=uw_y+66+i*58
    txt(a,uw_x+16,ty2,fnt('calibri.ttf',33),fill=GREEN_D)
    txt(b,uw_x+270,ty2,fnt('calibri.ttf',33),fill=GREEN_D)

# ═══════════════════════════════════════════════════════
# SECTION B  — Write a paragraph
# ═══════════════════════════════════════════════════════
section_label('B',70,y,BLUE,'Write a paragraph about your last weekend.')
y+=92
txt('Use the ideas below to write 5–7 sentences about what you did.',
    70,y,fnt('calibri.ttf',38),fill=GREY)
y+=56

# Prompt cards
cards=[('🕐','What time\ndid you get up?'),
       ('📍','Where\ndid you go?'),
       ('🍽','What did you\neat / cook?'),
       ('🎯','What did you\ndo for fun?'),
       ('💤','What time did\nyou go to bed?')]
cw=(W-140-80)//5
for i,(icon,lbl) in enumerate(cards):
    cx=70+i*(cw+20)
    box(cx,y,cx+cw,y+160,fill=BLUE_L,border=BLUE,bw=3,r=14)
    txt(icon,cx+cw//2,y+54,fnt('seguiemj.ttf',56),fill=BLUE,a='mm')
    wrap(lbl,cx+cw//2,y+100,fnt('calibri.ttf',29),BLUE,cw-20,36,a='mm')

y+=180

# Writing lines
y=wlines(y,70,W-70,7,gap=78)
y+=30

# ── ABOUT ME example box (right) + TEACHER TIP (right) ──
ex_x=W-660; ex_y=y-78*7-180
box(ex_x,ex_y,W-50,ex_y+340,fill=PURPLE_L,border=PURPLE,bw=3,r=14)
box(ex_x,ex_y,W-50,ex_y+52,fill=PURPLE,r=10)
txt('ABOUT ME — EXAMPLE',(ex_x+W-50)//2,ex_y+26,fnt('calibrib.ttf',30),fill=WHITE,a='mm')
example_lines=[
    'Last Saturday I got up at 8 o\'clock.',
    'I had breakfast with my family.',
    'Then I went to the park and played',
    'football with my friends. After that,',
    'we had lunch together. In the evening',
    'I watched a film and went to bed late.',
]
for i,ln in enumerate(example_lines):
    txt(ln,ex_x+16,ex_y+66+i*44,fnt('calibrii.ttf',31),fill=DARK)

wline(y-10,60,W-60,color=BLUE_L,lw=4)

# ═══════════════════════════════════════════════════════
# SECTION C  — Answer the questions
# ═══════════════════════════════════════════════════════
section_label('C',70,y,TEAL,'Answer the questions about your paragraph.')
y+=92
txt('Write full sentences.',70,y,fnt('calibri.ttf',38),fill=GREY)
y+=56

questions=['1.  What time did you usually get up last weekend?',
           '2.  Where did you go and who did you go with?',
           '3.  What was your favourite activity?',
           '4.  What time did you go to bed?']
for q in questions:
    txt(q,70,y,fnt('calibri.ttf',38),fill=DARK)
    y+=46
    wline(y,70,W-70)
    y+=66

wline(y,60,W-60,color=TEAL_L,lw=4)
y+=28

# ═══════════════════════════════════════════════════════
# TEACHER TIP  +  CHALLENGE  (side by side)
# ═══════════════════════════════════════════════════════
col_mid2=(W-140)//2+70
tip_h=200

# Teacher Tip
box(70,y,col_mid2-20,y+tip_h,fill=BLUE_L,border=BLUE,bw=3,r=14)
box(70,y,col_mid2-20,y+54,fill=BLUE,r=10)
d.ellipse([80,y+60,136,y+116],fill=YELLOW_D)
txt('★',108,y+88,fnt('calibrib.ttf',42),fill=WHITE,a='mm')
txt('TEACHER TIP',160,y+26,fnt('calibrib.ttf',38),fill=WHITE,a='lm')
wrap('Encourage students to use time expressions: last Saturday, in the morning, after that, finally, in the evening.',
     144,y+68,fnt('calibri.ttf',33),DARK,col_mid2-230,42)

# Challenge
box(col_mid2+20,y,W-50,y+tip_h,fill=ORANGE_L,border=ORANGE,bw=3,r=14)
box(col_mid2+20,y,W-50,y+54,fill=ORANGE,r=10)
d.ellipse([col_mid2+30,y+60,col_mid2+86,y+116],fill=YELLOW_D)
txt('🏆',col_mid2+58,y+88,fnt('seguiemj.ttf',36),fill=WHITE,a='mm')
txt('CHALLENGE!',col_mid2+100,y+26,fnt('calibrib.ttf',38),fill=WHITE,a='lm')
wrap('Add TWO more sentences to your paragraph. Use a different time expression in each one.',
     col_mid2+36,y+68,fnt('calibri.ttf',33),DARK,W-col_mid2-86,42)

y+=tip_h+28

# ── Extra writing lines for challenge ─────────────────
wlines(y,70,W-70,2,gap=78)
y+=2*78+20

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
box(0,H-70,W,H,fill=GREEN)
txt('workshido.com',W//2,H-35,fnt('calibri.ttf',46),fill=WHITE,a='mm')

# ── SAVE ──────────────────────────────────────────────
img.save(OUT,'PNG',dpi=(300,300))
print(f'Saved: {OUT}')

"""Genera el HTML del recurso 'Complete List of English Irregular Verbs'.
Uso: python tools/build_irregular_verbs.py
Salida: tools/te_output/irregular-verbs-list.html
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = open(os.path.join(REPO, 'tools/te_output/_logo_datauri.txt'), encoding='utf-8').read().strip()

# (base, past simple, past participle)
GROUP_SAME = [
    ("bet","bet","bet"),("burst","burst","burst"),("cast","cast","cast"),("cost","cost","cost"),
    ("cut","cut","cut"),("fit","fit","fit"),("hit","hit","hit"),("hurt","hurt","hurt"),
    ("let","let","let"),("put","put","put"),("quit","quit","quit"),("read","read","read"),
    ("set","set","set"),("shut","shut","shut"),("spread","spread","spread"),("split","split","split"),
    ("bid","bid","bid"),("broadcast","broadcast","broadcast"),("knit","knit","knit"),("rid","rid","rid"),
    ("shed","shed","shed"),("slit","slit","slit"),("upset","upset","upset"),("wed","wed","wed"),
]

# Group B (56 verbs, past simple = past participle) is the biggest single
# block in the whole sheet, so it benefits the most from pattern grouping:
# 10 shared-ending families cover 42 of the 56 verbs.
GROUP_B_SUBGROUPS = [
    ("&minus;ought / &minus;aught pattern", [
        ("bring","brought","brought"),("buy","bought","bought"),("catch","caught","caught"),("fight","fought","fought"),
        ("seek","sought","sought"),("teach","taught","taught"),("think","thought","thought"),
    ]),
    ("Shifts to a short &ldquo;u&rdquo; sound", [
        ("dig","dug","dug"),("hang","hung","hung"),("spin","spun","spun"),("stick","stuck","stuck"),
        ("sting","stung","stung"),("strike","struck","struck"),("swing","swung","swung"),
    ]),
    ("&minus;eep &rarr; &minus;ept pattern", [
        ("creep","crept","crept"),("keep","kept","kept"),("sleep","slept","slept"),("sweep","swept","swept"),
        ("weep","wept","wept"),
    ]),
    ("Long ee/ea &rarr; short e", [
        ("bleed","bled","bled"),("feed","fed","fed"),("flee","fled","fled"),("lead","led","led"),("meet","met","met"),
    ]),
    ("&minus;ind &rarr; &minus;ound pattern", [
        ("bind","bound","bound"),("find","found","found"),("grind","ground","ground"),("wind","wound","wound"),
    ]),
    ("&minus;end &rarr; &minus;ent pattern", [
        ("bend","bent","bent"),("lend","lent","lent"),("send","sent","sent"),("spend","spent","spent"),
    ]),
    ("&minus;ay &rarr; &minus;aid pattern", [
        ("lay","laid","laid"),("pay","paid","paid"),("say","said","said"),
    ]),
    ("Just add &minus;t", [
        ("deal","dealt","dealt"),("feel","felt","felt"),("mean","meant","meant"),
    ]),
    ("stand / understand", [
        ("stand","stood","stood"),("understand","understood","understood"),
    ]),
    ("&minus;ell &rarr; &minus;old pattern", [
        ("sell","sold","sold"),("tell","told","told"),
    ]),
    ("No shared pattern &mdash; memorize individually", [
        ("build","built","built"),("get","got","got"),("have","had","had"),("hear","heard","heard"),
        ("hold","held","held"),("leave","left","left"),("lose","lost","lost"),("make","made","made"),
        ("shine","shone","shone"),("shoot","shot","shot"),("sit","sat","sat"),("slide","slid","slid"),
        ("win","won","won"),("light","lit","lit"),
    ]),
]
GROUP_PAST_PP_SAME = [v for _, vs in GROUP_B_SUBGROUPS for v in vs]

GROUP_BASE_PP_SAME = [
    ("become","became","become"),("come","came","come"),("run","ran","run"),
]

# Group D (all three forms different) is the one worth teaching by sub-pattern
# rather than alphabetically: 8 of the 9 recognisable vowel/ending families
# below cover 36 of the 46 verbs, leaving only 10 true one-offs to memorize
# with no shared shape at all.
GROUP_D_SUBGROUPS = [
    ("i &rarr; a &rarr; u vowel shift", [
        ("begin","began","begun"),("drink","drank","drunk"),("ring","rang","rung"),("shrink","shrank","shrunk"),
        ("sing","sang","sung"),("sink","sank","sunk"),("spring","sprang","sprung"),("swim","swam","swum"),
    ]),
    ("&minus;oke / &minus;oken pattern", [
        ("break","broke","broken"),("choose","chose","chosen"),("freeze","froze","frozen"),("speak","spoke","spoken"),
        ("steal","stole","stolen"),("wake","woke","woken"),("weave","wove","woven"),
    ]),
    ("&minus;ew / &minus;own pattern", [
        ("blow","blew","blown"),("draw","drew","drawn"),("fly","flew","flown"),("grow","grew","grown"),
        ("know","knew","known"),("throw","threw","thrown"),("withdraw","withdrew","withdrawn"),
    ]),
    ("i_e &rarr; o_e &rarr; ‑en pattern", [
        ("drive","drove","driven"),("ride","rode","ridden"),("rise","rose","risen"),("write","wrote","written"),
    ]),
    ("&minus;ake / &minus;ook / &minus;aken pattern", [
        ("mistake","mistook","mistaken"),("shake","shook","shaken"),("take","took","taken"),
    ]),
    ("&minus;ear / &minus;ore / &minus;orn pattern", [
        ("swear","swore","sworn"),("tear","tore","torn"),("wear","wore","worn"),
    ]),
    ("&minus;ive / &minus;iven pattern", [
        ("forgive","forgave","forgiven"),("give","gave","given"),
    ]),
    ("Long vowel shortens + ‑en", [
        ("bite","bit","bitten"),("hide","hid","hidden"),
    ]),
    ("No shared pattern &mdash; memorize individually", [
        ("be","was / were","been"),("do","did","done"),("eat","ate","eaten"),("fall","fell","fallen"),
        ("forbid","forbade","forbidden"),("forget","forgot","forgotten"),("go","went","gone"),("lie","lay","lain"),
        ("see","saw","seen"),("show","showed","shown"),
    ]),
]
GROUP_ALL_DIFFERENT = [v for _, vs in GROUP_D_SUBGROUPS for v in vs]

def verb_cell(v):
    base, past, pp = v
    return f"<div class='v-row'><span class='vb'>{base}</span><span class='ar'>&rarr;</span><span class='vp'>{past}</span><span class='ar'>&rarr;</span><span class='vpp'>{pp}</span></div>"

def section_html(letter, title, note, color, verbs):
    cells = "".join(verb_cell(v) for v in verbs)
    return f"""
    <div class="section" style="--accent:{color}">
      <div class="section-head">
        <span class="badge">{letter}</span>
        <span class="s-title">{title}</span>
        <span class="s-note">{note}</span>
        <span class="s-count">{len(verbs)} verbs</span>
      </div>
      <div class="v-grid">{cells}</div>
    </div>
    """

def subgroup_block(label, verbs):
    cells = "".join(verb_cell(v) for v in verbs)
    return f"<div class='sub-label'>{label} <span class='sub-count'>({len(verbs)})</span></div>{cells}"

def section_grouped_html(letter, title, note, color, subgroups):
    total_g = sum(len(vs) for _, vs in subgroups)
    blocks = "".join(subgroup_block(label, vs) for label, vs in subgroups)
    return f"""
    <div class="section" style="--accent:{color}">
      <div class="section-head">
        <span class="badge">{letter}</span>
        <span class="s-title">{title}</span>
        <span class="s-note">{note}</span>
        <span class="s-count">{total_g} verbs</span>
      </div>
      <div class="v-grid grouped">{blocks}</div>
    </div>
    """

sections_html = section_html("A", "All Three Forms Are the Same", "base = past simple = past participle", "#0e7c66", GROUP_SAME)
sections_html += section_grouped_html("B", "Past Simple = Past Participle", "only the base form is different &mdash; grouped by shared ending", "#1a3a5c", GROUP_B_SUBGROUPS)
sections_html += section_html("C", "Base Form = Past Participle", "only the past simple is different", "#7b2d8b", GROUP_BASE_PP_SAME)
sections_html += section_grouped_html("D", "All Three Forms Are Different", "grouped by shared vowel/ending pattern where one exists", "#c0392b", GROUP_D_SUBGROUPS)
total = len(GROUP_SAME) + len(GROUP_PAST_PP_SAME) + len(GROUP_BASE_PP_SAME) + len(GROUP_ALL_DIFFERENT)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Caveat:wght@600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Nunito','Arial',sans-serif; font-size:11.5px; color:#1a1a2e; background:#fff; }}
  .page-wrap {{ padding:10px 34px 6px; }}

  .brand-row {{ display:flex; align-items:center; gap:9px; margin-bottom:3px; }}
  .brand-logo {{ width:24px; height:24px; border-radius:7px; }}
  .brand-mini {{ font-size:15px; font-weight:900; letter-spacing:0.3px; color:#1a3a5c; }}
  .brand-mini .brand-accent {{ color:#6ea8dc; }}

  .header {{ text-align:center; margin:3px 0 3px; }}
  .header .eyebrow {{ font-size:9.5px; font-weight:800; letter-spacing:3px; text-transform:uppercase; color:#e67e22; }}
  .header h1 {{ margin-top:3px; font-size:22px; font-weight:900; color:#1a3a5c; }}
  .header .subtitle {{ margin-top:3px; font-size:11px; font-weight:600; color:#555; }}

  .header-rule {{ border-bottom:2px solid #1a3a5c; margin:7px 0 7px; }}

  .legend {{ display:flex; justify-content:center; gap:26px; background:#f4f7fb; border:1px solid #d7e0ea; border-radius:10px; padding:6px 18px; margin-bottom:9px; font-size:10.5px; font-weight:700; color:#1a3a5c; }}
  .legend span.lg-arrow {{ color:#8a97a8; font-weight:400; margin:0 4px; }}

  .section {{ margin-bottom:6px; break-inside:avoid; page-break-inside:avoid; }}
  .section-head {{ display:flex; align-items:baseline; gap:10px; border-bottom:2px solid var(--accent); padding-bottom:2px; margin-bottom:4px; }}
  .badge {{ width:18px; height:18px; min-width:18px; border-radius:50%; background:var(--accent); color:#fff; font-size:10.5px; font-weight:800; display:flex; align-items:center; justify-content:center; }}
  .s-title {{ font-size:13px; font-weight:800; color:var(--accent); text-transform:uppercase; letter-spacing:0.3px; }}
  .s-note {{ font-size:9.5px; font-style:italic; color:#6b7686; flex:1; }}
  .s-count {{ font-size:9.5px; font-weight:700; color:#8a97a8; white-space:nowrap; }}

  .v-grid {{ column-count:3; column-gap:20px; }}
  .v-row {{ display:flex; align-items:baseline; font-size:10.4px; line-height:1.3; break-inside:avoid; white-space:nowrap; }}
  .v-row .vb {{ font-weight:800; color:#1a1a2e; min-width:52px; }}
  .v-row .ar {{ color:#b7c0cc; margin:0 2px; font-size:8px; }}
  .v-row .vp {{ color:#333; min-width:56px; }}
  .v-row .vpp {{ color:#333; }}

  .v-grid.grouped {{ display:grid; grid-template-columns:repeat(4, 170px); column-gap:12px; row-gap:0; }}
  .v-grid.grouped .v-row {{ line-height:1.14; overflow:visible; }}
  .v-grid.grouped .sub-label {{ grid-column:1 / -1; font-size:8.6px; font-weight:700; color:var(--accent); opacity:0.8; margin:2px 0 0; line-height:1.1; }}
  .sub-label .sub-count {{ font-weight:600; color:#8a97a8; }}

  .footer-note {{ background:#fff8ea; border:1px solid #f0dca0; border-radius:10px; padding:7px 18px; margin-top:4px; font-size:10.5px; line-height:1.4; color:#6b5300; }}
  .footer-note b {{ color:#8a5a00; }}

  .footer {{ text-align:center; margin-top:4px; padding-top:4px; border-top:1px solid #d7e0ea; font-size:9px; color:#8a97a8; letter-spacing:0.5px; }}
</style>
</head>
<body>
<div class="page-wrap">

  <div class="brand-row" style="justify-content:center;">
    <img class="brand-logo" src="{LOGO}" alt="Workshido">
    <div class="brand-mini">Work<span class="brand-accent">shido</span></div>
  </div>

  <div class="header">
    <div class="eyebrow">Free Reference Sheet</div>
    <h1>The Complete List of English Irregular Verbs</h1>
    <div class="subtitle">Base Form &middot; Past Simple &middot; Past Participle &mdash; {total} verbs grouped by pattern, from A1 to C1</div>
  </div>
  <div class="header-rule"></div>

  <div class="legend">
    <span>Base Form <span class="lg-arrow">&rarr;</span> Past Simple <span class="lg-arrow">&rarr;</span> Past Participle</span>
  </div>

  {sections_html}

  <div class="footer-note">
    <b>Study tip:</b> Learn irregular verbs by pattern, not alphabetically. Groups A and C are the fastest to memorize, and even Groups B and D &mdash; the biggest and the hardest &mdash; break into shared ending/vowel families; only 24 of the 129 verbs truly share no pattern with anything else.
  </div>

  <div class="footer">workshido.com</div>

</div>
</body>
</html>
"""

out = os.path.join(REPO, 'tools/te_output/irregular-verbs-list.html')
open(out, 'w', encoding='utf-8').write(html)
print('OK', out, len(html), 'chars', '| total verbs:', total)

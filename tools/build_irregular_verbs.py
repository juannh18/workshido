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

GROUP_PAST_PP_SAME = [
    ("bend","bent","bent"),("bleed","bled","bled"),("bring","brought","brought"),("build","built","built"),
    ("buy","bought","bought"),("catch","caught","caught"),("creep","crept","crept"),("deal","dealt","dealt"),
    ("dig","dug","dug"),("feed","fed","fed"),("feel","felt","felt"),("fight","fought","fought"),
    ("find","found","found"),("flee","fled","fled"),("get","got","got"),("grind","ground","ground"),
    ("hang","hung","hung"),("have","had","had"),("hear","heard","heard"),("hold","held","held"),
    ("keep","kept","kept"),("lay","laid","laid"),("lead","led","led"),("leave","left","left"),
    ("lend","lent","lent"),("lose","lost","lost"),("make","made","made"),("mean","meant","meant"),
    ("meet","met","met"),("pay","paid","paid"),("say","said","said"),("seek","sought","sought"),
    ("sell","sold","sold"),("send","sent","sent"),("shine","shone","shone"),("shoot","shot","shot"),
    ("sit","sat","sat"),("sleep","slept","slept"),("slide","slid","slid"),("spend","spent","spent"),
    ("stand","stood","stood"),("stick","stuck","stuck"),("sting","stung","stung"),("strike","struck","struck"),
    ("sweep","swept","swept"),("swing","swung","swung"),("teach","taught","taught"),("tell","told","told"),
    ("think","thought","thought"),("understand","understood","understood"),("weep","wept","wept"),("win","won","won"),
    ("wind","wound","wound"),("bind","bound","bound"),("light","lit","lit"),("spin","spun","spun"),
    ("shake","-","-"),  # placeholder removed below
]
GROUP_PAST_PP_SAME = [v for v in GROUP_PAST_PP_SAME if v[1] != "-"]

GROUP_BASE_PP_SAME = [
    ("become","became","become"),("come","came","come"),("run","ran","run"),
]

GROUP_ALL_DIFFERENT = [
    ("be","was / were","been"),("begin","began","begun"),("bite","bit","bitten"),("blow","blew","blown"),
    ("break","broke","broken"),("choose","chose","chosen"),("do","did","done"),("draw","drew","drawn"),
    ("drink","drank","drunk"),("drive","drove","driven"),("eat","ate","eaten"),("fall","fell","fallen"),
    ("fly","flew","flown"),("forbid","forbade","forbidden"),("forget","forgot","forgotten"),("forgive","forgave","forgiven"),
    ("freeze","froze","frozen"),("give","gave","given"),("go","went","gone"),("grow","grew","grown"),
    ("hide","hid","hidden"),("know","knew","known"),("lie","lay","lain"),("mistake","mistook","mistaken"),
    ("ride","rode","ridden"),("ring","rang","rung"),("rise","rose","risen"),("see","saw","seen"),
    ("shake","shook","shaken"),("show","showed","shown"),("shrink","shrank","shrunk"),("sing","sang","sung"),
    ("sink","sank","sunk"),("speak","spoke","spoken"),("spring","sprang","sprung"),("steal","stole","stolen"),
    ("swear","swore","sworn"),("swim","swam","swum"),("take","took","taken"),("tear","tore","torn"),
    ("throw","threw","thrown"),("wake","woke","woken"),("wear","wore","worn"),("weave","wove","woven"),
    ("withdraw","withdrew","withdrawn"),("write","wrote","written"),
]

SECTIONS = [
    ("A", "All Three Forms Are the Same", "base = past simple = past participle", "#0e7c66", GROUP_SAME),
    ("B", "Past Simple = Past Participle", "only the base form is different", "#1a3a5c", GROUP_PAST_PP_SAME),
    ("C", "Base Form = Past Participle", "only the past simple is different", "#7b2d8b", GROUP_BASE_PP_SAME),
    ("D", "All Three Forms Are Different", "the hardest group &mdash; memorize each one", "#c0392b", GROUP_ALL_DIFFERENT),
]

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

sections_html = "".join(section_html(*s) for s in SECTIONS)
total = sum(len(s[4]) for s in SECTIONS)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Caveat:wght@600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Nunito','Arial',sans-serif; font-size:11.5px; color:#1a1a2e; background:#fff; }}
  .page-wrap {{ padding:16px 34px 8px; }}

  .brand-row {{ display:flex; align-items:center; gap:9px; margin-bottom:4px; }}
  .brand-logo {{ width:26px; height:26px; border-radius:7px; }}
  .brand-mini {{ font-size:16px; font-weight:900; letter-spacing:0.3px; color:#1a3a5c; }}
  .brand-mini .brand-accent {{ color:#6ea8dc; }}

  .header {{ text-align:center; margin:6px 0 4px; }}
  .header .eyebrow {{ font-size:10px; font-weight:800; letter-spacing:3px; text-transform:uppercase; color:#e67e22; }}
  .header h1 {{ margin-top:5px; font-size:25px; font-weight:900; color:#1a3a5c; }}
  .header .subtitle {{ margin-top:5px; font-size:11.5px; font-weight:600; color:#555; }}

  .header-rule {{ border-bottom:2px solid #1a3a5c; margin:10px 0 10px; }}

  .legend {{ display:flex; justify-content:center; gap:26px; background:#f4f7fb; border:1px solid #d7e0ea; border-radius:10px; padding:8px 18px; margin-bottom:14px; font-size:10.5px; font-weight:700; color:#1a3a5c; }}
  .legend span.lg-arrow {{ color:#8a97a8; font-weight:400; margin:0 4px; }}

  .section {{ margin-bottom:12px; break-inside:avoid; page-break-inside:avoid; }}
  .section-head {{ display:flex; align-items:baseline; gap:10px; border-bottom:2px solid var(--accent); padding-bottom:4px; margin-bottom:8px; }}
  .badge {{ width:20px; height:20px; min-width:20px; border-radius:50%; background:var(--accent); color:#fff; font-size:11px; font-weight:800; display:flex; align-items:center; justify-content:center; }}
  .s-title {{ font-size:13.5px; font-weight:800; color:var(--accent); text-transform:uppercase; letter-spacing:0.3px; }}
  .s-note {{ font-size:10px; font-style:italic; color:#6b7686; flex:1; }}
  .s-count {{ font-size:9.5px; font-weight:700; color:#8a97a8; white-space:nowrap; }}

  .v-grid {{ column-count:3; column-gap:20px; }}
  .v-row {{ display:flex; align-items:baseline; font-size:10.6px; line-height:1.36; break-inside:avoid; white-space:nowrap; }}
  .v-row .vb {{ font-weight:800; color:#1a1a2e; min-width:52px; }}
  .v-row .ar {{ color:#b7c0cc; margin:0 2px; font-size:8px; }}
  .v-row .vp {{ color:#333; min-width:56px; }}
  .v-row .vpp {{ color:#333; }}

  .footer-note {{ background:#fff8ea; border:1px solid #f0dca0; border-radius:10px; padding:9px 18px; margin-top:6px; font-size:11px; line-height:1.5; color:#6b5300; }}
  .footer-note b {{ color:#8a5a00; }}

  .footer {{ text-align:center; margin-top:6px; padding-top:5px; border-top:1px solid #d7e0ea; font-size:9px; color:#8a97a8; letter-spacing:0.5px; }}
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
    <b>Study tip:</b> Learn irregular verbs by pattern, not alphabetically. Group A (all forms the same) and Group C (base = past participle) are the fastest to memorize &mdash; start there before tackling Group D.
  </div>

  <div class="footer">workshido.com</div>

</div>
</body>
</html>
"""

out = os.path.join(REPO, 'tools/te_output/irregular-verbs-list.html')
open(out, 'w', encoding='utf-8').write(html)
print('OK', out, len(html), 'chars', '| total verbs:', total)

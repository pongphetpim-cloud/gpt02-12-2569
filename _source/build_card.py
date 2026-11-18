"""สร้าง prompt-card.html + PDF (A4 หน้าเดียว) — prompt ดึงจาก content.py
ใช้: PYTHONIOENCODING=utf-8 python build_card.py
"""
from html import escape
from content import P
from common import ROOT, html_to_pdf

steps = ["ใส่ไฟล์", "ถามดูว่าเข้าใจถูก", "Slide deck<br>ภาษาไทย · Presenter", "วาง prompt<br>กด Generate now",
         "ตรวจ 3 อย่าง<br>แล้วสั่งแก้ทีละสไลด์", "ดาวน์โหลด + ซ้อมตอบ"]
six = "".join(f"<div><b>{i}</b><span>{s}</span></div>" for i, s in enumerate(steps, 1))

page = f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8">
<title>การ์ด prompt — AI ช่วยงาน ภาค 2</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"IBM Plex Sans Thai","Noto Sans Thai","Leelawadee UI",Tahoma,sans-serif;color:#16181d;background:#fff;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:296mm;padding:11mm 12mm 9mm;display:flex;flex-direction:column;gap:4.2mm;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2.5px solid #16181d;padding-bottom:2.5mm}}
.top h1{{font-size:21pt;line-height:1.1;letter-spacing:-.4px}}
.top h1 span{{color:#0e5e58}}
.top p{{font-size:8.6pt;color:#737b89;text-align:right;line-height:1.4}}
.half{{border-radius:4mm;padding:4mm 4.5mm;display:flex;flex-direction:column;gap:2.6mm}}
.nb{{background:#f3f1fe;border:1px solid #d9d3fb}}
.cg{{background:#eef7f2;border:1px solid #cfe7da}}
.hd{{display:flex;align-items:center;gap:2.5mm}}
.chip{{font-size:8pt;font-weight:700;letter-spacing:1px;color:#fff;padding:.8mm 2.6mm;border-radius:1.4mm}}
.nb .chip{{background:#5b46d6}} .cg .chip{{background:#0f7a4a}}
.hd h2{{font-size:13.5pt;letter-spacing:-.2px}}
.hd small{{margin-left:auto;font-size:8.4pt;color:#737b89}}
.six{{display:grid;grid-template-columns:repeat(6,1fr);gap:1.8mm}}
.six div{{background:#fff;border:1px solid #d9d3fb;border-radius:2.4mm;padding:2mm 2.2mm;font-size:8.3pt;line-height:1.35;font-weight:600}}
.six b{{display:grid;place-items:center;width:5.2mm;height:5.2mm;border-radius:1.4mm;background:#5b46d6;color:#fff;font-size:8.5pt;margin-bottom:1.2mm}}
.lbl{{font-size:8.2pt;font-weight:700;letter-spacing:.8px;color:#5a6172}}
pre{{font-family:inherit;white-space:pre-wrap;background:#171b26;color:#e9edf5;border-radius:2.6mm;padding:3mm 3.6mm;
  font-size:9.6pt;line-height:1.6}}
.row{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm}}
.chk{{background:#fff;border:1px solid #d9d3fb;border-radius:2.4mm;padding:2.2mm 2.8mm;font-size:8.6pt;line-height:1.4;color:#3b4150}}
.chk b{{display:block;font-size:9.6pt;color:#16181d}}
.gold{{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}}
.gold > div{{background:#fff;border:1px solid #cfe7da;border-radius:2.4mm;padding:2.4mm 3mm}}
.gold pre{{font-size:10pt;margin-top:1.2mm;background:#0e3b37}}
.gold p{{font-size:8.2pt;color:#5a6172;margin-top:1.2mm;line-height:1.4}}
.rules{{display:flex;gap:2mm;font-size:8.4pt;color:#3b4150;line-height:1.4}}
.rules div{{flex:1;border-left:3px solid #a52a2a;background:#fbeaea;padding:1.8mm 2.6mm;border-radius:0 2mm 2mm 0}}
.rules b{{color:#a52a2a}}
.foot{{margin-top:auto;font-size:7.8pt;color:#9aa1ad;display:flex;justify-content:space-between}}
@media screen{{body{{background:#e6e3dc}} .page{{margin:10mm auto;background:#fff;box-shadow:0 2px 14px rgba(0,0,0,.15)}}}}
</style></head><body><div class="page">

<div class="top"><h1>การ์ด prompt · <span>AI ช่วยงาน ภาค 2</span></h1>
<p>ติดไว้ข้างจอ · ถ่ายรูปเก็บไว้ได้<br>prompt ทั้งหมดมีปุ่มคัดลอกในคู่มือผู้เรียน</p></div>

<div class="half nb">
<div class="hd"><span class="chip">NotebookLM</span><h2>ทำสไลด์ประชุมใน 30 นาที</h2><small>notebooklm.google.com · ฟรี</small></div>
<div class="six">{six}</div>
<div class="lbl">แม่แบบ prompt สไลด์ — เติม [วงเล็บ] แล้ววางในช่อง Describe</div>
<pre>{escape(P['nb_slide_tpl'])}</pre>
<div class="lbl">ตรวจ 3 อย่างก่อนเชื่อ</div>
<div class="row">
<div class="chk"><b>1 · ตัวสะกดไทย</b>สไลด์เป็นรูปที่ AI วาด กดขยายดูทีละหน้า</div>
<div class="chk"><b>2 · ตัวเลขตรงเอกสาร</b>เทียบกับต้นฉบับอย่างน้อย 3 ตัวเลข</div>
<div class="chk"><b>3 · คำที่ AI เติมเอง</b>ชื่อ ตำแหน่ง คำคุณศัพท์ที่เอกสารไม่ได้พูด</div>
</div>
</div>

<div class="half cg">
<div class="hd"><span class="chip">ChatGPT</span><h2>สูตรสั่งงาน R-C-C-F + 2 ประโยคทอง</h2><small>chatgpt.com</small></div>
<pre>{escape(P['f_tpl'])}</pre>
<div class="gold">
<div><div class="lbl">ประโยคทอง 1 · ตอนยังไม่รู้จะบอกอะไร</div><pre>{escape(P['gold1'])}</pre></div>
<div><div class="lbl">ประโยคทอง 2 · บอกเกณฑ์ผ่าน</div><pre>{escape(P['gold2'])}</pre><p>เกณฑ์ต้องตรวจได้ เช่น ไม่เกิน 8 บรรทัด · มีวันที่ — ไม่ใช่ "ให้ดี ให้สวย"</p></div>
</div>
</div>

<div class="rules">
<div><b>ห้าม</b> ใส่ข้อมูลลับบริษัท/ลูกค้าจริง ในบัญชีส่วนตัว</div>
<div><b>ห้าม</b> ส่งงานของ AI ออกไปโดยไม่ตรวจ</div>
<div><b>ห้าม</b> กด "อนุญาต" โดยไม่อ่าน · คนกดส่งต้องเป็นคุณ</div>
</div>
<div class="foot"><span>ชื่อคุณอยู่บนงานนั้น ไม่ใช่ชื่อ AI</span><span>พุธ 2 ธ.ค. 2569</span></div>
</div></body></html>
"""
out = ROOT / "prompt-card.html"
out.write_text(page, encoding="utf-8")
html_to_pdf(out, ROOT / "prompt-card.pdf")
print("prompt-card.html + pdf done")

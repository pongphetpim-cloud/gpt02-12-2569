"""สร้าง คู่มือเตรียมตัวก่อนอบรม.html + PDF (A4 2 หน้า) สำหรับรุ่น 2
CSS และ QR กลุ่มไลน์ ยกจากคู่มือของรุ่นแรก (../คู่มือเตรียมตัวก่อนอบรม.html — ไม่แก้ไฟล์นั้น)
ใช้: PYTHONIOENCODING=utf-8 python build_prep.py
"""
import re
from common import ROOT, html_to_pdf

OLD = (ROOT.parent / "คู่มือเตรียมตัวก่อนอบรม.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", OLD, re.S).group(1)
QR = re.search(r'<img class="qr" src="(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)"', OLD).group(1)
CSS = (CSS.replace("--brand:#1c3f8f; --soft:#eaf0fb;", "--brand:#0e5e58; --soft:#e1f0ed;")
          .replace("#c5d3ee", "#c4e3dd").replace("#4a67a8", "#3d827a").replace("#dbe4f5", "#d6ece8")
          .replace("#8aa0cf", "#8cc4bb").replace("#c3d1ee", "#bfded8")
       + """
.faq span b{display:inline;color:var(--ink);font-size:inherit}
.nbc{background:#f3f1fe;border-color:#d9d3fb}
.nbc ol.steps li::before{color:#5b46d6}
.nbtag{display:inline-block;background:#5b46d6;color:#fff;font-size:10px;font-weight:700;letter-spacing:.8px;padding:1px 8px;border-radius:5px;vertical-align:1px}
""")

page = f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8">
<title>เตรียมตัวก่อนอบรม — AI ช่วยงาน ภาค 2</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<div class="hero">
<h1>เตรียมตัวก่อนเข้าอบรม<br>AI ช่วยงาน ภาค 2</h1>
<p>ทำสไลด์ประชุมใน 30 นาทีด้วย NotebookLM + มอบงานให้ ChatGPT ทำทั้งชิ้น — ใช้เวลาเตรียม 10 นาที</p>
<div class="when"><span><b>วันอบรม</b> พุธ 2 ธันวาคม 2569</span><span><b>รอบเช้า</b> 09:00–12:00 น.</span><span><b>รอบบ่าย</b> 13:00–17:00 น.</span></div>
<p class="note2">คุณเข้าอบรม <b>รอบใดรอบหนึ่ง</b> ตามที่ผู้จัดแจ้ง — รอบบ่ายมีโมดูลเสริมเพิ่มอีก 1 ชั่วโมง · <b>ทุกอย่างในคลาสใช้บัญชีฟรีได้</b></p>
</div>

<!-- ============ 1 ============ -->
<h2><span class="n" style="background:#5b46d6">1</span>ลองเข้า NotebookLM มาก่อน 1 ครั้ง <span class="t">ใช้เวลา 5 นาที · ฟรี · ข้อนี้สำคัญที่สุด</span></h2>
<div class="card nbc">
<p><span class="nbtag">ของใหม่</span> &nbsp;เรื่องแรกของคลาสคือทำสไลด์ด้วย <b>NotebookLM</b> ของ Google (ชื่อใหม่ <b>Gemini Notebook</b> — ตัวเดียวกัน)
คนที่เข้าได้ตั้งแต่ที่บ้าน จะได้สไลด์ชุดแรกภายใน 30 นาทีแรกของคลาส</p>
<ol class="steps">
<li>เปิดเบราว์เซอร์ (Chrome / Edge) เข้า <b>notebooklm.google.com</b> <span class="dim">— จะเด้งไปหน้าใหม่ชื่อ Gemini Notebook เอง ไม่ต้องตกใจ</span></li>
<li>ล็อกอินด้วยบัญชี Google <span class="dim">(Gmail ส่วนตัวได้เลย)</span></li>
<li>กด <b>+ New notebook</b> (มุมขวาบน) แล้วใส่ไฟล์อะไรก็ได้ที่ไม่ลับ 1 ไฟล์ เช่น PDF หรือ Word</li>
<li>พิมพ์ถาม 1 คำถามเกี่ยวกับไฟล์นั้น — ถ้ามันตอบกลับมาพร้อมเลขอ้างอิง <b>[1]</b> แปลว่าพร้อมแล้ว</li>
</ol>
<div style="margin-top:7px;padding-top:6px;border-top:1px solid #d9d3fb">
<b>ถ้าเข้าไม่ได้ หรือขึ้นว่าไม่มีสิทธิ์ใช้งาน:</b> บัญชี Google ของบริษัทบางแห่งปิดบริการนี้ไว้ ให้ใช้ <b>Gmail ส่วนตัว</b> แทน ·
ถ้ายังไม่มี Gmail ให้สมัครมาก่อน (ฟรี 3 นาที) อย่ารอไปสมัครในห้อง
</div>
</div>

<!-- ============ 2 ============ -->
<h2><span class="n">2</span>เช็ก ChatGPT ว่ายังเข้าได้ <span class="t">2 นาที</span></h2>
<div class="card hi">
<ol class="steps">
<li>เข้า <b>chatgpt.com</b> ล็อกอินบัญชีเดิมที่ใช้ตอนเรียนรอบที่แล้ว แล้วลองพิมพ์ 1 ข้อ</li>
<li>มือถือ: ติดตั้ง/อัปเดต <b>แอป ChatGPT</b> ให้เป็นรุ่นล่าสุด <span class="dim">(รอบบ่ายมีช่วงซ้อมคุยด้วยเสียง)</span></li>
<li><b>ไม่บังคับ:</b> ถ้ามีคอมส่วนตัว ลง <b>แอป ChatGPT บนคอม</b> ไว้ด้วย <span class="dim">— ใช้ทำการบ้าน "มอบงานให้ AI ทำทั้งชิ้น"</span></li>
</ol>
</div>

<!-- ============ 3 ============ -->
<h2><span class="n">3</span>เตรียมของ + เข้ากลุ่มไลน์</h2>
<div class="two">
<div class="card">
<div class="chk"><span class="b"></span><div><b>โน้ตบุ๊ก + สายชาร์จ</b> <span>คลาสนี้ลงมือทำตลอด เครื่องอะไรก็ได้ที่เปิดเว็บได้</span></div></div>
<div class="chk"><span class="b"></span><div><b>มือถือ + หูฟัง</b> <span>หูฟังข้างเดียวก็พอ ใช้ตอนซ้อมคุยด้วยเสียง</span></div></div>
<div class="chk" style="margin-bottom:0"><span class="b"></span><div><b>รหัสผ่าน Google และ ChatGPT</b> <span>ต้องล็อกอินทั้ง 2 อย่าง ถ้าจำไม่ได้ให้รีเซ็ตมาก่อน</span></div></div>
</div>
<div class="card hi" style="display:flex;gap:12px;align-items:flex-start">
<div style="flex:none;text-align:center">
<img class="qr" src="{QR}" alt="QR กลุ่มไลน์ของคลาส">
<span class="dim" style="font-size:9.8px;display:block;margin-top:2px">กลุ่มเดิม</span>
</div>
<div style="min-width:0">
<div class="chk"><span class="b"></span><div><b>อยู่ในกลุ่มไลน์ของคลาส</b> <span>ใช้กลุ่มเดิมจากรอบที่แล้ว ถ้าออกไปแล้วสแกน QR หรือเข้า <b>line.me/R/ti/g/AXVM5NDZLE</b></span></div></div>
<div class="chk" style="margin-bottom:0"><span class="b"></span><div><b>ดาวน์โหลดไฟล์ตัวอย่างมาก่อน</b> <span>โหลดจากลิงก์ในกลุ่มไลน์ <b>แตกไฟล์ zip</b> ไว้ในเครื่อง และจำให้ได้ว่าเก็บตรงไหน</span></div></div>
</div>
</div>
</div>

<!-- ============ 4 ============ -->
<h2><span class="n">4</span>คิดล่วงหน้าไว้ 2 เรื่อง <span class="t">ไม่ต้องเขียนยาว นึกไว้ในหัวก็พอ</span></h2>
<div class="card ok">
<div class="two">
<div><b class="big">ก. สไลด์ที่คุณอยากได้ 1 ชุด</b>
<p style="margin-top:3px">งานไหนที่คุณต้องทำสไลด์บ่อย เช่น สรุปยอดเดือน รายงานโครงการ อบรมพนักงานใหม่ —
และมีเอกสารต้นทาง<b>ที่ไม่ลับ</b>อยู่แล้ว (รายงาน คู่มือ บันทึก) <span class="dim">ใช้ทำการบ้านหลังคลาส</span></p></div>
<div><b class="big">ข. เรื่องเล่า 30 วินาที</b>
<p style="margin-top:3px">หลังคลาสรอบที่แล้ว คุณใช้ AI กับงานอะไรแล้ว<b>เวิร์ก</b> หรือ<b>พัง</b> — เรื่องพังมีค่าพอ ๆ กับเรื่องเวิร์ก
ผู้สอนจะสุ่มถาม 2 คนตอนเปิดคลาส</p></div>
</div>
</div>

<!-- ============ หน้า 2 ============ -->
<div class="p2"></div>
<div class="p2hd"><span>เตรียมตัวก่อนเข้าอบรม AI ช่วยงาน ภาค 2 — หน้า 2</span><span>เรื่องที่ควรรู้ก่อนมา</span></div>

<div class="card warn">
<h2 style="margin-bottom:5px"><span class="n" style="background:var(--r)">!</span> ห้ามเอามา — ข้อนี้ห้ามพลาด</h2>
<p><b>อย่าใส่ข้อมูลลับของบริษัทหรือข้อมูลลูกค้าจริงลงในบัญชีส่วนตัว</b> ทั้ง ChatGPT และ NotebookLM — เช่น รายชื่อลูกค้า ราคาทุน สัญญา ข้อมูลพนักงาน</p>
<p style="margin-top:4px" class="dim">ในคลาสเราเตรียมไฟล์ของบริษัทสมมติไว้ให้ครบแล้ว ส่วนตอนทำการบ้านด้วยงานจริง ให้เปลี่ยนชื่อและตัวเลขสำคัญก่อน หรือใช้บัญชีที่บริษัทอนุญาต</p>
</div>

<h2 style="margin-top:10px"><span class="n">?</span>คำถามที่ถามกันบ่อย</h2>
<div class="two">
<div class="card">
<div class="faq"><b>ต้องเสียเงินไหม</b> <span>ไม่ต้อง <b>NotebookLM และ ChatGPT บัญชีฟรีเรียนได้ทั้งคลาส</b> มีช่วงเดียวที่ผู้สอนเดโมให้ดู (โหมด Work) ไม่ต้องซื้อมาเรียน</span></div>
<div class="faq"><b>NotebookLM ต่างจาก ChatGPT ยังไง</b> <span>NotebookLM ตอบจาก<b>เอกสารที่คุณใส่เท่านั้น</b> และบอกที่มาทุกประโยค เหมาะกับงานที่ต้องอิงเอกสารจริง เช่น สรุปรายงานเป็นสไลด์</span></div>
<div class="faq"><b>ใช้มือถืออย่างเดียวได้ไหม</b> <span>ลำบากมาก ช่วงทำสไลด์และ Excel ต้องใช้จอใหญ่ <b>แนะนำให้เอาโน้ตบุ๊กมา</b></span></div>
</div>
<div class="card">
<div class="faq"><b>ไม่ได้ทำการบ้านรอบที่แล้ว มาได้ไหม</b> <span>ได้ คลาสนี้ทวนสูตรสั่งงานเดิมให้ก่อน 1 นาที แล้วต่อยอด ไม่มีใครถูกทิ้งไว้ข้างหลัง</span></div>
<div class="faq"><b>บัญชีบริษัทเข้า NotebookLM ไม่ได้</b> <span>ใช้ Gmail ส่วนตัวแทน — ไฟล์ในคลาสเป็นข้อมูลสมมติ ใส่บัญชีส่วนตัวได้</span></div>
<div class="faq"><b>มาสายได้ไหม</b> <span>พยายามอย่าสาย <b>30 นาทีแรกคือช่วงทำสไลด์ด้วย NotebookLM</b> ซึ่งเป็นไฮไลต์ของวัน พลาดแล้วตามยาก</span></div>
</div>
</div>

<div class="card" style="margin-top:2px;background:#f5f3ef">
<p style="text-align:center;font-size:12.4px">
<b>สรุปสั้น ๆ:</b> ลองเข้า notebooklm.google.com + สร้างสมุด 1 อัน · เช็ก chatgpt.com · เอาโน้ตบุ๊ก + หูฟังมา · โหลดไฟล์ตัวอย่างจากกลุ่มไลน์ · นึกไว้ 1 งานที่อยากทำสไลด์
<span class="tag">แค่นี้พอ</span></p>
</div>

<div class="ft">
<span>AI ช่วยงาน ภาค 2 · คู่มือเตรียมตัวก่อนอบรม</span>
<span>มีคำถามก่อนวันอบรม ถามได้ในกลุ่มไลน์ของคลาส</span>
</div>
</body>
</html>
"""
out = ROOT / "คู่มือเตรียมตัวก่อนอบรม.html"
out.write_text(page, encoding="utf-8")
html_to_pdf(out, ROOT / "คู่มือเตรียมตัวก่อนอบรม.pdf")
print("prep guide done")

"""โฟลเดอร์ใบเสร็จงานเลี้ยงปีใหม่พนักงาน (ใช้เดโม ChatGPT Work — ผู้สอนทำ)
8 ไฟล์ + งบที่อนุมัติ.xlsx
กับดักที่ตั้งใจใส่:
  - R07 คือใบเดียวกับ R02 ถ่ายซ้ำ (เลขที่เดียวกัน) → ถ้าไม่จับ ของรางวัลจะเกินงบ
  - R04 บิลเงินสดเขียนมือ ไม่มีเลขผู้เสียภาษี → บัญชีต้องทำใบรับรองแทนใบเสร็จ
  - หมวดตกแต่ง/ป้าย เกินงบจริง (2,800 + 2,680 = 5,480 > 5,000)
"""
import random
from PIL import Image, ImageFilter, ImageEnhance
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from common import *

OUTDIR = ASSETS / "W-ใบเสร็จงานเลี้ยงปีใหม่"
FONTS = (SRC / "fonts").resolve().as_uri()
rnd = random.Random(7)

BASE_CSS = f"""
@font-face{{font-family:'Itim';src:url('{FONTS}/Itim-Regular.ttf')}}
@font-face{{font-family:'Mali';src:url('{FONTS}/Mali-Regular.ttf')}}
@font-face{{font-family:'Sriracha';src:url('{FONTS}/Sriracha.ttf')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;color:#111;font-family:'Leelawadee UI',Tahoma,sans-serif}}
"""

BUYER = "บริษัท หอมกรุ่น ฟู้ดแอนด์กิฟท์ จำกัด (สำนักงานใหญ่)<br>ต.ยายชา อ.สามพราน จ.นครปฐม 73110<br>เลขประจำตัวผู้เสียภาษี 0735560009999"


def a4_invoice(fname, shop, shop_addr, taxid, title, no, date, rows, note, vat=True):
    sub = sum(q * p for _, q, p in rows)
    if vat:
        before = round(sub / 1.07, 2); v = round(sub - before, 2)
    trs = "".join(f"<tr><td>{i}</td><td>{d}</td><td class='r'>{q:,}</td><td class='r'>{p:,.2f}</td><td class='r'>{q * p:,.2f}</td></tr>"
                  for i, (d, q, p) in enumerate(rows, 1))
    tot = (f"<tr><td colspan=4 class='r'>มูลค่าก่อนภาษี</td><td class='r'>{before:,.2f}</td></tr>"
           f"<tr><td colspan=4 class='r'>ภาษีมูลค่าเพิ่ม 7%</td><td class='r'>{v:,.2f}</td></tr>") if vat else ""
    html = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{BASE_CSS}
@page{{size:A4;margin:0}} body{{width:210mm;padding:16mm 16mm;font-size:12.5px;line-height:1.55}}
.top{{display:flex;justify-content:space-between;border-bottom:2.5px solid #2c5f2d;padding-bottom:10px}}
.shop{{font-size:19px;font-weight:700;color:#2c5f2d}} .shop small{{display:block;font-size:11px;color:#555;font-weight:400}}
h1{{font-size:20px;text-align:right;color:#2c5f2d}} h1 small{{display:block;font-size:11px;color:#777;font-weight:400}}
.info{{display:grid;grid-template-columns:1.4fr 1fr;gap:16px;margin:14px 0}}
.info div{{background:#f3f7f2;padding:9px 12px;border-left:3px solid #2c5f2d;font-size:12px}}
table{{width:100%;border-collapse:collapse}} th{{background:#2c5f2d;color:#fff;padding:7px;text-align:left;font-size:12px}}
td{{padding:7px;border-bottom:1px solid #e1e6e0}} .r{{text-align:right}}
.grand td{{font-weight:700;font-size:15px;border-top:2px solid #2c5f2d;color:#2c5f2d}}
.note{{margin-top:16px;font-size:11.5px;color:#444;border:1px solid #dfe5de;padding:9px 12px}}
.sign{{margin-top:40px;display:flex;justify-content:space-between;font-size:11.5px;color:#555;text-align:center}}
.sign div{{width:200px;border-top:1px solid #999;padding-top:6px}}
</style></head><body>
<div class="top"><div class="shop">{shop}<small>{shop_addr}<br>เลขประจำตัวผู้เสียภาษี {taxid}</small></div>
<h1>{title}<small>เลขที่ {no}<br>วันที่ {date}</small></h1></div>
<div class="info"><div><b>ลูกค้า</b><br>{BUYER}</div><div><b>อ้างอิง</b><br>งานเลี้ยงปีใหม่พนักงาน<br>ศุกร์ 25 ธ.ค. 2569</div></div>
<table><tr><th>#</th><th>รายการ</th><th class='r'>จำนวน</th><th class='r'>ราคา/หน่วย</th><th class='r'>จำนวนเงิน</th></tr>{trs}
{tot}<tr class="grand"><td colspan=4 class='r'>รวมทั้งสิ้น</td><td class='r'>{sub:,.2f}</td></tr></table>
<div class="note">{note}</div>
<div class="sign"><div>ผู้รับเงิน</div><div>ผู้จ่ายเงิน</div></div>
</body></html>"""
    p = HTML / f"{fname}.html"; p.write_text(html, encoding="utf-8")
    return p


def thermal(fname, lines_html, width=380, height=900):
    html = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{BASE_CSS}
body{{background:#cfcac0;display:flex;justify-content:center;padding:30px 0}}
.slip{{width:{width - 60}px;background:#fbfaf6;padding:18px 16px 26px;font-family:'Courier New','Leelawadee UI',monospace;font-size:13px;
line-height:1.45;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.c{{text-align:center}} .b{{font-weight:700}} .row{{display:flex;justify-content:space-between}} hr{{border:0;border-top:1px dashed #777;margin:7px 0}}
.big{{font-size:17px}}
</style></head><body><div class="slip">{lines_html}</div></body></html>"""
    p = HTML / f"{fname}.html"; p.write_text(html, encoding="utf-8")
    return p


def handwritten(fname, shop, shop_sub, no, date, rows, total_words, font, has_tax=False):
    trs = "".join(f"<tr><td class='h'>{d}</td><td class='h c'>{q}</td><td class='h r'>{a:,}</td></tr>" for d, q, a in rows)
    trs += "<tr><td>&nbsp;</td><td></td><td></td></tr>" * (6 - len(rows))
    tot = sum(a for _, _, a in rows)
    html = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{BASE_CSS}
body{{background:#bdb6a8;display:flex;justify-content:center;padding:28px}}
.bill{{width:560px;background:#fffdf3;border:1px solid #9a8f7a;padding:18px 22px;color:#1d2a6b;font-size:14px;box-shadow:0 2px 10px rgba(0,0,0,.25)}}
.hd{{text-align:center;border-bottom:2px solid #1d2a6b;padding-bottom:8px;margin-bottom:8px}}
.hd b{{font-size:22px}} .hd small{{display:block;font-size:12px}}
.meta{{display:flex;justify-content:space-between;margin:6px 0 10px;font-size:13px}}
.h{{font-family:'{font}';color:#0d1b8c;font-size:19px}}
table{{width:100%;border-collapse:collapse}} th{{border:1px solid #1d2a6b;font-size:13px;padding:4px;background:#eef0fb}}
td{{border:1px solid #1d2a6b;padding:3px 8px;height:34px}} .r{{text-align:right}} .c{{text-align:center}}
.tot{{margin-top:8px;display:flex;justify-content:space-between;align-items:center}}
.stamp{{border:2px solid #b3261e;color:#b3261e;border-radius:6px;padding:4px 10px;transform:rotate(-8deg);font-weight:700;font-size:15px}}
.sig{{margin-top:14px;text-align:right;font-size:13px}}
</style></head><body><div class="bill">
<div class="hd"><b>{shop}</b><small>{shop_sub}</small><small style="font-size:15px;font-weight:700">บิลเงินสด / ใบเสร็จรับเงิน</small></div>
<div class="meta"><span>เลขที่ <span class="h">{no}</span></span><span>วันที่ <span class="h">{date}</span></span></div>
<div class="meta"><span>นาม <span class="h">บ.หอมกรุ่น (งานปีใหม่)</span></span></div>
<table><tr><th style="width:60%">รายการ</th><th>จำนวน</th><th>จำนวนเงิน</th></tr>{trs}
<tr><td class="r"><b>รวมเงิน</b></td><td></td><td class="h r">{tot:,}</td></tr></table>
<div class="tot"><span>ตัวอักษร <span class="h">({total_words})</span></span><span class="stamp">รับเงินแล้ว</span></div>
<div class="sig">ผู้รับเงิน <span class="h">สมใจ</span></div>
</div></body></html>"""
    p = HTML / f"{fname}.html"; p.write_text(html, encoding="utf-8")
    return p


def photo(png, jpg, angle, pad=36, shift=(0, 0), dark=1.0, blur=0.0):
    """ครอปเหลือเฉพาะกระดาษ + ขอบพื้นหลังนิดหน่อย แล้วหมุน/ปรับแสงให้เหมือนถ่ายด้วยมือถือ"""
    im = Image.open(png).convert("RGB")
    x0, y0, x1, y1 = Image.eval(im.convert("L"), lambda v: 255 if v > 238 else 0).getbbox()
    dx, dy = shift
    im = im.crop((max(0, x0 - pad + dx), max(0, y0 - pad + dy), min(im.width, x1 + pad + dx), min(im.height, y1 + pad + dy)))
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(120, 112, 100))
    im = ImageEnhance.Brightness(im).enhance(dark)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(jpg, quality=82)


tmp = SRC / "_tmp"; tmp.mkdir(exist_ok=True)

# R01 ร้านอาหาร มัดจำ (PDF ใบกำกับภาษี)
p = a4_invoice("r01", "ร้านอาหารเรือนไทยริมน้ำ", "88 ม.3 ต.ท่าตลาด อ.สามพราน จ.นครปฐม", "0735561004321",
               "ใบเสร็จรับเงิน/ใบกำกับภาษี", "RT-691120-07", "20 พฤศจิกายน 2569",
               [("มัดจำค่าอาหารโต๊ะจีน งานเลี้ยงปีใหม่ 9 โต๊ะ (50%)", 1, 30000)],
               "ยอดเต็ม 60,000 บาท (9 โต๊ะ โต๊ะละ 6,500 + ค่าห้อง 1,500) ส่วนที่เหลือ 30,000 บาท ชำระในวันงาน")
html_to_pdf(p, OUTDIR / "R01-ร้านอาหาร-มัดจำ.pdf")

# R02 ดีเดย์มาร์ท ของรางวัล (ใบกำกับภาษีอย่างย่อ)
items = [("ชุดเครื่องนอน 6 ฟุต", 2, 1890), ("กระติกน้ำร้อน 1.8L", 4, 790), ("กระเป๋าเดินทาง 24นิ้ว", 2, 1590),
         ("ชุดแก้วน้ำ 6 ใบ", 10, 259), ("ตุ๊กตาหมี 50ซม.", 4, 390), ("ไดร์เป่าผม 1600W", 2, 685), ("บัตรของขวัญ 500", 6, 500)]
tot = sum(q * p for _, q, p in items)
lines = ("<div class='c b big'>DDay Mart ดีเดย์มาร์ท</div><div class='c'>สาขาพุทธมณฑลสาย 4</div>"
         "<div class='c'>TAX ID 0105559012345 (สนญ.)</div><div class='c b'>ใบกำกับภาษีอย่างย่อ</div><hr>"
         "<div class='row'><span>เลขที่ ABB-2611-004187</span></div><div class='row'><span>22/11/2026 14:37</span><span>POS 07</span></div><hr>"
         + "".join(f"<div>{d}</div><div class='row'><span>&nbsp;&nbsp;{q} x {p:,.2f}</span><span>{q * p:,.2f}</span></div>" for d, q, p in items)
         + f"<hr><div class='row b big'><span>รวม {sum(q for _, q, _ in items)} ชิ้น</span><span>{tot:,.2f}</span></div>"
         f"<div class='row'><span>VAT 7% INCLUDED</span><span>{tot - tot / 1.07:,.2f}</span></div>"
         "<div class='row'><span>บัตรเครดิต ****4412</span><span></span></div><hr><div class='c'>ขอบคุณที่ใช้บริการ</div>")
assert tot == 18640, tot
p = thermal("r02", lines, 400, 1100)
html_to_png(p, tmp / "r02.png", 640, 1000)
photo(tmp / "r02.png", OUTDIR / "R02-ดีเดย์มาร์ท-ของรางวัล.jpg", -2.2)
# R07 = ใบเดียวกันถ่ายซ้ำ มุมต่าง แสงต่าง
photo(tmp / "r02.png", OUTDIR / "R07-ใบเสร็จของรางวัล-ถ่ายใหม่.jpg", 3.4, pad=22, shift=(10, -8), dark=0.9, blur=0.6)

# R03 ร้านเครื่องใช้ไฟฟ้า (A4 พิมพ์ → ถ่ายรูป)
p = a4_invoice("r03", "ห้างหุ้นส่วนจำกัด สามพรานอิเล็กทริค", "45/2 ถ.เพชรเกษม ต.อ้อมใหญ่ อ.สามพราน จ.นครปฐม", "0733550002468",
               "ใบเสร็จรับเงิน/ใบกำกับภาษี", "SE-2569/1187", "24 พฤศจิกายน 2569",
               [("หม้อทอดไร้น้ำมัน 5 ลิตร", 2, 2990), ("พัดลมตั้งพื้น 16 นิ้ว", 3, 1290), ("เครื่องปั่นน้ำผลไม้", 2, 1595)],
               "ของรางวัลจับฉลากงานปีใหม่ · รับประกันสินค้า 1 ปี")
html_to_png(p, tmp / "r03.png", 794, 1123)
photo(tmp / "r03.png", OUTDIR / "R03-ร้านเครื่องใช้ไฟฟ้า-ของรางวัล.jpg", 1.6, dark=0.96)

# R04 ร้านป้ายไวนิล บิลเงินสดเขียนมือ ไม่มีเลขผู้เสียภาษี
p = handwritten("r04", "ร้านเจริญป้ายไวนิล", "ตลาดสามพราน โทร 08x-xxx-xxxx", "054", "26/11/69",
                [("ป้ายไวนิล 1.2x3 ม. งานปีใหม่", "1", 1800), ("แบ็กดรอปถ่ายรูป", "1", 1000)],
                "สองพันแปดร้อยบาทถ้วน", "Itim")
html_to_png(p, tmp / "r04.png", 620, 640)
photo(tmp / "r04.png", OUTDIR / "R04-ร้านป้ายไวนิล-บิลเงินสด.jpg", -3.0, dark=0.93)

# R05 เครื่องเสียง มัดจำ (เขียนมือ มีเลขผู้เสียภาษี)
p = handwritten("r05", "เอกซาวด์ แอนด์ ไลท์", "รับจัดเครื่องเสียง เวที ไฟ · เลขผู้เสียภาษี 3739900123456",
                "0217", "27/11/69", [("มัดจำเครื่องเสียง+ไฟ+พิธีกร งานวันที่ 25 ธ.ค.", "1 งาน", 6000)],
                "หกพันบาทถ้วน", "Mali")
html_to_png(p, tmp / "r05.png", 620, 640)
photo(tmp / "r05.png", OUTDIR / "R05-เครื่องเสียง-มัดจำ.jpg", 2.1)

# R06 ร้านเครื่องเขียน/ของตกแต่ง (thermal)
items6 = [("ลูกโป่งฟอยล์ 2570", 2, 290), ("ลูกโป่งยาง ถุง100", 4, 150), ("ธงราวกระดาษทอง", 6, 85),
          ("กระดาษห่อของขวัญ", 10, 35), ("ริบบิ้นทอง ม้วนใหญ่", 3, 120), ("เทปกาวสองหน้า", 7, 40)]
t6 = sum(q * p for _, q, p in items6)
assert t6 == 2680, t6
lines6 = ("<div class='c b big'>ร้านศรีสุขเครื่องเขียน</div><div class='c'>อ.สามพราน นครปฐม</div>"
          "<div class='c'>เลขผู้เสียภาษี 0735558011223</div><div class='c b'>ใบเสร็จรับเงิน</div><hr>"
          "<div class='row'><span>No. 6911-0388</span><span>28/11/69</span></div><hr>"
          + "".join(f"<div>{d}</div><div class='row'><span>&nbsp;&nbsp;{q} x {p:,}</span><span>{q * p:,}.00</span></div>" for d, q, p in items6)
          + f"<hr><div class='row b big'><span>รวม</span><span>{t6:,}.00</span></div><div class='row'><span>เงินสด</span><span>3,000.00</span></div>"
          f"<div class='row'><span>ทอน</span><span>{3000 - t6:,}.00</span></div><hr><div class='c'>ขอบคุณค่ะ</div>")
p = thermal("r06", lines6, 400, 900)
html_to_png(p, tmp / "r06.png", 640, 820)
photo(tmp / "r06.png", OUTDIR / "R06-ร้านเครื่องเขียน-ของตกแต่ง.jpg", 1.2)

# R08 ค่ารถตู้ มัดจำ (PDF ไม่มี VAT)
p = a4_invoice("r08", "สามพรานทัวร์ รถตู้เช่า", "12/4 ม.5 ต.บางกระทึก อ.สามพราน จ.นครปฐม", "3730100778899",
               "ใบเสร็จรับเงิน", "VAN-2569-142", "1 ธันวาคม 2569",
               [("มัดจำรถตู้ 2 คัน รับ-ส่งพนักงาน วันที่ 25 ธ.ค. 2569 (คันละ 3,500 / มัดจำ 50%)", 1, 3500)],
               "ยอดเต็ม 7,000 บาท ส่วนที่เหลือ 3,500 บาท ชำระวันเดินทาง · ผู้ประกอบการไม่ได้จดทะเบียนภาษีมูลค่าเพิ่ม", vat=False)
html_to_pdf(p, OUTDIR / "R08-รถตู้-มัดจำ.pdf")

# งบที่อนุมัติ
wb = Workbook(); ws = wb.active; ws.title = "งบงานเลี้ยงปีใหม่"
ws.append(["งบงานเลี้ยงปีใหม่พนักงาน 2570 (อนุมัติโดยคุณกมลวรรณ 18 พ.ย. 2569)"]); ws["A1"].font = Font(bold=True, size=13)
ws.append(["วันงาน: ศุกร์ 25 ธ.ค. 2569 · ผู้เข้าร่วม 90 คน (พนักงานประจำ 82 + ชั่วคราว 8)"])
ws.append([])
ws.append(["หมวด", "งบที่อนุมัติ (บาท)", "หมายเหตุ"])
for c in ws[4]:
    c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="F2E6D0")
for r in [("อาหารและสถานที่", 60000, "ร้านอาหารเรือนไทยริมน้ำ 9 โต๊ะ"), ("ของรางวัลจับฉลาก", 35000, ""),
          ("เครื่องเสียง เวที พิธีกร", 12000, ""), ("ของตกแต่งและป้าย", 5000, ""), ("การเดินทาง", 8000, "รถตู้รับ-ส่ง")]:
    ws.append(list(r))
ws.append(["รวม", "=SUM(B5:B9)", ""])
ws["A10"].font = Font(bold=True); ws["B10"].font = Font(bold=True)
for row in ws.iter_rows(min_row=5, max_row=10, min_col=2, max_col=2):
    for c in row: c.number_format = "#,##0"
ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 20; ws.column_dimensions["C"].width = 34
wb.save(OUTDIR / "งบงานเลี้ยงปีใหม่-ที่อนุมัติ.xlsx")
print("receipts done:", sorted(x.name for x in OUTDIR.iterdir()))

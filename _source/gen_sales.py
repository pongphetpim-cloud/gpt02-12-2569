"""สร้างไฟล์ยอดขาย ม.ค.–พ.ย. 2569 ของ บจก. หอมกรุ่น ฟู้ดแอนด์กิฟท์ (บริษัทสมมติ)

ผลลัพธ์
  _source/sales_clean.csv          ข้อมูลสะอาด (ใช้คำนวณตัวเลขในรายงาน NB1)
  _source/sales_stats.json         ตัวเลขสรุปที่รายงาน/สไลด์ต้องใช้
  _source/uc2_answer_key.json      เฉลยความสกปรกที่ใส่ไว้ (ให้ผู้สอนใช้)
  assets/UC2-ยอดขาย-มค-พย-2569.xlsx   ไฟล์สกปรกโดยตั้งใจ แจกผู้เรียน

รันซ้ำได้ ผลเหมือนเดิมทุกครั้ง (fixed seed)
"""
import csv, json, random, datetime as dt
from collections import defaultdict
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source"
OUT = ROOT / "assets"
rnd = random.Random(2569)

# ---------------- สินค้า ----------------
PRODUCTS = {
    "ขนมไทยอบกรอบ": [("ทองม้วนกรอบ 250 ก.", 85), ("ถั่วตัดงาดำ 200 ก.", 65),
                    ("กล้วยอบเนย 180 ก.", 59), ("ข้าวตังหน้าธัญพืช 150 ก.", 75)],
    "คุกกี้และเบเกอรี่": [("คุกกี้เนยสด กล่องเหล็ก 400 ก.", 189), ("พายสับปะรด 12 ชิ้น", 120)],
    "ชาและกาแฟ": [("ชาเขียวมะลิ 20 ซอง", 79), ("กาแฟดริป 10 ซอง", 149)],
    "กระเช้าและของขวัญ": [("กระเช้าสุขสันต์", 690), ("กระเช้ามั่งมี", 1290),
                         ("กระเช้ามหามงคล", 2490), ("กล่องของขวัญองค์กร", 450)],
}
PRICE = {name: p for g in PRODUCTS.values() for name, p in g}
GROUP = {name: g for g, items in PRODUCTS.items() for name, _ in items}

# ---------------- ลูกค้า ----------------
CH_TRAD, CH_MT, CH_CORP, CH_ONL = "ร้านค้าส่ง/ของฝาก", "โมเดิร์นเทรด", "องค์กร", "ออนไลน์"
CUSTOMERS = {
    CH_TRAD: [("ร้านบ้านขนมอัมพวา", 1.3), ("หจก.ทองสุขค้าส่ง", 1.6), ("ร้านของฝากเมืองเพชร", 1.0),
              ("ร้านศรีนวลของฝาก", 1.1), ("ร้านป้าแดงของฝากกาญจน์", 0.8), ("ร้านเจ๊หมวยดอนหวาย", 0.9),
              ("ร้านสายใจของฝากหัวหิน", 0.9), ("หจก.เพชรเกษมค้าส่ง", 1.2)],
    CH_MT: [("ดีเดย์มาร์ท", 1.6), ("สุขสวัสดิ์ซูเปอร์", 1.0)],
    CH_CORP: [("บจก.เจริญวัฒนาออโต้พาร์ท", 1.8), ("บมจ.รุ่งอรุณประกันชีวิต", 1.5),
              ("โรงพยาบาลสามพรานเวชการ", 0.9), ("บจก.สยามโพลีแพ็ค", 1.0),
              ("บจก.นครชัยโลจิสติกส์", 0.8), ("บจก.ไทยเฟิร์สอีเลคทรอนิกส์", 1.2),
              ("บมจ.ศรีเมืองพร็อพเพอร์ตี้", 1.0), ("สำนักงานบัญชีกิจเจริญ", 0.4)],
    CH_ONL: [("ลูกค้าออนไลน์ (LINE OA/Shopee)", 1.0)],
}
SELLER = {CH_TRAD: ["นุชจรี", "ธีรวัฒน์"], CH_MT: ["ปิยะพงษ์"],
          CH_CORP: ["ปิยะพงษ์", "แพรวา"], CH_ONL: ["ทีมออนไลน์"]}

# ฤดูกาลรายเดือน (ม.ค.–พ.ย.) และยอดฐานต่อเดือน (บาท) ต่อช่องทาง
SEASON = {
    CH_TRAD: [1.15, 1.30, 0.95, 1.25, 0.90, 0.80, 0.60, 0.90, 0.95, 1.05, 1.10],
    CH_MT:   [1.10, 1.20, 1.00, 1.05, 0.85, 0.80, 0.58, 0.78, 0.80, 0.85, 0.95],
    CH_CORP: [0.60, 0.90, 0.20, 0.30, 0.15, 0.15, 0.12, 0.30, 0.50, 2.50, 5.00],
    CH_ONL:  [0.70, 0.80, 0.85, 0.90, 0.95, 1.00, 0.70, 1.15, 1.25, 1.40, 1.60],
}
BASE = {CH_TRAD: 1_550_000, CH_MT: 1_250_000, CH_CORP: 1_000_000, CH_ONL: 220_000}


def pick_line(ch, month):
    """คืน (สินค้า, จำนวน) หนึ่งบรรทัด"""
    if ch == CH_TRAD:
        g = rnd.choices(["ขนมไทยอบกรอบ", "คุกกี้และเบเกอรี่", "ชาและกาแฟ"], [6, 3, 1.5])[0]
        name = rnd.choice(PRODUCTS[g])[0]
        qty = rnd.randrange(80, 420, 10)
    elif ch == CH_MT:
        pool = [n for g in ["ขนมไทยอบกรอบ", "คุกกี้และเบเกอรี่", "ชาและกาแฟ"] for n, _ in PRODUCTS[g]]
        if month in (10, 11):
            pool += ["กระเช้าสุขสันต์"] * 2
        name = rnd.choice(pool)
        qty = rnd.randrange(240, 1300, 24) if GROUP[name] != "กระเช้าและของขวัญ" else rnd.randrange(40, 160, 10)
    elif ch == CH_CORP:
        if month in (1, 2):
            name = rnd.choice(["คุกกี้เนยสด กล่องเหล็ก 400 ก.", "กล่องของขวัญองค์กร", "กระเช้าสุขสันต์"])
        elif month in (10, 11):
            name = rnd.choices(["กระเช้าสุขสันต์", "กระเช้ามั่งมี", "กระเช้ามหามงคล", "กล่องของขวัญองค์กร"],
                               [3, 4, 1.5, 2])[0]
        else:
            name = rnd.choice(["กล่องของขวัญองค์กร", "คุกกี้เนยสด กล่องเหล็ก 400 ก.", "พายสับปะรด 12 ชิ้น"])
        if GROUP[name] == "กระเช้าและของขวัญ":
            qty = rnd.randrange(30, 260, 10) if name != "กระเช้ามหามงคล" else rnd.randrange(10, 60, 5)
        else:
            qty = rnd.randrange(50, 300, 10)
    else:  # ออนไลน์ = ยอดรวมรายสัปดาห์ต่อสินค้า
        pool = [n for g in ["ขนมไทยอบกรอบ", "คุกกี้และเบเกอรี่", "ชาและกาแฟ"] for n, _ in PRODUCTS[g]]
        if month == 11:
            pool += ["กระเช้าสุขสันต์", "กระเช้ามั่งมี"]
        name = rnd.choice(pool)
        qty = rnd.randrange(12, 130) if GROUP[name] != "กระเช้าและของขวัญ" else rnd.randrange(4, 25)
    return name, qty


def workdays(year, month):
    d = dt.date(year, month, 1)
    out = []
    while d.month == month:
        if d.weekday() < 6:  # จันทร์–เสาร์
            out.append(d)
        d += dt.timedelta(days=1)
    return out


rows = []  # dict ต่อบรรทัด (สะอาด)
bill_no = defaultdict(int)
for m in range(1, 12):
    days = workdays(2026, m)
    if m == 7:  # เครื่องอบเสีย 8–16 ก.ค. ส่งของน้อยมาก
        days = [d for d in days if not (8 <= d.day <= 16)] + [d for d in days if 8 <= d.day <= 16][:2]
    for ch, base in BASE.items():
        target = base * SEASON[ch][m - 1]
        total = 0
        names = [c for c, _ in CUSTOMERS[ch]]
        weights = [w for _, w in CUSTOMERS[ch]]
        while total < target:
            cust = rnd.choices(names, weights)[0]
            day = rnd.choice(days)
            bill_no[m] += 1
            bill = f"INV-69{m:02d}-{bill_no[m]:04d}"
            nlines = rnd.choices([1, 2, 3, 4], [3, 3, 2, 1])[0] if ch != CH_ONL else 1
            seller = rnd.choice(SELLER[ch])
            used = set()
            for _ in range(nlines):
                name, qty = pick_line(ch, m)
                if name in used:
                    continue
                used.add(name)
                amt = qty * PRICE[name]
                rows.append(dict(date=day, bill=bill, cust=cust, ch=ch, group=GROUP[name], item=name,
                                 qty=qty, price=PRICE[name], amt=amt, seller=seller))
                total += amt

# รายการรับคืน (ถูกต้อง ไม่ใช่ข้อผิดพลาด) 9 รายการ
RETURNS = [(2, "ดีเดย์มาร์ท", "พายสับปะรด 12 ชิ้น", 96), (3, "หจก.ทองสุขค้าส่ง", "กล้วยอบเนย 180 ก.", 60),
           (5, "สุขสวัสดิ์ซูเปอร์", "ทองม้วนกรอบ 250 ก.", 72), (6, "ร้านบ้านขนมอัมพวา", "ถั่วตัดงาดำ 200 ก.", 40),
           (7, "ดีเดย์มาร์ท", "คุกกี้เนยสด กล่องเหล็ก 400 ก.", 48), (8, "ร้านศรีนวลของฝาก", "ข้าวตังหน้าธัญพืช 150 ก.", 30),
           (9, "ดีเดย์มาร์ท", "กาแฟดริป 10 ซอง", 120), (11, "บจก.เจริญวัฒนาออโต้พาร์ท", "กระเช้ามั่งมี", 11),
           (11, "สุขสวัสดิ์ซูเปอร์", "กระเช้าสุขสันต์", 12)]
for i, (m, cust, name, q) in enumerate(RETURNS, 1):
    ch = next(c for c, lst in CUSTOMERS.items() if cust in [x for x, _ in lst])
    day = rnd.choice(workdays(2026, m))
    if m == 11 and cust == "บจก.เจริญวัฒนาออโต้พาร์ท":
        day = dt.date(2026, 11, 28)  # ตรงกับเรื่องร้องเรียน UC3 (ส่ง 27 พ.ย. เสียหาย 11 ใบ)
    rows.append(dict(date=day, bill=f"CN-69{m:02d}-{i:03d}", cust=cust, ch=ch, group=GROUP[name], item=name,
                     qty=-q, price=PRICE[name], amt=-q * PRICE[name], seller=rnd.choice(SELLER[ch])))

# ออเดอร์ใหญ่ของเจริญวัฒนา 27 พ.ย. (ใช้ใน UC3) — 200 ใบ กระเช้ามั่งมี
rows.append(dict(date=dt.date(2026, 11, 27), bill="INV-6911-9001", cust="บจก.เจริญวัฒนาออโต้พาร์ท", ch=CH_CORP,
                 group="กระเช้าและของขวัญ", item="กระเช้ามั่งมี", qty=200, price=1290, amt=258000, seller="แพรวา"))

rows.sort(key=lambda r: (r["date"], r["bill"]))

# เลือกแถวที่จะจงใจพิมพ์จำนวนผิดในไฟล์สกปรก — ในข้อมูลสะอาดกำหนดให้เป็น 120 ใบ
_cand = [r for r in rows if r["date"].month == 10 and r["item"] == "กระเช้ามั่งมี" and r["ch"] == CH_CORP]
TYPO = _cand[len(_cand) // 2]
TYPO["qty"] = 120; TYPO["amt"] = 120 * TYPO["price"]

# ---------------- ตัวเลขสรุปจากข้อมูลสะอาด ----------------
TH_M = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย."]
by_month = defaultdict(int); by_q_ch = defaultdict(int); by_cust = defaultdict(int)
by_group = defaultdict(int); by_ch = defaultdict(int); by_m_ch = defaultdict(int)
for r in rows:
    m = r["date"].month
    by_month[m] += r["amt"]; by_ch[r["ch"]] += r["amt"]; by_m_ch[(m, r["ch"])] += r["amt"]
    by_q_ch[((m - 1) // 3 + 1, r["ch"])] += r["amt"]; by_cust[r["cust"]] += r["amt"]
    by_group[r["group"]] += r["amt"]
total = sum(by_month.values())
stats = {
    "rows_clean": len(rows),
    "total_jan_nov": total,
    "by_month": {TH_M[m - 1]: by_month[m] for m in range(1, 12)},
    "by_channel": dict(by_ch),
    "by_quarter_channel": {f"Q{q}": {ch: by_q_ch[(q, ch)] for ch in BASE} for q in range(1, 5)},
    "by_month_channel": {TH_M[m - 1]: {ch: by_m_ch[(m, ch)] for ch in BASE} for m in range(1, 12)},
    "by_group": dict(by_group),
    "top_customers": sorted(by_cust.items(), key=lambda x: -x[1])[:8],
}

# ---------------- ทำให้สกปรกโดยตั้งใจ ----------------
dirty = [dict(r) for r in rows]
key = {"duplicates": [], "qty_typo": None, "amount_mismatch": [], "blank_rows": [], "returns": len(RETURNS),
       "name_variants": {}, "channel_variants": {}, "excel_dates": 0}

# 1) จำนวนพิมพ์เกิน 1 ศูนย์: กระเช้ามั่งมี ต.ค. 120 → 1200
t = next(r for r in dirty if r["bill"] == TYPO["bill"] and r["item"] == TYPO["item"])
right_amt = t["amt"]
t["qty"] = 1200; t["amt"] = 1200 * t["price"]
key["qty_typo"] = {"bill": t["bill"], "cust": t["cust"], "item": t["item"], "qty_in_file": 1200,
                   "qty_correct": 120, "overstated_by": t["amt"] - right_amt}

# 2) ยอดรวมพิมพ์ผิด 6 แถว
for r in rnd.sample([r for r in dirty if r["amt"] > 5000 and r is not t], 6):
    s = str(r["amt"]); i = rnd.randrange(len(s) - 1)
    wrong = int(s[:i] + s[i + 1] + s[i] + s[i + 2:]) if s[i] != s[i + 1] else r["amt"] + 1000
    key["amount_mismatch"].append({"bill": r["bill"], "item": r["item"], "qty": r["qty"], "price": r["price"],
                                   "amount_in_file": wrong, "amount_correct": r["amt"]})
    r["amt"] = wrong

# 3) ชื่อลูกค้า/ช่องทางเขียนไม่ตรงกัน
NAME_VAR = {"ดีเดย์มาร์ท": ["ดีเดย์ มาร์ท", "DDay Mart", "บจก.ดีเดย์มาร์ท"],
            "บจก.เจริญวัฒนาออโต้พาร์ท": ["เจริญวัฒนา ออโต้พาร์ท", "บริษัท เจริญวัฒนาออโต้พาร์ท จำกัด"],
            "ร้านบ้านขนมอัมพวา": ["บ้านขนม อัมพวา"], "หจก.ทองสุขค้าส่ง": ["ทองสุขค้าส่ง", "ทองสุข ค้าส่ง"],
            "บมจ.รุ่งอรุณประกันชีวิต": ["รุ่งอรุณประกันชีวิต"]}
CH_VAR = {CH_MT: ["Modern Trade", "MT"], CH_TRAD: ["ค้าส่ง", "ร้านของฝาก"], CH_CORP: ["Corporate"],
          CH_ONL: ["Online"]}
for r in dirty:
    if r["cust"] in NAME_VAR and rnd.random() < 0.18:
        v = rnd.choice(NAME_VAR[r["cust"]]); key["name_variants"].setdefault(r["cust"], set()).add(v); r["cust"] = v
    if rnd.random() < 0.07:
        v = rnd.choice(CH_VAR[r["ch"]]); key["channel_variants"].setdefault(r["ch"], set()).add(v); r["ch"] = v

# 4) แถวซ้ำ 14 แถว (ส่วนใหญ่ ส.ค.–พ.ย. ช่วงคนรับออเดอร์เยอะ)
pool = [i for i, r in enumerate(dirty) if r["date"].month >= 8 and r["amt"] > 0]
dup_idx = sorted(rnd.sample(pool, 11) + rnd.sample([i for i, r in enumerate(dirty) if r["date"].month < 8], 3))
for i in reversed(dup_idx):
    dirty.insert(i + 1, dict(dirty[i]))
    key["duplicates"].append({"bill": dirty[i]["bill"], "item": dirty[i]["item"], "amount": dirty[i]["amt"],
                              "month": TH_M[dirty[i]["date"].month - 1]})

# 5) แถวว่าง 3 แถว
for pos in sorted(rnd.sample(range(50, len(dirty) - 50), 3), reverse=True):
    dirty.insert(pos, None); key["blank_rows"].append(pos + 2)

# ---------------- เขียน Excel ----------------
wb = Workbook(); ws = wb.active; ws.title = "ยอดขาย"
head = ["วันที่", "เลขที่บิล", "ลูกค้า", "ช่องทาง", "กลุ่มสินค้า", "สินค้า", "จำนวน", "ราคา/หน่วย", "ยอดรวม", "พนักงานขาย"]
ws.append(head)
for c in ws[1]:
    c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="F2E6D0")
excel_dates = 0
for r in dirty:
    if r is None:
        ws.append([]); continue
    d = r["date"]
    if rnd.random() < 0.15:
        dval = d; excel_dates += 1  # วันที่จริงของ Excel (ค.ศ.)
    else:
        dval = f"{d.day:02d}/{d.month:02d}/{d.year + 543}"  # ข้อความ พ.ศ.
    ws.append([dval, r["bill"], r["cust"], r["ch"], r["group"], r["item"], r["qty"], r["price"], r["amt"], r["seller"]])
    if isinstance(dval, dt.date):
        ws.cell(ws.max_row, 1).number_format = "yyyy-mm-dd"
key["excel_dates"] = excel_dates
for col, w in zip("ABCDEFGHIJ", [12, 15, 32, 18, 18, 30, 9, 11, 12, 12]):
    ws.column_dimensions[col].width = w
for row in ws.iter_rows(min_row=2, min_col=7, max_col=9):
    for c in row:
        c.number_format = "#,##0"
ws.freeze_panes = "A2"
wb.save(OUT / "UC2-ยอดขาย-มค-พย-2569.xlsx")

# ---------------- สถิติของไฟล์สกปรก (เผื่อ AI ไม่ล้าง) ----------------
dsum = defaultdict(int)
for r in dirty:
    if r: dsum[r["date"].month] += r["amt"]
stats["dirty_by_month"] = {TH_M[m - 1]: dsum[m] for m in range(1, 12)}
stats["dirty_total"] = sum(dsum.values())
stats["rows_dirty"] = sum(1 for r in dirty if r)

with open(SRC / "sales_clean.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(head)
    for r in rows:
        w.writerow([r["date"].isoformat(), r["bill"], r["cust"], r["ch"], r["group"], r["item"],
                    r["qty"], r["price"], r["amt"], r["seller"]])
json.dump(stats, open(SRC / "sales_stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
key = {k: ({kk: sorted(vv) for kk, vv in v.items()} if isinstance(v, dict) and k.endswith("variants") else v)
       for k, v in key.items()}
json.dump(key, open(SRC / "uc2_answer_key.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("clean rows", len(rows), "dirty rows", stats["rows_dirty"], "excel-dates", excel_dates)
print("total clean", f"{total:,}", "dirty", f"{stats['dirty_total']:,}")
for m in range(1, 12):
    print(TH_M[m - 1], f"{by_month[m]:>12,}", f"{dsum[m]:>12,}")
print({k: f"{v:,}" for k, v in by_ch.items()})

"""ของใช้ร่วมของสคริปต์สร้างไฟล์"""
import json, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source"
HTML = SRC / "html"
ASSETS = ROOT / "assets"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def stats():
    return json.load(open(SRC / "sales_stats.json", encoding="utf-8"))


def m(x, d=2):
    """บาท → 'ล้านบาท' ทศนิยม d ตำแหน่ง"""
    return f"{x / 1_000_000:,.{d}f}"


def baht(x):
    return f"{x:,.0f}"


def write_text(path, text):
    """ไฟล์ข้อความทุกไฟล์ต้องมี UTF-8 BOM (ไม่งั้นภาษาไทยเพี้ยนตอนเปิดผ่าน Notion/เบราว์เซอร์)"""
    Path(path).write_text(text.lstrip("\n"), encoding="utf-8-sig", newline="\r\n")


def html_to_pdf(html_path, pdf_path):
    """เรนเดอร์ HTML เป็น PDF ด้วย headless Chrome — ทำงานผ่านโฟลเดอร์ชั่วคราวชื่อ ASCII
    เพราะ file:// กับพาธภาษาไทยพัง"""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.pdf"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", Path(html_path).resolve().as_uri()],
                       check=True, capture_output=True, timeout=120)
        shutil.copyfile(out, pdf_path)


def html_to_png(html_path, png_path, w, h):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={w},{h}", f"--screenshot={out}", Path(html_path).resolve().as_uri()],
                       check=True, capture_output=True, timeout=120)
        shutil.copyfile(out, png_path)

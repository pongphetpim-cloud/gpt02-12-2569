"""ตรวจสไลด์: หาสไลด์ที่เนื้อหาล้น + ทำภาพรวม (contact sheet) ไว้ดูด้วยตา
ใช้: python check_slides.py [--sheets]
"""
import re, subprocess, sys, tempfile, shutil
from pathlib import Path
from common import ROOT, CHROME

src = (ROOT / "slides.html").read_text(encoding="utf-8")
probe = r"""
<script>
window.addEventListener('load', function(){ setTimeout(function(){
  var out = [];
  var all = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  all.forEach(function(s, i){
    all.forEach(function(x){ x.classList.remove('on'); });
    s.classList.add('on');
    var sb = s.getBoundingClientRect();
    var issues = [];
    s.querySelectorAll('pre,.box,.steps,.tbl-wrap,.watch,.files,.mp,.dlg,.check3 > div,.hw div,.six div,.ti').forEach(function(e){
      if (e.scrollHeight > e.clientHeight + 3) issues.push((e.className||e.tagName) + ' scroll ' + (e.scrollHeight - e.clientHeight));
    });
    s.querySelectorAll('*').forEach(function(e){
      var r = e.getBoundingClientRect();
      if (r.height && (r.bottom > sb.bottom + 1 || r.right > sb.right + 1)) issues.push('out ' + (e.className||e.tagName));
    });
    if (issues.length) out.push((i+1) + ' [' + (s.dataset.mode) + '] ' + (s.querySelector('h1,h2')||{textContent:''}).textContent.slice(0,40) + ' :: ' + issues.slice(0,4).join(' | '));
  });
  var p = document.createElement('pre'); p.id = 'probe-out'; p.textContent = out.join('\n') || 'OK';
  document.body.appendChild(p);
}, 1500); });
</script>
"""
# บังคับ stage ไม่ scale + โชว์สไลด์ทั้งหมด (รวมโหมดบ่าย)
test = src.replace("</body>", probe + "</body>").replace("var pm = false;", "var pm = true;")
td = Path(tempfile.mkdtemp())
(td / "t.html").write_text(test, encoding="utf-8")
r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1280,720", "--virtual-time-budget=6000",
                    "--dump-dom", (td / "t.html").as_uri()], capture_output=True, timeout=120)
dom = r.stdout.decode("utf-8", "replace")
m = re.search(r'<pre id="probe-out">(.*?)</pre>', dom, re.S)
print(m.group(1).replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&") if m else "probe failed")

if "--sheets" in sys.argv:
    from PIL import Image
    n = src.count('<section class="slide')
    shots = td / "shots"; shots.mkdir()
    test2 = src.replace("var pm = false;", "var pm = true;")
    (td / "s.html").write_text(test2, encoding="utf-8")
    for i in range(1, n + 1):
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                        "--virtual-time-budget=3000", f"--screenshot={shots / f'{i:02d}.png'}",
                        (td / "s.html").as_uri() + f"#{i}"], capture_output=True, timeout=60)
    out = Path(sys.argv[sys.argv.index("--sheets") + 1]) if len(sys.argv) > sys.argv.index("--sheets") + 1 else td
    per = 6
    for k in range(0, n, per):
        sheet = Image.new("RGB", (2 * 800, 3 * 450), "white")
        for j in range(per):
            f = shots / f"{k + j + 1:02d}.png"
            if not f.exists(): continue
            im = Image.open(f).resize((800, 450))
            sheet.paste(im, ((j % 2) * 800, (j // 2) * 450))
        sheet.save(out / f"sheet_{k // per + 1:02d}.png")
    print("sheets saved to", out)
shutil.rmtree(td, ignore_errors=True) if "--sheets" not in sys.argv else None

(function(){
  var stage = document.getElementById('stage');
  var all   = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var bar   = document.getElementById('bar');
  var hpos  = document.getElementById('hpos');
  var hmode = document.getElementById('hmode');
  var hclock= document.getElementById('hclock');
  var notes = document.getElementById('notes');
  var ntext = document.getElementById('ntext');
  var help  = document.getElementById('help');
  var ovw   = document.getElementById('ovw');

  var pm = false;         // false = เช้า 3 ชม. / true = บ่าย 4 ชม.
  var deck = [], i = 0;
  var tick = null, left = 0, paused = false;

  function build(keep){
    var cur = deck[i];
    deck = all.filter(function(s){ return pm || s.dataset.mode !== 'pm'; });
    all.forEach(function(s){ s.classList.toggle('hidepm', !pm && s.dataset.mode==='pm'); });
    var idx = keep ? deck.indexOf(cur) : 0;
    i = idx < 0 ? 0 : idx;
    hmode.textContent = pm ? 'บ่าย 4 ชม.' : 'เช้า 3 ชม.';
    buildOverview();
    show();
  }

  function show(){
    all.forEach(function(s){ s.classList.remove('on'); });
    var s = deck[i]; if(!s) return;
    s.classList.add('on');
    grow(s);
    hpos.textContent = (i+1) + ' / ' + deck.length;
    bar.style.width = ((i+1)/deck.length*100) + '%';
    ntext.textContent = s.dataset.notes || 'ไม่มีโน้ตสำหรับสไลด์นี้';
    Array.prototype.forEach.call(ovw.children, function(c,n){ c.classList.toggle('cur', n===i); });
    startTimer(s);
  }

  /* ---------- ขยายตัวอักษรในกล่อง prompt ให้เต็มที่ว่าง (ไม่เกิน 24px) ---------- */
  function grow(s){
    s.querySelectorAll('pre:not(.gp)').forEach(function(p){
      if (p.closest('.watch') || p.closest('.e4')) return;
      if (!p.dataset.base) p.dataset.base = parseFloat(getComputedStyle(p).fontSize);
      var base = +p.dataset.base, lo = base, hi = Math.max(base, 24);
      p.style.fontSize = base + 'px';
      if (p.scrollHeight > p.clientHeight + 1) return;
      for (var k = 0; k < 7; k++){
        var mid = (lo + hi) / 2;
        p.style.fontSize = mid + 'px';
        if (p.scrollHeight > p.clientHeight + 1) hi = mid; else lo = mid;
      }
      p.style.fontSize = Math.floor(lo * 2) / 2 + 'px';
    });
  }

  /* ---------- ตัวจับเวลา ---------- */
  function fmt(sec){
    if(sec<0) sec = -sec;
    var m = Math.floor(sec/60), s = sec%60;
    return m + ':' + (s<10?'0':'') + s;
  }
  function faces(){
    var s = deck[i]; if(!s) return [];
    return Array.prototype.slice.call(s.querySelectorAll('.timer .t, [data-clock]'));
  }
  function startTimer(s){
    if(tick){ clearInterval(tick); tick = null; }
    var min = parseFloat(s.dataset.min || '0');
    var el  = s.querySelector('.timer');
    if(el) el.classList.remove('over','paused');
    if(!min){ hclock.textContent = '--:--'; return; }
    left = Math.round(min*60); paused = false;
    render();
    tick = setInterval(function(){
      if(paused) return;
      left--; render();
    }, 1000);
  }
  function render(){
    var txt = (left<0 ? '+' : '') + fmt(left);
    faces().forEach(function(f){ f.textContent = txt; });
    hclock.textContent = txt;
    var el = deck[i] && deck[i].querySelector('.timer');
    if(el){ el.classList.toggle('over', left<0); el.classList.toggle('paused', paused); }
  }

  /* ---------- ภาพรวมสไลด์ ---------- */
  function buildOverview(){
    ovw.innerHTML = '';
    deck.forEach(function(s,n){
      var d = document.createElement('div');
      d.className = 'ov';
      var lbl = s.querySelector('.chip'), h = s.querySelector('h1,h2');
      d.innerHTML = '<small>' + (n+1) + (lbl ? ' · ' + lbl.textContent : '') + '</small>' +
                    (h ? h.textContent.replace(/\s+/g,' ').slice(0,72) : '—');
      d.addEventListener('click', function(){ i = n; ovw.classList.remove('on'); show(); });
      ovw.appendChild(d);
    });
  }

  /* ---------- ปรับขนาดให้พอดีจอ ---------- */
  function fit(){
    var s = Math.min(window.innerWidth/1280, window.innerHeight/720);
    stage.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', fit);

  /* ---------- คีย์ ---------- */
  function go(d){
    var n = i + d;
    if(n < 0 || n >= deck.length) return;
    i = n; show();
  }
  document.addEventListener('keydown', function(e){
    var k = e.key;
    if(k === 'Escape'){ help.classList.remove('on'); ovw.classList.remove('on'); return; }
    if(k === '?' || k === '/'){ help.classList.toggle('on'); ovw.classList.remove('on'); return; }
    if(help.classList.contains('on') && k !== 'F5') { return; }
    if(k === 'ArrowRight' || k === 'PageDown' || k === ' '){ e.preventDefault(); go(1); }
    else if(k === 'ArrowLeft' || k === 'PageUp'){ e.preventDefault(); go(-1); }
    else if(k === 'Home'){ i = 0; show(); }
    else if(k === 'End'){ i = deck.length-1; show(); }
    else if(k === 'm' || k === 'M'){ pm = !pm; build(true); }
    else if(k === 'p' || k === 'P'){ notes.classList.toggle('on'); }
    else if(k === 'o' || k === 'O'){ ovw.classList.toggle('on'); }
    else if(k === 't' || k === 'T'){ paused = !paused; render(); }
    else if(k === 'r' || k === 'R'){ startTimer(deck[i]); }
    else if(k === 'f' || k === 'F'){
      if(document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }
  });
  document.addEventListener('click', function(e){
    if(e.target.closest('#ovw') || e.target.closest('#help') || e.target.closest('#notes')) return;
    if(help.classList.contains('on') || ovw.classList.contains('on')) return;
    go(e.clientX < window.innerWidth*0.22 ? -1 : 1);
  });

  function fromHash(){
    var n = parseInt((location.hash||'').replace('#',''),10);
    if(!isNaN(n) && n>=1 && n<=deck.length){ i = n-1; show(); }
  }
  window.addEventListener('hashchange', fromHash);
  fit(); build(false); fromHash();
})();

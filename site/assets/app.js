(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var P = window.PP || {}, page = document.body.getAttribute("data-page");
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (x) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (x) {} }
  };
  var tt;
  function toast(m) { var t = $("#toast"); if (!t) return; t.textContent = m; t.classList.add("on"); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove("on"); }, 2200); }
  var pick = function (a) { return a[Math.floor(Math.random() * a.length)]; };
  var fmt = function (n) { return Math.round(n).toLocaleString("en-US"); };
  /* segmented buttons */
  function seg(el, cb) {
    if (!el) return;
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("button", el).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      cb(b.getAttribute("data-v"));
    });
  }
  var segVal = function (el) { var b = $('button[aria-pressed="true"]', el); return b ? b.getAttribute("data-v") : ""; };

  /* nav */
  var bg = $(".burger"), nav = $("#nav");
  if (bg) bg.addEventListener("click", function () { var o = nav.classList.toggle("open"); bg.setAttribute("aria-expanded", o); });

  /* ---------- HOME ---------- */
  if (page === "index" && P.prompts) {
    var pk = $("#peek"); if (pk) pk.textContent = pick(P.prompts.theme) + " + " + pick(P.prompts.ephemera).toLowerCase();
  }

  /* ---------- ROW COUNTER ---------- */
  if (page === "row-counter") {
    var KEY = "pp-counters", S = store.get(KEY, null), undo = [], wake = null;
    if (!S || !S.list || !S.list.length) S = { list: [{ id: 1, name: "Rows", n: 0, target: "", rep: "" }], buzz: true, next: 2 };
    var wrap = $("#counters"), undoBtn = $("#rc-undo");
    var save = function () { store.set(KEY, S); };
    var find = function (id) { return S.list.filter(function (c) { return c.id === id; })[0]; };
    function info(c) {
      var t = parseInt(c.target, 10), r = parseInt(c.rep, 10), of = "", rep = "";
      if (t > 0) of = "of " + t + " rows" + (c.n >= t ? " · done!" : "");
      if (r > 0) rep = "Next: row " + (c.n % r + 1) + " of " + r + " · " + Math.floor(c.n / r) + " repeat" + (Math.floor(c.n / r) === 1 ? "" : "s") + " done";
      return { of: of, rep: rep, pct: t > 0 ? Math.min(100, c.n / t * 100) : 0 };
    }
    function odo(n) {
      var s = String(n); while (s.length < 3) s = "0" + s;
      return '<div class="odo" role="img" aria-label="' + n + ' rows">' + s.split("").map(function (d) { return '<span class="dg"><span class="strip" style="--d:' + d + '">' + "0123456789".split("").map(function (x) { return "<b>" + x + "</b>"; }).join("") + "</span></span>"; }).join("") + "</div>";
    }
    function setOdo(el, n) {
      var o = $(".odo", el), s = String(n); while (s.length < 3) s = "0" + s;
      var strips = $$(".strip", o);
      if (strips.length !== s.length) { o.outerHTML = odo(n); return; }
      s.split("").forEach(function (d, i) { strips[i].style.setProperty("--d", d); });
      o.setAttribute("aria-label", n + " rows");
    }
    function card(c) {
      var i = info(c);
      return '<article class="counter" data-id="' + c.id + '"><label class="sr-only" for="cn' + c.id + '">Counter name</label><input class="c-name" id="cn' + c.id + '" value="' + esc(c.name) + '" maxlength="40">' +
        '<button type="button" class="c-del" aria-label="Delete this counter" title="Delete">✕</button>' +
        '<div class="c-wheel">' + odo(c.n) + '</div><span class="sr-only c-num" aria-live="polite">' + c.n + '</span><div class="c-of">' + esc(i.of) + '</div><div class="c-bar"' + (i.pct ? "" : " hidden") + '><i style="width:' + i.pct + '%"></i></div>' +
        '<div class="c-btns"><button type="button" class="c-minus" aria-label="Take one row away">−</button><button type="button" class="c-plus" aria-label="Add one row">+</button></div>' +
        '<div class="c-rep"' + (i.rep ? "" : " hidden") + ">" + esc(i.rep) + "</div>" +
        '<div class="c-opts"><div><label for="ct' + c.id + '">Target rows</label><input type="number" min="0" inputmode="numeric" id="ct' + c.id + '" data-f="target" value="' + esc(c.target) + '" placeholder="Optional"></div>' +
        '<div><label for="cr' + c.id + '">Repeat every</label><input type="number" min="0" inputmode="numeric" id="cr' + c.id + '" data-f="rep" value="' + esc(c.rep) + '" placeholder="Rows"></div></div>' +
        '<div class="c-foot"><button type="button" class="linkbtn c-reset">Reset to 0</button><button type="button" class="linkbtn c-set">Set number</button></div></article>';
    }
    function render() { wrap.innerHTML = S.list.map(card).join(""); undoBtn.disabled = !undo.length; }
    function refresh(c, bump) {
      var el = $('.counter[data-id="' + c.id + '"]'); if (!el) return; var i = info(c), num = $(".c-num", el);
      num.textContent = c.n; setOdo(el, c.n); $(".c-of", el).textContent = i.of;
      $(".c-bar", el).hidden = !i.pct; $(".c-bar i", el).style.width = i.pct + "%";
      $(".c-rep", el).hidden = !i.rep; $(".c-rep", el).textContent = i.rep;
      undoBtn.disabled = !undo.length;
    }
    function change(c, d) {
      var nv = Math.max(0, c.n + d); if (nv === c.n) return;
      undo.push({ id: c.id, n: c.n }); if (undo.length > 50) undo.shift();
      c.n = nv; save(); refresh(c, d > 0);
      if (d > 0 && S.buzz && navigator.vibrate) navigator.vibrate(18);
      var t = parseInt(c.target, 10), r = parseInt(c.rep, 10);
      if (d > 0 && t > 0 && c.n === t) toast("Target reached: " + t + " rows");
      else if (d > 0 && r > 0 && c.n % r === 0) toast("Repeat " + c.n / r + " finished");
    }
    wrap.addEventListener("click", function (e) {
      var el = e.target.closest(".counter"); if (!el) return; var c = find(+el.getAttribute("data-id"));
      if (e.target.closest(".c-plus")) change(c, 1);
      else if (e.target.closest(".c-minus")) change(c, -1);
      else if (e.target.closest(".c-reset")) { if (c.n) { undo.push({ id: c.id, n: c.n }); c.n = 0; save(); refresh(c); toast("Reset. Use Undo if that was a mistake."); } }
      else if (e.target.closest(".c-set")) {
        var v = window.prompt("Set the count to:", c.n); if (v === null) return; v = parseInt(v, 10);
        if (v >= 0) { undo.push({ id: c.id, n: c.n }); c.n = v; save(); refresh(c); }
      } else if (e.target.closest(".c-del")) {
        var b = e.target.closest(".c-del");
        if (b.getAttribute("data-sure")) { S.list = S.list.filter(function (x) { return x !== c; }); if (!S.list.length) S.list.push({ id: S.next++, name: "Rows", n: 0, target: "", rep: "" }); save(); render(); toast("Counter deleted"); }
        else { b.setAttribute("data-sure", "1"); b.textContent = "?"; b.setAttribute("aria-label", "Tap again to delete"); toast("Tap ✕ again to delete this counter"); setTimeout(function () { if (b.isConnected) { b.removeAttribute("data-sure"); b.textContent = "✕"; } }, 3000); }
      }
    });
    wrap.addEventListener("input", function (e) {
      var el = e.target.closest(".counter"); if (!el) return; var c = find(+el.getAttribute("data-id"));
      if (e.target.classList.contains("c-name")) c.name = e.target.value;
      else if (e.target.getAttribute("data-f")) { c[e.target.getAttribute("data-f")] = e.target.value; refresh(c); }
      save();
    });
    $("#rc-add").addEventListener("click", function () {
      var names = ["Repeats", "Sleeve", "Decreases", "Rounds", "Pattern row"];
      S.list.push({ id: S.next++, name: names[(S.list.length - 1) % names.length], n: 0, target: "", rep: "" }); save(); render();
      var last = $$(".counter").pop(); if (last) last.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
    undoBtn.addEventListener("click", function () { var u = undo.pop(); if (!u) return; var c = find(u.id); if (c) { c.n = u.n; save(); refresh(c); } undoBtn.disabled = !undo.length; });
    var buzz = $("#rc-buzz"); buzz.checked = S.buzz !== false; buzz.addEventListener("change", function () { S.buzz = buzz.checked; save(); });
    var wk = $("#rc-wake");
    function lock() { if (!("wakeLock" in navigator)) return Promise.reject(); return navigator.wakeLock.request("screen").then(function (l) { wake = l; }); }
    wk.addEventListener("change", function () {
      if (wk.checked) lock().then(function () { toast("Screen will stay on while this page is open"); }, function () { wk.checked = false; toast("Your browser can't keep the screen on. Try Chrome, Edge or Safari 16.4+."); });
      else if (wake) { wake.release(); wake = null; }
    });
    document.addEventListener("visibilitychange", function () { if (wk.checked && document.visibilityState === "visible") lock().catch(function () {}); });
    document.addEventListener("keydown", function (e) {
      if (/input|textarea|select/i.test((e.target.tagName || ""))) return;
      var c = S.list[0]; if (!c) return;
      if (e.key === " " || e.key === "+" || e.key === "=") { e.preventDefault(); change(c, 1); }
      if (e.key === "-" || e.key === "_") { e.preventDefault(); change(c, -1); }
    });
    render();
  }

  /* a wound ball of yarn */
  function ball(c, spare, i) {
    var r = (i * 37) % 360, id = "yb" + i;
    return '<svg viewBox="0 0 48 48"' + (spare ? ' class="spare"' : "") + '><defs><radialGradient id="' + id + '" cx="38%" cy="32%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>' +
      '<circle cx="24" cy="24" r="19" fill="' + c + '"/><g transform="rotate(' + r + ' 24 24)" fill="none" stroke="rgba(0,0,0,.22)" stroke-width="1.1"><path d="M8 17c10 6 22 7 32 3M6 25c11 6 25 6 36 0M9 33c10 3 21 2 30-4"/><path d="M17 6c-4 10-3 25 3 37M27 5c5 9 6 25 0 38" stroke="rgba(255,255,255,.25)"/></g>' +
      '<circle cx="24" cy="24" r="19" fill="url(#' + id + ')"/><path d="M40 33c4 3 6 7 6 11" fill="none" stroke="' + c + '" stroke-width="2" stroke-linecap="round"/></svg>';
  }

  /* ---------- YARN CALCULATOR ---------- */
  if (page === "yarn-calculator") {
    var proj = $("#yc-proj"), sizeF = $("#yc-size-f"), size = $("#yc-size"), wt = $("#yc-weight"), sk = $("#yc-skein"), unit = $("#yc-unit"), out = $("#yc-out");
    var projs = P.projects || [], weights = P.weights || [];
    var pref = store.get("pp-yarn", null);
    if (pref) { proj.value = pref.p || proj.value; wt.value = pref.w || wt.value; sk.value = pref.s || sk.value; unit.value = pref.u || unit.value; }
    function sizes() {
      var p = projs.filter(function (x) { return x.id === proj.value; })[0];
      if (p && p.sizes) { var keep = size.value; size.innerHTML = Object.keys(p.sizes).map(function (k) { return "<option" + (k === (keep || "M") ? " selected" : "") + ">" + k + "</option>"; }).join(""); if (!size.value) size.value = "M"; sizeF.hidden = false; }
      else sizeF.hidden = true;
    }
    function calc() {
      var p = projs.filter(function (x) { return x.id === proj.value; })[0], w = weights.filter(function (x) { return String(x.n) === wt.value; })[0];
      if (!p || !w) return;
      var f = (p.sizes ? p.sizes[size.value] || 1 : 1) * w.m * (segVal($("#yc-craft")) === "crochet" ? 1.27 : 1) * parseFloat(segVal($("#yc-dense")) || 1);
      var yd = p.yd * f, lo = yd * 0.88, hi = yd * 1.12;
      var per = parseFloat(sk.value) || 0, perYd = unit.value === "m" ? per / 0.9144 : per;
      var n = perYd > 0 ? Math.ceil(hi / perYd) : 0, exact = perYd > 0 ? yd / perYd : 0;
      var col = ($('#yc-col [aria-pressed="true"]') || {}).getAttribute ? $('#yc-col [aria-pressed="true"]').getAttribute("data-c") : "#2f8f8a";
      var icons = ""; for (var i = 0; i < Math.min(n, 30); i++) icons += ball(col, i >= Math.ceil(exact), i);
      out.innerHTML = "<h3>Buy this many skeins</h3><div class=\"big\">" + (n || "–") + "</div>" +
        (n ? '<div class="balls" aria-hidden="true">' + icons + "</div>" : "") +
        "<p>You'll need about <strong>" + fmt(lo) + "–" + fmt(hi) + " yards</strong> (" + fmt(lo * 0.9144) + "–" + fmt(hi * 0.9144) + " m) of weight " + w.n + " " + esc(w.name.toLowerCase()) + " yarn.</p>" +
        (n ? '<p class="sub">That covers the high end of the estimate, so you shouldn\'t run short.' + (n > Math.ceil(exact) ? " The paler skein is your spare." : "") + "</p>" : '<p class="sub">Enter the length per skein from your yarn label to see how many to buy.</p>') +
        "<hr><p class=\"sub\">Needles: " + esc(w.needle) + "<br>Hook: " + esc(w.hook) + "</p>" + '<p class="aff-shop"><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Shop ' + esc(w.name.toLowerCase()) + ' yarn</a> · <a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">hooks</a> · <a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">needles</a></p><p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>';
      store.set("pp-yarn", { p: proj.value, w: wt.value, s: sk.value, u: unit.value });
    }
    seg($("#yc-craft"), calc); seg($("#yc-dense"), calc); seg($("#yc-col"), calc);
    [proj, size, wt, sk, unit].forEach(function (el) { el.addEventListener("input", function () { if (el === proj) sizes(); calc(); }); el.addEventListener("change", function () { if (el === proj) sizes(); calc(); }); });
    sizes(); calc();
  }

  /* ---------- BLANKET SIZE CALCULATOR ---------- */
  if ($("#bk-size") && $("#bk-out")) {
    var bkS = $("#bk-size"), bkC = $("#bk-custom"), bkW = $("#bk-w"), bkL = $("#bk-l"), bkWt = $("#bk-weight"), bkSk = $("#bk-skein"), bkU = $("#bk-unit"), bkO = $("#bk-out"), bkSvg = $("#bk-svg");
    var blankets = P.blankets || [], bkWeights = P.weights || [];
    var YD_PER_SQIN = 0.667; /* plain worsted knitting; matches the yarn calculator's throw estimate */
    var bkPref = store.get("pp-blanket", null);
    if (bkPref) { if (bkPref.s) bkS.value = bkPref.s; if (bkPref.w) bkW.value = bkPref.w; if (bkPref.l) bkL.value = bkPref.l; if (bkPref.y) bkWt.value = bkPref.y; if (bkPref.k) bkSk.value = bkPref.k; if (bkPref.u) bkU.value = bkPref.u; }
    function bkDraw(w, l, name) {
      /* everything in inches, 1 unit = 1 inch; a queen bed (60 x 80) for scale */
      var bedW = 60, bedL = 80, pad = 12, maxL = Math.max(l, bedL + 10);
      var sc = Math.min((320 - pad * 2) / (bedW + 30 + w), (240 - pad * 2 - 20) / maxL);
      var bx = pad, by = 240 - pad - bedL * sc, kx = pad + (bedW + 30) * sc, ky = 240 - pad - l * sc;
      var stripes = "", n = Math.max(3, Math.round(l / 6));
      for (var i = 1; i < n; i++) stripes += '<line x1="' + kx + '" x2="' + (kx + w * sc) + '" y1="' + (ky + i * l * sc / n) + '" y2="' + (ky + i * l * sc / n) + '" stroke="rgba(255,255,255,.35)" stroke-width="1" stroke-dasharray="3 2"/>';
      bkSvg.innerHTML =
        '<rect x="' + bx + '" y="' + by + '" width="' + bedW * sc + '" height="' + bedL * sc + '" rx="4" fill="#eef2ef" stroke="#1f2a44" stroke-width="1.5"/>' +
        '<rect x="' + (bx + 6 * sc) + '" y="' + (by + 4 * sc) + '" width="' + 21 * sc + '" height="' + 12 * sc + '" rx="3" fill="#fff" stroke="#1f2a44" stroke-width="1"/>' +
        '<rect x="' + (bx + 33 * sc) + '" y="' + (by + 4 * sc) + '" width="' + 21 * sc + '" height="' + 12 * sc + '" rx="3" fill="#fff" stroke="#1f2a44" stroke-width="1"/>' +
        '<text x="' + (bx + bedW * sc / 2) + '" y="' + (by + bedL * sc / 2 + 12) + '" text-anchor="middle" font-size="10" fill="#4a5470">Queen bed</text>' +
        '<text x="' + (bx + bedW * sc / 2) + '" y="' + (by + bedL * sc / 2 + 25) + '" text-anchor="middle" font-size="9" fill="#4a5470">60 × 80 in</text>' +
        '<rect x="' + kx + '" y="' + ky + '" width="' + w * sc + '" height="' + l * sc + '" rx="3" fill="#b8326a"/>' + stripes +
        '<rect x="' + kx + '" y="' + ky + '" width="' + w * sc + '" height="' + l * sc + '" rx="3" fill="none" stroke="#f4a823" stroke-width="3" stroke-dasharray="5 3"/>' +
        '<text x="' + (kx + w * sc / 2) + '" y="' + Math.max(12, ky - 6) + '" text-anchor="middle" font-size="10" font-weight="700" fill="#1f2a44">' + esc(name) + "</text>";
      $("#bk-cap").textContent = "Drawn to scale next to a queen mattress (60 × 80 in). Your blanket: " + w + " × " + l + " in.";
    }
    function bkCalc() {
      var custom = bkS.value === "custom", b = blankets.filter(function (x) { return x.id === bkS.value; })[0];
      bkC.hidden = !custom;
      var w = custom ? Math.min(140, Math.max(6, parseFloat(bkW.value) || 0)) : (b ? b.w : 50), l = custom ? Math.min(140, Math.max(6, parseFloat(bkL.value) || 0)) : (b ? b.l : 60);
      var name = custom ? "Your blanket" : (b ? b.name : "");
      var wt = bkWeights.filter(function (x) { return String(x.n) === bkWt.value; })[0]; if (!wt) return;
      var craft = segVal($("#bk-craft")) === "crochet" ? 1.27 : 1, dense = parseFloat(segVal($("#bk-dense")) || 1);
      var yd = w * l * YD_PER_SQIN * wt.m * craft * dense, lo = yd * 0.88, hi = yd * 1.12;
      var per = parseFloat(bkSk.value) || 0, perYd = bkU.value === "m" ? per / 0.9144 : per;
      var n = perYd > 0 ? Math.ceil(hi / perYd) : 0, exact = perYd > 0 ? yd / perYd : 0;
      var icons = ""; for (var i = 0; i < Math.min(n, 30); i++) icons += ball("#2f8f8a", i >= Math.ceil(exact), i);
      bkO.innerHTML = "<h3>" + esc(name) + '</h3><div class="bk-dims">' + w + " × " + l + " in<small>" + Math.round(w * 2.54) + " × " + Math.round(l * 2.54) + " cm" + (b && !custom ? " · common range " + esc(b.range) : "") + "</small></div>" +
        "<p>You'll need about <strong>" + fmt(lo) + "–" + fmt(hi) + " yards</strong> (" + fmt(lo * 0.9144) + "–" + fmt(hi * 0.9144) + " m) of weight " + wt.n + " " + esc(wt.name.toLowerCase()) + " yarn.</p>" +
        "<h3>Skeins to buy</h3><div class=\"big\">" + (n || "–") + "</div>" + (n ? '<div class="balls" aria-hidden="true">' + icons + "</div>" : "") +
        (n ? '<p class="sub">Covers the high end of the estimate' + (n > 30 ? " (first 30 skeins shown)" : "") + ". Add 5 to 10 percent for a wide border or fringe.</p>" : '<p class="sub">Enter the length per skein from your yarn label to see how many to buy.</p>') +
        '<hr><p class="sub">Hook: ' + esc(wt.hook) + "<br>Needles: " + esc(wt.needle) + "</p>";
      bkDraw(w, l, name);
      store.set("pp-blanket", { s: bkS.value, w: bkW.value, l: bkL.value, y: bkWt.value, k: bkSk.value, u: bkU.value });
    }
    seg($("#bk-craft"), bkCalc); seg($("#bk-dense"), bkCalc);
    [bkS, bkW, bkL, bkWt, bkSk, bkU].forEach(function (el) { el.addEventListener("input", bkCalc); el.addEventListener("change", bkCalc); });
    bkCalc();
  }

  /* ---------- GAUGE ---------- */
  if (page === "gauge-converter") {
    var ids = ["gc-ps", "gc-pr", "gc-ys", "gc-yr", "gc-cast", "gc-len"], go = $("#gc-out");
    var g = store.get("pp-gauge", null); if (g) ids.forEach(function (id) { if (g[id]) $("#" + id).value = g[id]; });
    var u = (g && g.u) || "in";
    $$("#gc-unit button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === u); });
    function strips() {
      var cv = $("#gv"); if (!cv || !window.Knit) return;
      var ps = parseFloat($("#gc-ps").value) || 0, ys = parseFloat($("#gc-ys").value) || 0, pr = parseFloat($("#gc-pr").value) || ps * 1.4, yr = parseFloat($("#gc-yr").value) || ys * 1.4;
      if (!ps || !ys) return;
      var base = u === "cm" ? 10 : 4, dpr = Math.min(window.devicePixelRatio || 1, 2), W = cv.clientWidth, H = 260, x = cv.getContext("2d");
      cv.width = W * dpr; cv.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, W, H);
      var n = Math.max(4, Math.min(40, Math.round(ps))), maxU = Math.max(base, base * ps / ys) * 1.06, ppu = (W - 8) / maxU;
      var rowsDrawn = 4;
      [[ps, pr, "#2f8f8a", "Pattern: " + n + " stitches"], [ys, yr, "#f4a823", "Yours: the same " + n + " stitches"]].forEach(function (g, i) {
        var sw = base / g[0] * ppu, sh = Math.min(base / g[1] * ppu, sw * 1.1), sp = new Knit.Sprites(sw, sh, dpr), top = 22 + i * 100;
        x.fillStyle = "rgba(255,255,255,0.85)"; x.font = "700 13px sans-serif"; x.fillText(g[3], 4, top - 6);
        for (var r = 0; r < rowsDrawn; r++) for (var c = 0; c < n; c++) sp.draw(x, g[2], 4 + c * sw, top + r * sh * 0.95, Knit.hash(r, c) === 0 ? -0.06 : 0);
      });
      var ry = 222; x.strokeStyle = "rgba(255,255,255,0.75)"; x.fillStyle = "rgba(255,255,255,0.75)"; x.lineWidth = 1.5;
      x.beginPath(); x.moveTo(4, ry); x.lineTo(4 + maxU * ppu, ry); x.stroke();
      for (var t = 0; t <= Math.floor(maxU); t++) { var tx = 4 + t * ppu; x.beginPath(); x.moveTo(tx, ry); x.lineTo(tx, ry + (t % (u === "cm" ? 5 : 1) === 0 ? 12 : 6)); x.stroke(); if (u !== "cm" || t % 5 === 0) x.fillText(t + (u === "cm" ? " cm" : " in"), tx + 2, ry + 26); }
    }
    function run() {
      var v = {}; ids.forEach(function (id) { v[id] = parseFloat($("#" + id).value) || 0; });
      var ul = u === "cm" ? "10 cm" : "4 in", base = u === "cm" ? 10 : 4, un = u === "cm" ? " cm" : " in";
      if (!v["gc-ps"] || !v["gc-ys"]) { go.innerHTML = "<p>Enter both gauges to compare.</p>"; return; }
      var pw = v["gc-cast"] / v["gc-ps"] * base, yw = v["gc-cast"] / v["gc-ys"] * base;
      var pl = v["gc-pr"] ? v["gc-len"] / v["gc-pr"] * base : 0, yl = v["gc-yr"] ? v["gc-len"] / v["gc-yr"] * base : 0;
      var dw = (yw / pw - 1) * 100, nc = Math.round(v["gc-cast"] * v["gc-ys"] / v["gc-ps"]), nr = v["gc-pr"] ? Math.round(v["gc-len"] * v["gc-yr"] / v["gc-pr"]) : 0;
      var r1 = function (x) { return (Math.round(x * 10) / 10).toString(); };
      var advice = Math.abs(dw) < 2 ? "Your gauge is close enough to the pattern. Go ahead." :
        (dw > 0 ? "Your fabric is looser than the pattern's, so the piece comes out bigger. Try a needle or hook about 0.5 mm smaller, or use the numbers below." : "Your fabric is tighter than the pattern's, so the piece comes out smaller. Try a needle or hook about 0.5 mm bigger, or use the numbers below.");
      go.innerHTML = "<h3>Your piece will be</h3><div class=\"big\">" + (dw > 0 ? "+" : "") + r1(dw) + "%</div>" +
        "<p>" + r1(yw) + un + " wide instead of " + r1(pw) + un + (pl ? ", and " + r1(yl) + un + " long instead of " + r1(pl) + un : "") + ".</p><p class=\"sub\">" + advice + "</p><hr>" +
        "<h3>To match the pattern's size, use</h3><p style=\"font-size:1.25rem;color:#fff\"><strong>" + nc + " stitches</strong>" + (nr ? " and <strong>" + nr + " rows</strong>" : "") + "</p>" +
        '<hr><h3>See the difference</h3><canvas class="gv" id="gv" role="img" aria-label="The same number of stitches knitted at the pattern gauge and at your gauge, over a ruler"></canvas>';
      strips();
      var sv = { u: u }; ids.forEach(function (id) { sv[id] = $("#" + id).value; }); store.set("pp-gauge", sv);
    }
    seg($("#gc-unit"), function (val) { u = val; run(); });
    ids.forEach(function (id) { $("#" + id).addEventListener("input", run); });
    run();
  }

  /* ---------- PROJECTS ---------- */
  if (page === "projects") {
    var PK = "pp-projects", list = store.get(PK, []), editing = null, filt = "";
    var colors = { Knitting: "#2f8f8a", Crochet: "#b8326a", "Junk journal": "#f4a823", Other: "#4a5470" };
    var F = { name: $("#pj-name"), craft: $("#pj-craft"), yarn: $("#pj-yarn"), tool: $("#pj-tool"), link: $("#pj-link"), start: $("#pj-start"), status: $("#pj-status"), prog: $("#pj-prog"), notes: $("#pj-notes") };
    var save2 = function () { store.set(PK, list); };
    function draw() {
      var rows = list.filter(function (p) { return !filt || p.status === filt; }), el = $("#pj-list");
      if (!rows.length) { el.innerHTML = '<div class="empty" style="grid-column:1/-1">' + (list.length ? "No projects with this status." : "No projects yet. Add your first one above, and it'll be saved on this device.") + "</div>"; return; }
      el.innerHTML = rows.map(function (p) {
        var link = p.link && /^https?:\/\//i.test(p.link) ? '<dt>Pattern</dt><dd><a href="' + esc(p.link) + '" target="_blank" rel="noopener nofollow">Open pattern</a></dd>' : "";
        return '<article class="proj" style="--pc:' + (colors[p.craft] || colors.Other) + '" data-id="' + p.id + '"><span class="tag">' + esc(p.craft) + '</span><span class="tag">' + esc(p.status) + "</span><h3>" + esc(p.name) + "</h3>" +
          '<div class="p-bar" aria-hidden="true"><i style="width:' + (+p.prog || 0) + '%"></i></div><p class="note" style="margin:0">' + (+p.prog || 0) + "% done</p>" +
          "<dl>" + (p.yarn ? "<dt>Yarn</dt><dd>" + esc(p.yarn) + "</dd>" : "") + (p.tool ? "<dt>Tool</dt><dd>" + esc(p.tool) + "</dd>" : "") + (p.start ? "<dt>Started</dt><dd>" + esc(p.start) + "</dd>" : "") + link + "</dl>" +
          (p.notes ? '<p style="white-space:pre-wrap;font-size:.95rem">' + esc(p.notes) + "</p>" : "") +
          '<div class="proj-actions"><button type="button" data-a="plus">+10%</button><button type="button" data-a="edit">Edit</button><button type="button" data-a="del">Delete</button></div></article>';
      }).join("");
    }
    function clear() { $("#pj-form").reset(); F.status.value = "In progress"; F.prog.value = 0; editing = null; $("#pj-cancel").hidden = true; $("#pj-form button[type=submit]").textContent = "Save project"; }
    $("#pj-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var p = editing ? list.filter(function (x) { return x.id === editing; })[0] : { id: Date.now() };
      Object.keys(F).forEach(function (k) { p[k] = F[k].value.trim ? F[k].value.trim() : F[k].value; });
      p.prog = Math.max(0, Math.min(100, parseInt(p.prog, 10) || 0)); if (p.status === "Finished") p.prog = 100;
      if (!editing) list.unshift(p); save2(); toast(editing ? "Project updated" : "Project saved"); clear(); draw();
    });
    $("#pj-cancel").addEventListener("click", clear);
    $("#pj-list").addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a]"); if (!b) return; var id = +b.closest(".proj").getAttribute("data-id"), p = list.filter(function (x) { return x.id === id; })[0]; if (!p) return;
      var a = b.getAttribute("data-a");
      if (a === "plus") { p.prog = Math.min(100, (+p.prog || 0) + 10); if (p.prog === 100) { p.status = "Finished"; toast("Finished! Well done."); } save2(); draw(); }
      if (a === "edit") { editing = id; Object.keys(F).forEach(function (k) { F[k].value = p[k] || ""; }); $("#pj-details").open = true; $("#pj-cancel").hidden = false; $("#pj-form button[type=submit]").textContent = "Update project"; F.name.focus(); $("#pj-details").scrollIntoView({ behavior: "smooth" }); }
      if (a === "del") {
        if (b.getAttribute("data-sure")) { list = list.filter(function (x) { return x !== p; }); save2(); draw(); toast("Project deleted"); }
        else { b.setAttribute("data-sure", "1"); b.textContent = "Tap again to delete"; setTimeout(function () { if (b.isConnected) { b.removeAttribute("data-sure"); b.textContent = "Delete"; } }, 3000); }
      }
    });
    seg($("#pj-filter"), function (v) { filt = v; draw(); });
    $("#pj-export").addEventListener("click", function () {
      var blob = new Blob([JSON.stringify({ site: "purl-and-paper", projects: list }, null, 2)], { type: "application/json" });
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "my-craft-projects.json"; document.body.appendChild(a); a.click(); a.remove();
    });
    $("#pj-import").addEventListener("change", function () {
      var f = this.files[0]; if (!f) return; var rd = new FileReader();
      rd.onload = function () {
        try { var d = JSON.parse(rd.result), got = (d.projects || []).filter(function (p) { return p && p.name; }), have = {};
          list.forEach(function (p) { have[p.id] = 1; }); got.forEach(function (p) { if (!have[p.id]) list.push(p); });
          save2(); draw(); toast(got.length + " projects restored"); } catch (x) { toast("That file isn't a project backup"); }
      };
      rd.readAsText(f); this.value = "";
    });
    draw();
  }

  /* ---------- PROMPTS ---------- */
  if (page === "journal-prompts" && P.prompts) {
    var cur = {}, locks = {}, SP = "pp-spreads", saved = store.get(SP, []), jpSets = P.prompts.sets || [], jpSea = $("#jp-season");
    if (jpSea) { var jpS0 = store.get("pp-season", ""); if (jpS0 && jpSets.some(function (x) { return x.id === jpS0; })) jpSea.value = jpS0; }
    function jpPool(k) {
      var set = jpSea ? jpSets.filter(function (x) { return x.id === jpSea.value; })[0] : null;
      return set && set[k] && set[k].length ? set[k] : P.prompts[k];
    }
    function fill(k, anim) {
      var el = $('[data-slot="' + k + '"]'), arr = jpPool(k), v; do { v = pick(arr); } while (arr.length > 1 && v === cur[k]); cur[k] = v;
      if (k === "palette") el.innerHTML = '<div class="palette">' + v.map(function (c) { return '<i style="background:' + c + '"><span>' + c + "</span></i>"; }).join("") + "</div>";
      else el.textContent = v;
      if (anim) { var cd = el.closest(".jp"); cd.classList.remove("drop"); void cd.offsetWidth; cd.style.animationDelay = (["theme", "ephemera", "technique", "palette", "write"].indexOf(k) * 70) + "ms"; cd.classList.add("drop"); }
    }
    function shuffle(anim) { ["theme", "ephemera", "technique", "palette", "write"].forEach(function (k) { if (!locks[k]) fill(k, anim); }); }
    $$(".lock").forEach(function (b) { b.addEventListener("click", function () { var k = b.getAttribute("data-lock"); locks[k] = !locks[k]; b.setAttribute("aria-pressed", locks[k]); b.textContent = locks[k] ? "Locked" : "Lock"; }); });
    function drawSaved() {
      var el = $("#jp-saved");
      el.innerHTML = saved.length ? saved.map(function (s, i) { return '<div class="sheet"><button type="button" class="linkbtn" data-del="' + i + '">Remove</button><strong>' + esc(s.theme) + "</strong><br>Glue in: " + esc(s.ephemera) + " · Try: " + esc(s.technique) + "<br>Write: " + esc(s.write) + '<div class="palette" style="height:18px;margin-top:8px;max-width:220px">' + (s.palette || []).map(function (c) { return '<i style="background:' + c + '"></i>'; }).join("") + "</div></div>"; }).join("") : '<p class="muted">Spreads you save appear here, on this device.</p>';
    }
    $("#jp-saved").addEventListener("click", function (e) { var b = e.target.closest("[data-del]"); if (!b) return; saved.splice(+b.getAttribute("data-del"), 1); store.set(SP, saved); drawSaved(); });
    $("#jp-go").addEventListener("click", function () { shuffle(true); });
    if (jpSea) jpSea.addEventListener("change", function () { store.set("pp-season", jpSea.value); shuffle(true); });
    $("#jp-save").addEventListener("click", function () { saved.unshift(JSON.parse(JSON.stringify(cur))); saved = saved.slice(0, 40); store.set(SP, saved); drawSaved(); toast("Spread saved"); });
    $("#jp-print").addEventListener("click", function () { window.print(); });
    shuffle(false); drawSaved();
  }

  /* ---------- HOOK + NEEDLE FINDER ---------- */
  if (page === "hook-needle-sizes") {
    var q = $("#hn-q"), hit = $("#hn-hit"), trs = $$("#hn-table tbody tr");
    q.addEventListener("input", function () {
      var s = q.value.trim().toLowerCase().replace(/\s+/g, " "), col = -1, val = s, found = null;
      trs.forEach(function (tr) { tr.classList.remove("hl"); });
      if (!s) { hit.textContent = ""; return; }
      if (/^uk/.test(s)) { col = 2; val = s.replace(/^uk ?/, ""); }
      else if (/^us/.test(s)) { col = 1; val = s.replace(/^us ?/, ""); }
      else if (/[a-z]/.test(s.replace(/mm$/, "").trim())) { col = 3; val = s; }
      else { col = 0; val = s.replace(/ ?mm$/, ""); }
      val = val.replace("1/2", "½").replace(".5", s.indexOf("mm") > -1 || col === 0 ? ".5" : "½");
      trs.forEach(function (tr) {
        if (found) return; var td = tr.children, t;
        if (col === 0) { if (tr.getAttribute("data-mm") === val) found = tr; }
        else { t = td[col].textContent.toLowerCase(); if (col === 3 ? (t === val || t.split(/[-/]/).indexOf(val) > -1) : t === val) found = tr; }
      });
      if (!found && col === 0) { var hv = val.replace(".5", "½"); trs.forEach(function (tr) { if (!found && tr.children[1].textContent.toLowerCase() === hv) found = tr; }); }
      if (found) {
        var c = found.children; found.classList.add("hl"); found.scrollIntoView({ block: "nearest", behavior: "smooth" });
        hit.textContent = c[0].textContent + " = US needle " + c[1].textContent + " = UK " + c[2].textContent + " = hook " + c[3].textContent;
      } else hit.textContent = "No exact match. Try a millimetre size like 4.5 or 5 mm.";
    });
  }

  /* ---------- HANDMADE GIFT PLANNER ---------- */
  if ($("#gp-form") && $("#gp-out") && P.gifts) {
    var GKEY = "pp-gifts", gifts = P.gifts, gpCols = ["#b8326a", "#f4a823", "#2f8f8a", "#efe6d6", "#8a5a44", "#9aa4b8"];
    var gById = function (id) { return gifts.filter(function (g) { return g.id === id; })[0]; };
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var defDue = function () { var d = new Date(today.getFullYear(), 11, 24); if (d < today) d = new Date(today.getFullYear() + 1, 11, 24); return d; };
    var iso = function (d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); };
    var nice = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }); };
    var half = function (n) { return Math.max(0.5, Math.round(n * 2) / 2); };
    var GS = store.get(GKEY, null);
    if (!GS || !GS.list) GS = { due: iso(defDue()), hrs: 7, speed: "1", next: 4, list: [
      { id: 1, who: "Mum", proj: "hat", craft: "knit", h: 9, done: false },
      { id: 2, who: "Sam", proj: "scarf", craft: "crochet", h: 12, done: false },
      { id: 3, who: "Neighbour", proj: "dishcloth", craft: "crochet", h: 1.5, done: false }] };
    var gDue = $("#gp-due"), gHrs = $("#gp-hrs"), gWho = $("#gp-who"), gProj = $("#gp-proj"), gYarn = $("#gp-yarn"), gH = $("#gp-h"), gList = $("#gp-list"), gOut = $("#gp-out");
    gDue.value = GS.due || iso(defDue()); gHrs.value = GS.hrs || 7;
    $$("#gp-speed button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === String(GS.speed || "1")); });
    var gSave = function () { store.set(GKEY, GS); };
    function suggest() {
      var g = gById(gProj.value); if (!g) return;
      var craft = segVal($("#gp-craft")) || "knit", base = g[craft] * parseFloat(gYarn.value || 1);
      gH.value = half(base);
      $("#gp-hint").textContent = "Typical: about " + half(base) + " hours to " + (craft === "knit" ? "knit" : "crochet") + " in this yarn at a comfortable pace. Change it if you know your own speed.";
    }
    function gpRender() {
      var speed = parseFloat(segVal($("#gp-speed")) || 1), hrs = Math.max(0, parseFloat(gHrs.value) || 0);
      var due = gDue.value ? new Date(gDue.value + "T00:00:00") : defDue();
      var days = Math.max(0, Math.round((due - today) / 86400000)), avail = days / 7 * hrs, perDay = hrs / 7;
      var todo = GS.list.filter(function (x) { return !x.done; }), need = 0;
      var sched = todo.map(function (x) { var h = x.h * speed; need += h; return { x: x, h: h, end: need }; });
      gList.innerHTML = GS.list.length ? GS.list.map(function (x, i) {
        var g = gById(x.proj) || { name: x.proj };
        return '<li class="gp-item' + (x.done ? " done" : "") + '" data-id="' + x.id + '"><i class="gp-dot" style="--c:' + gpCols[i % gpCols.length] + '" aria-hidden="true"></i>' +
          '<div class="gp-what"><strong>' + esc(x.who || "Someone") + "</strong><span>" + esc(g.name) + " · " + (x.craft === "crochet" ? "crochet" : "knit") + " · " + x.h + " h</span></div>" +
          '<label class="gp-done"><input type="checkbox" data-act="done"' + (x.done ? " checked" : "") + "> Done</label>" +
          (i ? '<button type="button" class="gp-mini" data-act="up" aria-label="Make this one sooner">↑</button>' : '<span class="gp-mini-sp"></span>') +
          '<button type="button" class="gp-mini" data-act="del" aria-label="Remove this gift">✕</button></li>';
      }).join("") : '<li class="note">No gifts yet. Add the first one above.</li>';
      var over = need - avail, scale = Math.max(avail, need, 1), cum = 0;
      var segs = sched.map(function (s) {
        var i = GS.list.indexOf(s.x), w = s.h / scale * 100, late = s.end > avail + 0.01; cum += s.h;
        return '<i class="gp-seg' + (late ? " late" : "") + '" style="width:' + w.toFixed(2) + "%;--c:" + gpCols[i % gpCols.length] + '" title="' + esc(s.x.who) + '"></i>';
      }).join("");
      var mark = Math.min(100, avail / scale * 100);
      var rows = sched.map(function (s) {
        var d = perDay > 0 ? new Date(today.getTime() + Math.ceil(s.end / perDay) * 86400000) : null, late = s.end > avail + 0.01, g = gById(s.x.proj) || { name: s.x.proj };
        return "<li" + (late ? ' class="late"' : "") + "><span>" + esc(s.x.who || "Someone") + ": " + esc(g.name.toLowerCase()) + "</span><b>" + (d ? (late ? "after the deadline" : "around " + nice(d)) : "–") + "</b></li>";
      }).join("");
      var verdict;
      if (!todo.length) verdict = '<p class="gp-ok">' + (GS.list.length ? "Everything on your list is done. Time to wrap!" : "Add a gift to see if it fits.") + "</p>";
      else if (over <= 0) verdict = '<p class="gp-ok">On track, with about <strong>' + fmt(-over) + " hours</strong> to spare.</p>";
      else {
        var lateOnes = sched.filter(function (s) { return s.end > avail + 0.01; }).length, big = sched.slice().sort(function (a, b) { return b.h - a.h; })[0];
        verdict = '<p class="gp-short">About <strong>' + fmt(over) + " hours short</strong>. " + lateOnes + " gift" + (lateOnes > 1 ? "s" : "") + " won't be ready in time.</p>" +
          '<p class="sub">Ideas: ' + (big.h >= 5 ? "make " + (big.x.who && big.x.who !== "Someone" ? esc(big.x.who) + "'s " : "the ") + esc((gById(big.x.proj) || { name: "" }).name.toLowerCase()) + " in chunky yarn (saves about " + fmt(big.h * 0.35) + " hours), " : "") +
          "find " + fmt(over / Math.max(days / 7, 0.15)) + " more hours a week, or swap something big for a quick hat or cowl.</p>";
      }
      gOut.innerHTML = "<h3>Time until " + esc(nice(due)) + '</h3><div class="big">' + fmt(avail) + "<small> h</small></div>" +
        '<p class="sub">' + days + " days at " + hrs + " hours a week. Your list needs about " + fmt(need) + " hours" + (speed !== 1 ? " at your pace" : "") + ".</p>" + verdict +
        (sched.length ? '<div class="gp-strand" role="img" aria-label="Your gifts in order along the time you have; the line marks your deadline">' + segs + '<span class="gp-due" style="left:' + mark.toFixed(2) + '%"></span></div><p class="sub" style="margin-top:6px">Each bead is a gift. The line is your deadline.</p><ul class="gp-dates">' + rows + "</ul>" : "") +
        '<hr><p class="sub">Times are estimates. Your own pace is the best guide.</p>';
      GS.due = gDue.value; GS.hrs = gHrs.value; GS.speed = segVal($("#gp-speed")); gSave();
    }
    seg($("#gp-craft"), suggest); seg($("#gp-speed"), gpRender);
    [gProj, gYarn].forEach(function (el) { el.addEventListener("change", suggest); });
    [gDue, gHrs].forEach(function (el) { el.addEventListener("input", gpRender); el.addEventListener("change", gpRender); });
    $("#gp-form").addEventListener("submit", function (ev) {
      ev.preventDefault();
      var h = parseFloat(gH.value); if (!(h > 0)) { suggest(); h = parseFloat(gH.value); }
      GS.list.push({ id: GS.next++, who: gWho.value.trim().slice(0, 40) || "Someone", proj: gProj.value, craft: segVal($("#gp-craft")) || "knit", h: Math.min(300, h), done: false });
      gWho.value = ""; gpRender(); toast("Added to your list");
    });
    gList.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-act]"), li = ev.target.closest("li[data-id]"); if (!b || !li) return;
      var id = parseInt(li.getAttribute("data-id"), 10), i = -1;
      GS.list.forEach(function (x, j) { if (x.id === id) i = j; }); if (i < 0) return;
      var act = b.getAttribute("data-act");
      if (act === "del") { GS.list.splice(i, 1); toast("Gift removed"); }
      else if (act === "up" && i > 0) { var t = GS.list[i - 1]; GS.list[i - 1] = GS.list[i]; GS.list[i] = t; }
      else if (act === "done") GS.list[i].done = b.checked;
      else return;
      gpRender();
    });
    $("#gp-print").addEventListener("click", function () { window.print(); });
    $("#gp-clear").addEventListener("click", function () { if (!GS.list.length) return; if (window.confirm("Remove every gift from the list?")) { GS.list = []; gpRender(); } });
    suggest(); gpRender();
  }
  /* ---------- Hat size calculator ---------- */
  if ($("#ht-size") && $("#ht-out")) {
    var htS = $("#ht-size"), htC = $("#ht-custom"), htH = $("#ht-head"), htHU = $("#ht-hu"), htE = $("#ht-ease"), htG = $("#ht-g"), htGU = $("#ht-gu"), htR = $("#ht-rep"), htO = $("#ht-out"), htSvg = $("#ht-svg");
    var hats = P.hats || [], htTouched = { e: false, g: false, r: false };
    var htPref = store.get("pp-hat", null);
    if (htPref) { ["s", "h", "hu", "e", "g", "gu", "r"].forEach(function (k) { var el = { s: htS, h: htH, hu: htHU, e: htE, g: htG, gu: htGU, r: htR }[k]; if (htPref[k] != null && htPref[k] !== "") el.value = htPref[k]; }); htTouched = { e: true, g: true, r: true }; if (htPref.c === "crochet") $$("#ht-craft button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "crochet"); }); }
    var r1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var both = function (inch) { return r1(inch) + " in (" + Math.round(inch * 2.54) + " cm)"; };
    function htDraw(fw, h, crochet) {
      var sc = 14, cx = 150, base = 196, w = Math.max(30, fw * sc), hh = Math.max(30, h * sc), x0 = cx - w / 2, top = base - hh, brim = Math.max(8, hh * 0.2), dome = Math.min(w * 0.42, hh * 0.45);
      var body = "M" + x0 + " " + base + " L" + x0 + " " + (top + dome) + " C" + x0 + " " + (top + dome * 0.2) + " " + (cx - w * 0.22) + " " + top + " " + cx + " " + top + " C" + (cx + w * 0.22) + " " + top + " " + (x0 + w) + " " + (top + dome * 0.2) + " " + (x0 + w) + " " + (top + dome) + " L" + (x0 + w) + " " + base + " Z";
      var lines = "", step = crochet ? 9 : 7, i;
      for (i = x0 + step / 2; i < x0 + w; i += step) lines += '<line x1="' + i + '" x2="' + i + '" y1="' + (base - brim) + '" y2="' + base + '" stroke="rgba(255,255,255,.45)" stroke-width="2"/>';
      for (var y = base - brim - 8; y > top + 6; y -= 8) lines += '<path d="M' + (x0 + 4) + " " + y + " q" + (w / 2 - 4) + " -4 " + (w - 8) + ' 0" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="1.5" stroke-dasharray="' + (crochet ? "2 3" : "4 2") + '"/>';
      htSvg.innerHTML = '<defs><clipPath id="htc"><path d="' + body + '"/></clipPath></defs>' +
        '<path d="' + body + '" fill="#b8326a"/><g clip-path="url(#htc)">' + lines + '<rect x="' + x0 + '" y="' + (base - brim) + '" width="' + w + '" height="' + brim + '" fill="rgba(31,42,68,.18)"/></g>' +
        '<path d="' + body + '" fill="none" stroke="#1f2a44" stroke-width="2"/>' +
        '<circle cx="' + cx + '" cy="' + (top - 7) + '" r="' + Math.max(6, w * 0.08) + '" fill="#f4a823" stroke="#1f2a44" stroke-width="1.5"/>' +
        '<line x1="' + x0 + '" x2="' + (x0 + w) + '" y1="' + (base + 14) + '" y2="' + (base + 14) + '" stroke="#2f8f8a" stroke-width="2"/><line x1="' + x0 + '" x2="' + x0 + '" y1="' + (base + 9) + '" y2="' + (base + 19) + '" stroke="#2f8f8a" stroke-width="2"/><line x1="' + (x0 + w) + '" x2="' + (x0 + w) + '" y1="' + (base + 9) + '" y2="' + (base + 19) + '" stroke="#2f8f8a" stroke-width="2"/>' +
        '<text x="' + cx + '" y="' + (base + 30) + '" text-anchor="middle" font-size="11" font-weight="700" fill="#1f2a44">' + r1(fw) + ' in flat</text>' +
        '<line x1="' + (x0 + w + 16) + '" x2="' + (x0 + w + 16) + '" y1="' + top + '" y2="' + base + '" stroke="#2f8f8a" stroke-width="2"/><line x1="' + (x0 + w + 11) + '" x2="' + (x0 + w + 21) + '" y1="' + top + '" y2="' + top + '" stroke="#2f8f8a" stroke-width="2"/><line x1="' + (x0 + w + 11) + '" x2="' + (x0 + w + 21) + '" y1="' + base + '" y2="' + base + '" stroke="#2f8f8a" stroke-width="2"/>' +
        '<text x="' + (x0 + w + 26) + '" y="' + ((top + base) / 2 + 4) + '" font-size="11" font-weight="700" fill="#1f2a44">' + r1(h) + ' in</text>';
    }
    function htCalc() {
      var crochet = segVal($("#ht-craft")) === "crochet", custom = htS.value === "custom";
      htC.hidden = !custom;
      var preset = hats.filter(function (x) { return x.id === htS.value; })[0], head;
      if (custom) { head = parseFloat(htH.value) || 0; if (htHU.value === "cm") head = head / 2.54; head = Math.min(30, Math.max(8, head)); }
      else head = preset ? preset.head : 22;
      var near = preset; if (custom || !near) near = hats.reduce(function (a, b) { return Math.abs(b.head - head) < Math.abs(a.head - head) ? b : a; }, hats[0] || { hn: 11, name: "Adult" });
      var h = near ? near.hn : 11, ease = parseFloat(htE.value) || 0, hat = head * (1 - ease / 100);
      var g = parseFloat(htG.value) || 0, spi = g / (htGU.value === "10" ? 10 / 2.54 : 4), rep = parseInt(htR.value, 10) || 1;
      var n = spi > 0 ? Math.max(rep, Math.round(hat * spi / rep) * rep) : 0, real = spi > 0 ? n / spi : hat;
      var crown = Math.min(3.25, Math.max(1.5, real / 7)), dia = real / Math.PI;
      var who = custom ? "A " + r1(head) + " in head" : (preset ? preset.name + " · " + preset.age : "");
      var out = "<h3>" + esc(who) + '</h3><div class="bk-dims">' + r1(real) + " in around<small>" + Math.round(real * 2.54) + " cm hat on a " + both(head) + " head · " + r1((1 - real / head) * 100) + "% smaller</small></div>";
      if (!n) out += '<p class="sub">Enter the stitches in your swatch to see the count.</p>';
      else if (!crochet) out += "<h3>Cast on</h3><div class=\"big\">" + n + "</div><p class=\"sub\">stitches, " + (rep > 1 ? "a multiple of " + rep + ", " : "") + "at " + r1(spi) + " stitches per inch.</p><hr>" +
        "<p>Knit until the hat measures about <strong>" + both(Math.max(1, h - crown)) + "</strong>, then start the crown decreases. The finished hat should be about <strong>" + both(h) + "</strong> tall, before any fold-up brim.</p>";
      else out += "<h3>Crochet the crown circle to</h3><div class=\"big\">" + r1(dia) + " in</div><p class=\"sub\">across (" + Math.round(dia * 2.54) + " cm), with about " + n + " stitches in the last increase round" + (rep > 1 ? " (a multiple of " + rep + ")" : "") + ".</p><hr>" +
        "<p>Then stop increasing and work even rounds until the hat measures about <strong>" + both(h) + "</strong> from the centre of the crown.</p>";
      out += '<p class="sub">Every head is different. These are good starting numbers, so try the hat on as you go.</p>';
      htO.innerHTML = out;
      htDraw(real / 2, h, crochet);
      $("#ht-cap").textContent = "Your hat laid flat: " + r1(real / 2) + " in wide and " + r1(h) + " in tall (" + Math.round(real / 2 * 2.54) + " × " + Math.round(h * 2.54) + " cm).";
      store.set("pp-hat", { s: htS.value, h: htH.value, hu: htHU.value, e: htE.value, g: htG.value, gu: htGU.value, r: htR.value, c: crochet ? "crochet" : "knit" });
    }
    seg($("#ht-craft"), function () {
      var crochet = segVal($("#ht-craft")) === "crochet";
      if (!htTouched.e) htE.value = crochet ? "8" : "12";
      if (!htTouched.g) htG.value = crochet ? "14" : "18";
      if (!htTouched.r) htR.value = crochet ? "6" : "8";
      htCalc();
    });
    htE.addEventListener("change", function () { htTouched.e = true; }); htG.addEventListener("input", function () { htTouched.g = true; }); htR.addEventListener("change", function () { htTouched.r = true; });
    [htS, htH, htHU, htE, htG, htGU, htR].forEach(function (el) { el.addEventListener("input", htCalc); el.addEventListener("change", htCalc); });
    htCalc();
  }
  /* ---------- Sock size calculator ---------- */
  if ($("#sk-size") && $("#sk-out")) {
    var skEl = {}; ["size", "custom", "circ", "len", "mu", "yarn", "g", "gu", "ease", "rep", "out", "svg", "cap"].forEach(function (k) { skEl[k] = $("#sk-" + k); });
    var socks = P.socks || [], skKeys = ["size", "circ", "len", "mu", "yarn", "g", "gu", "ease", "rep"], skTouchedG = false;
    var SOCK_K = 1.32; /* yd of fingering per sq in of sock fabric, heel and toe included (estimate; women's medium pair ~350 yd) */
    var skPref = store.get("pp-sock", null);
    if (skPref) { skKeys.forEach(function (k) { if (skPref[k] != null && skPref[k] !== "") skEl[k].value = skPref[k]; }); skTouchedG = true; }
    var s1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var sBoth = function (inch) { return s1(inch) + " in (" + Math.round(inch * 2.54) + " cm)"; };
    var even = function (n) { return Math.max(2, Math.round(n / 2) * 2); };
    function skDraw(leg, foot, circ) {
      var sc = Math.min(150 / Math.max(foot, 1), 140 / Math.max(leg, 1), 16), w = Math.max(26, circ / 2 * sc * 0.9);
      var x0 = 70, top = 22, lh = leg * sc, fl = foot * sc, base = top + lh + w * 0.55, xr = x0 + w;
      if (base + w * 0.5 > 200) { var k = (200 - top) / (lh + w * 1.05); sc *= k; lh = leg * sc; fl = foot * sc; w *= k; xr = x0 + w; base = top + lh + w * 0.55; }
      var heelX = x0, toeX = x0 + fl, fy = base - w * 0.5;
      var d = "M" + x0 + " " + top + " L" + xr + " " + top + " L" + xr + " " + fy + " L" + (toeX - w * 0.45) + " " + fy +
        " Q" + toeX + " " + fy + " " + toeX + " " + (fy + w * 0.25) + " Q" + toeX + " " + base + " " + (toeX - w * 0.45) + " " + base +
        " L" + (heelX + w * 0.4) + " " + base + " Q" + (heelX - w * 0.15) + " " + base + " " + (heelX - w * 0.12) + " " + (base - w * 0.5) + " L" + x0 + " " + (top + lh) + " Z";
      var cuff = Math.min(lh * 0.3, 1.5 * sc), ribs = "", i;
      for (i = x0 + 4; i < xr - 2; i += 6) ribs += '<line x1="' + i + '" x2="' + i + '" y1="' + top + '" y2="' + (top + cuff) + '" stroke="rgba(255,255,255,.5)" stroke-width="2"/>';
      var toeL = Math.min(w * 0.9, fl * 0.22);
      skEl.svg.innerHTML = '<defs><clipPath id="skc"><path d="' + d + '"/></clipPath></defs><path d="' + d + '" fill="#2f8f8a"/>' +
        '<g clip-path="url(#skc)">' + ribs + '<rect x="' + (heelX - w) + '" y="' + (base - w * 0.75) + '" width="' + (w * 1.3) + '" height="' + w + '" fill="#f4a823" opacity=".9"/><rect x="' + (toeX - toeL) + '" y="' + (fy - 2) + '" width="' + (toeL + 4) + '" height="' + (w + 4) + '" fill="#b8326a" opacity=".9"/></g>' +
        '<path d="' + d + '" fill="none" stroke="#1f2a44" stroke-width="2"/>' +
        '<line x1="' + (x0 - 14) + '" x2="' + (x0 - 14) + '" y1="' + top + '" y2="' + (top + lh) + '" stroke="#1f2a44" stroke-width="1.5"/><text x="' + (x0 - 18) + '" y="' + (top + lh / 2) + '" text-anchor="end" font-size="11" font-weight="700" fill="#1f2a44">' + s1(leg) + ' in</text>' +
        '<text x="' + (x0 - 18) + '" y="' + (top + lh / 2 + 13) + '" text-anchor="end" font-size="10" fill="#1f2a44">leg</text>' +
        '<line x1="' + (heelX - w * 0.12) + '" x2="' + toeX + '" y1="' + (base + 14) + '" y2="' + (base + 14) + '" stroke="#1f2a44" stroke-width="1.5"/><text x="' + ((heelX + toeX) / 2) + '" y="' + (base + 28) + '" text-anchor="middle" font-size="11" font-weight="700" fill="#1f2a44">' + s1(foot) + ' in foot</text>';
    }
    function skCalc() {
      var custom = skEl.size.value === "custom"; skEl.custom.hidden = !custom;
      var pre = socks.filter(function (x) { return x.id === skEl.size.value; })[0], circ, len, leg, who;
      if (custom) {
        var f = skEl.mu.value === "cm" ? 1 / 2.54 : 1;
        circ = Math.min(14, Math.max(3, (parseFloat(skEl.circ.value) || 0) * f)); len = Math.min(16, Math.max(2.5, (parseFloat(skEl.len.value) || 0) * f));
        var near = socks.reduce(function (a, b) { return Math.abs((b.lmin + b.lmax) / 2 - len) < Math.abs((a.lmin + a.lmax) / 2 - len) ? b : a; }, socks[0] || { leg: 7 });
        leg = near.leg; who = "A foot " + s1(circ) + " in around, " + s1(len) + " in long";
      } else { pre = pre || socks[0]; circ = pre.circ; len = (pre.lmin + pre.lmax) / 2; leg = pre.leg; who = pre.name + " · " + pre.shoe; }
      var yp = skEl.yarn.value.split("|"), yf = parseFloat(yp[0]) || 1;
      var g = parseFloat(skEl.g.value) || 0, spi = g / (skEl.gu.value === "10" ? 10 / 2.54 : 4), ease = parseFloat(skEl.ease.value) || 0, rep = parseInt(skEl.rep.value, 10) || 4;
      var target = circ * (1 - ease / 100), n = spi > 0 ? Math.max(rep, Math.round(target * spi / rep) * rep) : 0, real = spi > 0 ? n / spi : target;
      var toe = len >= 8 ? 2 : Math.max(0.75, len * 0.2), heel = even(n / 2), flapRows = heel, pick = Math.round(flapRows / 2) + 1, toeEnd = Math.max(8, even(n / 4));
      var yd = SOCK_K * circ * (len + leg) * 2 * yf, lo = Math.round(yd * 0.88 / 5) * 5, hi = Math.round(yd * 1.12 / 5) * 5;
      var out = "<h3>" + esc(who) + '</h3><div class="bk-dims">' + s1(real) + " in around<small>" + Math.round(real * 2.54) + " cm sock on a " + sBoth(circ) + " foot · " + s1((1 - real / circ) * 100) + "% smaller</small></div>";
      if (!n) out += '<p class="sub">Enter the stitches in your swatch to see the numbers.</p>';
      else out += "<h3>Cast on</h3><div class=\"big\">" + n + "</div><p class=\"sub\">stitches, a multiple of " + rep + ", at " + s1(spi) + " stitches per inch.</p><hr>" +
        "<ol class=\"sk-steps\"><li><strong>Leg:</strong> cuff and leg about " + sBoth(leg) + " for a crew sock.</li>" +
        "<li><strong>Heel flap:</strong> " + heel + " stitches, worked for about " + flapRows + " rows.</li>" +
        "<li><strong>Gusset:</strong> pick up about " + pick + " stitches on each side, then decrease every other round back to " + n + ".</li>" +
        "<li><strong>Foot:</strong> knit until it measures <strong>" + sBoth(Math.max(1, len - toe)) + "</strong> from the back of the heel.</li>" +
        "<li><strong>Toe:</strong> decrease 4 every other round to " + even(n / 2) + ", then every round to about " + toeEnd + ". Graft closed.</li></ol>";
      out += "<hr><h3>Yarn for the pair</h3><p><strong>" + lo + "–" + hi + " yd</strong> (" + Math.round(lo * 0.9144) + "–" + Math.round(hi * 0.9144) + " m). An estimate for plain socks; buy a little extra for cables or a taller leg.</p>";
      out += '<p class="sub">Feet vary, so try the sock on as you go. Next: <a href="' + (location.protocol === "file:" ? "row-counter.html" : "/row-counter") + '">row counter</a> for the heel flap, <a href="' + (location.protocol === "file:" ? "hook-needle-sizes.html" : "/hook-needle-sizes") + '">needle sizes</a>.</p>';
      skEl.out.innerHTML = out;
      skDraw(leg, len, circ);
      skEl.cap.textContent = "Your sock: leg about " + s1(leg) + " in, foot " + s1(len) + " in, heel in gold and toe in pink.";
      var save = {}; skKeys.forEach(function (k) { save[k] = skEl[k].value; }); store.set("pp-sock", save);
    }
    var skMu = skEl.mu.value;
    skEl.mu.addEventListener("change", function () {
      var f = skEl.mu.value === "cm" && skMu === "in" ? 2.54 : (skEl.mu.value === "in" && skMu === "cm" ? 1 / 2.54 : 1); skMu = skEl.mu.value;
      [skEl.circ, skEl.len].forEach(function (el) { var v = parseFloat(el.value); if (v) el.value = Math.round(v * f * 4) / 4; });
    });
    skEl.g.addEventListener("input", function () { skTouchedG = true; });
    skEl.yarn.addEventListener("change", function () { if (!skTouchedG) skEl.g.value = skEl.yarn.value.split("|")[1]; });
    skKeys.forEach(function (k) { skEl[k].addEventListener("input", skCalc); skEl[k].addEventListener("change", skCalc); });
    skCalc();
  }
  /* ---------- Cast on calculator ---------- */
  if ($("#co-what") && $("#co-out")) {
    var coEl = {}; ["what", "custom", "w", "wu", "mode", "yarn", "g", "gu", "pat", "rep", "m", "x", "flat", "b", "s", "out", "svg", "cap"].forEach(function (k) { coEl[k] = $("#co-" + k); });
    var coKeys = ["what", "w", "wu", "mode", "yarn", "g", "gu", "pat", "m", "x", "b", "s"], coTouchedG = false;
    var CO_TAIL = 4.5; /* tail per stitch = 4.5 / stitches per inch (about 1 in per stitch at worsted), plus 6 in: estimate */
    var coPref = store.get("pp-caston", null);
    if (coPref) { coKeys.forEach(function (k) { if (coPref[k] != null && coPref[k] !== "" && coEl[k]) coEl[k].value = coPref[k]; }); coTouchedG = true; }
    var c1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var cBoth = function (inch) { return c1(inch) + " in (" + Math.round(inch * 2.54) + " cm)"; };
    var coLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function coCount(width, spi, mult, extra, border, selv) {
      var b = border ? Math.round(border * spi) : 0, reps = Math.max(1, Math.round((width * spi - 2 * b - 2 * selv - extra) / mult));
      return { reps: reps, b: b, total: reps * mult + extra + 2 * b + 2 * selv };
    }
    function coDraw(r, mult, extra, selv, round, real) {
      var n = r.total, x0 = 14, W = 292, y = 56, h = 70, u = W / n, g = "";
      var seg = function (x, w, col) { return '<rect x="' + x.toFixed(2) + '" y="' + y + '" width="' + Math.max(0.5, w).toFixed(2) + '" height="' + h + '" fill="' + col + '"/>'; };
      var x = x0;
      if (r.b) { g += seg(x, r.b * u, "#2f8f8a"); x += r.b * u; }
      if (selv) { g += seg(x, selv * u, "#f4a823"); x += selv * u; }
      for (var i = 0; i < r.reps; i++) { g += seg(x, mult * u, i % 2 ? "#d9668f" : "#b8326a"); x += mult * u; }
      if (extra) { g += seg(x, extra * u, "#e9a3bd"); x += extra * u; }
      if (selv) { g += seg(x, selv * u, "#f4a823"); x += selv * u; }
      if (r.b) { g += seg(x, r.b * u, "#2f8f8a"); }
      var vs = "", step = Math.max(u, 6), cx;
      for (cx = x0 + step / 2; cx < x0 + W; cx += step) vs += '<path d="M' + (cx - 2.4).toFixed(1) + " " + (y + 10) + " l2.4 6 l2.4 -6" + '" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.3"/>';
      coEl.svg.innerHTML = '<line x1="6" x2="314" y1="' + (y - 8) + '" y2="' + (y - 8) + '" stroke="#8a6e55" stroke-width="5" stroke-linecap="round"/><circle cx="312" cy="' + (y - 8) + '" r="6" fill="#1f2a44"/>' +
        '<text x="160" y="24" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2a44">' + n + " stitches" + (round ? " joined in the round" : "") + "</text>" + g + vs +
        '<rect x="' + x0 + '" y="' + y + '" width="' + W + '" height="' + h + '" fill="none" stroke="#1f2a44" stroke-width="2"/>' +
        '<line x1="' + x0 + '" x2="' + (x0 + W) + '" y1="' + (y + h + 16) + '" y2="' + (y + h + 16) + '" stroke="#1f2a44" stroke-width="1.5"/>' +
        '<line x1="' + x0 + '" x2="' + x0 + '" y1="' + (y + h + 10) + '" y2="' + (y + h + 22) + '" stroke="#1f2a44" stroke-width="1.5"/><line x1="' + (x0 + W) + '" x2="' + (x0 + W) + '" y1="' + (y + h + 10) + '" y2="' + (y + h + 22) + '" stroke="#1f2a44" stroke-width="1.5"/>' +
        '<text x="160" y="163" text-anchor="middle" font-size="12" font-weight="700" fill="#1f2a44">about ' + c1(real) + " in " + (round ? "around" : "wide") + "</text>";
    }
    function coCalc() {
      var custom = coEl.what.value === "custom"; coEl.custom.hidden = !custom;
      var width, round;
      if (custom) { width = Math.min(240, Math.max(1, (parseFloat(coEl.w.value) || 0) / (coEl.wu.value === "cm" ? 2.54 : 1))); round = coEl.mode.value === "round"; }
      else { var pv = coEl.what.value.split("|"); width = parseFloat(pv[0]) || 8; round = pv[1] === "round"; }
      coEl.flat.hidden = round;
      var pc = coEl.pat.value === "custom"; coEl.rep.hidden = !pc;
      var mult, extra;
      if (pc) { mult = Math.max(1, Math.min(80, parseInt(coEl.m.value, 10) || 1)); extra = Math.max(0, Math.min(40, parseInt(coEl.x.value, 10) || 0)); }
      else { var pp = coEl.pat.value.split("|"); mult = parseInt(pp[0], 10) || 1; extra = parseInt(pp[round ? 2 : 1], 10) || 0; }
      if (round && pc) extra = 0;
      var border = round ? 0 : parseFloat(coEl.b.value) || 0, selv = round ? 0 : parseInt(coEl.s.value, 10) || 0;
      var g = parseFloat(coEl.g.value) || 0, spi = g / (coEl.gu.value === "10" ? 10 / 2.54 : 4);
      if (!(spi > 0)) { coEl.out.innerHTML = '<h3>Cast on</h3><p class="sub">Enter the stitches in your swatch to see the number.</p>'; coEl.svg.innerHTML = ""; return; }
      var r = coCount(width, spi, mult, extra, border, selv), real = r.total / spi;
      var parts = [];
      if (r.b) parts.push(r.b + " border");
      if (selv) parts.push(selv + " edge");
      parts.push(r.reps * mult + extra + " pattern" + (mult > 1 ? " (" + r.reps + " × " + mult + (extra ? " + " + extra : "") + ")" : ""));
      if (selv) parts.push(selv + " edge");
      if (r.b) parts.push(r.b + " border");
      var diff = real - width, tail = r.total * CO_TAIL / spi + 6;
      var out = "<h3>Cast on</h3><div class=\"big\">" + r.total + "</div><p class=\"sub\">stitches at " + c1(spi) + " per inch" + (round ? ", joined in the round" : "") + ".</p>" +
        '<p class="id-line">' + parts.join(" + ") + "</p>" +
        '<div class="bk-dims">' + cBoth(real) + "<small>" + (round ? "around" : "wide") + ", for a target of " + cBoth(width) + (Math.abs(diff) >= 0.1 ? " (" + (diff > 0 ? "+" : "−") + c1(Math.abs(diff)) + " in)" : "") + "</small></div>";
      if (mult > 1 || r.b) {
        var lo = r.reps > 1 ? r.total - mult : 0, hi = r.total + mult;
        out += "<hr><h3>Other numbers that fit</h3><ul class=\"co-alt\">" + (lo ? "<li><strong>" + lo + "</strong> stitches · " + cBoth(lo / spi) + "</li>" : "") + "<li><strong>" + hi + "</strong> stitches · " + cBoth(hi / spi) + "</li></ul>";
      }
      out += "<hr><h3>Long-tail cast on</h3><p>Leave a tail of about <strong>" + cBoth(tail) + "</strong>" + (tail > 72 ? ", that's about " + c1(tail / 36) + " yd" : "") + ". An estimate: wrap the yarn 10 times around the needle to check.</p>";
      var needle;
      if (round) {
        var cables = [9, 12, 16, 24, 32, 40, 47, 60], fit = cables.filter(function (c) { return c <= width; }).pop();
        needle = fit ? "Use a " + fit + " in circular needle (shorter than " + c1(width) + " in around), or magic loop on a longer one." : "This is small: use double-pointed needles or magic loop.";
      } else needle = real > 14 ? "That's wide: use a 32 to 40 in circular needle (longer for big blankets) and knit back and forth." : "Straight needles or a 24 in circular will hold it.";
      out += "<p>" + needle + "</p>";
      out += '<p class="sub">Next: ' + coLink("yarn-calculator", "how much yarn") + ", " + coLink("row-counter", "row counter") + (width >= 30 && !round ? ", " + coLink("blanket-size-calculator", "blanket yarn") : "") + ", " + coLink("gauge-converter", "gauge converter") + ".</p>";
      coEl.out.innerHTML = out;
      coDraw(r, mult, extra, selv, round, real);
      coEl.cap.textContent = "Your cast-on row: " + r.total + " stitches, about " + c1(real) + " in " + (round ? "around" : "wide") + ".";
      var save = {}; coKeys.forEach(function (k) { save[k] = coEl[k].value; }); store.set("pp-caston", save);
    }
    var coWu = coEl.wu.value;
    coEl.wu.addEventListener("change", function () { var v = parseFloat(coEl.w.value); if (v && coWu !== coEl.wu.value) coEl.w.value = Math.round(v * (coEl.wu.value === "cm" ? 2.54 : 1 / 2.54) * 2) / 2; coWu = coEl.wu.value; });
    coEl.g.addEventListener("input", function () { coTouchedG = true; });
    coEl.yarn.addEventListener("change", function () { if (!coTouchedG) { var gv = parseFloat(coEl.yarn.value.split("|")[1]) || 18; coEl.g.value = coEl.gu.value === "10" ? Math.round(gv * 2.5 / 2.54 * 2) / 2 : gv; } });
    coKeys.forEach(function (k) { coEl[k].addEventListener("input", coCalc); coEl[k].addEventListener("change", coCalc); });
    coCalc();
  }
  /* ---- Crochet circle + amigurumi ball calculator ---- */
  if ($("#ci-shape") && $("#ci-out")) {
    var ciEl = {}; ["shape", "flat", "st", "goal", "size-f", "d", "du", "n-f", "n", "n-l", "yarn", "g", "gu", "gnote", "svg", "cap", "key", "out"].forEach(function (k) { ciEl[k] = $("#ci-" + k); });
    var CI_AMI = 1.25; /* amigurumi on a smaller hook: about a quarter more stitches per inch (estimate) */
    var ciKeys = ["st", "d", "du", "n", "yarn", "g", "gu"], ciTouched = false;
    var ciPref = store.get("pp-circle", null);
    if (ciPref) {
      ciKeys.forEach(function (k) { if (ciPref[k] != null && ciPref[k] !== "" && ciEl[k]) ciEl[k].value = ciPref[k]; });
      ["shape", "goal"].forEach(function (k) { if (ciPref[k]) $$("button", ciEl[k]).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === ciPref[k]); }); });
      ciTouched = true;
    }
    var ciLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    var c1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    function ciRep(m, st, inc, s) { return m <= 0 ? inc + " × " + s : "(" + m + " " + st + ", " + inc + ") × " + s; }
    function ciStag(m, st, inc, s) { var a = m - Math.floor(m / 2), b = Math.floor(m / 2); return a + " " + st + ", " + inc + ", (" + m + " " + st + ", " + inc + ") × " + (s - 1) + (b ? ", " + b + " " + st : ""); }
    function ciRound(r, st, s) {
      if (r === 1) return { t: s + " " + st + " in a magic ring", c: s };
      if (r === 2) return { t: "inc × " + s + " (2 " + st + " in every stitch)", c: 2 * s };
      var m = r - 2; return { t: r % 2 === 0 ? ciStag(m, st, "inc", s) : ciRep(m, st, "inc", s), c: s * r };
    }
    function ciBall(n) {
      var out = [], r, k;
      for (r = 1; r <= n; r++) { var x = ciRound(r, "sc", 6); out.push({ k: "inc", r: r, t: x.t, c: x.c }); }
      r = n;
      for (k = 0; k < n; k++) { r++; out.push({ k: "even", r: r, t: "sc in each stitch", c: 6 * n }); }
      for (k = n - 1; k >= 1; k--) { r++; var m = k - 1; out.push({ k: "dec", r: r, t: (m && k % 2 === 0) ? ciStag(m, "sc", "dec", 6) : ciRep(m, "sc", "dec", 6), c: 6 * k }); }
      return out;
    }
    var CI_COL = { inc: "#b8326a", even: "#2f8f8a", dec: "#f4a823" };
    function ciDrawFlat(n, s, spi) {
      var R = 118, cx = 160, cy = 130, g = "", pal = ["#b8326a", "#f4a823", "#2f8f8a", "#1f2a44", "#e07a9f"], step = R / n;
      for (var r = n; r >= 1; r--) {
        g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r * step).toFixed(2) + '" fill="' + pal[(r - 1) % 5] + '" stroke="#fbfcfa" stroke-width="' + (n > 30 ? 0.4 : 1) + '"/>';
      }
      if (n <= 30) for (r = 2; r <= n; r++) {
        var off = (r >= 4 && r % 2 === 0) ? Math.PI / s : 0;
        for (var i = 0; i < s; i++) {
          var a = off + i * 2 * Math.PI / s - Math.PI / 2, rr = (r - 0.5) * step;
          g += '<circle cx="' + (cx + rr * Math.cos(a)).toFixed(1) + '" cy="' + (cy + rr * Math.sin(a)).toFixed(1) + '" r="' + Math.max(1, Math.min(3, step * 0.28)).toFixed(1) + '" fill="#fbfcfa"/>';
        }
      }
      ciEl.svg.innerHTML = g;
      ciEl.key.innerHTML = '<li><i style="background:#b8326a"></i>Rounds, one colour each</li>' + (n <= 30 ? '<li><i style="background:#fbfcfa;border:1px solid #1f2a44"></i>Where the increases sit</li>' : "");
    }
    function ciDrawBall(rows) {
      var max = 0; rows.forEach(function (x) { if (x.c > max) max = x.c; });
      var H = 230, rh = H / rows.length, g = "";
      rows.forEach(function (x, i) {
        var w = Math.max(10, 240 * Math.sin(Math.PI * (i + 0.5) / rows.length)), y = 15 + i * rh;
        g += '<rect x="' + (160 - w / 2).toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + Math.max(1, rh - 1).toFixed(1) + '" rx="' + Math.min(6, rh / 2).toFixed(1) + '" fill="' + CI_COL[x.k] + '"/>';
      });
      ciEl.svg.innerHTML = g;
      ciEl.key.innerHTML = '<li><i style="background:#b8326a"></i>Increase rounds</li><li><i style="background:#2f8f8a"></i>Even rounds</li><li><i style="background:#f4a823"></i>Decrease rounds</li>';
    }
    function ciList(rows, flatSt) {
      return '<ol class="ci-list">' + rows.map(function (x) { return "<li><b>R" + x.r + "</b> " + esc(x.t) + ' <span class="ci-c">' + x.c + "</span></li>"; }).join("") + "</ol>";
    }
    function ciCalc() {
      var shape = segVal(ciEl.shape) || "flat", goal = segVal(ciEl.goal) || "size", ball = shape === "ball";
      ciEl.flat.hidden = ball; ciEl["size-f"].hidden = goal !== "size"; ciEl["n-f"].hidden = goal === "size";
      ciEl["n-l"].textContent = ball ? "Increase rounds" : "Rounds";
      var sp = ciEl.st.value.split("|"), st = ball ? "sc" : sp[0], s = ball ? 6 : parseInt(sp[1], 10) || 6;
      var g = parseFloat(ciEl.g.value) || 0, spi = g / (ciEl.gu.value === "10" ? 10 / 2.54 : 4);
      if (!(spi > 0)) { ciEl.out.innerHTML = "<h3>Your circle</h3><p class=\"sub\">Enter the stitches in your swatch to start.</p>"; ciEl.svg.innerHTML = ""; return; }
      var D = (parseFloat(ciEl.d.value) || 0) / (ciEl.du.value === "cm" ? 2.54 : 1), n, maxN = ball ? 25 : 60;
      if (goal === "size") n = Math.round(D * Math.PI * spi / s);
      else n = parseInt(ciEl.n.value, 10) || 1;
      n = Math.max(ball ? 2 : 1, Math.min(maxN, n));
      var last = s * n, real = last / (Math.PI * spi), out, rows, txt;
      var dims = '<div class="bk-dims">' + c1(real) + " in (" + Math.round(real * 2.54) + " cm)<small>across, our estimate" + (goal === "size" && D > 0 ? ", for a target of " + c1(D) + " in" : "") + "</small></div>";
      if (!ball) {
        rows = []; for (var r = 1; r <= n; r++) { var x = ciRound(r, st, s); rows.push({ r: r, t: x.t, c: x.c }); }
        var tot = s * n * (n + 1) / 2;
        out = "<h3>Flat circle in " + esc(st) + "</h3><div class=\"big\">" + n + " <small>rounds</small></div><p class=\"sub\">" + last + " stitches in the last round, " + fmt(tot) + " stitches in all.</p>" + dims;
        txt = rows.map(function (x) { return "R" + x.r + ": " + x.t + " (" + x.c + ")"; }).join("\n");
        out += "<hr><h3>Round by round</h3>" + ciList(rows) + '<p class="sub">inc = 2 ' + esc(st) + " in the same stitch. Numbers on the right are the stitches at the end of the round.</p>";
      } else {
        rows = ciBall(n);
        out = "<h3>Amigurumi ball</h3><div class=\"big\">" + rows.length + " <small>rounds</small></div><p class=\"sub\">" + n + " increase, " + n + " even and " + (n - 1) + " decrease rounds in sc, up to " + last + " stitches.</p>" + dims;
        var stuffAt = 0; rows.forEach(function (x) { if (x.k === "dec" && x.c === 18) stuffAt = x.r; });
        txt = rows.map(function (x) { return "R" + x.r + ": " + x.t + " (" + x.c + ")"; }).join("\n");
        out += "<hr><h3>Round by round</h3>" + ciList(rows) + '<p class="sub">inc = 2 sc in one stitch, dec = sc 2 together. ' + (stuffAt ? "Stuff firmly after round " + stuffAt + " (18 stitches), and top up before the last round. " : "Stuff before the last round. ") + "Fasten off and close the last 6 stitches by weaving the tail through the front loops.</p>";
      }
      out += '<p><button type="button" class="btn gold sm" id="ci-copy">Copy the pattern</button></p>';
      out += '<p class="sub">Next: ' + ciLink("row-counter", "count your rounds") + ", " + ciLink("increase-decrease-calculator", "increase evenly") + ", " + ciLink("crochet-terms", "US and UK terms") + ".</p>";
      ciEl.out.innerHTML = out;
      if (ball) ciDrawBall(rows); else ciDrawFlat(n, s, spi);
      ciEl.cap.textContent = ball ? "Side view of your ball, " + rows.length + " rounds, the first at the top, about " + c1(real) + " in across." : "Your circle from above: " + n + " rounds, about " + c1(real) + " in across.";
      var cp = $("#ci-copy"); if (cp) cp.addEventListener("click", function () {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { toast("Copied"); }, function () { toast("Couldn't copy. Select the text instead."); });
        else toast("Select the text to copy it");
      });
      var save = { shape: shape, goal: goal }; ciKeys.forEach(function (k) { save[k] = ciEl[k].value; }); store.set("pp-circle", save);
    }
    function ciDefG() {
      if (ciTouched) return;
      var gv = (parseFloat(ciEl.yarn.value.split("|")[1]) || 12) * (segVal(ciEl.shape) === "ball" ? CI_AMI : 1);
      ciEl.g.value = Math.round((ciEl.gu.value === "10" ? gv * 2.5 / 2.54 : gv) * 2) / 2;
    }
    var ciDu = ciEl.du.value;
    ciEl.du.addEventListener("change", function () { var v = parseFloat(ciEl.d.value); if (v && ciDu !== ciEl.du.value) ciEl.d.value = Math.round(v * (ciEl.du.value === "cm" ? 2.54 : 1 / 2.54) * 2) / 2; ciDu = ciEl.du.value; });
    ciEl.g.addEventListener("input", function () { ciTouched = true; });
    ciEl.yarn.addEventListener("change", ciDefG);
    seg(ciEl.shape, function (v) { if (ciEl.du.value === "in") { if (v === "ball" && ciEl.d.value === "8") ciEl.d.value = 3; else if (v === "flat" && ciEl.d.value === "3") ciEl.d.value = 8; } ciDefG(); ciCalc(); }); seg(ciEl.goal, ciCalc);
    ciKeys.forEach(function (k) { ciEl[k].addEventListener("input", ciCalc); ciEl[k].addEventListener("change", ciCalc); });
    ciCalc();
  }
  /* ---- Granny square blanket calculator ---- */
  if ($("#gs-size") && $("#gs-out")) {
    var gsEl = {}; ["size", "custom", "bw", "bl", "sq", "su", "join", "border", "weight", "ypsq", "skein", "unit", "cols", "out", "svg", "cap"].forEach(function (k) { gsEl[k] = $("#gs-" + k); });
    var gsB = P.blankets || [], gsWts = P.weights || [];
    var GS_YD = 0.9;      /* yd per sq in of a worsted granny square (estimate): 5 in square ~25 yd; whole granny throws land near 1 yd per sq in incl. joins and border */
    var GS_SOLID = 0.85;  /* yd per sq in of solid crochet border in worsted (estimate, as the blanket calculator) */
    var GS_PAL = ["#b8326a", "#f4a823", "#2f8f8a", "#1f2a44", "#e07a9f", "#7fc4bd", "#c9822a", "#6b7aa6", "#9a2456", "#f6cf7a", "#246f6b", "#4a5470"];
    var gsKeys = ["size", "bw", "bl", "sq", "su", "join", "border", "weight", "ypsq", "skein", "unit", "cols"];
    var gsPref = store.get("pp-granny", null);
    if (gsPref) gsKeys.forEach(function (k) { if (gsPref[k] != null && gsPref[k] !== "") gsEl[k].value = gsPref[k]; });
    var r1 = function (n) { return Math.round(n * 10) / 10; };
    function gsSquare(x, y, s, c1, c2) {
      var g = '<rect x="' + x + '" y="' + y + '" width="' + s + '" height="' + s + '" fill="' + c1 + '"/>';
      if (s >= 9) g += '<rect x="' + (x + s * 0.2) + '" y="' + (y + s * 0.2) + '" width="' + s * 0.6 + '" height="' + s * 0.6 + '" fill="none" stroke="' + c2 + '" stroke-width="' + Math.max(1, s * 0.09) + '" stroke-dasharray="' + s * 0.12 + " " + s * 0.06 + '"/>';
      if (s >= 16) g += '<rect x="' + (x + s * 0.4) + '" y="' + (y + s * 0.4) + '" width="' + s * 0.2 + '" height="' + s * 0.2 + '" fill="' + c2 + '"/>';
      return g;
    }
    function gsDraw(cols, rows, nc, bdr, sq, fw, fl) {
      var room = 300, sc = Math.min(room / fw, room / fl), bw = fw * sc, bh = fl * sc, x0 = (320 - bw) / 2, y0 = (320 - bh) / 2;
      var b = bdr * sc, cell = (bw - 2 * b) / cols, cellH = (bh - 2 * b) / rows, s = Math.min(cell, cellH), gap = Math.max(0.6, s * 0.06);
      var g = '<rect x="' + x0 + '" y="' + y0 + '" width="' + bw + '" height="' + bh + '" rx="3" fill="' + (b > 0.5 ? "#f6f1e7" : "none") + '" stroke="#1f2a44" stroke-width="1.5"/>';
      for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {
        var i = (r + c * 2) % nc, j = (i + 1 + (r % 2)) % Math.max(2, nc);
        g += gsSquare(x0 + b + c * cell + gap / 2, y0 + b + r * cellH + gap / 2, s - gap, GS_PAL[i % 12], nc > 1 ? GS_PAL[j % 12] : "#fbfcfa");
      }
      gsEl.svg.innerHTML = g;
      gsEl.cap.textContent = cols + " across × " + rows + " down" + (bdr > 0 ? ", with a " + bdr + " in border" : "") + ". Colours are shuffled for the preview only.";
    }
    function gsCalc() {
      var custom = gsEl.size.value === "custom", b = gsB.filter(function (x) { return x.id === gsEl.size.value; })[0];
      gsEl.custom.hidden = !custom;
      var tw = custom ? Math.min(140, Math.max(6, parseFloat(gsEl.bw.value) || 0)) : (b ? b.w : 50);
      var tl = custom ? Math.min(140, Math.max(6, parseFloat(gsEl.bl.value) || 0)) : (b ? b.l : 60);
      var sq = parseFloat(gsEl.sq.value) || 0; if (gsEl.su.value === "cm") sq = sq / 2.54;
      if (sq < 0.5) { gsEl.out.innerHTML = "<h3>Square size</h3><p>Type the size of one finished square to start.</p>"; return; }
      var jp = gsEl.join.value.split("|"), seam = parseFloat(jp[0]) || 0, jFrac = parseFloat(jp[1]) || 0;
      var bdr = Math.max(0, parseFloat(gsEl.border.value) || 0), nc = Math.min(12, Math.max(1, parseInt(gsEl.cols.value, 10) || 1));
      var fit = function (t) { var room = t - 2 * bdr + seam; return Math.max(1, Math.round(room / (sq + seam))); };
      var cols = fit(tw), rows = fit(tl), n = cols * rows;
      var fw = cols * sq + (cols - 1) * seam + 2 * bdr, fl = rows * sq + (rows - 1) * seam + 2 * bdr;
      var wt = gsWts.filter(function (x) { return String(x.n) === gsEl.weight.value; })[0]; if (!wt) return;
      var mine = parseFloat(gsEl.ypsq.value) || 0, per = mine > 0 ? mine : sq * sq * GS_YD * wt.m;
      var sqYd = per * n, joinYd = sqYd * jFrac, bYd = (fw * fl - (fw - 2 * bdr) * (fl - 2 * bdr)) * GS_SOLID * wt.m, tot = sqYd + joinYd + bYd;
      var spread = mine > 0 ? 0.08 : 0.15, hi = tot * (1 + spread), lo = tot * (1 - spread);
      var skein = parseFloat(gsEl.skein.value) || 0, skYd = gsEl.unit.value === "m" ? skein / 0.9144 : skein;
      var sk = skYd > 0 ? Math.ceil(hi / skYd) : 0;
      var perCol = Math.ceil(n / nc), colYd = per * perCol * (1 + spread), colSk = skYd > 0 ? Math.ceil(colYd / skYd) : 0;
      var diff = function (f, t, big, small) { var d = r1(f - t); return d === 0 ? "exact " + (big === "wider" ? "width" : "length") : (d > 0 ? d + " in " + big : (-d) + " in " + small); };
      gsEl.out.innerHTML = "<h3>Squares to make</h3><div class=\"big\">" + fmt(n) + "</div>" +
        '<p class="sub">' + cols + " across × " + rows + " down, " + r1(sq) + " in (" + r1(sq * 2.54) + " cm) squares.</p>" +
        '<h3>Finished size</h3><div class="bk-dims">' + r1(fw) + " × " + r1(fl) + " in<small>" + Math.round(fw * 2.54) + " × " + Math.round(fl * 2.54) + " cm · " + diff(fw, tw, "wider", "narrower") + ", " + diff(fl, tl, "longer", "shorter") + " than " + tw + " × " + tl + " in</small></div>" +
        "<p>Yarn, about <strong>" + fmt(lo) + "–" + fmt(hi) + " yards</strong> (" + fmt(lo * 0.9144) + "–" + fmt(hi * 0.9144) + " m) of weight " + wt.n + " " + esc(wt.name.toLowerCase()) + ":</p>" +
        '<p class="sub">Squares ' + fmt(sqYd) + " yd (" + r1(per) + " yd each" + (mine > 0 ? ", your figure" : ", our estimate") + ")<br>Joining " + fmt(joinYd) + " yd<br>Border " + fmt(bYd) + " yd</p>" +
        (sk ? "<h3>Skeins to buy</h3><div class=\"big\">" + sk + "</div>" : '<p class="sub">Enter the length per skein to see how many to buy.</p>') +
        (nc > 1 ? '<p class="sub">With ' + nc + " colours: about " + perCol + " squares each, roughly " + fmt(colYd) + " yd" + (colSk ? " (" + colSk + " skein" + (colSk > 1 ? "s" : "") + ")" : "") + " per colour, plus " + fmt((joinYd + bYd) * (1 + spread)) + " yd for joining and border in your main colour.</p>" : "") +
        '<hr><p class="sub">Yarn amounts are estimates. Buy from one dye lot and keep a spare skein of the joining colour.</p>';
      gsDraw(cols, rows, nc, bdr, sq, fw, fl);
      var sv = {}; gsKeys.forEach(function (k) { sv[k] = gsEl[k].value; }); store.set("pp-granny", sv);
    }
    gsKeys.forEach(function (k) { gsEl[k].addEventListener("input", gsCalc); gsEl[k].addEventListener("change", gsCalc); });
    gsCalc();
  }
  /* ---- Increase / decrease evenly calculator (same maths as spacing() in build.py) ---- */
  if ($("#id-s") && $("#id-out")) {
    var idE = {}; ["craft", "dir", "s", "n", "n-l", "target", "way", "kind", "kind-f", "stag", "stag-f", "svg", "cap", "out"].forEach(function (k) { idE[k] = $("#id-" + k); });
    var idPref = store.get("pp-incdec", null);
    var idSetSeg = function (el, v) { $$("button", el).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === v); }); };
    if (idPref) { idSetSeg(idE.craft, idPref.craft); idSetSeg(idE.dir, idPref.dir); idSetSeg(idE.way, idPref.way); if (idPref.s) idE.s.value = idPref.s; if (idPref.n) idE.n.value = idPref.n; }
    function idPlan(S, N, use, flat) {
      if (N < 1 || S < 1 || N * Math.max(use, 1) > S) return null;
      var p = [], i; for (i = 0; i < N; i++) p.push(Math.floor((i + 1) * S / N) - Math.floor(i * S / N) - use);
      if (!flat) return { t: p, tail: 0 };
      var last = p[p.length - 1], a = Math.floor(last / 2);
      return { t: [a].concat(p.slice(0, -1)), tail: last - a };
    }
    function idText(pl, knit, act) {
      var unit = function (n) { return knit ? "K" + n : n + " sc"; };
      var tok = function (n) { return (n ? unit(n) + ", " : "") + act; };
      var t = pl.t, out = [], i = 0;
      while (i < t.length) {
        var bp = 1, bc = 1;
        for (var per = 1; per <= 3; per++) {
          var c = 1;
          while (i + (c + 1) * per <= t.length && t.slice(i + c * per, i + (c + 1) * per).join() === t.slice(i, i + per).join()) c++;
          if (c >= 2 && c * per > bp * bc && !(bc >= 2 && per > bp)) { bp = per; bc = c; }
        }
        var blk = t.slice(i, i + bp).map(tok).join(", ");
        out.push(bc === 1 ? blk : (knit ? "[" + blk + "] " : "(" + blk + ") ") + bc + " times");
        i += bp * bc;
      }
      if (pl.tail) out.push(unit(pl.tail));
      return out.join(", ");
    }
    function idDraw(pl, use, S, dec) {
      var per = 30, cw = 320 / per, seq = [], i, j;
      pl.t.forEach(function (n) { for (j = 0; j < n; j++) seq.push(0); seq.push(use === 0 ? 3 : (dec ? 2 : 1)); });
      for (j = 0; j < pl.tail; j++) seq.push(0);
      var cells = [];  /* each old stitch is a cell; type 3 = M1 marker drawn between cells */
      seq.forEach(function (k) { if (k === 3) { if (cells.length) cells[cells.length - 1].m1 = true; else cells.push({ k: -1, m1: true }); } else if (k === 2) { cells.push({ k: 2 }); cells.push({ k: 2, second: true }); } else cells.push({ k: k }); });
      cells = cells.filter(function (c) { return c.k !== -1 || c.m1; });
      var shown = Math.min(cells.length, 360), rows = Math.ceil(shown / per), h = Math.max(40, rows * 26 + 12), g = "";
      for (i = 0; i < shown; i++) {
        var c = cells[i], x = (i % per) * cw + cw / 2, y = Math.floor(i / per) * 26 + 20;
        if (c.k === -1) { g += '<circle cx="' + (x - cw / 2) + '" cy="' + y + '" r="3.4" fill="#b8326a"/>'; continue; }
        var col = c.k === 2 ? "#2f8f8a" : c.k === 1 ? "#b8326a" : "#1f2a44";
        g += '<path d="M' + (x - cw * 0.34) + " " + (y - 8) + "L" + x + " " + (y + 7) + "L" + (x + cw * 0.34) + " " + (y - 8) + '" fill="none" stroke="' + col + '" stroke-width="' + (c.k ? 2.4 : 1.5) + '" stroke-linecap="round" stroke-linejoin="round"/>';
        if (c.k === 2 && !c.second) g += '<path d="M' + (x - cw * 0.4) + " " + (y + 10) + "Q" + (x + cw / 2) + " " + (y + 16) + " " + (x + cw * 1.4) + " " + (y + 10) + '" fill="none" stroke="#2f8f8a" stroke-width="1.6"/>';
        if (c.m1) g += '<circle cx="' + (x + cw / 2) + '" cy="' + y + '" r="3.4" fill="#b8326a"/>';
      }
      idE.svg.setAttribute("viewBox", "0 0 320 " + h); idE.svg.innerHTML = g;
      idE.cap.textContent = "Each V is a stitch you have now. " + (dec ? "Teal pairs are worked together." : use === 0 ? "Berry dots are the new stitches made between." : "Berry stitches are the ones you increase into.") + (cells.length > shown ? " Showing the first " + shown + " stitches." : "");
    }
    function idCalc() {
      var knit = segVal(idE.craft) === "knit", dec = segVal(idE.dir) === "dec", flat = segVal(idE.way) === "flat";
      var S = parseInt(idE.s.value, 10) || 0, N = parseInt(idE.n.value, 10) || 0;
      idE["kind-f"].hidden = !knit || dec; idE["stag-f"].hidden = flat;
      idE["n-l"].textContent = dec ? "How many to decrease" : "How many to increase";
      var use = dec ? 2 : (knit && idE.kind.value === "m1" ? 0 : 1);
      var act = dec ? (knit ? "k2tog" : "dec") : (knit ? (use ? "kfb" : "M1") : "inc");
      idE.target.textContent = S > 0 && N > 0 ? "You'll end with " + (dec ? S - N : S + N) + " stitches." : "";
      var pl = idPlan(S, N, use, flat || idE.stag.checked);
      if (!pl) {
        idE.out.innerHTML = "<h3>Check the numbers</h3><p>" + (S < 1 || N < 1 ? "Type the stitches you have and how many to change." : dec ? "Each decrease uses two stitches, so " + S + " stitches allow at most " + Math.floor(S / 2) + " decreases in one row." : "That's more increases than stitches. Spread them over two rows, or increase twice into some stitches.") + "</p>";
        idE.svg.innerHTML = ""; idE.cap.textContent = ""; return;
      }
      var rp = idPlan(S, N, use, false), line = idText(pl, knit, act), lo = Math.min.apply(null, rp.t), hi = Math.max.apply(null, rp.t);
      idE.out.innerHTML = "<h3>" + (flat ? "Your row" : "Your round") + '</h3><p class="id-line" id="id-line">' + esc(line) + "</p>" +
        '<button type="button" class="btn gold sm" id="id-copy">Copy instruction</button>' +
        "<h3 style=\"margin-top:18px\">Stitch count</h3><div class=\"big\">" + S + "<small> → </small>" + (dec ? S - N : S + N) + "</div>" +
        '<p class="sub">' + N + " " + (dec ? "decreases" : "increases") + ", " + (lo === hi ? "every " + (lo + use) + " stitches" : "every " + (lo + use) + " or " + (hi + use) + " stitches") + (flat ? ", with half a gap at each edge." : idE.stag.checked ? ", starting halfway into a repeat." : ".") + "</p>" +
        '<p class="sub">' + (knit ? (dec ? "k2tog = knit 2 together." : use ? "kfb = knit into the front and back of the same stitch." : "M1 = make one: lift the bar between stitches and knit into the back of it.") + (flat ? " On a purl row, purl the plain stitches (p2tog or M1P for the shaping)." : "") : (dec ? "dec = sc2tog (or an invisible decrease)." : "inc = 2 sc in the same stitch.") + " Using hdc or dc? Swap sc for your stitch.") + "</p>" +
        '<hr><p class="sub">Next: <a href="' + (location.protocol === "file:" ? "row-counter.html" : "/row-counter") + '" style="color:#f4a823">count the rows</a> or <a href="' + (location.protocol === "file:" ? "gauge-converter.html" : "/gauge-converter") + '" style="color:#f4a823">check your gauge</a>.</p>';
      var cp = $("#id-copy"); if (cp) cp.addEventListener("click", function () {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(line).then(function () { toast("Copied"); }, function () { toast("Couldn't copy. Select the text instead."); });
        else toast("Select the text to copy it");
      });
      idDraw(pl, use, S, dec);
      store.set("pp-incdec", { craft: knit ? "knit" : "crochet", dir: dec ? "dec" : "inc", way: flat ? "flat" : "round", s: S, n: N });
    }
    [idE.craft, idE.dir, idE.way].forEach(function (el) { seg(el, idCalc); });
    [idE.s, idE.n, idE.kind, idE.stag].forEach(function (el) { el.addEventListener("input", idCalc); el.addEventListener("change", idCalc); });
    idCalc();
  }
  /* ---- Crochet / knitting price calculator ---- */
  if ($("#pr-m") && $("#pr-out")) {
    var prE = {}; ["m", "h", "r", "oh", "ch", "fair", "bf", "bn", "cf", "con", "cp", "try", "out"].forEach(function (k) { prE[k] = $("#pr-" + k); });
    var prKeys = ["m", "h", "r", "oh", "ch", "bf", "bn", "cf", "cp"], prPref = store.get("pp-price", null);
    if (prPref) prKeys.forEach(function (k) { if (prPref[k] != null && prPref[k] !== "") prE[k].value = prPref[k]; });
    var money = function (n) { return "$" + (Math.round(n * 100) / 100).toFixed(2); };
    var num = function (el) { return Math.max(0, parseFloat(el.value) || 0); };
    function prCalc() {
      var m = num(prE.m), h = num(prE.h), r = num(prE.r), oh = num(prE.oh) / 100, ch = prE.ch.value;
      prE.fair.hidden = ch !== "fair"; prE.con.hidden = ch !== "consign";
      var labour = h * r, base = (m + labour) * (1 + oh), pct = 0, fix = 0, extra = 0, note = "";
      if (ch === "etsy") { pct = 0.095; fix = 0.45; note = "Etsy US fees: 6.5% transaction + 3% and $0.25 processing + $0.20 listing. Offsite Ads sales cost 12–15% more."; }
      else if (ch === "fair") { pct = num(prE.cf) / 100; extra = num(prE.bf) / Math.max(1, parseInt(prE.bn.value, 10) || 1); note = "Includes " + money(extra) + " of the table fee per item and the card reader fee."; }
      else if (ch === "consign") { pct = Math.min(0.8, num(prE.cp) / 100); note = "The shop keeps " + Math.round(pct * 100) + "%, so the price is raised to leave you the full amount."; }
      else note = "No fees, so you keep the whole price.";
      var price = (base + extra + fix) / (1 - pct), fees = price * pct + fix;
      var nice = price < 20 ? Math.ceil(price) : Math.ceil(price / 5) * 5;
      var x3 = m * 3, t = parseFloat(prE.try.value) || 0, tryHtml = "";
      if (t > 0) {
        var keep = t * (1 - pct) - fix - extra, perHr = h > 0 ? (keep - m * (1 + oh)) / h / (1 + oh) : 0;
        tryHtml = '<hr><h3>At ' + money(t) + "</h3><p>You'd keep about <strong>" + money(Math.max(0, keep)) + "</strong>, which pays you about <strong>" + money(Math.max(0, perHr)) + " an hour</strong>" + (perHr < r ? " (below your " + money(r) + " rate)." : ".") + "</p>";
      }
      prE.out.innerHTML = "<h3>Price to charge</h3><div class=\"big\">" + money(price) + "</div>" +
        '<p class="sub">Round it to about <strong>' + money(nice) + "</strong>. " + esc(note) + "</p>" +
        '<p class="sub">Materials ' + money(m) + "<br>Your time " + money(labour) + " (" + h + " h × " + money(r) + ")<br>Overheads " + money(base - m - labour) + (extra ? "<br>Table fee share " + money(extra) : "") + (fees > 0.004 ? "<br>Fees about " + money(fees) : "") + "</p>" +
        '<p class="sub">Wholesale to a shop that resells: about ' + money(base) + ". Materials × 3 would say " + money(x3) + (h > 0 ? ", which pays " + money(Math.max(0, (x3 - m) / h)) + " an hour." : ".") + "</p>" + tryHtml +
        '<hr><p class="sub">Shipping is extra: charge what posting costs you. Fees are estimates; check your platform. Next: <a href="' + (location.protocol === "file:" ? "projects.html" : "/projects") + '" style="color:#f4a823">log the hours in the project tracker</a>.</p>';
      var sv = {}; prKeys.forEach(function (k) { sv[k] = prE[k].value; }); store.set("pp-price", sv);
    }
    prKeys.concat(["try"]).forEach(function (k) { prE[k].addEventListener("input", prCalc); prE[k].addEventListener("change", prCalc); });
    prCalc();
  }
  /* ---- Yarn substitution calculator ---- */
  if ($("#ys-n") && $("#ys-out")) {
    var ysE = {}; ["n", "pw", "pl", "pu", "pg", "ml", "mu", "mg", "mw", "out"].forEach(function (k) { ysE[k] = $("#ys-" + k); });
    var ysKeys = ["n", "pw", "pl", "pu", "pg", "ml", "mu", "mg", "mw"], ysPref = store.get("pp-subst", null);
    if (ysPref) ysKeys.forEach(function (k) { if (ysPref[k] != null && ysPref[k] !== "") ysE[k].value = ysPref[k]; });
    var WN = {}; (P.weights || []).forEach(function (w) { WN[w.n] = w.name + " (" + String(w.also || "").split(",")[0] + ")"; });
    var DBL = { 1: [2, 3], 2: [4], 3: [4], 4: [5] };
    function ysCalc() {
      var n = Math.max(0, parseFloat(ysE.n.value) || 0), pl = Math.max(0, parseFloat(ysE.pl.value) || 0), ml = Math.max(0, parseFloat(ysE.ml.value) || 0);
      var plm = ysE.pu.value === "yd" ? pl * 0.9144 : pl, mlm = ysE.mu.value === "yd" ? ml * 0.9144 : ml;
      var st = parseInt(segVal($("#ys-st")), 10) || 1, sp = segVal($("#ys-sp"));
      var pg = parseFloat(ysE.pg.value) || 0, mg = parseFloat(ysE.mg.value) || 0, pw = parseInt(ysE.pw.value, 10), mw = parseInt(ysE.mw.value, 10);
      if (!n || !plm || !mlm) { ysE.out.innerHTML = "<h3>Balls of your yarn</h3><div class=\"big\">–</div><p class=\"sub\">Enter the number of balls and the length per ball from both labels.</p>"; return; }
      var totM = n * plm, needM = totM * st, exact = needM / mlm, base = Math.ceil(exact - 1e-9), buy = base;
      if (sp === "10") buy = Math.ceil(exact * 1.1 - 1e-9); else if (sp === "ball") buy = base + 1;
      var icons = ""; for (var i = 0; i < Math.min(buy, 40); i++) icons += ball(i < base ? "#b8326a" : "#2f8f8a", i >= base, i);
      var tips = [];
      if (st === 2) {
        var ok = DBL[mw] || [];
        tips.push(ok.indexOf(pw) >= 0 ? "Two strands of " + esc(WN[mw]) + " usually work like " + esc(WN[pw]) + ". Swatch to be sure." :
          "Two strands of " + esc(WN[mw]) + " aren't a usual match for " + esc(WN[pw]) + " yarn. Swatch carefully, or pick a different yarn.");
      } else if (pw === mw) tips.push("Same yarn weight: " + pw + " " + esc(WN[pw]) + ". Good start: now swatch for gauge.");
      else tips.push("Different yarn weights (" + pw + " vs " + mw + "). Your gauge and size will change unless you rework the pattern.");
      if (pg > 0 && mg > 0) {
        var pd = plm / pg * 100, md = mlm / mg * 100 / st, r = md / pd;
        var txt = "Length per 100 g: pattern " + fmt(pd) + " m, yours " + fmt(md) + " m" + (st === 2 ? " (held double)" : "") + ". ";
        if (Math.abs(r - 1) <= 0.1) txt += "Very close, so the thickness is likely a good match.";
        else if (r > 1) txt += (r <= 1.25 ? "Yours is a little thinner. " : "Yours is much thinner. ") + "Expect more stitches per 10 cm.";
        else txt += (r >= 0.8 ? "Yours is a little thicker. " : "Yours is much thicker. ") + "Expect fewer stitches per 10 cm.";
        tips.push(txt + " (Dense fibres like cotton have less length per gram at the same thickness.)");
      }
      var grams = mg > 0 ? " Buying " + buy + " balls is about " + fmt(buy * mg) + " g." : "";
      ysE.out.innerHTML = "<h3>Balls of your yarn to buy</h3><div class=\"big\">" + buy + "</div>" +
        '<div class="balls" aria-hidden="true">' + icons + "</div>" +
        "<p>The pattern uses about <strong>" + fmt(totM) + " m</strong> (" + fmt(totM / 0.9144) + " yd)" + (st === 2 ? ", so held double you need <strong>" + fmt(needM) + " m</strong>" : "") + ". That's " + (Math.abs(exact - base) < 0.05 ? "exactly " + base + " balls of yours" : (Math.round(exact * 10) / 10) + " balls of yours, rounded up to " + base) + (buy > base ? ", plus spare" : "") + "." + grams + "</p>" +
        (buy > base ? '<p class="sub">The teal balls are your spare.</p>' : "") +
        "<hr>" + tips.map(function (t) { return '<p class="sub">' + t + "</p>"; }).join("") +
        '<p class="sub">Buy every ball from the same dye lot. These are estimates; your tension can change how much you use.</p>';
      var sv = {}; ysKeys.forEach(function (k) { sv[k] = ysE[k].value; }); store.set("pp-subst", sv);
    }
    ysKeys.forEach(function (k) { ysE[k].addEventListener("input", ysCalc); ysE[k].addEventListener("change", ysCalc); });
    seg($("#ys-st"), ysCalc); seg($("#ys-sp"), ysCalc);
    ysCalc();
  }
  /* ---- Tea stain shade tester ---- */
  if ($("#ts-svg") && $("#ts-out")) {
    var tsSvg = $("#ts-svg"), tsOut = $("#ts-out"), tsSeed = 7;
    var TEA = {
      black: { name: "black tea", c: ["#ead6ae", "#d8b47e", "#bf8f56"], bags: ["1 bag", "3 bags", "5 bags"], note: "The classic warm, golden brown." },
      green: { name: "green tea", c: ["#ece6bf", "#ddd398", "#c8bb72"], bags: ["2 bags", "4 bags", "6 bags"], note: "Paler and yellow-green. Needs more bags than black tea." },
      coffee: { name: "instant coffee", c: ["#dfc6a2", "#c09a6b", "#906a44"], bags: ["½ tsp", "1 tsp", "2 tsp"], note: "Darker and browner than tea." },
      herbal: { name: "herbal or fruit tea", c: ["#e8d2cb", "#d2b1ad", "#b49795"], bags: ["2 bags", "4 bags", "6 bags"], note: "Unpredictable: reds can dry grey or green. Test a scrap first." }
    };
    function rnd() { tsSeed = (tsSeed * 16807) % 2147483647; return (tsSeed - 1) / 2147483646; }
    function mix(a, b, t) { var x = parseInt(a.slice(1), 16), y = parseInt(b.slice(1), 16), o = "#"; [16, 8, 0].forEach(function (s) { var v = Math.round(((x >> s) & 255) * (1 - t) + ((y >> s) & 255) * t); o += ("0" + v.toString(16)).slice(-2); }); return o; }
    function tsDraw() {
      var tea = TEA[$("#ts-tea").value] || TEA.black, s = (parseInt(segVal($("#ts-str")), 10) || 2) - 1, coats = parseInt(segVal($("#ts-coats")), 10) || 1, how = $("#ts-how").value;
      var col = tea.c[s], dark = mix(col, "#5a3a1c", 0.18 + 0.08 * coats), main = coats > 1 ? mix(col, dark, (coats - 1) * 0.35) : col;
      var start = tsSeed; var W = 260, H = 340, x0 = 20, y0 = 20, edge = "";
      if ($("#ts-torn").checked) {
        var pts = [], i;
        for (i = 0; i <= 26; i++) pts.push([x0 + W * i / 26, y0 + rnd() * 5]);
        for (i = 1; i <= 34; i++) pts.push([x0 + W - rnd() * 5, y0 + H * i / 34]);
        for (i = 25; i >= 0; i--) pts.push([x0 + W * i / 26, y0 + H - rnd() * 5]);
        for (i = 33; i >= 1; i--) pts.push([x0 + rnd() * 5, y0 + H * i / 34]);
        edge = "M" + pts.map(function (p) { return p[0].toFixed(1) + " " + p[1].toFixed(1); }).join("L") + "Z";
      } else edge = "M" + x0 + " " + y0 + "h" + W + "v" + H + "h-" + W + "Z";
      var g = '<defs><clipPath id="ts-clip"><path d="' + edge + '"/></clipPath><radialGradient id="ts-v" cx="50%" cy="50%" r="70%"><stop offset=".55" stop-color="' + dark + '" stop-opacity="0"/><stop offset="1" stop-color="' + dark + '" stop-opacity="' + (how === "dip" ? 0.85 : 0.5) + '"/></radialGradient></defs>';
      g += '<rect x="0" y="0" width="300" height="380" fill="#f3efe6"/><path d="' + edge + '" fill="#000" opacity=".12" transform="translate(4 5)"/>';
      g += '<g clip-path="url(#ts-clip)"><rect x="0" y="0" width="300" height="380" fill="' + main + '"/>';
      var k, n;
      if (how === "brush") for (k = 0; k < 7; k++) g += '<rect x="-20" y="' + (rnd() * 360) + '" width="340" height="' + (14 + rnd() * 30) + '" fill="' + dark + '" opacity="' + (0.08 + rnd() * 0.12) + '" transform="rotate(' + (-8 + rnd() * 16) + ' 150 190)"/>';
      if (how === "dab") for (k = 0; k < 16; k++) g += '<ellipse cx="' + (x0 + rnd() * W) + '" cy="' + (y0 + rnd() * H) + '" rx="' + (16 + rnd() * 26) + '" ry="' + (12 + rnd() * 20) + '" fill="' + dark + '" opacity="' + (0.1 + rnd() * 0.18) + '"/>';
      if (how === "pour") for (k = 0; k < 4; k++) { var cx = x0 + rnd() * W, cy = y0 + rnd() * H, r = 30 + rnd() * 50; g += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + r + '" ry="' + r * 0.7 + '" fill="' + dark + '" opacity=".14" stroke="' + dark + '" stroke-width="2.5" stroke-opacity=".5"/>'; }
      if ($("#ts-crumple").checked) for (k = 0; k < 9; k++) { var ax = x0 + rnd() * W, ay = y0 + rnd() * H; g += '<path d="M' + ax + " " + ay + "l" + (rnd() * 120 - 60) + " " + (rnd() * 120 - 60) + "l" + (rnd() * 80 - 40) + " " + (rnd() * 80 - 40) + '" fill="none" stroke="' + dark + '" stroke-width="' + (1 + rnd() * 1.5) + '" opacity=".45"/>'; }
      if ($("#ts-spots").checked) for (k = 0; k < 40; k++) g += '<circle cx="' + (x0 + rnd() * W) + '" cy="' + (y0 + rnd() * H) + '" r="' + (0.8 + rnd() * 2.6) + '" fill="' + mix(dark, "#3a220e", 0.5) + '" opacity="' + (0.4 + rnd() * 0.5) + '"/>';
      if ($("#ts-ring").checked) { var rx = 70 + rnd() * 160, ry = 80 + rnd() * 200; g += '<circle cx="' + rx + '" cy="' + ry + '" r="38" fill="none" stroke="' + dark + '" stroke-width="4" opacity=".55" stroke-dasharray="70 6 40 4"/>'; }
      g += '<rect x="0" y="0" width="300" height="380" fill="url(#ts-v)"/>';
      for (n = 0; n < 7; n++) g += '<line x1="46" x2="254" y1="' + (210 + n * 20) + '" y2="' + (210 + n * 20) + '" stroke="#5b6f8a" stroke-opacity=".28" stroke-width="1"/>';
      g += "</g>";
      tsSvg.innerHTML = g; tsSeed = start;
      var str = ["light", "medium", "strong"][s], water = tea === TEA.coffee ? "1 cup of hot water" : "½ cup of hot water";
      var method = { brush: "Brush or sponge it on, letting some tea pool.", dip: "Lay the sheet in a shallow tray of tea for a few minutes; lift it with both hands.", dab: "Squeeze the wet tea bag and press it all over the page.", pour: "Pour a little onto a rimmed baking sheet, press the paper in, wait 2 minutes and lift." }[how];
      tsOut.innerHTML = "<h3>Your recipe</h3><div class=\"big\" style=\"font-size:2.4rem\">" + esc(tea.bags[s]) + "</div>" +
        "<p>of " + esc(tea.name) + " in " + water + " for a " + str + " shade. Steep about 5 minutes and let it cool a little.</p>" +
        '<ol class="sk-steps"><li>' + method + "</li>" + (coats > 1 ? "<li>Let it dry, then add " + (coats - 1) + " more coat" + (coats > 2 ? "s" : "") + ".</li>" : "") +
        ($("#ts-spots").checked ? "<li>While damp, sprinkle a pinch of instant tea or coffee; brush the grains off when dry.</li>" : "") +
        ($("#ts-ring").checked ? "<li>Stand a wet mug on the page while it dries.</li>" : "") +
        ($("#ts-crumple").checked ? "<li>Crumple the sheet before staining so tea gathers in the creases.</li>" : "") +
        ($("#ts-torn").checked ? "<li>Rub or tear the edges while they're still wet.</li>" : "") +
        "<li>Dry flat, pressed under books, or about 5 minutes in a 200°F (95°C) oven on a tray, watching it.</li></ol>" +
        '<hr><p class="sub">' + esc(tea.note) + " Colours on screen are only a guide.</p>";
    }
    ["#ts-tea", "#ts-how", "#ts-spots", "#ts-ring", "#ts-crumple", "#ts-torn"].forEach(function (s) { $(s).addEventListener("change", tsDraw); });
    seg($("#ts-str"), tsDraw); seg($("#ts-coats"), tsDraw);
    $("#ts-again").addEventListener("click", function () { tsSeed = 1 + Math.floor(Math.random() * 100000); tsDraw(); });
    tsDraw();
  }
  /* ---------- KNITTING ABBREVIATIONS ---------- */
  if (page === "knitting-abbreviations" && $("#ka-in") && window.KA) {
    var KM = {}, KMULTI = [];
    window.KA.forEach(function (r) { KM[r[0]] = r; if (r[0].indexOf(" ") > 0) KMULTI.push(r[0]); });
    KMULTI.sort(function (a, b) { return b.length - a.length; });
    var kaRe = new RegExp("\\b(" + KMULTI.map(function (m) { return m.replace(/ /g, "\\s+"); }).join("|") + ")\\b|\\*|[A-Za-z][A-Za-z0-9&]*(?:'d)?", "gi");
    var UNIT = { "in": 1, "m": 1, "g": 1, "oz": 1, "cm": 1, "mm": 1, "yd": 1, "yds": 1 };
    function kaDecode(txt) {
      var found = [], seen = {};
      var add = function (key, d, s, l) { if (seen[key]) return; seen[key] = 1; found.push([d, s, l]); };
      var out = txt.replace(kaRe, function (m, multi, off) {
        var w = m, past = "";
        if (/'d$/.test(w)) { w = w.slice(0, -2); past = "d"; }
        var lw = w.toLowerCase().replace(/\s+/g, " ");
        if (m === "*") { add("*", "*", KM["*"][1], KM["*"][3]); return "*"; }
        if (UNIT[lw] && !/\d\s*$/.test(txt.slice(0, off))) return m;
        var r = KM[lw], x;
        if (r) { add(r[2], r[2], r[1], r[3]); if (lw === "sts") return "stitches"; if (lw === "st") return "stitch"; return past && /^(dec|inc)$/.test(lw) ? r[1] + past : r[1]; }
        if ((x = /^(k|p)(\d+)tog$/i.exec(w))) { add(lw, w, (x[1].toLowerCase() === "k" ? "knit " : "purl ") + x[2] + " together", "Work " + x[2] + " stitches as one. Loses " + (x[2] - 1) + " stitch" + (x[2] > 2 ? "es." : ".")); return (x[1].toLowerCase() === "k" ? "knit " : "purl ") + x[2] + " together"; }
        if ((x = /^(k|p|sl)(\d+)$/i.exec(w))) {
          var v = { k: "knit", p: "purl", sl: "slip" }[x[1].toLowerCase()];
          var base = KM[x[1].toLowerCase()]; add(base[2] === "sl" ? "sl" : x[1].toLowerCase(), base[2], base[1], base[3]);
          return v + " " + x[2];
        }
        if ((x = /^c(\d+)([fb])$/i.exec(w))) {
          var n = +x[1], h = Math.floor(n / 2), fr = x[2].toLowerCase() === "f";
          var s = "cable " + n + " " + (fr ? "front" : "back");
          add(lw, w.toUpperCase(), s, "Slip " + h + " stitches to a cable needle and hold it in " + (fr ? "front" : "back") + ", knit " + (n - h) + ", then knit the " + h + " from the cable needle. Leans " + (fr ? "left." : "right."));
          return s;
        }
        return m;
      });
      return { out: out, found: found };
    }
    var kaRun = function () {
      var t = $("#ka-in").value.trim(), r = kaDecode(t);
      var o = r.out.replace(/\s+/g, " ");
      $("#ka-plain").textContent = t ? o.charAt(0).toUpperCase() + o.slice(1) : "Paste a pattern line to see it in plain words.";
      $("#ka-found").innerHTML = r.found.length ? r.found.map(function (f) { return "<li><strong>" + esc(f[0]) + "</strong> = " + esc(f[1]) + (f[2] ? "<br><span>" + esc(f[2]) + "</span>" : "") + "</li>"; }).join("") : "<li>No abbreviations found yet.</li>";
    };
    $("#ka-in").addEventListener("input", kaRun);
    $$(".ka-ex button").forEach(function (b) { b.addEventListener("click", function () { $("#ka-in").value = b.getAttribute("data-ex"); kaRun(); }); });
    kaRun();
    var kaG = "", kaFilter = function () {
      var q = ($("#ka-q").value || "").trim().toLowerCase(), n = 0;
      $$("#ka-body tr").forEach(function (tr) {
        var ok = (!kaG || tr.getAttribute("data-g") === kaG) && (!q || tr.getAttribute("data-s").indexOf(q) >= 0);
        tr.hidden = !ok; if (ok) n++;
      });
      $("#ka-none").hidden = n > 0;
    };
    $("#ka-q").addEventListener("input", kaFilter);
    $("#ka-g").addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      $$("#ka-g button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      kaG = b.getAttribute("data-g"); kaFilter();
    });
  }

  /* ---------- EPHEMERA CHECKLIST ---------- */
  if (page === "junk-journal-ephemera-ideas" && $("#ep-list")) {
    var EK = "pp-ephemera", ES = store.get(EK, {}) || {};
    var boxes = $$("#ep-list input[type=checkbox]");
    var USE = ["Tuck them behind a strip of lace or paper glued along the edges.", "Make a pocket from half an envelope and slide them in.", "Wrap a belly band of ribbon round the page and tuck them under it.",
      "Layer them biggest to smallest, slightly off-centre, with one on top as the focal point.", "Glue just the top edge of one so it flips up, and write underneath.", "Make a small cluster in one corner and leave space to write a few lines."];
    var epCount = function () {
      var n = 0;
      boxes.forEach(function (b) { b.checked = !!ES[b.getAttribute("data-id")]; if (b.checked) n++; });
      $("#ep-count").textContent = n + " of " + boxes.length + " collected";
      $$(".ep-gc").forEach(function (sp) {
        var g = sp.getAttribute("data-g"), all = $$('#ep-list fieldset[data-g="' + g + '"] input'), k = all.filter(function (b) { return b.checked; }).length;
        sp.textContent = k + "/" + all.length;
      });
    };
    $("#ep-list").addEventListener("change", function (ev) {
      var b = ev.target; if (!b.matches("input[type=checkbox]")) return;
      if (b.checked) ES[b.getAttribute("data-id")] = 1; else delete ES[b.getAttribute("data-id")];
      store.set(EK, ES); epCount();
    });
    $("#ep-clear").addEventListener("click", function () { if (!confirm("Clear all your ticks?")) return; ES = {}; store.set(EK, ES); epCount(); toast("Ticks cleared"); });
    $("#ep-print").addEventListener("click", function () { window.print(); });
    var epPick = function () {
      var pool = boxes.filter(function (b) { return b.checked; });
      var own = pool.length >= 3;
      if (!own) pool = boxes.slice();
      var bag = pool.slice(), got = [], groups = {};
      while (got.length < 3 && bag.length) {
        var i = Math.floor(Math.random() * bag.length), b = bag.splice(i, 1)[0], g = b.closest("fieldset").getAttribute("data-g");
        if (groups[g] && bag.some(function (o) { return !groups[o.closest("fieldset").getAttribute("data-g")]; })) continue;
        groups[g] = 1; got.push(b.getAttribute("data-n"));
      }
      $("#ep-pile").innerHTML = got.map(function (n, i) { return '<span class="ep-tag t' + i + '">' + esc(n) + "</span>"; }).join("");
      $("#ep-how").textContent = pick(USE);
      $("#ep-hint").textContent = own ? "Picked from the " + pool.length + " things you've ticked." : "Picked from the whole list. Tick at least 3 things you have to pick only from those.";
    };
    $("#ep-go").addEventListener("click", epPick);
    epCount(); epPick();
  }

  /* ---------- YARN YARDAGE (how much is left) ---------- */
  if ($("#yy-list") && $("#yy-out")) {
    var yyE = {}; ["ll", "lu", "lg", "lgu", "ml", "mu", "mg", "core", "need", "nu", "list", "out", "lab", "mea", "add"].forEach(function (k) { yyE[k] = $("#yy-" + k); });
    var yyKeys = ["ll", "lu", "lg", "lgu", "ml", "mu", "mg", "core", "need", "nu"];
    var yyS = store.get("pp-yardage", null) || {};
    yyKeys.forEach(function (k) { if (yyS[k] != null && yyS[k] !== "") yyE[k].value = yyS[k]; });
    var yyBalls = (yyS.balls && yyS.balls.length) ? yyS.balls : ["37"];
    var setSeg = function (el, v) { $$("button", el).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-v") === v); }); };
    if (yyS.mode) setSeg($("#yy-mode"), yyS.mode);
    if (yyS.wu) setSeg($("#yy-wu"), yyS.wu);
    function yyRows() {
      yyE.list.innerHTML = yyBalls.map(function (v, i) {
        return '<li><label for="yy-b' + i + '">Ball ' + (i + 1) + '</label><input type="number" id="yy-b' + i + '" data-i="' + i + '" value="' + esc(v) + '" min="0" max="100000" step="0.1" inputmode="decimal" placeholder="Weight">' +
          (yyBalls.length > 1 ? '<button type="button" class="linkbtn" data-del="' + i + '" aria-label="Remove ball ' + (i + 1) + '">Remove</button>' : "") + "</li>";
      }).join("");
    }
    function yyCalc() {
      var mode = segVal($("#yy-mode")), wu = segVal($("#yy-wu")), OZ = 28.3495;
      yyE.lab.hidden = mode !== "label"; yyE.mea.hidden = mode === "label";
      var ypg = 0, src = "";
      if (mode === "label") {
        var L = parseFloat(yyE.ll.value) || 0, G = parseFloat(yyE.lg.value) || 0;
        if (yyE.lu.value === "m") L = L / 0.9144;
        if (yyE.lgu.value === "oz") G = G * OZ;
        if (L > 0 && G > 0) { ypg = L / G; src = "from your label"; }
      } else {
        var ML = parseFloat(yyE.ml.value) || 0, MG = parseFloat(yyE.mg.value) || 0;
        if (yyE.mu.value === "m") ML = ML / 0.9144;
        if (ML > 0 && MG > 0) { ypg = ML / MG; src = "from your measured piece"; }
      }
      var core = Math.max(0, parseFloat(yyE.core.value) || 0), per = [], tg = 0, any = false;
      yyBalls.forEach(function (v) {
        var w = parseFloat(v); if (!(w > 0)) { per.push(null); return; }
        any = true; var g = (wu === "oz" ? w * OZ : w) - core; g = Math.max(0, g); per.push(g); tg += g;
      });
      var sv = { balls: yyBalls, mode: mode, wu: wu }; yyKeys.forEach(function (k) { sv[k] = yyE[k].value; }); store.set("pp-yardage", sv);
      if (!ypg) { yyE.out.innerHTML = '<h3>Yarn left</h3><div class="big">–</div><p class="sub">' + (mode === "label" ? "Enter the length and weight of a full ball from the label." : "Enter the length you measured and what it weighs.") + "</p>"; return; }
      if (!any) { yyE.out.innerHTML = '<h3>Yarn left</h3><div class="big">–</div><p class="sub">Weigh your leftover ball and type the weight in.</p>'; return; }
      var yd = tg * ypg, m = yd * 0.9144, fullG = 0;
      if (mode === "label") { fullG = parseFloat(yyE.lg.value) || 0; if (yyE.lgu.value === "oz") fullG *= OZ; }
      var out = '<h3>Yarn left' + (yyBalls.length > 1 ? " in " + per.filter(function (x) { return x != null; }).length + " balls" : "") + '</h3><div class="big">' + fmt(yd) + ' <small>yd</small></div>' +
        '<p>That\'s about <strong>' + fmt(m) + ' m</strong> in ' + (Math.round(tg * 10) / 10) + ' g of yarn' + (core > 0 ? " (cores taken off)" : "") + '. Your yarn is <strong>' + (Math.round(ypg * 100) / 100) + ' yd per gram</strong> (' + (Math.round(ypg * 0.9144 * 100) / 100) + ' m), ' + src + '.</p>';
      if (fullG > 0) {
        var balls = tg / fullG, icons = "", whole = Math.floor(balls + 1e-9), part = balls - whole;
        for (var i = 0; i < Math.min(whole, 30); i++) icons += ball("#b8326a", false, i);
        if (part > 0.02 && whole < 30) icons += ball("#2f8f8a", true, whole);
        out += '<div class="balls" aria-hidden="true">' + icons + '</div><p class="sub">Equal to ' + (Math.round(balls * 100) / 100) + " full balls" + (part > 0.02 ? " (the teal one is a part ball)" : "") + ".</p>";
      }
      if (yyBalls.length > 1) {
        out += '<ul class="co-alt">' + per.map(function (g, i) { return g == null ? "" : "<li>Ball " + (i + 1) + ": <strong>" + fmt(g * ypg) + " yd</strong> (" + fmt(g * ypg * 0.9144) + " m)</li>"; }).join("") + "</ul>";
      }
      var need = parseFloat(yyE.need.value) || 0;
      if (need > 0) {
        var nyd = yyE.nu.value === "m" ? need / 0.9144 : need, safe = nyd * 1.1, u = yyE.nu.value, cv = function (y) { return u === "m" ? fmt(y * 0.9144) + " m" : fmt(y) + " yd"; };
        out += "<hr>";
        if (yd >= safe) out += '<p class="gp-ok"><strong>Enough.</strong> You have ' + cv(yd) + " for a project needing " + cv(nyd) + ", with " + cv(yd - nyd) + " to spare.</p>";
        else if (yd >= nyd) out += '<p class="gp-short"><strong>Only just.</strong> You have ' + cv(yd) + " and need " + cv(nyd) + ". That's less than 10% spare, so tension or a swatch could tip you over. Have a plan B colour for a border or stripe.</p>";
        else out += '<p class="gp-short"><strong>Not enough.</strong> You\'re about ' + cv(nyd - yd) + " short (about " + fmt((nyd - yd) / ypg) + " g of this yarn)" + (fullG > 0 ? ", so get " + Math.max(1, Math.ceil((safe - yd) / (fullG * ypg) - 1e-9)) + " more ball" + (Math.ceil((safe - yd) / (fullG * ypg) - 1e-9) > 1 ? "s" : "") + " to be safe" : "") + ".</p>";
        out += '<p class="sub">To wind off exactly ' + cv(nyd) + ", take " + fmt(nyd / ypg) + " g off the ball.</p>";
      }
      var err = 0.5 * ypg * per.filter(function (x) { return x != null; }).length;
      out += '<p class="sub">Estimate. A whole-gram scale can be off by half a gram, about ' + fmt(Math.max(1, err)) + " yd here, and label lengths are rounded.</p>";
      yyE.out.innerHTML = out;
    }
    yyRows();
    yyE.list.addEventListener("input", function (ev) { var i = ev.target.getAttribute("data-i"); if (i == null) return; yyBalls[+i] = ev.target.value; yyCalc(); });
    yyE.list.addEventListener("click", function (ev) { var d = ev.target.getAttribute("data-del"); if (d == null) return; yyBalls.splice(+d, 1); yyRows(); yyCalc(); });
    yyE.add.addEventListener("click", function () { if (yyBalls.length >= 30) return; yyBalls.push(""); yyRows(); var l = $("#yy-b" + (yyBalls.length - 1)); if (l) l.focus(); yyCalc(); });
    yyKeys.forEach(function (k) { yyE[k].addEventListener("input", yyCalc); yyE[k].addEventListener("change", yyCalc); });
    seg($("#yy-mode"), yyCalc); seg($("#yy-wu"), yyCalc);
    yyCalc();
  }
  /* ---------- CRAFT FAIR CHECKLIST + STOCK PLANNER ---------- */
  if ($("#cf-list") && $("#cf-out")) {
    var CK = "pp-craftfair", CS = store.get(CK, {}) || {}; CS.t = CS.t || {};
    var cfBoxes = $$("#cf-list input[type=checkbox]");
    ["goal", "avg", "date"].forEach(function (k) { if (CS[k] != null && CS[k] !== "") $("#cf-" + k).value = CS[k]; });
    var cfCount = function () {
      var n = 0;
      cfBoxes.forEach(function (b) { b.checked = !!CS.t[b.getAttribute("data-id")]; if (b.checked) n++; });
      $("#cf-count").textContent = n + " of " + cfBoxes.length + " packed";
      $$("#cf-list .ep-gc").forEach(function (sp) {
        var g = sp.getAttribute("data-g"), all = $$('#cf-list fieldset[data-g="' + g + '"] input'), k = all.filter(function (b) { return b.checked; }).length;
        sp.textContent = k + "/" + all.length;
      });
    };
    $("#cf-list").addEventListener("change", function (ev) {
      var b = ev.target; if (!b.matches("input[type=checkbox]")) return;
      if (b.checked) CS.t[b.getAttribute("data-id")] = 1; else delete CS.t[b.getAttribute("data-id")];
      store.set(CK, CS); cfCount();
    });
    $("#cf-clear").addEventListener("click", function () { if (!confirm("Clear all your ticks?")) return; CS.t = {}; store.set(CK, CS); cfCount(); toast("Ticks cleared"); });
    $("#cf-print").addEventListener("click", function () { window.print(); });
    function cfPlan() {
      var goal = Math.max(0, parseFloat($("#cf-goal").value) || 0), avg = Math.max(0, parseFloat($("#cf-avg").value) || 0), dv = $("#cf-date").value;
      CS.goal = $("#cf-goal").value; CS.avg = $("#cf-avg").value; CS.date = dv; store.set(CK, CS);
      var h = "";
      if (goal > 0 && avg > 0) {
        var sales = Math.max(1, Math.round(goal / avg)), lo = sales * 2, hi = sales * 3, mid = Math.round((lo + hi) / 2);
        var s1 = Math.round(mid * 0.5), s2 = Math.round(mid / 3), s3 = Math.max(1, mid - s1 - s2);
        var lowP = Math.max(1, Math.round(avg * 0.5)), hiP = Math.round(avg * 2);
        h += '<div class="big">' + lo + "–" + hi + ' <small>items</small></div><p>About <strong>' + sales + " sales</strong> gets you $" + fmt(goal) + " at $" + fmt(avg) + " each, so bring two to three times that.</p>" +
          '<div class="tb-stats"><div><strong>' + s1 + '</strong><span>small makes, around $' + lowP + '</span></div><div><strong>' + s2 + '</strong><span>mid-price, around $' + fmt(avg) + '</span></div><div><strong>' + s3 + '</strong><span>showpieces, $' + hiP + ' and up</span></div><div><strong>$' + (goal >= 600 ? "100" : goal >= 250 ? "75" : "50") + '</strong><span>cash float in small notes</span></div></div>' +
          '<p class="sub">Split for a typical ' + mid + ' pieces. The split and float are our rule of thumb; adjust after your first fair.' + (Math.round(avg) !== avg ? " Round prices to whole dollars to make change easy." : "") + "</p>";
      } else h += '<p class="sub">Enter your sales goal and typical price to see how much stock to bring.</p>';
      if (dv) {
        var d = new Date(dv + "T12:00:00"), now = new Date(); now.setHours(12, 0, 0, 0);
        var days = Math.round((d - now) / 864e5), todo;
        if (days < 0) todo = "That date has passed. Count what sold against your stock list and note what to make more of.";
        else if (days === 0) todo = "It's today! Arrive early, set up from your photo, and keep the float on you.";
        else if (days <= 2) todo = "Charge the card reader and phone, get your float, and pack the car the night before.";
        else if (days <= 14) todo = "Finish making, price and tag everything, practise your set-up, and order cards, bags or a sign if you need them.";
        else todo = "Plenty of time: confirm the booth details, plan your stock list and price bands, and make the bigger pieces first.";
        h += "<hr><p><strong>" + (days > 0 ? days + " day" + (days === 1 ? "" : "s") + " to go." : days === 0 ? "Fair day." : "") + "</strong> " + todo + "</p>";
      }
      $("#cf-res").innerHTML = h;
    }
    ["goal", "avg", "date"].forEach(function (k) { $("#cf-" + k).addEventListener("input", cfPlan); $("#cf-" + k).addEventListener("change", cfPlan); });
    cfCount(); cfPlan();
  }
  /* ---------- TEMPERATURE BLANKET PLANNER ---------- */
  if ($("#tb-out") && P.tblanket) {
    var TBD = P.tblanket, tbW = P.weights || [], TB_YD = 0.667, tbSvg = $("#tb-svg");
    var tbF = ["lo", "hi", "step", "pal", "mode", "st", "y", "w", "wu", "days", "sep", "sk", "gs", "gr", "gu", "data"];
    var tbP = store.get("pp-tblanket", null) || {}, tbUnit = tbP.unit || "F", tbCol = tbP.cols || {}, tbSepCol = "#fbf6ea";
    tbF.forEach(function (k) { var el = $("#tb-" + k); if (el && tbP[k] != null) el.value = tbP[k]; });
    $$("#tb-unit button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === tbUnit); });
    var num = function (id, d) { var x = parseFloat($("#tb-" + id).value); return isFinite(x) ? x : d; };
    function hex2(c) { return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)]; }
    function mix(stops, t) {
      var p = t * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(p)), f = p - i, a = hex2(stops[i]), b = hex2(stops[i + 1]);
      return "#" + [0, 1, 2].map(function (k) { var v = Math.round(a[k] + (b[k] - a[k]) * f); return (v < 16 ? "0" : "") + v.toString(16); }).join("");
    }
    function bands() {
      var lo = Math.round(num("lo", 20)), hi = Math.round(num("hi", 100)), step = Math.max(1, Math.round(num("step", 10)));
      if (hi <= lo) hi = lo + step;
      var mid = Math.min(18, Math.ceil((hi - lo) / step)), out = [], u = "°" + tbUnit;
      out.push({ lo: -1e9, hi: lo - 1, label: "Below " + lo + u });
      for (var i = 0; i < mid; i++) { var a = lo + i * step, b = Math.min(hi - 1, a + step - 1); out.push({ lo: a, hi: b, label: (a === b ? a : a + " to " + b) + u }); }
      out.push({ lo: lo + mid * step, hi: 1e9, label: (lo + mid * step) + u + " and above" });
      var pal = (TBD.palettes.filter(function (p) { return p.id === $("#tb-pal").value; })[0] || TBD.palettes[0]).c;
      out.forEach(function (b, i) { var key = $("#tb-pal").value + ":" + out.length + ":" + i; b.key = key; b.c = tbCol[key] || mix(pal, out.length > 1 ? i / (out.length - 1) : 0); });
      return out;
    }
    function bandOf(bs, v) { v = Math.round(v); for (var i = 0; i < bs.length; i++) if (v >= bs[i].lo && v <= bs[i].hi) return i; return v < bs[0].hi ? 0 : bs.length - 1; }
    function parseData() {
      var lines = ($("#tb-data").value || "").split(/\n/), days = [];
      lines.forEach(function (l) { var m = l.match(/-?\d+(?:\.\d+)?/g); if (m) days.push(m.map(parseFloat)); });
      return days.length >= 2 ? days : null;
    }
    function sampleDays(n, lo, hi) {
      var mid = (lo + hi) / 2, amp = (hi - lo) * 0.42, d = [];
      for (var i = 0; i < n; i++) {
        var base = mid - amp * Math.cos(2 * Math.PI * (i - 18) / 365), noise = (Math.sin(i * 12.9898) * 43758.5453 % 1) * (hi - lo) * 0.16;
        d.push([base + noise, base + noise - (hi - lo) * 0.18]);
      }
      return d;
    }
    function tbCalc() {
      var bs = bands(), mode = $("#tb-mode").value, rpd = mode === "1" ? 1 : 2, data = parseData(), nd = data ? data.length : parseInt($("#tb-days").value, 10) || 365;
      var lo = num("lo", 20), hi = num("hi", 100), days = data || sampleDays(nd, lo, hi);
      var sepN = parseInt($("#tb-sep").value, 10) || 0, months = Math.max(0, Math.round(nd / 30.4) - 1), sepRows = sepN * months;
      var rows = [], monthLen = nd / (months + 1);
      days.forEach(function (d, i) {
        if (sepN && i > 0 && Math.floor(i / monthLen) !== Math.floor((i - 1) / monthLen)) for (var s = 0; s < sepN; s++) rows.push(-1);
        if (mode === "hl") { rows.push(bandOf(bs, d[0])); rows.push(bandOf(bs, d.length > 1 ? d[1] : d[0])); }
        else { var b = bandOf(bs, d[0]); rows.push(b); if (rpd === 2) rows.push(b); }
      });
      var st = TBD.stitches.filter(function (s) { return s.id === $("#tb-st").value; })[0] || TBD.stitches[0];
      var wn = $("#tb-y").value, wt = tbW.filter(function (x) { return String(x.n) === wn; })[0] || { m: 1, name: "" };
      var crochet = st.craft === "crochet", base = (crochet ? TBD.cg : TBD.kg)[wn] || 12.5;
      var gu = parseFloat($("#tb-gu").value) || 4, gs = num("gs", 0), gr = num("gr", 0);
      var spi = gs > 0 ? gs / (gu === 10 ? 3.937 : 4) : base * st.w / 4, rpi = gr > 0 ? gr / (gu === 10 ? 3.937 : 4) : base * st.r / 4;
      var cm = $("#tb-wu").value === "cm", wIn = Math.min(140, Math.max(6, num("w", 50) / (cm ? 2.54 : 1)));
      var sts = Math.max(4, Math.round(wIn * spi)); if (st.even && sts % 2) sts++;
      var nRows = rows.length, lenIn = nRows / rpi;
      var dens = gs > 0 ? (base * st.w / 4) / spi : 1; /* looser than typical uses a little less yarn per area */
      var yd = wIn * lenIn * TB_YD * (wt.m || 1) * (crochet ? 1.27 : 1) * st.d * Math.max(0.75, Math.min(1.3, dens)), perRow = yd / nRows;
      var sk = Math.max(10, num("sk", 200)), cnt = bs.map(function () { return 0; }), sepCnt = 0;
      rows.forEach(function (r) { if (r < 0) sepCnt++; else cnt[r]++; });
      var used = bs.filter(function (b, i) { return cnt[i] > 0; }).length;
      /* colour key */
      var body = "", txt = [];
      bs.forEach(function (b, i) {
        var y = data ? cnt[i] * perRow * 1.1 : yd * (nRows - sepCnt) / nRows / bs.length * 1.25, k = Math.ceil(y / sk);
        var dayTxt = data ? (rpd === 2 && mode === "hl" ? cnt[i] + " rows" : Math.round(cnt[i] / rpd) + " days") : "";
        body += '<tr><td><input type="color" value="' + b.c + '" data-k="' + esc(b.key) + '" aria-label="Colour for ' + esc(b.label) + '"></td><td>' + esc(b.label) + "</td><td>" + (data ? dayTxt : '<span class="muted">–</span>') + "</td><td>" + (y > 0 ? fmt(y) + " yd<br><span class=\"muted\">" + k + " skein" + (k === 1 ? "" : "s") + "</span>" : "–") + "</td></tr>";
        txt.push("Colour " + (i + 1) + " (" + b.c + "): " + b.label + (data ? ", " + dayTxt : "") + (y > 0 ? ", about " + fmt(y) + " yd" : ""));
      });
      if (sepN) { var sy = sepCnt * perRow * 1.15, sk2 = Math.ceil(sy / sk); body += '<tr><td><span class="tb-sw" style="display:inline-block;width:40px;height:28px;border-radius:8px;border:2px solid #d8d4c8;background:' + tbSepCol + '"></span></td><td>Month rows (and border)</td><td>' + sepCnt + " rows</td><td>" + fmt(sy) + ' yd<br><span class="muted">' + sk2 + " skein" + (sk2 === 1 ? "" : "s") + " + border</span></td></tr>"; txt.push("Month rows: " + sepCnt + " rows, about " + fmt(sy) + " yd plus the border"); }
      $("#tb-key").innerHTML = body;
      $$("#tb-key input[type=color]").forEach(function (inp) { inp.addEventListener("input", function () { tbCol[inp.getAttribute("data-k")] = inp.value; tbSave(); tbDraw(rows, bs, wIn, lenIn, !!data); }); });
      tbCalc.txt = txt;
      /* result */
      var found = crochet ? "Chain " + (sts + (st.turn || 0)) + (st.even ? " (an even number)" : "") : "Cast on " + sts;
      var lenCm = lenIn * 2.54, long = lenIn > 90, short = lenIn < wIn * 0.9;
      var out = "<h3>Your blanket</h3>" + '<div class="bk-dims">' + Math.round(wIn) + " × " + Math.round(lenIn) + " in<small>" + Math.round(wIn * 2.54) + " × " + Math.round(lenCm) + " cm, " + nRows + " rows" + (sepRows ? " (incl. " + sepCnt + " month rows)" : "") + "</small></div>" +
        '<div class="tb-stats"><div><strong>' + esc(found) + "</strong><span>" + (crochet ? sts + " stitches a row, plus the turning chain" : "stitches, on a long circular needle") + "</span></div>" +
        "<div><strong>" + bs.length + " colours</strong><span>" + (data ? used + " used by your data" : "including the two end colours") + "</span></div>" +
        "<div><strong>" + fmt(Math.round(yd * 0.088) * 10) + "–" + fmt(Math.round(yd * 0.112) * 10) + " yd</strong><span>" + fmt(Math.round(yd * 0.088 * 0.9144) * 10) + "–" + fmt(Math.round(yd * 0.112 * 0.9144) * 10) + " m in all</span></div>" +
        "<div><strong>" + (perRow < 10 ? perRow.toFixed(1) : fmt(perRow)) + " yd a row</strong><span>about " + fmt(perRow * rpd) + " yd a day</span></div></div>" +
        (long ? '<p class="sub tb-warn">That\'s longer than a queen bed (80 in). For a shorter blanket try a thinner yarn, garter stitch, or fewer rows a day.</p>' : "") +
        (short && nd >= 300 ? '<p class="sub">Wider than it is long. That\'s fine for a throw; or make it narrower to save yarn.</p>' : "") +
        '<p class="sub">' + (data ? "Yarn per colour is from your temperatures, plus 10% spare." : "Yarn per colour is an even share plus 25%; middle colours usually get the most days. Paste real temperatures for exact amounts.") + " Gauge: " + (spi * 4).toFixed(1) + " sts and " + (rpi * 4).toFixed(1) + " rows per 4 in" + (gs > 0 || gr > 0 ? " (yours)" : " (typical, our estimate)") + ".</p>";
      $("#tb-out").innerHTML = out;
      tbDraw(rows, bs, wIn, lenIn, !!data);
      tbSave();
    }
    function tbDraw(rows, bs, wIn, lenIn, real) {
      var H = 280, W = Math.max(60, Math.min(200, H * wIn / lenIn)), h = Math.min(H, W * lenIn / wIn), x0 = (220 - W) / 2, y0 = 10 + (H - h) / 2, rh = h / rows.length, svg = "";
      var cols = bs.map(function (b) { return b.c; });
      $$("#tb-key input[type=color]").forEach(function (inp, i) { cols[i] = inp.value; });
      for (var i = 0; i < rows.length; i++) svg += '<rect x="' + x0.toFixed(1) + '" y="' + (y0 + i * rh).toFixed(2) + '" width="' + W.toFixed(1) + '" height="' + (rh + 0.4).toFixed(2) + '" fill="' + (rows[i] < 0 ? tbSepCol : cols[rows[i]]) + '"/>';
      svg += '<rect x="' + (x0 - 3) + '" y="' + (y0 - 3) + '" width="' + (W + 6) + '" height="' + (h + 6) + '" rx="4" fill="none" stroke="' + tbSepCol + '" stroke-width="4"/>';
      tbSvg.innerHTML = svg;
      $("#tb-cap").textContent = real ? "Your temperatures, first day at the top. Drawn to scale." : "A made-up sample year (cold January at the top) to show your colours. Paste real temperatures to see your own.";
    }
    function tbSave() { var o = { unit: tbUnit, cols: tbCol }; tbF.forEach(function (k) { var el = $("#tb-" + k); if (el) o[k] = el.value; }); store.set("pp-tblanket", o); }
    var tbLast = null;
    seg($("#tb-unit"), function (v) {
      if (v === tbUnit) return;
      var c = v === "C", conv = function (x) { return c ? Math.round((x - 32) * 5 / 9) : Math.round(x * 9 / 5 + 32); };
      var cur = [num("lo", 20), num("hi", 100), num("step", 10)], nx;
      if (tbLast && tbLast.u === v && tbLast.conv.join() === cur.join()) nx = tbLast.orig;
      else nx = [conv(cur[0]), conv(cur[1]), Math.max(1, Math.round(cur[2] * (c ? 5 / 9 : 9 / 5)))];
      tbLast = { u: tbUnit, orig: cur, conv: nx };
      $("#tb-lo").value = nx[0]; $("#tb-hi").value = nx[1]; $("#tb-step").value = nx[2];
      tbUnit = v; tbCalc();
    });
    tbF.forEach(function (k) { var el = $("#tb-" + k); if (el) { el.addEventListener("change", tbCalc); if (el.tagName !== "SELECT") el.addEventListener("input", tbCalc); } });
    $("#tb-reset").addEventListener("click", function () { tbCol = {}; tbCalc(); toast("Colours reset"); });
    $("#tb-copy").addEventListener("click", function () {
      var t = "Temperature blanket colour key\n" + (tbCalc.txt || []).join("\n");
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function () { toast("Copied"); }, function () { toast("Couldn't copy"); });
      else toast("Couldn't copy");
    });
    tbCalc();
  }

  /* ---------- FOUNDATION CHAIN CALCULATOR ---------- */
  if ($("#fc-what") && $("#fc-out")) {
    var fcEl = {}; ["what", "custom", "w", "l", "u", "st", "yarn", "g", "gu", "gnote", "k", "cnt", "pat", "rep", "m", "x", "b", "out", "svg", "cap"].forEach(function (k) { fcEl[k] = $("#fc-" + k); });
    var FC_G = { 1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8, 7: 6 }; /* typical sc per 4 in: middle of the Craft Yarn Council crochet ranges */
    var FC_ST = { sc: { n: "sc", long: "single crochet", k: 2, c: "0", w: 1, r: 1.15 }, hdc: { n: "hdc", long: "half double crochet", k: 3, c: "0", w: 0.95, r: 0.8 },
      dc: { n: "dc", long: "double crochet", k: 4, c: "1", w: 0.9, r: 0.6 }, tr: { n: "tr", long: "treble crochet", k: 5, c: "1", w: 0.85, r: 0.45 } }; /* width and row factors: our estimates */
    var fcKeys = ["what", "w", "l", "u", "st", "yarn", "g", "gu", "k", "cnt", "pat", "m", "x", "b"], fcTouched = { g: false, k: false };
    var fcPref = store.get("pp-fchain", null);
    if (fcPref) { fcKeys.forEach(function (k) { if (fcPref[k] != null && fcPref[k] !== "" && fcEl[k]) fcEl[k].value = fcPref[k]; }); fcTouched = { g: !!fcPref.tg, k: !!fcPref.tk }; }
    var f1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var fBoth = function (inch) { return f1(inch) + " in (" + Math.round(inch * 2.54) + " cm)"; };
    var fLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function fcDefaults() {
      var st = FC_ST[fcEl.st.value] || FC_ST.dc, wn = parseInt(fcEl.yarn.value, 10) || 4, g4 = FC_G[wn] * st.w;
      if (!fcTouched.g) { fcEl.g.value = fcEl.gu.value === "10" ? Math.round(g4 * 10 / 4 / 2.54 * 2) / 2 : Math.round(g4 * 2) / 2; }
      if (!fcTouched.k) { fcEl.k.value = String(st.k); fcEl.cnt.value = st.c; }
      fcEl.gnote.textContent = fcTouched.g ? "Your swatch, in " + st.long + "." : "Filled in with a typical " + st.long + " gauge for this yarn until you type your own.";
    }
    function fcDraw(ch, skip, sts, counts, real, rows) {
      var x0 = 14, W = 292, show = Math.min(ch, 40), u = W / show, g = "", y = 150, i;
      for (i = 0; i < show; i++) {
        var fromHook = show - i; /* chain nearest the hook is on the right */
        var col = fromHook < skip ? "#f4a823" : "#b8326a";
        g += '<ellipse cx="' + (x0 + i * u + u / 2).toFixed(1) + '" cy="' + y + '" rx="' + Math.max(1.6, u / 2 - 0.6).toFixed(1) + '" ry="5" fill="none" stroke="' + col + '" stroke-width="2.4"/>';
      }
      var rh = Math.min(104, 60 + Math.min(rows, 44)), top = y - 10 - rh;
      g += '<rect x="' + x0 + '" y="' + top + '" width="' + W + '" height="' + rh + '" rx="4" fill="#2f8f8a" opacity=".9"/>';
      var colsN = Math.min(sts, 40), cw = W / colsN;
      for (i = 0; i < colsN; i++) g += '<path d="M' + (x0 + i * cw + cw / 2).toFixed(1) + " " + (top + 6) + " v" + (rh - 12) + '" stroke="rgba(255,255,255,.45)" stroke-width="1.4"/>';
      g += '<text x="160" y="' + (top + rh / 2 + 5) + '" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">' + sts + " stitches · about " + f1(real) + " in</text>";
      g += '<text x="160" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2a44">Chain ' + ch + (ch > show ? " (first 40 shown)" : "") + "</text>";
      g += '<path d="M' + (x0 + W + 2) + " " + y + ' l4 0" stroke="#1f2a44" stroke-width="2"/><circle cx="' + (x0 + W + 2) + '" cy="' + y + '" r="3.5" fill="#1f2a44"/>';
      g += '<text x="' + (x0 + W) + '" y="' + (y + 24) + '" text-anchor="end" font-size="11" fill="#1f2a44">hook end</text><text x="' + x0 + '" y="' + (y + 24) + '" font-size="11" fill="#1f2a44">tail</text>';
      fcEl.svg.innerHTML = g;
    }
    function fcCalc() {
      fcDefaults();
      var custom = fcEl.what.value === "custom"; fcEl.custom.hidden = !custom;
      var width, len, cm = fcEl.u.value === "cm";
      if (custom) { width = Math.min(240, Math.max(1, (parseFloat(fcEl.w.value) || 0) / (cm ? 2.54 : 1))); len = Math.min(300, Math.max(0, (parseFloat(fcEl.l.value) || 0) / (cm ? 2.54 : 1))); }
      else { var pv = fcEl.what.value.split("|"); width = parseFloat(pv[0]) || 36; len = parseFloat(pv[1]) || 0; }
      var st = FC_ST[fcEl.st.value] || FC_ST.dc, wn = parseInt(fcEl.yarn.value, 10) || 4;
      var border = parseFloat(fcEl.b.value) || 0, target = Math.max(1, width - 2 * border);
      var g = parseFloat(fcEl.g.value) || 0, spi = g / (fcEl.gu.value === "10" ? 10 / 2.54 : 4);
      if (!(spi > 0)) { fcEl.out.innerHTML = '<h3>Foundation chain</h3><p class="sub">Enter the stitches in your swatch to see the number.</p>'; fcEl.svg.innerHTML = ""; return; }
      var k = parseInt(fcEl.k.value, 10) || 2, counts = fcEl.cnt.value === "1", extra = (k - 1) - (counts ? 1 : 0);
      var sts = Math.max(2, Math.round(target * spi)), ch = sts + extra, pc = fcEl.pat.value === "custom"; fcEl.rep.hidden = !pc;
      var mult = 1, plus = 0, alt = "";
      if (pc) {
        mult = Math.max(1, Math.min(60, parseInt(fcEl.m.value, 10) || 1)); plus = Math.max(0, Math.min(40, parseInt(fcEl.x.value, 10) || 0));
        var reps = Math.max(1, Math.round((ch - plus) / mult)); ch = reps * mult + plus; sts = Math.max(1, ch - extra);
        var lo = reps > 1 ? ch - mult : 0, hi = ch + mult;
        alt = "<hr><h3>Other numbers that fit</h3><ul class=\"co-alt\">" + (lo ? "<li><strong>" + lo + "</strong> chains · about " + fBoth((lo - extra) / spi) + "</li>" : "") + "<li><strong>" + hi + "</strong> chains · about " + fBoth((hi - extra) / spi) + "</li></ul>";
      }
      var real = sts / spi, diff = real - target;
      var ord = function (n) { return n + (n === 2 ? "nd" : n === 3 ? "rd" : "th"); };
      var row1 = "Ch " + ch + ". " + st.n.charAt(0).toUpperCase() + st.n.slice(1) + " in " + ord(k) + " ch from hook and in each ch across" + (pc ? " (or follow your pattern's row 1)" : "") + ": " + sts + " stitches" + (counts && k > 2 ? ", counting the skipped chains as the first " + st.n : "") + ".";
      var rows4 = spi * 4 / st.w * st.r; /* rows per 4 in from the stitch gauge: estimate */
      var rowH = 4 / rows4, rows = len > 0 ? Math.max(1, Math.round((len - 2 * border) / rowH)) : 0;
      var out = "<h3>Foundation chain</h3><div class=\"big\">" + ch + "</div><p class=\"sub\">chains: " + sts + " " + st.long + " stitches + " + extra + " for the turning chain" + (pc ? " (rounded to a multiple of " + mult + (plus ? " + " + plus : "") + ")" : "") + ".</p>" +
        '<p class="id-line">' + esc(row1) + "</p>" +
        '<div class="bk-dims">' + fBoth(real) + "<small>wide, for a target of " + fBoth(target) + (Math.abs(diff) >= 0.1 ? " (" + (diff > 0 ? "+" : "−") + f1(Math.abs(diff)) + " in)" : "") + (border ? ", before a " + border + " in border each side" : "") + "</small></div>";
      if (rows) out += '<div class="tb-stats"><div><strong>about ' + rows + '</strong><span>rows to reach ' + fBoth(len - 2 * border) + "</span></div><div><strong>" + f1(rowH) + ' in</strong><span>per row (estimate, check your swatch)</span></div></div>';
      out += alt;
      out += "<hr><p>Chain loosely, or use a hook one size larger just for the chain. " + (ch > 60 ? "Chain about " + Math.min(10, Math.max(5, Math.round(ch / 30))) + " extra and place a marker every 25, then unpick the spare chains after row 1." : "") + "</p>";
      out += '<p class="sub">Next: ' + fLink("blanket-size-calculator", "how much yarn") + ", " + fLink("row-counter", "row counter") + ", " + fLink("crochet-terms", "US vs UK terms") + ".</p>";
      fcEl.out.innerHTML = out;
      fcDraw(ch, k, sts, counts, real, rows);
      fcEl.cap.textContent = "Chain " + ch + ": the " + (k - 1) + " chain" + (k - 1 === 1 ? "" : "s") + " nearest the hook are skipped, then row 1 has " + sts + " stitches.";
      var save = { tg: fcTouched.g, tk: fcTouched.k }; fcKeys.forEach(function (kk) { save[kk] = fcEl[kk].value; }); store.set("pp-fchain", save);
    }
    var fcU = fcEl.u.value;
    fcEl.u.addEventListener("change", function () { if (fcU !== fcEl.u.value) { var f = fcEl.u.value === "cm" ? 2.54 : 1 / 2.54; ["w", "l"].forEach(function (k) { var v = parseFloat(fcEl[k].value); if (v) fcEl[k].value = Math.round(v * f * 2) / 2; }); } fcU = fcEl.u.value; });
    var fcGu = fcEl.gu.value;
    fcEl.gu.addEventListener("change", function () { var v = parseFloat(fcEl.g.value); if (v && fcGu !== fcEl.gu.value && fcTouched.g) fcEl.g.value = Math.round(v * (fcEl.gu.value === "10" ? 10 / 2.54 / 4 : 4 / (10 / 2.54)) * 2) / 2; fcGu = fcEl.gu.value; });
    fcEl.g.addEventListener("input", function () { fcTouched.g = true; });
    fcEl.k.addEventListener("change", function () { fcTouched.k = true; });
    fcEl.cnt.addEventListener("change", function () { fcTouched.k = true; });
    fcEl.st.addEventListener("change", function () { fcTouched.k = false; fcTouched.g = false; });
    fcEl.yarn.addEventListener("change", function () { fcTouched.g = false; });
    fcKeys.forEach(function (k) { fcEl[k].addEventListener("input", fcCalc); fcEl[k].addEventListener("change", fcCalc); });
    fcCalc();
  }

  /* ---------- JUNK JOURNAL SIGNATURE CALCULATOR ---------- */
  if ($("#js-paper") && $("#js-out")) {
    var jsEl = {}; ["paper", "custom", "a", "bb", "u", "mode", "s", "n", "n-f", "p", "p-f", "t", "puff", "out", "svg", "cap"].forEach(function (k) { jsEl[k] = $("#js-" + k); });
    var jsKeys = ["paper", "a", "bb", "u", "s", "n", "p", "t", "puff"];
    var jsPref = store.get("pp-signature", null);
    if (jsPref) { jsKeys.forEach(function (k) { if (jsPref[k] != null && jsPref[k] !== "") jsEl[k].value = jsPref[k]; }); if (jsPref.mode === "pages") $$("#js-mode button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "pages"); }); }
    var j1 = function (n, d) { var m = Math.pow(10, d == null ? 1 : d); return (Math.round(n * m) / m).toLocaleString("en-US"); };
    var jBoth = function (inch) { return j1(inch, 2) + " in (" + j1(inch * 2.54) + " cm)"; };
    var jLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function jsHoles(h) {
      var n = h <= 6 ? 3 : h <= 10 ? 5 : 7, end = h <= 6 ? 0.5 : 0.75, pos = [], i; /* our rule of thumb */
      for (i = 0; i < n; i++) pos.push(end + (h - 2 * end) * i / (n - 1));
      return { n: n, end: end, pos: pos };
    }
    function jsDraw(pw, ph, sheets, sigs, holes) {
      var g = "", sc = Math.min(150 / ph, 140 / (pw * 2)), H = ph * sc, Wp = pw * sc, x0 = 14, y0 = 30 + (150 - H) / 2;
      g += '<text x="' + (x0 + Wp) + '" y="20" text-anchor="middle" font-size="12" font-weight="700" fill="#1f2a44">Open signature</text>';
      g += '<rect x="' + x0 + '" y="' + y0 + '" width="' + (Wp * 2) + '" height="' + H + '" rx="3" fill="#fbf6ea" stroke="#1f2a44" stroke-width="2"/>';
      g += '<line x1="' + (x0 + Wp) + '" x2="' + (x0 + Wp) + '" y1="' + y0 + '" y2="' + (y0 + H) + '" stroke="#8a6e55" stroke-width="1.5" stroke-dasharray="4 3"/>';
      holes.pos.forEach(function (p, i) {
        var yy = y0 + p * sc; g += '<circle cx="' + (x0 + Wp) + '" cy="' + yy.toFixed(1) + '" r="3.6" fill="' + (i === (holes.n - 1) / 2 ? "#b8326a" : "#1f2a44") + '"/>';
      });
      for (var i = 0; i < holes.n - 1; i++) g += '<line x1="' + (x0 + Wp) + '" x2="' + (x0 + Wp) + '" y1="' + (y0 + holes.pos[i] * sc + 4).toFixed(1) + '" y2="' + (y0 + holes.pos[i + 1] * sc - 4).toFixed(1) + '" stroke="#b8326a" stroke-width="2.2"/>';
      g += '<text x="' + (x0 + Wp) + '" y="' + (y0 + H + 18) + '" text-anchor="middle" font-size="11" fill="#1f2a44">' + j1(pw, 2) + " × " + j1(ph, 2) + " in pages, " + holes.n + " holes</text>";
      /* stack of signatures seen from the head */
      var sx = 196, cols = ["#b8326a", "#2f8f8a", "#f4a823", "#1f2a44"], show = Math.min(sigs, 8), gap = Math.min(14, 100 / show), sh = Math.min(sheets, 10);
      g += '<text x="255" y="20" text-anchor="middle" font-size="12" font-weight="700" fill="#1f2a44">From the top</text>';
      g += '<rect x="' + (sx - 4) + '" y="40" width="' + (show * gap + 8) + '" height="8" rx="2" fill="#8a6e55"/>';
      for (var sg = 0; sg < show; sg++) {
        var cx = sx + sg * gap + gap / 2;
        for (var k = 0; k < sh; k++) {
          var d = 1 + k * Math.min(1.1, (gap / 2 - 1) / sh), len = 110 - k * 1.5;
          g += '<path d="M' + (cx - d).toFixed(1) + " " + (48 + len) + " L" + (cx - d).toFixed(1) + " 52 Q" + cx.toFixed(1) + " 46 " + (cx + d).toFixed(1) + " 52 L" + (cx + d).toFixed(1) + " " + (48 + len) + '" fill="none" stroke="' + cols[sg % 4] + '" stroke-width="1.1"/>';
        }
      }
      g += '<text x="255" y="182" text-anchor="middle" font-size="11" fill="#1f2a44">' + sigs + " signature" + (sigs === 1 ? "" : "s") + (sigs > show ? " (8 shown)" : "") + " × " + sheets + " sheets</text>";
      jsEl.svg.innerHTML = g;
    }
    function jsCalc() {
      var custom = jsEl.paper.value === "custom"; jsEl.custom.hidden = !custom;
      var a, b;
      if (custom) { var f = jsEl.u.value === "cm" ? 2.54 : 1; a = Math.min(40, Math.max(1, (parseFloat(jsEl.a.value) || 0) / f)); b = Math.min(40, Math.max(1, (parseFloat(jsEl.bb.value) || 0) / f)); }
      else { var pv = jsEl.paper.value.split("|"); a = parseFloat(pv[1]); b = parseFloat(pv[2]); }
      var pw = a / 2, ph = b, byPages = segVal($("#js-mode")) === "pages";
      jsEl["n-f"].hidden = byPages; jsEl["p-f"].hidden = !byPages;
      var sheets = Math.max(1, Math.min(20, parseInt(jsEl.s.value, 10) || 1)), sigs, want = 0;
      if (byPages) { want = Math.max(4, Math.min(800, parseInt(jsEl.p.value, 10) || 4)); sigs = Math.ceil(want / (sheets * 4)); }
      else sigs = Math.max(1, Math.min(20, parseInt(jsEl.n.value, 10) || 1));
      var t = parseFloat(jsEl.t.value) || 0.1, puff = parseFloat(jsEl.puff.value) || 1;
      var pages = sheets * 4 * sigs, flat = sheets * 2 * sigs * t * 1.15, spine = flat * puff; /* mm; 1.15 for air in the folds: estimate */
      var holes = jsHoles(ph), thread = ph * 3, totalSheets = sheets * sigs;
      var cw = pw + 0.25, chh = ph + 0.25, spineIn = spine / 25.4 + 0.125;
      var out = "<h3>Your journal</h3><div class=\"big\">" + pages + " <small>pages</small></div><p class=\"sub\">" + sigs + " signature" + (sigs === 1 ? "" : "s") + " × " + sheets + " sheets × 4 pages" + (byPages && pages > want ? " (" + (pages - want) + " more than you asked, so every signature is the same)" : "") + ".</p>" +
        '<div class="tb-stats"><div><strong>' + totalSheets + '</strong><span>sheets to fold</span></div><div><strong>' + (totalSheets * 2) + '</strong><span>leaves</span></div>' +
        '<div><strong>' + j1(pw, 2) + " × " + j1(ph, 2) + ' in</strong><span>page size (' + j1(pw * 2.54) + " × " + j1(ph * 2.54) + ' cm)</span></div>' +
        '<div><strong>' + j1(spine * 0.85, 0) + "–" + j1(spine * 1.2, 0) + ' mm</strong><span>spine thickness' + (puff > 1 ? ", filled (about " + j1(flat, 0) + " mm flat)" : "") + "</span></div></div>" +
        "<hr><h3>Sewing</h3><p><strong>" + holes.n + " holes</strong> per signature at " + holes.pos.map(function (p) { return j1(p, 2); }).join(", ") + " in from the top. Cut about <strong>" + jBoth(thread) + "</strong> of thread per signature, " + j1(thread * sigs / 36, 1) + " yd (" + j1(thread * sigs * 2.54 / 100, 1) + " m) in all.</p>" +
        (sheets > 8 && t >= 0.13 ? '<p class="tb-warn">That\'s a lot of sheets of thicker paper for one fold. Try 4 to 6 per signature so it closes flat.</p>' : sheets > 10 ? '<p class="tb-warn">More than 10 sheets is a thick fold: the middle pages will stick out at the edge. Trim them, or use more signatures with fewer sheets.</p>' : "") +
        "<hr><h3>Cover</h3><p>Cut the cover about <strong>" + jBoth(cw * 2 + spineIn) + "</strong> wide by <strong>" + jBoth(chh) + "</strong> tall: two pages plus a little overhang, and a spine of about " + jBoth(spineIn) + ". An estimate: wrap your stack before you cut.</p>" +
        '<p class="sub">Next: ' + jLink("junk-journal-ephemera-ideas", "ephemera ideas") + ", " + jLink("journal-prompts", "journal prompts") + ", " + jLink("how-to-tea-stain-paper", "tea staining") + ".</p>";
      jsEl.out.innerHTML = out;
      jsDraw(pw, ph, sheets, sigs, holes);
      jsEl.cap.textContent = sigs + " signature" + (sigs === 1 ? "" : "s") + " of " + sheets + " sheets: " + pages + " pages of " + j1(pw, 2) + " × " + j1(ph, 2) + " in, sewn through " + holes.n + " holes.";
      var save = { mode: byPages ? "pages" : "sigs" }; jsKeys.forEach(function (k) { save[k] = jsEl[k].value; }); store.set("pp-signature", save);
    }
    var jsU = jsEl.u.value;
    jsEl.u.addEventListener("change", function () { if (jsU !== jsEl.u.value) { var f = jsEl.u.value === "cm" ? 2.54 : 1 / 2.54; ["a", "bb"].forEach(function (k) { var v = parseFloat(jsEl[k].value); if (v) jsEl[k].value = Math.round(v * f * 4) / 4; }); } jsU = jsEl.u.value; });
    seg(jsEl.mode, jsCalc);
    jsKeys.forEach(function (k) { jsEl[k].addEventListener("input", jsCalc); jsEl[k].addEventListener("change", jsCalc); });
    jsCalc();
  }
  /* ---------- MAGIC RING ROUND WRITER ---------- */
  if ($("#mr-out") && $("#mr-svg")) {
    var MRC = { sc: [1, "sc", 6, false], hdc: [2, "hdc", 8, false], dc: [3, "dc", 12, true] }, mrSt = "sc", mrNTouched = false;
    var mrEl = { n: $("#mr-n"), r: $("#mr-r"), cnt: $("#mr-cnt"), join: $("#mr-join"), st: $("#mr-st"), out: $("#mr-out"), svg: $("#mr-svg"), cap: $("#mr-cap") };
    function mrCalc() {
      var c = MRC[mrSt], n = Math.max(3, Math.min(16, parseInt(mrEl.n.value, 10) || c[2])), R = parseInt(mrEl.r.value, 10) || 3;
      var spiral = segVal(mrEl.join) === "spiral", counts = mrEl.cnt.checked && !spiral, st = c[1], ch = "ch " + c[0];
      var lines = [], r, tot;
      var r1 = "Magic ring, " + ch + (counts ? " (counts as the first " + st + "), " + (n - 1) + " " + st : " (doesn't count), " + n + " " + st) + " into the ring. Pull the tail to close" + (spiral ? ". Place a marker in the first stitch." : ", then sl st into the " + (counts ? "top of the " + ch : "first " + st) + " to join.");
      lines.push(["Round 1", r1, n]);
      for (r = 2; r <= R; r++) {
        tot = n * r;
        var body = r === 2 ? "2 " + st + " in each stitch around" : "(" + (r - 2) + " " + st + ", 2 " + st + " in next st) × " + n;
        var start = spiral ? "" : ch + (counts ? " (counts as the first " + st + "; work the rest around it), " : " (doesn't count), ");
        var end = spiral ? ". Move the marker up." : ", sl st to join.";
        lines.push(["Round " + r, start + body + end, tot]);
      }
      var h = "<h3>Your first rounds</h3>" + '<ol class="sk-steps mr-lines">' + lines.map(function (l) { return "<li><strong>" + l[0] + ":</strong> " + esc(l[1]) + " <span class=\"muted\">(" + l[2] + " sts)</span></li>"; }).join("") + "</ol>";
      if (n !== c[2]) h += '<p class="sub">Most ' + st + " rings start with " + c[2] + (st === "dc" ? " (or 10)" : "") + ". " + (n > c[2] ? "With more, the circle may ruffle." : "With fewer, the circle may cup.") + " Follow your pattern if it says otherwise.</p>";
      if (st === "dc") h += '<p class="sub">Some patterns count the ch 3 as a stitch and some don\'t. Tick the box if yours does.</p>';
      h += '<p><button type="button" class="btn gold sm" id="mr-copy">Copy the rounds</button></p><hr><p class="sub">Next: keep the circle flat to any size with the <a href="' + (location.protocol === "file:" ? "crochet-circle-calculator.html" : "/crochet-circle-calculator") + '">crochet circle calculator</a>, or stripe it with our <a href="' + (location.protocol === "file:" ? "how-to-change-colors-in-crochet.html" : "/how-to-change-colors-in-crochet") + '">colour change guide</a>.</p>';
      mrEl.out.innerHTML = h;
      $("#mr-copy").addEventListener("click", function () { var t = lines.map(function (l) { return l[0] + ": " + l[1] + " (" + l[2] + ")"; }).join("\n"); try { navigator.clipboard.writeText(t).then(function () { toast("Rounds copied"); }); } catch (x) { toast("Couldn't copy"); } });
      var g = "", cols = ["#b8326a", "#2f8f8a", "#f4a823", "#1f2a44", "#c9a37a", "#d97aa0"];
      for (r = R; r >= 1; r--) {
        var k = n * r, rad = 14 + r * 15, i;
        for (i = 0; i < k; i++) {
          var a = -Math.PI / 2 + 2 * Math.PI * i / k, x = 110 + rad * Math.cos(a), y = 110 + rad * Math.sin(a), sz = Math.min(6, 2 * Math.PI * rad / k / 2.4);
          g += '<ellipse cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" rx="' + (sz * 0.7).toFixed(1) + '" ry="' + sz.toFixed(1) + '" transform="rotate(' + (a * 180 / Math.PI + 90).toFixed(1) + " " + x.toFixed(1) + " " + y.toFixed(1) + ')" fill="#fbfcfa" stroke="' + cols[(r - 1) % cols.length] + '" stroke-width="2.4"/>';
        }
      }
      g += '<circle cx="110" cy="110" r="4" fill="#d97aa0"/>';
      if (spiral) g += '<path d="M110 ' + (110 - 14 - R * 15 - 9) + ' l-5 -9 l10 0 z" fill="#2f8f8a"/>';
      mrEl.svg.innerHTML = g;
      mrEl.cap.textContent = R + " round" + (R === 1 ? "" : "s") + " seen from above: " + lines.map(function (l) { return l[2]; }).join(", ") + " stitches.";
      $("#mr-cnt-f").hidden = spiral;
    }
    seg(mrEl.st, function (v) { mrSt = v; if (!mrNTouched) mrEl.n.value = MRC[v][2]; mrEl.cnt.checked = MRC[v][3]; mrCalc(); });
    seg(mrEl.join, mrCalc);
    mrEl.n.addEventListener("input", function () { mrNTouched = true; mrCalc(); });
    mrEl.r.addEventListener("change", mrCalc); mrEl.cnt.addEventListener("change", mrCalc);
    mrCalc();
  }

  /* ---------- STRIPE PLANNER (colour changes) ---------- */
  if ($("#cc-out") && $("#cc-list")) {
    var CCP = ["#f2e6cf", "#b8326a", "#2f8f8a", "#f4a823", "#1f2a44", "#c9a37a", "#7a9e6e", "#9b6fb0"];
    var CCN = ["Cream", "Berry", "Teal", "Gold", "Navy", "Oat", "Sage", "Plum"];
    var ccS = store.get("pp-stripes", null);
    if (!ccS || !ccS.list || !ccS.list.length) ccS = { list: [{ c: 0, r: 2 }, { c: 1, r: 2 }, { c: 0, r: 2 }, { c: 2, r: 2 }], rep: 3, mode: "rows" };
    var ccList = $("#cc-list"), ccRep = $("#cc-rep"), ccMode = $("#cc-mode");
    ccRep.value = ccS.rep || 3;
    $$("button", ccMode).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === (ccS.mode || "rows")); });
    var CARRY_MAX = 8;   // rows; our rule of thumb
    function ccRender() {
      ccList.innerHTML = ccS.list.map(function (s, i) {
        return '<div class="cc-row" data-i="' + i + '"><span class="cc-dot" style="background:' + CCP[s.c] + '"></span><label class="sr-only" for="cc-c' + i + '">Colour</label><select id="cc-c' + i + '" data-k="c">' +
          CCN.map(function (n, k) { return '<option value="' + k + '"' + (k === s.c ? " selected" : "") + ">" + n + "</option>"; }).join("") + '</select><label class="sr-only" for="cc-r' + i + '">Rows</label><input id="cc-r' + i + '" data-k="r" type="number" min="1" max="40" value="' + s.r + '" inputmode="numeric"><span class="muted">rows</span>' +
          (ccS.list.length > 1 ? '<button type="button" class="cc-del" aria-label="Remove stripe ' + (i + 1) + '">×</button>' : "") + "</div>";
      }).join("");
      ccCalc();
    }
    function ccCalc() {
      var rounds = segVal(ccMode) === "rounds", rep = parseInt(ccRep.value, 10) || 1, unit = rounds ? "round" : "row";
      ccS.rep = rep; ccS.mode = rounds ? "rounds" : "rows"; store.set("pp-stripes", ccS);
      var seq = [], i, k;
      for (k = 0; k < rep; k++) ccS.list.forEach(function (s) { var r = Math.max(1, Math.min(40, parseInt(s.r, 10) || 1)); if (seq.length && seq[seq.length - 1].c === s.c) seq[seq.length - 1].r += r; else seq.push({ c: s.c, r: r }); });
      // simulate: edge 0 = starting edge; a row ends at the other edge.
      var row = 0, where = {}, steps = [], carries = [], joins = [], ends = 0, cuts = 0, carried = 0;
      seq.forEach(function (s, idx) {
        var edge = rounds ? 0 : row % 2, from = row, how;
        if (idx === 0) { how = "join"; ends++; }
        else {
          var w = where[s.c];
          if (w && w.edge === edge && (row - w.row) <= CARRY_MAX) { how = "carry"; carries.push({ c: s.c, from: w.row, to: row, edge: edge }); carried++; }
          else { how = "join"; ends++; if (w) { cuts++; ends++; w.cut = true; } }
          delete where[s.c];
        }
        joins.push({ row: row, how: how, c: s.c });
        steps.push({ s: s, from: from, how: how, edge: edge, gap: how === "carry" ? row - carries[carries.length - 1].from : 0 });
        row += s.r;
        // drop this colour at the edge where its last row ends (rows) or at the join (rounds)
        if (idx < seq.length - 1) where[s.c] = { edge: rounds ? 0 : row % 2, row: row };
      });
      var left = Object.keys(where).length; ends += 1 + left; cuts += left;
      // plan text (first two repeats is plenty)
      var maxShow = Math.min(steps.length, ccS.list.length * 2 + 1), h = "";
      h += "<h3>Your stripes</h3><div class=\"tb-stats\"><div><strong>" + row + "</strong><span>" + unit + "s in all</span></div><div><strong>" + carried + "</strong><span>times you carry, no cutting</span></div><div><strong>" + (joins.length - 1 - carried) + "</strong><span>times you join a new end</span></div><div><strong>" + ends + "</strong><span>ends to weave in</span></div></div>";
      h += '<ol class="sk-steps">';
      for (i = 0; i < maxShow; i++) {
        var st = steps[i], nm = CCN[st.s.c], a = st.from + 1, b = st.from + st.s.r;
        var t = "<strong>" + (a === b ? unit.charAt(0).toUpperCase() + unit.slice(1) + " " + a : unit.charAt(0).toUpperCase() + unit.slice(1) + "s " + a + "–" + b) + ": " + nm + ".</strong> ";
        if (i === 0) t += "Start with " + nm + ".";
        else if (st.how === "carry") t += "Pick " + nm + " up from " + (rounds ? "behind the join" : "the edge") + ", where it has waited " + st.gap + " " + unit + (st.gap === 1 ? "" : "s") + ". No cutting.";
        else t += "Change on the last yarn over of " + unit + " " + st.from + " and join " + nm + " with a 6 in tail.";
        var nxt = steps.slice(i + 1).filter(function (x) { return x.s.c === st.s.c; })[0];
        if (i < steps.length - 1) t += nxt ? (nxt.how === "carry" ? " Leave it hanging when you change: you'll carry it." : " Cut it when you change (it would be on the wrong edge, or waiting too long).") : " Cut it when you change: it isn't used again.";
        h += "<li>" + t + "</li>";
      }
      if (steps.length > maxShow) h += "<li class=\"muted\">…the same again for the other repeats.</li>";
      h += "</ol>";
      var odd = !rounds && seq.some(function (s, i2) { return i2 < seq.length - 1 && s.r % 2; });
      if (odd) h += '<p class="tb-warn">Some stripes have an odd number of rows, so a colour can end up at the wrong edge. Make every stripe 2, 4 or 6 rows to carry everything up the side.</p>';
      h += '<p class="sub">We carry a colour only when it waits at the same edge for ' + CARRY_MAX + " " + unit + "s or fewer (our rule of thumb; longer carries pull and show). Tails of about 6 in (15 cm).</p>";
      $("#cc-out").innerHTML = h;
      // drawing: rows from the bottom, carried strands on the edge
      var H = 270, rh = Math.min(18, H / row), y0 = 285, g = "", x0 = 50, W = 160;
      steps.forEach(function (st) { g += '<rect x="' + x0 + '" y="' + (y0 - (st.from + st.s.r) * rh).toFixed(1) + '" width="' + W + '" height="' + (st.s.r * rh).toFixed(1) + '" fill="' + CCP[st.s.c] + '"/>'; });
      if (!rounds && rh >= 6) for (i = 1; i < row; i++) g += '<line x1="' + x0 + '" x2="' + (x0 + W) + '" y1="' + (y0 - i * rh).toFixed(1) + '" y2="' + (y0 - i * rh).toFixed(1) + '" stroke="#1f2a44" stroke-opacity=".1"/>';
      g += '<rect x="' + x0 + '" y="' + (y0 - row * rh).toFixed(1) + '" width="' + W + '" height="' + (row * rh).toFixed(1) + '" fill="none" stroke="rgba(31,42,68,.3)"/>';
      carries.forEach(function (c, n) {
        var x = rounds ? x0 + W / 2 : (c.edge === 0 ? x0 - 6 - (n % 3) * 4 : x0 + W + 6 + (n % 3) * 4);
        g += '<line x1="' + x + '" x2="' + x + '" y1="' + (y0 - c.from * rh).toFixed(1) + '" y2="' + (y0 - c.to * rh).toFixed(1) + '" stroke="' + CCP[c.c] + '" stroke-width="3" stroke-linecap="round"' + (rounds ? ' stroke-dasharray="4 3"' : "") + "/>";
      });
      joins.forEach(function (j) { if (j.how === "join") { var x = rounds ? x0 + W / 2 : (j.row % 2 === 0 ? x0 : x0 + W); g += '<circle cx="' + x + '" cy="' + (y0 - j.row * rh).toFixed(1) + '" r="4" fill="#f4a823" stroke="#1f2a44" stroke-width="1"/>'; } });
      $("#cc-svg").innerHTML = g;
    }
    ccList.addEventListener("input", function (e) { var r = e.target.closest(".cc-row"); if (!r) return; var s = ccS.list[+r.getAttribute("data-i")], k = e.target.getAttribute("data-k"); if (k === "c") { s.c = +e.target.value; $(".cc-dot", r).style.background = CCP[s.c]; } if (k === "r") s.r = parseInt(e.target.value, 10) || 1; ccCalc(); });
    ccList.addEventListener("change", function (e) { if (e.target.getAttribute("data-k") === "c") { ccS.list[+e.target.closest(".cc-row").getAttribute("data-i")].c = +e.target.value; ccCalc(); } });
    ccList.addEventListener("click", function (e) { var b = e.target.closest(".cc-del"); if (!b) return; ccS.list.splice(+b.closest(".cc-row").getAttribute("data-i"), 1); ccRender(); });
    $("#cc-add").addEventListener("click", function () { if (ccS.list.length >= 8) { toast("Up to 8 stripes"); return; } var last = ccS.list[ccS.list.length - 1]; ccS.list.push({ c: (last.c + 1) % CCP.length, r: 2 }); ccRender(); });
    ccRep.addEventListener("change", ccCalc); seg(ccMode, ccCalc);
    ccRender();
  }

  /* ---------- YARN WEIGHT FINDER ---------- */
  if ($("#yw-out") && window.YWID && P.weights) {
    var ywMode = $("#yw-mode");
    function ywCalc() {
      var wpi = segVal(ywMode) === "wpi", hits = [], val, txt;
      $("#yw-label").hidden = wpi; $("#yw-wpi").hidden = !wpi;
      if (wpi) {
        val = parseFloat($("#yw-w").value);
        if (!(val > 0)) { $("#yw-out").innerHTML = "<p>Enter the number of wraps.</p>"; return; }
        hits = window.YWID.filter(function (r) { return val >= r[2] && val <= r[3]; });
        txt = val + " wraps per inch";
      } else {
        var len = parseFloat($("#yw-len").value), g = parseFloat($("#yw-g").value);
        if (!(len > 0) || !(g > 0)) { $("#yw-out").innerHTML = "<p>Enter the length and weight from the label.</p>"; return; }
        if ($("#yw-lu").value === "yd") len *= 0.9144;
        if ($("#yw-gu").value === "oz") g *= 28.35;
        val = len / g * 100;
        hits = window.YWID.filter(function (r) { return val >= r[4] * 0.97 && val <= r[5] * 1.03; });
        if (!hits.length) { var best = null, bd = 1e9; window.YWID.forEach(function (r) { var d = Math.min(Math.abs(val - r[4]), Math.abs(val - r[5])); if (d < bd) { bd = d; best = r; } }); hits = [best]; }
        txt = fmt(val) + " m per 100 g (" + fmt(val * 1.0936) + " yd)";
      }
      var W = P.weights, h = "<h3>Your yarn is most likely</h3>";
      h += '<div class="big" style="font-size:2rem">' + hits.map(function (r) { return esc(r[1]) + " (" + r[0] + ")"; }).join(" or ") + "</div><p class=\"sub\">" + esc(txt) + (hits.length > 1 ? ". That's on the line between two weights, so swatch with both needle sizes." : ".") + "</p>";
      hits.forEach(function (r) { var w = W[r[0]]; if (!w) return; h += "<hr><p><strong>" + esc(w.name) + " (" + r[0] + ")</strong>, also called " + esc(w.also) + ". UK: " + esc(w.uk) + ".</p><p>Needles <strong>" + esc(w.needle) + "</strong>, hook <strong>" + esc(w.hook) + "</strong>. Good for " + esc(w.use.toLowerCase()) + '. <a href="#w' + r[0] + '">See it in the chart</a>.</p>'; });
      h += '<hr><p class="sub">Typical ranges from Yarn.com\'s yarn weight chart. Fluffy or very dense yarns can sit outside them.</p>';
      $("#yw-out").innerHTML = h;
      var s = "", i, on = hits.map(function (r) { return r[0]; });
      for (i = 0; i <= 7; i++) {
        var x = 18 + i * 37, th = 3 + i * 3.2, hit = on.indexOf(i) >= 0;
        s += '<rect x="' + (x - th / 2) + '" y="' + (58 - th * 1.6) + '" width="' + th + '" height="' + (th * 3.2 + 10) + '" rx="' + th / 2 + '" fill="' + (hit ? "#b8326a" : "#c9a37a") + '" opacity="' + (hit ? 1 : 0.55) + '"/>';
        s += '<text x="' + x + '" y="104" text-anchor="middle" font-size="12" fill="#1f2a44" font-weight="' + (hit ? 700 : 400) + '">' + i + "</text>";
      }
      $("#yw-svg").innerHTML = s;
    }
    seg(ywMode, ywCalc);
    ["#yw-len", "#yw-g", "#yw-w"].forEach(function (k) { $(k).addEventListener("input", ywCalc); });
    ["#yw-lu", "#yw-gu"].forEach(function (k) { $(k).addEventListener("change", ywCalc); });
    ywCalc();
  }
  /* ---------- BIND OFF CHOOSER ---------- */
  if ($("#bo-out") && $("#bo-edge")) {
    // method, stretch 1-3, yarn multiple of edge width (+ tail), needle advice, steps
    var BOM = {
      scarf: ["Basic bind off", 1, 3, "Use your working needle, or 1 size larger if your bind offs usually come out tight.", ["Knit 2.", "Lift the first stitch over the second and off.", "Knit 1, lift over. Repeat to the last stitch.", "Cut the yarn and pull it through the last loop."], "An edge that doesn't stretch suits scarves, blankets and dishcloths."],
      rib: ["Bind off in pattern", 2, 3, "Use the working needle or 1 size larger.", ["Work 2 stitches as they look: knit the knits, purl the purls.", "Lift the first over the second.", "Work the next stitch as it looks, lift over. Repeat.", "Cut and pull through. If it must stretch over a head or hand, use Jeny's stretchy instead."], "The edge follows the rib, so it doesn't pull in or flare."],
      neck: ["Jeny's surprisingly stretchy bind off", 3, 6.25, "Use the working needle; go up a size if it still feels firm.", ["Before a knit stitch: yarn over backwards (back to front over the needle), then knit 1.", "Lift the yarn over over the knit stitch.", "Before a purl: a normal yarn over, purl 1, lift the yarn over over it.", "With 2 stitches on the right needle, lift the first over the second. Repeat to the end."], "It adds a yarn over to every stitch, so the edge stretches as far as the rib below."],
      sock: ["Jeny's surprisingly stretchy bind off", 3, 6.25, "Use the working needle.", ["Yarn over (backwards before a knit, normal before a purl), work the stitch, lift the yarn over over it.", "Lift the first stitch on the right needle over the second.", "Repeat all the way round.", "Test: the cuff must pull over your heel. If not, go up a needle size."], "A toe-up cuff has to stretch over the heel, so the basic bind off is too tight."],
      rib11: ["Tubular bind off", 3, 4, "Work it with a tapestry needle. Some knitters do 2 set-up rows of slipped stitches first, as the pattern says.", ["Cut a tail about 4 times the edge.", "Separate or work the knit and purl stitches in pairs with the needle, the way your pattern shows.", "Sew through each stitch twice, taking it off the needle after the second pass.", "Keep the yarn snug, not tight."], "It runs the yarn round the knits and purls like a tube, so the edge is stretchy and almost invisible."],
      shawl: ["Loose basic bind off", 2, 3.5, "Use a needle at least 2 sizes larger, or switch to Jeny's stretchy if you'll block it hard.", ["Knit 2 with the larger needle.", "Lift the first over the second, without tugging.", "Knit 1, lift over. Repeat.", "Check the edge stretches as far as the lace before you cut."], "Blocking stretches lace a lot. A tight edge stops the points opening out."],
      garter: ["Long-tail bind off (or the sewn bind off)", 2, 4, "Use the working needle.", ["Cut a tail about 4 times the edge (Purl Soho).", "Work the bind off with the tail as the pattern or tutorial shows, so the edge mirrors the long-tail cast on.", "Or use Elizabeth Zimmermann's sewn bind off with a tapestry needle and a tail 3 to 4 times the edge.", "Finish the last stitch knitwise and pull the yarn through."], "Both edges then match, which looks neat on scarves and blankets."],
      seam: ["Three-needle bind off", 1, 3, "Use a third needle the same size or 1 size larger.", ["Put the two pieces right sides together, needles parallel.", "Knit 1 stitch from the front and back needle together.", "Do it again, then lift the first over the second.", "Repeat to the end; cut and pull through."], "It joins and binds off in one go, so there's no seam to sew."]
    };
    var boWay = $("#bo-way");
    function boCalc() {
      var k = $("#bo-edge").value, m = BOM[k], round = segVal(boWay) === "round";
      var w = parseFloat($("#bo-w").value), cm = $("#bo-u").value === "cm", n = parseInt($("#bo-n").value, 10) || 0;
      if (!(w > 0)) { $("#bo-out").innerHTML = "<p>Enter the width of the edge.</p>"; return; }
      var win = cm ? w / 2.54 : w, tail = 8, yarnIn = win * m[2] + tail;
      var u = function (inch) { return cm ? fmt(inch * 2.54) + " cm" : (inch < 36 ? fmt(inch) + " in" : (inch / 36).toFixed(1) + " yd"); };
      var alt = function (inch) { return cm ? Math.round(inch) + " in" : fmt(inch * 2.54) + " cm"; };
      var h = "<h3>Use</h3><div class=\"big\" style=\"font-size:1.9rem;line-height:1.1\">" + esc(m[0]) + "</div>";
      h += "<p class=\"sub\">Stretch: " + "●●●".slice(0, m[1]) + "○○○".slice(0, 3 - m[1]) + ". " + esc(m[5]) + "</p>";
      h += '<div class="tb-stats"><div><strong>' + u(yarnIn) + "</strong><span>yarn to keep (" + alt(yarnIn) + ")</span></div><div><strong>" + (cm ? "20 cm" : "8 in") + "</strong><span>tail left to weave in</span></div>" +
        (n > 1 ? "<div><strong>" + n + "</strong><span>stitches to bind off" + (k === "seam" ? " (" + Math.round(n / 2) + " on each needle)" : "") + "</span></div>" : "") + "<div><strong>" + m[2] + "×</strong><span>the edge width, plus the tail</span></div></div>";
      h += "<h3>How</h3><ol class=\"sk-steps\">" + m[4].map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") +
        (round ? "<li>In the round: when 1 stitch is left, cut and pull through, then take the tail under both legs of the first bound-off stitch and back into the last one to close the gap.</li>" : "") + "</ol>";
      h += "<p class=\"sub\"><strong>Needle:</strong> " + esc(m[3]) + "</p>";
      h += '<hr><p class="sub">Yarn amounts are our estimates: about 3× the width for a lift-over bind off, 3-4× for sewn and long-tail ones (Purl Soho), about 6¼× for Jeny\'s (one knitter\'s measure, via Cocoknits). Add 8 in (20 cm) to weave in. Next: <a href="' + (location.protocol === "file:" ? "how-to-weave-in-ends.html" : "/how-to-weave-in-ends") + '" style="color:#ffd38a">weave in the tail</a>.</p>';
      $("#bo-out").innerHTML = h;
      // drawing: edge bar + the yarn folded into lines of the edge width
      var lines = m[2] + tail / win, full = Math.floor(lines), part = lines - full, g = "", x0 = 30, W = 240, y = 20, i;
      g += '<rect x="' + x0 + '" y="' + y + '" width="' + W + '" height="16" rx="5" fill="#1f2a44"/>';
      g += '<text x="150" y="' + (y + 12) + '" text-anchor="middle" font-size="11" fill="#fff">your edge: ' + esc(u(win)) + "</text>";
      var gap = Math.min(12, 90 / Math.max(1, full + 1));
      for (i = 0; i < full; i++) g += '<line x1="' + x0 + '" x2="' + (x0 + W) + '" y1="' + (y + 32 + i * gap) + '" y2="' + (y + 32 + i * gap) + '" stroke="#b8326a" stroke-width="3" stroke-linecap="round"/>';
      if (part > 0.02) g += '<line x1="' + x0 + '" x2="' + (x0 + W * part).toFixed(1) + '" y1="' + (y + 32 + full * gap) + '" y2="' + (y + 32 + full * gap) + '" stroke="#f4a823" stroke-width="3" stroke-linecap="round"/>';
      $("#bo-svg").innerHTML = g;
    }
    ["#bo-edge", "#bo-u"].forEach(function (s) { $(s).addEventListener("change", boCalc); });
    ["#bo-w", "#bo-n"].forEach(function (s) { $(s).addEventListener("input", boCalc); });
    seg(boWay, boCalc);
    boCalc();
  }

  /* ---------- WEAVING IN ENDS HELPER ---------- */
  if ($("#we-out") && $("#we-fab")) {
    var WEY = { // tail in, stitches each way, extra
      wool: [6, "3-5", "Wool grips itself, so a short weave holds."],
      smooth: [6, "5-7", "Smooth yarn slides, so go a little further and split the plies on the way back."],
      slip: [8, "5-7", "Split the plies, and for extra hold whipstitch the tails together with sewing thread, then knot and clip the thread (Cocoknits)."],
      bulky: [8, "3-5", "Split the plies and weave each one separately so there's no lump."],
      chenille: [8, "5-7", "Chenille and T-shirt yarn can't be split. Pull the tail through with a small crochet hook instead of a needle (Make and Do Crew)."],
      fuzzy: [6, "3-4", "Fuzzy yarn grabs on to itself, so a short weave holds, but it's hard to undo. Weave carefully the first time."]
    };
    var weCraft = $("#we-craft");
    function weCalc() {
      var knit = segVal(weCraft) === "knit", fab = $("#we-fab").value, y = WEY[$("#we-yarn").value], use = $("#we-use").value;
      var n = Math.max(1, parseInt($("#we-n").value, 10) || 1), dirs = use === "heavy" || $("#we-yarn").value === "slip" ? 3 : 2;
      var tool = $("#we-yarn").value === "chenille" ? "a small crochet hook" : ($("#we-yarn").value === "bulky" ? "a big-eye tapestry needle" : "a blunt tapestry needle");
      var how = [];
      if (fab === "ami") how = ["Close the opening: sew through the front loops of the last round and pull tight.", "Push the needle into the toy, through the stuffing and out the other side.", "Squash the toy a little, snip the tail close and let go: it disappears inside."];
      else if (fab === "granny") how = ["On the back, weave under the thick clusters of the last round, not the chain spaces.", "Change direction and go back through the round below.", "If you'll join the squares, you can sew with one tail and weave the other."];
      else if (fab === "stripes") how = ["Weave each tail into stitches of its own colour, so it can't show through.", knit ? "On the purl side, follow the purl bumps of the same colour (duplicate stitch)." : "On the wrong side, run it through the posts of the same colour.", "Tails at the edge can go up the edge stitches; a border will cover them."];
      else if (fab === "lace") how = ["Find a solid line: an edge, a seam, or a column of stitches with no holes.", knit ? "Follow the yarn's path with duplicate stitch, staying out of the eyelets." : "Weave through the posts of solid stitches, never across a chain space.", "Keep the tension loose so the lace still opens out when you block it."];
      else if (fab === "rib") how = [knit ? "On the wrong side, weave up and down inside one column of stitches." : "Weave along the rib's columns, not across them.", "That way the rib can still stretch without the tail pulling.", "Change direction inside the same column."];
      else if (fab === "rounds") how = [knit ? "At the top of a hat, run the tail through the live stitches, pull them closed and take it to the inside." : "Finish with an invisible fasten off: under both loops of the first stitch, then back into the last one.", "On the wrong side, weave along the round for about 1 to 2 in.", "Turn and come back through a different round."];
      else how = [knit ? "On the purl side, follow the path of the yarn through the stitches (duplicate stitch), or weave up the edge stitches." : "On the wrong side, run the tail through the posts of a few stitches.", "Go about 1 to 2 in (3 to 5 cm), then turn and come back through different strands.", "At the edges, weave into the edge stitches first, then turn into the fabric."];
      if (fab !== "ami") how.push("Make " + dirs + " passes in different directions" + (dirs === 3 ? " (it'll get stretched or washed a lot)" : "") + ". Stretch the fabric gently, then trim close.");
      var mins = n * (fab === "ami" ? 1 : 1.5) * (y[0] === 8 ? 1.2 : 1);
      var h = "<h3>Leave a tail of</h3><div class=\"big\" style=\"font-size:2.6rem\">" + y[0] + " in <small>(" + Math.round(y[0] * 2.54) + " cm)</small></div>";
      h += '<div class="tb-stats"><div><strong>' + y[1] + "</strong><span>stitches each way</span></div><div><strong>" + (fab === "ami" ? "1" : dirs) + "</strong><span>direction" + (fab === "ami" ? " (through the toy)" : "s") + "</span></div><div><strong>" + n + "</strong><span>ends</span></div><div><strong>about " + (mins < 60 ? Math.round(mins) + " min" : (mins / 60).toFixed(1) + " hours") + "</strong><span>to weave them in</span></div></div>";
      h += "<p class=\"sub\"><strong>Tool:</strong> " + tool + ". " + esc(y[2]) + "</p>";
      h += "<h3>How</h3><ol class=\"sk-steps\">" + how.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ol>";
      if (n >= 30) h += '<p class="tb-warn">That\'s a lot of ends. Weave them in as you go, crochet over tails, or carry colours up the side to cut the pile next time.</p>';
      h += '<hr><p class="sub">Time is our rough estimate (about 1½ minutes an end). Don\'t knot the tails, and weave in before blocking.</p>';
      $("#we-out").innerHTML = h;
      // drawing: stitch grid + path with the right number of passes
      var g = '<rect x="10" y="10" width="240" height="130" rx="10" fill="#f2e6cf"/>', r, c;
      for (r = 0; r < 5; r++) for (c = 0; c < 9; c++) {
        var x = 30 + c * 25, yy = 30 + r * 23;
        g += knit ? '<path d="M' + (x - 7) + " " + (yy - 6) + " q7 6 0 12 M" + (x + 7) + " " + (yy - 6) + ' q-7 6 0 12" fill="none" stroke="#d97aa0" stroke-width="2.2"/>'
                  : '<rect x="' + (x - 4) + '" y="' + (yy - 8) + '" width="8" height="17" rx="3" fill="none" stroke="#d97aa0" stroke-width="2.2"/>';
      }
      var span = { "3-4": 3.5, "3-5": 4, "5-7": 6 }[y[1]] || 4, len = span * 25, sx = 235, sy = 122, d = "M" + sx + " " + sy, cx = sx, cy = sy, k;
      var nd = fab === "ami" ? 1 : dirs;
      for (k = 0; k < nd; k++) {
        if (k % 2 === 0) { cx -= len; d += " L" + cx + " " + cy; } else { cx += len * 0.8; d += " L" + cx + " " + cy; }
        if (k < nd - 1) { cy -= 23; d += " Q" + (k % 2 === 0 ? cx - 12 : cx + 12) + " " + (cy + 11) + " " + cx + " " + cy; }
      }
      g += '<path d="' + d + '" fill="none" stroke="#2f8f8a" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="' + cx + '" cy="' + cy + '" r="5" fill="#f4a823" stroke="#1f2a44"/>';
      $("#we-svg").innerHTML = g;
    }
    ["#we-fab", "#we-yarn", "#we-use"].forEach(function (s) { $(s).addEventListener("change", weCalc); });
    $("#we-n").addEventListener("input", weCalc); seg(weCraft, weCalc);
    weCalc();
  }

})();

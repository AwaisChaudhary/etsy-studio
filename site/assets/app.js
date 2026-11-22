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
    var cur = {}, locks = {}, SP = "pp-spreads", saved = store.get(SP, []);
    function fill(k, anim) {
      var el = $('[data-slot="' + k + '"]'), arr = P.prompts[k], v; do { v = pick(arr); } while (arr.length > 1 && v === cur[k]); cur[k] = v;
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
})();

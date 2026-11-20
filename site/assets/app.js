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
})();

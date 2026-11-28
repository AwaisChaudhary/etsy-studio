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
    if ($("#rc-nl") && $("#rc-need")) {
      var rcRows = function () {
        var cm = $("#rc-nu").value === "cm", len = (parseFloat($("#rc-nl").value) || 0) / (cm ? 2.54 : 1), over = $("#rc-no").value === "10" ? 10 / 2.54 : 4, rg = parseFloat($("#rc-nr").value) || 0;
        return len > 0 && rg > 0 ? Math.ceil(len * rg / over) : 0;
      };
      var rcShow = function () { var r = rcRows(); $("#rc-need").innerHTML = r ? "<strong>" + r + " rows</strong> to work " + esc($("#rc-nl").value) + " " + $("#rc-nu").value + "." : "Type a length and your row gauge."; $("#rc-nset").disabled = !r; };
      ["#rc-nl", "#rc-nu", "#rc-nr", "#rc-no"].forEach(function (q) { $(q).addEventListener("input", rcShow); $(q).addEventListener("change", rcShow); });
      $("#rc-nset").addEventListener("click", function () { var r = rcRows(); if (!r) return; S.list[0].target = String(r); save(); render(); toast("Target set: " + r + " rows"); window.scrollTo({ top: 0, behavior: "smooth" }); });
      rcShow();
    }
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
    var prE = {}; ["m", "h", "r", "oh", "ch", "fair", "bf", "bn", "cf", "con", "cp", "try", "out", "cur"].forEach(function (k) { prE[k] = $("#pr-" + k); });
    var prKeys = ["m", "h", "r", "oh", "ch", "bf", "bn", "cf", "cp"].concat(prE.cur ? ["cur"] : []), prPref = store.get("pp-price", null);
    if (prPref) prKeys.forEach(function (k) { if (prPref[k] != null && prPref[k] !== "") prE[k].value = prPref[k]; });
    var money = function (n) { return (prE.cur ? prE.cur.value : "$") + (Math.round(n * 100) / 100).toFixed(2); };
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

  /* ---------- CAST ON CHOOSER + LONG-TAIL TAIL CALCULATOR ---------- */
  if ($("#cn-out") && $("#cn-what")) {
    // method, stretch 1-3, uses a tail?, why, steps, alternative
    var CNM = {
      first: ["Long-tail cast on", 2, true, "It's the one you'll use most, and it gives a neat edge that's ready to knit.", ["Pull out the tail below and make a slip knot on the needle.", "Tail over your thumb, ball yarn over your index finger, both ends in your palm.", "Up through the thumb loop, over and behind the finger strand to catch it.", "Back down through the thumb loop, drop it and snug the stitch. Repeat."], "Rather not guess a tail? Use the knitted cast on: knit into the slip knot, and put the new loop back on the left needle. Repeat."],
      scarf: ["Long-tail cast on", 2, true, "Neat, fairly stretchy and quick for a lot of stitches.", ["Pull out the tail below and make a slip knot.", "Slingshot: tail over thumb, ball yarn over finger.", "Up through the thumb loop, catch the finger strand, back down.", "Drop the loop, snug, repeat. Place a marker every 20 or 25 stitches so you can count."], "Garter scarf? The German twisted cast on gives a bit more stretch and a pretty edge."],
      big: ["Long-tail cast on with two strands", 2, false, "With a lot of stitches, guessing the tail is risky. Two strands mean you can't run out.", ["Take one end from the outside of the ball and one from the middle (or use two balls).", "Tie them together in a slip knot and put it on the needle.", "Cast on as normal: one strand over your thumb, the other over your finger.", "At the end, cut the thumb strand with a 6 in tail. Drop the slip knot off the needle on the first row: it doesn't count here.", "Place a marker every 20 or 25 stitches so you can count."], "Use a long circular needle and knit back and forth, so the blanket's weight sits on the cable."],
      rib: ["Long-tail or German twisted cast on", 3, true, "A brim or cuff has to stretch over a head or hand, so it needs a stretchy edge.", ["Pull out the tail below; add a little extra for the German twisted.", "For extra stretch, cast on with a needle 1 size larger or over two needles held together.", "Long-tail as normal, or German twisted: go under both thumb strands, down into the thumb loop from above, then catch the finger strand.", "Switch to your rib needle for the first row."], "For a 1×1 rib that must look invisible, try the tubular cast on."],
      rib11: ["Tubular cast on", 3, true, "It rolls the rib round the edge, so it's very elastic and almost invisible.", ["Work it with a long tail or over waste yarn, as your tutorial or pattern shows.", "Cast on half the stitches (plus one), then work the set-up rows the method asks for.", "Work the first rows of 1×1 rib with a needle 1 or 2 sizes smaller if the edge looks loose.", "Take out any waste yarn once the rib is set."], "In a hurry? A long-tail cast on with a needle 1 size up is the next best for rib."],
      sock: ["German twisted cast on", 3, true, "Sock knitters love it: the cuff must stretch over the heel.", ["Pull out the tail below; this one uses a bit more than a plain long-tail.", "Slingshot as for the long-tail.", "Bring the needle under both thumb strands, down into the thumb loop from above, then over the finger strand and back out.", "Drop the thumb loop and snug gently. Test: the cuff must pull over your heel."], "The long-tail over two needles held together also works."],
      firm: ["Cable cast on", 1, false, "It makes a firm, corded edge that holds its shape and is great to pick up stitches from.", ["Make a slip knot and knit into it; put the new loop on the left needle.", "Put the right needle between the first two stitches on the left needle.", "Wrap and pull a loop through, then put it on the left needle.", "Repeat between the first two stitches each time."], "Not for hats, socks or cuffs: it doesn't stretch much."],
      later: ["Provisional cast on", 2, false, "You'll pull out waste yarn later and have live stitches to knit from or graft.", ["With smooth waste yarn in a contrast colour, crochet a chain a few stitches longer than you need.", "With your real yarn, pick up and knit one stitch into the back bump of each chain.", "Knit your piece.", "Later, undo the chain from the end with the knot, putting each freed stitch onto a needle."], "No crochet hook? Some provisional cast ons are worked round a spare needle or cable instead."],
      add: ["Backward loop cast on", 3, false, "It's the quickest way to add a few stitches in the middle or at the end of a row.", ["Hold the working yarn in your left hand.", "Make a loop round your thumb so the yarn crosses over itself.", "Slip the loop onto the right needle and tighten gently.", "Repeat for each stitch. Knit into them carefully on the next row: they can loosen."], "Adding stitches at the start of a row? The knitted or cable cast on is neater."]
    };
    function cnCalc() {
      var k = $("#cn-what").value, m = CNM[k], n = parseInt($("#cn-n").value, 10) || 0, g4 = parseFloat($("#cn-y").value) || 18;
      var wr = parseFloat($("#cn-wrap").value), cm = $("#cn-u").value === "cm";
      var per = wr > 0 ? (cm ? wr / 2.54 : wr) / 10 : 4.5 / (g4 / 4), extra = k === "sock" ? 1.1 : 1;
      if (!(n > 0)) { $("#cn-out").innerHTML = "<p>Enter how many stitches you'll cast on.</p>"; return; }
      var tail = n * per * extra + 6, safe = tail * 1.15;
      var u = function (inch) { return inch < 36 ? Math.round(inch) + " in" : (inch / 36).toFixed(1) + " yd"; };
      var c = function (inch) { return inch < 100 / 2.54 ? Math.round(inch * 2.54) + " cm" : (inch * 0.0254).toFixed(2) + " m"; };
      var h = "<h3>Use</h3><div class=\"big\" style=\"font-size:1.9rem;line-height:1.1\">" + esc(m[0]) + "</div>";
      h += "<p class=\"sub\">Stretch: " + "●●●".slice(0, m[1]) + "○○○".slice(0, 3 - m[1]) + ". " + esc(m[3]) + "</p>";
      if (m[2]) h += '<div class="tb-stats"><div><strong>' + u(tail) + "</strong><span>tail to pull out (" + c(tail) + ")</span></div><div><strong>" + u(safe) + "</strong><span>safe length, if you'd hate to run short</span></div><div><strong>" + (per * extra).toFixed(2) + " in</strong><span>per stitch" + (wr > 0 ? " (from your wraps)" : " (our estimate)") + "</span></div><div><strong>" + n + "</strong><span>stitches, slip knot included</span></div></div>";
      else h += '<div class="tb-stats"><div><strong>No tail to guess</strong><span>leave about 6 in (15 cm) to weave in</span></div><div><strong>' + n + "</strong><span>stitches to cast on</span></div></div>";
      h += "<h3>How</h3><ol class=\"sk-steps\">" + m[4].map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ol>";
      h += "<p class=\"sub\"><strong>Also good:</strong> " + esc(m[5]) + "</p>";
      h += '<hr><p class="sub">Tail = stitches × about 1 in per stitch at worsted gauge (Marly Bird\'s rule), scaled by gauge, plus 6 in. Our estimate; your own 10 wraps are more accurate. Next: <a href="' + (location.protocol === "file:" ? "cast-on-calculator.html" : "/cast-on-calculator") + '" style="color:#ffd38a">how many stitches to cast on</a>.</p>';
      $("#cn-out").innerHTML = h;
      // drawing: tail against a 1-yard ruler (wraps onto more lines past a yard)
      var len = m[2] ? tail : 6, g = "", x0 = 20, W = 260, yd = 36, lines = Math.ceil(len / yd), i, y;
      g += '<rect x="' + x0 + '" y="12" width="' + W + '" height="18" rx="3" fill="#f2e6cf" stroke="#c9a37a"/>';
      for (i = 0; i <= 36; i++) g += '<line x1="' + (x0 + W * i / 36).toFixed(1) + '" x2="' + (x0 + W * i / 36).toFixed(1) + '" y1="12" y2="' + (i % 12 === 0 ? 28 : (i % 6 === 0 ? 24 : 18)) + '" stroke="#1f2a44" stroke-width="' + (i % 12 === 0 ? 1.6 : 0.8) + '"/>';
      g += '<text x="' + (x0 + W) + '" y="44" text-anchor="end" font-size="10" fill="#4a5470">1 yd (91 cm)</text>';
      var gap = Math.min(16, 66 / Math.max(1, lines));
      for (i = 0; i < Math.min(lines, 8); i++) {
        var part = Math.min(1, (len - i * yd) / yd); y = 54 + i * gap;
        g += '<line x1="' + x0 + '" x2="' + (x0 + W * part).toFixed(1) + '" y1="' + y + '" y2="' + y + '" stroke="' + (i % 2 ? "#d97aa0" : "#b8326a") + '" stroke-width="4" stroke-linecap="round"/>';
      }
      if (lines > 8) g += '<text x="150" y="' + (54 + 8 * gap) + '" text-anchor="middle" font-size="10" fill="#4a5470">and ' + (lines - 8) + " more yards</text>";
      $("#cn-svg").innerHTML = g;
      $("#cn-cap").textContent = m[2] ? "The tail to pull out, about " + u(tail) + ", drawn against a 1 yard ruler." : "Only a short end to weave in: this cast on needs no long tail.";
    }
    ["#cn-what", "#cn-y", "#cn-u"].forEach(function (s) { $(s).addEventListener("change", cnCalc); });
    ["#cn-n", "#cn-wrap"].forEach(function (s) { $(s).addEventListener("input", cnCalc); });
    cnCalc();
  }

  /* ---------- CROCHET DECREASE ROUND WRITER ---------- */
  if ($("#dc-out") && $("#dc-s")) {
    var DCN = { sc: ["sc", "sc2tog"], hdc: ["hdc", "hdc2tog"], dc: ["dc", "dc2tog"] };
    // same maths as build.py dc_round: returns {txt, pairs} or null
    function dcRound(S, T, st, inv, stagger) {
      var D = S - T; if (D < 1 || 2 * D > S) return null;
      var a = Math.floor((S - 2 * D) / D), ex = (S - 2 * D) % D, s = DCN[st][0], dec = inv && st === "sc" ? "invdec" : DCN[st][1];
      var w = function (n) { return n ? s + " " + n : ""; }, j = function () { return Array.prototype.filter.call(arguments, Boolean).join(", "); };
      var seq = [], i, k; // seq: 0 plain stitch, 1 = first of a decrease pair
      var txt;
      if (a === 0 && ex === 0) { txt = dec + " around (" + T + ")"; for (i = 0; i < D; i++) seq.push(1); }
      else if (ex === 0) {
        if (stagger && a >= 2) {
          var h = Math.floor(a / 2);
          txt = j(w(h), (D > 1 ? "[" + dec + ", " + w(a) + "] × " + (D - 1) + ", " : "") + dec, w(a - h)) + " (" + T + ")";
          for (i = 0; i < h; i++) seq.push(0);
          for (k = 0; k < D; k++) { seq.push(1); if (k < D - 1) for (i = 0; i < a; i++) seq.push(0); }
          for (i = 0; i < a - h; i++) seq.push(0);
        } else { txt = "[" + j(w(a), dec) + "] × " + D + " (" + T + ")"; for (k = 0; k < D; k++) { for (i = 0; i < a; i++) seq.push(0); seq.push(1); } }
      } else {
        txt = "[" + j(w(a + 1), dec) + "] × " + ex + ", [" + j(w(a), dec) + "] × " + (D - ex) + " (" + T + ")";
        for (k = 0; k < D; k++) { for (i = 0; i < (k < ex ? a + 1 : a); i++) seq.push(0); seq.push(1); }
      }
      return { txt: txt, seq: seq };
    }
    var dcMode = $("#dc-mode"), dcWay = $("#dc-way");
    function dcCalc() {
      var close = segVal(dcMode) !== "one", S = parseInt($("#dc-s").value, 10) || 0, st = $("#dc-st").value, inv = $("#dc-type").value === "inv";
      $("#dc-t-f").hidden = close; $("#dc-per-f").hidden = !close; $("#dc-way-f").hidden = close;
      var out = $("#dc-out"), rounds = [], first = null, h = "";
      if (S < 2) { out.innerHTML = "<p>Enter how many stitches you have.</p>"; return; }
      if (close) {
        var per = parseInt($("#dc-per").value, 10), n = S, k = 0, end = Math.min(6, S - 1);
        if (S <= 6) { out.innerHTML = "<p>With " + S + " stitches or fewer you're ready to close: sew through the front loops and pull tight (steps below the helper).</p>"; $("#dc-svg").innerHTML = ""; return; }
        while (n > end && k < 60) {
          var t = Math.max(end, n - per); if (2 * (n - t) > n) t = Math.ceil(n / 2);
          var r = dcRound(n, t, st, inv, k % 2 === 1); rounds.push(r); if (!first) first = { S: n, r: r }; n = t; k++;
        }
        h = "<h3>Decrease rounds</h3><div class=\"big\" style=\"font-size:2.2rem\">" + rounds.length + " round" + (rounds.length > 1 ? "s" : "") + " <small>" + S + " → " + n + " stitches</small></div>";
        h += "<ol class=\"sk-steps\">" + rounds.map(function (r) { return "<li><code>" + esc(r.txt) + "</code></li>"; }).join("") + "</ol>";
        h += "<p class=\"sub\">Number these after your pattern's last round. Alternate rounds start halfway into the repeat so the decreases don't stack into corners.</p>";
        h += "<h3>Then close it</h3><ol class=\"sk-steps\"><li>Stuff firmly before the hole gets too small, and top up as you go.</li><li>Fasten off with a 6 in (15 cm) tail.</li><li>Sew through the front loop only of each of the last " + n + " stitches, all in the same direction, and pull tight.</li><li>Push the needle through the middle and out elsewhere, pull, and snip close.</li></ol>";
      } else {
        var T = parseInt($("#dc-t").value, 10) || 0, flat = segVal(dcWay) === "flat";
        if (T >= S) { out.innerHTML = "<p>The stitches you want must be fewer than the stitches you have. Adding stitches? Use the <a href=\"" + (location.protocol === "file:" ? "increase-decrease-calculator.html" : "/increase-decrease-calculator") + "\" style=\"color:#ffd38a\">increase evenly calculator</a>.</p>"; $("#dc-svg").innerHTML = ""; return; }
        var r1 = dcRound(S, T, st, inv, flat);
        if (!r1) { out.innerHTML = "<p class=\"tb-warn\">You can't go from " + S + " to " + T + " in one " + (flat ? "row" : "round") + " with 2-together decreases: each one only takes away 1 stitch. Do it over two rounds (first to " + Math.ceil(S / 2) + "), or use 3-together decreases.</p>"; $("#dc-svg").innerHTML = ""; return; }
        first = { S: S, r: r1 };
        h = "<h3>Work this " + (flat ? "row" : "round") + "</h3><div class=\"big\" style=\"font-size:1.5rem;line-height:1.3\"><code style=\"color:#fff;background:none\">" + esc(r1.txt) + "</code></div>";
        h += '<div class="tb-stats"><div><strong>' + (S - T) + "</strong><span>decreases</span></div><div><strong>" + (S - 2 * (S - T)) + "</strong><span>plain stitches</span></div><div><strong>" + T + "</strong><span>stitches at the end</span></div><div><strong>" + (2 * (S - T)) + "</strong><span>stitches used by the decreases</span></div></div>";
        if (flat) h += "<p class=\"sub\">Working in rows, the first and last decreases sit away from the edges, which keeps a seam or border neat. Your turning chain doesn't count here.</p>";
      }
      h += '<hr><p class="sub">Our own maths: each 2-together decrease uses 2 stitches and makes 1. ' + (inv && st !== "sc" ? "The invisible decrease is mostly used with single crochet, so taller stitches show the standard 2-together. " : "") + 'Next: <a href="' + (location.protocol === "file:" ? "how-to-weave-in-ends.html" : "/how-to-weave-in-ends") + '" style="color:#ffd38a">hide the tail</a>.</p>';
      out.innerHTML = h;
      // drawing: the first round's stitches on a circle, decrease pairs in berry
      var seq = first.r.seq, tot = first.S, g = "", cx = 150, cy = 100, R = Math.min(84, 30 + tot * 1.2), idx = 0, q, ang, x, y;
      var dot = function (i, col, big) { ang = -Math.PI / 2 + 2 * Math.PI * i / tot; x = cx + R * Math.cos(ang); y = cy + R * Math.sin(ang); return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (big ? Math.max(2.5, Math.min(6, 200 / tot)) : Math.max(2, Math.min(5, 160 / tot))) + '" fill="' + col + '"/>'; };
      g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="none" stroke="#e5d6bd" stroke-width="2"/>';
      for (q = 0; q < seq.length; q++) {
        if (seq[q]) {
          var a1 = -Math.PI / 2 + 2 * Math.PI * idx / tot, a2 = -Math.PI / 2 + 2 * Math.PI * (idx + 1) / tot;
          g += '<path d="M' + (cx + R * Math.cos(a1)).toFixed(1) + " " + (cy + R * Math.sin(a1)).toFixed(1) + " A" + R + " " + R + " 0 0 1 " + (cx + R * Math.cos(a2)).toFixed(1) + " " + (cy + R * Math.sin(a2)).toFixed(1) + '" fill="none" stroke="#b8326a" stroke-width="6" stroke-linecap="round"/>';
          g += dot(idx, "#b8326a", true) + dot(idx + 1, "#b8326a", true); idx += 2;
        } else { g += dot(idx, "#2f8f8a"); idx++; }
      }
      g += '<text x="' + cx + '" y="' + (cy - 4) + '" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2a44">' + tot + " → " + (tot - (seq.filter(Boolean).length)) + '</text><text x="' + cx + '" y="' + (cy + 12) + '" text-anchor="middle" font-size="10" fill="#4a5470">' + (close ? "first round" : "stitches") + "</text>";
      $("#dc-svg").innerHTML = g;
    }
    ["#dc-st", "#dc-type", "#dc-per"].forEach(function (s) { $(s).addEventListener("change", dcCalc); });
    ["#dc-s", "#dc-t"].forEach(function (s) { $(s).addEventListener("input", dcCalc); });
    seg(dcMode, dcCalc); seg(dcWay, dcCalc);
    dcCalc();
  }


  /* ---------- DROPPED STITCH HELPER ---------- */
  if ($("#ds-out") && $("#ds-fab")) {
    var dsFirst = $("#ds-first"), dsWhen = $("#ds-when");
    var DSF = {
      stk: ["Stockinette, knit side facing", "all"], stp: ["Stockinette, purl side facing", "turn"], gar: ["Garter stitch", "alt"],
      ribk: ["Rib, knit column", "all"], ribp: ["Rib, purl column", "turn"], seed: ["Seed or moss stitch", "alt"]
    };
    function dsCalc() {
      var f = $("#ds-fab").value, kind = DSF[f][1], rows = Math.max(1, Math.min(200, parseInt($("#ds-rows").value, 10) || 1));
      var n = Math.max(1, parseInt($("#ds-n").value, 10) || 1), mm = parseFloat($("#ds-mm").value) || 4, above = $("#ds-above").value, done = segVal(dsWhen) === "done";
      $("#ds-first-f").hidden = kind !== "alt";
      var first = segVal(dsFirst) || "k", rungs = [], i;
      for (i = 0; i < rows; i++) rungs.push(kind === "alt" ? ((i % 2 === 0) === (first === "k") ? "k" : "p") : "k");
      var lo = Math.max(1.5, Math.round((mm - 0.5) * 4) / 4), hook = (lo === mm ? mm : lo + "–" + mm) + " mm";
      var verdict, vc = "", h = "";
      if (above === "fancy") { verdict = "Rip back, or fix it with care"; vc = " tb-warn"; }
      else if (above === "shape") { verdict = "Fix it up to the shaping"; vc = " tb-warn"; }
      else if (rows <= 10) verdict = "Easy fix: ladder it up";
      else if (rows <= 30) verdict = "Fixable: ladder it up slowly";
      else { verdict = "Fixable, but think about ripping back"; vc = " tb-warn"; }
      h += "<h3>What to do</h3><div class=\"big" + vc + "\" style=\"font-size:1.7rem;line-height:1.15\">" + esc(verdict) + "</div>";
      h += '<div class="tb-stats"><div><strong>' + rows + "</strong><span>rung" + (rows > 1 ? "s" : "") + " to pick up" + (n > 1 ? ", per stitch" : "") + "</span></div><div><strong>" + hook + "</strong><span>crochet hook</span></div>";
      if (kind === "alt") { var nk = rungs.filter(function (r) { return r === "k"; }).length; h += "<div><strong>" + nk + " + " + (rows - nk) + "</strong><span>knit + purl pickups</span></div>"; }
      else h += "<div><strong>All knit</strong><span>" + (kind === "turn" ? "after you turn the work" : "pull every rung toward you") + "</span></div>";
      h += "<div><strong>" + n + "</strong><span>stitch" + (n > 1 ? "es" : "") + " to fix" + (n > 1 ? ", one at a time" : "") + "</span></div></div>";
      var st = ["Catch the loose loop" + (n > 1 ? "s, each with its own" : " with a") + " locking stitch marker or safety pin."];
      if (kind === "turn") st.push(f === "ribp" ? "Turn the work over. From the back, a purl column is a knit column." : "Turn the work so the knit side faces you. Purl stitches are knit stitches from the other side.");
      st.push("Put the hook into the loop from the front, hook pointing up.");
      if (kind === "alt") st.push("Follow the rung list below from the bottom up: for a knit rung, pull it through from the front; for a purl rung, take the hook out and put it in from the back first (or turn the work over between rungs).");
      else st.push("Catch the lowest rung and pull it through the loop. Repeat for each rung, in order, checking each new stitch matches the ones beside it.");
      if (above === "shape") st.push("Stop when you reach the row with the increase or decrease. Rip back the rows above it to that point, or work the shaping by hand with a spare needle if you know how.");
      if (above === "fancy") st.push("Ladders can't rebuild a cable cross, yarn over or colour change by themselves. Rip back to just below the drop (put a lifeline in first), or ladder up only if you know exactly how that column is worked.");
      if (n > 2) st.push("With several stitches, a spare pair of needles about the size of yours can be easier than a hook (LoveCrafts).");
      if (rows > 30 && above === "plain") st.push("A long ladder can come out tight or loose. Tug the fabric gently both ways, and wash or block it to even it out. Yarnspirations suggests ripping back once a drop is several inches down, so choose whichever feels easier.");
      st.push(done ? "At the top, sew the last loop to the bound off edge with a length of matching yarn, through the loop at least once, and weave in the ends." : "At the top, put the loop on the left needle with its front leg toward the tip, so it isn't twisted, then knit on.");
      h += "<h3>Steps</h3><ol class=\"sk-steps\">" + st.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ol>";
      if (kind === "alt") h += "<h3>Rung list, bottom first</h3><p class=\"sub\">" + rungs.slice(0, 40).map(function (r, k) { return (k + 1) + ": " + (r === "k" ? "knit (from the front)" : "purl (from the back)"); }).join(" · ") + (rows > 40 ? " · and so on, alternating" : "") + "</p>";
      h += '<hr><p class="sub">Our own advice, from the methods in Yarnspirations, Dummies and LoveCrafts. Row limits are rough guides. Next: <a href="' + (location.protocol === "file:" ? "row-counter.html" : "/row-counter") + '" style="color:#ffd38a">count your rows</a> so you know where you are.</p>';
      $("#ds-out").innerHTML = h;
      // drawing: ladder (max 12 rungs drawn), knit columns either side
      var show = Math.min(rows, 12), g = "", x = 150, top = 26, step = Math.min(16, 150 / (show + 1)), base = top + step * (show + 1) + 8, c, k;
      g += '<rect x="40" y="14" width="220" height="' + (base + 12 - 14) + '" rx="10" fill="#f2e6cf"/>';
      for (c = -3; c <= 3; c++) {
        if (c === 0) continue;
        for (k = 0; k <= show + 1; k++) {
          var yy = top + k * step, xx = x + c * 26;
          g += '<path d="M' + (xx - 7) + " " + (yy - 6) + " Q" + xx + " " + (yy + 2) + " " + xx + " " + (yy + 6) + " M" + (xx + 7) + " " + (yy - 6) + " Q" + xx + " " + (yy + 2) + " " + xx + " " + (yy + 6) + '" fill="none" stroke="#d97aa0" stroke-width="2" stroke-linecap="round"/>';
        }
      }
      for (k = 0; k < show; k++) {
        var r = rungs[k], y = base - 14 - (k + 1) * step + 4, col = r === "k" ? "#2f8f8a" : "#f4a823";
        g += '<path d="M' + (x - 15) + " " + y + " Q" + x + " " + (y + 4) + " " + (x + 15) + " " + y + '" fill="none" stroke="' + col + '" stroke-width="3" stroke-linecap="round"/>';
        if (kind === "alt" || k === 0) g += '<text x="' + (x + 116) + '" y="' + (y + 4) + '" font-size="10" fill="#1f2a44">' + (k + 1) + " " + (r === "k" ? "K" : "P") + "</text>";
      }
      g += '<ellipse cx="' + x + '" cy="' + (base - 8) + '" rx="7" ry="10" fill="#fbfcfa" stroke="#b8326a" stroke-width="3"/>';
      g += '<text x="' + (x + 14) + '" y="' + (base + 4) + '" font-size="10" fill="#4a5470">loose loop</text>';
      if (rows > show) g += '<text x="' + x + '" y="10" text-anchor="middle" font-size="10" fill="#4a5470">+ ' + (rows - show) + " more rungs above</text>";
      $("#ds-svg").setAttribute("viewBox", "0 0 300 " + Math.round(base + 14));
      $("#ds-svg").innerHTML = g;
      $("#ds-cap").textContent = kind === "alt" ? "Teal rungs are knit pickups, gold are purl. Work from the bottom up." : "Every rung is a knit pickup" + (kind === "turn" ? " once the work is turned" : "") + ". Work from the bottom up.";
    }
    ["#ds-fab", "#ds-above"].forEach(function (s) { $(s).addEventListener("change", dsCalc); });
    ["#ds-rows", "#ds-n", "#ds-mm"].forEach(function (s) { $(s).addEventListener("input", dsCalc); });
    seg(dsFirst, dsCalc); seg(dsWhen, dsCalc);
    dsCalc();
  }

  /* ---------- CROCHET BLANKET PRICE CALCULATOR ---------- */
  if ($("#bp-out") && $("#bp-size")) {
    var BPTF = { 1: 1.45, 2: 1.35, 3: 1.2, 4: 1, 5: 0.75, 6: 0.6, 7: 0.45 }, bpCraft = $("#bp-craft");
    var bpWM = {}; (P.weights || []).forEach(function (w) { bpWM[w.n] = w.m; });
    var money = function (x) { return "$" + (x >= 100 ? Math.round(x).toLocaleString("en-US") : x.toFixed(2)); };
    function bpCalc() {
      var id = $("#bp-size").value, b, custom = id === "custom";
      $("#bp-custom").hidden = !custom;
      if (custom) b = { name: "Your blanket", w: parseFloat($("#bp-w").value) || 0, l: parseFloat($("#bp-l").value) || 0 };
      else b = (P.blankets || []).filter(function (x) { return x.id === id; })[0];
      var out = $("#bp-out");
      if (!b || !(b.w > 0 && b.l > 0)) { out.innerHTML = "<p>Enter the blanket's width and length.</p>"; return; }
      var knit = segVal(bpCraft) === "knit", wn = parseInt($("#bp-weight").value, 10), sk = parseFloat($("#bp-sk").value) || 200, cost = parseFloat($("#bp-cost").value) || 0;
      var extra = parseFloat($("#bp-extra").value) || 0, speed = parseFloat($("#bp-speed").value) || 1, rate = parseFloat($("#bp-rate").value) || 0, oh = (parseFloat($("#bp-oh").value) || 0) / 100;
      var yd = b.w * b.l * 0.667 * (bpWM[wn] || 1) * (knit ? 1 : 1.27), skeins = Math.ceil(yd / sk), mat = skeins * cost + extra;
      var est = b.w * b.l * 25 / 3000 * BPTF[wn] * (knit ? 2 : 1) * speed, hIn = parseFloat($("#bp-h").value), hrs = hIn > 0 ? hIn : est;
      $("#bp-h-note").textContent = hIn > 0 ? "Our estimate was about " + Math.round(est) + " h." : "Leave empty to use our estimate (about " + Math.round(est) + " h).";
      var labour = hrs * rate, base = (mat + labour) * (1 + oh), ch = $("#bp-ch").value, price, fees;
      if (ch === "etsy") price = (base + 0.45) / (1 - 0.095); else if (ch === "fair") price = base / 0.97; else price = base;
      fees = price - base;
      var r5 = function (x) { return "$" + (Math.round(x / 5) * 5).toLocaleString("en-US"); };
      var x3 = mat * 3, x3h = Math.max(0, (x3 * (ch === "etsy" ? 0.905 : ch === "fair" ? 0.97 : 1) - (ch === "etsy" ? 0.45 : 0) - mat) / hrs);
      var dc = mat * 2 + labour;
      var h = "<h3>Fair price</h3><div class=\"big\">" + r5(price) + " <small>" + (ch === "etsy" ? "on Etsy" : ch === "fair" ? "at a craft fair" : "direct") + "</small></div>";
      h += "<p class=\"sub\">" + esc(b.name) + ", " + b.w + " × " + b.l + " in, " + (knit ? "knitted" : "crocheted") + ". Plus shipping, charged separately.</p>";
      h += '<div class="tb-stats"><div><strong>' + fmt(yd) + " yd</strong><span>yarn, about " + skeins + " skein" + (skeins > 1 ? "s" : "") + " (" + money(skeins * cost) + ")</span></div><div><strong>" + (Math.round(hrs * 2) / 2) + " h</strong><span>" + (hIn > 0 ? "your hours" : "our estimate of the hours") + "</span></div>";
      h += "<div><strong>" + money(labour) + "</strong><span>your pay at $" + rate + "/h</span></div><div><strong>" + money(fees) + "</strong><span>" + (ch === "direct" ? "no fees" : "fees covered") + "</span></div></div>";
      h += "<h3>Other ways to work it out</h3><ul class=\"sk-steps\"><li><strong>Materials × 2 + labour</strong> (Daisy Cottage Designs' method): about " + r5(dc) + " before fees, with doubled yarn standing in for overheads.</li><li><strong>Materials × 3:</strong> " + r5(x3) + ", which would pay you about <strong>$" + x3h.toFixed(2) + " an hour</strong>.</li></ul>";
      var tr = parseFloat($("#bp-try").value);
      if (tr > 0) {
        var net = ch === "etsy" ? tr * 0.905 - 0.45 : ch === "fair" ? tr * 0.97 : tr, ph = (net / (1 + oh) - mat) / hrs;
        h += "<p class=\"sub" + (ph < rate ? " tb-warn" : "") + "\">At " + money(tr) + " you'd earn about <strong>$" + ph.toFixed(2) + " an hour</strong>" + (ph < rate ? ", less than the $" + rate + " you set." : ". Nice.") + "</p>";
      }
      if (price > 300 && !knit && wn < 6) h += "<p class=\"sub\">Price feels high? The same size in super bulky yarn would take about " + Math.round(b.w * b.l * 25 / 3000 * BPTF[6] * speed) + " h instead of " + Math.round(est) + ".</p>";
      h += '<hr><p class="sub">Hours and yarn are our estimates for plain stitches (LoveCrafts\' 25 h for a crocheted throw, scaled by size and yarn). Etsy: 6.5% + 3% + $0.25 + $0.20 listing (US). Next: <a href="' + (location.protocol === "file:" ? "how-to-price-crochet-items.html" : "/how-to-price-crochet-items") + '" style="color:#ffd38a">pricing other crochet items</a>.</p>';
      out.innerHTML = h;
      // stacked bar: yarn, time, overheads, fees
      var parts = [["Yarn and extras", mat, "#f4a823"], ["Your time", labour, "#b8326a"], ["Overheads", (mat + labour) * oh, "#2f8f8a"], ["Fees", fees, "#4a5470"]];
      var tot = parts.reduce(function (a, p) { return a + p[1]; }, 0) || 1, X = 20, W = 260, g = "", k;
      parts.forEach(function (p, i) {
        var w = W * p[1] / tot; if (w > 0) g += '<rect x="' + X.toFixed(1) + '" y="24" width="' + w.toFixed(1) + '" height="34" fill="' + p[2] + '"' + (i === 0 ? ' rx="4"' : "") + "/>"; X += w;
      });
      for (k = 0; k < 4; k++) {
        var p = parts[k], yy = 84 + k * 16;
        g += '<rect x="20" y="' + (yy - 9) + '" width="10" height="10" rx="2" fill="' + p[2] + '"/><text x="36" y="' + yy + '" font-size="11" fill="#1f2a44">' + p[0] + '</text><text x="280" y="' + yy + '" font-size="11" text-anchor="end" fill="#1f2a44">' + money(p[1]) + " (" + Math.round(p[1] / tot * 100) + "%)</text>";
      }
      g += '<text x="20" y="16" font-size="11" fill="#4a5470">What the price is made of</text>';
      $("#bp-svg").innerHTML = g;
      $("#bp-cap").textContent = "Your time is " + Math.round(labour / tot * 100) + "% of this blanket's price.";
    }
    ["#bp-size", "#bp-weight", "#bp-speed", "#bp-ch"].forEach(function (s) { $(s).addEventListener("change", bpCalc); });
    ["#bp-w", "#bp-l", "#bp-sk", "#bp-cost", "#bp-extra", "#bp-h", "#bp-rate", "#bp-oh", "#bp-try"].forEach(function (s) { $(s).addEventListener("input", bpCalc); });
    seg(bpCraft, bpCalc);
    bpCalc();
  }



  /* ---------- KNIT IN THE ROUND: circular needle length finder ---------- */
  if ($("#kr-out") && $("#kr-c")) {
    var krMode = $("#kr-mode"), krUnit = $("#kr-unit");
    var KRL = [[9, 23], [12, 30], [16, 40], [24, 60], [32, 80], [40, 100], [47, 120], [60, 150]];
    var krLast = "in";
    function krCalc() {
      var u = segVal(krUnit) || "in", mode = segVal(krMode) || "size", f = u === "cm" ? 2.54 : 1;
      if (u !== krLast) { // convert the typed values when the unit changes
        var k = u === "cm" ? 2.54 : 1 / 2.54;
        $("#kr-c").value = Math.round(parseFloat($("#kr-c").value || 0) * k * 2) / 2;
        $("#kr-g").value = Math.round(parseFloat($("#kr-g").value || 0) * 2) / 2;
        krLast = u;
      }
      $("#kr-c-l").textContent = "Size around (" + u + ")";
      $("#kr-g-l").textContent = u === "cm" ? "Stitches per 10 cm" : "Stitches per 4 in";
      $("#kr-size-f").hidden = mode !== "size"; $("#kr-sts-f").hidden = mode !== "sts";
      var c; // circumference in inches
      if (mode === "sts") {
        var n = Math.max(1, parseInt($("#kr-n").value, 10) || 1), g = Math.max(1, parseFloat($("#kr-g").value) || 20);
        c = u === "cm" ? n / g * 10 / 2.54 : n / g * 4;
      } else c = Math.max(1, parseFloat($("#kr-c").value) || 1) / f;
      var lim = c < 12 ? c * 1.1 : c, ok = KRL.filter(function (l) { return l[0] <= lim; }), best = ok.length ? ok[ok.length - 1] : null;
      var nxt = best ? KRL.filter(function (l) { return l[0] > best[0]; })[0] : KRL[0];
      var len = function (l) { return u === "cm" ? l[1] + " cm" : l[0] + " in"; };
      var cs = u === "cm" ? (c * 2.54).toFixed(0) + " cm" : c.toFixed(1).replace(/\.0$/, "") + " in";
      var h = "<h3>Your needle</h3>";
      if (best) {
        var ratio = c / best[0];
        h += '<div class="big" style="font-size:1.9rem;line-height:1.15">' + len(best) + " circular</div>";
        h += '<div class="tb-stats"><div><strong>' + cs + "</strong><span>around your project</span></div><div><strong>" + (ratio < 1 ? "Slight stretch" : ratio <= 1.6 ? "Comfortable" : "Crowded") + "</strong><span>stitches on the needle</span></div><div><strong>" + (c < 30 ? (u === "cm" ? "80 cm+" : "32 in+") : (u === "cm" ? "100 cm+" : "40 in+")) + "</strong><span>for magic loop instead</span></div></div>";
        var tips = [];
        if (ratio < 1) tips.push("The needle is a little longer than the project, so the stitches stretch slightly to meet. That's usually fine for socks and sleeves; if it feels tight, use magic loop.");
        if (ratio > 1.6) tips.push("That's a lot of stitches for this length. " + (nxt ? "If you have a " + len(nxt) + " that's no longer than the project, it'll be roomier." : "") + " Longer cables are easier to knit with on big projects.");
        if (nxt) tips.push("Don't go longer than " + len(best) + ": a " + len(nxt) + " needle won't let the stitches reach round.");
        if (c < 22) tips.push("At the crown or toe, the stitches get too few for any circular. Change to magic loop or DPNs then.");
        h += "<h3>Good to know</h3><ul class=\"sk-steps\">" + tips.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>";
      } else {
        h += '<div class="big tb-warn" style="font-size:1.6rem;line-height:1.15">Too small for a circular</div>';
        h += '<div class="tb-stats"><div><strong>' + cs + "</strong><span>around your project</span></div><div><strong>" + (u === "cm" ? "80 cm+" : "32 in+") + "</strong><span>circular for magic loop</span></div><div><strong>4 or 5</strong><span>DPNs, or 2 circulars</span></div></div>";
        h += "<p class=\"sub\">Even a 9 in (23 cm) circular is too long, so the stitches won't reach round. Use magic loop on a 32 in (80 cm) or 40 in (100 cm) circular, double-pointed needles, or two circulars.</p>";
      }
      var st = (mode === "sts" ? parseInt($("#kr-n").value, 10) || 0 : 0);
      var join = ["Cast on" + (st ? " " + st + " stitches" : "") + ", spread them round the cable and check the cast-on edge sits on the inside, with no twist.", "Slip a marker onto the right tip, the one with the working yarn.", "Knit the first stitch on the left tip with the working yarn, pull it snug, and knit to the marker."];
      if (st > 150) join.splice(1, 0, "With this many stitches, a twist is easy to miss. Cocoknits' trick: knit one row flat first, then join, and sew the tiny gap with the tail later.");
      h += "<h3>Join without twisting</h3><ol class=\"sk-steps\">" + join.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ol>";
      var hr = location.protocol === "file:" ? function (x) { return x + ".html"; } : function (x) { return "/" + x; };
      h += '<hr><p class="sub">Our rule: the longest common circular no longer than the project (up to about 10% longer for socks and sleeves, which stretch) (Knit Picks and Elizabeth Smith Knits say shorter than the circumference). Next: <a href="' + hr("cast-on-calculator") + '" style="color:#ffd38a">how many stitches to cast on</a> or the <a href="' + hr("hat-size-chart") + '" style="color:#ffd38a">hat size calculator</a>.</p>';
      $("#kr-out").innerHTML = h;
      // drawing: project circle vs needle circle, same scale
      var maxIn = Math.max(c, best ? best[0] : 9), sc = 80 / (maxIn / Math.PI / 2), rp = c / Math.PI / 2 * sc, rn = (best ? best[0] : 9) / Math.PI / 2 * sc, g2 = "";
      g2 += '<circle cx="150" cy="105" r="' + rp.toFixed(1) + '" fill="#f6dbe6" stroke="#b8326a" stroke-width="5" stroke-dasharray="2 5" stroke-linecap="round"/>';
      g2 += '<circle cx="150" cy="105" r="' + rn.toFixed(1) + '" fill="none" stroke="' + (best ? "#f4a823" : "#4a5470") + '" stroke-width="3"' + (best ? "" : ' stroke-dasharray="6 4"') + "/>";
      g2 += '<text x="150" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2a44">' + cs + '</text><text x="150" y="121" text-anchor="middle" font-size="11" fill="#4a5470">needle ' + (best ? len(best) : "9 in: too long") + "</text>";
      $("#kr-svg").innerHTML = g2;
      $("#kr-cap").textContent = best ? "Your project (pink) and the " + len(best) + " needle (gold), to scale. The needle should be the same size or a little smaller." : "Your project (pink) is smaller than the shortest circular (grey).";
    }
    $("#kr-proj").addEventListener("change", function () {
      var v = $("#kr-proj").value; if (v !== "own") $("#kr-c").value = segVal(krUnit) === "cm" ? Math.round(parseFloat(v) * 2.54) : v; krCalc();
    });
    $("#kr-c").addEventListener("input", function () { $("#kr-proj").value = "own"; krCalc(); });
    ["#kr-n", "#kr-g"].forEach(function (s) { $(s).addEventListener("input", krCalc); });
    seg(krMode, krCalc); seg(krUnit, krCalc);
    krCalc();
  }

  /* ---------- JUNK JOURNAL SUPPLY CHECKLIST ---------- */
  if ($("#js-list") && $("#js-out")) {
    var JK = "pp-jj-supplies", JSS = store.get(JK, {}) || {};
    if (!JSS.t) JSS = { t: {}, plan: "basic" };
    var jsBoxes = $$("#js-list input[type=checkbox]"), jsPlan = $("#js-plan");
    if (JSS.plan) $$("button", jsPlan).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === JSS.plan); });
    var LV = { free: 0, basic: 1, extra: 2 }, TN = { free: "free from home", basic: "worth buying first", extra: "nice to have" };
    function jsCalc() {
      var n = 0;
      jsBoxes.forEach(function (b) { b.checked = !!JSS.t[b.getAttribute("data-id")]; if (b.checked) n++; });
      $("#js-count").textContent = n + " of " + jsBoxes.length + " ticked";
      $$("#js-list .ep-gc").forEach(function (sp) {
        var g = sp.getAttribute("data-g"), all = $$('#js-list fieldset[data-g="' + g + '"] input'), k = all.filter(function (b) { return b.checked; }).length;
        sp.textContent = k + "/" + all.length;
      });
      var plan = segVal(jsPlan) || "basic", lim = LV[plan];
      var miss = jsBoxes.filter(function (b) { return !b.checked && LV[b.getAttribute("data-t")] <= lim; });
      var core = ["base-paper-for-the-pages", "base-a-cover", "base-thread-or-string", "tools-scissors", "glue-glue-stick"];
      var coreMiss = core.filter(function (id) { return !JSS.t[id]; }).length;
      var h = '<div class="big" style="font-size:1.6rem;line-height:1.15">' + (coreMiss === 0 ? "You're ready to start" : coreMiss + " must-have" + (coreMiss > 1 ? "s" : "") + " to find") + "</div>";
      h += '<p class="sub">Must-haves: paper, a cover, thread, scissors and a glue stick (or any glue).</p>';
      var gath = miss.filter(function (b) { return b.getAttribute("data-t") === "free"; }), buy = miss.filter(function (b) { return b.getAttribute("data-t") !== "free"; });
      var li = function (b) { var sw = b.getAttribute("data-s"); return "<li><strong>" + esc(b.getAttribute("data-n")) + "</strong>" + (sw ? " <span class=\"sub\">(or free: " + esc(sw.toLowerCase()) + ")</span>" : "") + "</li>"; };
      if (gath.length) h += "<h3>Gather from home (" + gath.length + ")</h3><ul class=\"sk-steps\">" + gath.map(li).join("") + "</ul>";
      if (buy.length) h += "<h3>Shopping list (" + buy.length + ")</h3><ul class=\"sk-steps\">" + buy.map(li).join("") + "</ul>";
      if (!miss.length) h += "<p>You've got everything on this plan. " + (plan !== "extra" ? "Switch to the next plan to see what to add later." : "Time to make a page!") + "</p>";
      var hr = location.protocol === "file:" ? function (x) { return x + ".html"; } : function (x) { return "/" + x; };
      h += '<hr><p class="sub">Next: <a href="' + hr("junk-journal-signature-calculator") + '" style="color:#ffd38a">plan your signatures</a>, gather <a href="' + hr("junk-journal-ephemera-ideas") + '" style="color:#ffd38a">free ephemera</a> or get a <a href="' + hr("journal-prompts") + '" style="color:#ffd38a">journal prompt</a>.</p>';
      $("#js-out").innerHTML = h;
    }
    $("#js-list").addEventListener("change", function (ev) {
      var b = ev.target; if (!b.matches("input[type=checkbox]")) return;
      if (b.checked) JSS.t[b.getAttribute("data-id")] = 1; else delete JSS.t[b.getAttribute("data-id")];
      store.set(JK, JSS); jsCalc();
    });
    seg(jsPlan, function (v) { JSS.plan = v; store.set(JK, JSS); jsCalc(); });
    $("#js-clear").addEventListener("click", function () { if (!confirm("Clear all your ticks?")) return; JSS.t = {}; store.set(JK, JSS); jsCalc(); toast("Ticks cleared"); });
    $("#js-print").addEventListener("click", function () { window.print(); });
    var tp = $("#js-tpl-print");
    if (tp) tp.addEventListener("click", function () {
      document.documentElement.classList.add("print-tpl");
      var off = function () { document.documentElement.classList.remove("print-tpl"); window.removeEventListener("afterprint", off); };
      window.addEventListener("afterprint", off);
      window.print();
      setTimeout(off, 1500);
    });
    jsCalc();
  }


  /* ---------- PICK UP STITCHES calculator ---------- */
  if ($("#pu-out") && $("#pu-edge")) {
    var puHow = $("#pu-how"), puFlat = $("#pu-flat");
    var gcd = function (a, b) { while (b) { var t = b; b = a % b; a = t; } return a; };
    var puLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#ffd38a">' + t + "</a>"; };
    function puRib(n, mult, extra) { var k = Math.max(1, Math.round((n - extra) / mult)); return mult * k + extra; }
    // even sequence of picks (true) and skips (false) for N picks along E units, N <= E
    function puSeq(E, N) {
      var out = [], i, S = E - N;
      if (S <= 0) { for (i = 0; i < E; i++) out.push(true); return out; }
      if (N >= S) {
        var q = Math.floor(N / S), r = N - q * S;
        for (i = 0; i < S; i++) { var sz = q + (Math.floor((i + 1) * r / S) - Math.floor(i * r / S)); for (var j = 0; j < sz; j++) out.push(true); out.push(false); }
      } else {
        var q2 = Math.floor(S / N), r2 = S - q2 * N;
        for (i = 0; i < N; i++) { out.push(true); var sk = q2 + (Math.floor((i + 1) * r2 / N) - Math.floor(i * r2 / N)); for (var k = 0; k < sk; k++) out.push(false); }
      }
      return out;
    }
    function puCalc() {
      var edge = $("#pu-edge").value, top = edge === "top", unit = top ? "stitch" : "row", units = top ? "stitches" : "rows";
      var measure = segVal(puHow) === "measure";
      $("#pu-count-f").hidden = measure; $("#pu-measure-f").hidden = !measure;
      $("#pu-n-l").textContent = top ? "Stitches along the edge" : "Rows along the edge";
      $("#pu-n-note").textContent = edge === "garter" ? "Count the ridges and double it (1 ridge = 2 rows)." : top ? "Count the stitches of the cast on or bound off edge." : "Count the rows, or measure instead.";
      var cm = $("#pu-unit").value === "cm";
      $("#pu-g-l").textContent = (top ? "Stitches" : "Rows") + " in " + (cm ? "10 cm" : "4 in") + " of the body";
      var E = measure ? Math.round((parseFloat($("#pu-len").value) || 0) * (parseFloat($("#pu-g").value) || 0) / (cm ? 10 : 4)) : Math.round(parseFloat($("#pu-n").value) || 0);
      var rsel = $("#pu-ratio").value, ratio, rname;
      $("#pu-gauge-f").hidden = rsel !== "gauge";
      if (rsel === "auto") ratio = top ? 1 : edge === "garter" ? 0.5 : 0.75;
      else if (rsel === "gauge") { var bg = parseFloat($("#pu-bg").value) || 0, rg = parseFloat($("#pu-rg").value) || 0; ratio = rg > 0 ? bg / rg : 0.75; }
      else ratio = parseFloat(rsel);
      var names = { "1": "1 in every " + unit, "0.75": "3 for every 4 rows", "0.6667": "2 for every 3 rows", "0.8": "4 for every 5 rows", "0.5": "1 for every 2 rows (1 per ridge)" };
      rname = rsel === "gauge" ? "your gauge (" + ratio.toFixed(2) + " stitches per row)" : names[String(ratio)] || ratio.toFixed(2);
      var out = $("#pu-out");
      if (!(E >= 2)) { out.innerHTML = "<h3>Stitches to pick up</h3><div class=\"big\">–</div><p class=\"sub\">Enter the " + units + " along the edge, or measure it.</p>"; $("#pu-svg").innerHTML = ""; return; }
      var tIn = parseInt($("#pu-target").value, 10), hasT = tIn > 0, band = $("#pu-band").value, round = segVal(puFlat) === "round";
      var raw = Math.max(1, Math.round(E * ratio)), N = raw, note = "";
      var mult = band === "r1" ? 2 : band === "r2" ? 4 : 0, extra = round ? 0 : (band === "r1" ? 1 : band === "r2" ? 2 : 0);
      if (hasT) {
        N = tIn;
        if (mult && (N - extra) % mult !== 0) note = "Heads up: " + N + " isn't a multiple of " + mult + (extra ? " + " + extra : "") + ", so the " + (band === "r1" ? "1×1" : "2×2") + " rib won't match at both ends. Follow the pattern if it says so.";
      } else if (mult) {
        N = puRib(raw, mult, extra);
        if (N !== raw) note = "Rounded from " + raw + " to " + N + " so the " + (band === "r1" ? "1×1" : "2×2") + " rib works out (a multiple of " + mult + (extra ? " + " + extra : "") + ").";
      }
      var h = "<h3>Stitches to pick up</h3><div class=\"big\">" + fmt(N) + " <small>along " + fmt(E) + " " + units + "</small></div>";
      h += "<p class=\"sub\">" + (hasT ? "Your pattern's number." : "At " + esc(rname) + ".") + (note ? " " + esc(note) : "") + "</p>";
      var how;
      if (N === E) how = "Pick up 1 in every " + unit + ".";
      else if (N > E) how = "That's more stitches than " + units + ". Pick up 1 in every " + unit + " (" + fmt(E) + "), then increase " + fmt(N - E) + " evenly on the next row, or pick up an extra stitch between " + units + " " + fmt(N - E) + " times along the edge.";
      else {
        var S = E - N, g = gcd(N, E);
        if (N >= S) {
          var q = Math.floor(N / S), r = N - q * S;
          how = r === 0 ? "<strong>Pick up " + q + ", skip 1</strong>, all the way along (" + S + " times)." :
            "<strong>Pick up " + q + ", skip 1</strong>, and in " + r + " of the " + S + " repeats pick up " + (q + 1) + " instead of " + q + ". Spread those out.";
        } else {
          var q2 = Math.floor(S / N), r2 = S - q2 * N;
          how = r2 === 0 ? "<strong>Pick up 1, skip " + q2 + "</strong>, all the way along." : "<strong>Pick up 1, skip " + q2 + "</strong>, and skip " + (q2 + 1) + " instead in " + r2 + " of the " + N + " repeats.";
        }
        if (E / g <= 12 && E / g > 1) how += " That's exactly " + (N / g) + " for every " + (E / g) + " " + units + ".";
      }
      h += "<h3>How to space them</h3><p>" + how + "</p>";
      var secs = E >= 40 ? 4 : E >= 16 ? 2 : 1;
      if (secs > 1) {
        h += "<h3>Markers</h3><p class=\"sub\">Put " + (secs - 1) + " locking markers on the edge to split it into " + secs + " equal parts, then check your count at each one:</p><ul class=\"sk-steps\">";
        var a0 = 0;
        for (var i = 0; i < secs; i++) {
          var eu = Math.floor((i + 1) * E / secs) - Math.floor(i * E / secs), nu = Math.floor((i + 1) * N / secs) - Math.floor(i * N / secs);
          h += "<li>Part " + (i + 1) + ": " + units + " " + (a0 + 1) + "–" + (a0 + eu) + ", pick up <strong>" + nu + "</strong></li>"; a0 += eu;
        }
        h += "</ul>";
      }
      h += "<p class=\"sub\">Tip: pick up with a needle a size or two smaller than the band's, then switch on the next row.</p>";
      h += '<hr><p class="sub">Ratios: Wikipedia, Purl Soho, Knotions, Interweave. Spacing and rounding are our own sums. Next: ' + puLink("how-to-bind-off-knitting", "a stretchy bind off for the band") + " or " + puLink("increase-decrease-calculator", "fix the count evenly") + ".</p>";
      out.innerHTML = h;
      // drawing: first up to 24 units of the edge
      var show = Math.min(E, 24), seq = N <= E ? puSeq(E, N) : [], g2 = "", cw = 260 / show;
      g2 += '<rect x="20" y="40" width="260" height="70" rx="6" fill="#f2e6cf"/><text x="20" y="22" font-size="11" fill="#4a5470">First ' + show + " " + units + " of " + fmt(E) + (top ? "" : ", edge along the top") + "</text>";
      for (var u = 0; u < show; u++) {
        var x = 20 + cw * (u + 0.5), pick = N > E ? true : seq[u];
        g2 += '<line x1="' + x.toFixed(1) + '" y1="56" x2="' + x.toFixed(1) + '" y2="104" stroke="#d97aa0" stroke-width="' + Math.max(1, Math.min(3, cw / 4)).toFixed(1) + '" stroke-linecap="round" opacity=".55"/>';
        g2 += pick ? '<circle cx="' + x.toFixed(1) + '" cy="40" r="' + Math.min(6, cw / 2.4).toFixed(1) + '" fill="#2f8f8a"/>' : '<text x="' + x.toFixed(1) + '" y="44" font-size="12" text-anchor="middle" fill="#b8326a" font-weight="700">×</text>';
      }
      g2 += '<circle cx="26" cy="132" r="5" fill="#2f8f8a"/><text x="36" y="136" font-size="11" fill="#1f2a44">pick up</text><text x="100" y="136" font-size="12" fill="#b8326a" font-weight="700">×</text><text x="112" y="136" font-size="11" fill="#1f2a44">skip this ' + unit + "</text>";
      $("#pu-svg").innerHTML = g2;
      $("#pu-cap").textContent = N >= E ? "Every " + unit + " gets a stitch." : "Pick up at the teal dots, skip the crosses, and keep the same rhythm to the end.";
    }
    ["#pu-edge", "#pu-ratio", "#pu-band", "#pu-unit"].forEach(function (s) { $(s).addEventListener("change", puCalc); });
    ["#pu-n", "#pu-len", "#pu-g", "#pu-bg", "#pu-rg", "#pu-target"].forEach(function (s) { $(s).addEventListener("input", puCalc); });
    seg(puHow, puCalc); seg(puFlat, puCalc);
    puCalc();
  }

  /* ---------- AMIGURUMI price calculator ---------- */
  if ($("#am-out") && $("#am-size")) {
    var AMG = { 1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8 }, AMSPM = 12;
    var amLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#ffd38a">' + t + "</a>"; };
    function amPreset() {
      var o = $("#am-size").selectedOptions[0];
      $("#am-custom").hidden = $("#am-size").value !== "custom";
      if (o && o.getAttribute("data-h")) {
        $("#am-parts").value = o.getAttribute("data-parts"); $("#am-cx").value = o.getAttribute("data-cx");
        $("#am-y").value = o.getAttribute("data-y"); $("#am-o").value = o.getAttribute("data-o");
      }
      amCalc();
    }
    function amCalc() {
      var o = $("#am-size").selectedOptions[0], hIn = o && o.getAttribute("data-h") ? parseFloat(o.getAttribute("data-h")) : (parseFloat($("#am-hgt").value) || 0) / ($("#am-hu").value === "cm" ? 2.54 : 1);
      var cur = $("#am-cur").value, money = function (x) { return cur + (x >= 100 ? Math.round(x).toLocaleString("en-US") : x.toFixed(2)); };
      var out = $("#am-out");
      if (!(hIn > 0)) { out.innerHTML = "<p>Enter the toy's height.</p>"; return; }
      var w = parseInt($("#am-w").value, 10), cx = parseFloat($("#am-cx").value) || 1.3, parts = Math.max(0, parseInt($("#am-parts").value, 10) || 0), face = $("#am-face").value;
      var speed = parseFloat($("#am-speed").value) || 1, spsi = Math.pow((AMG[w] || 12) * 1.25 / 4, 2), sts = Math.PI * hIn * hIn * spsi * cx;
      var hC = sts / (AMSPM * 60) * speed, hP = parts * 10 / 60 * speed, hF = (face === "eyes" ? 5 : 20) / 60 * speed, hS = (10 + hIn * 1.5) / 60 * speed;
      var est = hC + hP + hF + hS, hIn2 = parseFloat($("#am-h").value), hrs = hIn2 > 0 ? hIn2 : est;
      $("#am-h-note").textContent = hIn2 > 0 ? "Our estimate was about " + est.toFixed(1) + " h." : "Leave empty to use our estimate (about " + est.toFixed(1) + " h).";
      var mat = (parseFloat($("#am-y").value) || 0) + (parseFloat($("#am-o").value) || 0), rate = parseFloat($("#am-rate").value) || 0, oh = (parseFloat($("#am-oh").value) || 0) / 100;
      var labour = hrs * rate, base = (mat + labour) * (1 + oh), ch = $("#am-ch").value, price;
      if (ch === "etsy") price = (base + 0.45) / (1 - 0.095); else if (ch === "fair") price = base / 0.97; else price = base;
      var fees = price - base, nice = price < 20 ? Math.ceil(price) : Math.ceil(price / 5) * 5;
      var h = "<h3>Fair price</h3><div class=\"big\">" + cur + nice.toLocaleString("en-US") + " <small>" + (ch === "etsy" ? "on Etsy" : ch === "fair" ? "at a craft fair" : "direct") + "</small></div>";
      h += "<p class=\"sub\">A " + (Math.round(hIn * 2) / 2) + " in (" + Math.round(hIn * 2.54) + " cm) toy, about " + fmt(Math.round(sts / 50) * 50) + " stitches" + (parts ? " plus " + parts + " part" + (parts > 1 ? "s" : "") + " to sew on" : "") + ". Exact: " + money(price) + ". Shipping is extra.</p>";
      h += '<div class="tb-stats"><div><strong>' + (Math.round(hrs * 4) / 4) + " h</strong><span>" + (hIn2 > 0 ? "your hours" : "our estimate") + "</span></div><div><strong>" + money(mat) + "</strong><span>materials</span></div>";
      h += "<div><strong>" + money(labour) + "</strong><span>your pay at " + cur + rate + "/h</span></div><div><strong>" + money(fees) + "</strong><span>" + (ch === "direct" ? "no fees" : "fees covered") + "</span></div></div>";
      var x3 = mat * 3, x3h = hrs > 0 ? Math.max(0, (x3 - mat) / hrs) : 0;
      h += "<h3>Compare</h3><ul class=\"sk-steps\"><li><strong>Materials × 3:</strong> " + money(x3) + ", which pays you about <strong>" + money(x3h) + " an hour</strong>.</li><li><strong>Wholesale to a shop:</strong> about " + money(base) + "; the shop adds its own markup.</li></ul>";
      var tr = parseFloat($("#am-try").value);
      if (tr > 0) {
        var net = ch === "etsy" ? tr * 0.905 - 0.45 : ch === "fair" ? tr * 0.97 : tr, ph = hrs > 0 ? (net / (1 + oh) - mat) / hrs : 0;
        h += "<p class=\"sub" + (ph < rate ? " tb-warn" : "") + "\">At " + money(tr) + " you'd earn about <strong>" + money(Math.max(0, ph)) + " an hour</strong>" + (ph < rate ? ", less than the " + cur + rate + " you set." : ". Nice.") + "</p>";
        if (ph < rate && rate > 0) { var fitH = Math.max(0, (net / (1 + oh) - mat) / rate); h += "<p class=\"sub\">To earn " + cur + rate + " an hour at that price, the toy needs to take about " + (Math.round(fitH * 4) / 4) + " h. Fewer parts, a smaller size or a one-piece design gets you there.</p>"; }
      }
      if (face === "emb") h += "<p class=\"sub\">Embroidered eyes: a good choice for babies and young children. Check the toy safety rules where you sell.</p>";
      h += '<hr><p class="sub">Hours are our estimate: about the surface of a ball as tall as the toy at amigurumi gauge, ' + AMSPM + " single crochet a minute, 10 min a part, plus face and stuffing. Etsy: US fees (6.5% + 3% + $0.25 + $0.20). Next: " + amLink("crochet-circle-calculator", "plan the rounds") + " or " + amLink("etsy-fee-calculator", "check Etsy fees") + ".</p>";
      out.innerHTML = h;
      var parts4 = [["Crocheting", hC, "#b8326a"], ["Sewing on parts", hP, "#f4a823"], ["Face", hF, "#2f8f8a"], ["Stuffing and closing", hS, "#4a5470"]];
      var sc = hIn2 > 0 && est > 0 ? hIn2 / est : 1, tot = est * sc || 1, X = 20, g = "", k;
      parts4.forEach(function (p, i) { var ww = 260 * p[1] * sc / tot; if (ww > 0) g += '<rect x="' + X.toFixed(1) + '" y="24" width="' + ww.toFixed(1) + '" height="34" fill="' + p[2] + '"' + (i === 0 ? ' rx="4"' : "") + "/>"; X += ww; });
      for (k = 0; k < 4; k++) { var p = parts4[k], yy = 84 + k * 16, mins = Math.round(p[1] * sc * 60);
        g += '<rect x="20" y="' + (yy - 9) + '" width="10" height="10" rx="2" fill="' + p[2] + '"/><text x="36" y="' + yy + '" font-size="11" fill="#1f2a44">' + p[0] + '</text><text x="280" y="' + yy + '" font-size="11" text-anchor="end" fill="#1f2a44">' + (mins >= 60 ? (Math.round(mins / 6) / 10) + " h" : mins + " min") + "</text>"; }
      g += '<text x="20" y="16" font-size="11" fill="#4a5470">Where the hours go</text>';
      $("#am-svg").innerHTML = g;
      $("#am-cap").textContent = "Finishing (parts, face, stuffing) is " + Math.round((hP + hF + hS) / est * 100) + "% of this toy's time.";
    }
    $("#am-size").addEventListener("change", amPreset);
    ["#am-w", "#am-cx", "#am-face", "#am-speed", "#am-ch", "#am-cur", "#am-hu"].forEach(function (s) { $(s).addEventListener("change", amCalc); });
    ["#am-hgt", "#am-parts", "#am-y", "#am-o", "#am-h", "#am-rate", "#am-oh", "#am-try"].forEach(function (s) { $(s).addEventListener("input", amCalc); });
    amCalc();
  }

  /* ---------- C2C BLANKET CALCULATOR ---------- */
  if ($("#c2-what") && $("#c2-out")) {
    var c2 = {}; ["what", "custom", "w", "l", "u", "yarn", "g", "gu", "gnote", "sk", "col", "out", "svg", "cap"].forEach(function (k) { c2[k] = $("#c2-" + k); });
    var C2T = { 2: 0.5, 3: 0.65, 4: 0.8, 5: 1.25, 6: 1.65 }; /* in per tile: worsted/bulky/super bulky from published patterns, fine/DK our estimates */
    var C2M = { 2: 1.35, 3: 1.18, 4: 1.0, 5: 0.72, 6: 0.52 }, C2Y = 0.667 * 1.27; /* yd per sq in: same model as the blanket calculator (estimate) */
    var c2Keys = ["what", "w", "l", "u", "yarn", "g", "gu", "sk", "col"], c2T = false, c2P = store.get("pp-c2c", null);
    if (c2P) { c2Keys.forEach(function (k) { if (c2P[k] != null && c2P[k] !== "" && c2[k]) c2[k].value = c2P[k]; }); c2T = !!c2P.t; }
    var c2f1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var c2Both = function (i) { return c2f1(i) + " in (" + Math.round(i * 2.54) + " cm)"; };
    var c2Link = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function c2Draw(a, b) {
      var W = 300, H = 200, s = Math.min(W / a, H / b), w = a * s, h = b * s, x0 = (320 - w) / 2, y0 = 20 + (H - h) / 2, m = Math.min(a, b), g = "";
      var P = function (i, j) { return (x0 + i * s).toFixed(1) + "," + (y0 + h - j * s).toFixed(1); }; /* i across from the left, j up from the bottom */
      g += '<rect x="' + x0.toFixed(1) + '" y="' + y0.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="#f4a823"/>';
      g += '<polygon points="' + P(0, 0) + " " + P(m, 0) + " " + P(0, m) + '" fill="#b8326a"/>';
      g += '<polygon points="' + P(a, b) + " " + P(a - m, b) + " " + P(a, b - m) + '" fill="#2f8f8a"/>';
      var n = a + b - 1, step = n > 80 ? 5 : (n > 40 ? 2 : 1), d = "";
      for (var r = step; r < n; r += step) {
        var i1 = Math.max(0, r - b), j1 = r - i1, i2 = Math.min(a, r), j2 = r - i2;
        d += "M" + P(i1, j1) + "L" + P(i2, j2);
      }
      g += '<path d="' + d + '" stroke="rgba(255,255,255,.55)" stroke-width="1"/>';
      if (a <= 60 && b <= 60) { var gd = ""; for (var i = 1; i < a; i++) gd += "M" + P(i, 0) + "L" + P(i, b); for (var j = 1; j < b; j++) gd += "M" + P(0, j) + "L" + P(a, j); g += '<path d="' + gd + '" stroke="rgba(31,42,68,.12)" stroke-width=".6"/>'; }
      g += '<rect x="' + x0.toFixed(1) + '" y="' + y0.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="none" stroke="#1f2a44" stroke-width="2"/>';
      g += '<circle cx="' + x0.toFixed(1) + '" cy="' + (y0 + h).toFixed(1) + '" r="5" fill="#1f2a44"/><text x="' + (x0 + 8).toFixed(1) + '" y="' + Math.min(236, y0 + h + 14).toFixed(1) + '" font-size="11" fill="#1f2a44">start</text>';
      g += '<text x="160" y="13" text-anchor="middle" font-size="12" font-weight="700" fill="#1f2a44">' + a + " tiles wide × " + b + " tiles tall</text>";
      c2.svg.innerHTML = g;
    }
    function c2Calc() {
      var wn = parseInt(c2.yarn.value, 10) || 4;
      if (!c2T) c2.g.value = c2.gu.value === "10" ? Math.round(10 / 2.54 / C2T[wn] * 2) / 2 : Math.round(4 / C2T[wn] * 2) / 2;
      c2.gnote.textContent = c2T ? "Your swatch." : "Filled in with a typical tile size for this yarn until you type your own.";
      var custom = c2.what.value === "custom", cm = c2.u.value === "cm", W, L; c2.custom.hidden = !custom;
      if (custom) { W = Math.min(240, Math.max(2, (parseFloat(c2.w.value) || 0) / (cm ? 2.54 : 1))); L = Math.min(240, Math.max(2, (parseFloat(c2.l.value) || 0) / (cm ? 2.54 : 1))); }
      else { var pv = c2.what.value.split("|"); W = parseFloat(pv[0]) || 50; L = parseFloat(pv[1]) || 60; }
      var gv = parseFloat(c2.g.value) || 0, t = gv > 0 ? (c2.gu.value === "10" ? 10 / 2.54 : 4) / gv : 0;
      if (!(t > 0)) { c2.out.innerHTML = '<h3>Your C2C blanket</h3><p class="sub">Enter the tiles in your swatch.</p>'; c2.svg.innerHTML = ""; return; }
      var a = Math.max(1, Math.round(W / t)), b = Math.max(1, Math.round(L / t)), m = Math.min(a, b), M = Math.max(a, b), rows = a + b - 1, tiles = a * b;
      var yd = a * t * b * t * C2Y * (C2M[wn] || 1), sk = Math.max(10, parseFloat(c2.sk.value) || 200), buy = yd * 1.1, nc = parseInt(c2.col.value, 10) || 1;
      var shortSide = a < b ? "width" : "length";
      var plan = "<ul><li><strong>Rows 1 to " + m + ":</strong> increase at both edges (row " + m + " has " + m + " tiles).</li>" +
        (M > m ? "<li><strong>Rows " + (m + 1) + " to " + M + ":</strong> increase on the long edge, decrease on the short edge (" + (M - m) + " rows of " + m + " tiles).</li>" : "") +
        (rows > M ? "<li><strong>Rows " + (M + 1) + " to " + rows + ":</strong> decrease at both edges, down to 1 tile.</li>" : "") + "</ul>";
      var out = "<h3>Your C2C blanket</h3><div class=\"bk-dims\">" + a + " × " + b + " tiles<small>" + tiles.toLocaleString("en-US") + " tiles · " + rows + " diagonal rows · finished about " + c2Both(a * t) + " × " + c2Both(b * t) + "</small></div>" +
        '<div class="tb-stats"><div><strong>' + fmt(Math.round(yd / 50) * 50) + ' yd</strong><span>yarn, our estimate (' + fmt(yd * 0.9144) + " m)</span></div><div><strong>" + Math.ceil(buy / sk) + " skeins</strong><span>of " + fmt(sk) + " yd, with 10% spare</span></div></div>" +
        "<hr><h3>Row plan</h3>" + plan +
        (a === b ? "" : '<p class="sub">The short side is the ' + shortSide + ". Put a marker on the long edge so you keep increasing there.</p>") +
        (nc > 1 ? '<p class="sub">With ' + nc + " colours in equal stripes, buy about " + Math.ceil(buy / nc / sk) + " skein" + (Math.ceil(buy / nc / sk) === 1 ? "" : "s") + " of each. For a graph, count the squares of each colour: each tile takes about " + c2f1(yd / tiles * 36) + " in of yarn.</p>" : '<p class="sub">Each tile takes about ' + c2f1(yd / tiles * 36) + " in of yarn. For a picture blanket, draw a " + a + " × " + b + " grid.</p>") +
        '<p class="sub">Next: ' + c2Link("blanket-size-calculator", "blanket sizes") + ", " + c2Link("row-counter", "row counter") + ", " + c2Link("how-to-price-a-crochet-blanket", "pricing a blanket") + ".</p>";
      c2.out.innerHTML = out; c2Draw(a, b);
      c2.cap.textContent = "Start in the bottom left corner. Pink rows grow at both edges" + (M > m ? ", yellow rows keep the same length" : "") + ", teal rows shrink to the last tile.";
      var sv = { t: c2T }; c2Keys.forEach(function (k) { sv[k] = c2[k].value; }); store.set("pp-c2c", sv);
    }
    var c2U = c2.u.value;
    c2.u.addEventListener("change", function () { if (c2U !== c2.u.value) { var f = c2.u.value === "cm" ? 2.54 : 1 / 2.54; ["w", "l"].forEach(function (k) { var v = parseFloat(c2[k].value); if (v) c2[k].value = Math.round(v * f * 2) / 2; }); } c2U = c2.u.value; });
    var c2Gu = c2.gu.value;
    c2.gu.addEventListener("change", function () { var v = parseFloat(c2.g.value); if (v && c2T && c2Gu !== c2.gu.value) c2.g.value = Math.round(v * (c2.gu.value === "10" ? 10 / 2.54 / 4 : 4 / (10 / 2.54)) * 2) / 2; c2Gu = c2.gu.value; });
    c2.g.addEventListener("input", function () { c2T = true; });
    c2.yarn.addEventListener("change", function () { c2T = false; });
    c2Keys.forEach(function (k) { c2[k].addEventListener("input", c2Calc); c2[k].addEventListener("change", c2Calc); });
    c2Calc();
  }

  /* ---------- SCARF SIZE CHART + YARN CALCULATOR ---------- */
  if ($("#sf-what") && $("#sf-out")) {
    var sf = {}; ["what", "hgt", "h", "hw", "custom", "l", "w", "t", "u", "craft", "yarn", "tex", "sk", "fr", "out", "svg", "cap"].forEach(function (k) { sf[k] = $("#sf-" + k); });
    var SFS = { child4: [37.5, 4, "flat", "child's scarf (4 to 5 years)"], child6: [55, 5, "flat", "child's scarf (6 to 10 years)"], teen: [60, 6, "flat", "teen scarf"], women: [65, 7, "flat", "women's scarf"], men: [70, 7, "flat", "men's scarf"],
      skinny: [65, 3.5, "flat", "skinny scarf"], long: [82.5, 8, "flat", "long scarf"], "super": [100, 8, "flat", "super long scarf"], wrap: [71, 20, "flat", "wrap"], infinity: [58, 9, "loop", "infinity scarf"], cowl: [27, 9, "loop", "cowl"], kidcowl: [20, 7, "loop", "child's cowl"] };
    var SFK = { 1: 28, 2: 24, 3: 22, 4: 18, 5: 14, 6: 9, 7: 6 }, SFC = { 1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8, 7: 6 }, SFM = { 1: 1.6, 2: 1.35, 3: 1.18, 4: 1.0, 5: 0.72, 6: 0.52, 7: 0.38 };
    var sfKeys = ["what", "h", "hw", "l", "w", "t", "u", "yarn", "tex", "sk", "fr"], sfP = store.get("pp-scarf", null);
    if (sfP) { sfKeys.forEach(function (k) { if (sfP[k] != null && sfP[k] !== "" && sf[k]) sf[k].value = sfP[k]; }); if (sfP.craft) $$("button", sf.craft).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-v") === sfP.craft); }); }
    var sf1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var sfBoth = function (i) { return sf1(i) + " in (" + Math.round(i * 2.54) + " cm)"; };
    var sfLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function sfDraw(L, W, loop) {
      var x0 = 14, span = 292, sc = span / Math.max(72, L), g = "", y = 70;
      g += '<path d="M' + x0 + ' 150h' + (72 * sc).toFixed(1) + '" stroke="#1f2a44" stroke-width="2"/>';
      for (var f = 0; f <= 6; f++) { var xx = x0 + f * 12 * sc; g += '<path d="M' + xx.toFixed(1) + ' 145v10" stroke="#1f2a44" stroke-width="1.6"/><text x="' + xx.toFixed(1) + '" y="166" text-anchor="middle" font-size="10" fill="#1f2a44">' + f + " ft</text>"; }
      if (loop) {
        var r = L * sc / (2 * Math.PI) * 2.2, cx = 160, cy = 72, ry = Math.min(52, r * 0.55), rx = Math.min(140, r), bw = Math.max(5, Math.min(30, W * sc));
        g += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx.toFixed(1) + '" ry="' + ry.toFixed(1) + '" fill="none" stroke="#b8326a" stroke-width="' + bw.toFixed(1) + '"/>';
        g += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx.toFixed(1) + '" ry="' + ry.toFixed(1) + '" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1.4" stroke-dasharray="5 5"/>';
        g += '<path d="M' + x0 + ' 134h' + (L * sc).toFixed(1) + '" stroke="#2f8f8a" stroke-width="5" stroke-linecap="round"/><text x="' + x0 + '" y="126" font-size="10" fill="#1f2a44">opened out: ' + sf1(L) + " in around</text>";
      } else {
        var len = L * sc, hh = Math.max(6, Math.min(80, W * sc)), d = "";
        g += '<rect x="' + x0 + '" y="' + (y - hh / 2).toFixed(1) + '" width="' + len.toFixed(1) + '" height="' + hh.toFixed(1) + '" rx="3" fill="#b8326a"/>';
        for (var i = 8; i < len - 4; i += 9) d += "M" + (x0 + i - 3).toFixed(1) + " " + (y - hh / 2 + 3).toFixed(1) + "v" + (hh - 6).toFixed(1);
        g += '<path d="' + d + '" stroke="rgba(255,255,255,.35)" stroke-width="1.2"/>';
        g += '<text x="' + x0 + '" y="' + (y - hh / 2 - 8).toFixed(1) + '" font-size="11" font-weight="700" fill="#1f2a44">' + sf1(L) + " × " + sf1(W) + " in</text>";
      }
      sf.svg.innerHTML = g;
    }
    function sfCalc() {
      var v = sf.what.value, cm = sf.u.value === "cm", k = cm ? 2.54 : 1, L, W, loop, name;
      sf.hgt.hidden = v !== "height"; sf.custom.hidden = v !== "custom";
      if (v === "height") { L = Math.max(8, Math.min(100, (parseFloat(sf.h.value) || 0) / k)); W = Math.max(1, Math.min(16, (parseFloat(sf.hw.value) || 0) / k)); loop = false; name = "scarf as long as the wearer is tall"; }
      else if (v === "custom") { L = Math.max(4, Math.min(120, (parseFloat(sf.l.value) || 0) / k)); W = Math.max(1, Math.min(40, (parseFloat(sf.w.value) || 0) / k)); loop = sf.t.value === "loop"; name = loop ? "loop" : "scarf"; }
      else { var p = SFS[v] || SFS.women; L = p[0]; W = p[1]; loop = p[2] === "loop"; name = p[3]; }
      var craft = segVal(sf.craft) || "knit", wn = parseInt(sf.yarn.value, 10) || 4, tex = parseFloat(sf.tex.value) || 1, sk = Math.max(10, parseFloat(sf.sk.value) || 200), fr = parseFloat(sf.fr.value) || 0;
      var yd = L * W * 0.667 * (SFM[wn] || 1) * (craft === "crochet" ? 1.27 : 1) * tex;
      var frYd = 0, tass = 0; if (fr && !loop) { tass = Math.max(3, Math.round(W)); frYd = 2 * tass * 4 * (2 * fr + 1) / 36; }
      var tot = yd + frYd, skN = Math.ceil(tot * 1.1 / sk);
      var start;
      if (craft === "knit") { var sts = Math.max(4, Math.round(W * SFK[wn] / 4 * (tex >= 1.25 ? 1.15 : 1))); start = "<strong>Cast on about " + sts + " stitches</strong> (" + (SFK[wn]) + " sts per 4 in typical for this yarn" + (tex >= 1.25 ? ", plus 15% because rib and cables pull in" : "") + ")."; }
      else { var cs = Math.max(3, Math.round(W * SFC[wn] * 0.9 / 4)); start = "<strong>Chain about " + (cs + 2) + "</strong> for " + cs + " double crochet (dc in the 4th ch from the hook), or " + (Math.round(W * SFC[wn] / 4) + 1) + " for single crochet."; }
      if (loop) start += " Work it flat and sew the short ends together, or " + (craft === "knit" ? "cast on " + Math.max(8, Math.round(L * SFK[wn] / 4)) + " stitches and knit " + sf1(W) + " in in the round" : "chain " + Math.round(L * SFC[wn] * 0.9 / 4) + ", join and work rounds to " + sf1(W) + " in") + ".";
      var out = "<h3>Your " + esc(name) + "</h3><div class=\"bk-dims\">" + sf1(L) + " × " + sf1(W) + " in<small>" + (loop ? "around × wide: " : "long × wide: ") + Math.round(L * 2.54) + " × " + Math.round(W * 2.54) + " cm</small></div>" +
        '<div class="tb-stats"><div><strong>' + fmt(Math.round(tot / 10) * 10) + ' yd</strong><span>yarn, our estimate (' + fmt(tot * 0.9144) + " m)" + (frYd ? ", incl. " + fmt(frYd) + " yd fringe" : "") + "</span></div><div><strong>" + skN + " skein" + (skN === 1 ? "" : "s") + "</strong><span>of " + fmt(sk) + " yd, with 10% spare</span></div></div>" +
        "<p>" + start + "</p>" + (frYd ? '<p class="sub">Fringe: ' + tass + " tassels at each end, 4 strands of " + sf1(2 * fr + 1) + " in each.</p>" : "") +
        (v === "child4" || v === "kidcowl" ? '<p class="sub">For toddlers and young children, skip loose fringe and pom-poms; a cowl is safer than a long scarf.</p>' : "") +
        '<p class="sub">Typical gauge for the yarn, so swatch and use your own in the ' + sfLink(craft === "knit" ? "cast-on-calculator" : "foundation-chain-calculator", craft === "knit" ? "cast on calculator" : "foundation chain calculator") + ". Next: " + sfLink("crochet-knitting-gift-planner", "will it be ready by Christmas?") + "</p>";
      sf.out.innerHTML = out; sfDraw(L, W, loop);
      sf.cap.textContent = loop ? "Your " + name + " as a loop, and opened out against a 6 ft ruler." : "Your " + name + " against a 6 ft ruler.";
      var s = { craft: craft }; sfKeys.forEach(function (kk) { s[kk] = sf[kk].value; }); store.set("pp-scarf", s);
    }
    var sfU = sf.u.value;
    sf.u.addEventListener("change", function () { if (sfU !== sf.u.value) { var f = sf.u.value === "cm" ? 2.54 : 1 / 2.54; ["h", "hw", "l", "w"].forEach(function (k) { var x = parseFloat(sf[k].value); if (x) sf[k].value = Math.round(x * f * 2) / 2; }); } sfU = sf.u.value; });
    seg(sf.craft, sfCalc);
    sfKeys.forEach(function (k) { sf[k].addEventListener("input", sfCalc); sf[k].addEventListener("change", sfCalc); });
    sfCalc();
  }



  /* ---------- CROCHET & KNITTING TIME ESTIMATOR ---------- */
  if ($("#te-what") && $("#te-out")) {
    var te = {}; ["craft", "what", "custom", "w", "l", "u", "cnt", "n", "size", "yarn", "st", "spm", "own", "my", "go", "tnote", "hd", "dw", "by", "out"].forEach(function (k) { te[k] = $("#te-" + k); });
    var TEK = { 1: 28, 2: 24, 3: 22, 4: 18, 5: 14, 6: 9, 7: 6 }, TEC = { 1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8, 7: 6 }; /* CYC typical gauge midpoints per 4 in */
    var TES = { sc: [1, 1.2, 1, 1.05], hdc: [0.95, 0.85, 1.25, 1.05], dc: [0.9, 0.6, 1.5, 1.05], granny: [0.9, 0.6, 1.6, 1.15], moss: [1, 1.2, 0.85, 1.05], textured: [0.9, 0.8, 1.8, 1.05],
      st: [1, 1.33, 1, 1.05], garter: [1, 1.8, 1, 1.05], rib: [1.2, 1.33, 1.15, 1.05], seed: [1, 1.5, 1.25, 1.05], cable: [1.15, 1.33, 1.5, 1.05], colour: [1.05, 1.1, 1.6, 1.1] }; /* our estimates */
    var teKeys = ["what", "w", "l", "u", "n", "yarn", "st", "spm", "my", "hd", "dw", "by"], teP = store.get("pp-time", null);
    if (teP) { if (teP.craft) $$("button", te.craft).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-v") === teP.craft); }); teKeys.forEach(function (k) { if (teP[k] != null && teP[k] !== "" && te[k]) te[k].value = teP[k]; }); }
    var teLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    var teH = function (h) { if (h < 1) return Math.max(5, Math.round(h * 60 / 5) * 5) + " min"; var hh = Math.floor(h), mm = Math.round((h - hh) * 60 / 5) * 5; if (mm === 60) { hh++; mm = 0; } return h >= 20 ? Math.round(h) + " h" : hh + " h" + (mm ? " " + mm + " min" : ""); };
    function teStitches() {
      $$("option", te.st).forEach(function (o) { o.hidden = o.getAttribute("data-c") !== segVal(te.craft); o.disabled = o.hidden; });
      var cur = te.st.options[te.st.selectedIndex]; if (!cur || cur.hidden) { var f = $$("option", te.st).filter(function (o) { return !o.hidden; })[0]; if (f) te.st.value = f.value; }
    }
    function teCalc() {
      teStitches();
      var craft = segVal(te.craft), wv = te.what.value, cnt = wv === "count", custom = wv === "custom", cm = te.u.value === "cm";
      te.custom.hidden = !custom; te.cnt.hidden = !cnt; te.own.hidden = te.spm.value !== "own";
      var s = TES[te.st.value] || TES.sc, wn = parseInt(te.yarn.value, 10) || 4, W, L, sts, name;
      if (cnt) { sts = Math.max(0, parseFloat(te.n.value) || 0); name = "your project"; }
      else {
        if (custom) { W = (parseFloat(te.w.value) || 0) / (cm ? 2.54 : 1); L = (parseFloat(te.l.value) || 0) / (cm ? 2.54 : 1); name = "your " + Math.round(W * 10) / 10 + " × " + Math.round(L * 10) / 10 + " in piece"; }
        else { var pv = wv.split("|"); W = parseFloat(pv[1]) || 50; L = parseFloat(pv[2]) || 60; name = "a " + te.what.options[te.what.selectedIndex].text.split(",")[0].toLowerCase(); }
        var base = (craft === "k" ? TEK : TEC)[wn] * s[0];
        sts = (W * base / 4) * (L * base * s[1] / 4);
      }
      var spm = te.spm.value === "own" ? (parseFloat(te.my.value) || 0) : parseFloat(te.spm.value);
      if (!(sts > 0) || !(spm > 0)) { te.out.innerHTML = "<h3>Your time</h3><p class=\"sub\">Enter a size and your pace.</p>"; return; }
      var mult = cnt ? s[3] : s[2] * s[3], hrs = sts * mult / spm / 60, hd = Math.max(0.1, parseFloat(te.hd.value) || 1), dw = parseInt(te.dw.value, 10) || 5;
      var sessions = hrs / hd, days = Math.ceil(sessions / dw * 7), fin = new Date(); fin.setDate(fin.getDate() + days);
      var fd = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
      var o = "<h3>How long " + esc(name) + " will take</h3><div class=\"bk-dims\">" + teH(hrs * 0.8) + " – " + teH(hrs * 1.2) + "<small>about " + teH(hrs) + " of " + (craft === "k" ? "knitting" : "crochet") + " at " + Math.round(spm) + " stitches a minute, edging and ends included</small></div>" +
        '<div class="tb-stats"><div><strong>' + fmt(Math.round(sts / 100) * 100) + "</strong><span>stitches" + (cnt ? "" : ", our estimate") + "</span></div><div><strong>" + Math.ceil(sessions) + " sessions</strong><span>of " + teH(hd) + "</span></div>" +
        "<div><strong>" + (days < 14 ? days + " days" : Math.round(days / 7 * 10) / 10 + " weeks") + "</strong><span>at " + dw + " day" + (dw === 1 ? "" : "s") + " a week</span></div><div><strong>" + fin.toLocaleDateString("en-US", { month: "short", day: "numeric" }) + "</strong><span>finish date if you start today</span></div></div>";
      if (te.by.value) {
        var by = new Date(te.by.value + "T12:00:00"), left = Math.floor((by - new Date()) / 864e5);
        if (left <= 0) o += '<p class="sub">That date has passed. Pick a later one.</p>';
        else {
          var craftDays = Math.max(1, Math.floor(left * dw / 7)), need = hrs / craftDays * 60;
          o += "<hr><h3>Needed by " + fd(by) + "</h3>" + (fin <= by ? "<p><strong>You're on track.</strong> At " + teH(hd) + " a day you'd finish about " + Math.max(0, left - days) + " days early.</p>" :
            "<p><strong>It's tight.</strong> You'd need about " + teH(need / 60) + " a day on " + craftDays + " crafting days. Try a thicker yarn, a taller stitch or a smaller size.</p>");
        }
      }
      if (!cnt) { var spr = Math.round(W * (craft === "k" ? TEK : TEC)[wn] * s[0] / 4); o += '<p class="sub">About ' + spr + " stitches a row, so a row takes about " + teH(spr * s[2] / spm / 60) + ".</p>"; }
      o += '<p class="sub">Next: ' + teLink("how-to-price-a-crochet-blanket", "price it") + ", " + teLink("crochet-knitting-gift-planner", "plan all your gifts") + ", " + teLink("row-counter", "count rows") + ".</p>";
      te.out.innerHTML = o;
      var sv = { craft: craft }; teKeys.forEach(function (k) { sv[k] = te[k].value; }); store.set("pp-time", sv);
    }
    var teTm = null;
    te.go.addEventListener("click", function () {
      if (teTm) return; var t = 60; te.go.textContent = "Go! 60"; te.tnote.textContent = "Crochet or knit at your normal speed and count your stitches.";
      teTm = setInterval(function () { t--; te.go.textContent = t > 0 ? "Go! " + t : "Time me for 1 minute"; if (t <= 0) { clearInterval(teTm); teTm = null; toast("Stop! Type how many stitches you made."); te.tnote.textContent = "Time's up. Type how many stitches you made."; te.my.focus(); te.my.select(); } }, 1000);
    });
    seg(te.craft, function () { teCalc(); });
    var teU = te.u.value;
    te.u.addEventListener("change", function () { if (teU !== te.u.value) { var f = te.u.value === "cm" ? 2.54 : 1 / 2.54; ["w", "l"].forEach(function (k) { var v = parseFloat(te[k].value); if (v) te[k].value = Math.round(v * f * 2) / 2; }); } teU = te.u.value; });
    teKeys.forEach(function (k) { te[k].addEventListener("input", teCalc); te[k].addEventListener("change", teCalc); });
    teCalc();
  }

  /* ---------- RANDOM STRIPE GENERATOR ---------- */
  if ($("#sg-cols") && $("#sg-out")) {
    var sg = {}; ["n", "cols", "mode", "rows", "mult", "rng", "min", "max", "yd", "go", "print", "svg", "out"].forEach(function (k) { sg[k] = $("#sg-" + k); });
    var SGD = ["#b8326a", "#f4a823", "#2f8f8a", "#e9dfcf", "#5b6b9a", "#8a5a9e", "#d9643a", "#7fb069"];
    var sgKeys = ["n", "mode", "rows", "mult", "min", "max", "yd"], sgP = store.get("pp-stripes", null) || {};
    sgKeys.forEach(function (k) { if (sgP[k] != null && sgP[k] !== "" && sg[k]) sg[k].value = sgP[k]; });
    var sgC = (sgP.cols || []).slice(0, 8), sgSeed = sgP.seed || Math.floor(Math.random() * 1e9);
    while (sgC.length < 8) sgC.push({ c: SGD[sgC.length], t: "" });
    function sgRand(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
    function sgName(i) { return sgC[i].t ? sgC[i].t : "Colour " + String.fromCharCode(65 + i); }
    function sgSwatches() {
      var n = parseInt(sg.n.value, 10) || 4, h = "";
      for (var i = 0; i < n; i++) h += '<div class="sg-col"><input type="color" value="' + esc(sgC[i].c) + '" data-i="' + i + '" aria-label="Colour ' + String.fromCharCode(65 + i) + '"><input type="text" value="' + esc(sgC[i].t) + '" data-i="' + i + '" maxlength="24" placeholder="Colour ' + String.fromCharCode(65 + i) + '" aria-label="Name for colour ' + String.fromCharCode(65 + i) + '"></div>';
      sg.cols.innerHTML = h;
    }
    function sgMake() {
      var n = parseInt(sg.n.value, 10) || 4, R = Math.min(1000, Math.max(4, parseInt(sg.rows.value, 10) || 120)), m = parseInt(sg.mult.value, 10) || 1, mode = sg.mode.value;
      var lo = Math.max(1, parseInt(sg.min.value, 10) || 1), hi = Math.max(lo, parseInt(sg.max.value, 10) || lo), rnd = sgRand(sgSeed), out = [], used = 0, prev = -1, k = 0;
      var loM = Math.max(1, Math.ceil(lo / m)), hiM = Math.max(loM, Math.floor(hi / m));
      var FIB = [1, 1, 2, 3, 5, 8, 5, 3, 2, 1], order = [];
      for (var i = 0; i < n; i++) order.push(i);
      for (i = n - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), x = order[i]; order[i] = order[j]; order[j] = x; }
      while (used < R && out.length < 2000) {
        var w, c;
        if (mode === "random") { w = (loM + Math.floor(rnd() * (hiM - loM + 1))) * m; do { c = Math.floor(rnd() * n); } while (c === prev && n > 1); }
        else if (mode === "fib") { w = FIB[k % FIB.length] * m; c = order[k % n]; if (c === prev && n > 1) c = order[(k + 1) % n]; }
        else { w = loM * m; c = order[k % n]; }
        w = Math.min(w, R - used); out.push([c, w]); used += w; prev = c; k++;
      }
      return { s: out, R: R, n: n };
    }
    function sgCalc() {
      sg.rng.hidden = sg.mode.value === "fib";
      var p = sgMake(), s = p.s, R = p.R, n = p.n, g = "", y = 196, scale = 188 / R, row = 1, tot = [];
      for (var i = 0; i < n; i++) tot.push(0);
      g += '<rect x="40" y="6" width="220" height="190" fill="#fff"/>';
      var list = "";
      s.forEach(function (st) {
        var h = st[1] * scale; y -= h;
        g += '<rect x="40" y="' + y.toFixed(2) + '" width="220" height="' + (h + 0.3).toFixed(2) + '" fill="' + esc(sgC[st[0]].c) + '"/>';
        tot[st[0]] += st[1];
        list += "<li><i style=\"background:" + esc(sgC[st[0]].c) + '"></i>Rows ' + row + (st[1] > 1 ? "–" + (row + st[1] - 1) : "") + ": <strong>" + esc(sgName(st[0])) + "</strong> (" + st[1] + " row" + (st[1] === 1 ? "" : "s") + ")</li>";
        row += st[1];
      });
      g += '<rect x="40" y="8" width="220" height="188" fill="none" stroke="#1f2a44" stroke-width="2"/><text x="34" y="196" font-size="10" text-anchor="end" fill="#1f2a44">row 1</text><text x="34" y="16" font-size="10" text-anchor="end" fill="#1f2a44">' + R + "</text>";
      sg.svg.innerHTML = g;
      var yd = parseFloat(sg.yd.value) || 0, sum = "";
      for (i = 0; i < n; i++) sum += "<li><i style=\"background:" + esc(sgC[i].c) + '"></i><strong>' + esc(sgName(i)) + "</strong>: " + tot[i] + " rows (" + Math.round(tot[i] / R * 100) + "%)" + (yd ? ", about " + fmt(Math.ceil(yd * tot[i] / R * 1.1 / 5) * 5) + " yd" : "") + "</li>";
      sg.out.innerHTML = "<h3>Your stripe pattern</h3><div class=\"bk-dims\">" + s.length + " stripes<small>" + R + " rows in " + n + " colours" + (yd ? ", yarn per colour with 10% spare" : "") + "</small></div><ul class=\"sg-list\">" + sum + "</ul><hr><h3>Row by row</h3><ol class=\"sg-list sg-rows\">" + list + "</ol>";
      var sv = { seed: sgSeed, cols: sgC }; sgKeys.forEach(function (k) { sv[k] = sg[k].value; }); store.set("pp-stripes", sv);
    }
    sg.cols.addEventListener("input", function (ev) { var t = ev.target, i = parseInt(t.getAttribute("data-i"), 10); if (isNaN(i)) return; if (t.type === "color") sgC[i].c = t.value; else sgC[i].t = t.value.slice(0, 24); sgCalc(); });
    sg.n.addEventListener("change", function () { sgSwatches(); sgCalc(); });
    sg.go.addEventListener("click", function () { sgSeed = Math.floor(Math.random() * 1e9); sgCalc(); toast("New stripes"); });
    sg.print.addEventListener("click", function () { window.print(); });
    ["mode", "rows", "mult", "min", "max", "yd"].forEach(function (k) { sg[k].addEventListener("input", sgCalc); sg[k].addEventListener("change", sgCalc); });
    sgSwatches(); sgCalc();
  }


  /* ---------- BASIC CROCHET STITCHES: US/UK toggle + step-through ---------- */
  if ($("#bs-terms")) {
    var bsT = store.get("pp-terms", "us");
    var bsSet = function (t) { $$(".tm").forEach(function (x) { x.textContent = x.getAttribute("data-" + t); }); $$("button", $("#bs-terms")).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === t); }); bsT = t; store.set("pp-terms", t); };
    seg($("#bs-terms"), bsSet); if (bsT === "uk") bsSet("uk");
  }
  if ($("#bs-st") && $("#bs-svg") && window.PP_BS) {
    var bsD = window.PP_BS, bsK = "sc", bsI = 0;
    function bsShow() {
      var s = bsD[bsK], st = s[bsI];
      $("#bs-svg").innerHTML = st.s.replace(/^<svg[^>]*>/, "").replace(/<\/svg>$/, "");
      $("#bs-svg").setAttribute("aria-label", st.t);
      var nm = $('button[data-v="' + bsK + '"] .tm', $("#bs-st")), name = nm ? nm.textContent : bsK;
      $("#bs-out").innerHTML = '<h3>Step ' + (bsI + 1) + " of " + s.length + ": " + esc(st.t) + '</h3><p>' + esc(st.x) + '</p><p class="sub">Stitch: ' + esc(name) + "</p>";
      $("#bs-prev").disabled = bsI === 0;
      $("#bs-next").textContent = bsI === s.length - 1 ? "Start again" : "Next step";
    }
    seg($("#bs-st"), function (v) { bsK = v; bsI = 0; bsShow(); });
    $("#bs-next").addEventListener("click", function () { bsI = bsI >= bsD[bsK].length - 1 ? 0 : bsI + 1; bsShow(); });
    $("#bs-prev").addEventListener("click", function () { if (bsI > 0) { bsI--; bsShow(); } });
    document.addEventListener("keydown", function (ev) { var t = ev.target.tagName; if (t === "INPUT" || t === "SELECT" || t === "TEXTAREA") return; if (ev.key === "ArrowRight") $("#bs-next").click(); else if (ev.key === "ArrowLeft") $("#bs-prev").click(); });
    $("#bs-terms") && $("#bs-terms").addEventListener("click", bsShow);
    bsShow();
  }

  /* ---------- SWEATER SIZE CALCULATOR ---------- */
  if ($("#sw-chest") && $("#sw-out")) {
    var sw = {}; ["craft", "chest", "u", "fit", "sizes", "len", "sl", "sll", "yarn", "tex", "sk", "out"].forEach(function (k) { sw[k] = $("#sw-" + k); });
    var SWF = { vclose: [-4, -2, "very close fitting"], close: [0, 0, "close fitting"], classic: [2, 4, "classic fit"], loose: [4, 6, "loose fit"], over: [6, 10, "oversized"] };
    var SWM = { 1: 1.6, 2: 1.35, 3: 1.18, 4: 1.0, 5: 0.72, 6: 0.52 }, SWSL = { long: 18, three: 11, "short": 4, none: 0 };
    var swKeys = ["chest", "u", "fit", "sizes", "len", "sl", "sll", "yarn", "tex", "sk"], swP = store.get("pp-sweater", null);
    if (swP) { swKeys.forEach(function (k) { if (swP[k] != null && sw[k]) sw[k].value = swP[k]; }); if (swP.craft) $$("button", sw.craft).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-v") === swP.craft); }); }
    var sw1 = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US"); };
    var swLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    function swCalc() {
      var cm = sw.u.value === "cm", k = cm ? 2.54 : 1, u = cm ? " cm" : " in";
      var body = Math.max(14, Math.min(80, (parseFloat(sw.chest.value) || 38) / k)), f = SWF[sw.fit.value] || SWF.classic;
      var lo = body + f[0], hi = body + f[1], mid = (lo + hi) / 2;
      var L = Math.max(6, Math.min(45, (parseFloat(sw.len.value) || 24) / k)), sl = sw.sl.value === "none" ? 0 : Math.max(0, Math.min(30, (parseFloat(sw.sll.value) || 0) / k));
      var craft = segVal(sw.craft) || "knit", wn = parseInt(sw.yarn.value, 10) || 4, tex = parseFloat(sw.tex.value) || 1, sk = Math.max(10, parseFloat(sw.sk.value) || 200);
      var arm = Math.max(10, mid * 0.33), cuff = sl > 6 ? 8 : arm;
      var area = mid * L + 2 * sl * (arm + cuff) / 2 + mid * 1.5;
      var yd = area * 0.667 * 1.25 * (SWM[wn] || 1) * (craft === "crochet" ? 1.27 : 1) * tex, skN = Math.ceil(yd * 1.12 / sk) + 1;
      var r100 = function (x) { return fmt(Math.round(x / 50) * 50); };
      var out = "<h3>Make a sweater about this size</h3><div class=\"bk-dims\">" + (f[0] === f[1] ? sw1(lo * k) : sw1(lo * k) + "–" + sw1(hi * k)) + u + "<small>finished chest for a " + f[2] + " on a " + sw1(body * k) + u + " body</small></div>";
      var sizes = (sw.sizes.value || "").split(/[^0-9.]+/).map(parseFloat).filter(function (x) { return x > 10 && x < 200; });
      if (sizes.length) {
        var best = sizes[0]; sizes.forEach(function (x) { if (Math.abs(x / k - mid) < Math.abs(best / k - mid)) best = x; });
        out += "<p><strong>Make the " + sw1(best) + u + " size.</strong> Ease in each size:</p><ul class=\"sg-list\">" + sizes.map(function (x) { var ez = x / k - body; return "<li" + (x === best ? ' style="font-weight:700"' : "") + ">" + sw1(x) + u + ": " + (Math.abs(ez) < 0.05 ? "0" : (ez > 0 ? "+" : "−") + sw1(Math.abs(ez) * k)) + u + " ease" + (ez < f[0] - 0.01 ? " (tighter than you want)" : ez > f[1] + 0.01 ? " (looser than you want)" : " (in your range)") + "</li>"; }).join("") + "</ul>";
      } else out += '<p class="sub">Add your pattern\'s finished chest sizes to see which one to make and the ease in each.</p>';
      out += '<div class="tb-stats"><div><strong>' + r100(yd * 0.88) + "–" + r100(yd * 1.12) + ' yd</strong><span>yarn, our estimate (' + r100(yd * 0.88 * 0.9144) + "–" + r100(yd * 1.12 * 0.9144) + " m)</span></div><div><strong>" + skN + " skeins</strong><span>of " + fmt(sk) + " yd, with one spare</span></div></div>";
      out += '<p class="sub">Yarn is a rough estimate from the sweater\'s area at a typical gauge; your pattern\'s yardage is more reliable. Next: ' + swLink(craft === "knit" ? "cast-on-calculator" : "foundation-chain-calculator", craft === "knit" ? "cast on calculator" : "foundation chain calculator") + ", " + swLink("crochet-time-estimator", "how long it will take") + ".</p>";
      sw.out.innerHTML = out;
      var s = { craft: craft }; swKeys.forEach(function (kk) { s[kk] = sw[kk].value; }); store.set("pp-sweater", s);
    }
    var swU = sw.u.value;
    sw.u.addEventListener("change", function () { if (swU !== sw.u.value) { var f = sw.u.value === "cm" ? 2.54 : 1 / 2.54; ["chest", "len", "sll"].forEach(function (k) { var x = parseFloat(sw[k].value); if (x) sw[k].value = Math.round(x * f * 2) / 2; }); } swU = sw.u.value; swCalc(); });
    sw.sl.addEventListener("change", function () { var c = sw.u.value === "cm" ? 2.54 : 1; sw.sll.value = Math.round(SWSL[sw.sl.value] * c * 2) / 2; swCalc(); });
    seg(sw.craft, swCalc);
    swKeys.forEach(function (k) { if (k !== "u" && k !== "sl") { sw[k].addEventListener("input", swCalc); sw[k].addEventListener("change", swCalc); } });
    swCalc();
  }

  /* ---------- CHRISTMAS STOCKING CALCULATOR (26 Nov run 4) ---------- */
  if (page === "christmas-stocking-calculator" && $("#xs-out")) {
    var SKS = { mini: [7, 3.5, 4.5, 1.5], small: [12, 5, 7, 2.5], standard: [18, 7, 10, 3.5], large: [22, 8, 12, 4], xl: [26, 9, 14, 5] };
    var SKG = { knit: { 3: 22, 4: 18, 5: 14, 6: 9 }, crochet: { 3: 15, 4: 13, 5: 10, 6: 8 } }, SKM = { 3: 1.18, 4: 1, 5: 0.72, 6: 0.52 }, SKY = { 3: 250, 4: 200, 5: 130, 6: 80 };
    var SKN = { 3: "DK", 4: "worsted", 5: "bulky", 6: "super bulky" };
    var sk = {}; ["size", "h", "w", "f", "c", "wt", "g", "sk", "cuff", "name"].forEach(function (k) { sk[k] = $("#xs-" + k); });
    var skCraft = $("#xs-craft");
    var skSaved = store.get("pp-stocking", null);
    if (skSaved) {
      Object.keys(sk).forEach(function (k) { if (skSaved[k] != null) sk[k].value = skSaved[k]; });
      if (skSaved.craft) $$("button", skCraft).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === skSaved.craft); });
    }
    var skNum = function (el, d) { var v = parseFloat(el.value); return isFinite(v) && v > 0 ? v : d; };
    var skR = function (y) { var r = y < 120 ? 5 : 10; return fmt(Math.round(y * 0.85 / r) * r) + "–" + fmt(Math.round(y * 1.15 / r) * r); };
    function skCalc() {
      var size = sk.size.value, custom = size === "custom", d = SKS[size] || SKS.standard;
      $("#xs-custom").hidden = !custom;
      if (!custom) { sk.h.value = d[0]; sk.w.value = d[1]; sk.f.value = d[2]; sk.c.value = d[3]; }
      var h = skNum(sk.h, 18), w = skNum(sk.w, 7), f = skNum(sk.f, 10), c = Math.max(0, parseFloat(sk.c.value) || 0);
      var craft = segVal(skCraft) || "knit", wt = +sk.wt.value, g = skNum(sk.g, SKG[craft][wt]), spi = g / 4, folded = sk.cuff.value === "fold";
      var body = 2 * (w * Math.max(h - w, 0) + f * w), cuffA = 2 * w * c * (folded ? 2 : 1), k = 0.667 * SKM[wt] * (craft === "crochet" ? 1.27 : 1) * 1.1;
      var cuffY = cuffA * k, heelY = body * 0.15 * k, mainY = Math.max(0, body - 2 * w * c - body * 0.15) * k, tot = cuffY + heelY + mainY;
      var skein = skNum(sk.sk, SKY[wt]), o = [];
      o.push("<h2>About " + skR(tot) + " yd</h2><p>of " + SKN[wt] + " yarn to " + (craft === "knit" ? "knit" : "crochet") + " " + (/^(8|11|18)/.test(String(h)) ? "an " : "a ") + h + " × " + w + " in stocking (" + Math.round(h * 2.54) + " × " + Math.round(w * 2.54) + " cm), foot " + f + " in. That's <strong>" + Math.ceil(tot * 1.15 / skein) + " skein" + (Math.ceil(tot * 1.15 / skein) > 1 ? "s" : "") + "</strong> of " + skein + " yd if it's all one colour.</p>");
      o.push("<p><strong>By colour:</strong> body about " + skR(mainY) + " yd, " + (folded ? "folded " : "") + "cuff " + skR(cuffY) + " yd, heel and toe " + skR(heelY) + " yd.</p>");
      if (craft === "knit") {
        var co = Math.max(8, Math.round(2 * w * spi / 4) * 4);
        o.push("<p><strong>Cast on " + co + " stitches</strong> to knit it in the round (a multiple of 4, so the heel takes " + co / 2 + "). Two flat pieces: " + (co / 2 + 2) + " each.</p>");
      } else {
        var ch = Math.max(6, Math.round(2 * w * spi));
        o.push("<p><strong>Chain " + ch + "</strong> and join to work it in rounds, or <strong>chain " + (Math.round(w * spi) + 1) + "</strong> for each of two flat panels (single crochet).</p>");
      }
      var nm = (sk.name.value || "").replace(/\s+/g, " ").trim(), fit = Math.max(0, Math.floor((w * spi - 2) / 6)), rpi = spi * (craft === "knit" ? 1.35 : 1.15), lh = 7 / rpi;
      if (nm) {
        var n = nm.replace(/ /g, "").length;
        o.push("<p>" + (n <= fit ? "✔ <strong>" + esc(nm) + "</strong> fits" : "✘ <strong>" + esc(nm) + "</strong> has " + n + " letters; about <strong>" + fit + "</strong> fit") + " across the front with a 5-stitch alphabet. Letters will be about " + (Math.round(lh * 10) / 10) + " in tall" + (lh > c && c > 0 ? ", taller than your cuff: make the cuff deeper or put the name on the leg" : "") + ".</p>");
      } else {
        o.push("<p>About <strong>" + fit + " letters</strong> fit across the front with a 5-stitch alphabet, each about " + (Math.round(lh * 10) / 10) + " in tall. Type a name to check it.</p>");
      }
      o.push('<p class="muted">Our estimate for plain stitches, with a hanging loop and ends. Colourwork, cables and furry yarn use more, so buy a little extra.</p>');
      o.push('<p class="sub">Next: <a href="' + (location.protocol === "file:" ? "crochet-time-estimator.html" : "/crochet-time-estimator") + '">how long it will take</a>, <a href="' + (location.protocol === "file:" ? "crochet-knitting-gift-planner.html" : "/crochet-knitting-gift-planner") + '">gift planner</a>.</p>');
      $("#xs-out").innerHTML = o.join("");
      var s = { craft: craft }; Object.keys(sk).forEach(function (k2) { s[k2] = sk[k2].value; }); store.set("pp-stocking", s);
    }
    function skGauge() { sk.g.value = SKG[segVal(skCraft) || "knit"][+sk.wt.value]; sk.sk.value = SKY[+sk.wt.value]; }
    seg(skCraft, function () { skGauge(); skCalc(); });
    sk.wt.addEventListener("change", function () { skGauge(); skCalc(); });
    Object.keys(sk).forEach(function (k) { if (k !== "wt") { sk[k].addEventListener("input", skCalc); sk[k].addEventListener("change", skCalc); } });
    skCalc();
  }

  /* ---------- CROCHET PATTERN LINE EXPLAINER (26 Nov run 4) ---------- */
  if (page === "how-to-read-crochet-patterns" && $("#rp-in")) {
    var RPN = { sc: "single crochet", hdc: "half double crochet", dc: "double crochet", tr: "treble crochet", dtr: "double treble crochet", "sl st": "slip stitch",
      inc: "increase", dec: "decrease", fpdc: "front post double crochet", bpdc: "back post double crochet", fphdc: "front post half double crochet", bphdc: "back post half double crochet",
      fpsc: "front post single crochet", bpsc: "back post single crochet", fptr: "front post treble", bptr: "back post treble", puff: "puff stitch", pc: "popcorn", bobble: "bobble", esc: "extended single crochet", edc: "extended double crochet" };
    var RPUK = { sc: "UK dc", hdc: "UK htr", dc: "UK tr", tr: "UK dtr", dtr: "UK trtr", "sl st": "UK ss" };
    var RPS = "(sl st|fpdc|bpdc|fphdc|bphdc|fpsc|bpsc|fptr|bptr|esc|edc|hdc|dtr|sc|dc|tr|inc|dec|[a-z]+[23]tog|puff|pc|bobble)";
    var NUMW = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12 };
    function stEff(s, n) { /* used, made per stitch */
      if (s === "inc") return [1, 2];
      if (s === "dec") return [2, 1];
      var m = s.match(/^([a-z]+)([23])tog$/); if (m) return [+m[2], 1];
      if (s === "sl st") return [1, 0];
      return [1, 1];
    }
    function stName(s) { var m = s.match(/^([a-z]+)([23])tog$/); if (m) return (RPN[m[1]] || m[1]) + " " + m[2] + " together (a decrease)"; return RPN[s] || s; }
    function one(n, s) { return n + " " + stName(s); }
    function plural(n, s) { return n === 1 ? s : s + "s"; }
    function item(t) {
      t = t.replace(/^[\s,;.]+|[\s,;.]+$/g, "").replace(/^(then|and)\s+/, "");
      if (!t) return null;
      var mult = 1, mm = t.match(/^(.*?)\s*(?:x\s*(\d+)|(\d+)\s*times)$/);
      if (mm && mm[1]) { t = mm[1]; mult = +(mm[2] || mm[3]); }
      var around = /\b(around|across|to end)\b/.test(t), m, r;
      t = t.replace(/\s*\b(around|across|to end)\b/, "").trim();
      if (/^(turn|join|fasten off|fo|finish off)$/.test(t) || /^(sl st|join)( with sl st)?\s*(to|in|into)\s*(the\s*)?(first|1st|top|beg)/.test(t) || /^join\b/.test(t))
        return { u: 0, m: 0, ch: 0, d: /turn/.test(t) ? "Turn your work." : /fasten|fo|finish/.test(t) ? "Fasten off." : "Join the round with a slip stitch into the first stitch (not counted).", seq: [] };
      if (/^(mr|magic ring|magic circle)$/.test(t)) return { u: 0, m: 0, ch: 0, d: "Make a magic ring.", seq: [] };
      if ((m = t.match(new RegExp("^(\\d+)\\s*" + RPS + "\\s*(?:in|into)\\s*(?:a\\s*|the\\s*)?(?:mr|magic ring|magic circle|ring|2nd ch from hook|second ch from hook)")))) {
        r = { u: 0, m: +m[1], ch: 0, d: "Work " + one(+m[1], m[2]) + " into the " + (/ch/.test(t) ? "chain" : "magic ring") + ".", seq: [m[1] + " " + m[2]] };
      } else if ((m = t.match(/^ch\s*-?\s*(\d+)?\s*(?:countsas\s*([a-z ]+))?$/))) {
        var nch = +(m[1] || 1);
        r = m[2] ? { u: 1, m: 1, ch: 0, d: "Chain " + nch + "; it counts as the first " + (RPN[m[2].trim()] || m[2]) + ".", seq: ["ch " + nch] } : { u: 0, m: 0, ch: nch, d: "Chain " + nch + " (chains aren't counted as stitches here).", seq: ["ch " + nch] };
      } else if ((m = t.match(/^(?:sk|skip)\s*(?:the\s*)?(?:next\s*)?(\d+)?\s*(st|ch|sc|dc|hdc)?$/))) {
        var nsk = +(m[1] || 1); r = { u: nsk, m: 0, ch: 0, d: "Skip the next " + (nsk > 1 ? nsk + " stitches" : "stitch") + ".", seq: ["skip " + nsk] };
      } else if ((m = t.match(new RegExp("^(\\d+)\\s*" + RPS + "\\s*(?:in|into)\\s*(?:the\\s*)?(same|next|each|first|last)\\s*(st|sp|ch-sp|ch)?")))) {
        var nn = +m[1], same = m[3] === "same", e1 = stEff(m[2]);
        if (m[3] === "each") around = true;
        r = { u: same ? 0 : 1, m: nn * e1[1], ch: 0, d: "Work " + one(nn, m[2]) + " all into the " + (same ? "same stitch" : m[3] === "each" ? "next stitch" : m[3] + " " + (m[4] === "ch-sp" ? "chain space" : "stitch")) + (nn > 1 && !same ? " (an increase of " + (nn - 1) + ")" : "") + ".", seq: [nn + " " + m[2] + " in 1"] };
      } else if ((m = t.match(new RegExp("^" + RPS + "\\s*(?:in|into)\\s*(?:each\\s*of\\s*)?(?:the\\s*)?next\\s*(\\d+)\\s*(?:st|ch)?$"))) || (m = t.match(new RegExp("^(?:\\d+\\s*)?" + RPS + "\\s*(\\d+)$"))) || (m = t.match(new RegExp("^(\\d+)\\s*" + RPS + "$")))) {
        var s1 = isNaN(+m[1]) ? m[1] : m[2], n1 = isNaN(+m[1]) ? +m[2] : +m[1], e2 = stEff(s1);
        r = { u: n1 * e2[0], m: n1 * e2[1], ch: 0, d: (s1 === "inc" ? n1 + " " + plural(n1, "increase") + ": 2 stitches in each of the next " + n1 + " " + plural(n1, "stitch").replace("stitchs", "stitches") : s1 === "dec" ? n1 + " " + plural(n1, "decrease") + ": work 2 stitches together, " + n1 + " " + plural(n1, "time") : "Work 1 " + stName(s1) + " in each of the next " + n1 + " stitches") + ".", seq: Array(Math.min(n1, 40) + 1).join(s1 + ",").split(",").slice(0, n1) };
      } else if ((m = t.match(new RegExp("^" + RPS + "\\s*(?:(?:in|into)\\s*(?:the\\s*)?(next|same|first|last|each)\\s*(st|ch|sp|ch-sp)?)?$")))) {
        var e3 = stEff(m[1]), sm = m[2] === "same";
        if (m[2] === "each") around = true;
        r = { u: sm ? 0 : e3[0], m: e3[1], ch: 0, d: (m[1] === "inc" ? "Increase: 2 stitches in the next stitch" : m[1] === "dec" ? "Decrease: work the next 2 stitches together as 1" : m[1] === "sl st" ? "Slip stitch into the " + (m[2] || "next") + " stitch (not counted)" : "Work 1 " + stName(m[1]) + " into the " + (sm ? "same" : (m[2] || "next")) + " stitch") + ".", seq: [m[1]] };
      } else return { bad: t };
      r.n = mult; r.around = around; return r;
    }
    function parse(s, i, close) {
      var out = [], buf = "";
      function flush() { if (buf.trim()) buf.split(/[,;]|\bthen\b/).forEach(function (p) { var it = item(p); if (it) out.push(it); }); buf = ""; }
      while (i < s.length) {
        var c = s[i];
        if (c === "[" || c === "(") {
          flush();
          var sub = parse(s, i + 1, c === "[" ? "]" : ")"); i = sub.i;
          var rest = s.slice(i), mm, g = { g: sub.items, n: 1, around: false, shell: false, sameSt: false };
          if ((mm = rest.match(/^\s*,?\s*(?:rep(?:eat)?\s*)?(?:x\s*(\d+)|(\d+)\s*(more\s*)?times)/))) { g.n = +(mm[1] || mm[2]) + (mm[3] ? 1 : 0); i += mm[0].length; }
          else if ((mm = rest.match(/^\s*,?\s*(?:rep(?:eat)?\s*)?(around|across|to end|in each (?:st|stitch|ch-sp|sp) around)/))) { g.around = true; if (/each/.test(mm[1])) g.shell = true; i += mm[0].length; }
          else if ((mm = rest.match(/^\s*(?:all\s*)?(?:in|into)\s*(?:the\s*)?(same|next|each|first|last|top|beg)\s*[a-z-]*/))) { g.shell = true; g.sameSt = mm[1] === "same"; if (mm[1] === "each") g.around = true; i += mm[0].length; }
          out.push(g); continue;
        }
        if (c === close) { flush(); return { items: out, i: i + 1 }; }
        buf += c; i++;
      }
      flush(); return { items: out, i: i };
    }
    function tot(items) { var u = 0, m = 0, ch = 0; items.forEach(function (it) { var t = it.g ? (it.shell ? { u: it.sameSt ? 0 : 1, m: tot(it.g).m, ch: tot(it.g).ch } : tot(it.g)) : it; var n = it.n || 1; if (it.bad) return; u += t.u * n; m += t.m * n; ch += t.ch * n; }); return { u: u, m: m, ch: ch }; }
    function rpRun() {
      var raw = $("#rp-in").value.trim(), prev = parseInt($("#rp-prev").value, 10), hasPrev = isFinite(prev) && prev >= 0 && $("#rp-prev").value !== "";
      if (!raw) { $("#rp-out").innerHTML = "<h3>Paste a line</h3><p>Paste one row or round from your pattern to see it step by step.</p>"; return; }
      var t = " " + raw.toLowerCase().replace(/[–—]/g, "-").replace(/×/g, "x").replace(/\s+/g, " ") + " ";
      Object.keys(NUMW).forEach(function (w) { t = t.replace(new RegExp("\\b" + w + "\\b", "g"), NUMW[w]); });
      t = t.replace(/\btwice\b/g, "2 times").replace(/\bstitches\b|\bstitch\b|\bsts\b/g, "st").replace(/\bslip st\b|\bslst\b|\bss\b/g, "sl st")
        .replace(/\binv(?:isible)?\s*dec(?:rease)?\b|\bsc2tog\b|\bdecrease\b/g, "dec").replace(/\bincrease\b/g, "inc").replace(/\bsingle crochet\b/g, "sc").replace(/\bhalf double crochet\b/g, "hdc").replace(/\bdouble crochet\b/g, "dc").replace(/\bchain\b/g, "ch").replace(/\brepeat\b/g, "rep");
      t = t.trim();
      var label = "", lm = t.match(/^(rnds?|rounds?|rows?|r)\s*(\d+)(?:\s*-\s*(\d+))?\s*[:.)-]?\s*/);
      if (lm) { label = (/^r(ow)?s?$/.test(lm[1]) && !/^rnd|^round/.test(lm[1]) ? "Row " : "Round ") + lm[2] + (lm[3] ? " to " + lm[3] : ""); t = t.slice(lm[0].length); }
      var stated = null, cm = t.match(/[\(\[{]\s*(\d+)\s*(?:st|sc|dc|hdc)?\s*[\)\]}]\s*\.?\s*$/) || t.match(/(?:-|=|:)\s*(\d+)\s*st\.?\s*$/);
      if (cm) { stated = +cm[1]; t = t.slice(0, cm.index); }
      t = t.replace(/\bch\s*-?\s*(\d+)\s*\(\s*counts? as (?:a |the |first |1 )*([a-z ]+?)\s*\)/g, "ch $1 countsas $2");
      if ((t.match(/\*/g) || []).length === 1 && /rep\s*from\s*\*/.test(t)) t = "*" + t;
      if (!/\*/.test(t)) t = t.replace(/^(.*)[,;]\s*rep(?:eat)?\s*((?:\d+\s*(?:more\s*)?times|x\s*\d+|around|across)\s*\.?)$/, "[$1] $2");
      t = t.replace(/\*([^*]+?)[;,.]?\s*rep\s*from\s*\*\s*/g, "[$1] ");
      t = t.replace(/\*([^*]+)\*\s*,?\s*/g, "[$1] ");
      t = t.replace(/\bin each st around\b/g, "around").replace(/\bin each st across\b/g, "across").replace(/\.\s*$/, "");
      var items = parse(t, 0, null).items, steps = [], seq = [], bad = [], warn = [];
      var fixed = { u: 0 }; items.forEach(function (it) { if (!it.around && !it.bad) fixed.u += tot([it]).u; });
      function reps(it) {
        if (!it.around) return it.n || 1;
        var per = it.g ? (it.shell ? (it.sameSt ? 0 : 1) : tot(it.g).u) : it.u;
        if (!hasPrev || per <= 0) return null;
        var r = (prev - fixed.u) / per; if (r !== Math.floor(r)) warn.push("The repeat doesn't divide evenly into " + prev + " stitches; check the stitch count of the last round.");
        return Math.max(0, Math.floor(r));
      }
      var U = 0, M = 0, CH = 0, unknown = false;
      function describe(list, depth, out) {
        list.forEach(function (it) {
          if (it.bad) { bad.push(it.bad); return; }
          var n = depth === 0 ? reps(it) : (it.around ? null : it.n || 1);
          if (n === null) { unknown = true; n = 1; }
          if (it.g) {
            var sub = [], tt = it.shell ? { u: it.sameSt ? 0 : 1, m: tot(it.g).m, ch: tot(it.g).ch } : tot(it.g), inner = [];
            describe(it.g, depth + 1, inner);
            sub = inner.map(function (x) { return x.d; });
            var shellSeq = []; inner.forEach(function (x) { shellSeq = shellSeq.concat(x.seq); });
            var txt = it.shell ? "Into " + (it.sameSt ? "the same stitch" : "the next stitch") + ", work all of: " + shellSeq.join(", ") + "." : "Repeat: " + sub.join(" ");
            var times = it.around ? (unknown && !hasPrev ? " Repeat to the end (enter the stitches in the round before to see how many times)." : " Do this " + n + " " + plural(n, "time") + " to the end.") : n > 1 ? " Do this " + n + " times." : "";
            out.push({ d: txt + times, sub: [] });
            var one1 = []; inner.forEach(function (x) { one1 = one1.concat(x.seq); });
            if (it.shell) one1 = ["(" + one1.join(" ") + ")"];
            out[out.length - 1].seq = [];
            for (var k2 = 0; k2 < n; k2++) out[out.length - 1].seq = out[out.length - 1].seq.concat(one1);
            if (depth === 0) { U += tt.u * n; M += tt.m * n; CH += tt.ch * n; }
          } else {
            var d = it.d + (it.around ? (n && hasPrev ? " Do this in each of the remaining " + n + " stitches." : " Do this to the end.") : n > 1 ? " Do this " + n + " times." : "");
            var sq = []; for (var k3 = 0; k3 < n; k3++) sq = sq.concat(it.seq);
            out.push({ d: d, seq: sq });
            if (depth === 0) { U += it.u * n; M += it.m * n; CH += it.ch * n; }
          }
        });
      }
      describe(items, 0, steps);
      steps.forEach(function (s) { seq = seq.concat(s.seq); });
      var o = [];
      o.push("<h3>" + (label ? esc(label) + ", step by step" : "Step by step") + "</h3><ol class=\"rp-steps\">" + steps.map(function (s) { return "<li>" + esc(s.d) + "</li>"; }).join("") + "</ol>");
      if (bad.length) o.push("<p>⚠ Couldn't read: <strong>" + bad.map(esc).join("</strong>, <strong>") + "</strong>. Check the pattern's own abbreviation list, or our <a href=\"" + (location.protocol === "file:" ? "crochet-terms.html" : "/crochet-terms") + "\">US and UK terms</a>.</p>");
      if (!unknown) {
        o.push("<h2>" + M + " " + plural(M, "stitch").replace("stitchs", "stitches") + "</h2><p>made in this " + (!label ? "line" : /^Row/.test(label) ? "row" : "round") + (hasPrev ? ", using " + U + " of the " + prev + " stitches from the one before" : "") + (CH ? ", plus " + CH + " " + plural(CH, "chain") + " not counted" : "") + ".</p>");
        if (stated !== null) o.push(stated === M ? "<p>✔ Matches the pattern's count of <strong>" + stated + "</strong>.</p>" : "<p>✘ The pattern says <strong>" + stated + "</strong>. " + (Math.abs(stated - M) <= CH + 1 ? "The difference may be a chain or slip stitch the pattern counts. " : "") + "Check the line, or the stitches in the round before.</p>");
        if (hasPrev && U !== prev && !bad.length) warn.push("This line uses " + U + " stitches but the round before had " + prev + ".");
      } else if (stated !== null) o.push("<p>The pattern says you'll end with <strong>" + stated + " stitches</strong>.</p>");
      warn.forEach(function (w) { o.push("<p>⚠ " + esc(w) + "</p>"); });
      if (seq.length && seq.length <= 120) o.push("<p class=\"sub\" style=\"color:#fff\">Written out in full:</p><p class=\"rp-seq\">" + esc(seq.join(", ")) + "</p>");
      var found = {}; (raw.toLowerCase().match(/\b(sl st|hdc|dtr|sc|dc|tr|inc|dec|sc2tog|ch|sk|fpdc|bpdc)\b/g) || []).forEach(function (a) { found[a] = 1; });
      var fl = Object.keys(found).filter(function (a) { return RPN[a] || a === "ch" || a === "sk" || a === "sc2tog"; });
      if (fl.length) o.push("<p class=\"sub\" style=\"color:#fff\">" + fl.map(function (a) { return "<strong>" + esc(a) + "</strong> = " + esc(a === "ch" ? "chain" : a === "sk" ? "skip" : a === "sc2tog" ? "single crochet 2 together" : RPN[a]) + (RPUK[a] ? " (" + RPUK[a] + ")" : ""); }).join(" · ") + "</p>");
      if (/\bhtr\b|\btrtr\b/.test(raw.toLowerCase())) o.push("<p>⚠ This line has UK terms (htr or trtr). Translate it to US terms first with our <a href=\"" + (location.protocol === "file:" ? "crochet-terms.html" : "/crochet-terms") + "\">US vs UK chart</a>.</p>");
      $("#rp-out").innerHTML = o.join("");
      store.set("pp-rp", { t: $("#rp-in").value, p: $("#rp-prev").value });
    }
    var rpS = store.get("pp-rp", null); if (rpS) { $("#rp-in").value = rpS.t || $("#rp-in").value; $("#rp-prev").value = rpS.p != null ? rpS.p : ""; }
    $("#rp-in").addEventListener("input", rpRun); $("#rp-prev").addEventListener("input", rpRun);
    $$(".ka-ex button").forEach(function (b) { b.addEventListener("click", function () { $("#rp-in").value = b.getAttribute("data-ex"); $("#rp-prev").value = b.getAttribute("data-prev"); rpRun(); }); });
    rpRun();
  }

  /* ---------- KNIT STITCH PATTERNS (row writer from our charts) ---------- */
  if ($("#ks-pat") && $("#ks-data")) {
    var KSD = JSON.parse($("#ks-data").textContent), KSB = {};
    KSD.forEach(function (p) { KSB[p.k] = p; });
    var ksBit = function (g, r, x) { var row = g[r % g.length]; return row.charAt(x % row.length) === "1"; };
    var ksOps = function (g, r, n) { var o = []; for (var i = 0; i < n; i++) { var xr = r % 2 === 0 ? i : n - 1 - i, k = ksBit(g, r, xr); o.push(r % 2 === 0 ? (k ? "k" : "p") : (k ? "p" : "k")); } return o; };
    var ksRl = function (a) { var u = [], i = 0; while (i < a.length) { var j = i; while (j < a.length && a[j] === a[i]) j++; u.push(a[i] + (j - i)); i = j; } return u; };
    var ksSay = function (o) {
      var n = o.length;
      for (var p = 1; p <= 8 && p <= n; p++) {
        var best = null;
        for (var a = 0; a < p && a < n; a++) {
          var ok = true; for (var i = a; i < n; i++) if (o[i] !== o[a + ((i - a) % p)]) { ok = false; break; }
          if (!ok) continue;
          var reps = Math.floor((n - a) / p); if (reps < 2 && p > 1) continue;
          var L = o.slice(0, a), U = o.slice(a, a + p), T = o.slice(a + reps * p), sc = ksRl(L).length + ksRl(T).length + ksRl(U).length;
          if (!best || sc < best.sc) best = { L: L, U: U, T: T, sc: sc };
        }
        if (!best) continue;
        if (p === 1 && !best.L.length) return o[0] === "k" ? "Knit every stitch." : "Purl every stitch.";
        var t = best.T.length, s = (best.L.length ? ksRl(best.L).join(", ") + ", " : "") + "*" + ksRl(best.U).join(", ") + "; repeat from * ";
        return t ? s + (t > 1 ? "to last " + t + " sts, " : "to last st, ") + ksRl(best.T).join(", ") + "." : s + "to end.";
      }
      return ksRl(o).join(", ") + ".";
    };
    var ksRows = function (g, n) {
      var H = g.length * (g.length % 2 ? 2 : 1), txt = [];
      for (var r = 0; r < H; r++) txt.push(ksSay(ksOps(g, r, n)));
      for (var per = 1; per <= H; per++) { if (H % per) continue; var ok = true; for (var r2 = 0; r2 < H; r2++) if (txt[r2] !== txt[r2 % per]) { ok = false; break; } if (ok) return txt.slice(0, per); }
      return txt;
    };
    var ksRun = function () {
      var p = KSB[$("#ks-pat").value] || KSD[0], u = $("#ks-u").value, w = parseFloat($("#ks-w").value) || 8, g = parseFloat($("#ks-g").value) || 18;
      var per = g / (u === "cm" ? 10 : 4), raw = w * per, own = parseInt($("#ks-n").value, 10), n;
      if (own >= 2) n = Math.min(600, own);
      else { var k = Math.max(1, Math.round((raw - p.x) / p.m)); n = p.m * k + p.x; if (n < 2) n = 2; }
      var fits = (n - p.x) % p.m === 0 && n - p.x >= (p.m > 1 ? p.m : 0);
      var rows = ksRows(p.g, n), o = [];
      o.push("<h3>" + esc(p.n) + "</h3><p class=\"big\">" + n + " <small>stitches to cast on</small></p>");
      o.push("<p>Comes out about <strong>" + (n / per).toFixed(1) + " " + u + "</strong> wide at " + g + " sts per " + (u === "cm" ? "10 cm" : "4 in") + ". Pattern multiple: " + (p.m === 1 ? "any number" : p.m + (p.x ? " + " + p.x : "")) + ".</p>");
      if (own >= 2 && !fits) {
        var lo = Math.max(p.m + p.x, Math.floor((n - p.x) / p.m) * p.m + p.x), hi = lo + p.m;
        o.push("<p>⚠ " + n + " doesn't fit the multiple, so the edges won't match. Nearest counts that do: <strong>" + lo + "</strong> or <strong>" + hi + "</strong>. The rows below are still correct for " + n + ".</p>");
      }
      o.push("<ol class=\"ks-out-rows\">" + rows.map(function (t, i) { return "<li><strong>Row " + (i + 1) + (rows.length > 1 ? (i % 2 === 0 ? " (RS)" : " (WS)") : "") + ":</strong> " + esc(t) + "</li>"; }).join("") + "</ol>");
      o.push("<p>" + (rows.length === 1 ? "Repeat this row." : "Repeat rows 1 to " + rows.length + ".") + " Want tidy edges? Cast on " + (n + 2) + " and knit the first and last stitch of every row.</p>");
      var cols = Math.min(n, 28), R = 12, cs = 10, W = cols * cs + 8, H = R * cs + 8, s = "";
      for (var r = 0; r < R; r++) for (var x = 0; x < cols; x++) {
        var cx = W - 4 - (x + 0.5) * cs, cy = H - 4 - (r + 0.5) * cs;
        s += ksBit(p.g, r, x) ? '<path d="M' + (cx - 3.5) + " " + (cy - 3.5) + ' l3.5 6.5 l3.5 -6.5" fill="none" stroke="#f4a823" stroke-width="2" stroke-linecap="round"/>' : '<path d="M' + (cx - 4) + " " + (cy + 1) + " q4 " + ((x + r) % 2 ? -5 : 5) + ' 8 0" fill="none" stroke="#e07aa3" stroke-width="2.2" stroke-linecap="round"/>';
      }
      o.push('<figure class="ks-prev"><svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Preview of the right side">' + s + "</svg><figcaption>Right side" + (n > 28 ? ", first 28 stitches" : "") + "</figcaption></figure>");
      $("#ks-out").innerHTML = o.join("");
      store.set("pp-ks", { p: $("#ks-pat").value, w: $("#ks-w").value, u: u, g: $("#ks-g").value, n: $("#ks-n").value });
    };
    var ksS = store.get("pp-ks", null);
    if (ksS && KSB[ksS.p]) { $("#ks-pat").value = ksS.p; $("#ks-w").value = ksS.w || 8; $("#ks-u").value = ksS.u || "in"; $("#ks-g").value = ksS.g || 18; $("#ks-n").value = ksS.n || ""; }
    if (location.hash && KSB[location.hash.slice(1)]) $("#ks-pat").value = location.hash.slice(1);
    ["#ks-pat", "#ks-w", "#ks-u", "#ks-g", "#ks-n"].forEach(function (id) { $(id).addEventListener("input", ksRun); $(id).addEventListener("change", ksRun); });
    ksRun();
  }

  /* ---------- SCRAPBOOK PAGE LAYOUT ---------- */
  if ($("#sb-page") && $("#sb-data")) {
    var SBD = JSON.parse($("#sb-data").textContent);
    var sbGrid = function (W, H, w, h, m, g) { return [Math.max(0, Math.floor((W - 2 * m + g + 1e-9) / (w + g))), Math.max(0, Math.floor((H - 2 * m + g + 1e-9) / (h + g)))]; };
    var sbRows = function (W, H, w, h, m, g) {
      var best = [];
      [[w, h], [h, w]].forEach(function (o) {
        var a = o[0], b = o[1], ca = sbGrid(W, H, a, b, m, g)[0], cb = sbGrid(W, H, b, a, m, g)[0];
        for (var ra = 0; ra < 40; ra++) {
          var used = ra * (b + g); if (ra && 2 * m + used - g > H + 1e-9) break;
          var rb = cb ? Math.max(0, Math.floor((H - 2 * m - used + g + 1e-9) / (a + g))) : 0;
          if (ra * ca + rb * cb > best.length) {
            var R = [], r, i;
            for (r = 0; r < ra; r++) for (i = 0; i < ca; i++) R.push([m + i * (a + g), m + r * (b + g), a, b]);
            for (r = 0; r < rb; r++) for (i = 0; i < cb; i++) R.push([m + i * (b + g), m + used + r * (a + g), b, a]);
            best = R;
          }
        }
      });
      return best;
    };
    var sbFit = function (W, H, w, h, m, g) {
      var best = sbRows(W, H, w, h, m, g), cols = sbRows(H, W, w, h, m, g).map(function (q) { return [q[1], q[0], q[3], q[2]]; });
      if (cols.length > best.length) best = cols;
      var L = Math.max(w, h), S = Math.min(w, h);
      if (L > S && L + S + g <= Math.min(W, H) - 2 * m + 1e-9 && best.length < 4) best = [[m, m, L, S], [m + L + g, m, S, L], [m + S + g, m + L + g, L, S], [m, m + S + g, S, L]];
      return { n: best.length, r: best };
    };
    var sbNum = function (id, d) { var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : d; };
    var fr = function (x) { var w = Math.floor(x + 1e-9), f = Math.round((x - w) * 8); if (f === 8) { w++; f = 0; } var F = ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f]; return (w ? w : (F ? "" : "0")) + F; };
    var sbRun = function () {
      var pk = $("#sb-page").value, fk = $("#sb-photo").value;
      $("#sb-pc").hidden = pk !== "custom"; $("#sb-fc").hidden = fk !== "custom";
      var P = pk === "custom" ? [sbNum("#sb-pw", 12), sbNum("#sb-ph", 12)] : SBD.p[pk], F = fk === "custom" ? [sbNum("#sb-fw", 4), sbNum("#sb-fh", 6)] : SBD.f[fk];
      var mat = parseFloat($("#sb-mat").value) || 0, m = sbNum("#sb-m", 0.5), g = sbNum("#sb-g", 0.25);
      var w = F[0] + 2 * mat, h = F[1] + 2 * mat, W = P[0], H = P[1], fit = sbFit(W, H, w, h, m, g), want = parseInt($("#sb-want").value, 10), o = [];
      var show = want > 0 ? Math.min(want, fit.n) : fit.n;
      o.push("<h3>" + W + " x " + H + " in page</h3><p class=\"big\">" + fit.n + " <small>photo" + (fit.n === 1 ? "" : "s") + " of " + F[0] + " x " + F[1] + " in fit" + (mat ? ", matted" : "") + "</small></p>");
      if (!fit.n) o.push("<p>The photo is bigger than the page inside the margin. Try a smaller print or a smaller margin.</p>");
      else {
        var used = show * w * h, area = W * H;
        o.push("<p>" + (mat ? "Each mat: <strong>" + fr(w) + " x " + fr(h) + " in</strong>. " : "") + "With " + show + " photo" + (show === 1 ? "" : "s") + " the page is <strong>" + Math.round(used / area * 100) + "% photos</strong>, leaving about " + Math.round(100 - used / area * 100) + "% for paper, a title and journaling.</p>");
        if (want > fit.n) o.push("<p>⚠ Only " + fit.n + " fit. Use smaller prints, or spread them over a two-page spread.</p>");
      }
      var S = 300 / Math.max(W, H), svg = '<rect x="1" y="1" width="' + (W * S) + '" height="' + (H * S) + '" rx="4" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>', C = ["#2f8f8a", "#b8326a", "#e39a14", "#5b6b94"];
      fit.r.slice(0, show).forEach(function (q, k) { svg += '<rect x="' + (1 + q[0] * S).toFixed(1) + '" y="' + (1 + q[1] * S).toFixed(1) + '" width="' + (q[2] * S).toFixed(1) + '" height="' + (q[3] * S).toFixed(1) + '" rx="2" fill="' + C[k % 4] + '" opacity=".9"/>'; });
      o.push('<figure class="sb-prev"><svg viewBox="0 0 ' + (W * S + 2).toFixed(0) + " " + (H * S + 2).toFixed(0) + '" role="img" aria-label="Layout preview">' + svg + "</svg><figcaption>Layout preview, to scale</figcaption></figure>");
      var tot = parseInt($("#sb-n").value, 10);
      if (tot > 0 && show > 0) { var pg = Math.ceil(tot / show); o.push("<p>For <strong>" + tot + " photos</strong> at " + show + " a page you need <strong>" + pg + " pages</strong>: " + Math.ceil(pg / 2) + " page protectors used both sides, or " + pg + " one-sided.</p>"); }
      $("#sb-out").innerHTML = o.join("");
      store.set("pp-sb", { p: pk, f: fk, pw: $("#sb-pw").value, ph: $("#sb-ph").value, fw: $("#sb-fw").value, fh: $("#sb-fh").value, mat: $("#sb-mat").value, m: $("#sb-m").value, g: $("#sb-g").value, n: $("#sb-n").value, want: $("#sb-want").value });
    };
    var sbS = store.get("pp-sb", null);
    if (sbS) { ["pw", "ph", "fw", "fh", "mat", "m", "g", "n", "want"].forEach(function (k) { if (sbS[k] != null && $("#sb-" + k)) $("#sb-" + k).value = sbS[k]; }); if (SBD.p[sbS.p] || sbS.p === "custom") $("#sb-page").value = sbS.p; if (SBD.f[sbS.f] || sbS.f === "custom") $("#sb-photo").value = sbS.f; }
    ["#sb-page", "#sb-photo", "#sb-pw", "#sb-ph", "#sb-fw", "#sb-fh", "#sb-mat", "#sb-m", "#sb-g", "#sb-n", "#sb-want"].forEach(function (id) { $(id).addEventListener("input", sbRun); $(id).addEventListener("change", sbRun); });
    sbRun();
  }

  /* ---------- CRAFT FAIR SALES LOG print ---------- */
  if ($("#cf-log-print")) {
    $("#cf-log-print").addEventListener("click", function () {
      document.body.classList.add("print-cflog");
      window.print();
      setTimeout(function () { document.body.classList.remove("print-cflog"); }, 500);
    });
  }

  /* ---------- FAT QUARTER CALCULATOR ---------- */
  if ($("#fq-mode") && $("#fq-data")) {
    var FQD = JSON.parse($("#fq-data").textContent);
    var fqRows = function (W, H, w, h) {
      var best = 0, pick = null;
      [[w, h], [h, w]].forEach(function (o) {
        var a = o[0], b = o[1], ca = Math.floor(W / a + 1e-9), cb = Math.floor(W / b + 1e-9);
        for (var ra = 0; ra < 200; ra++) {
          var used = ra * b; if (used > H + 1e-9) break;
          var rb = cb ? Math.floor((H - used) / a + 1e-9) : 0, n = ra * ca + rb * cb;
          if (n > best) { best = n; pick = [a, b, ca, ra, cb, rb]; }
        }
      });
      return { n: best, p: pick };
    };
    var fqFit = function (W, H, w, h) { var A = fqRows(W, H, w, h), B = fqRows(H, W, w, h); return A.n >= B.n ? { n: A.n, p: A.p, t: false } : { n: B.n, p: B.p, t: true }; };
    var fqFr = function (x) { var w = Math.floor(x + 1e-9), f = Math.round((x - w) * 8); if (f === 8) { w++; f = 0; } var F = ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f]; return (w ? w : (F ? "" : "0")) + F; };
    var fqSvg = function (W, H, fit) {
      var S = 260 / Math.max(W, H), s = '<rect x="1" y="1" width="' + (W * S).toFixed(1) + '" height="' + (H * S).toFixed(1) + '" rx="4" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>', C = ["#2f8f8a", "#b8326a", "#e39a14"], k = 0;
      if (fit.p) {
        var p = fit.p, R = [], r, i;
        for (r = 0; r < p[3]; r++) for (i = 0; i < p[2]; i++) R.push([i * p[0], r * p[1], p[0], p[1]]);
        for (r = 0; r < p[5]; r++) for (i = 0; i < p[4]; i++) R.push([i * p[1], p[3] * p[1] + r * p[0], p[1], p[0]]);
        R.forEach(function (q) { if (fit.t) q = [q[1], q[0], q[3], q[2]]; s += '<rect x="' + (1.5 + q[0] * S).toFixed(1) + '" y="' + (1.5 + q[1] * S).toFixed(1) + '" width="' + Math.max(1, q[2] * S - 2).toFixed(1) + '" height="' + Math.max(1, q[3] * S - 2).toFixed(1) + '" rx="2" fill="' + C[(k++) % 3] + '" opacity=".85"/>'; });
      }
      return '<figure class="sb-prev"><svg viewBox="0 0 ' + (W * S + 3).toFixed(0) + " " + (H * S + 3).toFixed(0) + '" role="img" aria-label="Cutting layout, to scale">' + s + "</svg><figcaption>Cutting layout, " + fqFr(W) + " x " + fqFr(H) + " in, to scale</figcaption></figure>";
    };
    var fqN = function (id, d) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : d; };
    var fqRun = function () {
      var mode = $("#fq-mode").value, t = $("#fq-type"), P = FQD[t.value] || [18, 21], W = P[0], H = P[1], nm = ({ fq: "fat quarter", "fq-full": "fat quarter", fe: "fat eighth", lq: "long quarter", "fq-m": "metric fat quarter", hy: "half yard" })[t.value] || "fat quarter", o = [];
      $("#fq-pieces").hidden = mode !== "pieces"; $("#fq-quilt").hidden = mode !== "quilt";
      if (mode === "pieces") {
        var w = fqN("#fq-w", 5), h = fqN("#fq-h", 5), fit = fqFit(W, H, w, h), need = parseInt($("#fq-need").value, 10);
        o.push("<h3>" + fqFr(w) + " x " + fqFr(h) + " in pieces</h3><p class=\"big\">" + fit.n + " <small>per " + esc(nm) + "</small></p>");
        if (!fit.n) o.push("<p>That piece is bigger than a " + esc(nm) + " (" + fqFr(W) + " x " + fqFr(H) + " in usable). Try a half yard or yardage.</p>");
        else {
          o.push("<p>Planning on " + fqFr(W) + " x " + fqFr(H) + " in usable, straight cuts only. Finished size with ¼ in seams: <strong>" + fqFr(Math.max(0, w - 0.5)) + " x " + fqFr(Math.max(0, h - 0.5)) + " in</strong>.</p>");
          if (need > 0) { var q = Math.ceil(need / fit.n); o.push("<p>For <strong>" + need + " pieces</strong> you need <strong>" + q + " " + esc(nm) + (q === 1 ? "" : "s") + "</strong>" + (q * fit.n > need ? ", with " + (q * fit.n - need) + " spare pieces" : "") + ". Buy one extra to move colours around.</p>"); }
          o.push(fqSvg(W, H, fit));
        }
        store.set("pp-fq", { m: mode, t: t.value, w: $("#fq-w").value, h: $("#fq-h").value, n: $("#fq-need").value, qw: $("#fq-qw").value, qh: $("#fq-qh").value, f: $("#fq-f").value });
      } else {
        var qw = fqN("#fq-qw", 50), qh = fqN("#fq-qh", 65), f = fqN("#fq-f", 5), cut = f + 0.5, ac = Math.ceil(qw / f - 1e-9), dn = Math.ceil(qh / f - 1e-9), sq = ac * dn, fit2 = fqFit(W, H, cut, cut);
        o.push("<h3>" + qw + " x " + qh + " in quilt top</h3>");
        if (!fit2.n) o.push("<p>A " + fqFr(cut) + " in square doesn't fit a " + esc(nm) + ". Use smaller squares or yardage.</p>");
        else {
          var fqs = Math.ceil(sq / fit2.n);
          o.push("<p class=\"big\">" + fqs + " <small>" + esc(nm) + (fqs === 1 ? "" : "s") + "</small></p>");
          o.push("<p><strong>" + sq + " squares</strong> (" + ac + " across x " + dn + " down), cut <strong>" + fqFr(cut) + " in</strong> for " + fqFr(f) + " in finished. " + fit2.n + " squares per " + esc(nm) + ". Top comes out " + (ac * f) + " x " + (dn * f) + " in before borders.</p>");
          o.push("<p>That's about <strong>" + (fqs / 4).toFixed(1) + " yards</strong> of fabric in total. Borders, binding and backing are extra: the <a href=\"" + ($("#fq-out").getAttribute("data-q") || "/quilt-size-calculator") + "\">quilt size calculator</a> works those out.</p>");
          o.push(fqSvg(W, H, fit2));
        }
        store.set("pp-fq", { m: mode, t: t.value, w: $("#fq-w").value, h: $("#fq-h").value, n: $("#fq-need").value, qw: $("#fq-qw").value, qh: $("#fq-qh").value, f: $("#fq-f").value });
      }
      $("#fq-out").innerHTML = o.join("");
    };
    var fqS = store.get("pp-fq", null);
    if (fqS) { if (fqS.m) $("#fq-mode").value = fqS.m; if (FQD[fqS.t]) $("#fq-type").value = fqS.t; [["w", "w"], ["h", "h"], ["need", "n"], ["qw", "qw"], ["qh", "qh"], ["f", "f"]].forEach(function (k) { if (fqS[k[1]] != null && fqS[k[1]] !== "") $("#fq-" + k[0]).value = fqS[k[1]]; }); }
    ["#fq-mode", "#fq-type", "#fq-w", "#fq-h", "#fq-need", "#fq-qw", "#fq-qh", "#fq-f"].forEach(function (id) { $(id).addEventListener("input", fqRun); $(id).addEventListener("change", fqRun); });
    fqRun();
  }

  /* ---------- SEAM ALLOWANCE CALCULATOR ---------- */
  if ($("#sa-mode") && $("#sa-out")) {
    var saFr = function (x) { var w = Math.floor(x + 1e-9), f = Math.round((x - w) * 8); if (f === 8) { w++; f = 0; } var F = ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f]; return (w ? w : (F ? "" : "0")) + F; };
    var saRun = function () {
      var mode = $("#sa-mode").value, u = $("#sa-u").value, sv = $("#sa-sa").value, cm = u === "cm";
      $("#sa-own-f").hidden = sv !== "own";
      $("#sa-wl").textContent = (mode === "add" ? "Finished" : "Cut") + " width"; $("#sa-hl").textContent = (mode === "add" ? "Finished" : "Cut") + " height";
      var sa;
      if (sv === "own") sa = Math.max(0, parseFloat($("#sa-own").value) || 0);
      else if (sv.indexOf("cm") === 0) { sa = parseFloat(sv.slice(2)); if (!cm) sa = sa / 2.54; }
      else { sa = parseFloat(sv); if (cm) sa = sa * 2.54; }
      var w = parseFloat($("#sa-w").value) || 0, h = parseFloat($("#sa-h").value) || 0, ns = parseInt($("#sa-sides").value, 10), nt = parseInt($("#sa-tb").value, 10), hem = Math.max(0, parseFloat($("#sa-hem").value) || 0), qty = parseInt($("#sa-qty").value, 10);
      var dw = sa * ns, dh = sa * nt + hem, sgn = mode === "add" ? 1 : -1, rw = w + sgn * dw, rh = h + sgn * dh;
      var fmt = function (x) { return cm ? (Math.round(x * 10) / 10) + " cm" : saFr(x) + " in" + (Math.abs(x * 8 - Math.round(x * 8)) > 0.01 ? " (" + (Math.round(x * 100) / 100) + ")" : ""); };
      var alt = function (x) { return cm ? (x / 2.54).toFixed(2) + " in" : (x * 2.54).toFixed(1) + " cm"; };
      var o = [];
      o.push("<h3>" + (mode === "add" ? "Cut your piece" : "Finished size") + "</h3><p class=\"big\">" + fmt(rw) + " x " + fmt(rh) + "</p>");
      if (rw <= 0 || rh <= 0) o.push("<p>⚠ The allowances are bigger than the piece. Check the numbers and units.</p>");
      else {
        o.push("<p>About " + alt(rw) + " x " + alt(rh) + ". Seam allowance " + fmt(sa) + " on " + ns + " side edge" + (ns === 1 ? "" : "s") + " (" + (sgn > 0 ? "+" : "-") + fmt(dw) + " across) and " + nt + " top/bottom edge" + (nt === 1 ? "" : "s") + (hem ? " plus a " + fmt(hem) + " hem" : "") + " (" + (sgn > 0 ? "+" : "-") + fmt(dh) + " down).</p>");
        if (qty > 0) {
          var aw = mode === "add" ? rw : w, ah = mode === "add" ? rh : h, area = aw * ah * qty, ya = cm ? area / (100 * 100) : area / (36 * 36);
          var fw = cm ? 110 : 42, per = Math.floor(fw / aw + 1e-9), len = per > 0 ? Math.ceil(qty / per) * ah : 0;
          o.push("<p>For <strong>" + qty + " pieces</strong>: " + (per > 0 ? per + " fit across " + fw + (cm ? " cm" : " in") + " wide fabric, so buy about <strong>" + (cm ? (len / 100).toFixed(2) + " m" : (len / 36).toFixed(2) + " yd") + "</strong> plus a little for straightening and shrinkage." : "the piece is wider than standard " + fw + (cm ? " cm" : " in") + " fabric; turn it or use wide fabric.") + "</p>");
        }
        var S = 200 / Math.max(mode === "add" ? rw : w, mode === "add" ? rh : h), CW = (mode === "add" ? rw : w) * S, CH = (mode === "add" ? rh : h) * S;
        var l = (ns >= 1 ? sa : 0) * S, r = (ns >= 2 ? sa : 0) * S, tp = (nt >= 1 ? sa : 0) * S, bt = ((nt >= 2 ? sa : 0) + hem) * S;
        var svg = '<rect x="2" y="2" width="' + CW.toFixed(1) + '" height="' + CH.toFixed(1) + '" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>' +
          '<rect x="' + (2 + l).toFixed(1) + '" y="' + (2 + tp).toFixed(1) + '" width="' + Math.max(1, CW - l - r).toFixed(1) + '" height="' + Math.max(1, CH - tp - bt).toFixed(1) + '" fill="#fbf8f1" stroke="#b8326a" stroke-width="2" stroke-dasharray="7 5"/>';
        o.push('<figure class="sb-prev"><svg viewBox="0 0 ' + (CW + 4).toFixed(0) + " " + (CH + 4).toFixed(0) + '" role="img" aria-label="Cut line and stitching line, to scale">' + svg + "</svg><figcaption>Solid = cut, dashed = sew (to scale). Edges with no allowance are folds or already finished.</figcaption></figure>");
      }
      $("#sa-out").innerHTML = o.join("");
      store.set("pp-sa", { m: mode, u: u, s: sv, o: $("#sa-own").value, w: $("#sa-w").value, h: $("#sa-h").value, si: $("#sa-sides").value, tb: $("#sa-tb").value, he: $("#sa-hem").value, q: $("#sa-qty").value });
    };
    var saS = store.get("pp-sa", null);
    if (saS) { $("#sa-mode").value = saS.m || "add"; $("#sa-u").value = saS.u || "in"; $("#sa-sa").value = saS.s || "0.5"; if (!$("#sa-sa").value) $("#sa-sa").value = "0.5"; $("#sa-own").value = saS.o || 0.5; $("#sa-w").value = saS.w || 16; $("#sa-h").value = saS.h || 16; $("#sa-sides").value = saS.si || "2"; $("#sa-tb").value = saS.tb || "2"; $("#sa-hem").value = saS.he || ""; $("#sa-qty").value = saS.q || ""; }
    ["#sa-mode", "#sa-u", "#sa-sa", "#sa-own", "#sa-w", "#sa-h", "#sa-sides", "#sa-tb", "#sa-hem", "#sa-qty"].forEach(function (id) { $(id).addEventListener("input", saRun); $(id).addEventListener("change", saRun); });
    saRun();
  }

  /* ---------- CROCHET PROJECT PLANNER PRINTABLE ---------- */
  if ($("#pjp-sheet") && $("#pjp-out")) {
    var PJF = ["name", "pattern", "size", "yarn", "colour", "yards", "tool", "gauge", "for", "start", "due"];
    var pjpV = function (k) { var el = $("#pjp-" + k); return el ? el.value.trim() : ""; };
    var pjpD = function (v) { if (!v) return ""; var d = new Date(v + "T12:00:00"); return isNaN(d) ? v : d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }); };
    var pjpLine = function (label, v) { return '<div class="pjp-ln"><span>' + esc(label) + '</span><b>' + esc(v) + "</b></div>"; };
    var pjpGrid = function (n) { var s = '<div class="pjp-grid">'; for (var i = 1; i <= n; i++) s += "<i>" + i + "</i>"; return s + "</div>"; };
    var pjpRun = function () {
      var sh = $("#pjp-sheet").value, cr = $("#pjp-craft").value, kn = cr === "Knitting", tl = kn ? "Needle size" : (cr === "Crochet" ? "Hook size" : "Hook / needle size"), rows = Math.max(5, Math.min(300, parseInt($("#pjp-rows").value, 10) || 60)), h = "";
      $("#pjp-proj").hidden = sh === "yarn" || sh === "year"; $("#pjp-rows-f").hidden = !(sh === "project" || sh === "tracker");
      if (sh === "project") {
        h = '<p class="pjp-k">' + esc(cr) + ' project</p><h3 class="pjp-t">' + (esc(pjpV("name")) || "&nbsp;") + "</h3>" +
          '<div class="pjp-2">' + pjpLine("Pattern", pjpV("pattern")) + pjpLine("Size", pjpV("size")) + pjpLine("Yarn", pjpV("yarn")) + pjpLine("Colours / dye lot", pjpV("colour")) + pjpLine("Yards / skeins", pjpV("yards")) + pjpLine(tl, pjpV("tool")) + pjpLine("Gauge", pjpV("gauge")) + pjpLine("Made for", pjpV("for")) + pjpLine("Started", pjpD(pjpV("start"))) + pjpLine("Due", pjpD(pjpV("due"))) + "</div>" +
          '<p class="pjp-h">Rows / rounds</p>' + pjpGrid(Math.min(rows, 120)) +
          '<div class="pjp-2"><div><p class="pjp-h">Changes and notes</p><div class="pjp-lines"><i></i><i></i><i></i><i></i><i></i></div></div><div><p class="pjp-h">Finishing</p><ul class="pjp-ck"><li>Gauge swatch</li><li>Weave in ends</li><li>Block</li><li>Label / care tag</li><li>Photo taken</li><li>Hours: ______  Cost: ______</li></ul></div></div>';
      } else if (sh === "tracker") {
        h = '<p class="pjp-k">' + esc(cr) + ' row tracker</p><h3 class="pjp-t">' + (esc(pjpV("name")) || "&nbsp;") + "</h3>" + '<p class="pjp-sm">Strike through a box at the end of every row or round. Colour every repeat start first.</p>' + pjpGrid(rows);
      } else if (sh === "yarn") {
        var tr = ""; for (var i = 0; i < 12; i++) tr += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>";
        h = '<p class="pjp-k">' + esc(cr) + '</p><h3 class="pjp-t">Yarn shopping list</h3><table class="pjp-tb"><thead><tr><th>Project</th><th>Yarn</th><th>Weight</th><th>Colour / lot</th><th>Yards</th><th>Skeins</th><th>✓</th></tr></thead><tbody>' + tr + "</tbody></table>";
      } else {
        var M = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], b = "";
        M.forEach(function (m) { b += '<div class="pjp-mo"><b>' + m + "</b><i></i><i></i><i></i></div>"; });
        h = '<p class="pjp-k">' + esc(cr) + '</p><h3 class="pjp-t">2027 make list</h3><div class="pjp-yr">' + b + '</div><div class="pjp-2"><div><p class="pjp-h">Gifts to make</p><div class="pjp-lines"><i></i><i></i><i></i></div></div><div><p class="pjp-h">Skills to learn</p><div class="pjp-lines"><i></i><i></i><i></i></div></div></div>';
      }
      $("#pjp-out").innerHTML = h + '<p class="pjp-foot">purlandpaperco.com · free crochet project planner</p>';
      var sv = { s: sh, c: cr, r: $("#pjp-rows").value }; PJF.forEach(function (k) { sv[k] = pjpV(k); }); store.set("pp-pjp", sv);
    };
    var pjS = store.get("pp-pjp", null);
    if (pjS) { if (pjS.s) $("#pjp-sheet").value = pjS.s; if (pjS.c) $("#pjp-craft").value = pjS.c; if (pjS.r) $("#pjp-rows").value = pjS.r; PJF.forEach(function (k) { if (pjS[k]) $("#pjp-" + k).value = pjS[k]; }); }
    ["#pjp-sheet", "#pjp-craft", "#pjp-rows"].concat(PJF.map(function (k) { return "#pjp-" + k; })).forEach(function (id) { $(id).addEventListener("input", pjpRun); $(id).addEventListener("change", pjpRun); });
    $("#pjp-clear").addEventListener("click", function () { PJF.forEach(function (k) { $("#pjp-" + k).value = ""; }); pjpRun(); });
    $("#pjp-print").addEventListener("click", function () {
      var bx = document.getElementById("pjp-printbox"); if (!bx) { bx = document.createElement("div"); bx.id = "pjp-printbox"; bx.className = "pjp-paper"; document.body.appendChild(bx); }
      bx.innerHTML = $("#pjp-out").innerHTML; document.body.classList.add("print-pjp"); window.print();
      setTimeout(function () { document.body.classList.remove("print-pjp"); }, 500);
    });
    pjpRun();
  }

  /* ---------- FABRIC YARDAGE CALCULATOR ---------- */
  if ($("#fy-fw") && $("#fy-out") && $("#fy-data")) {
    var FYD = JSON.parse($("#fy-data").textContent);
    var fyFr = function (y) { var w = Math.floor(y + 1e-9), f = Math.round((y - w) * 8); if (f === 8) { w++; f = 0; } return (w ? w : "") + ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f] + " yd"; };
    var fyIds = ["#fy-u", "#fy-fw", "#fy-own", "#fy-sa", "#fy-x", "#fy-dir", "#fy-w0", "#fy-h0", "#fy-q0", "#fy-w1", "#fy-h1", "#fy-q1", "#fy-w2", "#fy-h2", "#fy-q2"];
    var fyCols = ["#2f8f8a", "#b8326a", "#e39a14"];
    var fyRun = function () {
      var cm = $("#fy-u").value === "cm", fwv = $("#fy-fw").value, rot = !$("#fy-dir").checked;
      $("#fy-own-f").hidden = fwv !== "own";
      var FW = fwv === "own" ? (parseFloat($("#fy-own").value) || 0) : parseFloat(fwv) * (cm ? 2.54 : 1);
      var sa = parseFloat($("#fy-sa").value) || 0; if (cm) sa *= 2.54;
      var ex = parseFloat($("#fy-x").value) || 0, u = cm ? " cm" : " in", P = [], o = [], bad = null;
      for (var i = 0; i < 3; i++) {
        var w = parseFloat($("#fy-w" + i).value) || 0, h = parseFloat($("#fy-h" + i).value) || 0, q = parseInt($("#fy-q" + i).value, 10) || 0;
        if (w > 0 && h > 0 && q > 0) P.push({ k: i, w: w + 2 * sa, h: h + 2 * sa, q: q });
      }
      if (!P.length || FW <= 0) { $("#fy-out").innerHTML = "<p>Type the width, length and number of at least one piece.</p>"; return; }
      var tot = 0, rows = [];
      P.forEach(function (p) {
        var best = null;
        (rot ? [[p.w, p.h], [p.h, p.w]] : [[p.w, p.h]]).forEach(function (ab) {
          if (ab[0] <= FW + 1e-9) { var per = Math.floor(FW / ab[0] + 1e-9), n = Math.ceil(p.q / per), L = n * ab[1]; if (!best || L < best.L) best = { a: ab[0], b: ab[1], per: per, n: n, L: L }; }
        });
        if (!best) bad = p; else { best.p = p; rows.push(best); tot += best.L; }
      });
      if (bad) { $("#fy-out").innerHTML = "<p>⚠ Piece " + "ABC"[bad.k] + " (" + (Math.round(bad.w * 10) / 10) + " x " + (Math.round(bad.h * 10) / 10) + u + ") is wider than the fabric both ways" + (rot ? "" : " (turning is off)") + ". Choose wider fabric or split the piece with a seam.</p>"; return; }
      var Lx = tot * (1 + ex), inches = cm ? Lx / 2.54 : Lx, yd = Math.ceil(inches / 4.5 - 1e-9) / 8, m = Math.ceil((cm ? Lx : Lx * 2.54) / 10 - 1e-9) / 10;
      o.push("<h3>Fabric to buy</h3><p class=\"big\">" + (cm ? m.toFixed(1) + " m" : fyFr(yd)) + "</p>");
      o.push("<p>" + (cm ? "About " + fyFr(yd) : "About " + m.toFixed(1) + " m") + ". Layout length " + (Math.round(tot * 10) / 10) + u + (ex ? " + " + Math.round(ex * 100) + "% extra" : "") + " on " + (Math.round(FW * 10) / 10) + u + " usable width.</p>");
      o.push("<ul>" + rows.map(function (r) { return "<li>Piece " + "ABC"[r.p.k] + ": " + r.p.q + " x " + (Math.round(r.p.w * 100) / 100) + " x " + (Math.round(r.p.h * 100) / 100) + u + (sa ? " (with seam allowance)" : "") + ", " + r.per + " across" + (r.a !== r.p.w ? " turned sideways" : "") + ", " + r.n + " row" + (r.n === 1 ? "" : "s") + " = " + (Math.round(r.L * 10) / 10) + u + "</li>"; }).join("") + "</ul>");
      var S = 260 / FW, y = 0, svg = '<rect x="0" y="0" width="260" height="' + (tot * S).toFixed(1) + '" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>', cnt = 0;
      rows.forEach(function (r) {
        var left = r.p.q;
        for (var n = 0; n < r.n; n++) { for (var c = 0; c < r.per && left > 0; c++, left--) { if (cnt++ < 400) svg += '<rect x="' + (c * r.a * S + 1).toFixed(1) + '" y="' + (y + 1).toFixed(1) + '" width="' + Math.max(1, r.a * S - 2).toFixed(1) + '" height="' + Math.max(1, r.b * S - 2).toFixed(1) + '" rx="2" fill="' + fyCols[r.p.k] + '" opacity=".85"/>'; } y += r.b * S; }
      });
      o.push('<figure class="sb-prev"><svg viewBox="-2 -2 264 ' + (tot * S + 4).toFixed(0) + '" role="img" aria-label="Cutting layout to scale">' + svg + "</svg><figcaption>Cutting layout to scale (fabric width across the top). Real layouts can often nest pieces tighter.</figcaption></figure>");
      $("#fy-out").innerHTML = o.join("");
      var st = {}; fyIds.forEach(function (id) { var el = $(id); st[id] = el.type === "checkbox" ? el.checked : el.value; }); store.set("pp-fy", st);
    };
    var fyS = store.get("pp-fy", null);
    if (fyS) fyIds.forEach(function (id) { var el = $(id); if (fyS[id] == null) return; if (el.type === "checkbox") el.checked = !!fyS[id]; else el.value = fyS[id]; });
    if (!$("#fy-fw").value) $("#fy-fw").value = "42";
    $("#fy-proj").addEventListener("change", function () {
      var p = FYD[this.value]; if (!p) return;
      $("#fy-u").value = "in"; $("#fy-sa").value = "0";
      for (var i = 0; i < 3; i++) { var r = p.p[i]; $("#fy-w" + i).value = r ? r[0] : ""; $("#fy-h" + i).value = r ? r[1] : ""; $("#fy-q" + i).value = r ? r[2] : ""; }
      fyRun();
    });
    fyIds.forEach(function (id) { $(id).addEventListener("input", fyRun); $(id).addEventListener("change", fyRun); });
    fyRun();
  }

  /* ---------- CHRISTMAS CRAFTS TO SELL: PRICE LIST ---------- */
  if ($("#cs-rate") && $("#cs-out") && $("#cs-data")) {
    var CSD = JSON.parse($("#cs-data").textContent);
    var csPrice = function (m, h, r, wh) { var b = (m + h * r) * 1.1; return wh === "etsy" ? (b + 0.45) / 0.905 : wh === "fair" ? b / 0.97 : b; };
    var csRun = function () {
      var r = Math.max(0, parseFloat($("#cs-rate").value) || 0), wh = $("#cs-where").value, g = $("#cs-g").value, mx = parseFloat($("#cs-max").value) || 99;
      var list = CSD.filter(function (x) { return (g === "all" || x[1] === g) && x[3] <= mx; });
      var rowsT = document.querySelectorAll("#cs-table tbody tr");
      CSD.forEach(function (x, i) { var tr = rowsT[i]; if (!tr) return; tr.hidden = !((g === "all" || x[1] === g) && x[3] <= mx); var td = tr.querySelectorAll("td")[3]; if (td) td.innerHTML = "<strong>$" + Math.ceil(csPrice(x[2], x[3], r, wh)) + "</strong>"; });
      var o = [];
      if (!list.length) o.push("<p>No ideas match. Try more hours or all crafts.</p>");
      else {
        var lo = list.slice().sort(function (a, b) { return csPrice(a[2], a[3], r, wh) - csPrice(b[2], b[3], r, wh); });
        o.push("<h3>" + list.length + " idea" + (list.length === 1 ? "" : "s") + " at $" + r + " an hour</h3>");
        o.push("<p>From <strong>$" + Math.ceil(csPrice(lo[0][2], lo[0][3], r, wh)) + "</strong> (" + esc(lo[0][0]) + ") to <strong>$" + Math.ceil(csPrice(lo[lo.length - 1][2], lo[lo.length - 1][3], r, wh)) + "</strong> (" + esc(lo[lo.length - 1][0]) + "). The table below now shows your prices.</p>");
        var q = lo.filter(function (x) { return x[3] <= 1.5; }).slice(0, 3);
        if (q.length) o.push("<p>Fastest to batch: " + q.map(function (x) { return esc(x[0]) + " ($" + Math.ceil(csPrice(x[2], x[3], r, wh)) + ")"; }).join(", ") + ".</p>");
        if (wh === "etsy") o.push('<p class="sub">Etsy US fees included: 6.5% transaction, 3% + $0.25 processing, $0.20 listing. Shipping and Offsite Ads are extra: check with the <a href="' + ($("#cs-out").getAttribute("data-fee") || "/etsy-fee-calculator") + '">Etsy fee calculator</a>.</p>');
        if (r < 10) o.push("<p>⚠ Below $10 an hour you're paying for your customers' gifts. Choose a faster make before you cut your rate.</p>");
      }
      $("#cs-out").innerHTML = o.join("");
      store.set("pp-cs", { r: $("#cs-rate").value, w: wh, g: g, m: $("#cs-max").value });
    };
    var csS = store.get("pp-cs", null);
    if (csS) { $("#cs-rate").value = csS.r || 15; $("#cs-where").value = csS.w || "etsy"; $("#cs-g").value = csS.g || "all"; $("#cs-max").value = csS.m || "99"; }
    ["#cs-rate", "#cs-where", "#cs-g", "#cs-max"].forEach(function (id) { $(id).addEventListener("input", csRun); $(id).addEventListener("change", csRun); });
    csRun();
  }

  /* ---------- JUNK JOURNAL VS SCRAPBOOK QUIZ ---------- */
  if ($("#jvs-form") && $("#jvs-out")) {
    var jvsRun = function () {
      var sc = { s: 0, j: 0, b: 0 }, done = 0, qs = document.querySelectorAll("#jvs-form .jvs-q");
      qs.forEach(function (f) { var c = f.querySelector("input:checked"); if (c) { done++; var p = c.value.split(":"); sc[p[0]] += parseInt(p[1], 10); } });
      var out = $("#jvs-out"), jj = out.getAttribute("data-jj"), sb = out.getAttribute("data-sb");
      if (done < qs.length) { out.innerHTML = "<p>" + done + " of " + qs.length + " answered. Pick an answer for each question to see your match.</p>"; return; }
      var d = sc.j - sc.s, h;
      if (d >= 3) h = '<h3>Junk journal</h3><p>You want the making, the textures and room to write. Start a junk journal from paper you already have: our <a href="' + jj + '">beginner guide</a> walks you through the first book.</p>';
      else if (d <= -3) h = '<h3>Scrapbook</h3><p>Your photos are the point and you want them to last. Go for an album with acid-free pages: see <a href="' + sb + '">scrapbook page sizes</a> to choose one and plan how many photos fit.</p>';
      else h = '<h3>Both: a memory junk journal</h3><p>Make a junk journal with pockets for photo prints, or a scrapbook with junk journal layers. Keep photos in sleeves or corners, away from old book pages. Start with the <a href="' + jj + '">junk journal guide</a> and the <a href="' + sb + '">scrapbook size chart</a>.</p>';
      out.innerHTML = h + '<p class="sub">Scrapbook ' + sc.s + " · Junk journal " + sc.j + "</p>";
    };
    document.querySelectorAll("#jvs-form input").forEach(function (el) { el.addEventListener("change", jvsRun); });
    jvsRun();
  }

  /* ---------- ETSY SHIPPING CALCULATOR ---------- */
  if ($("#sh-label") && $("#sh-out")) {
    var shIds = ["#sh-label", "#sh-pack", "#sh-price", "#sh-ads", "#sh-wi", "#sh-wp", "#sh-l", "#sh-w", "#sh-h"];
    var usd = function (x) { return "$" + (Math.round(x * 100) / 100).toFixed(2); };
    var shRun = function () {
      var n = function (id) { return Math.max(0, parseFloat($(id).value) || 0); };
      var L = n("#sh-label"), P = n("#sh-pack"), pr = n("#sh-price"), ads = parseFloat($("#sh-ads").value) || 0;
      var f = 0.065 + 0.03 + ads, keep = 1 - f, o = [];
      var S = (L + P) / keep, Sr = Math.ceil(S * 4 - 1e-9) / 4;
      o.push("<h3>Charge for shipping</h3><p class=\"big\">" + usd(S) + "</p>");
      o.push("<p>Covers the " + usd(L) + " label, " + usd(P) + " packaging and " + usd(S * f) + " of Etsy fees on the shipping charge (" + Math.round(f * 1000) / 10 + "%). Rounded up: <strong>" + usd(Sr) + "</strong>.</p>");
      if (pr > 0) {
        var fp = pr + S, tot = pr + S;
        var fees = tot * f + 0.25 + 0.20, net = tot - fees - L - P;
        o.push("<h3>Or offer free shipping</h3><p>Price the item at about <strong>" + usd(fp) + "</strong> instead of " + usd(pr) + "." + (fp >= 35 ? " That's over $35, so US buyers see free shipping and the listing gets the US search boost." : (fp >= 25 ? " Close to $35: buyers who add a second item reach the free shipping boost." : "")) + "</p>");
        o.push("<p>Either way you keep about <strong>" + usd(net) + "</strong> from the order after all Etsy fees (incl. $0.25 processing and $0.20 listing), the label and packaging, before your materials. Check the whole sale in the <a href=\"" + ($("#sh-out").getAttribute("data-fee") || "/etsy-fee-calculator") + "\">Etsy fee calculator</a>.</p>");
      }
      var oz = n("#sh-wi") + n("#sh-wp"), vol = n("#sh-l") * n("#sh-w") * n("#sh-h");
      if (oz > 0) {
        var tier = oz <= 4 ? "up to 4 oz" : oz <= 8 ? "4.01 to 8 oz" : oz <= 12 ? "8.01 to 12 oz" : oz < 16 ? "12.01 to 15.99 oz" : Math.ceil(oz / 16 - 1e-9) + " lb";
        var t = "<h3>Package</h3><p>" + (Math.round(oz * 10) / 10) + " oz packed (" + (Math.round(oz * 28.35)) + " g): USPS Ground Advantage step <strong>" + tier + "</strong>.";
        if (oz < 16) { var nx = oz <= 4 ? 4 : oz <= 8 ? 8 : oz <= 12 ? 12 : 15.99; if (nx - oz < 1) t += " You're within an ounce of the next step: keep the packaging light."; }
        if (vol > 1728) { var dw = Math.ceil(vol / 166); t += " The box is " + Math.round(vol) + " cu in, over 1 cubic foot, so USPS charges dimensional weight of about <strong>" + dw + " lb</strong>" + (dw * 16 > oz ? ", more than the real weight. A smaller box or a soft mailer would cost less." : "."); }
        else if (vol > 0) t += " Box " + Math.round(vol) + " cu in: under 1 cubic foot, so it's priced by real weight.";
        o.push(t + "</p>");
      }
      $("#sh-out").innerHTML = o.join("");
      var st = {}; shIds.forEach(function (id) { st[id] = $(id).value; }); store.set("pp-sh", st);
    };
    var shS = store.get("pp-sh", null);
    if (shS) shIds.forEach(function (id) { if (shS[id] != null) $(id).value = shS[id]; });
    shIds.forEach(function (id) { $(id).addEventListener("input", shRun); $(id).addEventListener("change", shRun); });
    shRun();
  }

  /* ---------- HOW TO CROSS STITCH: NEEDLE + CENTRE HELPER ---------- */
  if ($("#cx-fab") && $("#cx-out") && $("#cx-data")) {
    var CXD = JSON.parse($("#cx-data").textContent);
    var cxRun = function () {
      var d = CXD[$("#cx-fab").value] || CXD["14"], w = parseInt($("#cx-w").value, 10) || 0, h = parseInt($("#cx-h").value, 10) || 0, o = [];
      o.push("<h3>Use</h3><p class=\"big\">" + d[1] + " <small>strand" + (d[1] === "1" ? "" : "s") + "</small></p>");
      o.push("<p>Tapestry needle size <strong>" + d[3] + "</strong>, " + d[2] + " strand" + (d[2] === "1" ? "" : "s") + " for backstitch, " + d[0] + " stitches to the inch.</p>");
      if (w > 0 && h > 0) {
        var fw = w / d[0], fh = h / d[0], cw = Math.ceil(w / 2), ch = Math.ceil(h / 2);
        o.push("<h3>Centre of the design</h3><p>Stitch " + cw + " across and " + ch + " down (counting from the top left of the chart). Start there, at the centre of your fabric.</p>");
        o.push("<p>Finished size about <strong>" + fw.toFixed(1) + " x " + fh.toFixed(1) + " in</strong> (" + (fw * 2.54).toFixed(1) + " x " + (fh * 2.54).toFixed(1) + " cm). Cut the fabric about <strong>" + Math.ceil(fw + 6) + " x " + Math.ceil(fh + 6) + " in</strong> to leave 3 in on each side. Floss amounts: <a href=\"" + ($("#cx-out").getAttribute("data-calc") || "/cross-stitch-calculator") + "\">cross stitch calculator</a>.</p>");
      }
      $("#cx-out").innerHTML = o.join("");
      store.set("pp-cx", { f: $("#cx-fab").value, w: $("#cx-w").value, h: $("#cx-h").value });
    };
    var cxS = store.get("pp-cx", null);
    if (cxS) { if (CXD[cxS.f]) $("#cx-fab").value = cxS.f; if (cxS.w) $("#cx-w").value = cxS.w; if (cxS.h) $("#cx-h").value = cxS.h; }
    ["#cx-fab", "#cx-w", "#cx-h"].forEach(function (id) { $(id).addEventListener("input", cxRun); $(id).addEventListener("change", cxRun); });
    cxRun();
  }

  /* ---------- GRANNY SQUARE PATTERN WRITER ---------- */
  if ($("#gq-n") && $("#gq-out")) {
    var gqRun = function () {
      var N = Math.min(20, Math.max(1, parseInt($("#gq-n").value, 10) || 1)), uk = $("#gq-t").value === "uk", cc = $("#gq-c").value === "2", y = $("#gq-y").value;
      var D = uk ? "tr" : "dc", SL = uk ? "ss" : "sl st", R = [], o = [];
      R.push("<li><strong>Start:</strong> ch 4, " + SL + " in first ch to form a ring.</li>");
      R.push("<li><strong>Round 1:</strong> ch 3 (counts as " + D + "), 2 " + D + " in ring, ch 2, [3 " + D + " in ring, ch 2] 3 times, " + SL + " to top of ch-3. <em>(4 clusters, 12 " + D + ")</em></li>");
      var mv = cc ? "Fasten off. Join new colour in any ch-2 corner sp, " : SL + " in next 2 " + D + " and into ch-2 corner sp, ";
      for (var r = 2; r <= N; r++) {
        var side = r - 2, sd = side ? ", [3 " + D + " in next ch-1 sp, ch 1] " + (side === 1 ? "once" : side + " times") : "";
        R.push("<li><strong>Round " + r + ":</strong> " + mv + "ch 3, (2 " + D + ", ch 2, 3 " + D + ") in same sp, ch 1" + sd + ", *(3 " + D + ", ch 2, 3 " + D + ") in next corner sp, ch 1" + sd + "; rep from * twice more, " + SL + " to top of ch-3. <em>(" + 4 * r + " clusters, " + 12 * r + " " + D + ")</em></li>");
      }
      R.push("<li><strong>Finish:</strong> fasten off and weave in the ends.</li>");
      var pr = { dk: [0.8, "DK"], w: [1.0, "worsted"], b: [1.3, "bulky"] }[y] || [1, "worsted"];
      var side_in = (N + 0.1) * pr[0], yd = side_in * side_in * (y === "dk" ? 1.4 : y === "b" ? 0.65 : 1.0); /* yd per sq in, our estimate: 5-round worsted ~5 in, ~26 yd */
      o.push("<h3>Your square</h3><p class=\"big\">" + side_in.toFixed(1) + " <small>in</small></p>");
      o.push("<p>About " + (side_in * 2.54).toFixed(0) + " cm across in " + pr[1] + ", using roughly <strong>" + Math.round(yd) + " yd</strong> (" + Math.round(yd * 0.9144) + " m) of yarn. Estimates: measure your first square. Planning a blanket? Use the <a href=\"" + ($("#gq-out").getAttribute("data-bl") || "/granny-square-blanket-calculator") + "\">granny square blanket calculator</a>.</p>");
      o.push("<h3>Pattern (" + (uk ? "UK" : "US") + " terms)</h3><ol class=\"gq-pat\">" + R.join("") + "</ol>");
      o.push('<p><button type="button" class="btn ghost sm" id="gq-print">Print the pattern</button></p>');
      $("#gq-out").innerHTML = o.join("");
      $("#gq-print").addEventListener("click", function () { window.print(); });
      store.set("pp-gq", { n: $("#gq-n").value, t: $("#gq-t").value, c: $("#gq-c").value, y: $("#gq-y").value });
    };
    var gqS = store.get("pp-gq", null);
    if (gqS) { ["n", "t", "c", "y"].forEach(function (k) { if (gqS[k]) $("#gq-" + k).value = gqS[k]; }); }
    ["#gq-n", "#gq-t", "#gq-c", "#gq-y"].forEach(function (id) { $(id).addEventListener("input", gqRun); $(id).addEventListener("change", gqRun); });
    gqRun();
  }

  /* ---------- GRANNY SQUARE JOINING CALCULATOR ---------- */
  if ($("#gj-a") && $("#gj-out")) {
    /* yarn per inch of seam, our rough estimates for worsted: sewn ~2.5-3x, slip stitch ~4x, single crochet ~6x, join as you go 0 */
    var GJ_F = { whip: [2.5, "whip stitch"], mattress: [3, "mattress stitch"], slip: [4, "slip stitch join"], sc: [6, "single crochet join"], jaygo: [0, "join as you go"] };
    var gjRun = function () {
      var a = Math.min(60, Math.max(1, parseInt($("#gj-a").value, 10) || 1)), b = Math.min(60, Math.max(1, parseInt($("#gj-b").value, 10) || 1));
      var s = Math.min(30, Math.max(1, parseFloat($("#gj-s").value) || 6)), m = GJ_F[$("#gj-m").value] ? $("#gj-m").value : "whip", f = GJ_F[m];
      var n = a * b, shortS = (a - 1) * b + (b - 1) * a, longS = (a - 1) + (b - 1), len = s * shortS, yd = len * f[0] / 36 * 1.1;
      var o = [];
      o.push("<h3>Your blanket</h3><p class=\"big\">" + n + " <small>squares</small></p>");
      o.push("<p>About <strong>" + (a * s).toFixed(1).replace(/\.0$/, "") + " × " + (b * s).toFixed(1).replace(/\.0$/, "") + " in</strong> (" + Math.round(a * s * 2.54) + " × " + Math.round(b * s * 2.54) + " cm) before a border.</p>");
      if (n < 2) { o.push("<p>Add a second square to see the seams.</p>"); }
      else {
        o.push("<h3>Seams</h3><p><strong>" + longS + " long seams</strong> if you join in strips (" + (a - 1) + " one way, " + (b - 1) + " the other), instead of " + shortS + " short ones. Total seam length about <strong>" + Math.round(len / 12) + " ft</strong> (" + (len * 0.0254).toFixed(1) + " m).</p>");
        if (m === "jaygo") o.push("<h3>Joining yarn</h3><p>No extra yarn: with join as you go the joins are worked on the last round of each square. You'll weave in only the ends from the squares themselves.</p>");
        else o.push("<h3>Joining yarn</h3><p class=\"big\">" + Math.ceil(yd) + " <small>yd</small></p><p>About " + Math.ceil(yd * 0.9144) + " m for a " + f[1] + " in worsted yarn, including about 10% for tails. That's our rough estimate: work 4 in of seam and measure your yarn to check. Joining in strips leaves about <strong>" + (longS * 2) + " ends</strong> to weave in.</p>");
      }
      o.push("<p class=\"sub\">Need squares and yarn for the whole blanket? Use the <a href=\"" + ($("#gj-out").getAttribute("data-bl") || "/granny-square-blanket-calculator") + "\">granny square blanket calculator</a>.</p>");
      $("#gj-out").innerHTML = o.join("");
      store.set("pp-gj", { a: $("#gj-a").value, b: $("#gj-b").value, s: $("#gj-s").value, m: $("#gj-m").value });
    };
    var gjS = store.get("pp-gj", null);
    if (gjS) { ["a", "b", "s", "m"].forEach(function (k) { if (gjS[k]) $("#gj-" + k).value = gjS[k]; }); }
    ["#gj-a", "#gj-b", "#gj-s", "#gj-m"].forEach(function (id) { $(id).addEventListener("input", gjRun); $(id).addEventListener("change", gjRun); });
    gjRun();
  }

  /* ---------- KNITTING INCREASE PICKER ---------- */
  if ($("#ki-hole") && $("#ki-out")) {
    var KI = {
      kfb: ["Knit front and back (kfb)", "Easy to learn and easy to count. The small bump it leaves hides in garter stitch and at edges.", ["Knit the stitch but leave it on the left needle.", "Knit into the back loop of the same stitch.", "Slip it off: one stitch is now two."]],
      m1l: ["Make 1 left (M1L)", "Almost invisible and closes without a hole when it's twisted.", ["Pick up the bar between stitches from front to back with the left needle.", "Knit it through the back loop."]],
      lift: ["Lifted increase (RLI or LLI)", "The least visible increase in stocking stitch, for when it really needs to disappear.", ["RLI: knit into the right leg of the stitch below the next stitch, then knit the stitch.", "LLI: knit a stitch, then knit into the left leg of the stitch two rows below it."]],
      pair: ["M1R before the marker, M1L after it", "A mirrored pair, so the increases lean away from the line on both sides, as on a raglan seam or a sleeve.", ["Knit to the marker and work M1R (pick up the bar from back to front and knit it through the front loop).", "Slip the marker and work M1L (pick up the bar from front to back and knit it through the back loop)."]],
      yo: ["Yarn over (yo)", "Adds a stitch and a neat eyelet hole on purpose: lace, raglan lines, pretty edges.", ["Bring the yarn to the front between the needles.", "Knit the next stitch: the yarn goes over the needle and makes the new loop.", "Work the loop as a normal stitch on the next row."]],
      yopair: ["Yarn over each side of the marker", "Two eyelets frame the line, a classic look on top-down raglans and shawls.", ["Knit to the marker, yarn over, slip the marker, yarn over.", "Work each yarn over as a stitch on the next row."]],
      rib: ["M1 worked as knit or purl (M1 or M1P)", "In ribbing the new stitch has to match the rib, so pick up the bar and knit or purl it twisted to keep the column going.", ["Pick up the bar between stitches from front to back.", "Knit it through the back loop if a knit column is next to it, or purl it through the back loop (M1P) if a purl column is."]]
    };
    var kiRun = function () {
      var hole = segVal($("#ki-hole")) || "no", where = segVal($("#ki-where")) || "edge", lvl = segVal($("#ki-lvl")) || "new", st = $("#ki-st").value, k, extra = "";
      if (hole === "yes") { k = where === "pair" ? "yopair" : "yo"; if (where === "edge") extra = "At an edge, work it one stitch in: k1, yo, knit to the last stitch, yo, k1."; }
      else if (st === "rib") k = "rib";
      else if (where === "pair") k = "pair";
      else if (st === "gt" || lvl === "new") { k = "kfb"; if (where === "edge") extra = "A common way at the edges: kfb into the first stitch and into the second-to-last stitch, so the edge stitch stays neat."; if (st === "st" && lvl === "new") extra += (extra ? " " : "") + "In stocking stitch the kfb bump shows a little. Once you're comfortable, try M1L instead."; }
      else { k = where === "mid" ? "lift" : "m1l"; if (where === "edge") { k = "pair"; extra = "A common recipe at the edges: k1, M1L, knit to the last stitch, M1R, k1. Try it on a swatch; some patterns mirror it the other way."; } }
      var x = KI[k], o = [];
      o.push("<h3>Use</h3><p class=\"big\" style=\"font-size:1.6rem\">" + esc(x[0]) + "</p><p>" + esc(x[1]) + "</p><ol>" + x[2].map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ol>");
      if (extra) o.push("<p>" + esc(extra) + "</p>");
      if (where === "mid") o.push("<p>Spacing several increases across a row? The <a href=\"" + ($("#ki-out").getAttribute("data-ev") || "/increase-decrease-calculator") + "\">increase evenly calculator</a> writes out the row for you.</p>");
      $("#ki-out").innerHTML = o.join("");
      store.set("pp-ki", { hole: hole, where: where, lvl: lvl, st: st });
    };
    var kiS = store.get("pp-ki", null);
    if (kiS) {
      ["hole", "where", "lvl"].forEach(function (g) { if (kiS[g]) $$("#ki-" + g + " button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === kiS[g]); }); });
      if (kiS.st) $("#ki-st").value = kiS.st;
    }
    seg($("#ki-hole"), kiRun); seg($("#ki-where"), kiRun); seg($("#ki-lvl"), kiRun);
    $("#ki-st").addEventListener("change", kiRun);
    kiRun();
  }

  /* ---------- CROCHET INCREASE WRITER ---------- */
  if ($("#ci-a") && $("#ci-out")) {
    var CI_N = { us: { sc: "sc", hdc: "hdc", dc: "dc" }, uk: { sc: "dc", hdc: "htr", dc: "tr" } };
    var ciText = function (tok, nm) {
      /* tok: array of "p"/"i"; compress into "(sc 3, inc) x 6" style */
      var items = [], i = 0;
      while (i < tok.length) {
        var p = 0; while (i < tok.length && tok[i] === "p") { p++; i++; }
        var inc = i < tok.length; if (inc) i++;
        items.push([p, inc]);
      }
      var out = [], j = 0;
      while (j < items.length) {
        var k = j; while (k + 1 < items.length && items[k + 1][0] === items[j][0] && items[k + 1][1] === items[j][1]) k++;
        var cnt = k - j + 1, it = items[j], part = (it[0] ? nm + " " + it[0] : "") + (it[1] ? (it[0] ? ", " : "") + "inc" : "");
        if (part) out.push(cnt > 1 ? "(" + part + ") " + cnt + " times" : part);
        j = k + 1;
      }
      return out.join(", ");
    };
    var ciRun = function () {
      var a = Math.min(500, Math.max(1, parseInt($("#ci-a").value, 10) || 1)), b = Math.min(1000, Math.max(1, parseInt($("#ci-b").value, 10) || 1));
      var w = segVal($("#ci-w")) || "round", t = segVal($("#ci-t")) || "us", st = CI_N[t][$("#ci-s").value] ? $("#ci-s").value : "sc", nm = CI_N[t][st], o = [];
      var k = b - a;
      if (k <= 0) {
        o.push("<h3>That's not an increase</h3><p>" + (k === 0 ? "Same count: just work 1 " + nm + " in each stitch." : "You want fewer stitches, so you need to decrease. See <a href=\"" + ($("#ci-out").getAttribute("data-dec") || "/how-to-crochet-decrease") + "\">how to decrease in crochet</a>.") + "</p>");
      } else if (k > a) {
        o.push("<h3>More than double</h3><p>Going from " + a + " to " + b + " needs " + k + " increases, but one round can at most double (inc in every stitch makes " + (2 * a) + "). Work <strong>inc in every stitch</strong> this round, then increase " + (b - 2 * a) + " more next round.</p>");
      } else {
        var q = Math.floor(a / k), r = a % k, sz = [], acc = 0;
        for (var g = 0; g < k; g++) { var big = Math.floor((g + 1) * r / k) > Math.floor(g * r / k); sz.push(q + (big ? 1 : 0)); acc += sz[g]; }
        var tok = []; sz.forEach(function (s) { for (var x = 0; x < s - 1; x++) tok.push("p"); tok.push("i"); });
        var lead = Math.floor((sz[0] - 1) / 2), rot = tok.slice(lead).concat(tok.slice(0, lead));
        o.push("<h3>" + k + " increases</h3><p class=\"big\" style=\"font-size:1.4rem\">" + esc(w === "row" ? ciText(rot, nm) : ciText(tok, nm)) + "</p>");
        o.push("<p>That makes <strong>" + b + " stitches</strong> (" + a + " + " + k + "). Inc = 2 " + esc(nm) + " in the same stitch" + (t === "uk" ? " (UK terms)" : "") + ".</p>");
        if (w === "round") {
          if (lead > 0) o.push("<h3>Staggered version</h3><p>" + esc(ciText(rot, nm)) + "</p><p class=\"sub\">Use it on every other round so the increases don't stack up into corners and your circle stays round.</p>");
          if (k === 6 && st === "sc" || k === 12 && st === "dc") o.push("<p class=\"sub\">Making a flat circle? The <a href=\"" + ($("#ci-out").getAttribute("data-circ") || "/crochet-circle-calculator") + "\">crochet circle calculator</a> writes every round.</p>");
        } else if (lead > 0) {
          o.push("<p class=\"sub\">The row starts with " + lead + " plain stitch" + (lead === 1 ? "" : "es") + " so no increase lands on the edge.</p>");
        }
      }
      $("#ci-out").innerHTML = o.join("");
      store.set("pp-ci", { a: $("#ci-a").value, b: $("#ci-b").value, s: $("#ci-s").value, w: w, t: t });
    };
    var ciS = store.get("pp-ci", null);
    if (ciS) {
      ["a", "b", "s"].forEach(function (x) { if (ciS[x]) $("#ci-" + x).value = ciS[x]; });
      ["w", "t"].forEach(function (g) { if (ciS[g]) $$("#ci-" + g + " button").forEach(function (bt) { bt.setAttribute("aria-pressed", bt.getAttribute("data-v") === ciS[g]); }); });
    }
    ["#ci-a", "#ci-b", "#ci-s"].forEach(function (id) { $(id).addEventListener("input", ciRun); $(id).addEventListener("change", ciRun); });
    seg($("#ci-w"), ciRun); seg($("#ci-t"), ciRun);
    ciRun();
  }

  /* ---------- EMBROIDERY TRANSFER PICKER ---------- */
  if ($("#et-c") && $("#et-out")) {
    var ET = {
      light: ["Trace with light and a water-soluble pen", ["Tape the pattern to a bright window, light pad or tablet on full white.", "Tape the fabric over it and trace with a water-soluble fabric marker.", "Stitch, then soak in cool water to remove the lines. Don't iron first."]],
      lightdry: ["Trace with light and a heat-erasable pen or light pencil", ["Tape the pattern to a bright window or light pad, fabric on top.", "Trace thin lines with a heat-erasable pen, or a sharp light pencil your stitches will cover.", "Stitch, then press lightly to clear heat-erasable lines (they can show again in the cold)."]],
      wss: ["Water-soluble stick-on stabilizer", ["Print the design onto the stabilizer sheet (check the pack) or trace it on.", "Peel and stick it in place, then hoop the fabric with it.", "Stitch through both layers, trim the extra and soak until it dissolves."]],
      carbon: ["White or yellow transfer (carbon) paper", ["Lay the fabric on a hard surface, transfer paper colour side down, pattern on top.", "Pin it all and draw over the lines with a ballpoint or stylus, pressing firmly.", "Check one corner before unpinning. Choose a wash-out paper if you can."]],
      tissue: ["Tissue paper or tear-away", ["Trace the design onto tissue paper or tear-away stabilizer.", "Tack it to the fabric with big running stitches round the edge.", "Stitch through it, then tear the paper away gently and pick out bits with tweezers."]]
    };
    var etRun = function () {
      var c = segVal($("#et-c")) || "light", k = segVal($("#et-k")) || "thin", w = segVal($("#et-w")) || "yes", d = segVal($("#et-d")) || "fine", best, alt, why;
      if (c === "light" && k === "thin") { best = w === "yes" ? "light" : "lightdry"; alt = w === "yes" ? "wss" : "tissue"; why = "Light, thin fabric lets the pattern show through, so tracing is quickest."; }
      else if (k === "thick") { best = w === "yes" ? "wss" : "tissue"; alt = w === "yes" ? "tissue" : (c === "dark" && d === "bold" ? "carbon" : "wss"); why = "Thick or textured fabric hides a traced line, so the design sits on top of it instead."; }
      else if (c === "mid") { best = w === "yes" ? (d === "fine" ? "wss" : "light") : "tissue"; alt = w === "yes" ? "carbon" : "carbon"; why = "Medium colours are hit and miss with light, so test a window first."; }
      else { best = w === "yes" ? "wss" : (d === "bold" ? "carbon" : "tissue"); alt = w === "yes" ? (d === "bold" ? "carbon" : "tissue") : (d === "bold" ? "tissue" : "carbon"); why = "You can't see through dark fabric, so trace onto something that sits on top, or use a light-coloured transfer paper."; }
      if (alt === best) alt = best === "tissue" ? "carbon" : "tissue";
      if (w === "no" && alt === "wss") alt = "carbon";
      var x = ET[best], y = ET[alt], o = [];
      o.push("<h3>Best for you</h3><p class=\"big\" style=\"font-size:1.5rem\">" + esc(x[0]) + "</p><p>" + esc(why) + "</p><ol>" + x[1].map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ol>");
      o.push("<h3>Also works</h3><p><strong>" + esc(y[0]) + ".</strong> " + esc(y[1][0]) + "</p>");
      if (d === "fine" && best === "carbon") o.push("<p class=\"sub\">Carbon lines are thicker than a pen line, so keep fine lettering simple.</p>");
      o.push("<p class=\"sub\">Need a design? Try the <a href=\"" + ($("#et-out").getAttribute("data-pat") || "/embroidery-patterns") + "\">embroidery pattern generator</a>. Always test a marker on a scrap first.</p>");
      $("#et-out").innerHTML = o.join("");
      store.set("pp-et", { c: c, k: k, w: w, d: d });
    };
    var etS = store.get("pp-et", null);
    if (etS) ["c", "k", "w", "d"].forEach(function (g) { if (etS[g]) $$("#et-" + g + " button").forEach(function (bt) { bt.setAttribute("aria-pressed", bt.getAttribute("data-v") === etS[g]); }); });
    ["c", "k", "w", "d"].forEach(function (g) { seg($("#et-" + g), etRun); });
    etRun();
  }

  /* ---------- BUTTON SPACING CALCULATOR ---------- */
  if ($("#bs-l") && $("#bs-out")) {
    var bsF = function (v, u) {
      if (u === "cm") return v.toFixed(1) + " cm";
      var e8 = Math.round(v * 8), w = Math.floor(e8 / 8), f = e8 % 8, fr = ["", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"][f];
      return (w ? w + (fr ? " " + fr : "") : (fr || "0")) + " in";
    };
    var bsU = "in";
    var bsRun = function () {
      var u = segVal($("#bs-u")) || "in";
      if (u !== bsU) { ["#bs-l", "#bs-t", "#bs-b"].forEach(function (id) { var v = parseFloat($(id).value); if (!isNaN(v)) $(id).value = +(u === "cm" ? v * 2.54 : v / 2.54).toFixed(u === "cm" ? 1 : 2); }); var rv = parseFloat($("#bs-r").value); if (rv) $("#bs-r").value = +(u === "cm" ? rv / 2.54 : rv * 2.54).toFixed(1); bsU = u; }
      var L = Math.max(0.5, parseFloat($("#bs-l").value) || 0), n = Math.min(40, Math.max(2, parseInt($("#bs-n").value, 10) || 2));
      var t = Math.max(0, parseFloat($("#bs-t").value) || 0), b = Math.max(0, parseFloat($("#bs-b").value) || 0), rpi = parseFloat($("#bs-r").value) || 0, o = [];
      var span = L - t - b;
      if (span <= 0) { o.push("<h3>Check the numbers</h3><p>The top and bottom gaps add up to more than the opening.</p>"); }
      else {
        var gap = span / (n - 1), pos = [];
        for (var i = 0; i < n; i++) pos.push(t + gap * i);
        o.push("<h3>Space between buttons</h3><p class=\"big\">" + bsF(gap, u) + "</p><p>" + n + " buttons over " + bsF(span, u) + " from the top button to the bottom one" + (u === "in" ? " (" + (gap * 2.54).toFixed(1) + " cm apart)" : " (" + (gap / 2.54).toFixed(2) + " in apart)") + ".</p>");
        o.push("<h3>Mark each button from the top edge</h3><ol>" + pos.map(function (p) { return "<li>" + bsF(p, u) + (rpi > 0 ? " — about row " + Math.round(p * rpi) + " of the band" : "") + "</li>"; }).join("") + "</ol>");
        if (rpi > 0) o.push("<p class=\"sub\">Rows counted from the top of the band at " + rpi + " rows per " + (u === "cm" ? "cm" : "inch") + ". For a buttonhole band knitted from the bottom up, count from the bottom instead.</p>");
        if (gap > (u === "cm" ? 12 : 4.75)) o.push("<p class=\"sub\">Gaps over about " + (u === "cm" ? "12 cm" : "4.75 in") + " can gape on a fitted top. Try one more button.</p>");
      }
      $("#bs-out").innerHTML = o.join("");
      store.set("pp-bs", { u: u, l: $("#bs-l").value, n: $("#bs-n").value, t: $("#bs-t").value, b: $("#bs-b").value, r: $("#bs-r").value });
    };
    var bsS = store.get("pp-bs", null);
    if (bsS) {
      ["l", "n", "t", "b", "r"].forEach(function (x) { if (bsS[x] != null && bsS[x] !== "") $("#bs-" + x).value = bsS[x]; });
      if (bsS.u) { $$("#bs-u button").forEach(function (bt) { bt.setAttribute("aria-pressed", bt.getAttribute("data-v") === bsS.u); }); bsU = bsS.u; }
    }
    ["#bs-l", "#bs-n", "#bs-t", "#bs-b", "#bs-r"].forEach(function (id) { $(id).addEventListener("input", bsRun); $(id).addEventListener("change", bsRun); });
    seg($("#bs-u"), bsRun);
    bsRun();
  }

  /* ---------- JUNK JOURNAL POCKET SIZE HELPER (run 11) ---------- */
  if ($("#jpk-pg") && $("#jpk-out")) {
    var jpkF = function (v) {
      var e8 = Math.round(v * 8), w = Math.floor(e8 / 8), f = e8 % 8, fr = ["", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"][f];
      return (w ? w + (fr ? " " + fr : "") : (fr || "0")) + " in";
    };
    var jpkC = function (v) { return (v * 2.54).toFixed(1) + " cm"; };
    var jpkD = function (a, b) { return jpkF(a).replace(" in", "") + " x " + jpkF(b) + " (" + (a * 2.54).toFixed(1) + " x " + jpkC(b) + ")"; };
    var r8 = function (v) { return Math.round(v * 8) / 8; };
    var ENV = [["A1 (4 bar)", 3.625, 5.125], ["#10", 4.125, 9.5], ["A2", 4.375, 5.75], ["C6", 4.49, 6.38], ["A6", 4.75, 6.5], ["A7", 5.25, 7.25], ["6 x 9 booklet", 6, 9], ["C5", 6.38, 9.02]];
    var jpkSvg = function (tw, th, body) {
      var w = +tw.toFixed(3), h = +th.toFixed(3);
      return '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + 'in" height="' + h + 'in" viewBox="0 0 ' + w + " " + h + '" style="--w:' + w + "in;--h:" + h + 'in" role="img" aria-label="Pocket cutting template"><rect width="' + w + '" height="' + h + '" fill="#fff"/>' + body + "</svg>";
    };
    var ln = function (x1, y1, x2, y2, dash) { return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' + (dash ? "#b8326a" : "#1f2a44") + '" stroke-width="0.02"' + (dash ? ' stroke-dasharray="0.08 0.06"' : "") + "/>"; };
    var tx = function (x, y, s, sz) { return '<text x="' + x + '" y="' + y + '" font-family="Inter,Arial,sans-serif" font-size="' + (sz || 0.15) + '" fill="#1f2a44" text-anchor="middle">' + esc(s) + "</text>"; };
    var rc = function (x, y, w, h, fill) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="' + (fill || "none") + '" stroke="#1f2a44" stroke-width="0.02"/>'; };
    var jpkRun = function () {
      var po = $("#jpk-pg").selectedOptions[0], fo = $("#jpk-fill").selectedOptions[0], t = $("#jpk-t").value, o = [], tpl = "", P = 0.25;
      var cust = $("#jpk-pg").value === "custom"; $("#jpk-cust").hidden = !cust;
      var pw = cust ? Math.min(14, Math.max(2, parseFloat($("#jpk-w").value) || 6)) : +po.getAttribute("data-w");
      var ph = cust ? Math.min(14, Math.max(2, parseFloat($("#jpk-h").value) || 8)) : +po.getAttribute("data-h");
      var cw = +fo.getAttribute("data-w"), ch = +fo.getAttribute("data-h"), side = false, warn = "";
      var sizeFor = function (a, b) { return { W: r8(a + 0.25), H: r8(Math.max(b - 1, b * 0.55)) }; };
      var s = sizeFor(cw, ch);
      if (t !== "corner" && t !== "band" && t !== "fold" && s.W > pw - 0.5) {
        var s2 = sizeFor(ch, cw);
        if (s2.W <= pw - 0.5) { s = s2; side = true; } else warn = "This card is wider than the page. Pick a smaller card or a bigger page.";
      }
      if (s.H > ph - 0.75) s.H = r8(ph * 0.6);
      var W = s.W, H = s.H, peek = (side ? cw : ch) - H;
      if (t === "flap" || t === "washi") {
        o.push("<h3>Pocket size</h3><p class=\"jpk-big\">" + jpkF(W).replace(" in", "") + " x " + jpkF(H) + "</p><p>" + (W * 2.54).toFixed(1) + " x " + jpkC(H) + ". Your " + esc(fo.textContent.split(" (")[0]) + (side ? " goes in sideways and" : "") + " shows about " + jpkF(peek) + " above the pocket.</p>");
        if (t === "flap") {
          o.push("<h3>Cut the card</h3><p>" + jpkD(W + 1, H + 0.5) + ". Score 1/2 in in from both sides and the bottom, fold the flaps back, trim the flap corners, and glue only the flaps.</p>");
          var x0 = P, mL = P + 0.5, mR = mL + W, xR = mR + 0.5, y0 = P, yB = P + H, yE = yB + 0.5;
          var path = "M" + mL + " " + y0 + " L" + mR + " " + y0 + " L" + xR + " " + (y0 + 0.2) + " L" + xR + " " + (yB - 0.1) + " L" + mR + " " + yB + " L" + (mR - 0.2) + " " + yE + " L" + (mL + 0.2) + " " + yE + " L" + mL + " " + yB + " L" + x0 + " " + (yB - 0.1) + " L" + x0 + " " + (y0 + 0.2) + " Z";
          tpl = jpkSvg(xR + P, yE + P, '<path d="' + path + '" fill="#fbf3f6" stroke="#1f2a44" stroke-width="0.02"/>' + ln(mL, y0, mL, yB, 1) + ln(mR, y0, mR, yB, 1) + ln(mL, yB, mR, yB, 1) + tx((mL + mR) / 2, y0 + H / 2, "pocket front") + tx((mL + mR) / 2, y0 + H / 2 + 0.22, jpkF(W) + " x " + jpkF(H), 0.12) + tx((mL + mR) / 2, yB + 0.3, "glue flap", 0.12) + tx((mL + mR) / 2, y0 + 0.2, "open top", 0.12));
        } else {
          o.push("<h3>Cut the paper</h3><p>" + jpkD(W + 0.5, H + 0.25) + ". Tape down the two sides and the bottom with washi tape about 1/2 in wide, half on the paper and half on the page.</p>");
          tpl = jpkSvg(W + 0.5 + 2 * P, H + 0.25 + 2 * P, rc(P, P, W + 0.5, H + 0.25, "#fbf3f6") + ln(P + 0.25, P, P + 0.25, P + H, 1) + ln(P + W + 0.25, P, P + W + 0.25, P + H, 1) + ln(P + 0.25, P + H, P + W + 0.25, P + H, 1) + tx(P + (W + 0.5) / 2, P + H / 2, "tape on the pink lines", 0.13));
        }
      } else if (t === "fold") {
        var Hf = r8(Math.min(Math.max(ch - 1, ch * 0.55), ph * 0.5));
        if (cw > pw - 0.25) warn = "The card is wider than the page, so it won't slide in. Try a smaller card.";
        o.push("<h3>Cut the page taller</h3><p class=\"jpk-big\">" + jpkF(pw).replace(" in", "") + " x " + jpkF(ph + Hf) + "</p><p>" + (pw * 2.54).toFixed(1) + " x " + jpkC(ph + Hf) + ". Fold the bottom " + jpkF(Hf) + " up against the front and glue or stitch the two sides, about 1/4 in in from the edge.</p>");
        o.push("<p>That makes a " + jpkD(pw, Hf) + " pocket the full width of the page, with " + jpkF(ch - Hf) + " of the card showing.</p>");
        if (ph + Hf > 11) o.push("<p class=\"sub\">Taller than a Letter sheet: glue a " + jpkF(Hf + 0.5) + " strip to the bottom of a normal page instead and fold that up.</p>");
        tpl = jpkSvg(pw + 2 * P, ph + Hf + 2 * P, rc(P, P, pw, ph + Hf, "#fff") + '<rect x="' + P + '" y="' + (P + ph) + '" width="' + pw + '" height="' + Hf + '" fill="#fbf3f6"/>' + ln(P, P + ph, P + pw, P + ph, 1) + ln(P + 0.25, P + ph, P + 0.25, P + ph + Hf, 1) + ln(P + pw - 0.25, P + ph, P + pw - 0.25, P + ph + Hf, 1) + tx(P + pw / 2, P + ph / 2, "journal page") + tx(P + pw / 2, P + ph + Hf / 2, "fold this up", 0.13) + tx(P + pw / 2, P + ph - 0.12, "fold line", 0.11));
      } else if (t === "env") {
        var need = W, best = null;
        ENV.forEach(function (en) {
          [[en[2], en[1], "long side up"], [en[1], en[2], "short side up"]].forEach(function (or) {
            if (or[0] >= need && or[1] >= H && or[0] <= pw && (!best || or[0] * H < best.w * H || (or[0] === best.w && or[1] < best.h))) best = { n: en[0], w: or[0], h: or[1], how: or[2] };
          });
        });
        o.push("<h3>Pocket size</h3><p class=\"jpk-big\">" + jpkF(W).replace(" in", "") + " x " + jpkF(H) + "</p><p>" + (W * 2.54).toFixed(1) + " x " + jpkC(H) + (side ? ", with the card sideways" : "") + ".</p>");
        if (best) {
          o.push("<h3>Envelope to use</h3><p>A <strong>" + esc(best.n) + "</strong> envelope (" + jpkF(Math.min(best.w, best.h)).replace(" in", "") + " x " + jpkF(Math.max(best.w, best.h)) + "), " + best.how + ". Cut it to " + jpkF(H) + " tall, keeping the bottom: the cut edge is the opening. Any old envelope at least " + jpkF(W) + " wide works too.</p>");
          tpl = jpkSvg(best.w + 2 * P, best.h + 2 * P, rc(P, P, best.w, best.h, "#fbf8f1") + '<path d="M' + P + " " + (P + best.h) + " L" + (P + best.w / 2) + " " + (P + best.h * 0.55) + " L" + (P + best.w) + " " + (P + best.h) + '" fill="none" stroke="#9aa6c4" stroke-width="0.02"/>' + ln(P, P + best.h - H, P + best.w, P + best.h - H, 1) + tx(P + best.w / 2, P + best.h - H - 0.1, "cut here", 0.13) + tx(P + best.w / 2, P + (best.h - H) / 2 + 0.05, "throw this part away", 0.12));
        } else o.push("<p>No standard envelope fits this page with that card. Make a glue-on pocket instead.</p>");
      } else if (t === "corner") {
        var S = r8(Math.min(3, Math.max(1.25, Math.min(cw, ch) * 0.5)));
        o.push("<h3>Cut two squares</h3><p class=\"jpk-big\">" + jpkF(S).replace(" in", "") + " x " + jpkF(S) + "</p><p>" + jpkC(S) + " squares. Fold each in half diagonally and glue one in the top left and one in the bottom right corner of the card's spot, with the folds facing in.</p><p>Place them so the card's corners sit about " + jpkF(S * 0.45) + " into each pocket.</p>");
        tpl = jpkSvg(2 * S + 3 * P, S + 2 * P, rc(P, P, S, S, "#e3f1ef") + ln(P, P + S, P + S, P, 1) + rc(2 * P + S, P, S, S, "#e3f1ef") + ln(2 * P + S, P + S, 2 * P + 2 * S, P, 1) + tx(P + S / 2, P + S + 0.18, "fold on the diagonal", 0.11));
      } else {
        var bw = cw <= 3.2 ? 1.5 : 2, L = r8(2 * pw + 1);
        o.push("<h3>Cut a strip</h3><p class=\"jpk-big\">" + jpkF(bw).replace(" in", "") + " x " + jpkF(L) + "</p><p>" + (bw * 2.54).toFixed(1) + " x " + jpkC(L) + ". Wrap it round the page, overlap the ends 1 in at the back and glue them to each other, not to the page, so the band slides.</p>");
        if (L > 10.5) o.push("<p class=\"sub\">Longer than a sheet of paper: join two strips with the overlap hidden at the back, or use ribbon.</p>");
        tpl = jpkSvg(L + 2 * P, bw + 2 * P, rc(P, P, L, bw, "#fdf0d8") + ln(P + L - 1, P, P + L - 1, P + bw, 1) + tx(P + (L - 1) / 2, P + bw / 2 + 0.05, "belly band", 0.14) + tx(P + L - 0.5, P + bw / 2 + 0.05, "glue", 0.12));
      }
      if (warn) o.unshift("<p><strong>" + esc(warn) + "</strong></p>");
      var big = false;
      if (tpl) {
        var m = tpl.match(/width="([\d.]+)in" height="([\d.]+)in"/); big = m && (+m[1] > 8 || +m[2] > 10.5);
        o.push("<h3>Template</h3><div class=\"jpk-prev\" id=\"jpk-tpl\">" + tpl + "</div>" + (big ? "<p class=\"sub\">Too big to print on one sheet: mark it out with a ruler from the sizes above.</p>" : "<p><button type=\"button\" class=\"btn gold sm\" id=\"jpk-print\">Print the template at actual size</button></p><p class=\"sub\">Print at 100% (turn off \"fit to page\"), then check one measurement with a ruler.</p>"));
      }
      $("#jpk-out").innerHTML = o.join("");
      var pb = $("#jpk-print");
      if (pb) pb.addEventListener("click", function () {
        var bx = document.getElementById("jpk-printbox"); if (!bx) { bx = document.createElement("div"); bx.id = "jpk-printbox"; document.body.appendChild(bx); }
        bx.innerHTML = $("#jpk-tpl").innerHTML; document.documentElement.classList.add("print-jpk");
        var off = function () { document.documentElement.classList.remove("print-jpk"); window.removeEventListener("afterprint", off); };
        window.addEventListener("afterprint", off); window.print(); setTimeout(off, 1500);
      });
      store.set("pp-jpk", { pg: $("#jpk-pg").value, f: $("#jpk-fill").value, t: t, w: $("#jpk-w").value, h: $("#jpk-h").value });
    };
    var jpkS = store.get("pp-jpk", null);
    if (jpkS) { if (jpkS.pg) $("#jpk-pg").value = jpkS.pg; if (jpkS.f) $("#jpk-fill").value = jpkS.f; if (jpkS.t) $("#jpk-t").value = jpkS.t; if (jpkS.w) $("#jpk-w").value = jpkS.w; if (jpkS.h) $("#jpk-h").value = jpkS.h; }
    if (!$("#jpk-pg").value) $("#jpk-pg").selectedIndex = 0;
    ["#jpk-pg", "#jpk-fill", "#jpk-t", "#jpk-w", "#jpk-h"].forEach(function (id) { $(id).addEventListener("input", jpkRun); $(id).addEventListener("change", jpkRun); });
    jpkRun();
  }

  /* ---------- 2027 GOAL PLANNER PRINTABLE (run 11) ---------- */
  if ($("#gpl-form") && $("#gpl-out")) {
    var GPL_IDS = ["name", "word", "theme", "g1", "y1", "s1", "d1", "g2", "y2", "s2", "d2", "g3", "y3", "s3", "d3", "g4", "y4", "s4", "d4", "h1", "h2", "h3"];
    var gV = function (k) { var el = $("#gpl-" + k); return el ? el.value.trim() : ""; };
    var gLn = function (label, v) { return '<div class="pjp-ln"><span>' + esc(label) + "</span><b>" + esc(v) + "</b></div>"; };
    var MO = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var gplPaper = "letter";
    var gplRun = function () {
      var h = [], th = gV("theme");
      h.push('<div class="gpl-pg"><p class="pjp-k">Purl &amp; Paper goal planner</p><p class="pjp-t">My 2027 goals' + (gV("name") ? " · " + esc(gV("name")) : "") + "</p>");
      h.push(gLn("Word of the year:", gV("word")));
      for (var i = 1; i <= 4; i++) {
        h.push('<div class="gpl-goal"><p class="pjp-h">Goal ' + i + "</p>" + gLn("Goal:", gV("g" + i)) + '<div class="pjp-2">' + gLn("Why:", gV("y" + i)) + gLn("First step:", gV("s" + i)) + "</div>" + gLn("Done by:", gV("d" + i)) +
          '<div class="gpl-q">' + ["Q1", "Q2", "Q3", "Q4"].map(function (q) { return '<div class="pjp-ln"><span>' + q + "</span><b></b></div>"; }).join("") + "</div></div>");
      }
      var tl = { craft: "Makes and skills for 2027", biz: "Shop and sales goals", read: "Books to read" }[th];
      if (tl) h.push('<p class="pjp-h">' + tl + '</p><div class="pjp-2">' + [1, 2, 3, 4, 5, 6].map(function () { return '<div class="pjp-ln"><span>☐</span><b></b></div>'; }).join("") + "</div>");
      h.push('<p class="pjp-h">Habits to track</p><table class="pjp-tb gpl-hb"><tr><th>Habit</th>' + MO.map(function (m) { return "<th>" + m.charAt(0) + "</th>"; }).join("") + "</tr>" +
        [1, 2, 3].map(function (n) { return "<tr><td>" + esc(gV("h" + n)) + "</td>" + MO.map(function () { return "<td></td>"; }).join("") + "</tr>"; }).join("") + "</table></div>");
      h.push('<div class="gpl-pg gpl-p2"><p class="pjp-k">Purl &amp; Paper goal planner</p><p class="pjp-t">2027 monthly check-in</p><p class="pjp-sm">At the end of each month: tick each goal you moved forward, write one win and choose next month\'s focus.</p><div class="gpl-mo">' +
        MO.map(function (m) {
          return '<div class="pjp-mo"><strong>' + m + '</strong><div class="gpl-tk">' + [1, 2, 3, 4].map(function (n) { var g = gV("g" + n); return '<span title="' + esc(g) + '">☐ ' + (g ? esc(g.length > 14 ? g.slice(0, 13) + "…" : g) : "Goal " + n) + "</span>"; }).join("") + "</div>" + gLn("Win:", "") + gLn("Next:", "") + "</div>";
        }).join("") + "</div><p class=\"pjp-sm\" style=\"margin-top:8px\">Free printable from purlandpaperco.com</p></div>");
      $("#gpl-out").innerHTML = h.join("");
      var sv = { paper: gplPaper }; GPL_IDS.forEach(function (k) { sv[k] = gV(k); }); store.set("pp-gpl", sv);
    };
    var gS = store.get("pp-gpl", null);
    if (gS) { GPL_IDS.forEach(function (k) { if (gS[k] != null && $("#gpl-" + k)) $("#gpl-" + k).value = gS[k]; }); if (gS.paper) { gplPaper = gS.paper; $$("#gpl-paper button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === gplPaper); }); } }
    if (!$("#gpl-theme").value) $("#gpl-theme").value = "none";
    GPL_IDS.forEach(function (k) { var el = $("#gpl-" + k); if (el) { el.addEventListener("input", gplRun); el.addEventListener("change", gplRun); } });
    seg($("#gpl-paper"), function (v) { gplPaper = v; gplRun(); });
    $("#gpl-clear").addEventListener("click", function () { GPL_IDS.forEach(function (k) { var el = $("#gpl-" + k); if (el) el.value = k === "theme" ? "none" : ""; }); gplRun(); });
    $("#gpl-print").addEventListener("click", function () {
      var st = $("#gpl-page"); if (!st) { st = document.createElement("style"); st.id = "gpl-page"; document.head.appendChild(st); }
      st.textContent = "@page { size: " + (gplPaper === "a4" ? "A4" : "letter") + "; margin: 0.45in; }";
      var bx = document.getElementById("gpl-printbox"); if (!bx) { bx = document.createElement("div"); bx.id = "gpl-printbox"; bx.className = "pjp-paper"; document.body.appendChild(bx); }
      bx.innerHTML = $("#gpl-out").innerHTML; document.body.classList.add("print-gpl"); window.print();
      setTimeout(function () { document.body.classList.remove("print-gpl"); }, 500);
    });
    gplRun();
  }

  /* ---------- BLOCKING HELPER (run 11) ---------- */
  if ($("#blk-f") && $("#blk-out")) {
    var BLK_F = {
      wool: { m: "Wet block", why: "Wool takes a new shape when it's wet and keeps it once it's dry.", dry: "24 to 48 hours", tip: "Don't rub or swish it in warm water: wool felts with heat plus friction." },
      sw: { m: "Wet block, gently", why: "Superwash wool relaxes and can grow a lot when wet.", dry: "24 to 48 hours", tip: "Squeeze out as much water as you can, push it back to size rather than stretching, and never hang it to dry." },
      acr: { m: "Steam block", why: "Acrylic doesn't reshape with water, but heat sets a new shape for good.", dry: "about 30 minutes, until cool", tip: "Keep the iron about 1 in above the yarn. Touching melts it flat and shiny, and the change can't be undone. Try your swatch first." },
      blend: { m: "Wet block (steam if it needs more)", why: "The wool part takes a shape from water; the acrylic part needs a little heat.", dry: "24 to 48 hours", tip: "Test on the swatch: if wet blocking doesn't hold, pin it out again and steam lightly from above." },
      cot: { m: "Wet block", why: "Cotton and plant fibres don't spring back, so water and pins settle the stitches well.", dry: "1 to 2 days (cotton holds water)", tip: "It won't stretch much, so pin to size rather than pulling. A steam iron held above is fine too." },
      moh: { m: "Spray or gentle wet block", why: "Fine and fluffy yarns need little help, and heavy handling can mat a mohair halo.", dry: "a few hours (spray) or a day (wet)", tip: "Skip hard steam: it flattens the halo. For silk lace, a full wet block opens the pattern." }
    };
    var BLK_I = {
      lace: "Pin out hard to open the lace: points first, every 1 in along the edges. Blocking wires along straight edges save a lot of pins.",
      sweater: "Block the pieces before seaming, flat, to the measurements on the pattern's schematic. Don't stretch the ribbing.",
      squares: "Draw your square size on the mat (or use a grid), pin each square at the corners and middles, and block the whole batch the same.",
      blanket: "Block it on a bed or a carpet with towels, in sections if it's big. Pin the edges straight with long pins.",
      scarf: "Pin the long edges straight with pins every 2 in, or run blocking wires along them.",
      hat: "Dry a hat over a balloon or a plate (for a beret) so it keeps its shape; socks and mittens on blockers or flat.",
      toy: "Toys usually don't need blocking. If a part is lumpy, steam it lightly from above and pat it into shape.",
      swatch: "Block it exactly as you'll block the finished piece, let it dry, unpin it and then measure your gauge."
    };
    var blkU = "in";
    var blkRun = function () {
      var u = segVal($("#blk-u")) || "in";
      if (u !== blkU) { ["#blk-w", "#blk-h"].forEach(function (id) { var v = parseFloat($(id).value); if (!isNaN(v)) $(id).value = +(u === "cm" ? v * 2.54 : v / 2.54).toFixed(1); }); blkU = u; }
      var f = $("#blk-f").value, it = $("#blk-i").value, F = BLK_F[f] || BLK_F.wool, o = [];
      var W = Math.max(1, parseFloat($("#blk-w").value) || 1), H = Math.max(1, parseFloat($("#blk-h").value) || 1);
      var m = F.m, dry = F.dry;
      if (it === "toy") { m = "Usually no blocking"; dry = "a few minutes"; }
      else if (it === "squares" && f !== "acr") { m = "Spray block (or wet block the batch)"; dry = "a few hours (spray)"; }
      else if (it === "lace" && f === "moh") { m = "Wet block and pin out"; dry = "about a day"; }
      o.push("<h3>Best method</h3><p class=\"blk-m\">" + esc(m) + "</p><p>" + esc(it === "toy" ? "Stuffed toys keep their shape from the stuffing." : F.why) + "</p>");
      o.push("<h3>For this project</h3><p>" + esc(BLK_I[it]) + "</p>");
      if (it !== "toy") {
        o.push("<p><strong>Watch out:</strong> " + esc(F.tip) + "</p><p>Drying time: " + esc(dry) + ".</p>");
        var tile = u === "cm" ? 30 : 12, cols = Math.ceil((W + (u === "cm" ? 5 : 2)) / tile), rows = Math.ceil((H + (u === "cm" ? 5 : 2)) / tile), tiles = cols * rows;
        var sp = it === "lace" ? (u === "cm" ? 2.5 : 1) : (u === "cm" ? 5 : 2), per = 2 * (W + H), pins = Math.ceil(per / sp);
        if (it === "sweater") pins = Math.ceil(pins / 2);
        o.push("<hr><h3>Mats and pins</h3><p class=\"blk-m\">" + tiles + " mat tile" + (tiles === 1 ? "" : "s") + "</p><p>" + cols + " across by " + rows + " down of " + (u === "cm" ? "30 cm" : "12 in") + " interlocking tiles, with a little room around the " + W + " x " + H + " " + u + " piece.</p>");
        o.push("<p>About <strong>" + pins + " pins</strong> (one every " + sp + " " + u + " round a " + (Math.round(per * 10) / 10) + " " + u + " edge)" + (it === "sweater" ? ", fewer for a sweater: pin the corners, hems and any curling edges" : "") + ".</p>");
        if (it === "lace" || it === "scarf") o.push("<p class=\"sub\">With blocking wires along the straight edges you need roughly half the pins.</p>");
        if (tiles > 16) o.push("<p class=\"sub\">That's a lot of tiles: a spare bed or a carpet with towels on it works just as well.</p>");
      }
      $("#blk-out").innerHTML = o.join("");
      store.set("pp-blk", { f: f, i: it, w: $("#blk-w").value, h: $("#blk-h").value, u: u });
    };
    var blkS = store.get("pp-blk", null);
    if (blkS) {
      if (blkS.f) $("#blk-f").value = blkS.f; if (blkS.i) $("#blk-i").value = blkS.i; if (blkS.w) $("#blk-w").value = blkS.w; if (blkS.h) $("#blk-h").value = blkS.h;
      if (blkS.u) { blkU = blkS.u; $$("#blk-u button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === blkS.u); }); }
    }
    if (!$("#blk-f").value) $("#blk-f").selectedIndex = 0; if (!$("#blk-i").value) $("#blk-i").selectedIndex = 0;
    ["#blk-f", "#blk-i", "#blk-w", "#blk-h"].forEach(function (id) { $(id).addEventListener("input", blkRun); $(id).addEventListener("change", blkRun); });
    seg($("#blk-u"), blkRun);
    blkRun();
  }

  /* ---------- MACRAME PROJECT FINDER (run 12) ---------- */
  if ($("#mkf-p") && $("#mkf-out")) {
    var MKK = { lark: "Lark's head", rlark: "Reverse lark's head", square: "Square knot", spiral: "Half knot spiral", hh: "Half hitch", dhh: "Double half hitch", diag: "Diagonal double half hitch", gather: "Gathering knot", over: "Overhand knot", berry: "Berry knot" };
    var MKP = {
      hanger: { k: ["gather", "square", "spiral", "over"], cord: "3-ply cotton rope, 4 to 5 mm", n: "4 cords folded over a wooden ring (8 ends), or 6 for a bigger pot", f: 8, fr: 10,
        steps: ["Fold the cords through a wooden ring and tie a gathering knot just below it.", "Split into 4 groups of 2 folded cords and tie a sinnet of square knots or a spiral in each: these are the arms.", "Drop down 3 in (8 cm) and tie alternating square knots between neighbouring groups to make the basket.", "Gather all the cords with a gathering knot under the basket and trim the tassel."] },
      wall: { k: ["rlark", "square", "dhh", "diag", "over"], cord: "Single-strand cotton, 4 to 5 mm", n: "12 to 20 cords for a 12 to 16 in (30 to 40 cm) dowel", f: 8, fr: 6,
        steps: ["Mount every cord on the dowel with a reverse lark's head.", "Tie a row of double half hitches straight across to make a neat top edge.", "Work rows of alternating square knots, then a V of diagonal double half hitches.", "Comb out the fringe and trim it straight, in a V or a curve."] },
      key: { k: ["lark", "square", "spiral", "gather"], cord: "Single-strand or braided cord, 3 mm", n: "2 to 4 cords folded onto the key ring", f: 9, fr: 3,
        steps: ["Mount the cords on the key ring with lark's head knots.", "Tie a short sinnet of square knots or a spiral.", "Finish with a gathering knot and comb out a short tassel."] },
      brace: { k: ["square", "spiral", "over"], cord: "Waxed cotton or nylon cord, 1 to 1.5 mm", n: "2 filler cords and 2 working cords (or 1 long one folded)", f: 0, fr: 0,
        steps: ["Tape the two fillers down with 6 in (15 cm) spare at the top for the ties.", "Tie the middle of the working cord under the fillers and work square knots down to the bracelet length.", "Seal the ends and tie a sliding square knot clasp over the crossed ties, or knot them with overhand knots."] },
      coaster: { k: ["lark", "square", "dhh", "over"], cord: "Single-strand cotton, 3 mm", n: "6 to 10 cords folded onto a mounting cord or wooden ring", f: 8, fr: 1.5,
        steps: ["Mount the cords with lark's head knots onto a short mounting cord.", "Tie alternating square knots or rows of double half hitches until the coaster is square.", "Tie the end off with a row of double half hitches and trim a short fringe."] },
      feather: { k: ["lark", "dhh", "over"], cord: "Single-strand cotton, 3 to 5 mm (soft, so it brushes out)", n: "1 folded spine cord and lots of short rib cords", f: 0, fr: 0,
        steps: ["Fold the spine cord and knot a loop at the top for hanging.", "Tie pairs of short rib cords to the spine with lark's head knots (one from each side), pushing each pair up tight.", "Brush the ribs out with a pet brush until fluffy, stiffen with fabric stiffener or hairspray, then trim to a feather shape."] },
      star: { k: ["lark", "square", "berry", "over"], cord: "Single-strand cotton, 3 mm", n: "1 cord folded onto each point of a star frame or a small ring", f: 8, fr: 2,
        steps: ["Mount the cords on a small ring or wire star with lark's head knots.", "Tie square knots or a berry knot along each arm.", "Finish with overhand knots, comb the fringe and add a loop for hanging."] },
      runner: { k: ["lark", "square", "dhh", "diag", "over"], cord: "Single-strand or 3-ply cotton, 4 to 5 mm", n: "20 to 30 cords folded onto a mounting cord for a 12 in (30 cm) wide runner", f: 8, fr: 6,
        steps: ["Mount the cords on a temporary mounting cord with lark's head knots.", "Work alternating square knots for the length, with rows of double half hitches for borders.", "Undo the mounting cord at the end so both ends have a fringe, and trim them to match."] }
    };
    var mkU = "in";
    var mkLen = function (v) { if (mkU === "cm") return Math.round(v) + " cm (" + (v / 100).toFixed(1) + " m)"; return (v >= 36 ? Math.round(v) + " in (" + (v / 12).toFixed(1) + " ft)" : (Math.round(v * 2) / 2) + " in"); };
    var mkfRun = function () {
      var p = $("#mkf-p").value, d = MKP[p], L = Math.min(400, Math.max(0.5, parseFloat($("#mkf-l").value) || 0)), cm = mkU === "cm", fr = cm ? d.fr * 2.5 : d.fr, o = [];
      o.push("<h3>Knots you need</h3><p>" + d.k.map(function (k) { return '<a href="#knot-' + k + '">' + esc(MKK[k]) + "</a>"; }).join(", ") + "</p>");
      o.push("<h3>Steps</h3><ol>" + d.steps.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ol>");
      o.push("<h3>Cord</h3><p>" + esc(d.cord) + ". " + esc(d.n) + ".</p>");
      if (p === "brace") {
        o.push('<h3>Cut lengths</h3><p class="jpk-big">' + mkLen(L * 5) + "</p><p>for the working cord (about 5 times the bracelet length), and " + mkLen(L + (cm ? 30 : 12)) + " for each filler cord, which leaves room for the ties.</p>");
      } else if (p === "feather") {
        o.push('<h3>Cut lengths</h3><p class="jpk-big">' + mkLen(L * 2 + (cm ? 20 : 8)) + "</p><p>for the spine cord (folded), and rib cords about " + mkLen(L + (cm ? 5 : 2)) + " each. You need roughly 2 pairs of ribs for every inch (2.5 cm) of feather.</p>");
      } else {
        o.push('<h3>Cut each cord</h3><p class="jpk-big">' + mkLen(L * d.f + 2 * fr) + "</p><p>That's about " + d.f + " times the finished length because each cord is folded in half, plus " + mkLen(fr) + " of fringe on each end.</p>");
      }
      o.push('<p class="sub">Estimates for beginner patterns. Tight knots and long sinnets use more, so cut a little extra. For a full cord count, try the <a href="' + esc($("#mkf-out").getAttribute("data-cc") || "macrame-cord-calculator.html") + '">macrame cord calculator</a>.</p>');
      $("#mkf-out").innerHTML = o.join("");
      store.set("pp-mkf", { p: p, l: $("#mkf-l").value, u: mkU });
    };
    var mkS = store.get("pp-mkf", null);
    if (mkS) { if (MKP[mkS.p]) $("#mkf-p").value = mkS.p; if (mkS.l) $("#mkf-l").value = mkS.l; if (mkS.u) { mkU = mkS.u; $$("#mkf-u button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === mkU); }); } }
    var MKD = { hanger: 30, wall: 24, key: 4, brace: 7, coaster: 4, feather: 8, star: 4, runner: 60 };
    $("#mkf-p").addEventListener("change", function () { var v = MKD[$("#mkf-p").value]; $("#mkf-l").value = mkU === "cm" ? Math.round(v * 2.54) : v; mkfRun(); });
    $("#mkf-l").addEventListener("input", mkfRun);
    seg($("#mkf-u"), function (v) { if (v !== mkU) { var x = parseFloat($("#mkf-l").value) || 0; $("#mkf-l").value = v === "cm" ? Math.round(x * 2.54) : Math.round(x / 2.54 * 2) / 2; mkU = v; } mkfRun(); });
    mkfRun();
  }

  /* ---------- JUNK JOURNAL SPREAD GENERATOR (run 12) ---------- */
  if ($("#jpi-go") && $("#jpi-out")) {
    var JPI = {
      base: { any: ["a page torn from an old book", "tea-stained copy paper", "a flattened brown paper bag", "an old map or atlas page", "sheet music", "a patterned scrapbook paper", "a coffee-dyed envelope opened flat", "plain card painted with a wash of watercolour"],
        winter: ["sheet music from an old carol book", "deep green or navy card", "a page from a Christmas catalogue"], new: ["a calendar page from last year", "graph paper", "a crisp white page with a gold edge"],
        nature: ["a tea-dyed page", "a seed catalogue page", "kraft card"], vintage: ["a ledger or accounts book page", "an old dictionary page", "a yellowed letter"], memory: ["a page from your own old diary", "a photocopied family document"],
        free: ["a cereal box, printed side in", "the inside of an envelope", "junk mail with a nice colour"] },
      focal: { any: ["a postcard", "a photo with a white border", "a big vintage label", "a cut-out from a magazine", "a playing card", "a pressed flower", "a quote typed on a strip", "a small drawing of your own"],
        winter: ["the front of an old Christmas card", "a paper snowflake", "a gift tag from last year"], new: ["your word of the year cut out in big letters", "a ticket to something you want to do this year"],
        nature: ["a pressed leaf", "a feather drawing", "a seed packet"], vintage: ["an old stamp blown up on the copier", "a cabinet card style portrait (your own family)", "a luggage label"], memory: ["a ticket stub", "a photo of a place you lived", "a child's drawing"],
        free: ["the front of a tea box", "a pretty bit of packaging", "a fortune from a fortune cookie"] },
      inter: ["a glue-on pocket with flaps", "a tag tucked behind the focal piece", "a fold-up page pocket", "a belly band with three cards", "a flap that opens to hidden journaling", "an envelope pocket", "a pull-tab under the photo", "a tiny folded mini book"],
      emb: ["two strips of washi tape crossed at a corner", "a line of running stitch round the edge", "a button tied with twine", "a rubber stamp in brown ink", "a scrap of lace", "a paper clip holding a ticket", "inked edges in brown", "a wax seal or round sticker", "a tea bag tag", "a ribbon from a gift"],
      words: { any: ["Today I noticed...", "Three small things that made me smile this week", "A place I want to go back to", "What I'm making right now", "Something I learned this month", "A letter to myself a year ago"],
        winter: ["My favourite winter smell", "The best gift I ever gave", "Five things on my cosy list"], new: ["My word for 2027 and why", "One thing I'll stop doing this year", "What I want to make in 2027"],
        nature: ["What the sky looked like today", "A walk I'd like to take again"], vintage: ["Who might have owned this paper?", "A story about an old photo"], memory: ["The first thing I remember about this day", "Who I was with and what we laughed about"],
        free: ["Where each scrap on this page came from", "What I almost threw away"] }
    };
    var JPL = [["base", "Background"], ["focal", "Focal piece"], ["inter", "Something interactive"], ["emb", "Embellishment"], ["words", "Words"]];
    var jpiPool = function (k, th) { var p = JPI[k]; if (Array.isArray(p)) return p; return th !== "any" && p[th] ? p[th].concat(p.any.slice(0, 3)) : p.any; };
    var jpiCur = store.get("pp-jpi", null);
    var jpiRender = function () {
      $("#jpi-out").innerHTML = "<h2>Your spread</h2><ol>" + JPL.map(function (l) {
        return '<li><button type="button" class="linkish" data-k="' + l[0] + '" title="Change this layer"><strong>' + esc(l[1]) + ":</strong> " + esc(jpiCur[l[0]]) + "</button></li>";
      }).join("") + '</ol><p class="sub">Tap a line to swap just that layer, or shuffle again for a whole new spread.</p>';
    };
    var jpiNew = function (k) {
      var th = $("#jpi-th").value, p = jpiPool(k, th), v = pick(p), g = 0;
      while (jpiCur && p.length > 1 && v === jpiCur[k] && g++ < 9) v = pick(p);
      return v;
    };
    var jpiShuffle = function () { var c = {}; jpiCur = jpiCur || {}; JPL.forEach(function (l) { c[l[0]] = jpiNew(l[0]); }); jpiCur = c; jpiCur.th = $("#jpi-th").value; store.set("pp-jpi", jpiCur); jpiRender(); };
    $("#jpi-go").addEventListener("click", jpiShuffle);
    $("#jpi-th").addEventListener("change", jpiShuffle);
    $("#jpi-out").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-k]"); if (!b) return;
      var k = b.getAttribute("data-k"); jpiCur[k] = jpiNew(k); store.set("pp-jpi", jpiCur); jpiRender();
      var nb = $('#jpi-out button[data-k="' + k + '"]'); if (nb) nb.focus();
    });
    if (jpiCur && jpiCur.base) { if (jpiCur.th) $("#jpi-th").value = jpiCur.th; jpiRender(); } else jpiShuffle();
  }

  /* ---------- SLIP STITCH JOINED ROUND WRITER (run 12) ---------- */
  if ($("#sls-st") && $("#sls-out")) {
    var SLS = { sc: { us: "sc", uk: "dc", ch: 1, cnt: false, nm: "single crochet" }, hdc: { us: "hdc", uk: "htr", ch: 2, cnt: false, nm: "half double crochet" },
                dc: { us: "dc", uk: "tr", ch: 3, cnt: true, nm: "double crochet" }, tr: { us: "tr", uk: "dtr", ch: 4, cnt: true, nm: "treble crochet" } };
    var slsT = "us";
    var slsRun = function () {
      var k = $("#sls-st").value, d = SLS[k], n = Math.min(400, Math.max(3, parseInt($("#sls-n").value, 10) || 12)), chs = $("#sls-ch").value, x = $("#sls-x").value;
      var a = d[slsT], ss = slsT === "uk" ? "ss" : "sl st", cnt = chs === "auto" ? d.cnt : chs === "yes", o = [];
      if (k === "sc" && cnt) o.push('<p class="sub">A ch 1 is too short to stand in for a single crochet, so almost no pattern counts it. Written below as asked anyway.</p>');
      var line = cnt
        ? "Ch " + d.ch + " (counts as first " + a + "), " + a + " in each st around, skipping the st at the base of the ch-" + d.ch + " (" + n + " " + a + ", counting the ch-" + d.ch + ")" 
        : "Ch " + d.ch + " (doesn't count as a st), " + a + " in same st as join and in each st around (" + n + " " + a + ")";
      var join = cnt ? ss + " to top of beginning ch-" + d.ch : ss + " to first " + a;
      o.push("<h2>Your round</h2><p class=\"sls-line\"><strong>" + esc(line + ", " + join + ".") + "</strong></p>");
      o.push("<h3>Where the join goes</h3><p>" + (cnt ? "Into the top chain of the ch " + d.ch + " you started with (the 3rd chain from the bottom for ch 3), under two loops." : "Into the top of the first " + d.nm + " you made after the chain, not into the chain itself.") + " The " + ss + " is not a stitch: don't work into it on the next round.</p>");
      if (x === "colour") o.push("<h3>Change colour at the join</h3><p>Insert the hook for the " + ss + ", drop the old colour, yarn over with the new colour and pull it through to make the " + ss + ". Start the next round's chain in the new colour. Leave 6 in (15 cm) tails to weave in.</p>");
      if (x === "last") o.push("<h3>Invisible join instead</h3><p>Skip the " + ss + ". Cut the yarn, leaving a 6 in (15 cm) tail, and pull it up through the last stitch. Thread it on a needle, go under both top loops of the " + (cnt ? "first real stitch after the chain" : "second stitch of the round") + ", then back down into the centre of the last stitch. Snug it to the size of one stitch and weave in the end.</p>");
      o.push("<h3>Check your count</h3><p>" + n + " stitches, plus the " + ss + " join (not counted). If you keep getting " + (n + 1) + ", you're working into the join" + (cnt ? " or into the stitch at the base of the chain" : "") + "; if you get " + (n - 1) + ", " + (cnt ? "you're not counting the ch-" + d.ch + " or you're skipping the last stitch before the join." : "you're skipping the first stitch.") + "</p>");
      $("#sls-out").innerHTML = o.join("");
      store.set("pp-sls", { k: k, n: n, c: chs, x: x, t: slsT });
    };
    var slsS = store.get("pp-sls", null);
    if (slsS) { if (SLS[slsS.k]) $("#sls-st").value = slsS.k; if (slsS.n) $("#sls-n").value = slsS.n; if (slsS.c) $("#sls-ch").value = slsS.c; if (slsS.x) $("#sls-x").value = slsS.x; if (slsS.t) { slsT = slsS.t; $$("#sls-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === slsT); }); } }
    ["#sls-st", "#sls-ch", "#sls-x"].forEach(function (s) { $(s).addEventListener("change", slsRun); });
    $("#sls-n").addEventListener("input", slsRun);
    seg($("#sls-t"), function (v) { slsT = v; slsRun(); });
    slsRun();
  }

  /* ---------- EMBROIDERY HOOP SIZE CALCULATOR (run 13) ---------- */
  if ($("#ehc-w") && $("#ehc-out")) {
    var EHC = [3, 4, 5, 6, 7, 8, 9, 10, 12, 14], ehcU = "in";
    var ehcF = function (v) { return ehcU === "cm" ? (Math.round(v * 2.54 * 2) / 2) + " cm" : (Math.round(v * 4) / 4) + " in"; };
    var ehcRun = function () {
      var k = ehcU === "cm" ? 2.54 : 1;
      var w = Math.max(0.2, parseFloat($("#ehc-w").value) || 4) / k, h = Math.max(0.2, parseFloat($("#ehc-h").value) || 4) / k;
      var rect = $("#ehc-sh").value === "rect", disp = $("#ehc-use").value === "display";
      var span = rect ? Math.sqrt(w * w + h * h) : Math.max(w, h), need = span + 1, hoop = null, o = [];
      for (var i = 0; i < EHC.length; i++) if (EHC[i] >= need - 0.001) { hoop = EHC[i]; break; }
      if (hoop) {
        o.push('<p class="sub">Hoop to buy</p><p class="big">' + hoop + ' in<small> hoop (' + (Math.round(hoop * 2.54 * 2) / 2) + ' cm)</small></p>');
        o.push("<p>Your design spans " + ehcF(span) + (rect ? " corner to corner" : " at its widest") + ", so it needs at least " + ehcF(need) + " inside the ring to keep a clear margin.</p>");
      } else {
        o.push('<p class="sub">Too big for one hoop</p><p style="font-size:1.6rem;font-weight:800">Scroll frame</p><p>Your design spans ' + ehcF(span) + ' and needs about ' + ehcF(need) + ': bigger than the 14 in hoops sold. Use a scroll, slate or clip frame, or stitch it in sections with a 7 in hoop that you move.</p>');
      }
      var fill = hoop ? Math.round(Math.max(w, h) / hoop * 100) : 0;
      if (hoop && disp) {
        o.push("<p><strong>As hoop art:</strong> the design fills about " + fill + "% of the hoop's width. " + (fill < 55 ? "That may look a little lost; a slightly bigger design, or a frame around the hoop, will balance it." : fill > 82 ? "It will look snug against the ring; that's fine for a bold motif." : "That's a nicely balanced look.") + "</p>");
      } else if (hoop && hoop > 9) {
        o.push("<p><strong>Comfort tip:</strong> a " + hoop + " in hoop is heavy to hold for long. If you'll frame the work, a 6 or 7 in hoop moved around the design is easier, or use a stand.</p>");
      }
      var base = hoop || Math.ceil(need), fab = disp ? base + 4 : Math.max(base + 4, Math.max(w, h) + 6);
      o.push("<h3>Fabric to cut</h3><p><strong>" + ehcF(fab) + " × " + ehcF(fab) + "</strong> (our rule of thumb: " + (disp ? "2 in past the hoop on every side, enough to gather or glue at the back" : "2 in past the hoop and 3 in round the design, enough to frame or sew it up") + ").</p>");
      if (hoop) {
        var sc = 150 / (hoop + 1), r = hoop / 2 * sc, dw = w * sc, dh = h * sc;
        var d = rect ? '<rect x="' + (100 - dw / 2).toFixed(1) + '" y="' + (90 - dh / 2).toFixed(1) + '" width="' + dw.toFixed(1) + '" height="' + dh.toFixed(1) + '" rx="3" fill="none" stroke="#b8326a" stroke-width="2" stroke-dasharray="5 3"/>'
                     : '<ellipse cx="100" cy="90" rx="' + (dw / 2).toFixed(1) + '" ry="' + (dh / 2).toFixed(1) + '" fill="none" stroke="#b8326a" stroke-width="2" stroke-dasharray="5 3"/>';
        o.push('<svg viewBox="0 0 200 180" role="img" aria-label="Your design drawn to scale inside a ' + hoop + ' in hoop" style="max-width:260px;display:block;margin:10px auto 0"><circle cx="100" cy="90" r="' + r.toFixed(1) + '" fill="#fbf8f1" stroke="#c99a5b" stroke-width="6"/>' + d + '</svg><p class="sub" style="text-align:center">To scale: design (dashed) in a ' + hoop + ' in hoop.</p>');
      }
      $("#ehc-out").innerHTML = o.join("");
      store.set("pp-ehc", { w: $("#ehc-w").value, h: $("#ehc-h").value, s: $("#ehc-sh").value, u: $("#ehc-use").value, n: ehcU });
    };
    var ehcS = store.get("pp-ehc", null);
    if (ehcS) { if (ehcS.w) $("#ehc-w").value = ehcS.w; if (ehcS.h) $("#ehc-h").value = ehcS.h; if (ehcS.s) $("#ehc-sh").value = ehcS.s; if (ehcS.u) $("#ehc-use").value = ehcS.u; if (ehcS.n === "cm") { ehcU = "cm"; $$("#ehc-u button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "cm" ? "true" : "false"); }); } }
    ["#ehc-sh", "#ehc-use"].forEach(function (s) { $(s).addEventListener("change", ehcRun); });
    ["#ehc-w", "#ehc-h"].forEach(function (s) { $(s).addEventListener("input", ehcRun); });
    seg($("#ehc-u"), function (v) {
      if (v === ehcU) return; var f = v === "cm" ? 2.54 : 1 / 2.54;
      ["#ehc-w", "#ehc-h"].forEach(function (s) { var x = parseFloat($(s).value); if (x) $(s).value = Math.round(x * f * 4) / 4; });
      ehcU = v; ehcRun();
    });
    ehcRun();
  }

  /* ---------- PUNCH NEEDLE MATCHER (run 13) ---------- */
  if ($("#pnm-y") && $("#pnm-out")) {
    var PNM = {
      floss: { n: "A small embroidery punch needle", why: "Floss and perle cotton need a fine, thin needle; rug and #10 needles are far too big.", f: "Tightly woven cotton, linen or weaver's cloth", ok: { rug: "Floss is too fine for a rug that gets walked on: switch to rug yarn and a regular needle." } },
      fine: { n: "A fine punch needle (like an Oxford #10 Fine), on a short setting", why: "Fingering, sport and DK run through the fine needle; very thin yarn can be held double so it fills.", f: "Weaver's cloth", ok: { rug: "Thin yarn makes a delicate pile; for a rug, hold it double or use rug yarn." } },
      worsted: { n: "A fine punch needle (like an Oxford #10 Fine)", why: "Worsted and aran are the fine needle's sweet spot. Or hold two strands together in a regular needle.", f: "Weaver's cloth (or monk's cloth if you use a regular needle)", ok: {} },
      bulky: { n: "A regular rug punch needle (like an Oxford #10 Regular)", why: "Chunky and rug yarn need the wider regular needle; forcing them through a fine needle snags.", f: "Monk's cloth", ok: {} },
      strip: { n: "A regular rug punch needle (like an Oxford #10 Regular)", why: "Cut strips about 1/4 in (6 mm) wide; wider strips jam the needle.", f: "Monk's cloth", ok: { hoop: "Fabric strips are bulky for small hoop art; save them for cushions and rugs." } }
    };
    var PNL = { flat: "the shortest setting, about 1/4 in (6 mm) loops or less, or use the flat side as the front", mid: "about 1/4 to 3/8 in (6 to 10 mm) loops", plush: "a tall setting, up to about 1/2 in (12 mm) loops, which uses noticeably more yarn" };
    var pnmRun = function () {
      var y = PNM[$("#pnm-y").value], p = $("#pnm-p").value, f = $("#pnm-f").value, o = [];
      o.push('<p class="sub">Needle</p><p style="font-size:1.3rem;font-weight:700;line-height:1.3">' + esc(y.n) + "</p><p>" + esc(y.why) + "</p>");
      o.push("<h3>Fabric and frame</h3><p><strong>" + esc(y.f) + "</strong>, stretched drum-tight in " + (p === "hoop" ? "a no-slip hoop (or a plain hoop with the inner ring wrapped in tape)." : "a gripper-strip frame; a hoop tends to let bigger pieces creep.") + " Leave at least 2 in (5 cm) of fabric beyond the design all round.</p>");
      o.push("<h3>Loop height</h3><p>Use " + esc(PNL[f]) + "." + (p === "rug" && f === "plush" ? " For a rug that's walked on, shorter, denser loops wear better and shed less dirt into the pile." : "") + "</p>");
      if (y.ok[p]) o.push('<p class="sub"><strong>Heads-up:</strong> ' + esc(y.ok[p]) + "</p>");
      o.push("<h3>Finish</h3><p>" + (p === "hoop" ? "Trim the fabric 1 in past the ring and glue or gather it behind the hoop." : p === "cushion" ? "Fold the margin to the back, stitch it down and back with felt or a cushion back." : "Fold under a 2 in margin, whip stitch or bind it, and add a non-slip backing.") + "</p>");
      $("#pnm-out").innerHTML = o.join("");
      store.set("pp-pnm", { y: $("#pnm-y").value, p: p, f: f });
    };
    var pnmS = store.get("pp-pnm", null);
    if (pnmS) { if (PNM[pnmS.y]) $("#pnm-y").value = pnmS.y; if (pnmS.p) $("#pnm-p").value = pnmS.p; if (pnmS.f) $("#pnm-f").value = pnmS.f; }
    ["#pnm-y", "#pnm-p", "#pnm-f"].forEach(function (s) { $(s).addEventListener("change", pnmRun); });
    pnmRun();
  }

  /* ---------- BEGINNER SCARF PATTERN WRITER (run 13) ---------- */
  if ($("#ksw-y") && $("#ksw-out")) {
    // Craft Yarn Council knit gauge ranges (sts per 4 in) with a mid value, and a needle within the CYC range.
    var KSW = { "3": { g: 22.5, r: "21–24", nd: "4.5 mm (US 7)", nm: "DK" }, "4": { g: 18, r: "16–20", nd: "5 mm (US 8)", nm: "worsted" },
                "5": { g: 13.5, r: "12–15", nd: "6.5 mm (US 10½)", nm: "chunky" }, "6": { g: 9, r: "7–11", nd: "10 mm (US 15)", nm: "super bulky" } };
    var kswRun = function () {
      var y = KSW[$("#ksw-y").value], st = $("#ksw-s").value;
      var w = Math.min(24, Math.max(2, parseFloat($("#ksw-w").value) || 7)), l = Math.min(120, Math.max(10, parseFloat($("#ksw-l").value) || 65));
      var mine = parseFloat($("#ksw-g").value), g = mine >= 4 && mine <= 40 ? mine : y.g;
      var n = w * g / 4 * (st === "rib" ? 1.25 : 1);
      if (st === "garter") n = Math.round(n);
      else if (st === "seed") { n = Math.round(n); if (n % 2 === 0) n += 1; }
      else { n = Math.round((n - 2) / 4) * 4 + 2; }
      n = Math.max(st === "rib" ? 10 : 9, n);
      var rows = { garter: ["<strong>Every row:</strong> knit to the end."],
                   seed: ["<strong>Every row:</strong> *k1, p1; repeat from * to the last stitch, k1."],
                   rib: ["<strong>Row 1:</strong> *k2, p2; repeat from * to the last 2 stitches, k2.", "<strong>Row 2:</strong> *p2, k2; repeat from * to the last 2 stitches, p2."] }[st];
      var o = [];
      o.push('<p class="sub">Cast on</p><p class="big">' + n + "<small> stitches</small></p><p>" + y.nd + " needles, " + y.nm + " yarn, " + (mine ? "your gauge of " + g + " sts per 4 in" : "about " + y.r + " sts per 4 in (the Craft Yarn Council range)") + ".</p>");
      o.push("<h3>Your pattern</h3><ol><li>Make a slip knot and cast on " + n + " stitches (long-tail cast on is ideal).</li>");
      rows.forEach(function (r) { o.push("<li>" + r + "</li>"); });
      o.push("<li>Repeat " + (rows.length > 1 ? "rows 1 and 2" : "this row") + " until the scarf measures " + l + " in (" + Math.round(l * 2.54) + " cm), or leave about 1 yard of yarn for the bind off.</li>");
      o.push("<li>Bind off " + (st === "garter" ? "knitwise" : "in pattern (knit the knits, purl the purls)") + ". Weave in the ends.</li></ol>");
      o.push('<p class="sub">Width: about ' + w + " in" + (st === "rib" ? " relaxed (ribbing pulls in, so we added stitches)" : "") + ". Knit 4 in, then measure: if it's wider than planned, start again with fewer stitches. " + (st !== "garter" ? "Tip: knit the first and last 3 stitches of every row for a garter border." : "Tip: slip the first stitch of each row purlwise for a neat edge.") + "</p>");
      o.push('<p class="sub">How much yarn? Pick the same size in the <a href="' + ($("#ksw-out").getAttribute("data-scarf") || "scarf-size-chart") + '">scarf size calculator</a>.</p>');
      $("#ksw-out").innerHTML = o.join("");
      store.set("pp-ksw", { y: $("#ksw-y").value, s: st, w: w, l: l, g: $("#ksw-g").value });
    };
    var kswS = store.get("pp-ksw", null);
    if (kswS) { if (KSW[kswS.y]) $("#ksw-y").value = kswS.y; if (kswS.s) $("#ksw-s").value = kswS.s; if (kswS.w) $("#ksw-w").value = kswS.w; if (kswS.l) $("#ksw-l").value = kswS.l; if (kswS.g) $("#ksw-g").value = kswS.g; }
    ["#ksw-y", "#ksw-s"].forEach(function (s) { $(s).addEventListener("change", kswRun); });
    ["#ksw-w", "#ksw-l", "#ksw-g"].forEach(function (s) { $(s).addEventListener("input", kswRun); });
    kswRun();
  }

  /* ---------- BEGINNER CROCHET SCARF PATTERN WRITER (run 14) ---------- */
  if ($("#csw-y") && $("#csw-out")) {
    // Craft Yarn Council crochet gauge (sc per 4 in) mid values and a hook in the CYC range. Taller stitches spread a little (our estimate).
    var CSW = { "3": { g: 14, r: "12–17", hk: "5 mm (H-8)", nm: "DK" }, "4": { g: 12, r: "11–14", hk: "6 mm (J-10)", nm: "worsted" },
                "5": { g: 9.5, r: "8–11", hk: "8 mm (L-11)", nm: "chunky" }, "6": { g: 8, r: "7–9", hk: "10 mm (N/P-15)", nm: "super bulky" } };
    var cswT = "us";
    var cswRun = function () {
      var y = CSW[$("#csw-y").value], st = $("#csw-s").value, uk = cswT === "uk";
      var w = Math.min(24, Math.max(2, parseFloat($("#csw-w").value) || 7)), l = Math.min(120, Math.max(10, parseFloat($("#csw-l").value) || 65));
      var mine = parseFloat($("#csw-g").value), g = mine >= 4 && mine <= 40 ? mine : y.g;
      var N = { sc: uk ? "dc" : "sc", hdc: uk ? "htr" : "hdc", dc: uk ? "tr" : "dc" };
      var NL = { sc: uk ? "double crochet (dc)" : "single crochet (sc)", hdc: uk ? "half treble (htr)" : "half double crochet (hdc)", dc: uk ? "treble (tr)" : "double crochet (dc)" };
      var f = { sc: 1, hdc: 0.95, dc: 0.92, moss: 1 }[st], n = Math.max(6, Math.round(w * g / 4 * f)), ch, rows, first;
      if (st === "sc") { ch = n + 1; first = "Row 1: " + N.sc + " in the 2nd ch from the hook and in each ch across (" + n + " sts)."; rows = ["Every row after: ch 1 (doesn't count as a stitch), turn, " + N.sc + " in each st across (" + n + " sts)."]; }
      else if (st === "hdc") { ch = n + 2; first = "Row 1: " + N.hdc + " in the 3rd ch from the hook and in each ch across (" + n + " sts)."; rows = ["Every row after: ch 2 (doesn't count as a stitch), turn, " + N.hdc + " in each st across (" + n + " sts)."]; }
      else if (st === "dc") { ch = n + 2; first = "Row 1: " + N.dc + " in the 4th ch from the hook (the skipped 3 ch count as the first stitch) and in each ch across (" + n + " sts)."; rows = ["Every row after: ch 3 (counts as a " + N.dc + "), turn, skip the first st, " + N.dc + " in each st across, and work the last " + N.dc + " into the top of the turning chain (" + n + " sts)."]; }
      else { ch = Math.max(8, Math.round((n + 2) / 2) * 2); first = "Row 1: " + N.sc + " in the 4th ch from the hook, *ch 1, skip 1 ch, " + N.sc + " in the next ch; repeat from * to the end."; rows = ["Every row after: ch 2, turn, " + N.sc + " in the first ch-1 space, *ch 1, " + N.sc + " in the next ch-1 space; repeat from * across, working the last " + N.sc + " into the turning-chain space."]; }
      var o = [];
      o.push('<p class="sub">Chain</p><p class="big">' + ch + "<small> chains to start</small></p><p>" + y.hk + " hook, " + y.nm + " yarn, " + (mine ? "your gauge of " + g + " sts per 4 in" : "about " + y.r + " " + N.sc + " per 4 in (the Craft Yarn Council range)") + ". Terms: " + (uk ? "UK" : "US") + ".</p>");
      o.push("<h3>Your pattern</h3><ol><li>Make a slip knot and chain " + ch + " loosely.</li><li>" + first + "</li>");
      rows.forEach(function (r) { o.push("<li>" + r + "</li>"); });
      o.push("<li>Repeat until the scarf measures " + l + " in (" + Math.round(l * 2.54) + " cm).</li><li>Fasten off: cut the yarn, leaving a 6 in tail, and pull it through the loop. Weave in both ends.</li></ol>");
      o.push('<p class="sub">Stitch: ' + (st === "moss" ? "moss (linen) stitch, worked in " + NL.sc : NL[st]) + ". Width: about " + w + " in. Work 4 in, then measure: if it's wider than planned, start again with fewer chains" + (st === "moss" ? " (keep an even number)" : "") + ". Stitch counts for taller stitches are our estimate, so a quick swatch helps.</p>");
      o.push('<p class="sub">How much yarn? Pick the same size in the <a href="' + ($("#csw-out").getAttribute("data-scarf") || "scarf-size-chart") + '">scarf size calculator</a> and choose crochet.</p>');
      $("#csw-out").innerHTML = o.join("");
      store.set("pp-csw", { y: $("#csw-y").value, s: st, w: w, l: l, g: $("#csw-g").value, t: cswT });
    };
    var cswS = store.get("pp-csw", null);
    if (cswS) { if (CSW[cswS.y]) $("#csw-y").value = cswS.y; if (cswS.s) $("#csw-s").value = cswS.s; if (cswS.w) $("#csw-w").value = cswS.w; if (cswS.l) $("#csw-l").value = cswS.l; if (cswS.g) $("#csw-g").value = cswS.g;
      if (cswS.t === "uk") { cswT = "uk"; $$("#csw-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); } }
    ["#csw-y", "#csw-s"].forEach(function (s) { $(s).addEventListener("change", cswRun); });
    ["#csw-w", "#csw-l", "#csw-g"].forEach(function (s) { $(s).addEventListener("input", cswRun); });
    seg($("#csw-t"), function (v) { cswT = v; cswRun(); });
    cswRun();
  }

  /* ---------- HAND SEWING STITCH CHOOSER (run 14) ---------- */
  if ($("#hss-job") && $("#hss-out")) {
    var HSN = { running: "Running stitch", baste: "Basting stitch", back: "Backstitch", whip: "Whip stitch", ladder: "Ladder stitch", slip: "Slip stitch (blind hem)", blanket: "Blanket stitch", "catch": "Catch stitch" };
    var HSJ = { seam: ["back", "Backstitch along the old seam line, starting and ending about 1/2 in (12 mm) past the split so the new stitches overlap the sound ones."],
                hem: ["slip", "Fold and press the hem, pin it, then slip stitch. Pick up only one or two threads of the main fabric so the front stays clean."],
                stretch: ["catch", "Catch stitch keeps a little give, so the thread doesn't snap when the fabric stretches. Keep the stitches loose."],
                gap: ["ladder", "Fold the seam allowances in, ladder stitch across, and pull the thread every few stitches to close the gap. Knot inside and bury the tail in the stuffing."],
                felt: ["whip", "Whip stitch close to the edge for a quick join; blanket stitch if you want the stitches to show as a border."],
                edge: ["blanket", "Space the stitches evenly with a ruler or by eye using the weave; keep each loop the same depth from the edge."],
                hole: ["whip", "For a small hole or tear, whip stitch the edges together from the wrong side with tiny stitches, or back a bigger hole with a patch and whip stitch round it."],
                gather: ["running", "Sew two parallel rows of running stitch inside the seam allowance with long tails, then pull the tails to gather evenly."],
                hold: ["baste", "Baste with long stitches in a contrasting colour, then remove them after the real seam is done."] };
    var HSF = { light: ["sharps size 9 to 10", "fine polyester or silk thread", "1/16 to 1/8 in (2 to 3 mm)"], medium: ["sharps size 7 to 9", "all-purpose polyester or cotton thread", "about 1/8 in (3 mm)"],
                heavy: ["sharps 5 to 6 or a heavy-duty needle (and a thimble)", "heavy-duty or upholstery thread", "1/8 to 1/4 in (3 to 6 mm)"], knit: ["a ballpoint hand needle", "all-purpose polyester thread", "about 1/8 in, kept loose"],
                felt: ["a sharps or embroidery needle", "embroidery floss (2 to 3 strands) or all-purpose thread", "about 1/8 in, close to the edge"] };
    var hssRun = function () {
      var j = HSJ[$("#hss-job").value], fb = $("#hss-fab").value, fv = HSF[fb], k = j[0];
      if ($("#hss-job").value === "hem" && fb === "knit") k = "catch";
      var dbl = ["seam", "hole"].indexOf($("#hss-job").value) >= 0 || fb === "heavy";
      var len = k === "baste" ? "1/4 to 1/2 in (6 to 12 mm)" : fv[2];
      var o = ['<p class="sub">Use</p><p class="big">' + HSN[k] + "</p>"];
      o.push("<p>" + (k !== j[0] ? "On stretchy fabric, catch stitch beats slip stitch for a hem. " + HSJ.stretch[1] : j[1]) + "</p>");
      o.push('<table class="mt"><tbody><tr><td>Needle</td><td>' + fv[0] + "</td></tr><tr><td>Thread</td><td>" + fv[1] + ", " + (dbl ? "doubled for strength" : "single") + ", about 18 in (45 cm)</td></tr><tr><td>Stitch length</td><td>" + len + " (typical)</td></tr></tbody></table>");
      o.push('<p class="sub"><a href="#hs-' + k + '">See how to sew ' + HSN[k].toLowerCase() + " ↓</a></p>");
      $("#hss-out").innerHTML = o.join("");
      store.set("pp-hss", { j: $("#hss-job").value, f: fb });
    };
    var hssS = store.get("pp-hss", null);
    if (hssS) { if (HSJ[hssS.j]) $("#hss-job").value = hssS.j; if (HSF[hssS.f]) $("#hss-fab").value = hssS.f; }
    ["#hss-job", "#hss-fab"].forEach(function (s) { $(s).addEventListener("change", hssRun); });
    hssRun();
  }

  /* ---------- CABLE PATTERN AND CHART WRITER (run 15) ---------- */
  if ($("#ckw-w") && $("#ckw-out")) {
    var ckwF = "flat";
    var ckwRun = function () {
      var w = parseInt($("#ckw-w").value, 10), d = $("#ckw-d").value, R = parseInt($("#ckw-r").value, 10);
      var p = Math.min(6, Math.max(1, parseInt($("#ckw-p").value, 10) || 2)), n = Math.min(8, Math.max(1, parseInt($("#ckw-n").value, 10) || 1));
      var rnd = ckwF === "round", h = w / 2, tot = rnd ? n * (w + p) : p + n * (w + p);
      var rows = d === "A" ? R * 2 : R;
      var cx = function (r) { return d === "A" ? (r === 1 ? "F" : "B") : d; };
      var plainRS = rnd ? "*p" + p + ", k" + w + "; repeat from * to the end" : "p" + p + ", *k" + w + ", p" + p + "; repeat from * to the end";
      var crossRS = function (c) { return rnd ? "*p" + p + ", C" + w + c + "; repeat from * to the end" : "p" + p + ", *C" + w + c + ", p" + p + "; repeat from * to the end"; };
      var plainWS = "k" + p + ", *p" + w + ", k" + p + "; repeat from * to the end";
      var o = ['<p class="sub">Cast on</p><p class="big">' + tot + "<small> stitches</small></p><p>" + n + " cable" + (n > 1 ? "s" : "") + " of " + w + " stitches with " + p + " purl stitches " + (rnd ? "between each (joined in the round)" : "between and at each edge") + ". Add any edge or rib stitches your project needs.</p>"];
      o.push("<h3>Your pattern" + (rnd ? " (rounds)" : " (rows)") + "</h3><ol>");
      for (var r = 1; r <= rows; r++) {
        var lbl = rnd ? "Round " + r : "Row " + r + (r % 2 ? " (RS)" : " (WS)");
        var isX = d === "A" ? (r === 1 || r === R + 1) : r === 1;
        var txt;
        if (!rnd && r % 2 === 0) txt = plainWS; else txt = isX ? crossRS(d === "A" ? (r === 1 ? "F" : "B") : d) : plainRS;
        o.push("<li><strong>" + lbl + ":</strong> " + txt + ".</li>");
      }
      o.push("</ol><p>Repeat " + (rnd ? "rounds" : "rows") + " 1 to " + rows + ".</p>");
      var cdesc = function (c) { return "<strong>C" + w + c + "</strong>: slip " + h + " sts to a cable needle and hold in " + (c === "F" ? "front" : "back") + ", k" + h + ", then k" + h + " from the cable needle (leans " + (c === "F" ? "left" : "right") + ")."; };
      o.push('<p class="sub">' + (d === "A" ? cdesc("F") + " " + cdesc("B") : cdesc(d)) + "</p>");
      // chart: one repeat of p + cable + p (flat) or cable + p (round)
      var cols = rnd ? w + p : p + w + p, cw = Math.min(26, Math.floor(300 / cols)), ch = 18, W = cols * cw, H = rows * ch, svg = [];
      svg.push('<svg viewBox="-28 -4 ' + (W + 36) + " " + (H + 24) + '" role="img" aria-label="Cable chart, ' + rows + ' rows" style="max-width:100%;height:auto">');
      var c0 = rnd ? 0 : p;
      for (var y = 0; y < rows; y++) {
        var rr = rows - y, isX2 = d === "A" ? (rr === 1 || rr === R + 1) : rr === 1, c2 = d === "A" ? (rr === 1 ? "F" : "B") : d;
        for (var x = 0; x < cols; x++) {
          var isP = x < c0 || x >= c0 + w;
          svg.push('<rect x="' + x * cw + '" y="' + y * ch + '" width="' + cw + '" height="' + ch + '" fill="' + (isP ? "#efe6d2" : "#fbfcfa") + '" stroke="#1f2a44" stroke-width=".6"/>');
          if (isP) svg.push('<circle cx="' + (x * cw + cw / 2) + '" cy="' + (y * ch + ch / 2) + '" r="2.2" fill="#1f2a44"/>');
        }
        if (isX2) {
          var x1 = c0 * cw, x2 = (c0 + w) * cw, yt = y * ch + 2, yb = y * ch + ch - 2, mid = (x1 + x2) / 2;
          svg.push('<rect x="' + x1 + '" y="' + y * ch + '" width="' + (x2 - x1) + '" height="' + ch + '" fill="#f4d9e4" stroke="#1f2a44" stroke-width=".8"/>');
          if (c2 === "F") svg.push('<path d="M' + (x1 + 3) + " " + yb + " L" + (mid - 1) + " " + yt + " M" + (mid + 1) + " " + yb + " L" + (x2 - 3) + " " + yt + '" stroke="#b8326a" stroke-width="2.4" fill="none"/><path d="M' + (mid + 1) + " " + yt + " L" + (x2 - 3) + " " + yb + '" stroke="#b8326a" stroke-width="1" fill="none"/>');
          else svg.push('<path d="M' + (x1 + 3) + " " + yt + " L" + (mid - 1) + " " + yb + '" stroke="#b8326a" stroke-width="1" fill="none"/><path d="M' + (mid + 1) + " " + yt + " L" + (x2 - 3) + " " + yb + " M" + (x1 + 3) + " " + yb + " L" + (mid - 1) + " " + yt + '" stroke="#b8326a" stroke-width="2.4" fill="none"/>');
        }
        svg.push('<text x="' + (rnd || rr % 2 ? W + 4 : -4) + '" y="' + (y * ch + 13) + '" font-size="10" font-family="Inter,sans-serif" fill="#1f2a44" text-anchor="' + (rnd || rr % 2 ? "start" : "end") + '">' + rr + "</text>");
      }
      svg.push("</svg>");
      o.push("<h3>Chart (one repeat)</h3>" + svg.join("") + '<p class="sub">Blank = knit on the RS, dot = purl on the RS, pink = the cable cross. Start at the bottom; ' + (rnd ? "read every round right to left." : "RS rows (numbers on the right) right to left, WS rows left to right, knitting the purls and purling the knits.") + " Allow a little extra yarn: cables use more than plain knitting (see below).</p>");
      $("#ckw-out").innerHTML = o.join("");
      store.set("pp-ckw", { w: $("#ckw-w").value, d: d, r: $("#ckw-r").value, p: p, n: n, f: ckwF });
    };
    var ckwS = store.get("pp-ckw", null);
    if (ckwS) { ["w", "d", "r"].forEach(function (k) { if (ckwS[k] && $("#ckw-" + k).querySelector('option[value="' + ckwS[k] + '"]')) $("#ckw-" + k).value = ckwS[k]; });
      if (ckwS.p) $("#ckw-p").value = ckwS.p; if (ckwS.n) $("#ckw-n").value = ckwS.n;
      if (ckwS.f === "round") { ckwF = "round"; $$("#ckw-f button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "round" ? "true" : "false"); }); } }
    ["#ckw-w", "#ckw-d", "#ckw-r"].forEach(function (s) { $(s).addEventListener("change", ckwRun); });
    ["#ckw-p", "#ckw-n"].forEach(function (s) { $(s).addEventListener("input", ckwRun); });
    seg($("#ckw-f"), function (v) { ckwF = v; ckwRun(); });
    ckwRun();
  }

  /* ---------- CROCHET SHEEP: ROUND TRACKER + YARN HELPER (run 15) ---------- */
  if ($("#shp-y") && $("#shp-out")) {
    // Stitch totals of our pattern: white 558 (body 504 + tuft 54), dark 440 (head 216 + ears 56 + legs 168). Yarn per tight sc and sizes are our estimates.
    var SHPY = { dk: { per: 1.25, len: 3.3, hk: "3 mm (C-2 or D-3)", eye: "6 to 8 mm" }, w: { per: 1.6, len: 4, hk: "3.5 mm (E-4)", eye: "8 mm" },
                 ch: { per: 2.3, len: 5.5, hk: "5 mm (H-8)", eye: "10 to 12 mm" }, sb: { per: 3.4, len: 8.5, hk: "6 mm (J-10)", eye: "12 to 15 mm" } };
    var shpBoxes = $$("input[data-shp]"), shpN = shpBoxes.length;
    var shpDone = store.get("pp-shp-done", []) || [];
    shpBoxes.forEach(function (b) { if (shpDone.indexOf(b.getAttribute("data-shp")) >= 0) b.checked = true; });
    var shpRun = function () {
      var y = SHPY[$("#shp-y").value], wy = Math.ceil(558 * y.per / 36 * 1.1 + 5), dy = Math.ceil(440 * y.per / 36 * 1.1 + 5);
      var done = shpBoxes.filter(function (b) { return b.checked; }).length;
      var o = ['<p class="sub">Your sheep</p><p class="big">' + y.len + '<small> in long (about ' + Math.round(y.len * 2.54) + " cm)</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>White</td><td>about ' + wy + " yd (" + Math.round(wy * 0.9144) + ' m)</td></tr><tr><td>Dark grey</td><td>about ' + dy + " yd (" + Math.round(dy * 0.9144) + " m)</td></tr><tr><td>Hook</td><td>" + y.hk + "</td></tr><tr><td>Safety eyes</td><td>" + y.eye + " (or embroider)</td></tr></tbody></table>");
      o.push('<p class="sub">Estimates from the stitch count of this pattern, with 10% spare and tails for sewing. Tension changes them.</p>');
      o.push("<p><strong>" + done + " of " + shpN + "</strong> rounds ticked" + (done === shpN ? ": all done, time to sew it together!" : ".") + ' <button type="button" class="btn ghost" id="shp-reset">Clear ticks</button></p>');
      $("#shp-out").innerHTML = o.join("");
      $("#shp-reset").addEventListener("click", function () { shpBoxes.forEach(function (b) { b.checked = false; }); store.set("pp-shp-done", []); shpRun(); });
      store.set("pp-shp", $("#shp-y").value);
    };
    var shpS = store.get("pp-shp", null); if (shpS && SHPY[shpS]) $("#shp-y").value = shpS;
    shpBoxes.forEach(function (b) { b.addEventListener("change", function () {
      store.set("pp-shp-done", shpBoxes.filter(function (x) { return x.checked; }).map(function (x) { return x.getAttribute("data-shp"); })); shpRun(); }); });
    $("#shp-y").addEventListener("change", shpRun);
    shpRun();
  }

  /* ---------- HAT PATTERN WRITERS + POM POM HELPER (run 16) ---------- */
  // Hat sizes: same table as /hat-size-chart (CYC head ranges; hat about 11-12% smaller than the head). Fitted beanie lengths are typical figures.
  var HATS = [[12, 10.5, 4.5], [14, 12.5, 5.5], [17, 15, 6.5], [18.5, 16.5, 7], [20, 17.5, 7.5], [21, 18.5, 8], [22, 19.5, 8.5], [23.5, 20.5, 9]];
  var hatSize = function (zSel, mSel) {
    var z = $(zSel).value, h;
    if (z === "m") { var m = Math.min(26, Math.max(10, parseFloat($(mSel).value) || 22)); h = [m, Math.round(m * 0.886 * 10) / 10, Math.round(m * 0.386 * 4) / 4]; }
    else h = HATS[+z] || HATS[6];
    $(mSel).closest(".field").style.opacity = z === "m" ? "1" : ".55";
    return { head: h[0], c: h[1], len: h[2] };
  };
  var r10 = function (n) { return Math.max(10, Math.round(n / 10) * 10); };
  var YF = { "3": 1.2, "4": 1, "5": 0.7, "6": 0.5 };
  if ($("#cht-z") && $("#cht-out")) {
    // CYC crochet gauge (sc per 4 in) mid values and hooks; taller stitch widths and round heights are our estimates.
    var CHY = { "3": { g: 14, hk: "4.5 to 5 mm (7 to H-8)", nm: "DK" }, "4": { g: 12, hk: "5.5 to 6 mm (I-9 to J-10)", nm: "worsted" },
                "5": { g: 9.5, hk: "8 mm (L-11)", nm: "chunky" }, "6": { g: 8, hk: "10 mm (N/P-15)", nm: "super bulky" } };
    var CHS = { sc: { b: 6, w: 1, h: 0.85, ch: 1, yd: 1.45 }, hdc: { b: 8, w: 1.05, h: 1.2, ch: 2, yd: 1.3 }, dc: { b: 12, w: 1.09, h: 1.55, ch: 2, yd: 1.2 } };
    var chtT = "us", chtB = "sc";
    var chtRun = function () {
      var hs = hatSize("#cht-z", "#cht-m"), yk = $("#cht-y").value, y = CHY[yk], sk = $("#cht-s").value, S = CHS[sk], uk = chtT === "uk";
      var NM = { sc: uk ? "dc" : "sc", hdc: uk ? "htr" : "hdc", dc: uk ? "tr" : "dc" }, st = NM[sk], scN = NM.sc;
      var ws = 4 / y.g, sw = ws * S.w, rh = ws * S.h;
      var Nt = Math.round(hs.c / sw); if (chtB === "rib" && Nt % 2) Nt++;
      var k = Math.max(3, Math.floor(Nt / S.b)), N = k * S.b, E = Math.max(0, Nt - N); if (E < 2) E = 0;
      var brimH = chtB === "rib" ? Math.max(0.75, Math.round(hs.head * 0.068 * 4) / 4) : 2 * ws * 0.85;
      var NF = N + E, even = Math.max(1, Math.round((hs.len - brimH - hs.c / (2 * Math.PI)) / rh) - (E ? 1 : 0)), k2 = k + (E ? 1 : 0);
      var ribR = Math.max(2, Math.round(brimH / (ws * 1.55)));
      var chs = "ch " + S.ch + " (doesn't count as a stitch)";
      var o = [];
      o.push('<p class="sub">Top circle</p><p class="big">' + k2 + "<small> increase rounds to " + NF + " stitches</small></p><p>" + y.hk + " hook, " + y.nm + " yarn, " + (uk ? "UK" : "US") + " terms. Hat " + hs.c + " in around for a " + hs.head + " in head; " + hs.len + " in long from the top.</p>");
      o.push("<h3>Your pattern</h3><ol>");
      o.push("<li><strong>Round 1:</strong> make a magic ring, " + chs + ", work " + S.b + " " + st + " into the ring. Pull the ring closed and join with a sl st to the first " + st + " (" + S.b + ").</li>");
      o.push("<li><strong>Round 2:</strong> " + chs.split(" (")[0] + ", 2 " + st + " in each st around, join (" + (2 * S.b) + ").</li>");
      for (var r = 3; r <= k; r++) o.push("<li><strong>Round " + r + ":</strong> " + chs.split(" (")[0] + ", *" + st + " in the next " + (r - 2 > 1 ? (r - 2) + " sts" : "st") + ", 2 " + st + " in the next st; repeat from * " + (S.b - 1) + " more times, join (" + (r * S.b) + ").</li>");
      if (E) { var q = Math.floor(N / E) - 1, rest = N - E * (q + 1); o.push("<li><strong>Round " + (k + 1) + " (part increase):</strong> " + chs.split(" (")[0] + ", *" + st + " in the next " + q + " sts, 2 " + st + " in the next st; repeat from * " + (E - 1) + " more times" + (rest ? ", " + st + " in the last " + rest + (rest > 1 ? " sts" : " st") : "") + ", join (" + NF + ").</li>"); }
      o.push('<li><strong>Check:</strong> the flat circle should be about <strong>' + (Math.round(hs.c / Math.PI * 10) / 10) + " in (" + Math.round(hs.c / Math.PI * 2.54) + " cm) across</strong>. Bigger? Pull out a round. Smaller? Work one more round with a few increases spread out, or go up a hook size.</li>");
      o.push("<li><strong>Rounds " + (k2 + 1) + " to " + (k2 + even) + ":</strong> " + chs.split(" (")[0] + ", 1 " + st + " in each st around, join (" + NF + "). That's about " + even + " rounds: keep going until the hat is " + (Math.round((hs.len - brimH) * 4) / 4) + " in (" + Math.round((hs.len - brimH) * 2.54) + " cm) from the centre top.</li>");
      if (chtB === "rib") o.push("<li><strong>Brim, " + ribR + " rounds:</strong> ch 2, *FP" + (uk ? "tr" : "dc") + " round the next st, BP" + (uk ? "tr" : "dc") + " round the next st; repeat from * around, join (" + NF + "). On later rounds work FP over FP and BP over BP. About " + brimH + " in deep.</li>");
      else o.push("<li><strong>Last 2 rounds:</strong> ch 1, " + scN + " in each st around, join (" + NF + ").</li>");
      o.push("<li>Fasten off, weave in the ends and add a pom pom if you like.</li></ol>");
      var yd = hs.c * hs.len * 0.93 * S.yd * YF[yk];
      o.push('<p class="sub">Yarn: about <strong>' + r10(yd * 0.9) + " to " + r10(yd * 1.15) + " yd</strong> (" + Math.round(yd * 0.9 * 0.9144) + " to " + Math.round(yd * 1.15 * 0.9144) + " m), our estimate. Round heights are estimates too, so try the hat on as you go. Sizes from the <a href=\"" + ($("#cht-out").getAttribute("data-chart") || "hat-size-chart") + "\">hat size chart</a>.</p>");
      $("#cht-out").innerHTML = o.join("");
      store.set("pp-cht", { z: $("#cht-z").value, m: $("#cht-m").value, y: yk, s: sk, t: chtT, b: chtB });
    };
    var chtS = store.get("pp-cht", null);
    if (chtS) { ["z", "m", "y", "s"].forEach(function (q) { if (chtS[q] != null && $("#cht-" + q)) $("#cht-" + q).value = chtS[q]; });
      if (!CHY[$("#cht-y").value]) $("#cht-y").value = "4"; if (!CHS[$("#cht-s").value]) $("#cht-s").value = "dc"; if (!$("#cht-z").value) $("#cht-z").value = "6";
      if (chtS.t === "uk") { chtT = "uk"; $$("#cht-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); }
      if (chtS.b === "rib") { chtB = "rib"; $$("#cht-b button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "rib" ? "true" : "false"); }); } }
    ["#cht-z", "#cht-y", "#cht-s"].forEach(function (s) { $(s).addEventListener("change", chtRun); });
    $("#cht-m").addEventListener("input", chtRun);
    seg($("#cht-t"), function (v) { chtT = v; chtRun(); });
    seg($("#cht-b"), function (v) { chtB = v; chtRun(); });
    chtRun();
  }

  if ($("#kht-z") && $("#kht-out")) {
    // CYC knit gauge ranges (sts per 4 in) mid values and needles; rows per inch estimated at 1.35 x stitches per inch (typical stocking stitch).
    var KHY = { "3": { g: 22.5, nd: "4 to 4.5 mm (US 6 to 7)", rb: "3.5 mm (US 4)", nm: "DK" }, "4": { g: 18, nd: "5 mm (US 8)", rb: "4.5 mm (US 7)", nm: "worsted" },
                "5": { g: 13.5, nd: "6.5 mm (US 10½)", rb: "6 mm (US 10)", nm: "chunky" }, "6": { g: 9, nd: "9 to 10 mm (US 13 to 15)", rb: "8 mm (US 11)", nm: "super bulky" } };
    var khtF = "fit";
    var khtRun = function () {
      var hs = hatSize("#kht-z", "#kht-m"), yk = $("#kht-y").value, y = KHY[yk], rib = $("#kht-r").value;
      var mine = parseFloat($("#kht-g").value), g = mine >= 6 && mine <= 40 ? mine : y.g, spi = g / 4, rpi = spi * 1.35;
      var N = Math.max(24, Math.round(hs.c * spi / 8) * 8), s = N / 8;
      var bd = Math.max(0.75, Math.round(hs.head * 0.09 * 4) / 4);
      var L = hs.len + (khtF === "slouch" ? Math.round(hs.head * 0.11 * 2) / 2 : 0) + (khtF === "fold" ? bd + 0.5 : 0);
      var brim = rib === "0" ? 0 : (khtF === "fold" ? 2 * bd + 0.5 : bd);
      var pairs = Math.max(0, s - 6), crownR = 2 * pairs + (Math.min(s, 6) - 1), crownD = crownR / rpi;
      var before = Math.max(brim + 0.5, Math.round((L - crownD) * 4) / 4);
      var ribTxt = rib === "2" ? "*k2, p2; repeat from * to the end" : "*k1, p1; repeat from * to the end";
      var o = [];
      o.push('<p class="sub">Cast on</p><p class="big">' + N + "<small> stitches</small></p><p>" + y.nd + " needles, " + y.nm + " yarn, " + (mine ? "your gauge of " + g + " sts per 4 in" : "about " + g + " sts per 4 in (the Craft Yarn Council range)") + ". Hat " + hs.c + " in around for a " + hs.head + " in head.</p>");
      o.push("<h3>Your pattern</h3><ol><li>Cast on " + N + " stitches onto a " + (hs.c >= 17 ? "16 in (40 cm) circular needle" : "set of double-pointed needles or a long circular for the magic loop (this size is too small for a 16 in circular)") + ". Place a marker and join in the round without twisting.</li>");
      if (rib === "0") o.push("<li>Knit every round. The edge will roll up into a neat curl (allow about 0.75 in for it).</li>");
      else o.push("<li><strong>Brim:</strong> " + ribTxt + ". Repeat this round for " + brim + " in (" + Math.round(brim * 2.54) + " cm)" + (khtF === "fold" ? ", long enough to fold up" : "") + ". A needle 1 or 2 sizes smaller, " + y.rb + ", makes a snugger brim.</li>");
      o.push("<li><strong>Body:</strong> knit every round until the hat measures <strong>" + before + " in (" + Math.round(before * 2.54) + " cm)</strong> from the cast-on edge" + (khtF === "fold" ? " (unfolded)" : "") + ".</li>");
      o.push("<li><strong>Set up the crown:</strong> *k" + s + ", place marker; repeat from * 7 more times (8 sections of " + s + ").</li>");
      var c = s, rn = 1, lines = [];
      while (c > 1) {
        lines.push("<strong>Crown round " + rn + ":</strong> " + (c - 2 > 0 ? "*knit to 2 sts before the marker (k" + (c - 2) + "), k2tog" : "*k2tog") + "; repeat from * 7 more times (" + ((c - 1) * 8) + " sts).");
        rn++; c--;
        if (c >= 6 && c > 1) { lines.push("<strong>Crown round " + rn + ":</strong> knit."); rn++; }
      }
      if (lines.length > 14) { o.push("<li>" + lines[0] + "</li><li>" + lines[1] + "</li><li>Repeat these 2 rounds (one fewer stitch before each k2tog every time) until 48 sts are left, ending with a knit round.</li>"); lines.filter(function (l) { return / \((40|32|24|16|8) sts\)/.test(l); }).forEach(function (l) { o.push("<li>" + l.replace(/Crown round \d+/, "Then") + "</li>"); }); }
      else lines.forEach(function (l) { o.push("<li>" + l + "</li>"); });
      o.push("<li>Switch to double-pointed needles or magic loop when the stitches get tight. With 8 sts left, cut the yarn with a 6 in tail, thread it through all 8, pull tight and weave in.</li></ol>");
      var yd = hs.c * L * 0.93 * YF[yk] * (rib === "0" ? 0.95 : 1.05);
      o.push('<p class="sub">Finished length about ' + (Math.round((before + crownD) * 4) / 4) + " in. The crown is about " + (Math.round(crownD * 4) / 4) + " in deep (our estimate from a typical row gauge). Yarn: about <strong>" + r10(yd * 0.9) + " to " + r10(yd * 1.15) + " yd</strong> (" + Math.round(yd * 0.9 * 0.9144) + " to " + Math.round(yd * 1.15 * 0.9144) + " m), our estimate. Sizes from the <a href=\"" + ($("#kht-out").getAttribute("data-chart") || "hat-size-chart") + "\">hat size chart</a>.</p>");
      $("#kht-out").innerHTML = o.join("");
      store.set("pp-kht", { z: $("#kht-z").value, m: $("#kht-m").value, y: yk, r: rib, g: $("#kht-g").value, f: khtF });
    };
    var khtS = store.get("pp-kht", null);
    if (khtS) { ["z", "m", "y", "r", "g"].forEach(function (q) { if (khtS[q] != null && $("#kht-" + q)) $("#kht-" + q).value = khtS[q]; });
      if (!KHY[$("#kht-y").value]) $("#kht-y").value = "4"; if (!$("#kht-r").value) $("#kht-r").value = "2"; if (!$("#kht-z").value) $("#kht-z").value = "6";
      if (khtS.f === "fold" || khtS.f === "slouch") { khtF = khtS.f; $$("#kht-f button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === khtF ? "true" : "false"); }); } }
    ["#kht-z", "#kht-y", "#kht-r"].forEach(function (s) { $(s).addEventListener("change", khtRun); });
    ["#kht-m", "#kht-g"].forEach(function (s) { $(s).addEventListener("input", khtRun); });
    seg($("#kht-f"), function (v) { khtF = v; khtRun(); });
    khtRun();
  }

  if ($("#ppm-d") && $("#ppm-out")) {
    // Our rough model: wraps ~ 20 x D^2 in worsted (scaled for yarn thickness); each wrap ~ ring width + card thickness. Labelled as estimates.
    var PPY = { dk: { w: 1.6, g: 2.3, nm: "DK" }, w: { w: 1, g: 1.9, nm: "worsted" }, ch: { w: 0.6, g: 1.3, nm: "chunky" }, sb: { w: 0.35, g: 0.8, nm: "super bulky" } };
    var ppmU = "in";
    var ppmRun = function () {
      var D = parseFloat($("#ppm-d").value) || 3, yk = $("#ppm-y").value, y = PPY[yk] || PPY.w, cm = ppmU === "cm";
      var out = D + 0.25, hole = Math.round(out * 0.4 * 8) / 8, wraps = Math.round(20 * D * D * y.w / 10) * 10;
      var yd = wraps * (out - hole + 0.2) / 36 + 0.3, u = function (v) { return cm ? (Math.round(v * 2.54 * 10) / 10) + " cm" : v + " in"; };
      var o = [];
      o.push('<p class="sub">Cut two card rings</p><p class="big">' + u(out) + "<small> across</small></p><p>Centre hole: <strong>" + u(hole) + "</strong> across.</p>");
      o.push("<p>Wrap about <strong>" + wraps + " times</strong> in " + y.nm + " (until the hole is full). Yarn: about <strong>" + Math.round(yd) + " to " + Math.round(yd * 1.3) + " yd</strong> (" + Math.round(yd * 0.9144) + " to " + Math.round(yd * 1.3 * 0.9144) + " m, roughly " + Math.max(1, Math.round(yd / y.g)) + " to " + Math.max(2, Math.round(yd * 1.3 / y.g)) + " g). Plus a 12 in piece of strong yarn for the middle tie.</p>");
      o.push("<p>" + (D <= 1.5 ? "<strong>Easiest method:</strong> a fork works for this size: wrap the tines about " + Math.round(wraps * 0.9 / 5) * 5 + " times." : D <= 3 ? "<strong>No card?</strong> Wrap " + (D <= 2 ? "two" : D <= 2.5 ? "three" : "four") + " fingers instead, about " + Math.round(wraps * 0.7 / 10) * 10 + " times (it's less even, so trim a little more)." : "<strong>Big pom pom:</strong> card is best; wrap in several colours or hold 2 strands together to fill it faster.") + "</p>");
      var R = out / 2, r = hole / 2, ring = function (cx) { return '<circle cx="' + cx + '" cy="' + R + '" r="' + R + '" fill="#efe3cf" stroke="#1f2a44" stroke-width="0.02"/><circle cx="' + cx + '" cy="' + R + '" r="' + r + '" fill="#fff" stroke="#1f2a44" stroke-width="0.02"/><rect x="' + (cx - 0.06) + '" y="0" width="0.12" height="' + (R - r) + '" fill="#fff" stroke="#1f2a44" stroke-width="0.015"/>'; };
      var two = 2 * out + 0.3 <= 7.5, tw = two ? 2 * out + 0.3 : out;
      o.push('<p class="sub">Template at actual size (print at 100%, no scaling)' + (two ? "" : "; cut it twice") + ':</p><div class="ppm-tpl" style="overflow-x:auto"><svg role="img" aria-label="Pom pom card ring template at actual size" width="' + tw + 'in" height="' + out + 'in" viewBox="0 0 ' + tw + " " + out + '">' + ring(R) + (two ? ring(out + 0.3 + R) : "") + "</svg></div>");
      o.push('<p class="sub">Ring and wrap numbers are our rough guide: tight or loose wrapping changes them. Cut the rings from a cereal box or a postcard.</p>');
      $("#ppm-out").innerHTML = o.join("");
      store.set("pp-ppm", { d: $("#ppm-d").value, y: yk, u: ppmU });
    };
    var ppmS = store.get("pp-ppm", null);
    if (ppmS) { if (ppmS.d) $("#ppm-d").value = ppmS.d; if (PPY[ppmS.y]) $("#ppm-y").value = ppmS.y; if (!$("#ppm-d").value) $("#ppm-d").value = "3";
      if (ppmS.u === "cm") { ppmU = "cm"; $$("#ppm-u button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "cm" ? "true" : "false"); }); } }
    ["#ppm-d", "#ppm-y"].forEach(function (s) { $(s).addEventListener("change", ppmRun); });
    seg($("#ppm-u"), function (v) { ppmU = v; ppmRun(); });
    ppmRun();
  }

  /* ---------- run 17: crochet bauble writer (cxo-*) ---------- */
  if ($("#cxo-k") && $("#cxo-out")) {
    // Standard amigurumi sphere: k increase rounds to 6k, k even rounds, k-1 decrease rounds. Gauge (tight sc per in) and yarn per 36 sc are our estimates.
    var CXY = { dk: { g: 5.5, per: 1.25, hk: "3 mm (C-2 or D-3)" }, w: { g: 4.5, per: 1.6, hk: "3.5 mm (E-4)" }, ch: { g: 3.2, per: 2.3, hk: "5 mm (H-8)" } };
    var cxoT = "us", cxoS = store.get("pp-cxo", null) || {};
    if (cxoS.k) $("#cxo-k").value = cxoS.k; if (cxoS.y && CXY[cxoS.y]) $("#cxo-y").value = cxoS.y; if (cxoS.s) $("#cxo-s").value = cxoS.s; if (cxoS.n) $("#cxo-n").value = cxoS.n;
    if (cxoS.t === "uk") { cxoT = "uk"; $$("#cxo-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); }
    var cxoRun = function () {
      var k = parseInt($("#cxo-k").value, 10) || 5, yk = $("#cxo-y").value, y = CXY[yk] || CXY.w, st = $("#cxo-s").value, n = Math.max(1, Math.min(60, parseInt($("#cxo-n").value, 10) || 1));
      var SC = cxoT === "uk" ? "dc" : "sc", DEC = cxoT === "uk" ? "dc2tog" : "sc2tog";
      var R = [], r = 1;
      R.push([r++, "6 " + SC + " in a magic ring", 6]);
      R.push([r++, "inc in each st around", 12]);
      for (var i = 3; i <= k; i++) R.push([r++, "(" + SC + " " + (i - 2) + ", inc) x 6", 6 * i]);
      var evenStart = r;
      for (var j = 0; j < k; j++) R.push([r++, SC + " in each st around", 6 * k]);
      var decStart = r;
      for (var m = k - 1; m >= 1; m--) R.push([r++, m > 1 ? "(" + SC + " " + (m - 1) + ", dec) x 6" : "dec x 6", 6 * m]);
      // colour plan
      var col = R.map(function () { return "A"; }), even = [];
      for (var q = evenStart; q < decStart; q++) even.push(q - 1);
      if (st === "band") { var bw = k >= 6 ? 3 : 2, b0 = Math.floor((k - bw) / 2); for (var b = 0; b < bw; b++) col[even[b0 + b]] = "B"; }
      else if (st === "stripes") { col[even[Math.max(0, Math.floor(k / 2) - 2)]] = "B"; col[even[Math.min(k - 1, Math.floor(k / 2) + 1)]] = "B"; }
      else if (st === "half") { for (var h = Math.ceil(k / 2) + evenStart - 1; h < R.length; h++) col[h] = "B"; }
      var key = "pp-cxo-done-" + k + st, done = store.get(key, []) || [];
      var stsA = 0, stsB = 0, rows = R.map(function (x, idx) {
        if (col[idx] === "B") stsB += x[2]; else stsA += x[2];
        var change = idx > 0 && col[idx] !== col[idx - 1] && st !== "plain" ? "<strong>Switch to colour " + col[idx] + ":</strong> " : "";
        var stuff = x[2] === 18 && idx >= decStart - 1 && k >= 4 ? " Stuff firmly now." : (x[2] === 12 && idx >= decStart - 1 && k === 3 ? " Stuff firmly now." : "");
        return '<li><label class="chk"><input type="checkbox" data-cxo="' + idx + '"' + (done.indexOf(idx) >= 0 ? " checked" : "") + '> <span><strong>R' + x[0] + ":</strong> " + (st !== "plain" && idx === 0 ? "With colour A, " : "") + change + x[1] + " <em>(" + x[2] + ")</em>" + stuff + "</span></label></li>";
      });
      var D = 6 * k / y.g / Math.PI, ydA = Math.ceil(stsA * y.per / 36 * 1.1 + 2), ydB = Math.ceil(stsB * y.per / 36 * 1.1 + (stsB ? 1 : 0));
      var o = ['<p class="sub">Your bauble</p><p class="big">' + (Math.round(D * 10) / 10) + '<small> in across (about ' + Math.round(D * 2.54 * 10) / 10 + " cm)</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Hook</td><td>' + y.hk + "</td></tr><tr><td>Colour A, per bauble</td><td>about " + ydA + " yd</td></tr>" + (stsB ? "<tr><td>Colour B, per bauble</td><td>about " + ydB + " yd</td></tr>" : "") +
        "<tr><td>Gold for cap and loop</td><td>about 3 yd</td></tr><tr><td>For " + n + " bauble" + (n > 1 ? "s" : "") + "</td><td>" + (ydA * n) + " yd of A" + (stsB ? ", " + (ydB * n) + " yd of B" : "") + ", " + (3 * n) + " yd of gold</td></tr><tr><td>Time</td><td>about " + Math.round(k * 10) + " to " + Math.round(k * 13) + " min each</td></tr></tbody></table>");
      o.push('<h3>Your pattern (' + (cxoT === "uk" ? "UK" : "US") + ' terms)</h3><p class="sub">Work in a spiral, moving a marker up each round. inc = 2 ' + SC + " in the same stitch; dec = " + DEC + ".</p><ul class=\"shp-list\">" + rows.join("") + '<li class="shp-note">Fasten off, thread the tail through the front loops of the last 6 stitches and pull closed. Make the cap and loop (below) and sew them on.</li></ul>');
      o.push('<p class="sub">Sizes and yarn are estimates from the stitch count with 10% spare; tension changes them. Ticks are kept on this device. <button type="button" class="btn ghost" id="cxo-reset">Clear ticks</button></p>');
      $("#cxo-out").innerHTML = o.join("");
      $$("input[data-cxo]", $("#cxo-out")).forEach(function (c) { c.addEventListener("change", function () { var d = $$("input[data-cxo]", $("#cxo-out")).filter(function (x) { return x.checked; }).map(function (x) { return parseInt(x.getAttribute("data-cxo"), 10); }); store.set(key, d); }); });
      $("#cxo-reset").addEventListener("click", function () { store.set(key, []); cxoRun(); });
      store.set("pp-cxo", { k: $("#cxo-k").value, y: yk, s: st, n: $("#cxo-n").value, t: cxoT });
    };
    ["#cxo-k", "#cxo-y", "#cxo-s", "#cxo-n"].forEach(function (s) { $(s).addEventListener("change", cxoRun); });
    $("#cxo-n").addEventListener("input", cxoRun);
    seg($("#cxo-t"), function (v) { cxoT = v; cxoRun(); });
    cxoRun();
  }

  /* ---------- run 17: crochet snowflake helper (csf-*) ---------- */
  if ($("#csf-y") && $("#csf-out")) {
    // Our estimates for the 4-round pattern on the page: finished diameter (in) and length per snowflake incl. tails (yd).
    var CSFY = { t10: { d: 3, yd: 7, nm: "size 10 cotton thread" }, t3: { d: 3.75, yd: 9, nm: "size 3 cotton" }, sp: { d: 4.25, yd: 10, nm: "sport yarn" }, dk: { d: 5, yd: 12, nm: "DK yarn" }, w: { d: 5.5, yd: 15, nm: "worsted yarn" } };
    var CSFM = { glue: ["White PVA glue + water", function (ml) { return "about " + Math.ceil(ml / 2) + " ml glue and " + Math.ceil(ml / 2) + " ml water (equal parts; more glue for stiffer)"; }, "overnight, up to 24 hours", "Firm and long-lasting."],
                 starch: ["Liquid laundry starch", function (ml) { return "about " + ml + " ml, straight from the bottle"; }, "overnight", "Medium stiff; washes out."],
                 corn: ["Cornflour paste", function () { return "1 tablespoon cornflour stirred into a little cold water, added to 1 cup (240 ml) boiling water and stirred until slightly thick; cool before use (one batch does a lot)"; }, "overnight", "Medium; can soften in damp rooms."],
                 sugar: ["Sugar syrup", function (ml) { var c = Math.max(0.25, Math.ceil(ml / 60) / 4); return "about " + c + " cup sugar + " + c + " cup water, warmed until clear, cooled"; }, "overnight; keep away from damp", "Very stiff, but sticky in humid air."],
                 spray: ["Spray starch", function () { return "a can of spray starch; spray the pinned snowflakes until damp, let dry, spray again"; }, "1 to 2 hours per coat", "Light hold."] };
    var CSF_UK = [["sc", "dc"], ["dc", "tr"]];
    var csfT = "us", csfS = store.get("pp-csf", null) || {}, csfBoxes = $$("input[data-csf]");
    if (csfS.y && CSFY[csfS.y]) $("#csf-y").value = csfS.y; if (csfS.m && CSFM[csfS.m]) $("#csf-m").value = csfS.m; if (csfS.n) $("#csf-n").value = csfS.n;
    if (csfS.t === "uk") { csfT = "uk"; $$("#csf-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); }
    var csfDone = store.get("pp-csf-done", []) || [];
    csfBoxes.forEach(function (b) { if (csfDone.indexOf(b.getAttribute("data-csf")) >= 0) b.checked = true; b.addEventListener("change", function () { store.set("pp-csf-done", csfBoxes.filter(function (x) { return x.checked; }).map(function (x) { return x.getAttribute("data-csf"); })); csfRun(); }); });
    var csfTerms = function () {
      $$("#csf-rounds [data-us]").forEach(function (s) {
        var t = s.getAttribute("data-us");
        if (csfT === "uk") t = t.replace(/\bdc\b/g, "@@").replace(/\bsc\b/g, "dc").replace(/@@/g, "tr");
        s.textContent = t;
      });
    };
    var csfRun = function () {
      var y = CSFY[$("#csf-y").value] || CSFY.t3, mk = $("#csf-m").value, m = CSFM[mk] || CSFM.glue, n = Math.max(1, Math.min(100, parseInt($("#csf-n").value, 10) || 1));
      var ml = Math.max(60, Math.ceil(n * y.d * y.d * 1.2 / 10) * 10), yd = y.yd * n, done = csfBoxes.filter(function (x) { return x.checked; }).length;
      var o = ['<p class="sub">Your snowflake in ' + y.nm + '</p><p class="big">' + y.d + '<small> in across (about ' + Math.round(y.d * 2.54 * 10) / 10 + " cm)</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Thread or yarn</td><td>about ' + y.yd + " yd each, " + yd + " yd for " + n + "</td></tr><tr><td>Time</td><td>about " + Math.round(n * 25 / 60 * 10) / 10 + " hours of crochet for " + n + "</td></tr><tr><td>Stiffener</td><td>" + m[0] + ": " + m[1](ml) + "</td></tr><tr><td>Drying</td><td>" + m[2] + "</td></tr><tr><td>Pins</td><td>about " + (n * 13) + " rust-proof pins (13 per snowflake: centre, 6 points, 6 side picots), or pin in batches</td></tr></tbody></table>");
      o.push("<p>" + m[3] + " Board space: about " + Math.ceil(Math.sqrt(n)) + " x " + Math.ceil(n / Math.ceil(Math.sqrt(n))) + " snowflakes, each " + (Math.round((y.d + 1) * 10) / 10) + " in apart.</p>");
      o.push('<p class="sub">Sizes, yarn and amounts are our estimates for the pattern on this page. ' + done + " of 4 rounds ticked.</p>");
      $("#csf-out").innerHTML = o.join("");
      csfTerms();
      store.set("pp-csf", { y: $("#csf-y").value, m: mk, n: $("#csf-n").value, t: csfT });
    };
    ["#csf-y", "#csf-m", "#csf-n"].forEach(function (s) { $(s).addEventListener("change", csfRun); });
    $("#csf-n").addEventListener("input", csfRun);
    seg($("#csf-t"), function (v) { csfT = v; csfRun(); });
    csfRun();
  }

  /* ---------- run 17: beginner crochet blanket writer (cbk-*) ---------- */
  if ($("#cbk-z") && $("#cbk-out") && P.tblanket) {
    // Same model as the blanket size calculator / temperature blanket planner: CYC-based sc gauge by weight x stitch factors; yardage 0.667 yd per sq in
    // x weight factor x 1.27 for crochet x stitch density. Speeds are our beginner estimates (12-18 stitches a minute).
    var CBK = P.tblanket, cbkW = P.weights || [], cbkT = "us", cbkS0 = store.get("pp-cbk", null) || {};
    var CBST = { sc: { ch: 1, from: "2nd", tc: "ch 1", uk: "dc" }, hdc: { ch: 2, from: "3rd", tc: "ch 2", uk: "htr" }, dc: { ch: 2, from: "4th", tc: "ch 3 (counts as the first dc)", uk: "tr" } };
    ["z", "w", "l", "y", "s", "k", "g"].forEach(function (f) { if (cbkS0[f] !== undefined && $("#cbk-" + f)) $("#cbk-" + f).value = cbkS0[f]; });
    if (cbkS0.t === "uk") { cbkT = "uk"; $$("#cbk-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); }
    var cbkRun = function () {
      var z = $("#cbk-z").value, own = z === "custom", bl = (P.blankets || []).filter(function (b) { return b.id === z; })[0];
      $("#cbk-own").hidden = !own;
      var W = own ? Math.min(120, Math.max(8, parseFloat($("#cbk-w").value) || 50)) : bl.w, L = own ? Math.min(120, Math.max(8, parseFloat($("#cbk-l").value) || 60)) : bl.l;
      var wn = $("#cbk-y").value, wt = cbkW.filter(function (x) { return String(x.n) === wn; })[0] || { m: 1, hook: "" }, sk = $("#cbk-s").value;
      var st = CBK.stitches.filter(function (x) { return x.id === sk; })[0], cs = CBST[sk], base = CBK.cg[wn] || 12.5;
      var g = parseFloat($("#cbk-g").value) || 0, spi = g > 0 ? g / 4 : base * st.w / 4, rpi = g > 0 ? g / 4 / st.w * st.r : base * st.r / 4;
      var bord = 3 * 2 / (base / 4); /* 3 sc rounds each side, in inches */
      var bodyW = Math.max(4, W - bord), bodyL = Math.max(4, L - bord), sts = Math.max(4, Math.round(bodyW * spi)), rows = Math.max(2, Math.round(bodyL * rpi)), chains = sts + cs.ch;
      var dens = g > 0 ? (base * st.w / 4) / spi : 1, yd = W * L * 0.667 * (wt.m || 1) * 1.27 * st.d * dens, lo = yd * 0.88, hi = yd * 1.12;
      var per = parseFloat($("#cbk-k").value) || 0, skeins = per > 0 ? Math.ceil(hi / per) : 0;
      var total = sts * rows + 2 * (sts + rows) * 3, hLo = total / 18 / 60, hHi = total / 12 / 60;
      var nm = cbkT === "uk" ? cs.uk : sk, SC = cbkT === "uk" ? "dc" : "sc", f = function (v) { return Math.round(v).toLocaleString(); };
      var o = ['<p class="sub">' + (own ? "Your blanket" : bl.name) + ", " + W + " x " + L + ' in</p><p class="big">' + chains + "<small> chains to start</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Stitches per row</td><td>' + sts + "</td></tr><tr><td>Rows</td><td>about " + rows + " (or work until the body is " + Math.round(bodyL) + " in long)</td></tr><tr><td>Yarn</td><td>about " + f(lo) + " to " + f(hi) + " yd (" + f(lo * 0.9144) + " to " + f(hi * 0.9144) + " m)</td></tr><tr><td>Skeins</td><td>" + (skeins ? skeins + " of " + per + " yd (covers the high end)" : "enter yards per skein") + "</td></tr><tr><td>Hook</td><td>" + wt.hook + "</td></tr><tr><td>Time</td><td>about " + Math.round(hLo) + " to " + Math.round(hHi) + " hours</td></tr></tbody></table>");
      o.push("<h3>Your pattern (" + (cbkT === "uk" ? "UK" : "US") + " terms)</h3><ol>" +
        "<li>Chain " + chains + ".</li>" +
        "<li><strong>Row 1:</strong> " + nm + " in the " + cs.from + " chain from the hook and in each chain to the end. Turn. (" + sts + " sts)</li>" +
        "<li><strong>Row 2:</strong> " + cs.tc + ", " + (sk === "dc" ? "skip the first st, " + nm + " in each st across, " + nm + " in the top of the turning chain" : nm + " in each st across") + ". Turn. (" + sts + " sts)</li>" +
        "<li><strong>Rows 3 to " + rows + ":</strong> repeat row 2. Don't fasten off.</li>" +
        "<li><strong>Border:</strong> ch 1, then work " + SC + " evenly round all four sides with 3 " + SC + " in each corner (along the side edges about " + (sk === "sc" ? "1 " + SC + " per row" : sk === "hdc" ? "3 " + SC + " for every 2 rows" : "2 " + SC + " per row") + "). Join with a sl st. Work 2 more rounds of " + SC + ", with 3 " + SC + " in each corner stitch.</li>" +
        "<li>Fasten off and weave in all ends.</li></ol>");
      o.push('<p class="sub">Estimates from typical gauge for this yarn and stitch' + (g > 0 ? " (using your swatch)" : "") + ", with the 3-round border taken off the body. Your tension changes everything: crochet a 6 in swatch first, and buy one spare skein in the same dye lot.</p>");
      $("#cbk-out").innerHTML = o.join("");
      var sv = { t: cbkT }; ["z", "w", "l", "y", "s", "k", "g"].forEach(function (k) { sv[k] = $("#cbk-" + k).value; }); store.set("pp-cbk", sv);
    };
    ["z", "w", "l", "y", "s", "k", "g"].forEach(function (k) { var el = $("#cbk-" + k); el.addEventListener("change", cbkRun); el.addEventListener("input", cbkRun); });
    seg($("#cbk-t"), function (v) { cbkT = v; cbkRun(); });
    cbkRun();
  }

  /* ---------- run 18: beginner knit blanket writer (kbk-*) ---------- */
  if ($("#kbk-z") && $("#kbk-out") && P.tblanket) {
    // CYC knit gauge by weight (tblanket.kg, sts per 4 in); row ratio garter 2.0, stockinette 1.33, seed 1.6 (typical); yardage 0.667 yd per sq in
    // x weight factor x stitch density. Speed 25-40 sts a minute (our estimate for a comfortable knitter).
    var KBK = P.tblanket, kbkW = P.weights || [], kbkS0 = store.get("pp-kbk", null) || {};
    var KST = { garter: { r: 2.0, d: 1.2 }, seed: { r: 1.6, d: 1.2 }, st: { r: 1.33, d: 1.05 } };
    ["z", "w", "l", "y", "s", "k", "g"].forEach(function (f) { if (kbkS0[f] !== undefined && $("#kbk-" + f)) $("#kbk-" + f).value = kbkS0[f]; });
    var kbkRun = function () {
      var z = $("#kbk-z").value, own = z === "custom", bl = (P.blankets || []).filter(function (b) { return b.id === z; })[0];
      if (!own && !bl) { z = "custom"; own = true; }
      $("#kbk-own").hidden = !own;
      var W = own ? Math.min(120, Math.max(8, parseFloat($("#kbk-w").value) || 40)) : bl.w, L = own ? Math.min(120, Math.max(8, parseFloat($("#kbk-l").value) || 50)) : bl.l;
      var wn = $("#kbk-y").value, wt = kbkW.filter(function (x) { return String(x.n) === wn; })[0] || { m: 1, needle: "" }, sk = $("#kbk-s").value, st = KST[sk] || KST.garter;
      var base = KBK.kg[wn] || 18, g = parseFloat($("#kbk-g").value) || 0, spi = (g > 0 ? g : base) / 4, rpi = spi * st.r;
      var co = Math.max(6, Math.round(W * spi)); if (sk === "seed" && co % 2 === 0) co += 1;
      var rows = Math.max(4, Math.round(L * rpi)); if (rows % 2) rows += 1;
      var dens = g > 0 ? base / g : 1, yd = W * L * 0.667 * (wt.m || 1) * st.d * dens, lo = yd * 0.88, hi = yd * 1.12;
      var per = parseFloat($("#kbk-k").value) || 0, balls = per > 0 ? Math.ceil(hi / per) : 0, total = co * rows, hLo = total / 40 / 60, hHi = total / 25 / 60;
      var cable = W <= 30 ? "32 in (80 cm)" : W <= 45 ? "40 in (100 cm)" : "47 in (120 cm) or longer", f = function (v) { return Math.round(v).toLocaleString(); };
      var o = ['<p class="sub">' + (own ? "Your blanket" : bl.name) + ", " + W + " x " + L + ' in</p><p class="big">' + co + "<small> stitches to cast on</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Rows</td><td>about ' + f(rows) + (sk === "garter" ? " (" + f(rows / 2) + " ridges)" : "") + ", or knit until it's " + L + " in long</td></tr><tr><td>Yarn</td><td>about " + f(lo) + " to " + f(hi) + " yd (" + f(lo * 0.9144) + " to " + f(hi * 0.9144) + " m)</td></tr><tr><td>Balls</td><td>" + (balls ? balls + " of " + per + " yd (covers the high end)" : "enter yards per ball") + "</td></tr><tr><td>Needle</td><td>" + wt.needle + ", " + cable + " circular, worked flat</td></tr><tr><td>Time</td><td>about " + f(hLo) + " to " + f(hHi) + " hours</td></tr></tbody></table>");
      var rowsTxt, b = 5, frame = 8;
      if (sk === "garter") rowsTxt = "<li><strong>Every row:</strong> knit all " + co + " stitches. (Optional neat edge: slip the first stitch purlwise with the yarn in front, then knit to the end.)</li><li>Repeat until you have knit about " + f(rows) + " rows, or the blanket measures " + L + " in, ending after a right-side row.</li>";
      else if (sk === "seed") rowsTxt = "<li><strong>Every row:</strong> *k1, p1; repeat from * to the last stitch, k1. (With an odd number of stitches every row is the same.)</li><li>Repeat until you have knit about " + f(rows) + " rows, or it measures " + L + " in.</li>";
      else rowsTxt = "<li><strong>Rows 1 to " + frame + ":</strong> knit (garter border).</li><li><strong>Right-side rows:</strong> knit all stitches.</li><li><strong>Wrong-side rows:</strong> k" + b + ", purl to the last " + b + " stitches, k" + b + ".</li><li>Repeat these two rows until it measures about " + (L - 1.5) + " in (" + f(rows - 2 * frame) + " rows), ending after a wrong-side row.</li><li><strong>Last " + frame + " rows:</strong> knit.</li>";
      o.push("<h3>Your pattern</h3><ol><li>Cast on " + co + " stitches with the long-tail cast on.</li>" + rowsTxt + "<li>Bind off loosely knitwise" + (sk === "seed" ? " (or in pattern)" : "") + ". Weave in the ends, then wash and lay flat.</li></ol>");
      o.push('<p class="sub">Estimates from typical gauge for this yarn' + (g > 0 ? " (using your swatch)" : "") + ". Your tension changes everything: knit a 6 in swatch first, and buy one spare ball in the same dye lot.</p>");
      $("#kbk-out").innerHTML = o.join("");
      var sv = {}; ["z", "w", "l", "y", "s", "k", "g"].forEach(function (k) { sv[k] = $("#kbk-" + k).value; }); store.set("pp-kbk", sv);
    };
    ["z", "w", "l", "y", "s", "k", "g"].forEach(function (k) { var el = $("#kbk-" + k); el.addEventListener("change", kbkRun); el.addEventListener("input", kbkRun); });
    kbkRun();
  }

  /* ---------- run 18: crochet ear warmer writer (chb-*) ---------- */
  if ($("#chb-z") && $("#chb-out") && P.tblanket) {
    // Strip of hdc in back loop only, worked sideways. Gauge: CYC sc gauge (tblanket.cg) x 0.95 for hdc width, 0.8 for rows; BLO rows ~10% shorter.
    // Length = 90% of head (rib stretch). Yardage 0.667 yd/sq in x weight factor x 1.27 (crochet) x 1.15 (hdc BLO). Speed 5-8 sts/min incl. turning (beginner-friendly estimate).
    var chbW = P.weights || [], chbT = "us", chbS0 = store.get("pp-chb", null) || {};
    ["z", "c", "y", "w", "f", "g"].forEach(function (k) { if (chbS0[k] !== undefined && $("#chb-" + k)) $("#chb-" + k).value = chbS0[k]; });
    if (chbS0.t === "uk") { chbT = "uk"; $$("#chb-t button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === "uk" ? "true" : "false"); }); }
    var chbRun = function () {
      var z = $("#chb-z").value, hz = (P.hats || []).filter(function (h) { return h.id === z; })[0], own = !hz;
      $("#chb-own").hidden = !own;
      var head = own ? Math.min(26, Math.max(14, parseFloat($("#chb-c").value) || 22)) : hz.head;
      var wn = $("#chb-y").value, wt = chbW.filter(function (x) { return String(x.n) === wn; })[0] || { m: 1, hook: "" }, base = (P.tblanket.cg || {})[wn] || 12.5;
      var g = parseFloat($("#chb-g").value) || 0, spi = g > 0 ? g / 4 : base * 0.95 / 4, rpi = (g > 0 ? g / 0.95 : base) * 0.8 * 1.1 / 4;
      var W = parseFloat($("#chb-w").value) || 3.5, len = head * 0.9, sts = Math.max(4, Math.round(W * spi)), ch = sts + 2, rows = Math.max(6, Math.round(len * rpi));
      var yd = W * len * 0.667 * (wt.m || 1) * 1.27 * 1.15 * (g > 0 ? (base * 0.95 / 4) / spi : 1) + 2, lo = yd * 0.85, hi = yd * 1.15;
      var mins = sts * rows, hLo = mins / 8 / 60 + 0.25, hHi = mins / 5 / 60 + 0.4;
      var H = chbT === "uk" ? "htr" : "hdc", SS = "sl st", tw = $("#chb-f").value === "twist", r1 = function (v) { return Math.round(v * 10) / 10; };
      var o = ['<p class="sub">' + (own ? "Your head, " + head + " in" : hz.name + ", " + hz.head + " in head") + ", " + W + ' in wide</p><p class="big">' + ch + "<small> chains to start</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Stitches per row</td><td>' + sts + "</td></tr><tr><td>Rows</td><td>about " + rows + " (strip about " + r1(len) + " in long, unstretched)</td></tr><tr><td>Yarn</td><td>about " + Math.round(lo) + " to " + Math.round(hi) + " yd (" + Math.round(lo * 0.9144) + " to " + Math.round(hi * 0.9144) + " m)</td></tr><tr><td>Hook</td><td>" + wt.hook + "</td></tr><tr><td>Time</td><td>about " + r1(hLo) + " to " + r1(hHi) + " hours</td></tr></tbody></table>");
      o.push("<h3>Your pattern (" + (chbT === "uk" ? "UK" : "US") + " terms)</h3><ol>" +
        "<li>Leave a 12 in tail for sewing. Chain " + ch + ".</li>" +
        "<li><strong>Row 1:</strong> " + H + " in the 3rd chain from the hook and in each chain to the end. Turn. (" + sts + " sts)</li>" +
        "<li><strong>Row 2:</strong> ch 2 (doesn't count as a stitch), " + H + " in the back loop only of each stitch across. Turn. (" + sts + " sts)</li>" +
        "<li><strong>Rows 3 to " + rows + ":</strong> repeat row 2. Wrap it round the head: it should feel snug when slightly stretched. Add or take off rows to fit.</li>" +
        (tw ? "<li><strong>Twist:</strong> fasten off, leaving a 12 in tail. Lay the strip right side up. Fold each short end in half lengthwise, then slide one folded end inside the other so they hug. Pin.</li><li><strong>Sew</strong> through all four layers with the tail, using small whip stitches. Turn right side out and weave in the ends.</li>"
            : "<li><strong>Join:</strong> bring the short ends together, right sides facing, and " + SS + " through both layers (or sew with the tail). Turn right side out and weave in the ends.</li>") + "</ol>");
      o.push('<p class="sub">Estimates from typical gauge' + (g > 0 ? " (using your swatch)" : "") + ". Back-loop rows stretch a lot, so trust the try-on more than the row count. One skein of most yarns makes two or three ear warmers.</p>");
      $("#chb-out").innerHTML = o.join("");
      var sv = { t: chbT }; ["z", "c", "y", "w", "f", "g"].forEach(function (k) { sv[k] = $("#chb-" + k).value; }); store.set("pp-chb", sv);
    };
    ["z", "c", "y", "w", "f", "g"].forEach(function (k) { var el = $("#chb-" + k); el.addEventListener("change", chbRun); el.addEventListener("input", chbRun); });
    seg($("#chb-t"), function (v) { chbT = v; chbRun(); });
    chbRun();
  }

  /* ---------- run 18: skein splitter (ywb-*) ---------- */
  if ($("#ywb-g") && $("#ywb-out")) {
    var ywbS0 = store.get("pp-ywb", null) || {};
    ["g", "lg", "ly", "n", "need"].forEach(function (k) { if (ywbS0[k] !== undefined && $("#ywb-" + k)) $("#ywb-" + k).value = ywbS0[k]; });
    var ywbRun = function () {
      var g = Math.max(0.5, parseFloat($("#ywb-g").value) || 100), lg = Math.max(1, parseFloat($("#ywb-lg").value) || 100), ly = Math.max(1, parseFloat($("#ywb-ly").value) || 400);
      var ypg = ly / lg, totY = g * ypg, n = $("#ywb-n").value, o = [], r1 = function (v) { return Math.round(v * 10) / 10; };
      $("#ywb-need-f").hidden = n !== "yd";
      if (n === "yd") {
        var need = Math.max(1, parseFloat($("#ywb-need").value) || 100), w = need / ypg;
        if (need >= totY) o.push('<p class="big">' + Math.round(totY) + '<small> yd in this skein</small></p><p>That\'s less than the ' + need + " yd you need: you'll need another skein.</p>");
        else o.push('<p class="sub">Wind the first ball until it weighs</p><p class="big">' + r1(w) + '<small> g</small></p><table class="mt"><tbody><tr><td>First ball</td><td>' + need + " yd (" + Math.round(need * 0.9144) + " m)</td></tr><tr><td>What's left</td><td>" + r1(g - w) + " g, about " + Math.round(totY - need) + " yd</td></tr><tr><td>Or watch the skein</td><td>stop when the skein on the scale reads " + r1(g - w) + " g</td></tr></tbody></table>");
      } else {
        var k = parseInt(n, 10) || 2, each = g / k, rows = "";
        for (var i = 1; i < k; i++) rows += "<tr><td>After ball " + i + "</td><td>skein reads " + r1(g - each * i) + " g</td></tr>";
        o.push('<p class="sub">Each of ' + k + " balls</p><p class=\"big\">" + r1(each) + '<small> g</small></p><table class="mt"><tbody><tr><td>Yards in each</td><td>about ' + Math.round(totY / k) + " yd (" + Math.round(totY / k * 0.9144) + " m)</td></tr>" + rows + "</tbody></table>");
      }
      o.push('<p class="sub">Yards from the label\'s ' + r1(ypg) + " yd per gram. Weigh the real skein: labels round the weight and skeins vary by a few grams. Tare the scale with a bowl, wind loosely, check often.</p>");
      $("#ywb-out").innerHTML = o.join("");
      var sv = {}; ["g", "lg", "ly", "n", "need"].forEach(function (k) { sv[k] = $("#ywb-" + k).value; }); store.set("pp-ywb", sv);
    };
    ["g", "lg", "ly", "n", "need"].forEach(function (k) { var el = $("#ywb-" + k); el.addEventListener("change", ywbRun); el.addEventListener("input", ywbRun); });
    ywbRun();
  }

  /* ---------- run 19: flat Christmas stocking writer (xks-*) ---------- */
  if ($("#xks-z") && $("#xks-out")) {
    // Sizes match /christmas-stocking-calculator [height, flat width, foot, cuff]. CYC knit gauge mid values; rows 1.35 x sts/in, garter 1.9.
    // Yardage = same model as the stocking calculator (0.667 yd per sq in x weight factor x 1.1). Speed 13-20 sts a minute (beginner estimate) + 1 h sewing.
    var XS = { mini: [7, 3.5, 4.5, 1.5], small: [12, 5, 7, 2.5], standard: [18, 7, 10, 3.5], large: [22, 8, 12, 4], xl: [26, 9, 14, 5] };
    var XG = { 3: 22, 4: 18, 5: 14, 6: 9 }, XM = { 3: 1.18, 4: 1, 5: 0.72, 6: 0.52 }, XN = { 3: "US 6 (4 mm)", 4: "US 8 (5 mm)", 5: "US 10.5 (6.5 mm)", 6: "US 13 (9 mm)" };
    var xkS0 = store.get("pp-xks", null) || {};
    ["z", "y", "g", "c"].forEach(function (k) { if (xkS0[k] !== undefined && $("#xks-" + k)) $("#xks-" + k).value = xkS0[k]; });
    var xkEven = function (v, m) { v = Math.max(m, Math.round(v)); return v % 2 ? v + 1 : v; };
    var xksRun = function () {
      var d = XS[$("#xks-z").value] || XS.standard, h = d[0], w = d[1], f = d[2], c = d[3], wt = $("#xks-y").value;
      var base = XG[wt] || 18, g = parseFloat($("#xks-g").value) || 0, spi = (g > 0 ? g : base) / 4, rpi = spi * 1.35, rib = $("#xks-c").value === "rib";
      var co = xkEven(w * spi, 6), cuffR = xkEven(c * spi * (rib ? 1.35 : 1.9), 4), legR = xkEven((h - c - w) * rpi, 2);
      var toe = Math.max(2, Math.round((f - w) * spi)), N = Math.max(1, Math.round(spi * 0.7)), footR = xkEven(w * rpi - 2 * N, 2), last = co + toe - 2 * N;
      var dens = g > 0 ? base / g : 1, k = 0.667 * (XM[wt] || 1) * 1.1 * dens, body = 2 * (w * Math.max(h - w, 0) + f * w), tot = body * k, cuffY = 2 * w * c * k;
      var sts = 2 * (co * (cuffR + legR) + (co + toe) * (footR + 2 * N)), hLo = sts / 20 / 60 + 1, hHi = sts / 13 / 60 + 1;
      var r5 = function (v) { return Math.round(v / 5) * 5; }, r1 = function (v) { return Math.round(v * 2) / 2; };
      var cuffTxt = rib ? "*k1, p1; repeat from * to the end" : "knit every stitch";
      var o = ['<p class="sub">' + h + " in tall, " + w + " in wide, foot " + f + ' in. Two pieces.</p><p class="big">' + co + "<small> stitches to cast on</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Yarn</td><td>about ' + r5(tot * 0.85) + " to " + r5(tot * 1.15) + " yd in all (" + r5(tot * 0.85 * 0.9144) + " to " + r5(tot * 1.15 * 0.9144) + " m), of which the cuff is about " + r5(cuffY * 1.15) + " yd</td></tr><tr><td>Needles</td><td>" + (g > 0 ? "the size that gave your swatch" : XN[wt]) + "</td></tr><tr><td>Time</td><td>about " + Math.round(hLo) + " to " + Math.round(hHi) + " hours, sewing included</td></tr></tbody></table>");
      o.push("<h3>Piece 1 (toe points right)</h3><ol>" +
        "<li><strong>Cuff:</strong> in the cuff colour, cast on " + co + " stitches. Rows 1 to " + cuffR + ": " + cuffTxt + ". (About " + c + " in.)</li>" +
        "<li><strong>Leg:</strong> join the main colour. Row 1 (right side): knit. Row 2: purl. Repeat these 2 rows " + (legR / 2) + " times in all (" + legR + " rows, about " + r1(h - c - w) + " in), ending after a purl row.</li>" +
        "<li><strong>Toe stitches:</strong> next row (right side): cast on " + toe + " stitches at the start of the row with the cable cast on, then knit to the end. (" + (co + toe) + " sts)</li>" +
        "<li><strong>Foot:</strong> starting with a purl row, work " + footR + " rows of stockinette, ending after a purl row.</li>" +
        "<li><strong>Round the heel and toe:</strong> right-side row: k2tog, knit to the last 2 stitches, ssk. Wrong-side row: purl. Repeat these 2 rows " + N + " time" + (N > 1 ? "s" : "") + " in all. (" + last + " sts)</li>" +
        "<li>Bind off loosely. Leave a long tail on one piece for sewing.</li></ol>");
      o.push("<h3>Piece 2 (toe points left)</h3><ol><li>Work the cuff and leg the same, then knit one more row so you finish after a right-side row.</li><li><strong>Toe stitches:</strong> next row (wrong side): cast on " + toe + " stitches at the start of the row, then purl to the end. (" + (co + toe) + " sts)</li><li>Starting with a knit row, work " + footR + " rows of stockinette, ending after a purl row, then round the heel and toe and bind off exactly as piece 1.</li></ol>");
      o.push("<h3>Finishing</h3><ol><li>Weave in the ends. Put the pieces right sides together and sew round the leg, heel, foot and toe, leaving the top open.</li><li>Turn right side out. For a loop, knit a 3-stitch i-cord about 4 in long (or crochet 25 chains) and sew both ends inside the cuff at the heel side.</li></ol>");
      o.push('<p class="sub">Estimates from typical gauge for this yarn' + (g > 0 ? " (using your swatch)" : "") + '. If your piece is wider than ' + w + ' in, go down a needle size. In the round instead? Use the <a href="' + (location.protocol === "file:" ? "christmas-stocking-calculator.html" : "/christmas-stocking-calculator") + '">stocking calculator</a>.</p>');
      $("#xks-out").innerHTML = o.join("");
      var sv = {}; ["z", "y", "g", "c"].forEach(function (k2) { sv[k2] = $("#xks-" + k2).value; }); store.set("pp-xks", sv);
    };
    ["z", "y", "g", "c"].forEach(function (k) { var el = $("#xks-" + k); el.addEventListener("change", xksRun); el.addEventListener("input", xksRun); });
    xksRun();
  }

  /* ---------- run 19: safety eye size helper (sey-*) ---------- */
  if ($("#sey-s") && $("#sey-out")) {
    // Head diameter from the widest round: circumference = stitches / sts per inch (tight amigurumi single crochet, our estimates by weight).
    // Eye diameter as a share of head width: cute 0.19, classic 0.14, realistic 0.10 (our design proportions). Snaps to common shop sizes.
    var SPI = { 1: 7, 3: 5.5, 4: 4.5, 5: 3.5, 6: 2.6 }, SR = { cute: 0.19, classic: 0.14, real: 0.1 }, SDY = { cute: 0.12, classic: 0.05, real: -0.02 }, SGP = { cute: 1.6, classic: 1.4, real: 1.3 };
    var SZ = [4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 30], seS0 = store.get("pp-sey", null) || {};
    ["y", "s", "l", "m"].forEach(function (k) { if (seS0[k] !== undefined && $("#sey-" + k)) $("#sey-" + k).value = seS0[k]; });
    var seyNear = function (v) { var b = SZ[0]; SZ.forEach(function (z) { if (Math.abs(z - v) < Math.abs(b - v)) b = z; }); return b; };
    var seyRun = function () {
      var y = $("#sey-y").value, S = Math.min(180, Math.max(12, parseInt($("#sey-s").value, 10) || 42)), look = $("#sey-l").value, spi = SPI[y] || 4.5;
      var circ = S / spi * 25.4, D = circ / Math.PI, ideal = D * SR[look], pick = $("#sey-m").value === "auto" ? seyNear(ideal) : parseFloat($("#sey-m").value);
      var i = SZ.indexOf(seyNear(ideal)), alt = [SZ[Math.max(0, i - 1)], SZ[Math.min(SZ.length - 1, i + 1)]];
      var gap = pick * SGP[look], stw = 25.4 / spi, gapSts = Math.max(1, Math.round(gap / stw)), cx = D / 2 + 4, cy = D / 2 + 4, ey = cy + D * SDY[look], off = (gap + pick) / 2, W = D + 8;
      var face = '<svg viewBox="0 0 ' + W.toFixed(1) + " " + W.toFixed(1) + '" style="width:' + W.toFixed(1) + "mm;max-width:100%;height:auto;display:block;margin:8px auto;background:#fbf8f1;border-radius:8px\" role=\"img\" aria-label=\"Head " + Math.round(D) + " mm wide with " + pick + ' mm eyes">' +
        '<circle cx="' + cx + '" cy="' + cy + '" r="' + (D / 2).toFixed(1) + '" fill="#f2e3cf" stroke="#1f2a44" stroke-width="0.6"/>' +
        [-1, 1].map(function (sgn) { var x = (cx + sgn * off).toFixed(1); return '<circle cx="' + x + '" cy="' + ey.toFixed(1) + '" r="' + (pick / 2) + '" fill="#1f2a44"/><circle cx="' + (cx + sgn * off - pick * 0.18).toFixed(1) + '" cy="' + (ey - pick * 0.18).toFixed(1) + '" r="' + (pick * 0.12).toFixed(2) + '" fill="#fff"/>'; }).join("") +
        '<path d="M' + (cx - D * 0.06).toFixed(1) + " " + (ey + pick * 0.9).toFixed(1) + " q" + (D * 0.06).toFixed(1) + " " + (D * 0.05).toFixed(1) + " " + (D * 0.12).toFixed(1) + ' 0" fill="none" stroke="#b8326a" stroke-width="' + Math.max(0.6, D * 0.012).toFixed(2) + '"/></svg>';
      var strip = '<p style="display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap">' + [alt[0], pick, alt[1]].filter(function (v, j, a) { return a.indexOf(v) === j; }).map(function (z) { return '<span style="text-align:center"><span style="display:block;width:' + z + "mm;height:" + z + 'mm;border-radius:50%;background:#fbf8f1;margin:0 auto 4px"></span>' + z + " mm</span>"; }).join("") + "</p>";
      var o = ['<p class="sub">Head about ' + Math.round(D) + " mm (" + (D / 25.4).toFixed(1) + ' in) across</p><p class="big">' + pick + "<small> mm eyes" + ($("#sey-m").value === "auto" ? " suggested" : "") + "</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Also try</td><td>' + alt.filter(function (z) { return z !== pick; }).join(" mm or ") + " mm</td></tr><tr><td>Between the eyes</td><td>about " + Math.round(gap) + " mm, roughly " + gapSts + " stitch" + (gapSts > 1 ? "es" : "") + "</td></tr><tr><td>Height</td><td>" + (look === "cute" ? "a round or two below the middle of the head" : look === "classic" ? "just below the middle" : "on or just above the middle") + "</td></tr></tbody></table>");
      o.push(face + strip);
      o.push('<p class="sub">Drawn close to actual size on most screens (it shrinks to fit on small phones). Head size is an estimate from a typical tight amigurumi gauge: measure your real head across for a better check. Not for toys for under 3s or pets: embroider the eyes.</p>');
      $("#sey-out").innerHTML = o.join("");
      var sv = {}; ["y", "s", "l", "m"].forEach(function (k) { sv[k] = $("#sey-" + k).value; }); store.set("pp-sey", sv);
    };
    ["y", "s", "l", "m"].forEach(function (k) { var el = $("#sey-" + k); el.addEventListener("change", seyRun); el.addEventListener("input", seyRun); });
    seyRun();
  }

  /* ---------- run 19: junk journal cover size calculator (jjc-*) ---------- */
  if ($("#jjc-p") && $("#jjc-out")) {
    // Boards: page + 1/8 in wide, + 1/4 in tall (1/8 in square on 3 sides). Spine: signatures x sheets x 2 leaves x paper thickness x bulk + thread.
    // Hinge gap: 2 x board thickness, at least 1/8 in. Turn-in 3/4 in. Linings 1/8 in smaller than the board on each side.
    var jjS0 = store.get("pp-jjc", null) || {};
    ["p", "w", "h", "n", "s", "t", "b", "x"].forEach(function (k) { if (jjS0[k] !== undefined && $("#jjc-" + k)) $("#jjc-" + k).value = jjS0[k]; });
    var jjcRun = function () {
      var pv = $("#jjc-p").value, own = pv === "custom"; $("#jjc-own").hidden = !own;
      var pw = own ? Math.min(14, Math.max(2, parseFloat($("#jjc-w").value) || 5)) : parseFloat(pv.split("x")[0]), ph = own ? Math.min(16, Math.max(2, parseFloat($("#jjc-h").value) || 7)) : parseFloat(pv.split("x")[1]);
      var n = Math.min(12, Math.max(1, parseInt($("#jjc-n").value, 10) || 4)), sh = Math.min(20, Math.max(1, parseInt($("#jjc-s").value, 10) || 6)), t = parseFloat($("#jjc-t").value) || 0.006, b = parseFloat($("#jjc-b").value) || 0.02, x = parseFloat($("#jjc-x").value) || 1.5;
      var bw = pw + 0.125, bh = ph + 0.25, stack = n * sh * 2 * t * x + n * 0.01, spine = Math.max(0.25, Math.ceil(stack * 16) / 16), hinge = Math.max(0.125, Math.ceil(2 * b * 16) / 16);
      var cw = 2 * bw + 2 * hinge + spine + 1.5, ch = bh + 1.5, row = spine / (n + 1);
      var q = function (v) { return (Math.round(v * 16) / 16).toFixed(2).replace(/0$/, "").replace(/\.0$/, ""); }, cm = function (v) { return (v * 2.54).toFixed(1); };
      var dim = function (a, c) { return q(a) + " x " + q(c) + " in (" + cm(a) + " x " + cm(c) + " cm)"; };
      var fits = cw <= 11 && ch <= 8.5 ? "letter or A4 paper (sideways)" : cw <= 12 && ch <= 12 ? "12 x 12 in scrapbook paper" : cw <= 17 && ch <= 11 ? "11 x 17 in (tabloid) or A3 paper" : "a big sheet: wrapping paper, fabric or two sheets joined at the spine";
      var o = ['<p class="sub">' + q(pw) + " x " + q(ph) + " in pages, " + n + " signature" + (n > 1 ? "s" : "") + " of " + sh + ' sheets</p><p class="big">' + q(spine) + "<small> in spine (" + cm(spine) + " cm)</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Front and back boards</td><td>2 at ' + dim(bw, bh) + "</td></tr><tr><td>Spine strip</td><td>" + dim(spine, bh) + "</td></tr><tr><td>Hinge gap</td><td>" + q(hinge) + " in (" + cm(hinge) + " cm) each side of the spine</td></tr><tr><td>Cover paper or fabric</td><td>" + dim(cw, ch) + ", fits on " + fits + "</td></tr><tr><td>Lining papers</td><td>2 at " + dim(bw - 0.25, bh - 0.25) + "</td></tr><tr><td>Sewing rows on the spine</td><td>" + n + " rows of 3 holes, about " + q(row) + " in apart; holes 1 in from top and bottom and one in the middle</td></tr></tbody></table>");
      var S = 300 / cw, H = ch * S, X = function (v) { return (v * S).toFixed(1); };
      var a = 0.75, g = '<svg viewBox="0 0 300 ' + H.toFixed(1) + '" role="img" aria-label="Cover cutting layout" style="width:100%;max-width:520px;height:auto;display:block;margin:10px 0;background:#fbf8f1;border-radius:8px">' +
        '<rect x="0.5" y="0.5" width="299" height="' + (H - 1).toFixed(1) + '" fill="#e9d9e8" stroke="#1f2a44"/>' +
        '<rect x="' + X(a) + '" y="' + X(a) + '" width="' + X(bw) + '" height="' + X(bh) + '" fill="#c9a77c" stroke="#1f2a44"/>' +
        '<rect x="' + X(a + bw + hinge) + '" y="' + X(a) + '" width="' + X(spine) + '" height="' + X(bh) + '" fill="#b48f63" stroke="#1f2a44"/>' +
        '<rect x="' + X(a + bw + 2 * hinge + spine) + '" y="' + X(a) + '" width="' + X(bw) + '" height="' + X(bh) + '" fill="#c9a77c" stroke="#1f2a44"/>' +
        '<text x="' + X(a + bw / 2) + '" y="' + X(a + bh / 2) + '" font-size="12" text-anchor="middle" fill="#1f2a44">back</text><text x="' + X(a + bw * 1.5 + 2 * hinge + spine) + '" y="' + X(a + bh / 2) + '" font-size="12" text-anchor="middle" fill="#1f2a44">front</text>' +
        '<text x="150" y="' + (H - 4).toFixed(1) + '" font-size="10" text-anchor="middle" fill="#1f2a44">' + q(cw) + " x " + q(ch) + " in cover, " + q(a) + " in to fold in all round</text></svg>";
      o.push(g);
      o.push('<p class="sub">Paper thickness and bulk are estimates. For the best fit, stack your finished signatures, press them flat and measure, then add a little for what you will tuck in later.</p>');
      $("#jjc-out").innerHTML = o.join("");
      var sv = {}; ["p", "w", "h", "n", "s", "t", "b", "x"].forEach(function (k) { sv[k] = $("#jjc-" + k).value; }); store.set("pp-jjc", sv);
    };
    ["p", "w", "h", "n", "s", "t", "b", "x"].forEach(function (k) { var el = $("#jjc-" + k); el.addEventListener("change", jjcRun); el.addEventListener("input", jjcRun); });
    jjcRun();
  }

  /* ---------- SLEEVE DECREASE CALCULATOR (28 Nov) ---------- */
  if (page === "sleeve-decrease-calculator") {
    var sdS0 = store.get("pp-sleevedec", {});
    ["s", "e", "k", "r", "len", "rg"].forEach(function (k) { if (sdS0[k] !== undefined && $("#sd-" + k)) $("#sd-" + k).value = sdS0[k]; });
    if (sdS0.rs !== undefined) $("#sd-rs").checked = sdS0.rs;
    var sdLink = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '">' + t + "</a>"; };
    var sdPlan = null;
    var sdRun = function () {
      var knit = segVal($("#sd-craft")) !== "crochet", inc = segVal($("#sd-dir")) === "inc";
      $("#sd-rs-f").hidden = !knit;
      var len = parseFloat($("#sd-len").value), rg = parseFloat($("#sd-rg").value), per = segVal($("#sd-u")) === "cm" ? 10 : 4;
      if (len > 0 && rg > 0) $("#sd-r").value = Math.max(1, Math.round(len / per * rg));
      var S = parseInt($("#sd-s").value, 10) || 0, E = parseInt($("#sd-e").value, 10) || 0, k = parseInt($("#sd-k").value, 10) || 2, R = parseInt($("#sd-r").value, 10) || 0;
      var rs = knit && $("#sd-rs").checked, word = inc ? "increase" : "decrease", rw = knit ? "row" : "row";
      var diff = inc ? E - S : S - E, out = [];
      var sv = { s: $("#sd-s").value, e: $("#sd-e").value, k: $("#sd-k").value, r: $("#sd-r").value, len: $("#sd-len").value, rg: $("#sd-rg").value, rs: $("#sd-rs").checked }; store.set("pp-sleevedec", sv);
      sdPlan = null;
      if (S < 1 || E < 1 || R < 1) { $("#sd-out").innerHTML = '<p class="sub">Enter your stitch counts and rows.</p>'; return; }
      if (diff <= 0) { $("#sd-out").innerHTML = '<p class="sub">To ' + word + ", the end count must be " + (inc ? "more" : "fewer") + " than the start count. Switch Increase/Decrease above or check the numbers.</p>"; return; }
      var n = Math.ceil(diff / k), extra = n * k - diff;
      var unit = rs ? 2 : 1, slots = Math.floor(R / unit);
      if (n > slots) {
        $("#sd-out").innerHTML = '<p class="big">' + n + "<small> shaping rows needed</small></p><p class=\"sub\">That's more than the " + slots + (rs ? " right-side rows" : " rows") + " you have. Shape more stitches per row (try 4), add rows, or change the end count.</p>";
        return;
      }
      var q = Math.floor(slots / n), rem = slots - q * n, gA = q * unit, gB = (q + 1) * unit, nB = rem, nA = n - rem;
      var parts = [];
      if (nA > 0) parts.push({ g: gA, t: nA });
      if (nB > 0) parts.push({ g: gB, t: nB });
      var used = nA * gA + nB * gB, left = R - used;
      var ord = function (x) { var s = ["th", "st", "nd", "rd"], v = x % 100; return x + (s[(v - 20) % 10] || s[v] || s[0]); };
      var edge = k === 2 ? "1 st at each end" : k === 1 ? "1 st at one edge" : "2 sts at each end (or at each marker)";
      var phr = parts.map(function (p, i) { return (i ? "then " : "") + "every " + (p.g === 1 ? "row" : ord(p.g) + " row") + " " + p.t + " time" + (p.t > 1 ? "s" : ""); }).join(", ");
      var line = word.charAt(0).toUpperCase() + word.slice(1) + " " + edge + (k === 1 ? " on " : " of ") + phr + ".";
      out.push('<p class="sub">' + S + " to " + E + " stitches over " + R + " rows</p>");
      out.push('<p class="big">' + n + "<small> shaping rows</small></p>");
      out.push('<p style="font-size:1.1em"><strong>' + esc(line) + "</strong></p>");
      var notes = [];
      if (extra > 0) notes.push("The last shaping row only needs " + (k - extra) + " stitch" + (k - extra > 1 ? "es" : "") + " " + word + "d, so you land exactly on " + E + ".");
      if (left > 0) notes.push("That uses " + used + " rows; work the last " + left + " row" + (left > 1 ? "s" : "") + " plain.");
      if (rs) notes.push("Gaps are even, so every shaping row is a right-side row. Count the first shaping row as row " + parts[0].g + ".");
      if (knit && !inc) notes.push("Neat pair: k1, ssk at the start and k2tog, k1 at the end of the row.");
      if (knit && inc) notes.push("Neat pair: k1, M1R at the start and M1L, k1 at the end of the row.");
      if (!knit) notes.push(inc ? "Work 2 stitches into the second stitch from each end." : "Work sc2tog (or dc2tog) one stitch in from each end.");
      out.push("<ul>" + notes.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>");
      var rows = [], r = 0, st = S;
      parts.forEach(function (p) { for (var i = 0; i < p.t; i++) { r += p.g; var d = Math.min(k, Math.abs(E - st)); st += inc ? d : -d; rows.push([r, st]); } });
      out.push('<details open><summary>Row-by-row list (' + rows.length + ' shaping rows)</summary><ol class="sd-list" style="columns:2;column-gap:24px;padding-left:22px">' + rows.map(function (x) { return '<li><label><input type="checkbox"> row ' + x[0] + ": " + x[1] + " sts</label></li>"; }).join("") + "</ol></details>");
      out.push('<p><button type="button" class="btn sm" id="sd-rc">Add to my row counter</button> <button type="button" class="btn ghost sm" onclick="window.print()">Print</button></p>');
      out.push('<p class="sub">Next: ' + sdLink("increase-decrease-calculator", "increase evenly across a row") + ", " + sdLink("sweater-size-calculator", "sweater size") + ", " + sdLink("row-counter", "row counter") + ".</p>");
      $("#sd-out").innerHTML = out.join("");
      sdPlan = { g: parts[0].g, total: used, name: "Sleeve: " + word + " every " + ord(parts[0].g) + (parts.length > 1 ? " then " + ord(parts[1].g) : "") };
      $("#sd-rc").addEventListener("click", function () {
        var C = store.get("pp-counters", null);
        if (!C || !C.list) C = { list: [], buzz: true, next: 1 };
        C.list.push({ id: C.next || (C.list.length + 1), name: sdPlan.name.slice(0, 40), n: 0, target: String(sdPlan.total), rep: String(sdPlan.g) });
        C.next = (C.next || C.list.length) + 1;
        store.set("pp-counters", C);
        toast("Added to your row counter");
        setTimeout(function () { location.href = location.protocol === "file:" ? "row-counter.html" : "/row-counter"; }, 600);
      });
    };
    seg($("#sd-craft"), sdRun); seg($("#sd-dir"), sdRun); seg($("#sd-u"), sdRun);
    ["s", "e", "k", "r", "len", "rg", "rs"].forEach(function (k) { var el = $("#sd-" + k); el.addEventListener("change", sdRun); el.addEventListener("input", sdRun); });
    sdRun();
  }

  /* ---------- run 20: crochet basket pattern writer (cbb-*) ---------- */
  if ($("#cbb-z") && $("#cbb-out")) {
    // Flat sc circle: 6 sts per round; base rounds from circumference (6R sts = pi x D x g). Walls: rounds = H x g (firm sc is near square).
    // Yarn = (base area + wall area) x yd per sq in (firm sc, estimates) x 1.1 for rim and ends.
    var CBY = { w2: { g: 3, k: 1.5, hook: "6 mm (US J-10)", ball: 200, n: "worsted held double (yards counted for both strands)" }, w1: { g: 4, k: 1.0, hook: "4.5 mm (US 7)", ball: 200, n: "worsted, one strand" },
      b: { g: 3, k: 0.75, hook: "5.5 to 6 mm (US I-9 to J-10)", ball: 130, n: "bulky (5)" }, sb: { g: 2.25, k: 0.55, hook: "8 mm (US L-11)", ball: 100, n: "super bulky (6)" }, t: { g: 1.75, k: 0.45, hook: "10 mm (US N/P-15)", ball: 120, n: "T-shirt yarn or cotton cord" } };
    var cbbS0 = store.get("pp-cbb", null) || {};
    ["z", "d", "h", "y", "g", "x", "t"].forEach(function (k) { if (cbbS0[k] !== undefined && $("#cbb-" + k)) $("#cbb-" + k).value = cbbS0[k]; });
    var cbbRun = function () {
      var zv = $("#cbb-z").value, own = zv === "custom"; $("#cbb-own").hidden = !own;
      var D = own ? Math.min(20, Math.max(3, parseFloat($("#cbb-d").value) || 8)) : parseFloat(zv.split("x")[0]), H = own ? Math.min(18, Math.max(1, parseFloat($("#cbb-h").value) || 6)) : parseFloat(zv.split("x")[1]);
      var Y = CBY[$("#cbb-y").value] || CBY.sb, sw = parseFloat($("#cbb-g").value), g = sw >= 4 && sw <= 24 ? sw / 4 : Y.g, x = $("#cbb-x").value, uk = $("#cbb-t").value === "uk";
      var sc = uk ? "dc" : "sc", inc = "inc (2 " + sc + " in next st)";
      var Rb = Math.max(3, Math.round(D * Math.PI * g / 6)), S = 6 * Rb, Dr = S / (Math.PI * g), W = Math.max(3, Math.round(H * g));
      var rows = [];
      for (var r = 1; r <= Rb; r++) {
        var t, k = r - 2;
        if (r === 1) t = "6 " + sc + " in a magic ring";
        else if (r === 2) t = "inc in each st around";
        else if (r % 2 === 1 || k < 2) t = "(" + sc + " " + k + ", inc) x 6";
        else { var a = Math.floor(k / 2), b = k - a; t = sc + " " + a + ", inc, (" + sc + " " + k + ", inc) x 5, " + sc + " " + b; }
        rows.push(["Round " + r, t + " (" + 6 * r + ")"]);
      }
      var first = Rb + 1, last = Rb + W, rim = last, warn = [];
      rows.push(["Round " + first, sc + " in the back loop only of each st around (" + S + "). This turns the corner."]);
      var hasH = x === "handles" || x === "both", hasY = x === "hole" || x === "both";
      var hR = hasH ? rim - 3 : 0, yR = hasY ? (hasH ? hR - 2 : rim - 3) : 0;
      if (hasH && hR <= first) { warn.push("The basket is too short for handle slots, so they're left out. Make it taller, or add a strap later."); hasH = false; hR = 0; }
      if (hasY && yR <= first) { yR = first + 1 < rim ? first + 1 : 0; if (!yR) { warn.push("Too short for a yarn hole; make it at least 2 in tall."); hasY = false; } }
      var L = Math.max(3, Math.round(3 * g)), half = Math.floor(S / 2), aa = Math.floor((half - L) / 2), c3 = Math.round(S / 4);
      var special = {};
      if (hasH) { special[hR] = sc + " " + aa + ", ch " + L + ", skip " + L + ", " + sc + " " + (half - L) + ", ch " + L + ", skip " + L + ", " + sc + " " + (S - aa - half - L) + " (two handle slots)"; special[hR + 1] = sc + " in each st and " + L + " " + sc + " into each chain space around (" + S + ")"; }
      if (hasY) { special[yR] = sc + " " + c3 + ", ch 3, skip 3, " + sc + " " + (S - c3 - 3) + " (yarn hole)"; special[yR + 1] = sc + " in each st and 3 " + sc + " into the ch-3 space (" + S + ")"; }
      var run0 = null, flush = function (to) { if (run0 !== null) { rows.push([run0 === to ? "Round " + run0 : "Rounds " + run0 + "-" + to, sc + " in each st around (" + S + ")"]); run0 = null; } };
      for (var q = first + 1; q < rim; q++) { if (special[q]) { flush(q - 1); rows.push(["Round " + q, special[q]]); } else if (run0 === null) run0 = q; }
      flush(rim - 1);
      rows.push(["Round " + rim, "sl st in next st, then reverse " + sc + " (crab stitch) in each st around, or sl st around for a plain rim. Fasten off and weave in."]);
      var area = Math.PI * Dr * Dr / 4 + Math.PI * Dr * H, yd = area * Y.k * 1.1 * (g / Y.g), balls = Math.ceil(yd / Y.ball);
      var sts = 3 * Rb * (Rb + 1) + S * W, hrs = sts / 9 / 60;
      var o = ['<p class="sub">' + D + " x " + H + " in basket in " + Y.n + ", about " + (g * 4).toFixed(1).replace(/\.0$/, "") + " " + sc + ' per 4 in</p><p class="big">' + Rb + "<small> base rounds, then " + W + " wall rounds</small></p>"];
      o.push('<table class="mt"><tbody><tr><td>Hook</td><td>' + Y.hook + " for firm fabric (go down a size if it's floppy)</td></tr><tr><td>Base</td><td>" + S + " sts, about " + Dr.toFixed(1) + " in (" + (Dr * 2.54).toFixed(0) + " cm) across</td></tr><tr><td>Yarn</td><td>about " + fmt(yd) + " yd (" + fmt(yd * 0.9144) + " m), roughly " + balls + " ball" + (balls > 1 ? "s" : "") + " of " + Y.ball + " yd</td></tr><tr><td>Time</td><td>about " + (hrs < 1 ? Math.max(15, Math.round(hrs * 60 / 5) * 5) + " minutes" : hrs.toFixed(1).replace(/\.0$/, "") + " hours") + " (" + fmt(sts) + " stitches)</td></tr></tbody></table>");
      if (warn.length) o.push("<ul>" + warn.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") + "</ul>");
      o.push('<p><strong>Pattern</strong> (' + (uk ? "UK" : "US") + " terms; work in a spiral, moving your marker up each round)</p>");
      o.push('<ol class="sd-list" style="list-style:none;padding-left:0">' + rows.map(function (r) { return '<li style="margin:4px 0"><label><input type="checkbox"> <strong>' + r[0] + ":</strong> " + esc(r[1]) + "</label></li>"; }).join("") + "</ol>");
      o.push('<p class="sub">Yardage and time are estimates for firm ' + sc + ". Count your stitches at the end of each base round: if the base cups or ripples, see the tips below.</p>");
      o.push('<p><button type="button" class="btn ghost sm" onclick="window.print()">Print pattern</button></p>');
      $("#cbb-out").innerHTML = o.join("");
      var sv = {}; ["z", "d", "h", "y", "g", "x", "t"].forEach(function (k) { sv[k] = $("#cbb-" + k).value; }); store.set("pp-cbb", sv);
    };
    ["z", "d", "h", "y", "g", "x", "t"].forEach(function (k) { var el = $("#cbb-" + k); el.addEventListener("change", cbbRun); el.addEventListener("input", cbbRun); });
    cbbRun();
  }

  /* ---------- run 20: pants hem calculator (hem-*) ---------- */
  if ($("#hem-m") && $("#hem-out")) {
    // Typical allowances (in): dress 1.5, tapered 1, jeans 0.5 + 0.5 double fold, wide 2, kids 2.5. Blind stitch every ~1/3 in. Thread ~ 2 x circumference + 8 in.
    var HEMT = { dress: { a: 1.5, d: false, n: "dress trousers", s: "blind hem" }, tapered: { a: 1, d: false, n: "a tapered leg", s: "blind hem" }, jeans: { a: 1, d: true, n: "jeans", s: "back stitch or running stitch close to the top fold" },
      wide: { a: 2, d: false, n: "wide-leg trousers", s: "blind hem" }, kids: { a: 2.5, d: false, n: "kids' trousers (let down later)", s: "loose blind hem" } };
    var hmS0 = store.get("pp-hem", null) || {};
    ["m", "u", "off", "c", "w", "t", "o"].forEach(function (k) { if (hmS0[k] !== undefined && $("#hem-" + k)) $("#hem-" + k).value = hmS0[k]; });
    var hemRun = function () {
      var byLen = $("#hem-m").value === "len", cm = $("#hem-u").value === "cm", U = cm ? 2.54 : 1, un = cm ? " cm" : " in";
      $("#hem-off-f").hidden = byLen; $("#hem-len-f").hidden = !byLen;
      var T = HEMT[$("#hem-t").value] || HEMT.dress;
      var off = byLen ? (parseFloat($("#hem-c").value) - parseFloat($("#hem-w").value)) / U : parseFloat($("#hem-off").value) / U;
      var sv = {}; ["m", "u", "off", "c", "w", "t", "o"].forEach(function (k) { sv[k] = $("#hem-" + k).value; }); store.set("pp-hem", sv);
      var f = function (v) { if (cm) return (Math.round(v * 2.54 * 2) / 2).toFixed(1).replace(/\.0$/, "") + " cm"; var w = Math.floor(v + 1e-9), fr = Math.round((v - w) * 8), F = ["", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"]; if (fr === 8) { w++; fr = 0; } return (w ? w + (fr ? " " : "") : (fr ? "" : "0")) + (fr ? F[fr] : "") + " in"; };
      if (!(off > 0)) { $("#hem-out").innerHTML = '<p class="sub">' + (byLen ? "The inseam you want must be shorter than the inseam now." : "Enter how much shorter you want them.") + "</p>"; return; }
      var cut = off - T.a, o = ['<p class="sub">Shortening ' + T.n + " by " + f(off) + '</p><p class="big">' + f(T.a) + "<small> hem allowance</small></p>"];
      var rowsT = [["Fold line", f(off) + " above the current bottom edge (mark it with chalk, both legs)"],
        ["Cut line", cut > 0.05 ? f(T.a) + " below the fold line, which is " + f(cut) + " above the current bottom edge" : "Don't cut: the amount you're taking off is less than the hem allowance. Unpick the old hem, press it flat and fold at the new line; the old hem fabric becomes part of the new hem. You need at least " + f(T.a - off) + " of fabric below the old edge."],
        ["How to fold", T.d ? "Fold up 1/2 in" + (cm ? " (1 cm)" : "") + ", then 1/2 in again, so the raw edge is hidden" : "Overcast or zigzag the raw edge, then fold up once along the fold line (or turn the raw edge under 1/4 in first: then cut " + f(0.25) + " lower)"],
        ["Stitch", T.s]];
      var op = parseFloat($("#hem-o").value);
      if (op > 0) { var circ = 2 * op / U, nst = Math.ceil(circ / 0.33), thr = 2 * circ + 8; rowsT.push(["Each leg", "about " + f(circ) + " round, roughly " + nst + " stitches 1/3 in apart; cut a single strand of thread about " + f(thr) + " (a bit more for jeans)"]); }
      o.push('<table class="mt"><tbody>' + rowsT.map(function (r) { return "<tr><td>" + r[0] + "</td><td>" + esc(r[1]) + "</td></tr>"; }).join("") + "</tbody></table>");
      var S = 280, sc = 150 / Math.max(off + 1, T.a + 1.5), y0 = 20, fy = y0 + 20, cy = fy + T.a * sc, by = fy + off * sc;
      var svg = '<svg viewBox="0 0 ' + S + " " + (Math.max(cy, by) + 30).toFixed(0) + '" role="img" aria-label="Fold and cut lines on the trouser leg" style="width:100%;max-width:420px;height:auto;display:block;margin:10px 0;background:#fbf8f1;border-radius:8px">' +
        '<path d="M70 ' + y0 + " h110 l6 " + (Math.max(cy, by) - y0).toFixed(1) + ' h-122 z" fill="#7d8db5" stroke="#1f2a44" stroke-width="1.5"/>' +
        '<line x1="55" y1="' + fy + '" x2="200" y2="' + fy + '" stroke="#b8326a" stroke-width="2"/><text x="204" y="' + (fy + 4) + '" font-size="11" fill="#1f2a44">fold line</text>' +
        (cut > 0.05 ? '<line x1="55" y1="' + cy.toFixed(1) + '" x2="200" y2="' + cy.toFixed(1) + '" stroke="#fff" stroke-width="2" stroke-dasharray="6 4"/><text x="204" y="' + (cy + 4).toFixed(1) + '" font-size="11" fill="#1f2a44">cut line</text>' : "") +
        '<line x1="55" y1="' + by.toFixed(1) + '" x2="200" y2="' + by.toFixed(1) + '" stroke="#1f2a44" stroke-width="2"/><text x="204" y="' + (by + 4).toFixed(1) + '" font-size="11" fill="#1f2a44">bottom now</text>' +
        '<text x="60" y="' + (fy - 6) + '" font-size="11" fill="#1f2a44" text-anchor="end">' + f(off) + "</text></svg>";
      o.push(svg);
      o.push('<p class="sub">Measure both legs separately, and pin and try on before cutting. Allowances are typical figures; if the old hem is deeper, you can match it.</p>');
      $("#hem-out").innerHTML = o.join("");
    };
    ["m", "u", "off", "c", "w", "t", "o"].forEach(function (k) { var el = $("#hem-" + k); el.addEventListener("change", hemRun); el.addEventListener("input", hemRun); });
    hemRun();
  }

  /* ---------- run 20: scrapbook layout sketch generator (sbl-*) ---------- */
  if ($("#sbl-p") && $("#sbl-out")) {
    // Templates on a 12 x 12 unit page: [type, x, y, w, h]; p photo, t title, j journaling, e embellishments. Scaled to the page size.
    var SBT = {
      1: [[["t", 1, 1, 10, 1.2], ["p", 2, 2.6, 8, 6], ["j", 2, 9, 5.4, 1.8], ["e", 8, 9, 2, 2]], [["p", 1, 1, 6, 8], ["t", 7.6, 1.5, 3.4, 1.4], ["j", 7.6, 3.4, 3.4, 4], ["e", 7.6, 8, 3.4, 2.8]], [["t", 3, 1.2, 6, 1.2], ["p", 3, 3, 6, 6], ["j", 3, 9.4, 4.6, 1.4], ["e", 8, 9.2, 2, 1.8]]],
      2: [[["p", 0.9, 2.4, 6, 4], ["p", 5.1, 6.8, 6, 4], ["t", 7.3, 2.6, 3.8, 1.2], ["j", 7.3, 4.2, 3.8, 2], ["e", 1, 7, 3.6, 3.6]], [["p", 1, 1, 4.8, 6.4], ["p", 6.2, 1, 4.8, 6.4], ["t", 1, 7.9, 10, 1.2], ["j", 1, 9.5, 6.6, 1.6], ["e", 8.2, 9.3, 2.8, 2]]],
      3: [[["p", 1, 1, 6, 4], ["p", 7.4, 1, 3.6, 4], ["p", 1, 5.4, 4, 3], ["t", 5.4, 5.6, 5.6, 1.2], ["j", 5.4, 7.2, 5.6, 1.8], ["e", 1, 9, 10, 2]], [["t", 1, 1.2, 10, 1.2], ["p", 1, 3, 3.1, 4.2], ["p", 4.45, 3, 3.1, 4.2], ["p", 7.9, 3, 3.1, 4.2], ["j", 1, 7.8, 7, 2], ["e", 8.4, 7.8, 2.6, 2.6]]],
      4: [[["p", 1, 1, 4.8, 3.6], ["p", 6.2, 1, 4.8, 3.6], ["p", 1, 5, 4.8, 3.6], ["p", 6.2, 5, 4.8, 3.6], ["t", 1, 9, 6, 1.2], ["j", 1, 10.4, 6, 0.8], ["e", 7.6, 9, 3.4, 2.2]], [["p", 1, 1, 7, 5], ["p", 8.4, 1, 2.6, 2.2], ["p", 8.4, 3.6, 2.6, 2.2], ["p", 8.4, 6.2, 2.6, 2.2], ["t", 1, 6.6, 7, 1.2], ["j", 1, 8.2, 7, 1.6], ["e", 8.4, 8.8, 2.6, 2.2]]],
      5: [[["p", 1, 1, 6, 4.5], ["p", 7.4, 1, 3.6, 2.1], ["p", 7.4, 3.4, 3.6, 2.1], ["p", 1, 6, 3.2, 2.4], ["p", 4.6, 6, 3.2, 2.4], ["t", 8.2, 6, 2.8, 1.2], ["j", 8.2, 7.4, 2.8, 1.6], ["e", 1, 9, 10, 2]], [["p", 1, 1, 3.1, 3.1], ["p", 4.45, 1, 3.1, 3.1], ["p", 7.9, 1, 3.1, 3.1], ["p", 1, 4.5, 4.8, 3.4], ["p", 6.2, 4.5, 4.8, 3.4], ["t", 1, 8.3, 10, 1.2], ["j", 1, 9.8, 7, 1.2], ["e", 8.4, 9.6, 2.6, 1.6]]],
      6: [[["p", 1, 1, 3.1, 3.6], ["p", 4.45, 1, 3.1, 3.6], ["p", 7.9, 1, 3.1, 3.6], ["p", 1, 5, 3.1, 3.6], ["p", 4.45, 5, 3.1, 3.6], ["p", 7.9, 5, 3.1, 3.6], ["t", 1, 9, 10, 1.2], ["j", 1, 10.4, 7, 0.8], ["e", 8.4, 10.2, 2.6, 1]], [["t", 1, 0.8, 7, 1.2], ["e", 8.4, 0.6, 2.6, 1.6], ["p", 1, 2.4, 4.8, 2.8], ["p", 6.2, 2.4, 4.8, 2.8], ["p", 1, 5.5, 4.8, 2.8], ["p", 6.2, 5.5, 4.8, 2.8], ["p", 1, 8.6, 4.8, 2.8], ["p", 6.2, 8.6, 4.8, 2.8]]]
    };
    var sbV = 0, sbS0 = store.get("pp-sbl", null) || {};
    ["p", "n", "m"].forEach(function (k) { if (sbS0[k] !== undefined && $("#sbl-" + k)) $("#sbl-" + k).value = sbS0[k]; });
    var sblRun = function () {
      var pv = $("#sbl-p").value.split("x"), W = parseFloat(pv[0]), H = parseFloat(pv[1]), n = parseInt($("#sbl-n").value, 10) || 3, m = parseFloat($("#sbl-m").value) || 0;
      var list = SBT[n] || SBT[3], tp = list[sbV % list.length], sx = W / 12, sy = H / 12, Z = 300 / Math.max(W, H);
      var q = function (v) { var r = Math.round(v * 8) / 8; return (r % 1 === 0 ? r.toFixed(0) : r.toFixed(3).replace(/0+$/, "")); };
      var frac = function (v) { var w = Math.floor(v + 1e-9), fr = Math.round((v - w) * 8), F = ["", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"]; if (fr === 8) { w++; fr = 0; } return (w ? w + (fr ? " " : "") : "") + (fr ? F[fr] : ""); };
      var g = '<svg viewBox="0 0 ' + (W * Z).toFixed(0) + " " + (H * Z).toFixed(0) + '" role="img" aria-label="Scrapbook page sketch" style="width:100%;max-width:420px;height:auto;display:block;margin:10px 0;border-radius:6px"><rect width="100%" height="100%" fill="#fbf8f1" stroke="#1f2a44" stroke-width="2"/>';
      var pn = 0, sizes = [];
      tp.forEach(function (it) {
        var x = it[1] * sx * Z, y = it[2] * sy * Z, w = it[3] * sx * Z, h = it[4] * sy * Z, ty = it[0];
        if (ty === "p") {
          pn++; var mm = m * Z;
          if (m > 0) g += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="#b8326a"/>';
          g += '<rect x="' + (x + mm).toFixed(1) + '" y="' + (y + mm).toFixed(1) + '" width="' + (w - 2 * mm).toFixed(1) + '" height="' + (h - 2 * mm).toFixed(1) + '" fill="' + (pn === 1 ? "#a9d2cc" : "#cfe3e0") + '" stroke="#1f2a44" stroke-width="1"/><text x="' + (x + w / 2).toFixed(1) + '" y="' + (y + h / 2 + 5).toFixed(1) + '" font-size="14" text-anchor="middle" fill="#1f2a44">' + pn + "</text>";
          var pw = it[3] * sx, ph = it[4] * sy; sizes.push([pn, pw, ph]);
        } else if (ty === "t") g += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" rx="3" fill="#f4dfb8"/><text x="' + (x + w / 2).toFixed(1) + '" y="' + (y + h / 2 + 5).toFixed(1) + '" font-family="Georgia,serif" font-size="14" text-anchor="middle" fill="#b8326a">Title</text>';
        else if (ty === "j") { g += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="#fff" stroke="#1f2a44" stroke-dasharray="3 3"/>'; for (var L = y + 8; L < y + h - 3; L += 7) g += '<path d="M' + (x + 5).toFixed(1) + " " + L.toFixed(1) + " h" + (w - 10).toFixed(1) + '" stroke="#9aa1ad" stroke-width="1"/>'; }
        else { var cx = x + w / 2, cy = y + h / 2, r = Math.min(w, h) / 5; g += '<circle cx="' + (cx - r * 1.3).toFixed(1) + '" cy="' + (cy + r * 0.6).toFixed(1) + '" r="' + r.toFixed(1) + '" fill="#e39a14"/><circle cx="' + (cx + r * 1.2).toFixed(1) + '" cy="' + (cy + r * 0.8).toFixed(1) + '" r="' + (r * 0.8).toFixed(1) + '" fill="#2f8f8a"/><circle cx="' + cx.toFixed(1) + '" cy="' + (cy - r * 0.9).toFixed(1) + '" r="' + (r * 0.7).toFixed(1) + '" fill="#e47aa3"/>'; }
      });
      g += "</svg>";
      var o = ['<p class="sub">' + W + " x " + H + " in page, " + n + " photo" + (n > 1 ? "s" : "") + ", sketch " + (sbV % list.length + 1) + " of " + list.length + "</p>", g];
      o.push('<table class="mt"><thead><tr><th>Photo</th><th>' + (m > 0 ? "Mat" : "Size") + "</th>" + (m > 0 ? "<th>Trim photo to</th>" : "") + "</tr></thead><tbody>" + sizes.map(function (s) { return "<tr><td>" + s[0] + (s[0] === 1 ? " (star)" : "") + "</td><td>" + frac(s[1]) + " x " + frac(s[2]) + " in</td>" + (m > 0 ? "<td>" + frac(s[1] - 2 * m) + " x " + frac(s[2] - 2 * m) + " in</td>" : "") + "</tr>"; }).join("") + "</tbody></table>");
      o.push('<p class="sub">Gold: title. Dashed box: journaling. Dots: a cluster of 3 embellishments. Photo 1 is the star; put your best photo there. Turn the sketch upside down or mirror it for a new look.</p><p><button type="button" class="btn ghost sm" onclick="window.print()">Print sketch</button></p>');
      $("#sbl-out").innerHTML = o.join("");
      store.set("pp-sbl", { p: $("#sbl-p").value, n: $("#sbl-n").value, m: $("#sbl-m").value });
    };
    ["p", "n", "m"].forEach(function (k) { $("#sbl-" + k).addEventListener("change", function () { sbV = 0; sblRun(); }); });
    $("#sbl-go").addEventListener("click", function () { sbV++; sblRun(); });
    sblRun();
  }

})();

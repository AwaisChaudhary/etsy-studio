/* Hero: full-width knitted fabric that knits itself row by row from the bottom. The rows still to knit show as a
   colour chart on graph paper. Pick a yarn and draw on the fabric to add colourwork. */
(function () {
  var cv = document.getElementById("swatch"); if (!cv || !window.Knit) return;
  var ctx = cv.getContext("2d"), K = window.Knit;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var COL = { c: "#f3eee6", b: "#b8326a", m: "#f4a823", t: "#2f8f8a", n: "#1f2a44" };
  var rowEl = document.getElementById("sw-row");
  var COLS, ROWS, W, H, w, h, dpr, sp, grid, done = 0, prog = 0, last = 0, running = true, visible = true, paint = "#b8326a", raf;

  /* colourwork bands, bottom to top, repeated to fill any size */
  var BANDS = ["t", "t", "t", "c", "cm", "c",
    "ccbccc", "cbbbcc", "bbbbbc", "cbbbcc", "ccbccc",
    "c", "mc", "c", "ctcc", "tttc", "ctcc", "c", "c", "b", "c",
    "ccbcccbccccc", "cbbbcbbbcccc", "cbbbbbbbcccc", "ccbbbbbccccc", "cccbbbcccccc", "ccccbccccccc", "c", "m", "c", "c",
    "nc", "c"];
  function motif() {
    var g = [], r, c;
    for (r = 0; r < ROWS; r++) {
      var pat = BANDS[r % BANDS.length], row = [], off = Math.floor((COLS % pat.length) / 2);
      for (c = 0; c < COLS; c++) row.push(COL[pat[(c + off) % pat.length]]);
      g.push(row);
    }
    return g;
  }
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    var target = W < 600 ? 22 : 30, oldCols = COLS;
    COLS = Math.max(14, Math.round(W / target)); w = W / COLS; h = w * 0.82; ROWS = Math.ceil(H / h) + 1;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    sp = new K.Sprites(w, h, dpr);
    if (!grid || oldCols !== COLS || grid.length !== ROWS) grid = motif();
    done = Math.min(done, ROWS); draw();
  }
  function cellY(r) { return H - (r + 1) * h; }
  function draw() {
    var r, c, y;
    ctx.fillStyle = "#f6f2ea"; ctx.fillRect(0, 0, W, H);
    for (r = done; r < ROWS; r++) {
      y = cellY(r); if (y + h < 0) break;
      for (c = (r === done ? Math.floor(prog) : 0); c < COLS; c++) {
        if (grid[r][c] === COL.c) continue;
        ctx.globalAlpha = 0.38; ctx.fillStyle = grid[r][c]; ctx.fillRect(c * w + 1, y + 1, w - 2, h - 2);
      }
    }
    ctx.globalAlpha = 1; ctx.strokeStyle = "rgba(47,143,138,0.2)"; ctx.lineWidth = 1; ctx.beginPath();
    for (c = 0; c <= COLS; c++) { ctx.moveTo(Math.round(c * w) + 0.5, 0); ctx.lineTo(Math.round(c * w) + 0.5, H); }
    for (r = 0; r <= ROWS; r++) { y = Math.round(cellY(r) + h) + 0.5; ctx.moveTo(0, y); ctx.lineTo(W, y); }
    ctx.stroke();
    var top = Math.min(ROWS, done + (prog > 0 ? 1 : 0));
    if (top > 0) { ctx.fillStyle = "#ddd5c6"; y = cellY(top - 1) - h * 0.25; ctx.fillRect(0, y, W, H - y); }
    for (r = top - 1; r >= 0; r--) {
      y = cellY(r); if (y > H + h) continue;
      var n = r < done ? COLS : Math.floor(prog);
      for (c = 0; c < n; c++) sp.draw(ctx, grid[r][c], c * w, y, K.hash(r, c) === 0 ? -0.06 : 0);
    }
    if (done < ROWS) {
      var ny = cellY(done) + h * 0.7, k = Math.floor(prog), tipX = Math.min(W - 6, k * w + w * 0.45), th = Math.max(5, w * 0.3);
      if (k > 0) {
        ctx.strokeStyle = grid[done][k - 1]; ctx.lineWidth = Math.max(2.5, w * 0.14); ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(tipX - w * 0.3, ny + h * 0.2); ctx.bezierCurveTo(tipX + w * 2, ny + h * 2.5, W - w * 2, ny - h * 3, W + 20, ny - h * 5); ctx.stroke();
      }
      var ng = ctx.createLinearGradient(0, ny - th, 0, ny + th); ng.addColorStop(0, "#ecd2ad"); ng.addColorStop(1, "#a97f52");
      ctx.fillStyle = ng; ctx.beginPath();
      ctx.moveTo(-10, ny - th / 2); ctx.lineTo(tipX - w * 0.7, ny - th / 2); ctx.lineTo(tipX + w * 0.55, ny); ctx.lineTo(tipX - w * 0.7, ny + th / 2); ctx.lineTo(-10, ny + th / 2); ctx.closePath(); ctx.fill();
    }
    if (rowEl) rowEl.textContent = done;
  }
  function loop(t) {
    if (!running || !visible) { last = 0; return; }
    if (!last) last = t; var dt = Math.min(64, t - last); last = t;
    prog += dt / (620 / COLS);
    if (prog >= COLS) { done++; prog = 0; if (done >= ROWS) { running = false; draw(); return; } }
    draw(); raf = requestAnimationFrame(loop);
  }
  function start() { cancelAnimationFrame(raf); last = 0; if (running && visible) raf = requestAnimationFrame(loop); }

  var painting = false;
  function at(e) {
    var b = cv.getBoundingClientRect(), x = e.clientX - b.left, y = e.clientY - b.top;
    var c = Math.floor(x / w), r = Math.floor((H - y) / h);
    if (c < 0 || c >= COLS || r < 0 || r >= ROWS) return;
    grid[r][c] = paint;
    if (!running || !visible) draw();
  }
  cv.addEventListener("pointerdown", function (e) { painting = true; try { cv.setPointerCapture(e.pointerId); } catch (x) {} at(e); });
  cv.addEventListener("pointermove", function (e) { if (painting) at(e); });
  ["pointerup", "pointercancel"].forEach(function (n) { cv.addEventListener(n, function () { painting = false; }); });
  Array.prototype.forEach.call(document.querySelectorAll(".yarn-btn"), function (b, i, all) {
    b.addEventListener("click", function () { paint = b.getAttribute("data-c"); Array.prototype.forEach.call(all, function (x) { x.setAttribute("aria-pressed", x === b); }); });
  });
  var reset = document.getElementById("sw-reset");
  if (reset) reset.addEventListener("click", function () {
    grid = motif();
    if (reduce) { done = ROWS; prog = 0; draw(); return; }
    done = 0; prog = 0; running = true; start();
  });
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) start(); }).observe(cv);
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(size, 120); });
  size();
  if (reduce) { done = ROWS; running = false; draw(); }
  else { done = Math.floor(ROWS * (W < 760 ? 0.3 : 0.45)); start(); }
})();

/* Shared stockinette renderer: pre-rendered stitch sprites drawn on canvas. Used by the hero and the gauge converter. */
window.Knit = (function () {
  function shade(hex, f) {
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    var m = function (v) { return Math.max(0, Math.min(255, Math.round(f > 0 ? v + (255 - v) * f : v * (1 + f)))); };
    return "rgb(" + m(r) + "," + m(g) + "," + m(b) + ")";
  }
  function Sprites(w, h, dpr) { this.w = w; this.h = h; this.dpr = dpr; this.c = {}; }
  Sprites.prototype.get = function (color, k) {
    var key = color + "|" + k; if (this.c[key]) return this.c[key];
    var w = this.w, h = this.h, dpr = this.dpr;
    var s = document.createElement("canvas"); s.width = Math.ceil(w * 1.15 * dpr); s.height = Math.ceil(h * 1.75 * dpr);
    var x = s.getContext("2d"); x.scale(dpr, dpr);
    var cx = w * 0.575, cy = h * 0.875;
    [-1, 1].forEach(function (side) {
      x.save(); x.translate(cx + side * w * 0.215, cy); x.rotate(side * 0.52);
      var gr = x.createLinearGradient(0, -h * 0.7, 0, h * 0.7);
      gr.addColorStop(0, shade(color, 0.3 + k)); gr.addColorStop(0.5, shade(color, k)); gr.addColorStop(1, shade(color, -0.32 + k));
      x.beginPath(); x.ellipse(0, 0, w * 0.245, h * 0.68, 0, 0, Math.PI * 2); x.fillStyle = gr; x.fill();
      x.lineWidth = 0.8; x.strokeStyle = "rgba(40,30,30,0.22)"; x.stroke();
      x.strokeStyle = "rgba(255,255,255,0.2)"; x.lineWidth = Math.max(0.5, w * 0.03);
      for (var i = -2; i <= 2; i++) { x.beginPath(); x.moveTo(-w * 0.15, h * (i * 0.2 - 0.25)); x.lineTo(w * 0.15, h * (i * 0.2 + 0.05)); x.stroke(); }
      x.restore();
    });
    this.c[key] = s; return s;
  };
  /* draw one stitch whose cell top-left is (x, y) */
  Sprites.prototype.draw = function (ctx, color, x, y, k) {
    ctx.drawImage(this.get(color, k || 0), x - this.w * 0.075, y - this.h * 0.375, this.w * 1.15, this.h * 1.75);
  };
  function hash(r, c) { return ((r * 73856093) ^ (c * 19349663)) & 3; }
  return { shade: shade, Sprites: Sprites, hash: hash };
})();

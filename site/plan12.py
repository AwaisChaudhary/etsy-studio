# ---------------- 27 Nov 2026 run 12: MACRAME KNOTS + JUNK JOURNAL PAGE IDEAS + HOW TO SLIP STITCH ----------------
# Executed from build.py after plan11.py (shares page(), top(), href(), e(), SHOP_FOR).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 12). Drawings our own SVG; wording our own. JS in assets/app.js (mkf-*, jpi-*, sls-*).

_T12 = 'font-family="Inter,sans-serif" font-size="12" fill="#1f2a44"'
_BG12 = '<rect width="280" height="200" rx="10" fill="#f6f1e6"/>'


def _svg12(body, label, vb="0 0 280 200"):
    return f'<svg viewBox="{vb}" role="img" aria-label="{e(label)}">{_BG12}{body}</svg>'


# ======== MACRAME KNOTS ========
# Demand: 'macrame knots for beginners', 'basic macrame knots', 'how to macrame' (SERP 27 Nov: Hobbii US+CA, Gathered, Marching North 17 knots,
# Bob Vila 7 knots, Sarah Maker, Hobbycraft projects, Twinkl, Hometalk x2, Gina Michele). Growth review E4 (macrame category). Wording ours.

_C_F, _C_A, _C_B = "#d9c59a", "#b8326a", "#2f8f8a"
_DOWEL = '<rect x="30" y="30" width="220" height="14" rx="7" fill="#a0703c" stroke="#1f2a44" stroke-width="1.6"/>'


def _cord(d, c, w=7):
    return f'<path d="{d}" fill="none" stroke="#1f2a44" stroke-width="{w + 2.4}" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def _bar(x, y, w, c, loop_left=True):
    lx = x - 6 if loop_left else x + w + 6
    return (_cord(f"M{x} {y} L{x + w} {y}", c, 8) +
            f'<circle cx="{lx}" cy="{y}" r="7" fill="none" stroke="#1f2a44" stroke-width="10.4"/><circle cx="{lx}" cy="{y}" r="7" fill="none" stroke="{c}" stroke-width="8"/>')


def _mk_svg(kind, label):
    if kind == "lark":
        s = (_cord("M126 180 L126 58 C126 18 154 18 154 58 L154 180", _C_A) + _DOWEL +
             _cord("M116 52 L164 52", _C_A, 9) + f'<text x="140" y="196" {_T12} text-anchor="middle">bar shows on the front</text>')
    elif kind == "rlark":
        s = (_cord("M126 180 L126 58 C126 18 154 18 154 58 L154 180", _C_B) + _DOWEL +
             '<path d="M118 52 L162 52" stroke="#1f2a44" stroke-width="2" stroke-dasharray="4 3"/>' + f'<text x="140" y="196" {_T12} text-anchor="middle">bar hidden at the back</text>')
    elif kind == "square":
        s = _cord("M128 14 L128 186", _C_F) + _cord("M152 14 L152 186", _C_F)
        for i, y in enumerate((50, 100, 150)):
            s += _cord(f"M100 {y - 34} L106 {y - 12}", _C_A) + _cord(f"M180 {y - 34} L174 {y - 12}", _C_B) if i == 0 else ""
            s += _bar(108, y - 9, 64, _C_A, True) + _bar(108, y + 9, 64, _C_B, False)
        s += _cord("M106 168 L100 190", _C_A) + _cord("M174 168 L180 190", _C_B) + f'<text x="236" y="104" {_T12} text-anchor="middle">bumps</text><text x="236" y="120" {_T12} text-anchor="middle">swap sides</text>'
    elif kind == "spiral":
        s = _cord("M140 14 L140 186", _C_F, 12)
        for i in range(7):
            y = 30 + i * 22
            s += f'<g transform="rotate({-14 + (i % 2) * 6} 140 {y})">' + _bar(112, y, 56, _C_A if i % 2 == 0 else _C_B, True) + '</g>'
        s += f'<text x="236" y="104" {_T12} text-anchor="middle">same side</text><text x="236" y="120" {_T12} text-anchor="middle">every time</text>'
    elif kind == "hh":
        s = (_cord("M30 110 L250 110", _C_F) + _cord("M140 14 L140 96", _C_A) +
             '<ellipse cx="140" cy="110" rx="12" ry="18" fill="none" stroke="#1f2a44" stroke-width="10.4"/><ellipse cx="140" cy="110" rx="12" ry="18" fill="none" stroke="#b8326a" stroke-width="8"/>' +
             _cord("M152 118 L156 186", _C_A) + f'<text x="60" y="96" {_T12}>holding cord</text><text x="168" y="60" {_T12}>working cord</text>')
    elif kind == "dhh":
        s = _cord("M24 92 L256 92", _C_F)
        for x in range(56, 240, 32):
            s += (_cord(f"M{x} 14 L{x} 78", _C_B) +
                  f'<ellipse cx="{x - 6}" cy="92" rx="7" ry="14" fill="none" stroke="#1f2a44" stroke-width="9.4"/><ellipse cx="{x - 6}" cy="92" rx="7" ry="14" fill="none" stroke="{_C_B}" stroke-width="7"/>'
                  f'<ellipse cx="{x + 6}" cy="92" rx="7" ry="14" fill="none" stroke="#1f2a44" stroke-width="9.4"/><ellipse cx="{x + 6}" cy="92" rx="7" ry="14" fill="none" stroke="{_C_B}" stroke-width="7"/>' +
                  _cord(f"M{x} 106 L{x} 186", _C_B))
        s += f'<text x="140" y="196" {_T12} text-anchor="middle">two loops per cord make a raised line</text>'
    elif kind == "diag":
        s = _cord("M30 30 L250 170", _C_F)
        for i, x in enumerate(range(70, 240, 34)):
            y = 30 + (x - 30) * 140 / 220
            s += (_cord(f"M{x} 14 L{x} {y - 16:.0f}", _C_A) +
                  f'<ellipse cx="{x}" cy="{y:.0f}" rx="10" ry="16" transform="rotate(-32 {x} {y:.0f})" fill="none" stroke="#1f2a44" stroke-width="9.4"/><ellipse cx="{x}" cy="{y:.0f}" rx="10" ry="16" transform="rotate(-32 {x} {y:.0f})" fill="none" stroke="{_C_A}" stroke-width="7"/>' +
                  _cord(f"M{x + 4} {y + 16:.0f} L{x + 4} 192", _C_A))
    elif kind == "gather":
        s = "".join(_cord(f"M{x} 10 L{x} 190", _C_F, 6) for x in range(118, 166, 10))
        for y in range(76, 136, 12):
            s += _cord(f"M108 {y} L172 {y}", _C_B, 9)
        s += _cord("M172 70 L188 30", _C_B) + _cord("M108 140 L96 186", _C_B) + f'<text x="214" y="34" {_T12}>pull</text><text x="40" y="186" {_T12}>trim</text>'
    elif kind == "over":
        s = _cord("M100 14 L120 80 C140 132 196 110 176 82 C156 56 116 96 132 124 L150 186", _C_A) + f'<text x="140" y="196" {_T12} text-anchor="middle">loop, tuck the end through, pull</text>'
    else:  # berry: square knot sinnet rolled up
        s = _cord("M128 14 L128 60", _C_F) + _cord("M152 14 L152 60", _C_F) + '<ellipse cx="140" cy="104" rx="46" ry="40" fill="#f4c6d4" stroke="#1f2a44" stroke-width="2.4"/>'
        s += "".join(f'<path d="M{100 + i * 10} {80 + (i % 2) * 6} q10 -6 20 0" fill="none" stroke="#b8326a" stroke-width="3"/>' for i in range(6))
        s += _cord("M128 148 L124 188", _C_F) + _cord("M152 148 L156 188", _C_F) + _cord("M98 130 L84 186", _C_A) + _cord("M182 130 L196 186", _C_B)
    return _svg12(s, label)


MK_KNOTS = [
    ("lark", "Lark's head knot", "Mounts a folded cord onto a dowel or ring. Fold the cord in half, lay the loop over the dowel, pull the two ends through the loop."),
    ("rlark", "Reverse lark's head", "The same mount made from the back, so only two neat bumps show. Most wall hangings start with this one."),
    ("square", "Square knot", "The main macrame knot. Two working cords tie round two filler cords: left over, right under, then the mirror image."),
    ("spiral", "Half knot spiral", "Only the first half of a square knot, repeated. The sinnet twists by itself, so let it turn as you go."),
    ("hh", "Half hitch", "A working cord loops once round a holding cord. Repeat on the same cord for a twisted chain."),
    ("dhh", "Double half hitch (clove hitch)", "Two half hitches in a row round a horizontal holding cord. Lines up into a raised bar across the piece."),
    ("diag", "Diagonal double half hitch", "The same knot with the holding cord held at a slant. Used for zigzags, leaves and V shapes."),
    ("gather", "Gathering (wrapping) knot", "Wraps a bundle of cords together. Finishes plant hangers and tassels and hides the ends inside."),
    ("over", "Overhand knot", "The simple knot everyone knows. Stops fringe from fraying and ties beads in place."),
    ("berry", "Berry knot", "A few square knots pulled up into a ball. A cute bobble for wall hangings and Christmas decorations."),
]
mk_cards = "".join(f'<figure class="gq-fig" id="knot-{k}"><div>{_mk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in MK_KNOTS)

mkp = top("Macrame knots for beginners", "The ten basic macrame knots, each drawn so you can see where the cords go, with plain step-by-step instructions. Then tell the project finder what you want to make and it lists the knots you need, in order, with the cord to buy and how long to cut it.", "Macrame knots") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> start with <strong>four knots</strong>. The <strong>lark's head</strong> (or reverse lark's head) mounts cords on a dowel or ring; the <strong>square knot</strong> is the knot most patterns are built from; the <strong>half knot spiral</strong> is half a square knot repeated; and the <strong>double half hitch</strong> makes straight or diagonal lines. Add the <strong>gathering knot</strong> to finish a plant hanger and the <strong>overhand knot</strong> for fringe and beads, and you can make most beginner patterns. Practise on 4 mm (about 3/16 in) single-strand or 3-ply cotton cord: it's soft, easy to undo and shows the knots clearly.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Macrame project finder</h3>
<div class="field"><label for="mkf-p">What do you want to make?</label><select id="mkf-p">
<option value="hanger">Plant hanger</option><option value="wall">Small wall hanging</option><option value="key">Keychain</option><option value="brace">Bracelet</option>
<option value="coaster">Coasters</option><option value="feather">Macrame feather or leaf</option><option value="star">Christmas star or tree ornament</option><option value="runner">Table runner</option></select></div>
<div class="row2"><div class="field"><label for="mkf-l">Finished length (without fringe)</label><input type="number" id="mkf-l" value="30" min="1" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><span class="label" id="mkf-u-l">Units</span><div class="seg" role="group" aria-labelledby="mkf-u-l" id="mkf-u"><button type="button" data-v="in" aria-pressed="true">Inches</button><button type="button" data-v="cm" aria-pressed="false">Centimetres</button></div></div></div>
<p class="sub">Cut lengths are rules of thumb for beginner patterns: if your pattern gives lengths, use those. For a full cord count for your dowel, use the <a href="{href("macrame-cord-calculator.html")}">macrame cord calculator</a>.</p>
</div><div class="result" aria-live="polite" id="mkf-out" data-cc="{href("macrame-cord-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>The 10 basic macrame knots</h2>
<p>Pink and green are the <strong>working cords</strong> (the ones you tie with). Tan is the <strong>filler</strong> or <strong>holding</strong> cord that the knot goes round.</p>
<div class="gq-figs">{mk_cards}</div>
<h2 id="lark">How to tie a lark's head knot</h2>
<ol><li>Fold a cord in half to make a loop at the middle.</li>
<li>Lay the loop over the front of the dowel (or ring) and fold it down behind.</li>
<li>Pull both cord ends through the loop from front to back, then pull them down to tighten.</li></ol>
<p>For a <strong>reverse lark's head</strong>, lay the loop over the back of the dowel and fold it down in front, then pull the ends through. The bar sits behind, so the front looks like two neat bumps. Both use the same amount of cord.</p>
<h2 id="square">How to tie a square knot</h2>
<p>You need four cords: an outer cord on each side (the working cords) and two in the middle (the fillers). Pull the fillers straight and keep a little tension on them.</p>
<ol><li><strong>Left over:</strong> take the left cord across the front of the fillers, making a shape like the number 4.</li>
<li><strong>Right over, under, through:</strong> lay the right cord over the left cord's tail, take it behind the fillers and bring it up through the loop on the left. Pull both working cords out to the sides to tighten. That's a half knot.</li>
<li><strong>Mirror it:</strong> now take the right cord across the front of the fillers (a backwards 4), lay the left cord over its tail, go behind the fillers and up through the loop on the right. Tighten.</li></ol>
<p>Done right, the bump (the little loop at the side) sits on the side you started from. If your sinnet starts twisting, you've tied the same half twice: start the next knot from the other side. A row of square knots that move across by two cords on every row is called <strong>alternating square knots</strong>, the net look on most wall hangings.</p>
<h2 id="spiral">How to make a half knot spiral</h2>
<p>Tie the first half of a square knot and then repeat it, always starting from the same side. After four to six knots the sinnet starts to turn. Let it: flip the working cords over each other as they swap sides and keep going. Starting from the left twists one way and starting from the right twists the other way, so keep to one side for a whole spiral.</p>
<h2 id="hitch">How to tie half hitches and double half hitches</h2>
<ol><li>Hold one cord (the holding cord) straight across the other cords, left to right, a little below where you want the line.</li>
<li>Take the first cord under it, bring it up over the holding cord and down through the loop it made. That's a half hitch.</li>
<li>Do it again with the same cord, to the right of the first loop. Two half hitches make a double half hitch.</li>
<li>Move to the next cord and repeat all the way across. Keep the holding cord tight and push each knot up close to the last.</li></ol>
<p>For a <strong>diagonal</strong> line, hold the holding cord at a slant instead of straight. To go back the other way, use the last cord as the new holding cord and tie right to left.</p>
<h2 id="gather">How to tie a gathering knot</h2>
<ol><li>Cut a separate cord about 3 ft (90 cm) long. Make a U shape with it and lay it along the bundle, loop pointing down, one short end sticking up.</li>
<li>Wrap the long end round the bundle and the U from the top down, tight and neat, 6 to 10 times.</li>
<li>Push the end of the wrapping cord through the loop at the bottom.</li>
<li>Pull the short end at the top until the loop and end disappear under the wraps. Trim both ends close and tuck them in.</li></ol>
<h2>Which cord to use</h2>
<ul><li><strong>Single-strand (single twist) cotton:</strong> soft, combs out into a fluffy fringe, best for wall hangings and feathers. Easy on the hands.</li>
<li><strong>3-ply cotton rope:</strong> stronger and more forgiving, the best choice for plant hangers that hold weight. Unravels into wavy fringe.</li>
<li><strong>Braided cord:</strong> doesn't fray and keeps its shape. Good for keychains and outdoor pieces, but the knots are harder to undo.</li>
<li><strong>Thickness:</strong> 3 mm for keychains, ornaments and coasters, 4 to 5 mm for most wall hangings and plant hangers, 6 mm and up for big statement pieces.</li></ul>
<h2>Tips for neat knots</h2>
<ul><li><strong>Hang your work at eye height:</strong> a dowel hung from a clothes rail, a door handle or an S hook makes tying much easier than working flat.</li>
<li><strong>Same tension every time:</strong> pull each knot to the same tightness. Loose and tight knots side by side are the main thing that makes macrame look uneven.</li>
<li><strong>Measure the gaps:</strong> leave the same space between rows. A ruler or a strip of card cut to the gap helps.</li>
<li><strong>Cut long:</strong> running out of cord halfway is the classic beginner mistake. Cut a test cord first and see how much a few knots use.</li>
<li><strong>Tape the ends</strong> of 3-ply cord while you work so it doesn't unravel before you want the fringe.</li></ul>
<h2>Selling macrame</h2>
<p>Plant hangers, wall hangings and keychains all sell well at craft fairs and online. Work out a fair price with the <a href="{href("craft-fair-profit-calculator.html")}">craft fair profit calculator</a> and check Etsy fees with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>. More fibre crafts: <a href="{href("punch-needle.html")}">punch needle</a>, <a href="{href("loom-knitting.html")}">loom knitting</a> and <a href="{href("friendship-bracelet-patterns.html")}">friendship bracelets</a>.</p>
</div></div></section>'''
mk_faq = [
    ("What are the basic macrame knots?", "The lark's head and reverse lark's head (to mount cords), the square knot, the half knot spiral, the half hitch and double half hitch, the gathering knot and the overhand knot."),
    ("What is the easiest macrame knot for beginners?", "The lark's head is the easiest and comes first in almost every project. The square knot is the one to practise next, because most patterns are built from it."),
    ("How do you tie a macrame square knot?", "Take the left cord over the fillers in a 4 shape, the right cord over it, behind the fillers and up through the loop. Then do the mirror image starting from the right."),
    ("Why is my macrame square knot twisting?", "You're tying the same half knot twice. Alternate the side you start from on every half knot. A twist on purpose is called a half knot spiral."),
    ("What size macrame cord is best for beginners?", "4 mm single-strand or 3-ply cotton cord. It's thick enough to see the knots, soft on the hands and easy to undo when you make a mistake."),
    ("What is the difference between a lark's head and a reverse lark's head?", "They're the same knot from opposite sides. The lark's head shows a bar across the front; the reverse lark's head hides it at the back and shows two bumps."),
]
SHOP_FOR["macrame-knots.html"] = ["small-business-pricing-inventory-spreadsheet", "christmas-gift-planner-budget", "2027-habit-tracker-spreadsheet", "christmas-gift-tags"]
page("macrame-knots.html", "Macrame Knots for Beginners: 10 Basic Knots Step by Step",
     "Macrame knots for beginners: the 10 basic knots drawn step by step, plus a project finder that lists the knots, cord size and cut lengths for your project.",
     mkp, mk_faq, "Macrame knots", app_name="Macrame project and knot finder")


# ======== JUNK JOURNAL PAGE IDEAS ========
# Demand: 'junk journal page ideas', 'junk journal ideas', 'junk journal spread ideas' (SERP 27 Nov: CBC artist ideas, Passion Planner, 101 Planners,
# Archer & Olive US+AU, Book Riot, Lemon8 x8, Organized Mom). Autocomplete 'junk journal' #7 (R5). Wording and ideas ours.

def _jl_svg(kind, label):
    sp = '<rect x="20" y="24" width="118" height="152" rx="3" fill="#efe6d2" stroke="#9aa6c4" stroke-width="2"/><rect x="142" y="24" width="118" height="152" rx="3" fill="#efe6d2" stroke="#9aa6c4" stroke-width="2"/><line x1="140" y1="22" x2="140" y2="178" stroke="#1f2a44" stroke-width="2"/>'
    r = lambda x, y, w, h, c, rot=0: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{c}" stroke="#1f2a44" stroke-width="1.4"' + (f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else "") + '/>'
    if kind == "collage":
        s = sp + r(28, 34, 70, 90, "#f4c6d4", -4) + r(60, 96, 70, 64, "#dbe9e8", 5) + r(150, 40, 96, 56, "#e8d3a6", 3) + r(160, 104, 60, 60, "#fff", -6) + '<circle cx="110" cy="60" r="16" fill="#e39a14" stroke="#1f2a44" stroke-width="1.4"/>'
    elif kind == "grid":
        s = sp + "".join(r(28 + (i % 3) * 36, 36 + (i // 3) * 46, 30, 40, ("#f4c6d4", "#dbe9e8", "#e8d3a6")[i % 3]) for i in range(9)) + r(152, 36, 98, 128, "#fff") + "".join(f'<line x1="162" y1="{y}" x2="240" y2="{y}" stroke="#9aa6c4" stroke-width="1.4"/>' for y in range(56, 160, 14))
    elif kind == "tuck":
        s = sp + r(36, 44, 50, 80, "#e8d3a6", -6) + r(28, 100, 102, 66, "#f4c6d4") + '<path d="M176 30 L176 70" stroke="#b8326a" stroke-width="2"/>' + r(160, 64, 40, 70, "#e8d3a6", 4) + '<circle cx="180" cy="74" r="3.5" fill="#fff" stroke="#1f2a44"/>' + r(150, 120, 104, 46, "#dbe9e8")
    elif kind == "focal":
        s = sp + r(34, 40, 90, 120, "#fff") + r(42, 48, 74, 80, "#dbe9e8") + '<path d="M50 120 L72 90 L90 110 L104 96 L114 120 Z" fill="#2f8f8a"/>' + "".join(r(158 + i * 20, 46 + i * 22, 44, 70, "#e8d3a6", -10 + i * 10) for i in range(3))
    elif kind == "map":
        s = sp + '<path d="M30 60 C60 30 100 90 130 50 M150 70 C180 40 210 110 250 80" fill="none" stroke="#9aa6c4" stroke-width="2"/><path d="M40 150 C70 120 90 160 120 120 C150 80 190 150 240 110" fill="none" stroke="#b8326a" stroke-width="2.4" stroke-dasharray="6 4"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#e39a14" stroke="#1f2a44" stroke-width="1.4"/>' for x, y in ((40, 150), (120, 120), (240, 110))) + r(160, 36, 60, 40, "#fff", 4)
    else:  # flip
        s = sp + r(30, 40, 98, 120, "#f4c6d4") + r(46, 70, 66, 60, "#efe6d2") + '<path d="M142 40 L230 30 L238 150 L142 160 Z" fill="#dbe9e8" stroke="#1f2a44" stroke-width="1.6"/><path d="M228 90 C250 80 256 100 246 112" fill="none" stroke="#e39a14" stroke-width="2.4"/>'
    return _svg12(s, label)


JL_LAYOUTS = [("collage", "Layered collage", "Three or four papers overlapping at slight angles, one bright focal circle. The look most people picture."),
              ("grid", "Grid and journaling", "A grid of small squares (stamps, swatches, tickets) on one side and lined journaling on the other."),
              ("tuck", "Tuck spot spread", "A pocket and a tag on each page. Hidden journaling goes on the tags."),
              ("focal", "Big focal and tag fan", "One large picture framed on the left, three tags fanned out on the right."),
              ("map", "Journey map", "A dashed path across both pages with dots for places, dates or milestones."),
              ("flip", "Flip-out page", "A glued-in flap that opens past the edge of the book to show a hidden layer.")]
jl_cards = "".join(f'<figure class="gq-fig"><div>{_jl_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in JL_LAYOUTS)

JI_IDEAS = [
    ("Memories", [("Ticket stub timeline", "Glue down tickets from a year in date order and write one line under each."),
                  ("A day in my life", "Times down the side, one small sketch or note for each hour."),
                  ("Then and now", "An old photo and a new one side by side, with what changed."),
                  ("Recipe page", "A family recipe in the cook's handwriting, a splash of tea stain and a fold-out for the story."),
                  ("Letter to future me", "Seal it in an envelope pocket with an open-on date."),
                  ("Favourite things list", "Book, song, smell, place, food: one tag each.")]),
    ("Seasons and holidays", [("Winter window", "A paper window frame with snowflakes behind it and a cosy list on the sill."),
                              ("Christmas card wall", "Cut fronts from last year's cards into a grid. Add who sent each one."),
                              ("Advent pocket page", "24 tiny tags in pockets, one line written each December day."),
                              ("New Year word", "Your word for the year in big letters cut from magazines, with three ways to live it."),
                              ("Spring seed packet page", "Old seed packets as pockets for garden notes."),
                              ("Summer postcard", "Make your own postcard from a scrap of card and write it to a friend you miss.")]),
    ("Nature", [("Pressed leaf page", "Flatten leaves in a heavy book for a week, tape them down and label them."),
                ("Weather log", "One small square a day coloured for the weather, like a temperature blanket on paper."),
                ("Moon phases strip", "Eight circles shaded for the moon's phases down the edge."),
                ("Botanical label page", "Vintage-style labels with plant names, real or made up."),
                ("Bird watch tally", "A tally of birds seen from your window this month."),
                ("Tea-stained sky", "A tea-dyed page with a cut paper landscape at the bottom.")]),
    ("Collage and vintage", [("Old book page base", "A page from a damaged book as the background, words picked out with a highlighter."),
                             ("Envelope layers", "Three envelopes in different sizes stacked like steps, each one a pocket."),
                             ("Ephemera cluster", "One corner packed with labels, stamps and tickets, the rest left calm."),
                             ("Lace and doily page", "A doily or lace strip across the middle with a photo on top."),
                             ("Map background", "An old map or atlas page with a dashed line to somewhere you want to go."),
                             ("Stamp collection grid", "Real or printed postage stamps in a 3 x 3 grid.")]),
    ("Writing and prompts", [("Gratitude tags", "Three tags: a person, a thing and a moment you're glad of this week."),
                             ("Overheard quotes", "Funny or kind things people said, typed on strips like fortune cookie papers."),
                             ("Blackout poem", "Black out words on a book page until a short poem is left."),
                             ("Lists of five", "Five things you can see, hear, smell, touch and taste right now."),
                             ("Question of the month", "One question at the top, a different answer each week."),
                             ("Dream page", "Last night's dream written fast, before you forget it, with doodles.")]),
    ("Interactive pages", [("Pull-tab reveal", "A tab that slides out from behind a photo to show the date and story."),
                           ("Mini book inside", "A tiny folded zine glued in as a page within the page."),
                           ("Belly band bundle", "Cards held under a band so they come out like a deck."),
                           ("Waterfall cards", "Overlapping cards that drop down when you pull a tab."),
                           ("Envelope of extras", "A sealed envelope full of loose ephemera to use another day."),
                           ("Tea bag pocket", "A dried, emptied tea bag as a tiny see-through pocket.")]),
    ("Free from what's at home", [("Packaging prints", "Cut pretty bits from food boxes and tea packets."),
                                  ("Receipt poetry", "A long receipt trimmed into a strip with the shop's name as a title."),
                                  ("Junk mail collage", "Colours and words from flyers, sorted into a rainbow."),
                                  ("Paper bag page", "A flattened brown bag as the page, its fold as a pocket."),
                                  ("Coffee stain circles", "Ring stains from a mug as frames for tiny drawings."),
                                  ("Kids' art page", "A child's drawing trimmed and framed with washi tape.")]),
]
_ji_total = sum(len(v) for _, v in JI_IDEAS)
ji_html = "".join(f'<h3>{e(g)}</h3><ol>' + "".join(f'<li><strong>{e(n)}.</strong> {e(d)}</li>' for n, d in v) + '</ol>' for g, v in JI_IDEAS)


# run 15 merge (DEMAND N2 'christmas junk journal ideas'): Christmas H2 with our own printable templates.
def _xj_svg():
    tag = (f'<path d="M30 40 h70 l22 22 v76 h-92 z" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.6" stroke-dasharray="5 4"/><circle cx="100" cy="58" r="6" fill="none" stroke="#1f2a44" stroke-width="1.4"/>'
           f'<path d="M48 96 l14 -26 l14 26 z M58 96 h8 v8 h-8z" fill="#2f8f8a"/><text x="76" y="156" {_T12} text-anchor="middle">gift tag</text>')
    mit = (f'<path d="M150 50 c0 -14 34 -14 34 0 v20 c10 -10 22 -2 16 10 l-12 14 v44 h-38 z" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.6" stroke-dasharray="5 4"/>'
           f'<rect x="150" y="128" width="38" height="10" fill="#b8326a"/><text x="174" y="156" {_T12} text-anchor="middle">mitten pocket</text>')
    tk = (f'<rect x="208" y="70" width="60" height="34" rx="3" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.6" stroke-dasharray="5 4"/><circle cx="208" cy="87" r="5" fill="#f6f1e6"/><circle cx="268" cy="87" r="5" fill="#f6f1e6"/>'
          f'<text x="238" y="91" font-family="Inter,sans-serif" font-size="9" fill="#b8326a" text-anchor="middle">North Pole</text><text x="238" y="124" {_T12} text-anchor="middle">ticket</text>')
    return _svg12(tag + mit + tk, "Printable Christmas junk journal templates: a gift tag, a mitten-shaped pocket and a North Pole ticket")
XJ = [("Advent tag strip", "Number 24 small tags and add one line or a tiny find to each December day."),
      ("Mitten pocket", "Cut the mitten template from a festive paper, glue three sides and tuck a wish list inside."),
      ("Christmas card mosaic", "Trim the fronts of last year's cards into squares and grid them across a spread."),
      ("Recipe of the season", "Write out a family bake on a recipe card, with a pocket for the crumb-stained original."),
      ("Gift log", "A simple table: who, what, made or bought. Handy for next year too."),
      ("North Pole ticket", "A ticket for a Christmas outing, real or pretend, with the date and who came."),
      ("Wrapping paper background", "Flatten leftover wrapping paper or tissue as the base layer."),
      ("Ornament page", "Draw or cut paper baubles and write a memory in each one."),
      ("Twelve days list", "Twelve tags or flaps, one small joy per day from Christmas to Twelfth Night."),
      ("Winter walk", "Pressed holly or a pine sprig sealed under a strip of packing tape, with where you found it."),
      ("Letter to Santa", "A sealed envelope pocket with a letter, or a grown-up version: what you'd wish for this year."),
      ("Year in review", "A spread for the end of December: best moment, hardest moment, one word for next year.")]
_xj_html = ('<h2 id="christmas">Christmas junk journal ideas</h2><p>December is a lovely time to start a junk journal: there\'s paper everywhere, from cards to wrapping to food packaging. Here are twelve Christmas page ideas and three free templates to trace or print and cut out (our own designs; dashed lines are the cut lines). Print on card or kraft paper and scale the drawing to the size you want.</p>'
            f'<div class="gq-figs"><figure class="gq-fig"><div>{_xj_svg()}<figcaption><strong>Free templates.</strong> Gift tag, mitten pocket and a North Pole ticket. Print this page or tap and save the drawing.</figcaption></div></figure></div><ol>'
            + "".join(f'<li><strong>{e(n)}.</strong> {e(d)}</li>' for n, d in XJ) + '</ol>'
            '<p>Want 25 ready-made December pages? Our December Days kit below has a page for every day, and the <a href="' + href("journal-prompts.html") + '">prompt shuffler</a> has a winter theme.</p>')

jip = top("Junk journal page ideas", f"{_ji_total} junk journal page ideas sorted by theme, six spread layouts drawn out, and a spread generator that picks a background, a focal piece, something interactive, an embellishment and a prompt for you, so you never face a blank page again.", "Junk journal page ideas") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a junk journal page comes together in <strong>five layers</strong>: a <strong>background</strong> (book page, map, tea-stained paper, a flattened paper bag), a <strong>focal piece</strong> (a photo, a postcard, a big label), something <strong>interactive</strong> (a pocket, tag, flap or tuck spot), a few <strong>embellishments</strong> (washi, stamps, stitching, a button) and a few <strong>words</strong>. Pick one idea from each layer and the page is done. Stuck? Press the shuffle button below for a ready-made spread, or try one of the {_ji_total} ideas further down: memories, seasons, nature, vintage collage, writing prompts, interactive pages and pages made only from things you already have at home.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Junk journal spread generator</h3>
<div class="field"><label for="jpi-th">Theme</label><select id="jpi-th"><option value="any">Any</option><option value="winter">Winter and Christmas</option><option value="new">New Year</option><option value="nature">Nature</option><option value="vintage">Vintage</option><option value="memory">Memories</option><option value="free">Free, from what's at home</option></select></div>
<div class="btns"><button type="button" class="btn" id="jpi-go">Shuffle a spread</button></div>
<p class="sub">Tap a line in the result to change just that layer. Your last spread is kept on this device only.</p>
</div><div class="result" aria-live="polite" id="jpi-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Six junk journal spread layouts</h2>
<div class="gq-figs">{jl_cards}</div>
<h2>{_ji_total} junk journal page ideas</h2>
{ji_html}
{_xj_html}
<h2>How to start a junk journal page</h2>
<ol><li><strong>Choose a background first.</strong> It sets the colours for everything else, so pick it before anything gets glued.</li>
<li><strong>Lay it all out dry.</strong> Move pieces around before gluing. Take a quick photo when you like it, so you can put it back.</li>
<li><strong>Glue the biggest pieces first,</strong> then the smaller ones on top. Leave the edges of a few pieces loose to make tuck spots.</li>
<li><strong>Add one interactive piece:</strong> a <a href="{href("junk-journal-pockets.html")}">pocket</a>, a tag, a flap. It gives the page a reason to be picked up.</li>
<li><strong>Finish with words.</strong> A date, a quote, a few lines from a <a href="{href("journal-prompts.html")}">journal prompt</a>. It's what makes the page yours.</li></ol>
<h2>What if my page looks too busy?</h2>
<p>Leave one area empty, or cover it with a single calm paper. Stick to three main colours, and repeat each one at least twice across the spread so the eye moves round it. Odd numbers (three tags, five stamps) look more relaxed than pairs. If a page really isn't working, glue a plain sheet over the worst part and call it a new background: nobody else will know.</p>
<h2>Where to find things for your pages</h2>
<p>Most of it is free: envelopes, packaging, receipts, old books, tea bags. See our <a href="{href("junk-journal-ephemera-ideas.html")}">62 ephemera ideas</a> and the <a href="{href("junk-journal-supply-checklist.html")}">supply checklist</a>, give white paper an old look by <a href="{href("how-to-tea-stain-paper.html")}">tea staining it</a>, and work out pages and binding with the <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a>. New to all this? Start with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a>.</p>
</div></div></section>'''
ji_faq = [
    ("What do you put on a junk journal page?", "A background paper, one focal piece like a photo or postcard, something interactive like a pocket or tag, a few embellishments and a few words."),
    ("How do I fill my junk journal?", "Do one spread at a time: pick a background, lay everything out before gluing, add one pocket or tag, then write a date or a few lines. Don't try to fill every gap."),
    ("What should be on the first page of a junk journal?", "Something that says whose journal it is: your name, the year or a word for the journal, with a favourite photo or paper. Many people leave it until last."),
    ("How do you make a junk journal page look vintage?", "Tea-stain the paper, ink the edges with brown ink, and use old book pages, stamps, lace and labels. Keep the colours warm and muted."),
    ("Can you junk journal without buying supplies?", "Yes. Envelopes, food packaging, receipts, junk mail, paper bags, tea bags and old books are all free and make great pages."),
    ("What can I put in a Christmas junk journal?", "Christmas cards, wrapping paper, gift tags, receipts from presents, recipe cards, ticket stubs, pressed holly or pine, photos and a gift list. Most of it is free from the season."),
    ("How do you make a Christmas junk journal?", "Fold a few signatures from festive paper and old cards, bind them into a cover made from a cereal box or cardstock, then add a page or two each day of December."),
    ("How many pages should a junk journal have?", "Most handmade junk journals have 3 to 6 signatures of 4 to 6 folded sheets each. Make it smaller than you think: a thin finished journal beats a fat empty one."),
]
SHOP_FOR["junk-journal-page-ideas.html"] = ["december-days-journal-kit", "winter-cottage-junk-journal-kit", "junk-journal-mega-bundle", "journaling-cards-3x4"]
page("junk-journal-page-ideas.html", f"{_ji_total} Junk Journal Page Ideas + a Spread Generator",
     f"{_ji_total} junk journal page ideas by theme, six spread layouts drawn out, and a free generator that picks the background, focal piece, pocket and prompt.",
     jip, ji_faq, "Junk journal page ideas", app_name="Junk journal spread generator")


# ======== HOW TO SLIP STITCH IN CROCHET ========
# Demand: 'how to slip stitch crochet', 'slip stitch join', 'how to join a round in crochet' (SERP 27 Nov: LoveCrafts x3, The Woobles slip stitch
# join x2, Annie's, Gathered, One Little Project, A Crocheted Simplicity special join, Dummies crochet in the round, Simply Crochet). Wording ours.

def _sl_svg(step, label):
    hook = lambda x, y, rot: (f'<g transform="rotate({rot} {x} {y})"><rect x="{x}" y="{y - 4}" width="120" height="8" rx="4" fill="#9aa6c4" stroke="#1f2a44" stroke-width="1.4"/>'
                              f'<path d="M{x} {y - 4} q-12 0 -12 8 q0 6 8 6" fill="none" stroke="#1f2a44" stroke-width="3"/></g>')
    sts = "".join(f'<ellipse cx="{x}" cy="150" rx="15" ry="9" fill="none" stroke="#2f8f8a" stroke-width="4"/>' for x in range(50, 250, 32))
    if step == 1:
        s = sts + hook(140, 146, -18) + '<ellipse cx="160" cy="132" rx="9" ry="13" fill="none" stroke="#b8326a" stroke-width="4"/>' + f'<text x="140" y="40" {_T12} text-anchor="middle">hook under both loops of the next stitch</text>'
    elif step == 2:
        s = sts + hook(140, 146, -18) + '<ellipse cx="160" cy="132" rx="9" ry="13" fill="none" stroke="#b8326a" stroke-width="4"/><path d="M128 146 C120 120 150 104 176 92 L250 70" fill="none" stroke="#b8326a" stroke-width="4"/>' + f'<text x="140" y="40" {_T12} text-anchor="middle">yarn over the hook</text>'
    elif step == 3:
        s = sts + hook(140, 118, -6) + '<ellipse cx="146" cy="120" rx="9" ry="13" fill="none" stroke="#b8326a" stroke-width="4"/><path d="M146 107 L250 80" fill="none" stroke="#b8326a" stroke-width="4"/><path d="M130 144 L136 128" stroke="#e39a14" stroke-width="2.6"/><path d="M130 132 L136 126 L140 134" fill="none" stroke="#e39a14" stroke-width="2.6"/>' + f'<text x="140" y="40" {_T12} text-anchor="middle">pull through the stitch and the loop in one go</text>'
    else:  # join round
        dots = ""
        for i in range(12):
            dots += f'<g transform="rotate({i * 30} 140 108)"><line x1="140" y1="56" x2="140" y2="34" stroke="#2f8f8a" stroke-width="3"/><line x1="134" y1="34" x2="146" y2="34" stroke="#2f8f8a" stroke-width="3"/><line x1="135" y1="47" x2="145" y2="43" stroke="#2f8f8a" stroke-width="2"/></g>'
        s = ('<circle cx="140" cy="108" r="22" fill="none" stroke="#9aa6c4" stroke-width="3"/>' + dots +
             '<circle cx="152" cy="30" r="5" fill="#b8326a"/><path d="M168 22 C190 12 206 24 200 40" fill="none" stroke="#b8326a" stroke-width="2"/>' +
             f'<text x="210" y="56" {_T12}>sl st (dot)</text>')
    return _svg12(s, label)


SL_STEPS = [(1, "1. Insert the hook", "Put the hook into the next stitch, under both top loops, with one loop already on the hook."),
            (2, "2. Yarn over", "Wrap the yarn over the hook from back to front, the same as for any stitch."),
            (3, "3. Pull through both", "Pull the yarn through the stitch and straight through the loop on the hook. One loop left: done."),
            (4, "Joining a round", "In charts the slip stitch is a small filled dot. It joins the last stitch of a round to the first.")]
sl_cards = "".join(f'<figure class="gq-fig"><div>{_sl_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in SL_STEPS)

slp = top("How to slip stitch in crochet", "The slip stitch is the smallest crochet stitch and the one that holds everything together: it joins rounds, moves the yarn along without adding height, sews seams and makes neat edges. Here it is in three drawn steps, then a round writer that tells you exactly how to start and join a round for your stitch.", "How to slip stitch in crochet") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to slip stitch (<strong>sl st</strong>, called <strong>ss</strong> or slip stitch in UK patterns too), <strong>insert the hook</strong> into the next stitch, <strong>yarn over</strong> and <strong>pull the loop through the stitch and the loop on the hook</strong> in one movement. It adds almost no height. To <strong>join a round</strong>, slip stitch into the top of the first stitch of the round (or into the top of the starting chain if that chain counts as a stitch), then chain up for the next round. Keep slip stitches loose: they're the easiest stitch to make too tight.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Joined round writer</h3>
<div class="row2"><div class="field"><label for="sls-st">Stitch in the round</label><select id="sls-st"><option value="sc">Single crochet</option><option value="hdc">Half double crochet</option><option value="dc" selected>Double crochet</option><option value="tr">Treble crochet</option></select></div>
<div class="field"><label for="sls-n">Stitches in the round</label><input type="number" id="sls-n" value="12" min="3" max="400" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="sls-ch">Starting chain</label><select id="sls-ch"><option value="auto">Usual for this stitch</option><option value="yes">Counts as a stitch</option><option value="no">Doesn't count</option></select></div>
<div class="field"><label for="sls-x">Extras</label><select id="sls-x"><option value="none">None</option><option value="colour">Change colour at the join</option><option value="last">This is the last round (invisible join)</option></select></div></div>
<div class="field"><span class="label" id="sls-t-l">Terms</span><div class="seg" role="group" aria-labelledby="sls-t-l" id="sls-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
</div><div class="result" aria-live="polite" id="sls-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to slip stitch, step by step</h2>
<div class="gq-figs">{sl_cards}</div>
<p>Start with a loop on the hook (a slip knot and a chain, or the last stitch you made). Insert the hook into the stitch, yarn over, and pull the new loop through the stitch and the loop on the hook together. Unlike a <a href="{href("basic-crochet-stitches.html")}">single crochet</a>, there's no second yarn over: that's why it's so flat.</p>
<h2>How to join a round with a slip stitch</h2>
<ol><li>Finish the last stitch of the round.</li>
<li>Find the first stitch of the round. If the round started with a chain that <strong>counts</strong> as a stitch (ch 3 for double crochet, usually), the join goes into the <strong>top chain</strong> of that ch 3. If the chain <strong>doesn't count</strong>, the join goes into the top of the first real stitch.</li>
<li>Insert the hook under both loops there, yarn over and pull through everything on the hook.</li>
<li>Chain up for the next round. A stitch marker in the first stitch of each round makes the join easy to find.</li></ol>
<p>A <strong>seam</strong> of joins appears where the rounds meet. It leans a little each round; turning your work after each join (joined and turned rounds) keeps it straighter.</p>
<h2>Joined rounds or spiral?</h2>
<p>Joined rounds give a clean colour change and a flat, even circle, which is what you want for coasters, rugs, granny squares and mandalas. Working in a <strong>spiral</strong> (no slip stitch, no chain, just keep going) is seamless, so it's the usual choice for <a href="{href("amigurumi.html")}">amigurumi</a>. Mark the first stitch of each spiral round, because there's no join to show where it starts. Both start the same way, usually with a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>.</p>
<h2>Other ways to use the slip stitch</h2>
<ul><li><strong>Move without adding height:</strong> slip stitch across stitches to get to the next chain space, as at the start of a <a href="{href("how-to-crochet-a-granny-square.html")}">granny square</a> round.</li>
<li><strong>Seams:</strong> hold two pieces together and slip stitch through both edges. Flat and firm; see <a href="{href("how-to-join-granny-squares.html")}">how to join granny squares</a>.</li>
<li><strong>Edging:</strong> a round of slip stitches round a finished piece tidies wobbly edges.</li>
<li><strong>Surface slip stitch:</strong> hold the yarn behind the fabric and slip stitch through it from the front, like drawing on the piece. Used for lines, plaid and lettering.</li>
<li><strong>Slip stitch ribbing:</strong> rows of slip stitches worked in the back loop only make a stretchy rib for hat brims and cuffs.</li>
<li><strong>Close a chain into a ring:</strong> chain a few, then slip stitch into the first chain.</li></ul>
<h2>Common slip stitch problems</h2>
<ul><li><strong>Too tight to work into:</strong> pull up the loop a little taller before you finish, or go up a hook size for slip stitch rows only.</li>
<li><strong>Stitch count grows every round:</strong> you're working a stitch into the slip stitch of the join. Skip it: the join isn't a stitch.</li>
<li><strong>Stitch count shrinks:</strong> the starting chain counts, but you skipped it at the join, or you joined into the second stitch.</li>
<li><strong>A gap or a lump at the join:</strong> join into the very top of the chain, not the side, and try the invisible join on the last round.</li></ul>
<p>Not sure what a pattern means by sl st, ss or "join"? See the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a> and <a href="{href("how-to-read-crochet-patterns.html")}">how to read crochet patterns</a>.</p>
</div></div></section>'''
sl_faq = [
    ("How do you slip stitch in crochet?", "Insert the hook into the next stitch, yarn over, and pull the loop through the stitch and the loop on the hook in one movement."),
    ("Is a slip stitch the same in US and UK crochet?", "Yes, it's the same stitch. US patterns write sl st; UK patterns often write ss or sl st. Only the taller stitch names differ."),
    ("Where do you slip stitch to join a round?", "Into the top of the first stitch of the round, or into the top chain of the starting chain if that chain counts as a stitch."),
    ("Does the slip stitch count as a stitch?", "No. The slip stitch used to join a round is never counted, and you don't work into it on the next round."),
    ("Why does my circle get bigger every round?", "You're probably working into the slip stitch join or into a starting chain that doesn't count. Use a marker in the first stitch of each round."),
    ("Should I join rounds or work in a spiral?", "Join for flat pieces and stripes, like coasters and granny squares. Work in a spiral for amigurumi, where a visible seam would show."),
]
SHOP_FOR["how-to-slip-stitch-crochet.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-slip-stitch-crochet.html", "How to Slip Stitch in Crochet (+ Joining Rounds)",
     "How to slip stitch in crochet in three drawn steps, plus how to join a round, spiral vs joined rounds, and a writer for starting and joining rounds.",
     slp, sl_faq, "How to slip stitch in crochet", app_name="Crochet joined round writer")

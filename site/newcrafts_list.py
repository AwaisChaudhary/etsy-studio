# Round-2 craft list + hub block (exec'd in crafts.py right after CRAFTS).
NEW_CRAFTS = [
 ("christmas-crafts.html", "Christmas crafts + printable gift tags", "Paper and yarn Christmas makes, plus free printable gift tags."),
 ("advent-calendar-ideas.html", "Advent calendar ideas + number cards", "48 small fillers and free printable 1-24 number cards."),
 ("coloring-pages.html", "Coloring pages generator", "Endless printable mandalas and pattern pages, never the same twice."),
 ("amigurumi.html", "Amigurumi ball pattern calculator", "Round-by-round pattern for a crochet ball of any size."),
 ("bookbinding.html", "Bookbinding hole template", "Sewing station positions and a printable punching guide."),
 ("origami.html", "Printable origami paper", "Patterned origami squares to print, plus beginner folds."),
 ("card-making.html", "Card and envelope size calculator", "Card sizes, matching envelopes and cuts per sheet of cardstock."),
 ("paper-flowers.html", "Paper flower petal templates", "Printable petal templates in graduated sizes."),
 ("punch-needle.html", "Punch needle fabric calculator", "How much fabric to cut and what frame size you need."),
 ("tunisian-crochet.html", "Tunisian crochet calculator", "Stitches to pick up, rows to work and which hook to use."),
 ("loom-knitting.html", "Loom knitting hat size guide", "Which round loom to use for any head size."),
 ("needle-felting.html", "Needle felting needle guide", "Which felting needle gauge to use at each stage."),
 ("tufting.html", "Tufting rug planner", "Tufting cloth cut size and frame size for any rug."),
 ("friendship-bracelet-patterns.html", "Friendship bracelet pattern maker", "Chevron and diagonal stripe patterns in your colours."),
 ("embroidery-patterns.html", "Embroidery pattern generator", "Printable floral hoop patterns to trace, any hoop size."),
 ("embroidery-stitches.html", "Embroidery stitches for beginners", "12 basic hand embroidery stitches with step diagrams."),
 ("scrapbook-page-sizes.html", "Scrapbook page sizes + photo layout", "Every page size and how many photos fit on it."),
]
CRAFTS.extend(NEW_CRAFTS)
NEW_HUB = '''<h2>Seasonal</h2><ul><li><a href="{H:christmas-crafts.html}">Christmas crafts</a>: paper and yarn makes, plus printable gift tags.</li><li><a href="{H:advent-calendar-ideas.html}">Advent calendar ideas</a>: fillers and printable 1-24 number cards.</li><li><a href="{H:2027-calendar-printable.html}">2027 calendar printable</a>.</li></ul>
<h2>More paper crafts</h2><ul><li><a href="{H:scrapbook-page-sizes.html}">Scrapbook page sizes</a>: every size and how many photos fit.</li><li><a href="{H:coloring-pages.html}">Coloring pages</a>: endless mandalas and patterns.</li><li><a href="{H:origami.html}">Origami paper</a> and beginner folds.</li><li><a href="{H:card-making.html}">Card and envelope sizes</a>.</li><li><a href="{H:paper-flowers.html}">Paper flower templates</a>.</li><li><a href="{H:bookbinding.html}">Bookbinding hole template</a> and stitch guide.</li></ul>
<h2>More yarn and fibre crafts</h2><ul><li><a href="{H:amigurumi.html}">Amigurumi ball calculator</a>.</li><li><a href="{H:tunisian-crochet.html}">Tunisian crochet calculator</a>.</li><li><a href="{H:loom-knitting.html}">Loom knitting hat sizes</a>.</li><li><a href="{H:punch-needle.html}">Punch needle fabric calculator</a>.</li><li><a href="{H:tufting.html}">Tufting rug planner</a>.</li><li><a href="{H:needle-felting.html}">Needle felting needle guide</a>.</li><li><a href="{H:friendship-bracelet-patterns.html}">Friendship bracelet patterns</a>.</li><li><a href="{H:embroidery-patterns.html}">Embroidery patterns</a> and <a href="{H:embroidery-stitches.html}">embroidery stitches for beginners</a>.</li></ul>'''

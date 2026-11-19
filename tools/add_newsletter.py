#!/usr/bin/env python3
"""One-off patch: adds the Kit email signup, /thanks and /welcome pages, and newsletter privacy text to each site build."""
import pathlib, re, sys

H = pathlib.Path("/home/claude")

SITES = {
    "neoncoast": dict(
        build=H / "repo/build.py", css=H / "repo/assets/style.css", form=10215418,
        h2="Get the GTA 6 100% checklist",
        pitch="Every mission, trophy and completion goal on one printable checklist, free. Plus a short weekly email when new map pins, cheats and secrets are confirmed.",
        cta="Send my checklist", file="gta-6-100-percent-checklist.pdf", thing="GTA 6 100% checklist",
        links=[("/map", "Interactive map"), ("/completion", "100% tracker"), ("/cheats", "All cheat codes")],
        css_vars=dict(card="var(--panel)", line="var(--line)", acc="var(--flamingo)", acc_ink="#fff", text="var(--ink)", muted="var(--muted)", input="rgba(255,255,255,.06)", font="var(--display)"),
        privacy_old="We do not ask you to sign up and we do not collect your name or email.",
        privacy_new="If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the download and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time. We don't collect anything else about you.",
    ),
    "dayonedrop": dict(
        build=H / "dayonedrop/build.py", css=H / "dayonedrop/assets/style.css", form=10215426,
        h2="Get the 2027 release calendar",
        pitch="All the 2027 games we track, month by month, as a free printable calendar. Plus a short weekly email when a date moves or a new game gets dated.",
        cta="Send my calendar", file="2027-game-release-calendar.pdf", thing="2027 game release calendar",
        links=[("/calendar", "Release calendar"), ("/games", "All 2027 games"), ("/tools", "Launch list tools")],
        css_vars=dict(card="var(--panel)", line="var(--rule)", acc="var(--amber)", acc_ink="#0c0d10", text="var(--text)", muted="var(--muted)", input="var(--flap)", font="var(--display)"),
        privacy_old="We don't ask for sign-ups. Your launch list is saved only in your own browser.",
        privacy_new="Your launch list is saved only in your own browser. If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the calendar and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.",
    ),
    "padel": dict(
        build=H / "padelglassbox/build.py", css=H / "padelglassbox/assets/style.css", form=10215431,
        h2="Free padel rules cheat sheet",
        pitch="All the rules on one printable page, including golden point and the new Star Point. Plus a short email when we add new tools and guides.",
        cta="Send my cheat sheet", file="padel-rules-cheat-sheet.pdf", thing="padel rules cheat sheet",
        links=[("/score", "Score keeper"), ("/americano", "Americano draw maker"), ("/racket-finder", "Racket finder")],
        css_vars=dict(card="var(--glass-2)", line="var(--line)", acc="var(--turf)", acc_ink="#fff", text="var(--ink)", muted="var(--muted)", input="#fff", font="var(--display)"),
        privacy_old="No sign-ups. Your score, checklist ticks and quiz answers are saved only in your own browser.",
        privacy_new="Your score, checklist ticks and quiz answers are saved only in your own browser. If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the cheat sheet and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.",
    ),
    "purl": dict(
        build=H / "etsy-studio/site/build.py", css=H / "etsy-studio/site/assets/style.css", form=10215409,
        h2="Free printable sampler",
        pitch="Journaling cards, a vintage ephemera sheet and a planner page from our shop, free to print. Plus new freebies and pattern ideas now and then.",
        cta="Send my printables", file="purl-and-paper-free-sampler.pdf", thing="free printable sampler",
        links=[("/row-counter", "Row counter"), ("/yarn-calculator", "Yarn calculator"), ("/journal-prompts", "Journal prompts")],
        css_vars=dict(card="var(--sheet)", line="var(--line)", acc="var(--berry)", acc_ink="#fff", text="var(--ink)", muted="var(--ink-2)", input="#fff", font="var(--display)"),
        privacy_old=None,
        privacy_new="If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the free printables and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.",
    ),
}


def css_block(v):
    return f"""
/* ---- Email signup (Kit) ---- */
.nl {{ padding: 28px 0 8px; }}
.nl-card {{ background: {v['card']}; border: 1px solid {v['line']}; border-radius: 16px; padding: 26px; display: grid; grid-template-columns: 1.1fr 1fr; gap: 18px 28px; align-items: center; color: {v['text']}; }}
.nl-card h2 {{ font-family: {v['font']}; margin: 0 0 6px; font-size: clamp(1.35rem, 2.6vw, 1.8rem); line-height: 1.15; }}
.nl-card p {{ margin: 0; color: {v['muted']}; }}
.nl-form {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.nl-form input {{ flex: 1 1 220px; min-height: 48px; padding: 0 14px; border-radius: 10px; border: 1px solid {v['line']}; background: {v['input']}; color: {v['text']}; font: inherit; font-size: 1rem; }}
.nl-form button {{ min-height: 48px; padding: 0 20px; border: 0; border-radius: 10px; background: {v['acc']}; color: {v['acc_ink']}; font: inherit; font-weight: 700; cursor: pointer; }}
.nl-form button:hover {{ filter: brightness(1.08); }}
.nl-form input:focus-visible, .nl-form button:focus-visible {{ outline: 3px solid {v['acc']}; outline-offset: 2px; }}
.nl-fine {{ grid-column: 1 / -1; font-size: .85rem; }}
.nl-fine a {{ color: inherit; }}
.nl-sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
.nl-done {{ text-align: center; max-width: 640px; margin: 0 auto; padding: 56px 0 28px; }}
.nl-done .nl-btn {{ display: inline-block; margin: 18px 0 8px; padding: 14px 24px; border-radius: 12px; background: {v['acc']}; color: {v['acc_ink']}; font-weight: 700; text-decoration: none; }}
.nl-links {{ display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 18px; }}
.nl-links a {{ padding: 8px 14px; border: 1px solid {v['line']}; border-radius: 999px; color: inherit; text-decoration: none; }}
@media (max-width: 760px) {{ .nl-card {{ grid-template-columns: 1fr; padding: 20px; }} }}
"""


def py_block(s):
    links = "".join(f'<a href="{u}">{n}</a>' for u, n in s["links"])
    return f'''
# ---- Email signup (Kit form {s["form"]}). Sign-ups go to Kit; Kit redirects to /thanks, then /welcome after confirming. ----
NL_SKIP = ("thanks.html", "welcome.html", "404.html", "privacy.html")
NOINDEX = ("thanks.html", "welcome.html", "404.html")
def signup(file):
    if file in NL_SKIP:
        return ""
    return """<section class="nl" id="newsletter"><div class="wrap"><div class="nl-card">
<div><h2>{s["h2"]}</h2><p>{s["pitch"]}</p></div>
<form class="nl-form" action="https://app.kit.com/forms/{s["form"]}/subscriptions" method="post">
<label class="nl-sr" for="nl-email">Email address</label>
<input id="nl-email" type="email" name="email_address" required placeholder="Your email address" autocomplete="email">
<button type="submit">{s["cta"]}</button>
</form>
<p class="nl-fine">Free. No spam, unsubscribe in one click. See our <a href="/privacy.html">privacy policy</a>.</p>
</div></div></section>"""
NL_THANKS = """<section><div class="wrap nl-done"><h1>Check your inbox</h1>
<p>We've just emailed you a confirmation link. Tap the button in that email and your {s["thing"]} opens straight away.</p>
<p>Can't see it after a minute? Look in your spam or promotions folder.</p>
<div class="nl-links">{links}</div></div></section>"""
NL_WELCOME = """<section><div class="wrap nl-done"><h1>You're in!</h1>
<p>Thanks for confirming. Here's your {s["thing"]}:</p>
<a class="nl-btn" href="/assets/free/{s["file"]}" download>Download the PDF</a>
<p>We'll email you when there's something worth knowing, never more than once a week.</p>
<div class="nl-links">{links}</div></div></section>"""
'''


def patch(name, s):
    b = s["build"].read_text()
    if "NL_SKIP" in b:
        print(name, "already patched"); return
    # 1. helper block before def page(
    b = b.replace("\ndef page(", py_block(s) + "\n\ndef page(", 1)
    # 2. signup before the bottom ad slot inside <main>
    m = re.search(r"\n(\{AD\.format\(file[^\n]*\})\n</main>", b)
    assert m, name + ": ad slot not found"
    b = b[:m.start()] + "\n{signup(file)}\n" + m.group(1) + "\n</main>" + b[m.end():]
    # 3. noindex on thanks/welcome
    b = b.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                  '<meta name="robots" content="{"noindex, follow" if file in NOINDEX else "index, follow, max-image-preview:large"}">', 1)
    # 4. privacy text
    if s["privacy_old"]:
        assert s["privacy_old"] in b, name + ": privacy text not found"
        b = b.replace(s["privacy_old"], s["privacy_new"], 1)
    else:
        anchor = "<h2>What we store</h2>"
        assert anchor in b, name + ": privacy anchor not found"
        b = b.replace(anchor, f"<h2>Email list</h2><p>{s['privacy_new']}</p>\n" + anchor, 1)
    s["build"].write_text(b)
    # 5. css
    c = s["css"].read_text()
    if "Email signup (Kit)" not in c:
        s["css"].write_text(c + css_block(s["css_vars"]))
    print(name, "patched")


if __name__ == "__main__":
    for n in (sys.argv[1:] or SITES):
        patch(n, SITES[n])

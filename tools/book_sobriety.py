"""KDP paperback: "Back to Daylight: A 90-Day Sobriety Journal" (6x9, B&W interior, white paper).
Built 24 Nov 2026 from competitor research: buyers of the top sobriety journals complain about
the same prompt repeated every day, grammar mistakes, books written only for people still drinking,
too much blank space with nothing to reflect on, and "nothing but a cute cover".
This book: 90 different prompts in 13 themed weeks, a craving log and HALT check on every day page,
a real relapse-prevention plan, milestone pages, weekly reviews, money-saved tracker, support log.
"""
import pathlib, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kdp

OUT = pathlib.Path("/home/claude/kdp/sobriety")
OUT.mkdir(parents=True, exist_ok=True)
TITLE = "Back to Daylight"
SUB = "A 90-Day Sobriety Journal"
BRAND = "Steady Ground Press"

WEEKS = [
    ("Week 1: Getting through the first days", [
        "Why did you decide to stop? Write the reason in your own words, as if explaining it to a friend.",
        "What did your body and mind feel like today? Write down every change you noticed, even small ones.",
        "Which time of day is hardest right now? Plan one thing you will do at that time tomorrow.",
        "Who knows you are doing this? Who could you tell next, and what would you say?",
        "What did you used to do with the time you now have back? Name three better ways to fill it.",
        "Describe a moment today when you wanted to give up and did not. What kept you going?",
        "You made it through your first week. What surprised you most about it?",
    ]),
    ("Week 2: Knowing your triggers", [
        "List the people, places and situations that make you want to drink or use. Circle the strongest one.",
        "Which feeling shows up right before a craving: boredom, stress, loneliness, celebration or something else?",
        "Think about your usual evening. Which part of it is built around drinking or using? How could you change that part?",
        "Write about a trigger you cannot avoid, such as a work event or a family dinner. What is your plan for it?",
        "What does your inner voice say when it wants you to use? Write its words, then write your answer back.",
        "Which trigger was easier today than it was a week ago?",
        "If a friend had your triggers, what advice would you give them?",
    ]),
    ("Week 3: Your body coming back", [
        "How are you sleeping compared with two weeks ago? What helps you fall asleep now?",
        "What have you been eating? Plan one simple, filling meal for tomorrow.",
        "Go for a ten-minute walk or stretch. How did your body feel before and after?",
        "What is one health worry you have put off? What is the first small step to deal with it?",
        "Describe your energy today from morning to night. When did you feel best?",
        "What does your face, skin or reflection look like to you this week?",
        "Write a thank-you note to your body for carrying you through this.",
    ]),
    ("Week 4: Feelings without numbing them", [
        "Name every feeling you had today. Which one was the hardest to sit with?",
        "When did you last cry, laugh hard or get angry without a drink in you? What was it like?",
        "What feeling did drinking or using help you avoid? What is it trying to tell you?",
        "Write about something that made you anxious today, and how the anxiety rose and then fell.",
        "Which healthy things calm you down? Make a list you can read during a bad moment.",
        "Is there an old hurt that keeps coming up? Write about it for five minutes without stopping.",
        "One month is close. Which feeling has become easier to handle?",
    ]),
    ("Week 5: Relationships", [
        "Who has been hurt by your drinking or using? You do not need to fix it today. Just write it down.",
        "Who has supported you this month? How could you let them know it mattered?",
        "Which relationship pulls you towards using? What boundary would protect you?",
        "Write about a conversation you are dreading. What is the one thing you most need to say?",
        "Who are you lonely for? What is one way to connect with someone this week?",
        "How do you want people to describe you a year from now?",
        "What did you learn this week about asking for help?",
    ]),
    ("Week 6: Saying no", [
        "Write down three ways to turn down a drink that feel natural to you.",
        "Who in your life expects you to drink or use? How will you handle them?",
        "Describe the last time you said yes when you meant no, about anything. What would no have cost you?",
        "Plan a social event without alcohol: where you would go, what you would drink, when you would leave.",
        "What does your exit plan look like if a situation gets risky?",
        "Write about a time this week you put yourself first. How did it feel?",
        "Which no was the most important one you said this week?",
    ]),
    ("Week 7: Money and time", [
        "Work out roughly what you spent on drinking or using each week. Write the yearly total.",
        "What will you do with the money you are saving? Pick something real and write the price.",
        "How many hours a week did drinking or using take, including recovering the next day?",
        "Which hobby or interest did you drop? What would it take to start again?",
        "Plan a free afternoon that would make you genuinely happy.",
        "What is one small purchase that would support your recovery?",
        "Look at your money and time saved so far. Write a sentence you would be proud to read later.",
    ]),
    ("Week 8: Hard days", [
        "Describe your worst day since you stopped. What got you through it?",
        "What are your early warning signs that a bad day is coming?",
        "Write the instructions you would give yourself for a bad night, step by step.",
        "What story do you tell yourself about why one drink or one time would be fine? Write the full story, then the true ending.",
        "Who can you call at 2 a.m.? If nobody comes to mind, how could you change that?",
        "What is something kind you could do for yourself on a hard day?",
        "You are two months in. Which hard moment are you most proud of handling?",
    ]),
    ("Week 9: Who you are becoming", [
        "Describe yourself in three words today. How are they different from three months ago?",
        "Which values matter most to you? How does staying sober protect them?",
        "What is something you have started doing well again?",
        "Write about a version of you five years from now who stayed on this path.",
        "What did you believe about yourself while drinking or using that you no longer believe?",
        "Which person do you admire, and what quality of theirs are you growing?",
        "What would you like to try for the first time sober?",
    ]),
    ("Week 10: Forgiveness", [
        "What do you still blame yourself for? Write it, then write what you would say to a friend who felt the same.",
        "Is there someone you need to forgive, even if you never tell them?",
        "What would making things right look like with one person you hurt? Is it safe and fair to them to try?",
        "Write a short letter to yourself from the day before you stopped.",
        "Which mistake taught you the most?",
        "How do you want to treat yourself after a bad day from now on?",
        "What feels lighter this week than it did at the start?",
    ]),
    ("Week 11: Joy and rest", [
        "When did you laugh today? Write about it in detail.",
        "List ten small things that give you pleasure and cost little or nothing.",
        "What does real rest look like for you? Plan an hour of it this week.",
        "Describe a place where you feel calm. When can you go there next?",
        "What did you enjoy as a child that you could enjoy again?",
        "Write about a good evening you had without drinking or using.",
        "What are you looking forward to next month?",
    ]),
    ("Week 12: Protecting what you have built", [
        "Read your relapse-prevention plan at the front of this book. What would you change now?",
        "Which routines are keeping you steady? Write them down as your daily non-negotiables.",
        "What situations still worry you in the months ahead (holidays, trips, anniversaries)?",
        "Who will you check in with after this journal ends?",
        "What would you tell someone on their first day?",
        "What does complacency look like for you? How will you notice it early?",
        "List everything you have gained in the last twelve weeks.",
    ]),
    ("Week 13: Ninety days", [
        "Go back and read Day 1. What would you say to the person who wrote it?",
        "Which part of this journey has changed you the most?",
        "Write about the support that made the biggest difference.",
        "What are your goals for the next ninety days?",
        "Write a promise to yourself for the year ahead, in one sentence.",
        "Ninety days. How do you want to mark it? Plan something that has nothing to do with drinking or using.",
    ]),
]
PROMPTS = [p for _, ps in WEEKS for p in ps]
assert len(PROMPTS) == 90, len(PROMPTS)
MILESTONES = {1: "24 hours", 7: "One week", 14: "Two weeks", 30: "Thirty days", 60: "Sixty days", 90: "Ninety days"}

CSS = """
body { font-family: 'Bitstream Charter', 'DejaVu Serif', serif; color:#111; }
.lab { font-family: Inter, sans-serif; font-size: 7.4pt; letter-spacing:.02em; color:#333; font-weight:600; }
h1 { font-family: Inter, sans-serif; font-weight: 800; font-size: 22pt; margin: 0 0 2pt; letter-spacing:-.01em; }
h2 { font-family: Inter, sans-serif; font-weight: 700; font-size: 13pt; margin: 0 0 6pt; }
h3 { font-family: Inter, sans-serif; font-weight: 700; font-size: 8.4pt; margin: 8pt 0 3pt; text-transform:none; }
p { font-size: 9.6pt; line-height: 1.42; margin: 0 0 6pt; }
.line { border-bottom: .6pt solid #777; height: 18pt; }
.line.s { height: 17pt; }
.row { display:flex; gap: 10pt; align-items:flex-end; }
.row > div { flex:1; }
.dots span { display:inline-block; width: 11pt; height:11pt; border:.8pt solid #222; border-radius:50%; margin-right:5pt; vertical-align:middle; }
.box { display:inline-block; width:9pt; height:9pt; border:.8pt solid #222; margin:0 3pt 0 8pt; vertical-align:-1pt; }
.prompt { font-size: 10.2pt; line-height:1.4; font-style: italic; margin: 3pt 0 2pt; }
.head { display:flex; justify-content:space-between; align-items:baseline; border-bottom: 1.6pt solid #111; padding-bottom: 3pt; margin-bottom: 6pt; }
.head .d { font-family: Inter, sans-serif; font-weight: 800; font-size: 17pt; }
.wk { font-family: Inter, sans-serif; font-size: 7pt; color:#444; }
.grid { display:grid; grid-template-columns: repeat(10, 1fr); gap: 3pt; }
.grid div { border:.8pt solid #222; height: 26pt; font-family: Inter, sans-serif; font-size: 6.5pt; padding: 2pt; box-sizing:border-box; }
table { border-collapse: collapse; width:100%; font-family: Inter, sans-serif; font-size: 7.4pt; }
td, th { border: .6pt solid #444; padding: 3pt 4pt; height: 16pt; text-align:left; }
th { font-weight:700; background:#eee; }
.c { text-align:center; }
.title { flex:1; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; }
.title .big { font-family: Inter, sans-serif; font-weight:800; font-size: 34pt; line-height:1; letter-spacing:-.02em; }
.title .sub { font-size: 14pt; margin-top: 8pt; }
.small { font-size: 8pt; line-height:1.4; color:#222; }
.mile { flex:1; display:flex; flex-direction:column; }
.mile .big { font-family: Inter, sans-serif; font-weight:800; font-size: 30pt; margin: 18pt 0 4pt; }
.blank {}
.sec { border: .7pt solid #222; border-radius: 7pt; padding: 5pt 8pt 6pt; margin-bottom: 6pt; }
.sec.last { flex: 1; }
.sh { display:flex; align-items:center; gap:5pt; font-family: Inter, sans-serif; font-weight: 800; font-size: 7.6pt; letter-spacing: .08em; margin-bottom: 4pt; }
.face { display:inline-block; margin-left: 7pt; vertical-align: middle; }
.intro { flex:1; display:flex; flex-direction:column; justify-content:center; }
.intro .it { font-family: 'GFS Baskerville', 'Bitstream Charter', serif; font-size: 27pt; line-height: 1.1; margin: 6pt 0 10pt; }
.intro .rule { width: 1.2in; border-top: 2pt solid #111; margin-bottom: 12pt; }
.intro .ip { font-size: 11pt; line-height: 1.55; }
.ideas { display:grid; grid-template-columns: 1fr 1fr; gap: 11pt 12pt; font-size: 9.2pt; line-height:1.3; }
.ideas .box { margin-left: 0; }
"""


def lines(n, cls=""):
    return "".join(f'<div class="line {cls}"></div>' for _ in range(n))


def esc(s):
    return html.escape(s)


pages = []
# 1 title
pages.append(f'<div class="title"><div class="big">{TITLE}</div><div class="sub">{SUB}</div>'
             f'<p style="margin-top:14pt">Daily prompts, craving check-ins, milestones and a plan for the hard days</p>'
             f'<div style="margin-top:40pt" class="lab">This journal belongs to</div><div class="line" style="width:3.2in"></div>'
             f'<div style="margin-top:14pt" class="lab">Day 1 date</div><div class="line" style="width:2in"></div></div>')
# 2 copyright + safety
pages.append(f'<div style="margin-top:auto" class="small"><p class="small"><b>{TITLE}: {SUB}</b><br>Copyright © 2026 {BRAND}. All rights reserved. No part of this book may be copied or reproduced without permission, except for personal use by the owner of this copy.</p>'
             '<p class="small">This journal is a support tool. It is not medical, psychological or addiction treatment advice and does not replace help from a doctor, counsellor or support group. Stopping alcohol or some drugs suddenly can be dangerous for people who drink or use heavily every day; talk to a doctor about safe withdrawal.</p>'
             '<p class="small">If you are in crisis or thinking about harming yourself, contact emergency services. In the US you can call or text 988 (Suicide and Crisis Lifeline) or call the SAMHSA National Helpline at 1-800-662-4357, free, confidential and open 24/7. In other countries, write your local numbers on the Support page.</p></div>')
# 3 how to use
pages.append('<h2>How to use this journal</h2>'
             '<p><b>Every morning</b> (two minutes): rate how you feel and write one thing you will do today to protect your sobriety.</p>'
             '<p><b>When a craving hits</b>: run the HALT check (are you Hungry, Angry, Lonely or Tired?), then use the craving plan on page 7. Later, note what set it off and what you did instead.</p>'
             '<p><b>Every evening</b> (five to ten minutes): answer the day\'s prompt. There are ninety different prompts, one for each day, grouped into thirteen weekly themes, from getting through the first days to planning the ninety days after this book.</p>'
             '<p><b>Every seventh day</b>: fill in the weekly review and add up the money you have saved.</p>'
             '<p><b>Milestones</b> at 24 hours, one week, two weeks, thirty, sixty and ninety days each get their own page.</p>'
             '<p>Missed a day or had a slip? Do not throw the book away. Start the next page honestly, write what happened on the Notes pages, and talk to someone on your support list. Recovery is not a straight line.</p>'
             '<p>This journal works whether you are on Day 1 or already a few weeks in, and whether you are stopping alcohol or something else.</p>')
# 4 reasons
pages.append('<h2>My reasons</h2><p>Why I am doing this. Read this page on hard days.</p>' + "".join(f'<div class="lab" style="margin-top:6pt">{i}.</div>' + lines(3) for i in range(1, 6)) +
             '<h3>What I will gain</h3>' + lines(4))
# 5 support people
rows = "".join("<tr><td></td><td></td><td></td></tr>" for _ in range(12))
pages.append('<h2>My support people</h2><p>People I can call or message, any time of day.</p>'
             f'<table><tr><th style="width:40%">Name</th><th style="width:35%">Phone</th><th>Best time</th></tr>{rows}</table>'
             '<h3>Sponsor, counsellor or doctor</h3>' + lines(2) + '<h3>Local crisis and helpline numbers</h3>' + lines(3) +
             '<h3>Meetings near me (day, time, place)</h3>' + lines(3))
# 6 triggers map
pages.append('<h2>My trigger map</h2><p>Fill this in during Week 2 and update it as you learn more.</p>' +
             "".join(f'<h3>{t}</h3>' + lines(3, "s") for t in ["People", "Places", "Times of day and days of the week", "Feelings", "Events and occasions", "Things I see, hear or smell"]))
# 7 craving plan
pages.append('<h2>When a craving hits</h2>'
             '<p><b>1. Pause and name it.</b> Say to yourself: "This is a craving. It will rise, peak and pass." Most cravings fade within 15 to 30 minutes if you do not act on them.</p>'
             '<p><b>2. HALT check.</b> Am I Hungry, Angry, Lonely or Tired? Deal with that first: eat something, step outside, message someone, rest.</p>'
             '<p><b>3. Change where you are.</b> Leave the room, go for a walk, take a shower, drive somewhere without a shop on the way.</p>'
             '<p><b>4. Play the tape forward.</b> Picture the whole night and the next morning, not just the first drink.</p>'
             '<p><b>5. Reach out.</b> Call or message someone from your support page before deciding anything.</p>'
             '<h3>My personal craving plan: what works for me</h3>' + lines(7) +
             '<h3>Things I keep within reach (drinks, snacks, music, phone numbers)</h3>' + lines(3))
IDEAS = ["Drink a tall glass of cold water", "Eat something with protein", "Walk around the block", "Take a hot shower", "Call or text someone on your list",
 "Go to a meeting, in person or online", "Make a cup of tea or a fancy alcohol-free drink", "Write the craving down here and rate it", "Breathe in for 4, hold 4, out for 6, five times",
 "Put on one song and really listen", "Leave the room or the place", "Do ten minutes of cleaning", "Read your reasons page", "Play the tape forward to tomorrow morning",
 "Lie down for twenty minutes", "Cook something simple", "Watch something funny", "Do a puzzle or a game on paper", "Stretch for five minutes", "Step outside and name five things you see",
 "Brush your teeth", "Go to a café or a library", "Write a letter you will not send", "Plan something for next weekend", "Look at your money-saved total",
 "Pet an animal or water a plant", "Tidy one drawer", "Go to bed early", "Message someone just to say hello", "Wait 20 minutes, then decide again"]
pages.append('<h2>Thirty things to do instead</h2><p>Pick one when a craving hits. Tick the ones that work for you.</p><div class="ideas">' + "".join(f'<div><span class="box"></span>{esc(x)}</div>' for x in IDEAS) + '</div>')
# 8 relapse prevention
pages.append('<h2>My relapse-prevention plan</h2>' +
             "".join(f'<h3>{t}</h3>' + lines(n, "s") for t, n in [("Early warning signs I am slipping (thoughts, moods, habits)", 4), ("What I will do as soon as I notice them", 4), ("High-risk situations coming up", 3), ("My plan for each of them", 4), ("If I slip, the first three things I will do", 3)]))
# 9 letter
pages.append('<h2>A letter to myself on Day 90</h2><p>Write to the person who will finish this book. What do you hope they feel? What do you want them to remember?</p>' + lines(19))
# 10 tracker grid
cells = "".join(f'<div>{i}</div>' for i in range(1, 91))
pages.append('<h2>Ninety-day tracker</h2><p>Mark each day: shade it for a sober day, or draw a line through it if you slipped and note the date on the Notes page. Keep going either way.</p>'
             f'<div class="grid">{cells}</div>')
# 11 money saved
mrows = "".join(f"<tr><td class='c'>{w}</td><td></td><td></td><td></td></tr>" for w in range(1, 14))
pages.append('<h2>Money and time saved</h2><p>What I used to spend in a typical week: $ ________ &nbsp; Hours a week: ________</p>'
             f'<table><tr><th style="width:12%">Week</th><th>Saved this week</th><th>Total so far</th><th>Hours back</th></tr>{mrows}</table>'
             '<h3>What I will do with the money</h3>' + lines(3))


SUN_I = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>'
MOON_I = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#111" stroke-width="1.8" stroke-linejoin="round"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'
WAVE_I = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round"><path d="M2 9c3-3 5 3 8 0s5 3 8 0 3-1 4 0M2 15c3-3 5 3 8 0s5 3 8 0 3-1 4 0"/></svg>'
def face(m):
    mouth = {0: "M8 17c2-2.5 6-2.5 8 0", 1: "M8 16.5c2-1 6-1 8 0", 2: "M8 16h8", 3: "M8 15.5c2 1 6 1 8 0", 4: "M8 15c2 2.5 6 2.5 8 0"}[m]
    return f'<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="#111" stroke-width="1.4" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="9" cy="10" r=".9" fill="#111"/><circle cx="15" cy="10" r=".9" fill="#111"/><path d="{mouth}"/></svg>'
FACES = "".join(f'<span class="face">{face(i)}</span>' for i in range(5))


def day_page(n, week_name):
    halt = "".join(f'<span class="box"></span>{w}' for w in ["Hungry", "Angry", "Lonely", "Tired"])
    crav = "".join(f'<span class="box"></span>{w}' for w in ["None", "1-2", "3-5", "6+"])
    return (f'<div class="head"><span class="d">Day {n}</span><span class="wk">{esc(week_name)}</span><span class="lab">Date ____________</span></div>'
            f'<div class="sec"><div class="sh">{SUN_I}<span>MORNING</span></div>'
            f'<div class="row" style="align-items:center"><span class="lab">I FEEL</span>{FACES}</div>'
            '<div class="lab" style="margin-top:4pt">ONE THING I WILL DO TODAY TO PROTECT MY SOBRIETY</div>' + lines(1, "s") + '</div>'
            f'<div class="sec"><div class="sh">{WAVE_I}<span>CRAVINGS</span></div>'
            f'<div class="lab">HOW MANY {crav}&nbsp;&nbsp; STRONGEST (1-10) ____</div>'
            f'<div class="lab" style="margin-top:4pt">HALT CHECK {halt}</div>'
            '<div class="lab" style="margin-top:5pt">WHAT SET IT OFF</div>' + lines(1, "s") + '<div class="lab" style="margin-top:3pt">WHAT I DID INSTEAD</div>' + lines(1, "s") + '</div>'
            f'<div class="sec last"><div class="sh">{MOON_I}<span>EVENING</span></div><div class="prompt">{esc(PROMPTS[n - 1])}</div>' + lines(8) +
            '<div class="lab" style="margin-top:5pt">GRATEFUL FOR</div>' + "".join(f'<div class="row"><span class="lab" style="flex:0 0 8pt">{i}</span><div class="line s"></div></div>' for i in (1, 2, 3)) +
            '<div class="lab" style="margin-top:5pt">TODAY\'S WIN, HOWEVER SMALL</div>' + lines(1, "s") + '</div>')


INTROS = [
 "The first days are about getting through, not getting it perfect. Eat, drink water, sleep when you can and keep your plan close. Every evening you write, you add proof that you can do this.",
 "Cravings rarely come from nowhere. This week you will start noticing the people, places, times and feelings that set them off, so you can plan for them instead of being surprised.",
 "Your body is already repairing itself. Sleep, appetite and energy can swing up and down at first. This week pays attention to the physical side of recovery and the small habits that help.",
 "Drinking or using often numbs feelings that then come back loudly. This week is about naming them, riding them out and building a short list of things that genuinely calm you.",
 "Recovery happens around other people. This week looks at who supports you, who pulls you back, and how to ask for help without feeling like a burden.",
 "Saying no gets easier with practice. This week you will plan your words, your exits and your alcohol-free options before you need them.",
 "Count what drinking or using really cost you in money and time. This week turns those savings into something you can see and look forward to.",
 "Hard days will come. This week is about spotting them early and having a plan written down for the worst nights, so you do not have to think clearly when it is hardest to.",
 "You are starting to change. This week looks at who you are becoming, the values you want to live by and the new things you could try.",
 "Guilt and shame are heavy to carry. This week is about being honest without punishing yourself, and about which amends are fair and safe to make.",
 "Sobriety is not only about what you give up. This week is about rest, fun and the small pleasures you can enjoy with a clear head.",
 "You have built something real. This week checks your routines and your plan for the months ahead, so complacency does not creep in.",
 "The last stretch. This week you look back at Day 1, notice how far you have come and set your goals for the next ninety days.",
]
assert len(INTROS) == 13


def intro_page(w, name, text):
    t = name.split(": ", 1)[1]
    return (f'<div class="intro"><div class="lab">WEEK {w} OF 13</div><div class="it">{esc(t)}</div><div class="rule"></div><p class="ip">{esc(text)}</p>'
            '<div class="lab" style="margin-top:22pt">MY FOCUS THIS WEEK</div>' + lines(3) + '</div>')


def review_page(w, name):
    cols = "".join(f"<th class='c'>{d}</th>" for d in ["Day 1", "2", "3", "4", "5", "6", "7"])
    return (f'<h2>Week {w} review</h2><p class="wk">{esc(name)}</p>'
            f'<table><tr><th></th>{cols}</tr><tr><td>Mood (1-5)</td>{"<td></td>" * 7}</tr><tr><td>Cravings</td>{"<td></td>" * 7}</tr><tr><td>Sleep (hours)</td>{"<td></td>" * 7}</tr></table>'
            + "".join(f'<h3>{t}</h3>' + lines(k, "s") for t, k in [("What helped most this week", 3), ("What was hardest", 3), ("A trigger I handled better", 2), ("Who I connected with", 2), ("Next week I will", 3)])
            + '<div class="lab" style="margin-top:8pt">MONEY SAVED THIS WEEK $ ________ &nbsp;&nbsp; TOTAL $ ________</div>')


def milestone_page(n, name):
    return (f'<div class="mile"><div class="lab">MILESTONE</div><div class="big">{name}</div><p>Day {n}. Stop and notice how far you have come.</p>'
            + "".join(f'<h3>{t}</h3>' + lines(k) for t, k in [("How I feel right now", 4), ("What is different from Day 1", 4), ("What got me here", 4), ("How I will celebrate (without drinking or using)", 3), ("My next milestone and the date I will reach it", 1)]) + '</div>')


day = 0
for w, (name, ps) in enumerate(WEEKS, 1):
    pages.append(intro_page(w, name, INTROS[w - 1]))
    for _ in ps:
        day += 1
        pages.append(day_page(day, name))
        if day in MILESTONES:
            pages.append(milestone_page(day, MILESTONES[day]))
    pages.append(review_page(w, name))
# back matter
lrows = "".join("<tr><td></td><td></td><td></td></tr>" for _ in range(16))
for _ in range(3):
    pages.append(f'<h2>Meeting and support log</h2><table><tr><th style="width:22%">Date</th><th style="width:33%">Meeting, call or session</th><th>What I took away</th></tr>{lrows}</table>')
pages.append('<h2>The next ninety days</h2>' + "".join(f'<h3>{t}</h3>' + lines(k) for t, k in [("What I will keep doing every day", 4), ("New goals", 4), ("Support I will keep in place", 3), ("Dates to watch (holidays, anniversaries, trips)", 3)]))
for _ in range(5):
    pages.append('<h2>Notes</h2>' + lines(25))
if len(pages) % 2:
    pages.append('<h2>Notes</h2>' + lines(25))

if __name__ == "__main__":
    prev = [(0, OUT / "p-title.png"), (2, OUT / "p-howto.png"), (6, OUT / "p-craving.png"), (11, OUT / "p-day1.png"), (12, OUT / "p-mile.png"), (19, OUT / "p-review.png")]
    n = kdp.interior(pages, CSS, 6, 9, OUT / "interior.pdf", inside=0.625, outside=0.5, top=0.5, bottom=0.5, previews=prev)
    (OUT / "pages.txt").write_text(str(n))
    print("pages", n)

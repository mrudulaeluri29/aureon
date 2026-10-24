# Freebie Radar

> **Free food, paid studies, and the internships your department never told you about, texted to you before they're gone.**

A [Cubbie](https://cubbie.ai) Skill by team **Aureon** for the [Cubbie Hackathon](https://hackathon.cubbie.ai).

## The problem

By the time you see "free pizza" or "$25 Amazon card for a 30-minute study," it's over or full. It was buried in a
club email, a muted Discord, or a Canvas announcement.

The worst part: some of the best opportunities are open to **every major** but posted by **one college**.
McLEAPS, a paid Maricopa County internship, is listed by ASU's Watts College as open to students "from any major
at ASU". A CS or biology student would never look there.

## Real tests on Cubbie (Oct 24, 2026)

**"Any free food this week? I am on tempe campus"**: two real SunDevilCentral events with free food, each with
its link, and a flag where the flyer and the calendar disagree on the start time.

![Cubbie finding free food on SunDevilCentral](screenshots/free-food.jpg)

**"I'm a CS major. any paid internships open to all majors that my department doesn't post?"**: McLEAPS,
posted only by Watts College, open to any ASU major.

![Cubbie finding McLEAPS, a paid internship open to all majors](screenshots/hidden-internship.jpg)

## What a weekly digest looks like

```text
You:    anything free this week?

Cubbie: 3 freebies this week
        🍕 Free boba, Indian Student Assoc, Tue 5 pm, Memorial Union
        💵 $25 Amazon card, 30 min online survey ($50/hr)
        🔎 Paid county internship open to all majors (Watts College)

        Want me to draft an email to the researcher?
You:    yes
Cubbie: Here's the draft. Send it?
```

(Example conversation. Real replies use only events, amounts and dates Cubbie actually read.)

## What it finds

| | Finds | From |
| --- | --- | --- |
| 🍕 | Free food in the next 48 hours that fits your diet, with the SunDevilCentral link to RSVP | SunDevilCentral club events, ASU Events, club emails, Canvas, Slack and Discord notification emails |
| 💵 | Paid research studies, ranked by pay per hour | Your email, department research pages |
| 🎓 | Open scholarships, with a reminder 3 days before the deadline | ASU and trusted scholarship pages |
| 🔎 | Hidden paid opportunities open to all majors but posted by another college | Every ASU college's website |

Plus a **Sunday digest** that never repeats an item, optional **same-day food alerts**, and a **send-to-a-friend**
message when a find fits someone else better.

## Built to be trusted

- Never signs you up, applies, or sends an email without your yes
- Never answers study screening questions for you
- Shows where each find came from and why you qualify
- Skips scams: anything asking for a fee, bank details or a password
- Never invents a date, amount or eligibility rule; says "not listed" instead

## Install

Text this link to Cubbie in iMessage and reply **yes**:

```
https://github.com/mrudulaeluri29/aureon/tree/main/freebie-radar
```

Then ask: **"anything free this week?"**

Like it? Vote for Freebie Radar at **[hackathon.cubbie.ai](https://hackathon.cubbie.ai)** (school email needed).

## Inside

```text
freebie-radar/
  SKILL.md                  what Cubbie does, step by step
  references/asu-sources.md ASU college, scholarship and research pages
  scripts/sundevil_food.py  finds SunDevilCentral events that serve food
  scripts/seen.py           never sends the same find twice, sorts by date
  assets/sample_finds.json  sample data for trying the script
```

Try the script without a phone: `cd freebie-radar && python3 scripts/seen.py new --sample`
(Python 3.9+, no packages). The Skill follows the open Agent Skills format, so other agents that support it can
use it too.

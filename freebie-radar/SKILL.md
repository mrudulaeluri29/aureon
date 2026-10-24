---
name: freebie-radar
description: Finds free food, paid research studies, scholarships and hidden paid opportunities for ASU students, and texts them before they're gone. Hidden opportunities are paid internships and programs open to all majors but posted by another college. Use when the student asks about free food, free stuff, scholarships, paid studies, research participants, gift cards for studies, paid internships open to any major, easy ways to earn money on campus, or wants a weekly digest of freebies, even if they don't say "freebie".
---

# Freebie Radar

Free food, paid studies, scholarships and paid programs are all over campus, but they are buried in club
emails, Canvas announcements, Slack or Discord servers, and the websites of colleges the student never visits.
A paid county internship open to every major can be posted only by the college of public service, so a CS
student never sees it. This Skill finds these things, keeps only what fits this student, and texts them in time
to act.

The rule for every find: it is **free or pays the student** (food, cash, gift cards, a stipend, a tuition waiver,
scholarship money) **and** the student would likely miss it. This is not a general job or event search.

Built for Arizona State University first (`references/asu-sources.md`). At other schools, use the same steps
with web search on that school's sites and say that results may be thinner.

## When to use

- "anything free this week?"
- "is there free food on campus tonight?"
- "any paid studies I can do?"
- "find me scholarships for CS majors"
- "any paid internships I can apply to? I'm a bio major"
- "send me freebies every Sunday"

Do not use it for a general internship or job search, writing scholarship essays (help only with a checklist
and reminders), emails to professors, or study plans.

## 1. Profile (first time only)

Check memory for a Freebie Radar profile. If there is none, ask these one at a time, each with a default the
student can accept with "yes", and remember the answers:

1. School, major and year ("ASU, and what's your major and year?").
2. Food preferences or restrictions (vegetarian, halal, no pork, none).
3. The campus they're usually on (Tempe, Downtown Phoenix, Polytechnic, West Valley, online).
4. Scholarship interests or groups, only what the student chooses to share (first generation, a club they lead).
5. Studies they're open to: online, in person, surveys, longer sessions.

If the student wants results right away, skip setup, search with what they already said, and offer setup after.

## 2. Collect finds

Search the sources below for the category the student asked about (all four for "anything free"). Use only
facts from pages, emails and posts you actually read. For each find, keep: type (food, study, scholarship or
opportunity), title, who posted it, date and time or deadline, place or online, pay or value, who can take part,
the link, and the exact sentence that shows the student qualifies.

A quick question ("anything free tonight?") gets a quick answer from email, Canvas and a few pages. For the
weekly digest, or when the student asks for everything, do the full sweep of `references/asu-sources.md` as a
background task and text the results when done.

### Free food

1. Start with SunDevilCentral, ASU's club event platform. Run, from this Skill's folder, with the student's local
   time now (Arizona time) and their campus from the profile:

   ```bash
   python3 scripts/sundevil_food.py --now <YYYY-MM-DDTHH:MM> --hours <hours> --campus <Tempe|Downtown|Poly|West Valley>
   ```

   Use `--hours 12` for "tonight", 48 by default, 168 for "this week" or the digest. Leave out `--campus` if
   it isn't known. The script prints upcoming events whose title or description mentions food, each with the
   club, start time, place, the food sentence and its SunDevilCentral link. Always give that link, on its own
   line, so the student can RSVP and see the location (most events show it only after signing in to
   SunDevilCentral). Check the food sentence yourself: skip events where food isn't really served, and say
   "may cost" when `may_cost` is true. Exit code 3 means the feed is unreachable: go on with steps 2 to 4.
2. If Google is connected, search the student's email from the last 7 days for club and department emails that
   mention food at an event (pizza, snacks, lunch, dinner, boba, "food provided", "refreshments"), including
   Slack and Discord notification emails.
3. If Canvas is connected, read course and department announcements for events with food.
4. Search ASU Events (https://asuevents.asu.edu) for this week's events on the student's campus that mention
   free food. If it won't load, rely on the steps above.
5. Keep only events in the next 48 hours (7 days for the digest) with a time and a place (a SunDevilCentral link counts as the place, since it shows the location after sign-in). Drop anything that
   conflicts with the student's food preferences, has ended, or needs a paid ticket.
6. A free-admission event with no food listed is not a food find. Mention at most one, last, as "free event, no
   food listed", and only when the student asked for anything free.

### Paid research studies

1. If Google is connected, search email from the last 14 days for "participants needed", "research study",
   "compensation", "gift card", "paid study", "survey" and "Amazon card", including Slack and Discord
   notification emails. Read the message text inside them.
2. Check the department research pages in `references/asu-sources.md`. Studies for course credit only are not
   paid; skip them unless the student asks for credit.
3. Work out pay per hour ($20 for 30 minutes is $40 an hour).
4. ASU studies come first: ones from the student's email, ASU labs and ASU pages. Add at most one online study
   pool from outside ASU, and only as a backup when ASU finds are thin. Skip studies the student plainly can't
   join (wrong age range, a city they're not in).
5. Send at most 3 studies, a few lines each: name, pay and pay per hour, time, online or where, one "Needs:"
   line, the sign-up link. End with "Want me to draft an email to the researcher?" for the best one.

### Scholarships

1. Search the public ASU scholarship and college pages in `references/asu-sources.md`, then trusted national
   sources, for scholarships matching the student's major, year and interests.
2. Keep only open ones with a deadline that hasn't passed. Never use a page that asks the student to pay to apply.
3. ASU's own scholarship search, Scholarship Universe, needs the student's ASU sign-in. Offer it once, as an
   option: "Want me to check Scholarship Universe too? You'd sign in to ASU once in my browser." If they agree,
   open it in the browser and ask the student to sign in (and take over for Duo). Never ask for their password in
   the chat.

### Hidden paid opportunities

Stay on ASU's own pages. A hidden opportunity is one an ASU college or office posts, not a national internship,
company job listing or job board. If the student wants a general internship search, say that's outside Freebie
Radar and answer normally without this Skill.

1. Read the college pages in `references/asu-sources.md`, plus a web search limited to each college's site for
   "internship", "fellowship", "stipend", "paid", "open to all majors", "any major".
2. Keep an item only if it is paid or funded (stipend, wage, tuition waiver, award) **and** its page says
   something like "all majors", "any major", "all ASU students" or "open to undergraduates from any
   discipline". Copy that sentence; it is the "why you qualify" line.
3. Drop items posted by the student's own college; they already see those.
4. Drop items with no current date: a page that only mentions past cohorts or past years is stale.

## 3. Drop what was already sent

Write the finds to `~/.cache/freebie-radar/finds.json` as a JSON list, one object per find:

```json
[{"type": "food", "title": "Free boba, Indian Student Assoc", "when": "2026-10-27T17:00",
  "where": "Memorial Union", "value": "free", "link": "https://...", "why": "..."}]
```

`when` is the event time or the deadline in the student's local time (`2026-10-27` or `2026-10-27T17:00`), or
leave it out if the page doesn't give one. Then run, from this Skill's folder, with the student's local date:

```bash
python3 scripts/seen.py new --finds ~/.cache/freebie-radar/finds.json --today <YYYY-MM-DD>
```

It prints only the finds this student hasn't been sent, without past dates, soonest first. After you text
them, record them so they never repeat:

```bash
python3 scripts/seen.py mark --finds ~/.cache/freebie-radar/finds.json
```

Exit code 2 means the finds file is malformed: fix it and run again once. If the script fails for another
reason, send the results anyway and say nothing about it.

## 4. Send results

Lead with what is happening soonest, then the highest value. At most 3 items per category in a text, and at
most 3 hidden opportunities in total; pick the ones closing soonest. If there
are more, make a one-page PDF with the documents ability, send it, and text a one-line summary.

Keep each find to about four short lines: what it is, the value, one line of requirements, the date, then the
link on its own line. Put a find's long details (hours, GPA, credits, background checks) on a single "Needs:"
line, not a paragraph.

For a hidden opportunity, include who posted it and the "why you qualify" line, so the student trusts it:

```text
🔎 McLEAPS, paid county internship, posted by Watts College
$6,000 stipend + tuition waiver
Why you qualify: "from any major at ASU"
Needs: 3.0 GPA, 60 credits, 40 hrs/week in person
Apply by Nov 1, 11:59 pm (page labels it Fall 2026, confirm first)
https://publicservice.asu.edu/impact/mcleaps-internships
```

End the results with exactly one question, about the most useful next step: usually a reminder before the
nearest deadline ("Want a reminder Oct 29, 3 days before it closes?"), or a draft email for a paid study.

When two pages disagree (different amounts or dates), say so and link the official page instead of picking one.
When a detail is missing, say it is missing instead of guessing.

## 5. Act only after a yes

- **Paid study:** offer to draft a short interest email to the researcher with Gmail. Show it; send only after
  the student says yes. Never answer screening questions for the student; they can ask about health, age or
  background, so the student answers them.
- **Scholarship or opportunity:** offer a reminder 3 days before the deadline and a short checklist of what to
  submit (essay, transcript, resume, recommendation). Never apply for the student.
- **Send to a friend:** when a find fits someone else better ("Know a nursing major?"), offer a ready-to-paste
  message the student can send themselves: the find, the deadline, the link, and "Found with Freebie Radar".
  Cubbie never texts anyone but its own student.

## 6. Offer a weekly digest and food alerts

After the first results, offer one at a time:

- A weekly digest, default Sunday 6 pm. Create the scheduled check-in only after the student agrees. Word it so
  it makes sense later: "Freebie Radar weekly digest: sweep free food for the next 7 days, open scholarships,
  paid studies and hidden paid opportunities for the student's saved profile, drop already-sent items with
  scripts/seen.py, and send only new ones."
- Same-day food alerts at a time the student picks (default 11 am), sent only on days with free food that fits
  their diet.

## 7. Slack and Discord through email (optional, offer later)

Cubbie can't read Slack or Discord directly, but it can read their notification emails. If the student is in
club, department or research servers, offer to walk them through it once, one app at a time (Google must be
connected):

- Slack, for each workspace: Preferences, then Notifications, then Channel keywords. Add: free food, pizza,
  snacks, study, participants, compensation, gift card, scholarship, stipend, internship. Then turn on email
  notifications for when they're not active.
- Discord: User Settings, then Notifications, turn on email notifications; on each club or research server, set
  notifications to All Messages for the channels that post events or studies.

Say plainly that Discord emails only some missed messages, so a few posts may not come through. Remember which
apps the student set up.

## Safety

- Skip scams: anything asking for bank details, a fee or a password, or a scholarship that charges to apply.
- Never sign the student up, apply, claim a spot or send an email without their yes.
- Keep the profile in memory; send nothing to any other server.
- Never invent an event, amount, date or eligibility rule.

## Replies

Keep each reply to a few short lines, plain text, no Markdown. One idea per text. Each link on its own line.
One emoji per category is fine: 🍕 food, 💵 studies, 🎓 scholarships, 🔎 hidden opportunities. Ask one question at
a time, with a default the student can accept with "yes". Example:

```text
3 freebies this week
🍕 Free boba, Indian Student Assoc, Tue 5 pm, Memorial Union
💵 $25 Amazon card, 30 min online survey ($50/hr)
🔎 Paid county internship open to all majors (Watts College)

Want me to draft an email to the researcher?
```

## When something fails

- Google or Canvas not connected: say which one would help, offer to connect it, and carry on with web results.
- Nothing found: say so in one line and offer to check again tomorrow.
- A page won't load or needs a sign-in: skip it and mention it only if it was the student's main ask.

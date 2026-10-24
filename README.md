# Freebie Radar

A [Cubbie](https://cubbie.ai) Skill for the Cubbie Hackathon (Track 1).

Free food, paid studies, scholarships and paid internships open to every major are all over ASU, buried in club
emails, Canvas, Slack and Discord, and the websites of colleges you never visit. Freebie Radar finds them, keeps
what fits you, and texts you before they're gone.

- 🍕 Free food in the next 48 hours that fits your diet
- 💵 Paid research studies, ranked by pay per hour
- 🎓 Open scholarships with deadline reminders
- 🔎 Hidden paid opportunities: programs open to all majors but posted by another college, like McLEAPS from
  Watts College

It never signs you up, applies or sends an email without your yes, and never invents a date or amount.

## Install

Text this link to Cubbie and reply "yes":

https://github.com/mrudulaeluri29/aureon/tree/main/freebie-radar

Then try: "anything free this week?"

## Try the script locally

```bash
cd freebie-radar
python3 scripts/seen.py new --sample
```

Python 3.9+, standard library only. The Skill is a standard Agent Skill, so it also works in Claude Code and
Codex.

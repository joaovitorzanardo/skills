# Diagnostic and Warm-up

The Diagnostic answers one question: **where should Lesson 1 start?** It isn't an exam, and a low score is useful information, not a failure. Tell the Learner that in one line before the first question, so they answer honestly instead of guessing.

## 1. Map the prerequisites (silently)

Before asking anything, sketch for yourself what the Topic stands on, two levels deep:

```
PCB design
├── circuit basics: voltage, current, resistance, Ohm's law, series/parallel
│   └── basic algebra, units
├── components: resistors, capacitors, diodes, transistors, ICs, datasheets
└── schematics: symbols, nets, reading a schematic
```

For a project Goal, add what the project specifically needs. A drone needs aerodynamic lift, thrust-to-weight, a basic PID idea and batteries; it doesn't need fluid dynamics in general. The Diagnostic should cover each branch, not just the Topic itself.

## 2. Plan the questions

Use 10–20 in total. Use fewer when the Topic is narrow or the first answers clearly show beginner or expert level.

- **About 60% on prerequisites** and **40% on the Topic itself** (familiarity, vocabulary, core intuitions).
- **Multiple choice for most of them**: 3 real options plus **"I don't know"**. That option matters. Without it, a lucky guess looks like knowledge and Lesson 1 starts too high.
- **Distractors that reveal misconceptions.** A wrong option should be what someone with a specific wrong model would pick (e.g. "current is used up by the resistor"), so even wrong answers tell you something.
- **1–2 written questions**, asked as plain chat messages:
  - one explanation: "In your own words, what does X do?"
  - one experience check: "Have you ever built/used/calculated X? Tell me briefly."
  Written answers show depth and vocabulary in a way multiple choice can't.
- **Questions that test understanding, not trivia.** "Which change doubles the current?" beats "What is the unit of resistance?"

## 3. Run it adaptively

- Use the question UI with up to 4 questions per call. Don't mark any option as recommended or correct; that would give the answer away.
- Start with the prerequisite questions, at the middle level of difficulty.
- After each batch, adapt:
  - If a prerequisite branch is clearly solid, skip the rest of it.
  - If it's shaky, probe one level lower to find the floor.
  - If everything is easy, jump to harder Topic questions to find the ceiling.
- Don't reveal correct answers mid-Diagnostic. You'd be teaching before you know where to start, and it skews the remaining answers. Go over the answers in the summary instead.

## 4. Summarize

Give a short message in the Learner's language with three groups:

- **Solid**: what they already know (you'll build on this and won't re-teach it).
- **Shaky**: partly there, to review briefly inside a Lesson.
- **Missing**: needs its own teaching, usually Lesson 1 or a review section.

Then add one or two of the most interesting misconceptions you spotted, explained kindly. Record the same three groups in `SYLLABUS.md` under "Starting point".

## Warm-up (a known Topic)

A Warm-up replaces the Diagnostic when the topic file already says what the Learner knows. It checks retention, not prerequisites.

- Ask 3–5 questions, drawn from "What the learner knows" and "Weak spots" in the topic file. Favour the oldest material and the former weak spots.
- If they've forgotten something, add it to the Syllabus as a review section.
- A Warm-up passed after a completed Syllabus is what earns Mastery 5.

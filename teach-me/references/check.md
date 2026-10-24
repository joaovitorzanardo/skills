# Check

The Check decides one thing: did this Lesson's concepts get absorbed? `record_results.py` computes the verdict so it's the same every time. Your job is to grade the written answers fairly, read the pattern behind the mistakes, and choose the next step.

## The results block

The Lesson page produces this block, and the Learner pastes it:

```
TEACH-ME RESULTS v1
{"course":"pcb-design","lesson":"lesson-01","submitted":"2026-10-24T19:02:11Z","answers":{"q1":0,"q2":2,"q6":"Because each branch…"}}
```

Copy everything from `TEACH-ME RESULTS` to the end of the JSON line into a scratch file and pass that file to the script. The rest of the paste might be something else (a question, a comment). Treat that as conversation.

- If the block is mangled (cut off, edited, JSON doesn't parse), the script says so. Ask the Learner to click **Copy results** again; the page keeps their answers.
- If the `course` in the block doesn't match a Course in memory, ask which Course it belongs to. Don't guess.
- If the page ever shows the Learner a different score from the script, the script is right. It uses the answer key in `practice.json`.

## Grading written answers

Grade against the question's `rubric`: 1, 0.5 or 0.
- **Grade understanding, not phrasing.** A correct idea in clumsy words, or in another language, gets full credit.
- **Grade the answer, not the effort.** A long answer built on a wrong model gets 0. A short, right answer gets 1.
- A blank answer gets 0. Mention it kindly, because skipping usually means "I don't know", which is itself useful information.
- Put what you noticed in `--notes`, one short clause per question. Notes go into `PRACTICE_RESULTS.md` and are what a later Remedial Lesson builds on.

## Acting on the verdict

The script prints the verdict, the overall score, and the core concepts that weren't answered fully correctly at least once. Before you act, look at the pattern. Two wrong answers on the same concept with the same kind of mistake mean a wrong mental model. Scattered single misses usually mean carelessness or a badly worded question. If one of your questions turns out to be ambiguous, say so, and don't count it against the Learner in your next step. Leave the recorded score alone.

**Pass.** Lead with what they got right, specifically. Then cover each wrong answer in a sentence or two, because even a passing attempt deserves to have its mistakes explained. In `SYLLABUS.md`, mark the Lesson `passed: <date>, <score>`, adjust the plan if the results showed something new (e.g. a concept that will need reinforcement), then hand off to a new Session for the next Lesson (SKILL.md, "Handoff").

**Fail, first time on these concepts.** Say plainly which concepts didn't land and what the answers suggest they're thinking. Ask whether they want to talk any of it through right now. If they don't, add `lesson-NN-remedial-1` to the Syllabus under "Changes" and hand off to a new Session to write it (see lesson-writing.md, section 5).

**Fail, second time on the same concepts.** Another Lesson in the same format is unlikely to work. Switch to conversation:
1. Ask them to explain the concept in their own words, or to talk you through how they answered one of the missed questions.
2. Find the specific wrong belief. Usually it's one small thing: a sign, a definition, which quantity depends on which.
3. Fix it with them using questions, a fresh example, or a quick sketch in the chat. Let them do the reasoning.
4. Close with a short Remedial Lesson: a recap section and 3–5 new questions.

If a concept fails a third time, that usually means a missing prerequisite. Look back at the Diagnostic, consider adding a prerequisite Lesson to the Syllabus, and tell the Learner why.

**Syllabus complete.** Sum up honestly what they can now do, connected to their Goal. Suggest a next step: a related Topic, a deeper one, or a small project that uses what they learned. Set Mastery to 4.

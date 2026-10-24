# Teach Me

A learning accelerator: it finds out what a Learner already knows about a Topic, teaches it in Lessons, and moves on only once Practice shows the Lesson was learned.

## People and subjects

**Learner**:
The person being taught.
_Avoid_: User, student

**Profile**:
The Learner's own description of who they are and how they like to learn. Written by the Learner and changed only with their consent.
_Avoid_: PROFILE.md, user profile

**Topic**:
A single, teachable subject the Learner asks to learn, narrower than a field.
_Avoid_: Subject, area, concept

**Goal**:
Why the Learner wants to learn a Topic, from plain curiosity to a concrete project that needs it.
_Avoid_: Motivation, reason

## Teaching loop

**Session**:
One invocation of the skill, or one pasted block of Practice Results. A Session writes at most one Lesson. The first Session for a Topic covers the Goal, the Diagnostic and Lesson 1. A later one starts from a Handoff and writes the next Lesson, or starts with a Check and ends with a Handoff.
_Avoid_: Study session, run

**Course**:
Everything taught for one Topic: its Syllabus, Lessons and Practice Results. It is separate from the Learner's memory, which holds only what was learned.
_Avoid_: Class, track

**Diagnostic**:
The 10–20 questions asked before any Lesson to measure the Learner's prerequisites and familiarity with the Topic.
_Avoid_: Evaluation, assessment, placement test

**Warm-up**:
A short 3–5 question Diagnostic that replaces the full one when the Topic is already in memory.
_Avoid_: Refresher quiz

**Syllabus**:
The ordered plan of Lessons for a Topic, prerequisite Lessons first. It is revised after each Check.
_Avoid_: Curriculum, course plan

**Lesson**:
One unit of teaching material on a Topic, ending in Practice and listing its sources.
_Avoid_: Lecture, class, module

**Remedial Lesson**:
A Lesson that reteaches only the concepts a failed Check found were not absorbed.
_Avoid_: Review lesson, retry

**Practice**:
The exercise at the end of a Lesson. It can be multiple choice, written answers or an interactive task.
_Avoid_: Test, quiz, exam

**Practice Results**:
The Learner's recorded answers and score for a Lesson's Practice.
_Avoid_: Test results

**Check**:
Judging the Practice Results to decide whether the Learner passed the Lesson or needs a Remedial Lesson. A Lesson passes at ≥ 80% correct with every core concept answered correctly at least once.
_Avoid_: Evaluation, grading

**Handoff**:
The short note a Session writes after a Check when another Lesson is due. A new Session starts from it and writes that Lesson, so a single Session's context never has to hold more than one Lesson.
_Avoid_: Continuation, resume prompt

**Mastery**:
A 1–5 rating of how well the Learner knows a Topic, based on Practice Results, not on how much was covered.
_Avoid_: Level, progress

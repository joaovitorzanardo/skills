# One Lesson per Session, continued through a Handoff

After a Check that calls for another Lesson, the Session doesn't write it. It asks the Learner whether to move on, updates memory, writes a short `HANDOFF.md` in the Course folder, and runs `launch_session.py`, which opens a new terminal running `claude` with the Handoff as its first prompt. The new Session writes the Lesson. We chose this because each Lesson brings web research and a large page into the context, and a Course worked through in one conversation would eventually fill it.

## Considered Options

- **Keep going in the same Session** (the previous behaviour): no friction, but the context grows by a whole Lesson each round until it runs out or gets summarized mid-Course.
- **Tell the Learner to start a new Session themselves**: works everywhere, but it's one more chore at the moment they want to keep going.
- **Handoff plus automatic launch**: the new Session opens on its own, and the command is printed only where no terminal can be opened.

## Consequences

- The Handoff is deliberately thin. Memory and `SYLLABUS.md` are the source of truth, and the Handoff carries only what the Check noticed that they don't record (misconceptions, pace).
- Memory is updated before the Handoff, so the new Session retrieves the current state.
- A second fail stays in the same Session: the conversation that finds the wrong model is the material for its short Remedial Lesson.
- Launching is platform-specific (Windows Terminal on WSL, Terminal.app, common Linux terminals). Elsewhere `launch_session.py` exits with code 3 and prints the command to run.

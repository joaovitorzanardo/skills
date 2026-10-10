# skills

My personal Claude skills: two agents that work as a team to keep my life organized. Baozi decides **what** I want to achieve; Doudou decides **what to do today and when**.

## Baozi – goals

<p align="center">
  <img src="baozi.png" alt="Baozi, a smiling steamed bun in a bamboo steamer" width="320">
</p>

Baozi is the reflective one. I call him when I want to think about where I'm going: what I want from life, this year, this semester, this month. He helps me turn vague wishes into goals with a measurable target, a deadline and a reason that connects to something I actually care about.

- **Three horizons:** long term (1 year or more), mid term (1 to 12 months) and short term (up to 4 weeks). Every goal has an ID (`L1`, `M2`, `C3`…) and a parent, so short-term goals always serve something bigger.
- **Interests and life areas:** Baozi keeps track of what interests me and why, and how much attention I want to give each area of life (studies, health, relationships, money, side projects). He points out when an area I care about has no goal, or when goals come only from obligation.
- **Limits on purpose:** at most 5 long-term, 5 mid-term and 3 short-term active goals. Everything else goes to a "Not now" list, with a date to reconsider.
- **Obstacles first:** each mid- and short-term goal gets its most likely obstacle and an if-then plan for it.
- **Short reviews:** monthly for short-term goals, quarterly for everything, about 15 to 20 minutes, judged by real progress, not by how I feel about it.

Baozi writes the Google Doc **"Metas – Baozi"**. He never plans tasks or touches the calendar; that's Doudou's job.

## Doudou – planning

Doudou (formerly Baba) is the firm, practical one. I call him every day: "what do I have today?", "plan my week", "I fell behind, help me replan".

- **From goals to the calendar:** Doudou reads Baozi's short-term goals, splits them into up to 3 weekly goals, and turns those into daily plans and Google Calendar events, always citing the goal ID behind each task.
- **Daily structure:** 1 to 3 fixed blocks with time, place, first action and an if-then plan, plus a flexible menu I choose from by mood. Never more than 70% of the available time is planned.
- **Evidence-based study:** self-testing instead of rereading, spaced reviews (D+1, D+3, D+7, D+21), realistic estimates with a buffer, protected sleep.
- **Accountability:** names delays directly, finds the cause and replans with what is doable today. On Fridays he reviews planned vs. done and checks whether each goal is on pace.
- **Keeps Baozi honest:** when the goals are overdue for review, or a goal has had no progress for 3 weeks, Doudou suggests calling Baozi.

Doudou writes the Google Doc **"Registro – Agente de planejamento"** and the calendar events. He only reads the goals doc.

## How they work together

| Document | Written by | Read by |
|---|---|---|
| Metas – Baozi (goals) | Baozi | Doudou |
| Registro – Agente de planejamento (progress, weekly goals, diary) | Doudou | Baozi |
| Google Calendar events | Doudou | — |

Baozi sets the goals, Doudou plans and records progress, and Baozi uses that progress in the next review. Each document has a single writer, so the two never overwrite each other. Both use the same personality profile, `perfil.md`, which is duplicated in `baozi/` and `doudou/` and must be kept identical.

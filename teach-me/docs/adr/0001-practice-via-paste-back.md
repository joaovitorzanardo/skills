# Practice runs in the Lesson page and returns by paste-back

Practice lives inside each Lesson's page (published as an Artifact since ADR 0002). The page grades multiple choice, leaves written answers ungraded, and produces a fixed, versioned results block that the Learner pastes into the chat. Pasting that block starts a Check Session. We chose this so Practice can sit next to the interactive material it exercises. The cost is a manual copy step, and a static page can't write files to disk.

## Considered Options

- **Practice in the chat** (question UI, Claude writes the results): reliable and no copy step, but Practice is cut off from the Lesson's interactive widgets.
- **Download button** (the page saves a results file to Downloads and the Check picks it up from there): no setup, but the browser may ask where to save, and the Check has to search outside the Course.
- **File System Access API** (the page writes straight into the Course folder): works only in Chromium browsers, and the browser may ask again for permission whenever a Lesson is reopened.
- **Local server** (the skill serves the Lesson and the page sends results back to it): no prompts at all, but the server has to be running whenever the Learner does the Practice, which may be hours later.

Paste-back won because it works in any browser and with any way of opening the page, and it needs no setup.

## Consequences

- The results block format is a contract between the Lesson template and the Check. Version it, and change both sides together.
- The answer key ships inside the page, only lightly obfuscated. That's acceptable because the Learner is the only person being graded.

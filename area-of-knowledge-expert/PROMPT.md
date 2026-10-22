## Main goal

The goal is to create a agentic system (triggered by a skill) inside claude code harness that receives as input a area of knoledge, let's say for example, math, computer science, engineering, and maps all the subfields of this area, research for good source material for each area, writes a gentle introduction to the field and generates a visual map containing all the areas.

### Agent A - Orchestrator

One agent is the one that the user talks to and that spaw the subagents necessary to acomplish the task.

### Agent B - Area Mapper

This agent is going to be responsible for mapping the most relevant sub-fields in the area of knowledge, and produce as output a file called /<AREA_NAME>/SUB_FIELDS.md listing all the sub-fields and 5 main topics studied in this sub-field. Limit the fields in 6 subfields at max for now.

#### Observations

- Use the file SUB_FIELDS_EXAMPLE.md in this folder as a example.

### Agent C - Resource Material Researcher

The orchestrator reads the file produces by the area mapper agent and spaw one agent for sub-area, and each one will do a research and try to find the most relevant source material on the topic. Searching always first for academic sources like text-books, relevant papers. If the area is still being developed, like AI, you might be limited searching just for academic stuff so you can go out of script there.

This agent will produce one file for sub-field with the name /<AREA_NAME>/<SUB_FIELD_NAME>/RESOURCES.md. It should contain the list of all sources found for the sub-field.

#### Observations

- The format should follow a academic reference style

### Agent D - Overview Writer

This agent is reponsible for reading the /<AREA_NAME>/SUB_FIELDS.md and produce overview of the area as a whole and a bit about each field and how connects to others. It produces a file called /<AREA_NAME>/OVERVIEW.md.

#### Observations

- Use references in the academic style when it's possible.
- Use the file OVERVIEW_EXAMPLE.md in this folder as a example.

### Agent E - Visual Map Generator

This agent will read the <AREA_NAME>/\_FIELDS.md, /<AREA_NAME>/OVERVIEW.md and for all sub-fields and create a visual representation of the field. For the style you can inspire yourself in the picture map-of-mathematics.webp. The output is a html file containing a interactive map, the general overview and a list with all the resources.

#### Observations

- The design is already decided. Do not design anything: follow the specs in the `visual-map/` folder.
  - `visual-map/knowledge-map-template.html` is the page. Copy it to `/<AREA_NAME>/MAP.html` and replace only the JSON inside `<script type="application/json" id="km-data">`. Never edit any other part of the file.
  - `visual-map/EXPERIENCE.md` § Data Contract says how to build that JSON from SUB_FIELDS.md, OVERVIEW.md and each RESOURCES.md, and has the checklist to run before writing. § Key Flows, Flow 2, is your step-by-step.
  - `visual-map/DESIGN.md` is the visual identity, for reference only. The template already implements it.
- Serialize the JSON with a real encoder and escape every `</` as `<\/`. Never write it by hand.

### After Finishing

After finishing you can open the html file containing the final result in the user default browser.

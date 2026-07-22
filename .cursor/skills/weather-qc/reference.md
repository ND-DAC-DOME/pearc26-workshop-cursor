# Project skills (quick reference)

A **project skill** is a markdown playbook the agent follows for a repeatable
workflow. In this repo, skills live under `.cursor/skills/<skill-name>/` with a
required `SKILL.md`.

## Using a skill in chat

- Open or `@`-mention `.cursor/skills/weather-qc/SKILL.md` when planning or
  implementing plotting/QC work so the agent loads these rules.
- Prefer completing the skill’s TODO sections *before* asking the agent to
  change `scripts/plot_wind_map.py`.

## Authoring tips

- Keep rules concrete and testable (“drop rows with wind_speed_mps < 0”).
- Say what *not* to do (e.g. do not impute wind from neighbors).
- Point at real paths in this repo when relevant.

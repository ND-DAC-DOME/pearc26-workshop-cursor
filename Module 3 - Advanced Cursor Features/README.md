# PEARC26 Cursor Workshop Module 3 — Advanced Cursor Features: Weather Patterns


## Prerequisites

Please make sure to have completed the pre-conference installation instructions found in this repository's root README file:

- [ ] Cursor installed and signed in  
- [ ] Python 3.10+ available (`python3 --version`)  
- [ ] Git available (`git --version`)  
- [ ] This repo cloned  
- [ ] Module 3 venv created and `pip install -r requirements.txt` succeeded

---

## Step 1 — Wind map

Plot meteorological wind barbs across the contiguous United States using the provided dataset in `data/` (~500 real CONUS stations with a week of hourly readings). See [data/README.md](data/README.md) for schema and units.

The dataset spans one week of hourly readings (`2025-06-09` through `2025-06-15`). Each run plots a **single** timestamp. For example, Wednesday noon UTC:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-11T12:00:00Z
```

Writes `output/wind_map.png` — open the PNG.

---

## Step 2 — Investigate a severe weather event

On the evening of **Friday, 13 June 2025**, a strong storm cell moved through central Oklahoma. Start by mapping winds around that time — for example:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-13T22:00:00Z
```

Study the map, then use Cursor to inspect the underlying hourly readings.

### Explore the hourly CSV

**Important:** Read these instructions yourself in the editor. During Ask/Agent investigation, attach **only** the data files you want analyzed (e.g. the CSV below). Do **not** `@README.md` — it will leak the exercise framing into the model’s context.

**1. Ask mode + `@File` the dataset**

Switch the chat to **Ask** mode, attach **only** `@data/weather_hourly.csv`, and run an open-ended quality check — for example:

> `@data/weather_hourly.csv` Do a quality check of this weather dataset. Flag any physically impossible or suspicious values.

Try a few follow-ups if the first pass is too broad (e.g. focus on wind, or on a specific evening window).

**2. Narrow the location**

If you find a suspicious `station_id`, you can `@data/stations.csv` (or `@data/README.md` for units) for coordinates and naming. For **hardware/software** details, use the station-metadata MCP in the next section — do not dig through metadata JSON files by hand.

**3. Ask Cursor to quantify**

Have Cursor summarize ranges, count impossible values, or walk the hours around the storm for the affected station — whatever helps you explain *why* the map looked wrong.

### Station metadata MCP (root-cause context)

Each station has hardware/software metadata (platform, sensors, firmware language and typed fields). That catalog is **not** meant to be browsed as raw files during the exercise — query it through a local MCP server so the agent can pull details on demand.

#### Start / connect the MCP server

Switch back to **Agent** mode for this step (Ask mode cannot call MCP tools).

1. This repo ships a project MCP config at [`.cursor/mcp.json`](.cursor/mcp.json) that launches:

```text
.venv/bin/python scripts/station_metadata_mcp.py
```

2. In Cursor: **Settings → MCP**. Confirm **station-metadata** appears and shows a green/connected status. If needed, click refresh/restart after creating the venv.

3. In an **Agent** chat, verify tools such as `get_station`, `get_firmware`, `list_stations`, `search_stations`, and `list_firmware` are available.

#### Discovery path

After you have a suspicious `station_id` from the hourly CSV (still in **Agent** mode):

1. Ask the agent to look up that station **via the station-metadata MCP** (not by opening JSON files in the editor).
2. Follow the station’s `firmware_id` with `get_firmware`.
3. Inspect how that firmware stores wind speed (language, integer width, signedness, range) and connect it to the impossible reading you found.

Example prompts (attach the CSV only if needed; prefer MCP for metadata):

> Using the station-metadata MCP, call `get_station` for the station_id with the impossible wind value. What hardware and software is it running?

> Using the station-metadata MCP, call `get_firmware` for that station’s firmware_id. How is wind speed stored, and could that explain a reading of -127?

---

## Step 3 — Author a Cursor skill, then apply it

Turn what you learned in Step 2 into a **project skill**, then use that skill to harden the wind map. Skills are markdown playbooks under `.cursor/skills/` that teach the agent a repeatable workflow (see [`.cursor/skills/weather-qc/reference.md`](.cursor/skills/weather-qc/reference.md)).

### Author the skill

Open the skeleton at [`.cursor/skills/weather-qc/SKILL.md`](.cursor/skills/weather-qc/SKILL.md) and fill in every `TODO` using your Step 2 findings. You can edit it directly or ask **Agent** mode for help — for example:

> Help me complete `@.cursor/skills/weather-qc/SKILL.md` based on what we learned: legacy signed int8 wind overflow can produce impossible negative speeds. Encode QC rules for plotting — do not invent replacement wind values.

Finish the skill **before** changing plotting code.

### Plan the fix (with the skill)

Switch to **Plan** mode. Attach the skill and the plotting script, and require the plan to follow your QC rules — for example:

> `@.cursor/skills/weather-qc/SKILL.md` `@scripts/plot_wind_map.py` Follow the weather-qc skill. Plan a fix in this plotting script so invalid wind values are handled safely (without silently inventing weather). Keep valid stations plotting as before.

Review the plan (what counts as invalid, drop vs flag, logging/messaging) before coding.

### Implement the fix

Switch to **Agent** mode with the skill still in context and have Cursor implement the agreed plan in `scripts/plot_wind_map.py`.

### Re-run the map

Regenerate the storm-time map and confirm it no longer blows up on the bad value:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-13T22:00:00Z
```

Compare `output/wind_map.png` to your earlier plot. The Oklahoma storm cell should still appear; the impossible barb should not dominate the map.


---

## Step 4 — Project rules (skills vs lasting guidance)

Skills are great for a focused workflow you attach in chat. **Project rules** live under `.cursor/rules/` and give Cursor persistent guidance—optionally scoped to file patterns—so you do not have to `@` a skill every time.

### Author a rule

Open the skeleton at [`.cursor/rules/weather-plotting.mdc.example`](.cursor/rules/weather-plotting.mdc.example). Fill every `TODO` using what you put in the `weather-qc` skill (keep the rule shorter—rules work best as concise must-follow guidance) and rename the file to `weather-plotting.mdc` (remove the `.example` at the end).

You can edit it directly or ask **Agent** mode:

> Help me complete `@.cursor/rules/weather-plotting.mdc` from our weather-qc skill. Keep it concise. It should apply when editing `scripts/plot_*.py`.

Frontmatter already sets `globs: scripts/plot_*.py` so the rule applies when those files are in play (not necessarily on every chat in the repo).

### Use the rule (without attaching the skill)

Start a **new** Agent chat. Open or mention `scripts/plot_wind_map.py`, but **do not** `@` the weather-qc skill. Ask for a small enhancement that should still obey QC—for example:

> `@scripts/plot_wind_map.py` Add a short comment or stderr message near the wind-loading logic reminding maintainers that invalid wind speeds must not be plotted. Follow project rules. Do not weaken QC if it already exists.

Check that the agent follows your rule (and does not invent weather or pull in heavy plotting libraries).

### Optional contrast

In another message, ask the same kind of change **with** `@.cursor/skills/weather-qc/SKILL.md` attached. Discuss with your neighbor: when would you use a **skill** vs a **rule**?


---

## Optional explorations (for fun!)

The week of data includes more than the Oklahoma wind event. Using Ask/Agent (and MCP when useful), see what else you can find—for example:

**Solar Energy Crashes (Monday, 9 June 2025)**
- How does **solar radiation** evolve across different regions that day?
- Do any stations show a brief daytime **temperature dip** lined up with a solar crash?
- Can you map which corridor was darkest?
- What is the explanation for seing this data?

**Midwest Humidity Pulse (11–12 June)**
- Look at **humidity** and **dew point** over the midwest—what agricultural weather story fits a hot, muggy midweek pulse?

**Indiana Morning Rain (every day, ~11:00 UTC)**
- One station reports **100% humidity**, a sharp **temperature drop**, and **heavy precipitation**—at the **same hour every morning**.
- What do the other nearby statiosn read?
- What non-meteorological explanation fits a short, clockwork wet burst under blue skies?

**Southwest heat & outages (14–15 June)**
- Several stations seem to be missing data during the week.
- How does this correlate with other readings going on around this time?
- What could explain the correlation between **temperature change/peaks** and the lack of data? 

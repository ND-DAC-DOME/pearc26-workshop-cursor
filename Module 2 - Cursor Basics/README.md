# PEARC26 Cursor Workshop Module 2 — Cursor Basics: Wind Map


## Prerequisites

Please make sure to have completed the pre-conference installation instructions found in this repository's root README file:

- [ ] Cursor installed and signed in  
- [ ] Python 3.10+ available (`python3 --version`)  
- [ ] Git available (`git --version`)  
- [ ] This repo cloned  
- [ ] Root `.venv` created and `pip install -r requirements.txt` succeeded  

Activate the shared environment from the **repository root** before the steps below:

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
cd "Module 2 - Cursor Basics"
```

---

## Step 1 — Run the starter map

This module ships an **incomplete** plotting script: it loads Mon–Wed station data (`2025-06-09` through `2025-06-11`), draws CONUS state outlines and a title, and writes a PNG. A north-compass helper is stubbed out for Tab completion, and wind overlays are left for the Agent steps.

From `Module 2 - Cursor Basics`:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png`. You should see land/ocean, state borders, and a title band (timestamp + station count). There is **no north arrow** yet and **no wind glyphs**.

Each run plots a **single** timestamp (default: middle of the Mon–Wed window). You can pick another hour if you like:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-10T12:00:00Z
```

---

## Step 2 — Tab completion (north compass)

Open `scripts/plot_wind_map.py` and find `draw_north_compass`. The function body is `pass`, with a detailed comment above it describing the geometry (shaft, small arrowhead, letter `"N"`).

1. Place the cursor in the function body (on `pass` / the blank line after the comment).
2. Use **Tab completion** (Cursor Tab / ghost text) to implement the body from the comment. Prefer accepting the suggestion over rewriting it by hand — the point is to practice Tab.
3. Save and re-run:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png` again. You should see a small north arrow with an `"N"` in the lower-left ocean margin.

---

## How to use the copy-paste prompts below

For Agent and Plan steps:

1. In the chat, **attach the file with Cursor’s @ menu** (or drag the file onto the chat). Choose:

   `Module 2 - Cursor Basics/scripts/plot_wind_map.py`

   Do **not** rely on pasting an `@...` path from this README — text inside code blocks will not create a real attachment.

2. Set the chat mode (**Agent** or **Plan**) as the step says.

3. **Copy the prompt from the fenced block** (the box under “Copy-paste prompt”) and paste it into the chat input, then send.

---

## Step 3 — Agent: show the wind (first pass)

A stakeholder asked to **show the wind** on the map for the selected hour. For a quick first draft, use simple markers (colored dots) — meteorological barbs come later, after a checkpoint, when the requirement gets more specific.

1. Switch the chat to **Agent** mode.
2. Attach `Module 2 - Cursor Basics/scripts/plot_wind_map.py` with **@** (see above).
3. Copy-paste prompt:

```
Work only inside Module 2. Do not use project rules or skills. Do not read, open, or copy from any files outside Module 2 - Cursor Basics/. Show the wind data on this map for the selected hour. Use the station rows already loaded in frame (lon, lat, wind_speed_mps, wind_direction_deg). For this first draft, use simple colored dots at each station (color and/or size by wind speed). Do not implement meteorological wind barbs yet. Keep using Pillow only — do not add matplotlib or cartopy.
```

4. Accept the changes, save, and re-run:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png`. You should see colored dots (or similar simple markers) for wind — not barbs yet.

### Checkpoint

When you are happy with this first pass, create a **checkpoint** (Cursor’s checkpoint / restore point for the Agent edits) so you can return to this state after the next change.

---

## Step 4 — Stakeholder clarity, Plan, rollback, then barbs

After reviewing the map, the stakeholder clarifies the requirement:

> We need **meteorological wind barbs** so direction and speed read the same way as our ops maps. Speed should be in **knots**, and direction is **from which the wind blows**.

### Plan the change

1. Switch the chat to **Plan** mode.
2. Attach `Module 2 - Cursor Basics/scripts/plot_wind_map.py` with **@**.
3. Copy-paste prompt:

```
Work only inside Module 2. Do not use project rules or skills. Do not read, open, or copy from any files outside Module 2 - Cursor Basics/. Plan how to replace the current wind overlay with meteorological wind barbs. Speed in knots; direction is meteorological (from which the wind blows). Keep Pillow only — do not add matplotlib or cartopy. Do not write code yet — outline the approach and which functions to add or change.
```

4. Review the plan. Adjust it in chat if anything looks off (glyph design, where the loop lives, units).

### Restore, then implement with Agent

1. **Restore** the checkpoint from Step 3 (undo the first-draft wind encoding).
2. Switch to **Agent** mode.
3. Attach `Module 2 - Cursor Basics/scripts/plot_wind_map.py` with **@** (if it is not still attached).
4. Copy-paste prompt:

```
Work only inside Module 2. Do not use project rules or skills. Do not read, open, or copy from any files outside Module 2 - Cursor Basics/. Implement the plan we just agreed: meteorological wind barbs, speed in knots, meteorological direction. Keep Pillow only; do not add matplotlib or cartopy.
```

5. Accept the changes, save, and re-run:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png`. You should see wind barbs across CONUS.

---

## What we practiced

- Running a project script from a shared venv  
- **Tab completion** for a small, comment-guided stubbed function  
- **Agent** mode for a quick first-draft feature  
- **Plan** mode to design a more specific change before coding  
- **Checkpoints / rollback** when requirements change after review  

Module 3 continues with the **full week** of data, quality issues, skills, rules, and MCP — leave that for the next session.

---

## Optional: pick another hour

Still in Module 2’s Mon–Wed window, try a different timestamp and regenerate the map:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-09T18:00:00Z
python scripts/plot_wind_map.py --hour-index 0
```

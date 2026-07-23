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

Open `output/wind_map.png`. You should see land/ocean, state borders, and a title band. There is **no north arrow** yet and **no wind glyphs**.

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

## Step 3 — Agent: show the wind (first pass)

A stakeholder asked to **show the wind** on the map for the selected hour, but did **not** specify the glyph style.

1. Switch the chat to **Agent** mode.
2. Attach `@scripts/plot_wind_map.py` (and data only if needed).
3. Ask for a reasonable first implementation — for example:

> `@scripts/plot_wind_map.py` Show the wind data on this map for the selected hour. Use the station rows already loaded in `frame` (lon, lat, wind_speed_mps, wind_direction_deg). Pick a clear visual encoding that makes sense for a first draft. Keep using Pillow only — do not add matplotlib or cartopy. Leave `draw_north_compass` alone.

4. Accept the changes, save, and re-run:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png`. You should see wind represented somehow (often colored dots or similar).

### Checkpoint

When you are happy with this first pass, create a **checkpoint** (Cursor’s checkpoint / restore point for the Agent edits) so you can return to this state after the next change.

---

## Step 4 — Stakeholder clarity + rollback + barbs

After reviewing the map, the stakeholder clarifies the requirement:

> We need **meteorological wind barbs** so direction and speed read the same way as our ops maps. Speed should be in **knots**, and direction is **from which the wind blows**.

1. **Restore** the checkpoint from Step 3 (undo the first wind encoding).
2. In **Agent** mode, ask for barbs instead — for example:

> `@scripts/plot_wind_map.py` Replace the wind overlay with meteorological wind barbs. Convert speed to knots for the barb encoding. Direction is meteorological (from which the wind blows). Keep Pillow only; do not add matplotlib or cartopy. Keep the north compass from Step 2.

3. Save and re-run:

```bash
python scripts/plot_wind_map.py
```

Open `output/wind_map.png`. You should see wind barbs across CONUS (and still the north arrow).

---

## What we practiced

- Running a project script from a shared venv  
- **Tab completion** for a small, comment-guided stubbed function  
- **Agent** mode for a larger feature with a vague request  
- **Checkpoints / rollback** when requirements change after review  

Module 3 continues with the **full week** of data, quality issues, skills, rules, and MCP — leave that for the next session.

---

## Optional: pick another hour

Still in Module 2’s Mon–Wed window, try a different timestamp and regenerate the map:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-09T18:00:00Z
python scripts/plot_wind_map.py --hour-index 0
```

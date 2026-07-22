---
name: weather-qc
description: >-
  Quality-control rules for ASOS/CONUS weather plotting and analysis in this
  workshop. Use when editing or writing wind/weather map scripts, handling
  suspicious sensor values, or applying QC before visualization.
---

# Weather QC

Project skill for plotting and analyzing workshop weather data. Complete the
TODO sections below using what you learned in Step 2 before applying this
skill to code changes.

## When this skill applies

TODO: List the tasks and file types this skill should guide (e.g. wind maps,
hourly CSV QC, related plotting scripts).

## What counts as invalid wind data

TODO: Define physically impossible or corrupted wind values the agent must
treat as invalid. Base this on Step 2 findings (do not invent new physics).

## How to treat invalid rows

TODO: Specify required behavior when invalid wind values appear.

- Prefer dropping or flagging bad rows over guessing replacements.
- Do **not** invent replacement wind speeds or directions.
- Say whether direction should be ignored when speed is invalid.

## Logging and messaging

TODO: What should the script or agent report when it skips bad data?
(e.g. count of dropped stations, example `station_id`, stderr vs stdout.)

## Preserve existing behavior for valid stations

TODO: Note CLI flags, output path, Cartopy CONUS styling, and barb conventions
that must stay the same for stations with valid wind.

## Out of scope

TODO: Anything this skill should *not* change (dataset regeneration, MCP
server, unrelated metrics).

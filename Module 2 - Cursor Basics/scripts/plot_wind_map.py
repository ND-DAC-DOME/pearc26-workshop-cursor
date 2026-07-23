#!/usr/bin/env python3
"""Plot CONUS wind speed and direction as meteorological wind barbs (PNG).

Reads data/stations.csv and data/weather_hourly.csv, selects one hour, and
writes output/wind_map.png. Uses stdlib + Pillow only (no matplotlib/cartopy).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"
BASEMAP_PATH = DATA_DIR / "basemap" / "conus_states.json"

# CONUS map extent (lon/lat)
LON_MIN, LON_MAX = -125.5, -66.0
LAT_MIN, LAT_MAX = 24.0, 50.0
# High-res output for workshop screens / projectors
IMG_WIDTH = 2800
IMG_HEIGHT = 1800
MARGIN = 112
TITLE_BAND = 88

OCEAN = (214, 232, 240)
LAND = (242, 239, 230)
LAND_EDGE = (85, 85, 85)
TITLE_COLOR = (26, 26, 26)


def load_frame(
    stations_path: Path,
    readings_path: Path,
    timestamp: str | None,
    hour_index: int | None,
) -> tuple[list[dict], str]:
    with stations_path.open(newline="", encoding="utf-8") as f:
        stations = {row["station_id"]: row for row in csv.DictReader(f)}

    with readings_path.open(newline="", encoding="utf-8") as f:
        readings = list(csv.DictReader(f))

    timestamps = sorted({row["timestamp_utc"] for row in readings})
    if not timestamps:
        raise SystemExit("No timestamps found in weather_hourly.csv")

    if timestamp is not None:
        chosen = timestamp
        if chosen not in timestamps:
            matches = [t for t in timestamps if t.startswith(chosen.rstrip("Z"))]
            if not matches:
                raise SystemExit(
                    f"Timestamp {timestamp!r} not in dataset. "
                    f"Example: {timestamps[len(timestamps) // 2]}"
                )
            chosen = matches[0]
    elif hour_index is not None:
        if hour_index < 0 or hour_index >= len(timestamps):
            raise SystemExit(
                f"--hour-index must be 0..{len(timestamps) - 1}, got {hour_index}"
            )
        chosen = timestamps[hour_index]
    else:
        chosen = timestamps[len(timestamps) // 2]

    frame: list[dict] = []
    for row in readings:
        if row["timestamp_utc"] != chosen:
            continue
        st = stations.get(row["station_id"])
        if not st:
            continue
        frame.append(
            {
                "station_id": row["station_id"],
                "lon": float(st["lon"]),
                "lat": float(st["lat"]),
                "wind_speed_mps": float(row["wind_speed_mps"]),
                "wind_direction_deg": float(row["wind_direction_deg"]),
            }
        )
    if not frame:
        raise SystemExit(f"No joined rows for timestamp {chosen}")
    return frame, chosen


def project_xy(
    lon: float,
    lat: float,
    *,
    width: int,
    height: int,
    margin: int,
    title_band: int,
) -> tuple[float, float]:
    plot_w = width - 2 * margin
    plot_h = height - 2 * margin - title_band
    x = margin + (lon - LON_MIN) / (LON_MAX - LON_MIN) * plot_w
    y = margin + title_band + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * plot_h
    return x, y


def iter_polygons(geom: dict):
    """Yield exterior rings (holes outlined separately)."""
    gtype = geom["type"]
    coords = geom["coordinates"]
    if gtype == "Polygon":
        yield coords[0]
    elif gtype == "MultiPolygon":
        for poly in coords:
            yield poly[0]


def iter_all_rings(geom: dict):
    gtype = geom["type"]
    coords = geom["coordinates"]
    if gtype == "Polygon":
        for ring in coords:
            yield ring
    elif gtype == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                yield ring


def ring_to_pixels(ring: list, proj) -> list[tuple[float, float]]:
    return [proj(float(lon), float(lat)) for lon, lat in ring]


def draw_states(draw: ImageDraw.ImageDraw, basemap_path: Path, proj, edge_width: int) -> None:
    geo = json.loads(basemap_path.read_text(encoding="utf-8"))
    for feat in geo["features"]:
        geom = feat["geometry"]
        for exterior in iter_polygons(geom):
            pts = ring_to_pixels(exterior, proj)
            if len(pts) >= 3:
                draw.polygon(pts, fill=LAND)
        for ring in iter_all_rings(geom):
            pts = ring_to_pixels(ring, proj)
            if len(pts) >= 2:
                draw.line(pts + [pts[0]], fill=LAND_EDGE, width=edge_width)


def draw_north_compass(
    draw: ImageDraw.ImageDraw,
    *,
    width: int,
    height: int,
    scale: int,
    font: ImageFont.ImageFont,
) -> None:
    # Draw a small north arrow in the lower-left ocean margin (decoration only).
    # North is toward the top of this map. Pillow y increases downward.
    #
    # Anchor: cx = 80 * scale, base_y = height - 64 * scale
    #   tip_y       = base_y - 48 * scale   # top of arrowhead
    #   head_base_y = tip_y + 16 * scale    # bottom of arrowhead (just below tip)
    #
    # Draw in this order, all TITLE_COLOR, stroke ~ max(2, 2 * scale):
    #   1) Shaft: vertical line from (cx, head_base_y) down to (cx, base_y)
    #      — do NOT extend the line through the arrowhead.
    #   2) Arrowhead: a SMALL filled triangle only at the top:
    #        (cx, tip_y),
    #        (cx - 10 * scale, head_base_y),
    #        (cx + 10 * scale, head_base_y)
    #      Triangle height stays ~16*scale — not a tall "tree" shape.
    #   3) Label "N" with the provided font. Measure with textbbox:
    #        tw = bbox[2] - bbox[0];  th = bbox[3] - bbox[1]
    #      draw.text y is the TOP of the glyphs, so place the letter with a
    #      clear gap above the tip:
    #        text_x = cx - tw / 2
    #        text_y = tip_y - th - 12 * scale
    #      The "N" must not overlap the arrowhead.
    #
    # No new imports. Do not draw wind glyphs or change the title.
    # Accept Tab completion to implement the body of this function.
    pass


def plot_wind_map(frame: list[dict], timestamp: str, basemap_path: Path, output_path: Path) -> None:
    # Render at 2x then downscale with LANCZOS for smoother edges
    scale = 2
    width, height = IMG_WIDTH * scale, IMG_HEIGHT * scale
    margin = MARGIN * scale
    title_band = TITLE_BAND * scale

    def proj(lon: float, lat: float) -> tuple[float, float]:
        return project_xy(
            lon, lat, width=width, height=height, margin=margin, title_band=title_band
        )

    img = Image.new("RGB", (width, height), OCEAN)
    draw = ImageDraw.Draw(img)
    draw_states(draw, basemap_path, proj, edge_width=3 * scale)

    title = (
        f"CONUS Wind Speed & Direction — {timestamp} — "
        f"{len(frame)} stations — barbs in knots"
    )
    font_size = 20 * scale
    try:
        font = ImageFont.truetype("Helvetica", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), title, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 12 * scale), title, fill=TITLE_COLOR, font=font)

    draw_north_compass(draw, width=width, height=height, scale=scale, font=font)

    img = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.LANCZOS)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="PNG", optimize=True)
    print(f"Wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="UTC timestamp to plot (must match weather_hourly.csv values)",
    )
    parser.add_argument(
        "--hour-index",
        type=int,
        default=None,
        help="0-based hour index within the week (alternative to --timestamp)",
    )
    parser.add_argument(
        "--stations",
        type=Path,
        default=DATA_DIR / "stations.csv",
        help="Path to stations.csv",
    )
    parser.add_argument(
        "--readings",
        type=Path,
        default=DATA_DIR / "weather_hourly.csv",
        help="Path to weather_hourly.csv",
    )
    parser.add_argument(
        "--basemap",
        type=Path,
        default=BASEMAP_PATH,
        help="Path to CONUS states GeoJSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR / "wind_map.png",
        help="Output PNG path",
    )
    args = parser.parse_args()

    if not args.stations.exists() or not args.readings.exists():
        raise SystemExit("Missing data files under data/ (stations.csv, weather_hourly.csv).")
    if not args.basemap.exists():
        raise SystemExit(f"Missing basemap: {args.basemap}")

    frame, chosen = load_frame(args.stations, args.readings, args.timestamp, args.hour_index)
    plot_wind_map(frame, chosen, args.basemap, args.output)


if __name__ == "__main__":
    main()

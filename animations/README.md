# Animation system

There's no separate animation runtime in this repo — every animation lives
inside its SVG file as native SMIL (`<animate>`, `<animateMotion>`) or a
gradient whose stops move. This file documents the shared timing/technique
vocabulary so the assets stay consistent when edited via
`scripts/build_theme_svgs.py`.

## Techniques used, by asset

| Asset | Technique |
|---|---|
| `hero.svg` | Radial gradient "glow" blobs drifting on `cy`; floating particle dots fading via `opacity`; gradient-fill title text; pulsing card border `stroke-opacity`. |
| `typing.svg` | Per-phrase `<clipPath>` with a `<rect>` whose `width` animates 0 → full → 0 on `keyTimes`, revealing/hiding each role title in sequence; a single cursor `<rect>` whose `x` tracks the same keyframes, plus an independent fast blink. |
| `terminal.svg` | Each line's `opacity` animates on its own slice of one shared, looping timeline (`keyTimes`), so lines appear to type in one after another; a blinking cursor rect; a soft horizontal "glow sweep" rect drifting left→right. |
| `skills.svg`, `projects.svg`, `contact.svg` | Card border `stroke-opacity` pulses on a loop, staggered per-card with a `begin` offset, standing in for a hover state that static `<img>`-embedded SVG can't receive from the mouse. |
| `timeline.svg` | A dash-offset animation draws the connecting line; each node's outer ring pulses radius + opacity in sequence down the timeline. |
| `footer.svg` | A wave `<path>` morphs between two curve definitions; star dots fade in/out independently; one particle travels the full width via `<animateMotion>`. |
| `divider.svg` | A bright "shine" segment sweeps left→right across a static gradient line; the center dot pulses. |

## Timing conventions

- **Loop durations** cluster around 2.5s–10s — fast enough to read as "alive"
  in a screenshot, slow enough not to be distracting in a document you're
  meant to read.
- **Stagger offsets** (`begin="0.5s"`, `begin="1s"`, …) are used whenever
  multiple copies of the same animation appear in one asset (e.g. four skill
  cards), so they don't all pulse in unison.
- **`repeatCount="indefinite"`** on every looping animation — nothing plays
  once and stops.

## Why not CSS `@keyframes` instead of SMIL?

Both work when the SVG is embedded via `<img src="...">` in a GitHub
markdown file. SMIL was used here because `keyTimes`/`values` is a more
direct match for "reveal a clip-path rect on a precise multi-phrase
schedule" than CSS keyframes would be, and it keeps every animation
self-contained inside a single element instead of needing a separate
`<style>` block per asset.

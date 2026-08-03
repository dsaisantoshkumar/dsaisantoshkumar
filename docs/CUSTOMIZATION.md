# Customizing this profile

Every visual asset in `assets/dark/` and `assets/light/` is **generated**, not
hand-edited. The real source of truth is `scripts/build_theme_svgs.py` — it
holds the content (name, roles, skills, projects, timeline, contact links)
and the two color palettes, and writes out all 18 SVG files from that single
source. To change anything:

1. Open `scripts/build_theme_svgs.py`.
2. Edit the relevant Python list/dict near the top of the file:
   - `ROLES` — phrases that rotate in the typing animation.
   - `SKILL_GROUPS` — skill category cards.
   - `PROJECTS` — featured project cards.
   - `TIMELINE` — the career/education roadmap.
   - `CONTACTS` — the contact cards (label, display text, URL).
   - `TERMINAL_LINES` — the lines shown in the terminal animation.
   - `DARK` / `LIGHT` — the two color palettes (currently copied 1:1 from
     `saisantoshkumard/css/style.css` so this profile and the portfolio site
     stay visually identical).
3. Re-run it:

   ```bash
   python3 scripts/build_theme_svgs.py
   ```

   This regenerates every file in `assets/dark/` and `assets/light/`
   consistently — you never hand-edit the generated SVGs directly.
4. Run `scripts/validate_svgs.py` to make sure everything still parses
   before committing:

   ```bash
   python3 scripts/validate_svgs.py
   ```

## Changing the GitHub stats widgets

The GitHub Analytics section in `README.md` uses three public, actively
maintained services (not this repo's own code):

- [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) — stats card + top languages
- [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) — streak card
- [github-readme-activity-graph](https://github.com/Ashutosh00710/github-readme-activity-graph) — contribution graph
- [github-profile-trophy](https://github.com/ryo-ma/github-profile-trophy) — trophy case

To point these at a different account, replace `username=dsaisantoshkumar`
(or `user=` for the streak widget) in each URL. The hex colors already in the
URLs match the `DARK`/`LIGHT` palettes above — update both together if you
change the color scheme.

## Known limitations (read before assuming something is broken)

- **Dark/light switching follows your operating system's color scheme, not
  GitHub's own light/dark toggle.** The `<picture>` + `prefers-color-scheme`
  technique used throughout this README is GitHub's officially supported way
  to ship theme-aware images, but it only reacts to your OS/browser setting.
  If your OS is set to light mode and you've manually switched GitHub's site
  theme to dark, the images will still show the light variant. This is a
  platform constraint, not a bug in these assets.
- **No true `:hover` interactivity.** SVGs embedded via `<img src="...">` are
  treated as static images by the browser — they don't receive mouse events,
  so real hover states aren't possible. Every place the brief asked for a
  "hover illusion" (project card glow, skill card border, contact card
  border) is instead an looping animation that pulses on its own, which reads
  as alive without depending on the cursor.
- **No JavaScript, anywhere.** Every animation is SMIL (`<animate>`,
  `<animateMotion>`) or a passive SVG gradient — this is what makes it
  compatible with GitHub's markdown sanitizer, which strips `<script>` tags.
- **The typing animation is hand-built, not a hosted service.** It uses
  chained `<animate>` elements with `keyTimes`/`values` on a clip-path to
  simulate typing and deleting text, entirely inside `typing.svg`. It doesn't
  call out to any external API.
- **Static SVG preview tools (e.g. `cairosvg`, some IDE SVG previewers) don't
  render SMIL animation at all** — they'll show a flat, sometimes-blank
  frame. This is a limitation of those tools, not the file. Open the SVG in
  an actual browser (or view it live on GitHub) to see the real animation.

# Portable SVG delivery

Separate the default drawing from optional viewer features. A complete light drawing must render without CSS; dark mode is an enhancement for viewers that support `prefers-color-scheme`. Do not infer viewer support from the operating system or the `.svg` extension.

## Baseline attributes and dark mode

Use concrete `fill`, `stroke`, `stroke-width`, `font-family`, `font-size`, and `font-weight` attributes on the relevant elements or inherited groups. A class name alone does not provide a fallback. Set `fill="none"` on open connections and explicitly color arrowheads. Avoid `var(...)`, `context-stroke`, and `currentColor` in essential paint values.

For example:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 160"
     role="img" aria-labelledby="example-title example-desc">
  <title id="example-title">Build step</title>
  <desc id="example-desc">A compilation step with an optional dark theme.</desc>
  <style>
    @media (prefers-color-scheme: dark) {
      .canvas { fill: #141a21; }
      .node { fill: #1c2b3a; stroke: #94b8da; }
      .label { fill: #e3eaf0; }
    }
  </style>
  <rect width="400" height="160" fill="#ffffff" class="canvas"/>
  <rect x="40" y="40" width="320" height="80" rx="6"
        fill="#eef3f8" stroke="#426b91" stroke-width="1.5" class="node"/>
  <text x="200" y="90" text-anchor="middle" fill="#25313a" class="label"
        font-family="Arial, 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', 'Source Han Sans CN', sans-serif"
        font-size="24">Compilation</text>
</svg>
```

Limit theme overrides to concrete paint colors. Do not change node geometry, text positions, font metrics, or content between themes. Use `href` plus `xlink:href` with the XLink namespace for a retained `<use>` that must work in older SVG viewers, or expand the small shape directly. Templates provide editable light baselines; add dark mode when requested.

## Fonts and delivery modes

- **Editable source:** retain `<text>` and `<tspan>`, with fallback fonts and room for metric differences. Suggested sans-serif stack: `Arial, 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', 'Source Han Sans CN', sans-serif`. For code, use `Consolas, Menlo, 'DejaVu Sans Mono', 'Liberation Mono', 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', monospace`. Confirm that the chosen local fonts cover the actual characters. A generic fallback cannot supply missing Chinese glyphs.
- **Font-independent sharing:** retain `diagram.editable.svg`, and outline its text into `diagram.svg` using an already installed exporter. Outlines fix glyph appearance and positions without embedding fonts. They increase file size and remove normal text selection/editing, so preserve useful `title`/`desc` and the editable source. Do not claim font independence for a file that still contains visible text elements.

If `rsvg-convert` is installed, the bundled helper outlines a presentation-attribute source, retains its accessibility description, and reconstructs optional dark paint overrides:

```bash
python scripts/outline_svg.py diagram.editable.svg diagram.svg
```

The helper accepts sources whose `<style>` blocks contain only `@media (prefers-color-scheme: dark)` rules. It renders the attribute baseline and the dark override separately, and refuses geometry changes or residual text. It does not install tools, repair missing glyphs, or prove the drawing's meaning and layout. Inspect the source before export and the result afterward. If no exporter is available, preserve the editable SVG and report the remaining dependency rather than silently installing tools or presenting it as font independent.

## Acceptance checks

1. Parse XML; check unique IDs, local references, `viewBox`, accessible title/description, and absence of external resources.
2. Remove `<style>` blocks in a temporary copy and inspect it. Backgrounds, boxes, lines, arrowheads, text colors, sizes, and placement must remain complete. Checking for a media query or valid XML is insufficient.
3. When dark mode is requested, inspect both theme preferences in a supporting browser. Confirm readability of text, code spans, shapes, and arrowheads. In a viewer without theme support, the light baseline is the expected result.
4. For editable text, replace the preferred font with another available family and inspect crowded labels. For font-independent delivery, confirm no `<text>`, `<tspan>`, font resources, or raster replacements remain, and keep the editable source.
5. Inspect normal and reduced display sizes. When a second renderer is already available, inspect its result, including text and arrows. Temporary previews are validation artifacts, not deliverables.
6. Report only verified viewers and modes. Distinguish successful rendering, font-independent geometry, theme support, and publishing-platform embedding; none proves the others.

# qiudengs-svg-diagrams

[简体中文](README.md)

SVG drawing guidance, templates, and contrasting examples for AI coding assistants working on software requirements and system design. The focus is readable relationships: direct connections, clear grouping, consistent spacing, and restrained colors.

Generated SVG files can be viewed directly in a browser and edited further, without installing additional dependencies.

![Component architecture with side labels and shared dependencies](assets/components.svg)

## Usage

Clone the repository into your local skills directory. For example, using this project's directory convention:

```bash
git clone https://github.com/qiudeng7/qiudengs-svg-diagrams.git \
  ~/.codex/skills/qiudengs-svg-diagrams
```

If the target directory already exists, inspect it first and preserve local changes. Other tools supporting local skills can use their own skills directory.

In an assistant that supports invoking skills by name, try:

```text
Use $qiudengs-svg-diagrams to draw a component architecture diagram.
The user model catalog and chat endpoint both depend on identity and permissions.
The catalog also depends on model configuration; the chat endpoint depends on
a gateway adapter. Save the result to docs/diagrams/components.svg.
```

Expect a standalone SVG file. Open it in a browser, or reference it from a Markdown page that supports SVG:

```markdown
![Component architecture](docs/diagrams/components.svg)
```

Relative paths are resolved from the Markdown file's directory. If the assistant cannot invoke skills by name, ask it to read [SKILL.md](SKILL.md) and follow its instructions.

## Documentation

- [SKILL.md](SKILL.md): diagram selection, workflow, and delivery checks.
- [Drawing rules](references/drawing-rules.md): connections, grouping, spacing, fixed palettes, and diagram semantics.
- [SVG templates](assets/): readable, editable source files. Their example content is not an approved project design.

## Diagram previews

The [component architecture diagram](assets/components.svg) appears above. Expand the other seven templates below; click an image to open its source.

<details>
<summary>System context · Who interacts with the system?</summary>

[![System context](assets/context.svg)](assets/context.svg)

</details>

<details>
<summary>Use cases · What can each actor do?</summary>

[![Use cases](assets/use-case.svg)](assets/use-case.svg)

</details>

<details>
<summary>Business flow · How does the process proceed and handle failures?</summary>

[![Business flow](assets/flow.svg)](assets/flow.svg)

</details>

<details>
<summary>State transitions · How do events change an object's state?</summary>

[![State transitions](assets/state.svg)](assets/state.svg)

</details>

<details>
<summary>Sequence · In what order do components interact?</summary>

[![Sequence](assets/sequence.svg)](assets/sequence.svg)

</details>

<details>
<summary>Data relationships · How are entities related, and with what cardinality?</summary>

[![Data relationships](assets/er.svg)](assets/er.svg)

</details>

<details>
<summary>Wireframe · Where does the user read information and act?</summary>

[![Wireframe](assets/wireframe.svg)](assets/wireframe.svg)

</details>

## Good and bad examples

These examples show how layout affects readability. Visual neatness must not change business semantics. See the [drawing rules](references/drawing-rules.md#分组标识与关系布局) for details.

### Group labels

Reserve a dedicated label area outside the content and connection paths. Side labels suit this example; they are not mandatory for every diagram.

| Bad example | Good example |
|---|---|
| [![Group labels: bad](references/examples/group-label-bad.svg)](references/examples/group-label-bad.svg) | [![Group labels: good](references/examples/group-label-good.svg)](references/examples/group-label-good.svg) |

### Dependency layout

Place shared dependencies near the center of their consumers and dedicated dependencies near their owners. Use symmetry when the relationships support it.

| Bad example | Good example |
|---|---|
| [![Dependency layout: bad](references/examples/dependency-affinity-bad.svg)](references/examples/dependency-affinity-bad.svg) | [![Dependency layout: good](references/examples/dependency-affinity-good.svg)](references/examples/dependency-affinity-good.svg) |

### Short retry loops

Label a simple retry on the return connection. Keep an explicit failure state when it must be persisted or has its own outgoing branches.

| Bad example | Good example |
|---|---|
| [![Short retry loops: bad](references/examples/state-retry-bad.svg)](references/examples/state-retry-bad.svg) | [![Short retry loops: good](assets/state.svg)](assets/state.svg) |

## Scope and limitations

- Templates demonstrate visual conventions. Adapt nodes, labels, and connections to the actual requirements.
- SVG files use system font fallbacks without external resources. Fonts may differ across environments; leave sufficient text space and inspect the result.
- Keep titles and business labels in the diagram. Explain colors, line conventions, and layout methods in accompanying documentation.
- When publishing diagrams to issues, pull requests, or other platforms, check SVG support at the intended destination.

## Repository structure

```text
SKILL.md
README.md
README.en.md
assets/                    Eight SVG templates
references/
  drawing-rules.md         Drawing rules
  examples/                Good and bad SVG examples
```

After changing rules or templates, check relative links, SVG structure, and layout. All previews reference the source files directly; no demo website is needed.

---
name: qiudengs-svg-diagrams
description: Create standalone SVG diagrams with minimal shapes, direct connections, and muted colors for software requirements and system design. Use for context, use-case, flow, state, sequence, data relationship, component, and wireframe diagrams. Not for raster images or data charts.
---

# Qiudeng's SVG Diagrams

Create reviewable SVG diagrams for software requirements and system design. Use simple shapes, a white background, readable text, direct connections, and muted colors.

## Output and dependencies

Write standalone SVG directly, without installing tools or dependencies. Do not generate PNG files or provide conversion workflows. Use system font fallbacks; do not embed fonts or raster images.

These are SVG style templates, not native draw.io files. Verify SVG support at the publishing destination separately: opening a file in a browser does not establish that a platform can embed it.

## Workflow

1. Identify the question, audience, and scope. Choose diagram types that serve the requirements; do not draw every type by default.
2. Read the relevant SVG source and [drawing rules](references/drawing-rules.md). Load only the templates needed for the task.
3. Replace example content with actual business concepts. Arrange nodes and groups around direct, shared, and dedicated relationships before drawing connections. Reserve space for group labels. See [group labels and relationship layout](references/drawing-rules.md#group-labels-and-relationship-layout). Templates teach visual conventions, not approved project requirements or fixed layouts.
4. Check meaning before layout. Split excessive content into separate diagrams instead of shrinking the text.
5. Check XML and references. Use available browser preview capabilities to inspect rendering; if unavailable, disclose that no visual inspection was performed. Do not install dependencies for this step.
6. Deliver SVG links and necessary accompanying notes about omitted scope and unresolved conditions.

## Diagram selection and templates

- [System context](assets/context.svg): who interacts with the system, and where is its boundary?
- [Use cases](assets/use-case.svg): what can users accomplish?
- [Business flow](assets/flow.svg): how does a request proceed, including unmet conditions?
- [State transitions](assets/state.svg): how does a generation request react to events?
- [Sequence](assets/sequence.svg): how do components collaborate, and when do responses and settlement occur?
- [Data relationships](assets/er.svg): how are entities related, and with what cardinality?
- [Component architecture](assets/components.svg): how are responsibilities divided, and which dependencies cross boundaries?
- [Wireframe](assets/wireframe.svg): where does the user read information, select a model, and send a message?

## Quality checks

- Ground labels, directions, branch conditions, and cardinalities in the requirements, not in the template.
- For short retry loops, prefer adjacent, opposite-direction connections labeled “Retry on failure.” Avoid redundant failure boxes that create sharp triangular loops. Preserve failure states with independent business meaning; see [retry examples](references/drawing-rules.md#short-retry-loops-use-adjacent-return-connections).
- Leave room around text, keep connections clear of nodes and labels, and end arrows at target boundaries.
- Keep spacing, padding, and alignment consistent among peers. Recheck related structures after local edits. Differences need an expressive purpose; see [consistent layout rhythm](references/drawing-rules.md#use-a-consistent-layout-rhythm-for-peers).
- Distinguish existing behavior, proposed designs, and unresolved items without relying on color alone.
- Apply colors, grouping, and line styles consistently without explaining those design choices inside the diagram. Put necessary relationship labels, such as «include», on the relevant connection.
- Keep the diagram title and business content. Place the question being answered, scope, and drawing explanations in accompanying documentation rather than subtitles or footnotes. Do not mix unrelated object lifecycles.
- Use only static SVG shapes and text: no scripts, external resources, or foreignObject.
- Include title, desc, viewBox, and self-contained styles.

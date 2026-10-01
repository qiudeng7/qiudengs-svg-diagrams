# Drawing rules

## Shared visual conventions

- Use a white background, dark text, thin strokes, and the fixed muted palette. Start with 1–1.5-unit borders and rectangular primary nodes. Preserve semantic shapes such as use-case ellipses and decision diamonds.
- Start around 1120 units wide, with 18-unit body text, 14-unit annotations, 26-unit titles, and 40-unit outer margins. Adjust for the actual display size.
- For editable text, use font fallbacks covering Windows, macOS, and Linux, with a generic family last. Leave room for long names and multilingual text rather than relying on exact metrics from one font. Wrap with text/tspan and enlarge the container. Follow [portability](portability.md) for font-independent delivery.
- Keep the main flow in one direction. Prefer direct horizontal, vertical, or diagonal lines when unobstructed. Use two nearby, opposite-direction lines for round trips. Route around obstacles only when needed; do not add bends merely to keep lines orthogonal. Omit arrowheads for undirected associations.
- End arrows at node boundaries. Keep connection labels away from intersections and body text. Make unavoidable crossings unambiguous about whether the lines connect.
- Use the title to identify the topic. Keep the question being answered, scope, and detailed rules in adjacent prose. Do not add question subtitles, drawing footnotes, or color and line-style legends.
- Color, grouping, and line style organize the design implicitly. Put necessary business meaning directly on nodes or connections, such as branch conditions, cardinalities, and «include».
- Each SVG must contain xmlns, viewBox, an explicit default background, title, desc, and aria-labelledby. Use markers when relationships need arrows. Put baseline colors, strokes, fonts, and sizes in presentation attributes; styles are optional enhancements. Prefix IDs uniquely when inlining multiple diagrams on one page.
- Escape XML characters such as &amp;, &lt;, and &gt;. Do not use external fonts, images, CSS, scripts, or foreignObject.

## Color and visual hierarchy

Reduce unnecessary crossings before using color, line style, and contrast to help readers follow relationships. Background containers should recede; business nodes and relationships should stand out. Color cannot repair a poor layout. This palette is for authors, not an in-diagram legend.

| Purpose | Stroke / text | Light background |
|---|---|---|
| Feasibility: feasible | `#327354` | `#EDF5EF` |
| Feasibility: infeasible | `#AA4E4E` | `#FAEEEE` |
| Feasibility: uncertain | `#926D20` | `#FBF5E5` |
| Group A: blue | `#426B91` | `#EEF3F8` |
| Group B: purple | `#786783` | `#F3EFF6` |
| Group C: teal | `#477C80` | `#EDF5F4` |
| Group D: brown | `#8A735C` | `#F6F1EB` |
| Background region | `#CBD5DF` | `#F5F7FA` |

Use `#25313A` for body text. Group colors do not imply good or bad: assign them to the current diagram's groups and stay consistent. Green, red, and yellow may express status, but must accompany explicit business labels. Yellow does not automatically mean failure.

When both dimensions are present, use light container fills for group membership and labeled status indicators for state. Avoid giving one color two meanings. Names, relationship labels, and structure must remain understandable without color.

## Group labels and relationship layout

### Reserve a stable reading position for group labels

Place labels where they clearly identify their group without interfering with content or connections, and reserve dedicated space. Use a consistent labeling approach for peer groups. Horizontal layers can use side labels; choose other positions according to the grouping direction. Side labels are not mandatory for every diagram.

- [Bad: labels compete with content and connections](examples/group-label-bad.svg). Small text at a container's upper edge conflicts with incoming lines.
- [Good: a dedicated label area](examples/group-label-good.svg). The content and connections remain the same; the label moves to a reserved side area with readable type.

### Let node positions reflect affinity and sharing

Identify direct, shared, and dedicated relationships before placing nodes. Keep closely related nodes near each other, shared nodes near the visual center of their consumers, and dedicated nodes near their respective owners. Reduce detours, crossings, and tracing distance through placement rather than simply spacing all nodes equally.

Use symmetry when the relationships are symmetric. Preserve asymmetry when they are not; do not force symmetry for neatness. Keep the reading direction, business sequence, and group boundaries clear. Different node sizes or labels need not produce identical line lengths.

- [Bad: even spacing ignores shared relationships](examples/dependency-affinity-bad.svg). Two interfaces share identity and permissions, but placing that dependency to one side creates long diagonals and crossings.
- [Good: center the shared dependency](examples/dependency-affinity-good.svg). The same nodes and dependencies are arranged with the shared capability between consumers and dedicated capabilities on the outside.

Arrange nodes and groups around relationships before drawing connections. Do not lay out an even grid first and compensate with routing later. Apply these principles to components, data relationships, system context, and swimlanes while preserving their semantic constraints, such as time order in sequence diagrams.

### Use a consistent layout rhythm for peers

Use consistent spacing, padding, and alignment for elements with the same structural role: peer groups, consecutive swimlanes, parallel nodes, and repeated cards. After changing one element, recheck its peers so local improvements do not disrupt overall consistency.

Spacing can vary with relationship density, content length, or annotation needs, but the variation must serve a clear expressive purpose, such as separating business phases. Otherwise, keep it consistent.

Relationships determine placement; consistency governs the arrangement of comparable structures. Shared dependencies can be centered and dedicated ones placed near their consumers while the spacing between peer groups remains uniform unless a difference conveys additional meaning.

See the complete [component architecture example](../assets/components.svg).

## Diagram semantics

### System context

Treat the system under analysis as a whole. Show people and external systems, not internal databases or controllers. Label interactions; use two nearby, opposite-direction arrows for bidirectional exchanges.

Reference: [context.svg](../assets/context.svg).

### Use cases

Place actors outside the system boundary and use cases inside. Association lines do not imply process order. Use include/extend only when needed and make their meaning clear.

Reference: [use-case.svg](../assets/use-case.svg).

### Business flow

Maintain one primary direction. Use diamonds for decisions and label each branch condition. Route loops outside the main flow. Add swimlanes when responsibility handoffs need clarification.

Reference: [flow.svg](../assets/flow.svg).

### State transitions

Nodes represent stable states; arrows represent events or conditions. Identify the object whose lifecycle is shown. Keep unrelated lifecycles, such as generation and settlement, separate.

Reference: [state.svg](../assets/state.svg).

#### Short retry loops: use adjacent return connections

When failure handling simply returns to a neighboring step and the diagram does not need an independent failure state, use nearby forward and return lines. Label the return “Retry on failure.” Include necessary conditions, such as user initiation, so simplification does not imply automatic retries.

Bad example: [redundant failure nodes create sharp triangular loops](examples/state-retry-bad.svg). Separate “Validation failed” and “Request failed” boxes below the main flow turn short retry relationships into sharp triangles, adding nodes and tracing effort.

Good example: [simplified state diagram](../assets/state.svg). Put retries directly on return connections between adjacent states instead of adding failure boxes.

This rule depends on the diagram's abstraction level. Preserve an explicit failure state when it must be persisted, wait for handling, or carry multiple outgoing branches. Optimize its layout rather than removing necessary business meaning.

### Sequence

Arrange participants horizontally and time vertically. Distinguish responses from asynchronous events. Use domain roles for business sequences and actual components for interface sequences. Mark alternatives explicitly; do not make asynchronous settlement a prerequisite for returning content.

Reference: [sequence.svg](../assets/sequence.svg).

### Data relationships

Distinguish conceptual entities from physical tables. Label cardinality at both ends using 1, 0..1, or 0..N. A foreign key does not imply that a child record must exist. Include only fields relevant to the relationships.

Reference: [er.svg](../assets/er.svg).

### Component architecture

Define boundaries, place components, and then connect dependencies. Give each node one responsibility. Distinguish existing, new, and unresolved components with explicit labels or boundary styles, not color alone. Example architecture is not an approved project design.

Reference: [components.svg](../assets/components.svg).

### Wireframes

Use recognizable boxes, text, and controls to express information hierarchy. Do not replace business information with decoration. Numbered callouts can refer to accompanying rules. Show complex interactions as separate states rather than combining every state on one page.

Reference: [wireframe.svg](../assets/wireframe.svg).

## Validation and delivery

Check business objects and relationships first, then XML structure, ID references, viewBox bounds, and text placement. Follow the [portability acceptance checks](portability.md#acceptance-checks): CSS disabled, requested themes, font fallback or outlined delivery, and an available second renderer. Use available browser capabilities to inspect normal and reduced display sizes; disclose when preview is unavailable. Valid XML does not prove correct layout or semantics.

Deliver SVG source files and, when font-independent sharing is required, outlined SVG exports made with already available tools. Choose links or embedding according to the destination's support; do not promise unverified compatibility.

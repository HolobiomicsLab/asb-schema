# Exploration trace

An exploration trace records the research path behind a paper's outcome as a tree of nodes. Each node is one step: a question, an experiment, a decision, a dead end or a pivot. Each node is marked `explicit` when the paper states the step, or `inferred` when the step was reconstructed from the surrounding narrative. The card records the outcome; the trace adds the branches a paper tried, including the ones it abandoned.

<div class="asb-spec-meta"> <span class="asb-badge asb-badge--version">asb_trace.yaml 0.1.0</span> <code>https://w3id.org/holobiomicslab/asb-schema/trace/v0.1</code> <span class="asb-badge asb-badge--normative">normative</span> </div>

The classes `ExplorationTree` and `ExplorationNode` are defined in `asb_trace.yaml`, which stands alone: the umbrella `asb.yaml` does not import it, and it declares no tree root, so a validator names the target class `ExplorationTree`. The file is reached through `importlib.resources.files("asb_schema") / "asb_trace.yaml"`.

## Example

A hand-authored trace of a hypothetical study (`10.1000/example` is a hypothetical DOI). The question N01 opens an experiment (N02) and a decision (N03); under the decision, a global correction was tried and abandoned (N04), which led to a change of approach (N05).

<div class="asb-example" markdown>
<span class="asb-eyebrow">Example</span>

```yaml
schema_version: "0.1.0"
source_doi: "10.1000/example"
nodes:
  - id: N01
    type: question
    title: Can peak alignment be transferred between two instruments?
    support_level: explicit
    source_refs: ["§1"]
    children:
      - id: N02
        type: experiment
        title: Align a reference mixture measured on both instruments
        support_level: explicit
        source_refs: ["§3.1", "Table 1"]
        result: Retention times agree after a linear correction
        evidence: ["Table 1"]
      - id: N03
        type: decision
        title: Choose the alignment model
        support_level: explicit
        source_refs: ["§3.2"]
        choice: Piecewise linear correction anchored on reference compounds
        alternatives:
          - Global linear correction
          - Dynamic time warping
        children:
          - id: N04
            type: dead_end
            title: Global linear correction across the full gradient
            support_level: inferred
            hypothesis: Retention-time drift is uniform along the gradient
            failure_mode: Late-eluting compounds remain misaligned after correction
            lesson: Check drift at both ends of the gradient before fitting one global model
          - id: N05
            type: pivot
            title: Move from a global to a piecewise correction
            support_level: explicit
            source_refs: ["§3.2", "Fig. 2"]
            from: Global linear correction
            to: Piecewise linear correction
            trigger: Residual drift of late-eluting compounds
            also_depends_on: [N04]
```

```bash
SCHEMA=$(python -c "from importlib.resources import files; print(files('asb_schema') / 'asb_trace.yaml')")
linkml-validate --target-class ExplorationTree -s "$SCHEMA" trace.yaml
# No issues found
```
</div>

## Classes

`ExplorationTree` holds `schema_version` (required), `source_doi` (mapped to `prov:wasDerivedFrom`) and `nodes`, the root nodes.

`ExplorationNode` requires `id` (pattern `^N\d{2,}$`, unique within the tree), `type`, `title` and `support_level`. `source_refs` locates the step in the source (section, table or figure) and is expected on every `explicit` node. Nodes nest through `children`; `also_depends_on` records cross-edges to nodes elsewhere in the tree, which makes the tree a directed acyclic graph.

<div class="asb-ref" markdown>

| Node type | Type-specific slots | Meaning |
|---|---|---|
| `question` | none | An open question, typically the root of a branch |
| `experiment` | `result`, `evidence` | An attempt that produced a result; `evidence` lists claim ids, figures or tables |
| `decision` | `choice`, `alternatives`, `alternatives_unanchored` | A choice between options; `alternatives_unanchored` counts alternatives a guard removed |
| `dead_end` | `hypothesis`, `failure_mode`, `lesson` | An approach tried and abandoned, always a leaf; `lesson` spares a later reader the same branch |
| `pivot` | `from`, `to`, `trigger` | A change of direction and what prompted it |

</div>

`support_level` is the honesty axis of the trace: an inferred node is never presented as directly observed.

## Type-dependent rules

The value of `type` selects which type-specific slots a node must carry. The reference pipeline enforces these rules in its trace gate; LinkML class rules (`preconditions` and `postconditions`, emitted as `if` and `then` in JSON Schema) could express them inside the schema. `linkml-validate` checks the required slots, the enumerations and the `id` pattern.

## Uses

The reference pipeline writes `trace/exploration_tree.yaml` (the paper's path) and `trace/build_trace.yaml` (the build's own decisions and retries); both validate against `ExplorationTree`. A trace feeds the decisions of an ASTRA analysis and the `trace/` layer of an ARA package; see [Analyses and research objects](../interop/analyses-and-research-objects.md).

## See also

- [Task card](task-card.md)
- [Field reference: `asb_trace.yaml`](../reference/index.md#file-asb_trace)

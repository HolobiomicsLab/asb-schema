# Authoring a task card

A guide for writing a card by hand or with a small script. A valid card fills the 15 required slots of `ASBTaskCard` and carries no undeclared key; with an RO-Crate 1.1 `ro-crate-metadata.json` beside it, it meets [minimal conformance](../reference/conformance.md#minimal-conformance).

## 1. Choose the task

A card holds one bounded task: one research question (`research_question`), the answer the source gives for it (`finding`), defined inputs and checkable outputs. A paper with several results yields several cards. `task_kind` states the relation to the paper:

| Value | Meaning |
|---|---|
| `reproduction` | A result the paper reported |
| `analysis` | A re-analysis of the paper's own data |
| `component_reconstruction` | A mechanism the paper describes, reconstructed as a checkable task |
| `extension` | A task beyond the paper's reported scope |

A task that consumes another task's output names it in `input_from`:

```json
{
  "task_id": "example-package__task_002",
  "task_kind": "analysis",
  "input_from": "example-package__task_001",
  "inputs": ["filtered feature table from example-package__task_001"]
}
```

## 2. Fill the required slots

| Slot | Form | Content |
|---|---|---|
| `task_id` | string | Unique identifier; the `doi-slug__task_001` form stays unique across papers |
| `title` | string | Short title |
| `source_package` | string | Path or identifier of the source package |
| `research_question` | string | The scientific question |
| `finding` | string | The source's answer for this task |
| `task_description` | string | Full description of the task |
| `inputs`, `expected_outputs` | list of strings | Inputs and expected outputs, in prose |
| `tools`, `skills` | list of strings | Software and reusable capabilities |
| `workflow_description` | string | Step-by-step method |
| `evaluation_strategy` | object | `direct_checks` (automated) and `expert_review` (human judgment), two lists of strings |
| `created_at` | string | ISO 8601 timestamp |
| `schema_version`, `scitask_version` | string | Card-format versions; the reference pipeline writes 0.18.0 and 0.1.1 |

```json
"evaluation_strategy": {
  "direct_checks": ["ranked_features.csv exists", "ranked_features.csv has one row per kept feature"],
  "expert_review": ["The ranking criterion matches the one stated in the source"]
}
```

## 3. Add evidence and context

| Slot | Content |
|---|---|
| `evidence_snippets` | Verbatim passages: `snippet_id`, `source_path`, `reason`, `text` |
| `available_artifacts` | Files of the package: `path`, `role` (for example `raw_data`, `figure`, `script`), optional `sha256` |
| `crossref_doi` | DOI of the source article |
| `provenance_source` | `published`, `preprint`, `draft_paper` or `local_project` |
| `reproducibility_tier` | `certified`, `type-checked`, `bypassed`, `manual-only` or `experimental` |
| `domain`, `keywords`, `techniques` | Classification |
| `methodology_summary` | Ordered procedure steps |
| `data_accessions` | Public repository accessions, as JSON objects |
| `run_command`, `run_cwd`, `run_timeout_seconds` | A command that re-runs the task |

```json
"evidence_snippets": [
  {
    "snippet_id": "snip_001",
    "source_path": "paper/methods.md",
    "reason": "States the ranking criterion.",
    "text": "Features were ranked by mean intensity."
  }
],
"available_artifacts": [
  {"path": "data/feature_table.csv", "role": "raw_data"}
]
```

Data the card does not declare (an execution environment, an oracle, a canary, a license, authors) goes in a sidecar file next to `task_card.json`.

## 4. Keep the answer with the evaluator

`finding`, and evidence that quotes the result, state the answer. When a card serves as an evaluation item, the agent receives the task text (`task_description`, `inputs`, `workflow_description`) and the evaluator keeps the full card.

## 5. Validate

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
# No issues found
```

## 6. Package

A minimal RO-Crate 1.1 crate has a descriptor `ro-crate-metadata.json` of type `CreativeWork` that is `about` the root, and a root `Dataset` `./` with `datePublished`; `name`, `description` and `license` are recommended[^rocrate-root]:

```json
{
  "@id": "./",
  "@type": "Dataset",
  "datePublished": "2026-10-30",
  "hasPart": [{"@id": "task_card.json"}]
}
```

The complete crate is on the [worked example](../schema/worked-example.md#2-the-capsule-crate). To record the action that produced the card, declare Process Run Crate 0.5 (`https://w3id.org/ro/wfrun/process/0.5`) in the root `conformsTo` and add a `CreateAction` with `instrument`, `object`, `result`, `agent` and `endTime`[^prc].

## Checklist

- One bounded task with `research_question`, `finding` and, when known, `task_kind`.
- The 15 required slots, lists as lists, `evaluation_strategy` as an object.
- `created_at` in ISO 8601.
- Evidence snippets with a reason for each.
- No undeclared key; extra data in a sidecar file.
- `linkml-validate` against `asb_card.yaml` reports no issues.
- A crate with a descriptor, a root `./` and a root `datePublished`.

[^rocrate-root]: Research Object, "Root Data Entity" (RO-Crate 1.1). <https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html>
[^prc]: Workflow Run RO-Crate, "Process Run Crate". <https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/>

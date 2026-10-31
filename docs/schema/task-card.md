# Task card

A task card is a structured record of one bounded, reproducible scientific task extracted from a paper or project. It states the research question, the answer the source reports, the inputs and expected outputs, the tools and skills involved, the workflow and a plan for evaluating an attempt. Its class is `ASBTaskCard` in `src/asb_schema/asb_card.yaml`; a card is one JSON document, conventionally `task_card.json`.

<div class="asb-spec-meta"> <span class="asb-badge asb-badge--version">asb_card.yaml 0.2.0</span> <code>https://w3id.org/holobiomicslab/asb-schema/card/v0.2</code> <span class="asb-badge asb-badge--normative">normative</span> <span class="asb-badge asb-badge--required">15 of 64 slots required</span> </div>

## Example

A hand-authored card with the 15 required slots and no other key. `source_package` is derived from the hypothetical DOI 10.1000/example.

<div class="asb-example" markdown>
<span class="asb-eyebrow">Example</span>

```json
{
  "task_id": "task_001",
  "schema_version": "0.18.0",
  "scitask_version": "0.1.1",
  "title": "Reproduce Figure 2A: feature importance ranking",
  "source_package": "10.1000_example-paper",
  "created_at": "2026-10-30T12:00:00Z",
  "task_description": "Re-run the random forest feature importance analysis and reproduce Figure 2A.",
  "research_question": "Which molecular features best discriminate group A from group B?",
  "finding": "m/z 523.2 and retention time 4.3 min ranked highest (importance > 0.15).",
  "inputs": ["mzML files for 60 samples", "metadata CSV"],
  "expected_outputs": ["feature_importance.csv", "figure_2a.png"],
  "tools": ["matchms", "scikit-learn", "matplotlib"],
  "skills": ["feature importance ranking", "figure reproduction"],
  "workflow_description": "1. Load spectra with matchms. 2. Train a random forest classifier. 3. Extract and plot feature importances.",
  "evaluation_strategy": {
    "direct_checks": ["feature_importance.csv exists and contains ranked features"],
    "expert_review": ["Top-5 features match the reference within rank 1"]
  }
}
```

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
# No issues found
```
</div>

## Structure

The 64 slots fall into fourteen groups. Required slots are in bold.

| Group | Slots | Purpose |
|---|---|---|
| Identity and origin | **`task_id`**, **`title`**, **`source_package`**, `crossref_doi`, `github_name`, `related_repos`, `provenance_source`, `synthesized_from`, **`created_at`** | Name the task and its source |
| Scientific content | **`research_question`**, **`finding`**, **`task_description`**, `task_objective`, `domain_knowledge` | What is asked and what the source answered |
| Inputs and outputs | **`inputs`**, **`expected_outputs`**, `data_in`, `data_out`, `task_inputs`, `task_outputs`, `available_artifacts`, `data_accessions`, `expected_artifact_name`, `landmark_outputs`, `artifact_refs` | Data a solver starts from and files it produces |
| Tools and skills | **`tools`**, **`skills`** | Software and reusable capabilities the task requires |
| Workflow | **`workflow_description`**, `methodology_summary`, `parameters`, `script_refs` | Procedure, parameters and source code per step |
| Evaluation | **`evaluation_strategy`**, `reproducibility_tier` | How an attempt is checked and how far the step re-executes |
| Execution | `run_command`, `run_cwd`, `run_timeout_seconds`, `executable`, `execution_profile`, `execution_environment`, `resumption_contract` | A command that re-runs the task, its requirements and how a workflow resumes |
| Chaining | `input_from` | A prior task whose output is this card's first input |
| Classification | `task_kind`, `domain`, `primary_domain`, `subdomains`, `article_type`, `techniques`, `keywords`, `subtask_categories` | Relation to the source, domain and technique |
| Evidence and claim links | `evidence_snippets`, `finding_evidence_span`, `linked_result_ids`, `section_provenance`, `prov` | Verbatim passages, claim-ledger entries and provenance links |
| Entity spine | `spine_entity_ids`, `spine_condition_ids`, `abstraction_frame` | Paper-level entities and conditions the card refers to |
| Quality notes | `uncertainty_notes`, `missing_information`, `review_questions` | Gaps and questions for a reviewer |
| Assignment | `scenario_id`, `project_id` | Scenario or project of the card |
| Format versions | **`schema_version`**, **`scitask_version`** | Card-format versions the producer followed |

The pair `research_question` and `finding` is the center of the card. The free-text lists `inputs`, `expected_outputs`, `tools` and `skills` describe the task in prose; `available_artifacts`, `data_accessions` and `artifact_refs` bind that prose to files and accessions. Every slot, with range and mappings, is in the [field reference](../reference/index.md#class-ASBTaskCard).

!!! note "The finding is the answer"
    `finding` holds the source's answer to the research question. When a card is used to build an evaluation item, the agent receives the task text (`task_description`, `inputs`, `workflow_description`) and the evaluator keeps the full card.

## Nested classes

| Class | Slot | Content |
|---|---|---|
| [`EvaluationStrategy`](../reference/index.md#class-EvaluationStrategy) | `evaluation_strategy` | `direct_checks` (automated, deterministic checks) and `expert_review` (criteria for human judgment), two lists of strings |
| [`EvidenceSnippet`](../reference/index.md#class-EvidenceSnippet) | `evidence_snippets` | One verbatim passage: `snippet_id`, `source_path`, `reason` and `text`, all required |
| [`AvailableArtifact`](../reference/index.md#class-AvailableArtifact) | `available_artifacts` | One file of the source package: `path` and `role` required, `indexable` and `sha256` optional |
| [`JsonObject`](../reference/index.md#class-JsonObject) | `parameters`, `data_accessions`, `artifact_refs`, `script_refs` | An open JSON object |

`asb_card.yaml` also defines eight classes for execution and typed ports, used by optional slots: `TaskPort` (`task_inputs`, `task_outputs`), `ProvenanceLinks` (`prov`), `ExecutionProfile` with `ToolAlternative` (`execution_profile`), `ResumptionContract` (`resumption_contract`), `ExecutableSpec` (`executable`), `ExecutionEnvironment` (`execution_environment`) and `TypedArtifact` (`data_in`, `data_out`). They are listed in the field reference.

## Enumerations used by the card

| Enumeration | Slot | Values |
|---|---|---|
| [`ProvenanceSourceEnum`](../reference/index.md#enum-ProvenanceSourceEnum) | `provenance_source` | `published`, `preprint`, `draft_paper`, `local_project` |
| [`TaskKindEnum`](../reference/index.md#enum-TaskKindEnum) | `task_kind` | `reproduction` (a reported result), `analysis` (a re-analysis of the paper's data), `component_reconstruction` (a described but not separately validated mechanism), `extension` (beyond the reported scope) |
| [`ReproducibilityTierEnum`](../reference/index.md#enum-ReproducibilityTierEnum) | `reproducibility_tier` | `certified`, `type-checked`, `bypassed`, `manual-only`, `experimental` |

## Versions

A card records two strings: `schema_version`, the version of the card format, and `scitask_version`, the version of the task specification (the slot keeps the former name of the standard). Both are required strings without a pattern. The reference pipeline writes `schema_version` 0.18.0 and `scitask_version` 0.1.1. Card-format history:

- 2026-05-22: SciTask Standard 0.1.0, card `schema_version` 0.17.0.
- 2026-05-24: rename to ASB Schema; `SciTaskCard` becomes `ASBTaskCard`.
- 2026-06-09: card `schema_version` 0.18.0, with `task_kind`.
- Release 0.4.0: `parameters`, `data_accessions`, `artifact_refs` and `script_refs` take lists of `JsonObject`; the fourteen optional slots that the reference pipeline writes beyond the former 50 are declared, so its cards validate closed.

## Scope of the card

The card records the scientific task and its evidence; its optional `execution_environment` records the software stack that ran the card or that it requires. The environment a benchmark gives a solver, the oracle, hidden answers, canary strings, license and authorship belong to the formats a card feeds: the license and credit of released material sit on the [skill collection](skill-collection.md), and benchmark formats add the rest ([Benchmarks and agents](../interop/benchmarks-and-agents.md)). A producer keeps such data in a sidecar file next to `task_card.json`.

## See also

- [Worked example](worked-example.md): a card packaged as a capsule.
- [Authoring a task card](../reuse/authoring-a-card.md).
- [Field reference: `ASBTaskCard`](../reference/index.md#class-ASBTaskCard).

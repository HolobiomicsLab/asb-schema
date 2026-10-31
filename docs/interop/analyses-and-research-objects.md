# Analyses and research objects

Formats that record a scientific analysis or package research outputs. In each case ASB Schema supplies the paper-grounded content: tasks, evidence, decisions and files.

## ASTRA

ASTRA (Agentic Schema for Transparent Research Analysis), published by Lightcone Research, records one scientific analysis while it is designed and run: inputs, outputs, decisions with named options, universes and insights backed by evidence[^astra-spec]. It is written in LinkML and ships a JSON Schema and a JSON-LD context[^astra-json].

ASB Schema produces ASTRA documents and is upstream of them for published research. The exporter of the reference pipeline writes two documents per run:

- `astra/astra.yaml`, the science view, from the paper, its cards and its exploration trace;
- `astra/run_trace.yaml`, the build view: one decision per resolved build flag, one per agent model, one sub-analysis per pipeline unit.

| ASB source | ASTRA element |
|---|---|
| Paper processed in the run | Root analysis |
| Task card | Sub-analysis |
| Trace `decision` node | Decision with options; untested `alternatives` stay ordinary options |
| Trace `pivot` node | Decision whose new approach is the default and former approach an excluded option, with `trigger` as the reason |
| Trace `dead_end` under a decision | Excluded option, with `failure_mode` as the exclusion reason |
| Trace `dead_end` with no enclosing decision | Finding of the root analysis |
| Claim-ledger claims | Findings with quoted evidence |
| Build flags and agent models | Decisions of `run_trace.yaml` |

Trace `question` and `experiment` nodes are reported as unmapped.

!!! bridge "ASB Schema to ASTRA"
    <span class="asb-badge asb-badge--existing">existing</span>

    The exporter targets ASTRA 0.0.12; the current release is 0.0.14[^astra-tags]. Moving to it means writing a root `id` in `astra.yaml` and setting `Output.format` on outputs that do not alias another output.

| Further bridge | What it needs | Status |
|---|---|---|
| `EvidenceSnippet` to ASTRA `Evidence` | `snippet_id` to `id`, `text` to `quote.exact`, the card's `crossref_doi` to `doi`; `reason` to the notes of the enclosing insight | <span class="asb-badge asb-badge--feasible">feasible</span> |
| ASTRA analysis to task cards | A reader and a rule for task boundaries, since one analysis can yield several cards | <span class="asb-badge asb-badge--feasible">feasible</span> |
| `astra:` mappings in the LinkML files | `close_mappings`, for example from `ASBTaskCard` to `astra:Analysis` | <span class="asb-badge asb-badge--feasible">feasible</span> |
| Evaluation records in ASTRA | An evaluation extension, proposed in issue #74[^astra-74] | <span class="asb-badge asb-badge--hard">needs new code</span> |

## RO-Crate

RO-Crate packages research data with their metadata in one JSON-LD file, `ro-crate-metadata.json`, based on schema.org[^rocrate-root]. The Workflow Run RO-Crate profiles describe executions: Process Run Crate for tool executions recorded as `CreateAction` entities, Workflow Run Crate for one workflow execution and Provenance Run Crate for per-step detail[^wrroc].

Every capsule carries an RO-Crate 1.1 metadata file whose `CreateAction` links the tool (`instrument`), the inputs (`object`) and the outputs (`result`); see [Capsule](../schema/capsule.md#ro-crate-metadata).

| Bridge | What it needs | Status |
|---|---|---|
| RO-Crate 1.1 | Written for every capsule; a root `datePublished` and a license entity complete it | <span class="asb-badge asb-badge--existing">existing</span> |
| Process Run Crate | The profile IRI in the root `conformsTo` (`https://w3id.org/ro/wfrun/process/0.5` for RO-Crate 1.1), and `agent` and `endTime` on the action[^prc] | <span class="asb-badge asb-badge--feasible">feasible</span> |
| RO-Crate 1.2 and 1.3 | New context and descriptor IRIs and `Profile` entities; `ro_crate_version` is a free string[^ro-13] | <span class="asb-badge asb-badge--feasible">feasible</span> |
| Workflow RO-Crate | A class for `workflow.yaml` and one crate per workflow with a `ComputationalWorkflow` main entity[^wfhub] | <span class="asb-badge asb-badge--hard">needs new code</span> |

`rocrate-validator` checks a crate against RO-Crate and its profiles[^rocrate-validator].

## ARA

ARA (Agent-Native Research Artifact) defines one artifact per paper or project, a directory with `PAPER.md`, `logic/`, `src/`, `trace/` and `evidence/` layers[^ara-readme]. Its `trace/` layer holds an exploration tree with the same five node types and the same two support levels as the [exploration trace](../schema/exploration-trace.md).

!!! bridge "ASB Schema to ARA"
    <span class="asb-badge asb-badge--existing">existing</span>

    `asb ara-export` writes an ARA package for each finished run under `ara_export/`, builds each layer from the run's records and copies the exploration trace. ARA names the top-level list `tree` where the trace uses `nodes`, and asks for a `description` on `question` nodes[^ara-tree]; the converter renames the key and fills the description.

## Workflow languages

`asb export-workflow` converts the run's `workflow.yaml` into CWL, Nextflow and Snakemake files under `exports/`[^cwl][^nextflow]. Command bodies come from each card's runtime executable command; a card without one yields a structural stub. The classes `ExecutableSpec`, `ExecutionEnvironment` and `TypedArtifact` in `asb_card.yaml` are ready to carry that command on the card itself.

<span class="asb-badge asb-badge--existing">existing</span>

## See also

- [Exploration trace](../schema/exploration-trace.md)
- [Capsule](../schema/capsule.md)

[^astra-spec]: ASTRA, "Specification". <https://astra-spec.org/latest/specification/>
[^astra-json]: Lightcone Research, "astra.schema.json". <https://astra-spec.org/latest/schema/astra.schema.json>
[^astra-tags]: GitHub, "Tags · LightconeResearch/astra-spec". <https://github.com/LightconeResearch/astra-spec/tags>
[^astra-74]: GitHub, "Proposal: evaluation extension for ASTRA records · Issue #74". <https://github.com/LightconeResearch/astra-spec/issues/74>
[^rocrate-root]: Research Object, "Root Data Entity" (RO-Crate 1.1). <https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html>
[^wrroc]: Research Object, "Workflow Run RO-Crate". <https://www.researchobject.org/workflow-run-crate/>
[^prc]: Workflow Run RO-Crate, "Process Run Crate". <https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/>
[^ro-13]: Research Object Crate (RO-Crate), "RO-Crate 1.3". <https://www.researchobject.org/ro-crate/specification/1.3/>
[^wfhub]: WorkflowHub, "Workflow RO-Crate". <https://about.workflowhub.eu/Workflow-RO-Crate/>
[^rocrate-validator]: GitHub, "crs4/rocrate-validator". <https://github.com/crs4/rocrate-validator>
[^ara-readme]: ARA-Labs, "README.md", Agent-Native-Research-Artifact repository. <https://raw.githubusercontent.com/ARA-Labs/Agent-Native-Research-Artifact/main/README.md>
[^ara-tree]: GitHub, "skills/compiler/references/exploration-tree-spec.md". <https://raw.githubusercontent.com/ARA-Labs/Agent-Native-Research-Artifact/main/skills/compiler/references/exploration-tree-spec.md>
[^cwl]: Common Workflow Language, "Home". <https://www.commonwl.org/>
[^nextflow]: Nextflow, "A DSL for parallel and scalable computational pipelines". <https://www.nextflow.io/>

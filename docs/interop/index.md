# Interoperability

**ASB is the provenance and specification layer that feeds benchmark formats, not a competitor to them.**

An ASB artifact starts from a paper and keeps the link to it: the research question, the reported finding, verbatim evidence, the inputs, outputs, tools and skills, an evaluation plan and the research path behind the result. Formats for analyses, research objects, benchmark tasks and agent skills can be written from that material. This section lists those bridges, what each one carries and its status.

- A task card records one bounded task extracted from a published paper.
- ASB Schema produces ASTRA documents and is upstream of them for published research: the paper's tasks, decisions and evidence become an ASTRA analysis.
- ASB Schema is upstream of Terminal-Bench, whose tasks need an oracle and a verifier that a card does not carry; the card supplies the provenance, the reference result and a draft task statement.

## Bridge status

<span class="asb-badge asb-badge--existing">existing</span>
:   Code of the reference pipeline writes or reads the format today.

<span class="asb-badge asb-badge--feasible">feasible</span>
:   The two formats line up field by field; a converter is a short piece of new code.

<span class="asb-badge asb-badge--hard">needs new code</span>
:   A new emitter, together with content the card does not carry (for example an oracle and a verifier), written for each task.

## Bridges

| Format | Description | Direction | Status |
|---|---|---|---|
| [ASTRA](analyses-and-research-objects.md#astra) `astra.yaml` | One scientific analysis: inputs, outputs, decisions, options, insights | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [ASTRA](analyses-and-research-objects.md#astra) `run_trace.yaml` | The build of a run, recorded as ASTRA decisions | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [RO-Crate 1.1](analyses-and-research-objects.md#ro-crate) | A directory of research data with one JSON-LD metadata file | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [Process Run Crate](analyses-and-research-objects.md#ro-crate) | RO-Crate profile for the execution of tools as `CreateAction` entities | destination | <span class="asb-badge asb-badge--feasible">feasible</span> |
| [ARA](analyses-and-research-objects.md#ara) | One agent-native research artifact per paper, with a `trace/` layer | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [CWL, Nextflow, Snakemake](analyses-and-research-objects.md#workflow-languages) | Workflow languages | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [Harbor and Terminal-Bench](benchmarks-and-agents.md#harbor-and-terminal-bench) | A task directory with an instruction, an environment, an oracle and a verifier that writes a reward | destination | <span class="asb-badge asb-badge--hard">needs new code</span> |
| [ScienceAgentBench](benchmarks-and-agents.md#scienceagentbench) | Data-driven tasks whose output is a Python program | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [PaperBench](benchmarks-and-agents.md#paperbench) | Replication of a whole paper graded by a rubric tree | destination and source | <span class="asb-badge asb-badge--existing">existing</span> |
| [MLE-bench](benchmarks-and-agents.md#mle-bench) | Machine-learning competitions graded against a leaderboard | destination | <span class="asb-badge asb-badge--hard">needs new code</span> |
| [Inspect](benchmarks-and-agents.md#inspect) | Evaluation framework: dataset, solver and scorer | destination | <span class="asb-badge asb-badge--feasible">feasible</span> |
| [BixBench, CORE-Bench, DiscoveryBench](benchmarks-and-agents.md#paper-derived-benchmarks) | Question-and-answer items about published analyses | destination | <span class="asb-badge asb-badge--feasible">feasible</span> |
| [Agent Skills](benchmarks-and-agents.md#agent-skills-and-mcp) `SKILL.md` | A skill directory with a front-matter `name` and `description` | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [MCP Skills extension](benchmarks-and-agents.md#agent-skills-and-mcp) | Skills served by a Model Context Protocol server | destination | <span class="asb-badge asb-badge--feasible">feasible</span> |
| [schema.org, PROV-O, Dublin Core, EDAM, P-Plan](vocabularies-and-claims.md#term-mappings) | Shared vocabularies | source of terms | <span class="asb-badge asb-badge--existing">existing</span> |
| [SSSOM](vocabularies-and-claims.md#sssom) | A table format for ontology mappings | destination | <span class="asb-badge asb-badge--existing">existing</span> |
| [Claim ledgers and nanopublications](vocabularies-and-claims.md#claims-and-evidence) | Verbatim claims grouped into results; RDF assertions with provenance | destination and source | <span class="asb-badge asb-badge--existing">existing</span> |
| [Zenodo and DataCite](vocabularies-and-claims.md#archive-and-identifiers) | Archived deposits with DOIs | destination | <span class="asb-badge asb-badge--existing">existing</span> |

## What the format carries

Properties that make a card a good source for these formats:

| Property | Slots |
|---|---|
| Typed origin of the task | `provenance_source` (`published`, `preprint`, `draft_paper`, `local_project`), `source_package`, `crossref_doi` |
| Verbatim evidence with a stated reason | `evidence_snippets` (`snippet_id`, `source_path`, `reason`, `text`) |
| Question and finding as a pair | `research_question`, `finding` |
| Declared relation to the paper | `task_kind` (`reproduction`, `analysis`, `component_reconstruction`, `extension`) |
| Graded executability | `reproducibility_tier`, `run_command`, `run_cwd`, `run_timeout_seconds` |
| Evaluation plan in two parts | `evaluation_strategy` (`direct_checks`, `expert_review`), `landmark_outputs`, `expected_artifact_name` |
| Binding to released skills and tools | `tools`, `skills`; `ASBSkill`, `ASBTool`, `SkillCollection` |
| Chained tasks | `input_from` |
| Research object as packaging unit | `SciTaskCapsule` with RO-Crate metadata |
| The research path, abandoned branches included | `ExplorationTree` with `support_level` on each step |
| Release and credit on the collection | `license`, `doi`, `lead_curators`, `roles` on `SkillCollection` |
| One schema language, generated forms | LinkML sources; JSON Schema and a JSON-LD context generated from them; 72 exact and 120 close mappings |

A card leaves to the destination format what belongs to it: the execution environment, an oracle solution, hidden answers, canary strings and per-task license and authorship.

## Pages

- [Analyses and research objects](analyses-and-research-objects.md): ASTRA, RO-Crate, ARA, workflow languages.
- [Benchmarks and agents](benchmarks-and-agents.md): Harbor and Terminal-Bench, science benchmarks, Inspect, Agent Skills and MCP.
- [Vocabularies and claims](vocabularies-and-claims.md): term mappings, SSSOM, claims and evidence, identifiers.

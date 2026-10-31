# How the artifacts are produced

The reference pipeline maintained by the same laboratory is a Python program that turns one research-article package at a time (the article with its supplementary information, figures, tables and references to code and data) into task cards, capsules, skill bundles, tool records, a claim ledger and a workflow. Skills from many runs are then consolidated and released as skill collections. The schemas do not depend on this pipeline; this page describes it because its outputs are the main source of released artifacts.

## Build stages

| Stage | What it does | Main outputs |
|---|---|---|
| 1. Ingest | Extracts body text (pdfplumber), figures and tables (docling, optional), JATS XML when present; `--enrich` adds Crossref, Unpaywall, GitHub and Zenodo metadata | `package_index.json`, `external_enrichment.json` |
| 2. Agents | A sequence of single-purpose agents, each with its own model setting (see below) | cards, skills, tool records, evaluation manifests, claim ledger, `workflow.yaml` |
| 3. Deterministic enrichment | No model call: thresholds become `parameters.json`, Crossref titles fill `papers.json`, URLs become `links.json`, prose checks become rubric checks; every file gets a provenance entry; capsules and their RO-Crate metadata are assembled | capsules, `artifact_provenance.json` |

| Agent | Role |
|---|---|
| 1 | Entity extraction: tools, datasets and claims |
| Classify | Domain and article-type triage; sets the default number of cards |
| 1.5 | Claim ledger: verbatim claims, grouped into results |
| 2a | Decomposition of the paper into task candidates |
| 2b | One card per task |
| 3 | Critique and groundedness check against evidence spans |
| 5 | Skill body synthesis |
| 6 | Typed evaluation manifest per card |
| 7 | Parameters and supplementary-information deep dive |
| 8 | Step-to-script linker over the linked code repositories |

Every model step has a heuristic fallback, so a build runs without the `--llm` option and the test suite runs without an API key. Each run records its own build: `build_manifest.json` holds the commit, environment, schema versions and, for each agent, its model setting, temperature, seed and prompt version; `trace/build_trace.yaml` holds the decisions and retries.

Three design boundaries shape the pipeline: heuristic steps set a reproducibility floor under every model step; a build reads one package, and corpus-level signal enters only through explicit passes that write provenance; curation happens in separate review commands whose decisions the next build reads.

## Grounding and evidence

Every statement of a card points to a passage of the source package. A card carries `evidence_snippets` with the verbatim `text`, its `source_path` and the `reason` it supports the card; a value absent from the package is recorded in `uncertainty_notes` or `missing_information`.

With `--claim-ledger`, agent 1.5 writes `ledger/claims.jsonl`, `ledger/results.jsonl` and `ledger/result_evaluations.jsonl`. Each claim keeps its verbatim excerpt, a character span into the package text and a `claim_class` (`scientific`, `methodological`, `operational`, `administrative`); claims are grouped into results and linked to evaluation checks through `claim_id` and `result_id`. Long quotations from sources not recorded as open access are cut to 150 characters in exports.

## Outputs of one build

| File | Format |
|---|---|
| `cards/task_NNN.json`, `capsules/*/task_card.json` | [`ASBTaskCard`](../schema/task-card.md) |
| `capsules/<capsule_id>/` | [`SciTaskCapsule`](../schema/capsule.md), with `ro-crate-metadata.json` |
| `skills/<slug>/` | [`SkillBundle`](../schema/skill-bundle.md) |
| `trace/exploration_tree.yaml`, `trace/build_trace.yaml` | [`ExplorationTree`](../schema/exploration-trace.md) |
| `eval.json`, `rubric.json`, `workflow.yaml`, `build_manifest.json` | runtime formats of the pipeline |
| `ledger/*.jsonl`, `nanopubs/claim_NNN.jsonld` | claim ledger and nanopublications |
| `astra/astra.yaml`, `astra/run_trace.yaml` | ASTRA |
| `ara_export/` | ARA package |
| `exports/cwl/`, `exports/nextflow/`, `exports/snakemake/` | CWL, Nextflow, Snakemake |
| `mappings.sssom.tsv` | SSSOM skill-to-EDAM mappings |

Each export is described on [Interoperability](../interop/index.md).

## Evaluation

The card declares an evaluation plan: `evaluation_strategy` lists `direct_checks` (automated, deterministic) and `expert_review` (criteria for human judgment). Optional slots add `landmark_outputs` (two to six intermediate output patterns for partial credit), `expected_artifact_name`, `reproducibility_tier`, `run_command`, `run_cwd` and `run_timeout_seconds`.

The pipeline turns the plan into executable material. Each capsule carries `eval.json`, a list of typed checks bound to the task's inputs and outputs:

```text
file_exists | file_format_is | row_count_equals | field_present | value_in_range
contains_substring | output_matches_reference | script_runs | expert_review | llm_judge
```

Each check also records `solution_space` (`single`, `multiple`, `open`) and `parameter_sensitivity` (`robust`, `sensitive`, `brittle`). An attempt is graded with deterministic checks first and a judge only where no deterministic check applies:

| Score or file | What it measures |
|---|---|
| `weighted_pass_rate` | Share of the declared check weight that passed |
| `policy_score` | The same checks with vacuous passes and undecidable results removed, split into final-value and process buckets; `ungraded` when both are empty |
| `rubric_score.json` | Rubric points weighted per card evaluation tier |
| `verification.json` | Existence of the expected outputs after `run_command` has run |

A judge verdict counts only after a blind expert label has calibrated the judge, and `asb judge-trials` tests a judge with null, cheating, foreign and oracle submissions. Count wording in card prose becomes an exact `row_count_equals` check only when it states an exact integer; bounds, intervals and approximate counts become `expert_review` checks that keep the full criterion text.

Several vocabularies are called tiers; only `reproducibility_tier` is a card slot:

| Vocabulary | Values | Classifies |
|---|---|---|
| `reproducibility_tier` (card) | `certified`, `type-checked`, `bypassed`, `manual-only`, `experimental` | How far a card's step re-executes; set by `asb certify-workflow` from what ran |
| Card evaluation tiers | `reproduced`, `replicated`, `re_analyzed`, `consistent`, `improved` | How an attempt's result relates to the paper's |
| Run tiers | `smoke`, `economy`, `production`, `frontier` | Model and option configurations of a build |
| Benchmark tier | `production`, `development`, `research`, with openness `closed`, `open` or `mixed` | Rubric configuration of a benchmark build |

## Release

**Consolidation.** `asb consolidate-skills` merges the skill bundles of many runs in three tiers: exact matches of slug and tool signature merge silently, bundles above an embedding-similarity threshold merge and are logged, and a lower band is left as suggestions for a reviewer. `merge_audit.jsonl` and `consolidation_report.json` record the decisions, thresholds and counts; [`MergeAuditRecord`](../schema/skill-bundle.md) models one decision.

**Cut.** `asb collection promote` writes the release layout (`SKILL.md` leaves with "Use when" descriptions, `tools/*.yaml`) and a cut record `MANIFEST.gen.json` (`asb-cut/v0`) with the inputs, the output tree, their SHA-256 digests, an inventory and `released: false`: a cut is a candidate. With `SOURCE_DATE_EPOCH` set, two cuts from the same inputs and options are byte-identical. `asb collection verify` recomputes the digests and exits 0 (verified), 1 (failed or uncheckable) or 2 (usage error). Each leaf also carries a `knowledge_base` block (`asb-kb-assessment/v1`) with `source`, `integrity`, `assessment` and `availability`.

**Gates.** The public repository [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) runs release gates in continuous integration: a lint of skill descriptions, an EDAM IRI prefix check, RO-Crate 1.1 checks of capsules and closed validation of each `collection.yaml` against `SkillCollection`. The gate report `gate_report.json` (`asbb-release-gate/1.1`) binds the payload tree by SHA-256 and records the content policy: 150 characters per verbatim span, 1,500 cumulative and 300 per text field.

**Readiness.** The rubric `reuse-readiness/v0` reviews a skill on five independent criteria: `concrete_procedure`, `applicability`, `source_support` and `declared_output_contract` (each `pass`, `fail` or `inconclusive`), and `example` (`none`, `illustrative`, `runnable`). `asb skill readiness-report` writes a JSON report and a Markdown summary.

**Collections.** Each release has an IRI `https://w3id.org/holobiomicslab/asb-skill/collection/<slug>/v<N>` and a Zenodo deposit prepared in `.zenodo.json`. Metabolomics v2 is the published release (5,859 skills, 909 tools, 21 workflows). Epigenomics v1, metabolomics v1 and transcriptomics v1 are staged and hold the 417 capsules and benchmark cards.

## See also

- [Getting started](../getting-started.md)
- [Converting and publishing](../reuse/converting.md)

# Capsule

A capsule is a directory that packages one task card as a research object: the card, the verbatim evidence, per-file provenance, evaluation material and script excerpts, described by an RO-Crate metadata file, `ro-crate-metadata.json`. The LinkML class `SciTaskCapsule` (the name dates from the SciTask period) models the directory in `src/asb_schema/asb_capsule.yaml`, which imports `asb_card.yaml`.

<div class="asb-spec-meta"> <span class="asb-badge asb-badge--version">asb_capsule.yaml 0.1.0</span> <code>https://w3id.org/holobiomicslab/asb-schema/capsule/v0.2</code> <span class="asb-badge asb-badge--normative">normative</span> <span class="asb-badge asb-badge--required">3 of 8 slots required</span> </div>

## Fields

<div class="asb-ref" markdown>

| Field | Type | Required | Definition |
|---|---|---|---|
| `capsule_task_id` | string | yes | Identifier of the capsule, typically `doi-slug__task_NNN` |
| `capsule_card` | `ASBTaskCard` | yes | The embedded task card |
| `capsule_created_at` | string | yes | ISO 8601 creation timestamp |
| `ro_crate_version` | string | | RO-Crate version, for example `1.1` |
| `profile_version` | string | | Version of the RO-Crate profile used |
| `capsule_artifacts` | list[`AvailableArtifact`] | | Files available in the capsule |
| `artifact_provenance` | list[`ArtifactProvenanceEntry`] | | Origin of each file |
| `capsule_dir` | string | | Path of the capsule directory |

</div>

`ArtifactProvenanceEntry` records `path` and `source` (required), `jsonpath` and `created_at`. Its `source` takes a value of [`ArtifactSourceEnum`](../reference/index.md#enum-ArtifactSourceEnum).

## Directory layout

The schema does not prescribe a layout. The reference pipeline writes `capsules/<capsule_id>/`, where `capsule_id` is `{doi_slug}__{task_id}` when the paper has a DOI slug:

```text
capsules/<capsule_id>/
├── task_card.json             the card (ASBTaskCard)
├── task_card.md               the card for human readers
├── ro-crate-metadata.json     RO-Crate metadata file
├── artifact_provenance.json   origin of every file
├── eval.json                  typed evaluation checks
├── rubric.json                checks parsed from the card
├── evidence/                  verbatim text from the paper
├── figures/                   figures the task refers to
├── scripts/                   line-range excerpts from linked repositories
├── evaluation/                review rubric and evaluation strategy
├── inputs/  outputs/  tables/  logs/
└── ledger/                    claims.jsonl, results.jsonl (optional claim ledger)
```

When no executable script exists, `scripts/` holds a `README.md` and a `no_executable.json` that explain why. `eval.json`, `rubric.json` and the claim ledger are runtime formats of the reference pipeline, described in [How the artifacts are produced](../pipeline/index.md).

A release copy of a capsule follows a slim profile: `artifact_provenance.json` gains a `release` block (`profile`, `contents`, `omitted_from_release`), and the cards of the release sit in the collection's `benchmark/cards/` directory.

## RO-Crate metadata

RO-Crate packages research data with their metadata in one JSON-LD file based on schema.org[^rocrate-root]. In a capsule, the metadata descriptor points to the root data entity `./`, typed `Dataset` and `repme:ScientificWorkflow`. The root lists the files in `hasPart` and refers through `mentions` to the task, to one `CreateAction` and, with the claim ledger, to claim and result nodes. The `CreateAction` records the creation of the task: its `instrument` is the tool, its `object` the inputs, its `result` the outputs. This structure follows the Process Run Crate profile[^prc]; the crates do not yet meet the Workflow Run Crate requirements, and that alignment is tracked in the reference pipeline.

<div class="asb-ref" markdown>

| Entity | `@type` | `@id` pattern |
|---|---|---|
| Metadata descriptor | `CreativeWork` | `ro-crate-metadata.json` |
| Root dataset | `Dataset`, `repme:ScientificWorkflow` | `./` |
| Task (the card) | `ScholarlyArticle`, `p-plan:Plan` | `urn:asb:task:{task_id}`, with `sameAs` `https://doi.org/{doi}#{task_id}` when the card has a DOI |
| Source article | `ScholarlyArticle` | `urn:asb:article:{key}` |
| CreateAction | `CreateAction`, `prov:Activity`, `p-plan:Step` | `#action-{task_id}` |
| Tool | `SoftwareApplication` | `urn:asb:tool:{slug}` |
| Input | `File` | `urn:asb:input:{task_id}_{n}` |
| Output | `File`, `prov:Entity` | `urn:asb:output:{task_id}_{n}` |
| Claim | `oa:Annotation` | `urn:asb:claim:{claim_id}` |
| Result | `sepio:Assertion` | `urn:asb:result:{result_id}` |

</div>

The `urn:asb:` names are local identifiers minted by the crate writer; `task_id` is unique within one paper, and the `sameAs` link makes the task node globally unique. The identifier rules are on [Conformance](../reference/conformance.md#identifiers-and-namespaces).

## Published capsules

The public repository [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) holds 417 capsules in the staged v1 collections: 44 in epigenomics, 336 in metabolomics and 37 in transcriptomics. Its release gate checks each crate against the structural requirements of RO-Crate 1.1 and against the files present. The remaining conformance points of these crates are listed under [Status](../about/index.md#status).

## See also

- [Worked example](worked-example.md): one capsule, file by file.
- [Analyses and research objects](../interop/analyses-and-research-objects.md): RO-Crate profiles.
- [Field reference: `asb_capsule.yaml`](../reference/index.md#file-asb_capsule).

[^rocrate-root]: Research Object Crate (RO-Crate), "Root Data Entity", RO-Crate 1.1. <https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html>
[^prc]: Workflow Run RO-Crate, "Process Run Crate". <https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/>

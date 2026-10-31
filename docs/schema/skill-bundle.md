# Skill bundle

A skill bundle describes one reusable computational skill identified across several papers: its purpose, when to use it, the tools it uses, its parameters, its known failure modes and the papers it comes from. A bundle is a directory with a human-readable `skill.md` file and structured sidecar files. The class `SkillBundle` and the related records are defined in `src/asb_schema/asb_skill_bundle.yaml`; the JSON-LD context `context.jsonld` is generated from this file.

<div class="asb-spec-meta"> <span class="asb-badge asb-badge--version">asb_skill_bundle.yaml 0.2.0</span> <code>https://w3id.org/holobiomicslab/asb-schema/skill-bundle/v0.2</code> <span class="asb-badge asb-badge--normative">normative</span> </div>

## Classes

<div class="asb-ref" markdown>

| Class | What it models | Required slots |
|---|---|---|
| [`SkillBundle`](../reference/index.md#class-SkillBundle) | One bundle directory | `slug`, `skill_name`, `bundle_version` |
| [`ASBSkill`](../reference/index.md#class-ASBSkill) | A skill record aggregated and deduplicated across a corpus | `slug`, `skill_name`, `description` |
| [`ASBTool`](../reference/index.md#class-ASBTool) | A tool record aggregated and deduplicated across a corpus | `slug`, `tool_name` |
| [`ToolRecord`](../reference/index.md#class-ToolRecord) | A tool named in a bundle (`skill_tools`) | `tool_name` |
| [`PaperReference`](../reference/index.md#class-PaperReference) | A source paper (`source_papers`) | none |
| [`MergeAuditRecord`](../reference/index.md#class-MergeAuditRecord) | One deduplication decision | `alias`, `target_slug`, `decision` |
| [`ToolAffordance`](../reference/index.md#class-ToolAffordance) <span class="asb-badge asb-badge--reserved">reserved</span> | A mixin for executable tools: `input_schema`, `output_schema`, `precondition`, `effect`, `side_effect_free` | none |

</div>

`SkillBundle` holds `skill_description`, `when_to_use`, `skill_tools`, EDAM topics and operation, script paths, source task identifiers and source papers. Its `slug` is lowercase and hyphen-separated, for example `spectral-similarity-scoring`, derived from the skill's main action and unique within a corpus.

`MergeAuditRecord` makes deduplication decisions queryable and citable. It names the `alias` and the `target_slug`, records the `decision` ([`MergeDecisionEnum`](../reference/index.md#enum-MergeDecisionEnum): `auto_merge`, `manual_merge`, `kept_separate`, `needs_review`) and may carry the evidence behind it: `jaccard_score`, `embedding_cosine`, `edam_match` and `llm_judge_verdict`. `SkillBundle` and `ASBSkill` hold such records in `merged_alias_records`.

## Description rule

The `description` of `ASBSkill` is the retrieval key of the skill. It starts with "Use when" (pattern `^[Uu]se when .+`), is 50 to 300 characters long and avoids marketing words. A record checked against `asb_skill_bundle.yaml` enforces the prefix:

<div class="asb-example" markdown>
<span class="asb-eyebrow">Example</span>

```json
{"slug": "spectral-similarity-scoring", "skill_name": "Spectral similarity scoring",
 "description": "Use when two sets of MS/MS spectra must be compared by a cosine-type similarity score before library matching or networking."}
```

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_skill_bundle'))")
linkml-validate -s "$SCHEMA" -C ASBSkill skill.json
# No issues found
```
</div>

The release gate of the collections repository checks the prefix and the length of every released leaf.

## Directory layout

The reference pipeline writes one bundle per skill under `skills/<slug>/`:

```text
skills/<slug>/
├── skill.md                  description: YAML front matter and sections
├── README.md                 summary and usage notes
├── scripts/                  line-range script excerpts from linked repositories
├── papers.json               related papers (title, DOI, relevance)
├── parameters.json           key parameters with typical ranges
├── failure_modes.jsonl       known failure modes, one JSON object per line
├── examples.jsonl            usage examples
├── ontology_refs.json        ontology term mappings (EDAM, OBO)
├── environments.json         execution environments (conda, docker)
├── links.json                documentation, repositories, tutorials
├── evolution.jsonl           version history of the bundle
├── tools.json                tool records
└── artifact_provenance.json  source of every file
```

A build fills the sidecars its options call for. Bundles hold scripts and documentation, not data payloads or library installations. When a collection is released, each bundle becomes a `SKILL.md` leaf and each tool a `tools/<slug>.yaml` file; see [Skill collection](skill-collection.md).

### failure_modes.jsonl

Each line records one failure mode: `symptom` (what a reader can recognize), `root_cause` and `mitigation` (either may be null), optional source fields, `extraction_method` (the route that produced the row) and `response_status`, which is `complete` when both `symptom` and `mitigation` hold text and `response_missing` otherwise. An empty file means that no failure mode was extracted.

## Released leaves and Agent Skills

A released `SKILL.md` leaf follows the Agent Skills layout, a directory with a `SKILL.md` file whose YAML front matter has a `name` and a `description`[^agentskills], and adds provenance keys such as `derived_from`, `evidence_spans`, `claims`, `provenance` and `attribution`. The run-level `skill.md` carries a `content_hash`; hashes of released files are recorded in each collection's `gate_report.json`. See [Benchmarks and agents](../interop/benchmarks-and-agents.md#agent-skills-and-mcp).

## See also

- [Skill collection](skill-collection.md)
- [Field reference: `asb_skill_bundle.yaml`](../reference/index.md#file-asb_skill_bundle)

[^agentskills]: Agent Skills, "Specification". <https://agentskills.io/specification>

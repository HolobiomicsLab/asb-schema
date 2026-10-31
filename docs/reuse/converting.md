# Converting and publishing

Any program can write task cards: it fills the 15 required slots of `ASBTaskCard`, keeps undeclared data in a sidecar file and validates the result. This page maps existing formats onto card slots and describes how a skill collection is published.

## Principles

1. Fill the 15 required slots ([Authoring a task card](authoring-a-card.md#2-fill-the-required-slots)).
2. Fill the optional slots the source supports, in particular `evidence_snippets`, `crossref_doi`, `task_kind` and `provenance_source`.
3. Keep data the card does not declare (environment, oracle, license, authors) in a sidecar file next to `task_card.json`.
4. Use the `doi-slug__task_001` form of `task_id` when cards from several papers are pooled.
5. Keep `finding`, the source's answer, out of what an agent under evaluation sees.
6. Record gaps in `uncertainty_notes` and `missing_information`.

## From benchmark rows

Several science benchmarks derive their tasks from published research and publish task rows that fill part of a card.

<div class="asb-ref" markdown>

| Benchmark | Fields that fill card slots | Authored or re-read |
|---|---|---|
| ScienceAgentBench[^sab-hf] | `instance_id` to `task_id`; `task_inst` to `task_description`; `domain`, `domain_knowledge`, `subtask_categories`, `github_name` to the slots of the same names; `output_fname` to `expected_artifact_name` | `crossref_doi`, `research_question`, `finding` from the paper |
| DiscoveryBench[^db-hf] | `domain`, `domain_knowledge`; `queries[].question` to `research_question`; `true_hypothesis` to `finding`; the gold workflow to `workflow_description` | The real split (264 tasks) derives from papers; the DOI from the paper |
| BixBench[^bix-hf] | `id` to `task_id`; `question` and `hypothesis` to `research_question`; `ideal` to `finding`; `paper` to `crossref_doi` when it holds a DOI | A `finding` stated as the paper's result |
| CORE-Bench[^core-hf] | `capsule_id` to `task_id`; `capsule_title` to `title`; `field` to `domain`; `task_prompt` to `task_description`; `results` to `finding` | The article DOI (`capsule_doi` names the code capsule); one card per difficulty level |

</div>

In each case `evidence_snippets` come from re-reading the source paper, and `source_package`, `tools`, `skills` and `evaluation_strategy` are authored. Benchmark licenses and environments go to the sidecar file. Answers that a benchmark withholds stay withheld: a card holds `finding` beside `task_description`.

```json
{
  "uncertainty_notes": [
    "finding taken from the benchmark answer key, not from the paper text"
  ],
  "missing_information": [
    "evidence_snippets not filled: source paper not re-read",
    "article DOI not checked against the capsule DOI"
  ]
}
```

<span class="asb-badge asb-badge--feasible">feasible</span>

## From ASTRA documents

An ASTRA document records one analysis: a root `Analysis` with a description, inputs, outputs, decisions, prior insights, findings and nested analyses[^astra-spec]. A reader can fill `finding` (from findings), `expected_outputs` (from outputs), `run_command` and `crossref_doi`; `research_question`, `tools`, `skills`, `workflow_description` and `evaluation_strategy` are authored, and a rule for task boundaries decides how one analysis splits into cards.

<span class="asb-badge asb-badge--feasible">feasible</span>

## From claim records

A claim record binds a scientific assertion to its evidence. The claim adapter of the reference pipeline projects one claim onto one `EvidenceSnippet`: `snippet_id` from the claim identifier, `source_path` from the first evidence artifact or `doi:<doi>`, `text` from the source excerpt, and `reason` rendered from the claim. Check that `source_path` and `text` are not empty strings.

<span class="asb-badge asb-badge--existing">existing</span>

## Exporting cards

The exporters of the reference pipeline (ASTRA, ScienceAgentBench, PaperBench, workflow languages, ARA, Agent Skills) are described on [Interoperability](../interop/index.md).

## Checks

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
```

Closed validation reports undeclared keys; the open root of `asb_card.schema.json` accepts them ([JSON Schema roots](../reference/conformance.md#json-schema-roots)). Minimal conformance also asks for an RO-Crate 1.1 metadata file.

## Publishing a collection

Collections are released through the public repository [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections), following its contributing guide.

1. **Propose.** Open an issue with the "Propose a new collection" template: domain, a one- or two-sentence description, a slug, three to five seed papers by DOI, and a lead curator (GitHub handle and ORCID iD).
2. **Stage.** After agreement, open a pull request that adds `staged-collections/<domain>/v1/collection.yaml`.
3. **Validate.** The manifest validates closed against `SkillCollection`:

    ```yaml
    iri: https://w3id.org/holobiomicslab/asb-skill/collection/glycomics/v1
    slug: glycomics
    version: 1
    title: Glycomics Skill Collection v1
    description: Hypothetical example. Skills and tool records for computational glycomics.
    license: CC-BY-4.0
    released_at: '2026-10-30T00:00:00Z'
    ```

    ```bash
    SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_skill_collection'))")
    linkml-validate --schema "$SCHEMA" --target-class SkillCollection collection.yaml
    # No issues found
    ```

4. **Pass the gates.** The repository's validation workflow checks the manifest, skill descriptions, `derived_from` DOIs, EDAM IRIs and capsule crates on every pull request.
5. **Merge and promote.** A maintainer merges; a later pull request moves the directory from `staged-collections/` to `collections/`, where every gate blocks.

Reviewers are vetted through a candidacy pull request (`candidates/<github-handle>.yaml`) that links a GitHub handle, an ORCID iD and publication DOIs. Community skills enter through a proposal rail, at `collections/<slug>/v<N>/proposals/skills/<skill-slug>/SKILL.md` with `provenance_tier: community` and `status: hold`; `provenance_tier` takes `literature`, `repository`, `synthetic` or `community`.

The collection IRI `https://w3id.org/holobiomicslab/asb-skill/collection/<slug>/v<N>` resolves to the promoted directory. Collection content is licensed under CC-BY-4.0 and code under Apache-2.0; reuse credits the collection through its `CITATION.cff` and the source paper of each skill. Each release is deposited on Zenodo, with the DOI recorded in `doi` and `zenodo_doi`.

## See also

- [Skill collection](../schema/skill-collection.md)
- [How the artifacts are produced](../pipeline/index.md#release)

[^sab-hf]: Hugging Face, "osunlp/ScienceAgentBench". <https://huggingface.co/datasets/osunlp/ScienceAgentBench>
[^db-hf]: Hugging Face, "allenai/discoverybench". <https://huggingface.co/datasets/allenai/discoverybench>
[^bix-hf]: Hugging Face, "futurehouse/BixBench". <https://huggingface.co/datasets/futurehouse/BixBench>
[^core-hf]: Hugging Face, "siegelz/core-bench". <https://huggingface.co/datasets/siegelz/core-bench>
[^astra-spec]: ASTRA, "Specification". <https://astra-spec.org/latest/specification/>

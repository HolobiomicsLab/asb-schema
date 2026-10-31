---
description: >-
  ASB Schema is a data standard, written in LinkML, for scientific tasks
  extracted from research papers and for the skills and releases built from
  them.
hide:
  - navigation
  - toc
---

<div class="asb-hero" markdown>
<span class="asb-eyebrow">Data standard · LinkML · release 0.4.0</span>

# ASB Schema

<p class="asb-hero__lede">ASB Schema is a data standard, written in LinkML, for scientific tasks extracted from research papers and for the skills and releases built from them. It defines six related artifacts, from the task card, which records one bounded task with its evidence, to the skill collection, which releases reusable skills and tools under a license.</p>

[Read the format](schema/index.md){ .md-button .md-button--primary }
[Validate a file](getting-started.md){ .md-button }
[Connect another format](interop/index.md){ .md-button }
</div>

!!! abstract "Positioning"

    **ASB is the provenance and specification layer that feeds benchmark formats, not a competitor to them.**

    - An ASB task card records one bounded task extracted from a published paper: the research question, the paper's finding, verbatim evidence, inputs, outputs, tools, skills and an evaluation plan.
    - ASB Schema produces ASTRA documents and, for published research, is upstream of them: the paper's tasks, decisions and evidence become an ASTRA analysis.
    - ASB Schema is upstream of Terminal-Bench: a card supplies the provenance, the reference result and a draft task statement, and the task author adds the oracle and the verifier that a Harbor task runs.

## The six artifacts

| Artifact | Class and file | Serialized as | What it records |
|---|---|---|---|
| [Task card](schema/task-card.md) | `ASBTaskCard`, `asb_card.yaml` | `task_card.json` | One bounded, reproducible task from one paper, with question, finding, evidence and evaluation plan |
| [Capsule](schema/capsule.md) | `SciTaskCapsule`, `asb_capsule.yaml` | A directory with `ro-crate-metadata.json` | One card packaged as a research object, with evidence and per-file provenance |
| [Skill bundle](schema/skill-bundle.md) | `SkillBundle`, `ASBSkill`, `ASBTool`, `asb_skill_bundle.yaml` | A directory with `skill.md` and sidecar files | One reusable skill found across several papers, with its tools, parameters and failure modes |
| [Skill collection](schema/skill-collection.md) | `SkillCollection`, `asb_skill_collection.yaml` | `collection.yaml` | A curated, licensed and citable release of skills and tools |
| [Collection registry](schema/skill-collection.md#collection-registry) | `SkillCollectionRegistry`, `asb_skill_collection_registry.yaml` | JSON or JSON-LD | The list of released collections |
| [Exploration trace](schema/exploration-trace.md) | `ExplorationTree`, `asb_trace.yaml` | `trace/*.yaml` | The research path behind a result: questions, experiments, decisions, dead ends and pivots |

The Python package [`asb-schema`](https://pypi.org/project/asb-schema/) ships the seven LinkML files (the six schemas and the umbrella `asb.yaml`), one generated JSON Schema per schema and a JSON-LD context. The standard was named SciTask until 2026-05-24.

A reference pipeline maintained by the same laboratory writes cards, capsules, skill bundles and traces from papers, and releases skill collections in the public repository [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections). The schemas do not depend on it: any program or person can write and validate these artifacts.

## Release

This site documents release **0.4.0**. The latest release on the Python Package Index is 0.3.0[^pypi]. Release 0.4.0 gives four card slots (`parameters`, `data_accessions`, `artifact_refs`, `script_refs`) lists of JSON objects instead of lists of strings; see the [changelog](changelog.md) and the [status](about/index.md#status).

[^pypi]: Python Package Index, `asb-schema` release history. <https://pypi.org/project/asb-schema/>

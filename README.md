<div align="center">
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/HolobiomicsLab/asb-schema/main/docs/assets/brand/asb-logo-dark.svg">
  <img src="https://raw.githubusercontent.com/HolobiomicsLab/asb-schema/main/docs/assets/brand/asb-logo.svg" width="38%" alt="ASB logo: a tower crane lifting three blocks for code, mathematics and data">
</picture>
</div>

<h1 align="center">ASB Schema</h1>

<p align="center">
  <em>LinkML schemas for machine-readable scientific tasks: task cards, capsules, skill bundles and skill collections.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/asb-schema/"><img src="https://img.shields.io/pypi/v/asb-schema?style=flat-square" alt="PyPI version"></a>
  <a href="https://pypi.org/project/asb-schema/"><img src="https://img.shields.io/pypi/pyversions/asb-schema?style=flat-square" alt="Python versions"></a>
  <a href="https://github.com/HolobiomicsLab/asb-schema/actions/workflows/ci.yml"><img src="https://github.com/HolobiomicsLab/asb-schema/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/HolobiomicsLab/asb-schema/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://holobiomicslab.github.io/asb-schema/">Documentation</a> ·
  <a href="https://holobiomicslab.github.io/asb-schema/getting-started/">Getting started</a> ·
  <a href="https://github.com/HolobiomicsLab/asb-schema/blob/main/CHANGELOG.md">Changelog</a>
</p>

---

ASB Schema is a data standard, written in [LinkML](https://linkml.io/), for
scientific tasks extracted from research papers and for the skills and
releases built from them. The package ships the LinkML sources, one generated
JSON Schema per schema and a JSON-LD context. Formerly named SciTask.

**ASB is the provenance and specification layer that feeds benchmark formats, not a competitor to them.**

```bash
pip install asb-schema
```

## The six artifacts

| Artifact | Class and file | Serialized as | What it records |
|---|---|---|---|
| Task card | `ASBTaskCard`, `asb_card.yaml` | `task_card.json` | One bounded, reproducible task from one paper, with question, finding, evidence and evaluation plan |
| Capsule | `SciTaskCapsule`, `asb_capsule.yaml` | A directory with `ro-crate-metadata.json` | One card packaged as a research object, with evidence and per-file provenance |
| Skill bundle | `SkillBundle`, `ASBSkill`, `ASBTool`, `asb_skill_bundle.yaml` | A directory with `skill.md` and sidecar files | One reusable skill found across several papers, with its tools, parameters and failure modes |
| Skill collection | `SkillCollection`, `asb_skill_collection.yaml` | `collection.yaml` | A curated, licensed and citable release of skills and tools |
| Collection registry | `SkillCollectionRegistry`, `asb_skill_collection_registry.yaml` | JSON or JSON-LD | The list of released collections |
| Exploration trace | `ExplorationTree`, `asb_trace.yaml` | `trace/*.yaml` | The research path behind a result: questions, experiments, decisions, dead ends and pivots |

Minimal conformance: a `task_card.json` that validates against `ASBTaskCard`,
and a `ro-crate-metadata.json` that conforms to RO-Crate 1.1.

Released collections are in
[asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections).
Bridges to ASTRA, RO-Crate, ARA, Harbor and Terminal-Bench, science
benchmarks and Agent Skills are described in the
[documentation](https://holobiomicslab.github.io/asb-schema/interop/).

## Validate

Each artifact is validated against its own schema file. Validation is
closed: an undeclared key is an error.

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
```

```python
from asb_schema import get_schema_path, get_json_schema_path, get_jsonld_context_path

get_schema_path("asb_card")          # LinkML source
get_json_schema_path("asb_card")     # JSON Schema
get_jsonld_context_path()            # JSON-LD context
```

More in [Getting started](https://holobiomicslab.github.io/asb-schema/getting-started/).

## Versioning

The package follows Semantic Versioning; before 1.0, a minor release may
change a schema so that previously valid data fails. Each LinkML file carries
its own `version` and a versioned `id` under
`https://w3id.org/holobiomicslab/asb-schema/`. Generated files are
regenerated with every LinkML change, and CI fails when they differ. A release
is a tag `v<version>` equal to the version in `pyproject.toml`.

## Development

```bash
git clone https://github.com/HolobiomicsLab/asb-schema.git
cd asb-schema
python -m pip install -c constraints/generate.txt -e ".[dev,docs]"
python -m pytest            # tests
bash generate.sh            # regenerate JSON Schema, JSON-LD and the field reference
mkdocs serve -a 127.0.0.1:8001   # documentation site at http://127.0.0.1:8001/
```

| Path | Content |
|---|---|
| `src/asb_schema/*.yaml` | LinkML sources |
| `src/asb_schema/*.schema.json`, `context.jsonld` | Generated files |
| `scripts/gen_reference.py` | Generator of the field reference page |
| `constraints/generate.txt` | Exact `linkml` versions that `generate.sh` and CI generate with |
| `tests/` | Test suite |
| `docs/` | Documentation site (MkDocs Material) |

## Citation and licence

Cite with [`CITATION.cff`](https://github.com/HolobiomicsLab/asb-schema/blob/main/CITATION.cff).
Apache License 2.0, see [`LICENSE`](https://github.com/HolobiomicsLab/asb-schema/blob/main/LICENSE);
each LinkML file declares `license: CC-BY-4.0`.

Holobiomics Lab, CNRS and Université Côte d'Azur.

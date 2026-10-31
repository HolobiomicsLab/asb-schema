# Conformance

How a file conforms to ASB Schema, how to validate each artifact, and the identifiers and versions the format uses.

## Minimal conformance

An output conforms when it contains:

1. a `task_card.json` that validates against `ASBTaskCard`;
2. a `ro-crate-metadata.json` that conforms to RO-Crate 1.1.

Capsules, skill bundles, skill collections and traces are optional extensions. RO-Crate 1.1 requires a root `Dataset` whose `@id` ends with `/` and a root `datePublished`; the `conformsTo` of the metadata descriptor is a versioned permalink of the specification[^rocrate-root]. Whether "validates against `ASBTaskCard`" reads closed or open is listed under [open decisions](../about/index.md#open-decisions); a card that passes `linkml-validate` meets both readings.

## Validation

Each artifact is validated against its own LinkML file. Slot names are global in LinkML, so loading the umbrella `asb.yaml` merges colliding slot definitions (for example, `ASBTaskCard.skills` and `tools` become optional); `asb.yaml` is therefore not a validation entry point.

| Artifact | Schema file | Target class | Path |
|---|---|---|---|
| Task card | `asb_card.yaml` | `ASBTaskCard` | `get_schema_path('asb_card')` |
| Capsule | `asb_capsule.yaml` | `SciTaskCapsule` | `get_schema_path('asb_capsule')` |
| Skill bundle, skill, tool | `asb_skill_bundle.yaml` | `SkillBundle`, `ASBSkill`, `ASBTool` | `get_schema_path('asb_skill_bundle')` |
| Skill collection | `asb_skill_collection.yaml` | `SkillCollection` | `get_schema_path('asb_skill_collection')` |
| Collection registry | `asb_skill_collection_registry.yaml` | `SkillCollectionRegistry` | `get_schema_path('asb_skill_collection_registry')` |
| Exploration trace | `asb_trace.yaml` | `ExplorationTree` | `importlib.resources.files("asb_schema") / "asb_trace.yaml"` |

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
# No issues found
```

| Stage | Tool | Checks | Undeclared keys |
|---|---|---|---|
| LinkML validation | `linkml-validate --target-class <Class>` | Required slots, ranges, patterns, enumerations | Rejected |
| Closed JSON Schema | Any draft 2019-09 validator, target `$defs/<Class>` | Required slots and types | Rejected |
| Open JSON Schema | Same file, its root | Top-level slots of the root class; nested classes closed | Accepted at the top level |
| RO-Crate | `rocrate-validator`[^rocrate-validator] | RO-Crate 1.1 to 1.3 and the Workflow RO-Crate profiles | Not applicable |
| Collection release gates | `.github/workflows/validate.yml` of asb-skill-collections | Each `collection.yaml` closed against `SkillCollection`; capsule crates against RO-Crate 1.1 | Rejected |

`linkml-validate` chooses its loader by file extension, so a `.jsonld` file is validated under a `.json` name. `SciTaskCapsule` and `SkillBundle` model directories; for a capsule, the card inside is validated against `ASBTaskCard` and the crate with RO-Crate tooling. Runtime files of the reference pipeline (`eval.json`, `rubric.json`, `build_manifest.json`, released `SKILL.md` leaves and `tools/*.yaml`) are described on [How the artifacts are produced](../pipeline/index.md) and have no class in the package.

## JSON Schema roots

Each generated JSON Schema file holds every class under `$defs`, each closed (`additionalProperties: false`) except the free-form `JsonObject` and `Any`. The root of each file is open and is one class:

| File | Root | Validate against |
|---|---|---|
| `asb_card.schema.json` | `ASBTaskCard` | the root (open) or `$defs/ASBTaskCard` (closed) |
| `asb_capsule.schema.json` | `ASBTaskCard` | `$defs/SciTaskCapsule` |
| `asb_skill_bundle.schema.json` | `SkillBundle` | the root or `$defs/SkillBundle` |
| `asb_skill_collection.schema.json` | `SkillBundle` | `$defs/SkillCollection` |
| `asb_skill_collection_registry.schema.json` | `SkillBundle` | `$defs/SkillCollectionRegistry` |
| `asb_trace.schema.json` | an object without properties | `$defs/ExplorationTree` |

A pointer to the class selects it:

```python
import json, yaml, jsonschema
from asb_schema import get_json_schema_path

schema = json.load(open(get_json_schema_path("asb_skill_collection")))
target = {"$schema": schema["$schema"], "$ref": "#/$defs/SkillCollection", "$defs": schema["$defs"]}
manifest = yaml.safe_load(open("collection.yaml"))
jsonschema.Draft201909Validator(target).validate(manifest)
```

`get_json_schema_path` accepts the same five names as `get_schema_path`.

## JSON-LD context

The package ships `context.jsonld`, generated from `asb_skill_bundle.yaml` by the LinkML JSON-LD context generator[^linkml-ctx] and loaded with `asb_schema.get_jsonld_context_path()`. It declares eleven prefixes, sets `@vocab` to `https://w3id.org/holobiomicslab/asb-schema/` and defines 56 terms (49 slots, 7 classes); slots whose range is a class carry `"@type": "@id"`.

```python
import json
from asb_schema import get_jsonld_context_path

with open(get_jsonld_context_path()) as handle:
    context = json.load(handle)["@context"]
print(context["@vocab"])
# https://w3id.org/holobiomicslab/asb-schema/
```

The context covers skill-bundle terms. Released collection manifests embed their own `@context`, with `@vocab` set to schema.org and `asb:` bound to `https://w3id.org/holobiomicslab/asb-skill/`; `SkillCollection` admits it through `jsonld_context`. One context per schema file can be generated with the same command.

## Identifiers and namespaces

| Prefix | IRI | Used for |
|---|---|---|
| `asb:` | `https://w3id.org/holobiomicslab/asb-schema/` | Schema `id`s, class and slot IRIs, `@vocab` of `context.jsonld` |
| none | `https://w3id.org/holobiomicslab/asb-schema/card/v0.2` | `id` of `asb_card.yaml`; the other files follow the pattern `<kind>/vX.Y` |
| `asbskill:` | `https://w3id.org/holobiomicslab/asb-skill/` | Skills and collections; bound to `asb:` in released manifests |
| none | `https://w3id.org/holobiomicslab/asb-skill/collection/<slug>/v<N>` | `iri` of a collection release; resolves to the release directory |
| none | `https://w3id.org/holobiomicslab/asb-skill/registry` | `@id` of the collection registry; resolves to `catalogue.jsonld` |
| none | `https://w3id.org/holobiomicslab/asb-tool/<slug>` | Tool IRIs named in slot descriptions |
| `asb:` in claim records | `https://w3id.org/asb#` | Claim vocabulary of the reference pipeline |

A prefix label expands from the context of the document that uses it. The rules are kept in the w3id.org repository[^htaccess-hb].

Capsule crates name their nodes `urn:asb:<kind>:<key>` with the kinds `task`, `tool`, `input`, `output`, `claim`, `result`, `researcher`, `library`, `locator`, `evaluation` and `article`, and fragments `urn:asb:{task_id}#figure-{n}` and `urn:asb:{task_id}#table-{page}-{index}`. These are local names; `asb` is not a registered URN namespace[^iana]. A task node is unique within one paper, and its `sameAs` `https://doi.org/{doi}#{task_id}` makes it globally unique. The package test `tests/test_urn_prefix.py` keeps `urn:scitask` out of the LinkML files.

## Versions

| Version | Where | Value |
|---|---|---|
| Package | `pyproject.toml`, `asb_schema.__version__`, `CITATION.cff` | 0.4.0 |
| Schema file | `version:` of each LinkML file | 0.1.0 to 0.3.0 |
| Schema `id` segment | end of each file's `id` | v0.1 to v0.3 |
| Card `schema_version` | each `task_card.json` | 0.18.0 |
| Card `scitask_version` | each `task_card.json` | 0.1.1 |
| Trace `schema_version` | each trace | 0.1.0 |
| Collection `version` | `collection.yaml` | an integer matching `v<N>` of the IRI |

| File | `id` segment | `version` |
|---|---|---|
| `asb.yaml` | v0.2 | 0.2.0 |
| `asb_card.yaml` | `card/v0.2` | 0.2.0 |
| `asb_capsule.yaml` | `capsule/v0.2` | 0.1.0 |
| `asb_skill_bundle.yaml` | `skill-bundle/v0.2` | 0.2.0 |
| `asb_skill_collection.yaml` | `skill-collection/v0.3` | 0.3.0 |
| `asb_skill_collection_registry.yaml` | `skill-collection-registry/v0.2` | 0.2.0 |
| `asb_trace.yaml` | `trace/v0.1` | 0.1.0 |

## Versioning policy

- The package follows [Semantic Versioning](https://semver.org/). Before 1.0, a minor release may change a schema so that previously valid data fails; a patch release does not.
- A change to a LinkML file bumps that file's `version`. A change that can reject previously valid data also moves the `vX.Y` segment of its `id`.
- The generated JSON Schema files, `context.jsonld` and the [field reference](index.md) are regenerated in the same commit as the LinkML change; continuous integration fails when they differ from the generator output.
- A release is a tag `v<version>` equal to the version in `pyproject.toml` and `asb_schema.__version__`; the publish workflow refuses any other tag.
- Each release has an entry in the [changelog](../changelog.md).

## Legacy identifiers

The standard was named SciTask until 2026-05-24.

| Identifier | Status |
|---|---|
| `SciTaskCard`, `SciSkill`, `SciTool` | Deprecated aliases of `ASBTaskCard`, `ASBSkill`, `ASBTool`, mapped by `asb_schema.compat.legacy_class_name()` |
| `scitask_card`, `scitask_capsule` and the other `scitask_*` schema names | Mapped to `asb_*` by `asb_schema.compat.legacy_schema_name()` |
| `scitask-schema`, `scitask_schema` | Former package and module names |
| `SciTaskCapsule`, `scitask_version` | Current names of the capsule class and a card slot |
| `urn:scitask:` | Former URN prefix |

The `asb_schema.compat` functions return name strings and emit a `DeprecationWarning`.

[^rocrate-root]: Research Object Crate (RO-Crate), "Root Data Entity", RO-Crate 1.1. <https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html>
[^rocrate-validator]: GitHub, "crs4/rocrate-validator". <https://github.com/crs4/rocrate-validator>
[^linkml-ctx]: LinkML, "JSON-LD Contexts". <https://linkml.io/linkml/generators/jsonld-context.html>
[^htaccess-hb]: perma-id/w3id.org repository, "ids/holobiomicslab/.htaccess". <https://raw.githubusercontent.com/perma-id/w3id.org/master/ids/holobiomicslab/.htaccess>
[^iana]: IANA, "Uniform Resource Names (URN) Namespaces". <https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml>

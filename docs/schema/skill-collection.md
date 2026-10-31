# Skill collection

A skill collection is a curated, licensed and citable release of skills and tools. It is serialized as a `collection.yaml` manifest described by the class `SkillCollection` in `src/asb_schema/asb_skill_collection.yaml`, which imports `asb_skill_bundle.yaml`. Each released version of a domain collection has its own directory, `collections/<domain>/v<N>/`, and its own manifest. The released collections are listed by a [collection registry](#collection-registry).

<div class="asb-spec-meta"> <span class="asb-badge asb-badge--version">asb_skill_collection.yaml 0.3.0</span> <code>https://w3id.org/holobiomicslab/asb-schema/skill-collection/v0.3</code> <span class="asb-badge asb-badge--normative">normative</span> <span class="asb-badge asb-badge--required">6 of 25 slots required</span> </div>

## Example

The start of `collections/metabolomics/v2/collection.yaml` in [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections), shortened: the description, attribution blocks and the keys after the skill list are omitted.

<div class="asb-example" markdown>
<span class="asb-eyebrow">Example</span>

```yaml
'@context':
  '@vocab': https://schema.org/
  asb: https://w3id.org/holobiomicslab/asb-skill/
  edam: http://edamontology.org/
'@type': asb:SkillCollection
'@id': https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
iri: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
title: ASB Metabolomics Skill Collection v2 (expansion)
slug: metabolomics
version: 2
license: CC-BY-4.0
doi: 10.5281/zenodo.20794027
zenodo_doi: 10.5281/zenodo.20794027
skills_count: 5859
tools_count: 909
workflows_count: 21
skills:
- 2d-nmr-pulse-sequence-implementation
- 2d-tic-preprocessing
- 4d-lcimmsms-feature-extraction
# 5,856 more
```

</div>

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_skill_collection'))")
linkml-validate --schema "$SCHEMA" --target-class SkillCollection collection.yaml
# No issues found
```

The four manifests of the collections repository pass this closed validation, and the repository's release workflow runs the same check on every `collection.yaml`.

## Fields

Required slots are in bold. The slots `jsonld_context`, `jsonld_type` and `jsonld_id` serialize as `@context`, `@type` and `@id`.

<div class="asb-ref" markdown>

| Group | Slots | Content |
|---|---|---|
| Identity | **`iri`**, **`slug`**, **`version`** (integer), **`title`**, **`description`**, `@context`, `@type`, `@id` | IRI of the release, `<N>` matching the `vN` of the IRI |
| License and citation | **`license`** (SPDX), `doi`, `zenodo_doi` (pattern `^10\.5281/zenodo\.[0-9]+$`), `released_at` | Terms of reuse and the archived deposit |
| Content | `skills`, `tools`, `skills_count`, `tools_count`, `workflows_count` | The released skills and tools, by slug or IRI, and their counts |
| Topics | `edam_topics`, `domain_topics` | EDAM topic IRIs of the whole release |
| Lineage | `source_collections`, `catalogue_membership`, `ro_crate_path` | Prior collections, the registry that lists this one, the release crate |
| Attribution | `contributors`, `lead_curators`, `roles` | People and roles; see below |

</div>

Each slot is in the [field reference](../reference/index.md#class-SkillCollection). The release gate report `gate_report.json` of each collection binds the payload tree by SHA-256.

## Attribution

| Slot | Class | Attributes |
|---|---|---|
| `contributors` | `Person` | `name` (required), `orcid` as a URI (`https://orcid.org/...`), `affiliation` |
| `lead_curators` | `Curator` | `name` (required), `orcid` as a bare iD (pattern `^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$`), `github` |
| `roles` | `CollectionRoles` | `generator` (the program that produced the content), `promoter`, `sponsor`, `curators` (people who modified or validated the content), `zenodo_authors` (creators of the deposit, in order) |

The manifest writer derives `contributors` from `lead_curators`, converting each bare iD to its URI form. `CollectionRoles` mirrors the per-skill `attribution` block of the released leaves.

## Release layout

```text
collections/<domain>/v<N>/
├── collection.yaml       the manifest (SkillCollection)
├── leaves/<slug>/SKILL.md   one leaf per skill (Agent Skills layout)
├── tools/<slug>.yaml     one record per tool
├── workflows/            multi-skill workflows, when declared
├── gate_report.json      release gate report with payload hashes
└── .zenodo.json          deposit metadata
```

How a collection is assembled and released is described in [How the artifacts are produced](../pipeline/index.md#release); how to publish one is in [Converting and publishing](../reuse/converting.md#publishing-a-collection).

## Collection registry

A collection registry lists released collections by IRI; it does not hold their content. The class `SkillCollectionRegistry` is the root of `asb_skill_collection_registry.yaml` (0.2.0, `https://w3id.org/holobiomicslab/asb-schema/skill-collection-registry/v0.2`), which imports `asb_skill_collection.yaml` for `Person`.

<div class="asb-ref" markdown>

| Field | Type | Required | Definition |
|---|---|---|---|
| `registry_iri` | uriorcurie | yes | Stable IRI of the registry (`schema:url`) |
| `registry_title` | string | yes | Title (`schema:name`) |
| `collections` | list of uriorcurie | yes | IRIs of the listed `SkillCollection` releases, one per version |
| `registry_description` | string | | Description (`schema:description`) |
| `registry_maintainers` | list of `Person` | | People who curate the registry |
| `generated_at` | datetime | | Time of the snapshot (`prov:generatedAtTime`) |
| `external_repos` <span class="asb-badge asb-badge--reserved">reserved</span> | list of uriorcurie | | Future federation: other repositories whose collections the registry aggregates |

</div>

A minimal registry:

```json
{
  "registry_iri": "https://w3id.org/holobiomicslab/asb-skill/registry",
  "registry_title": "ASB skill collections",
  "collections": [
    "https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2"
  ]
}
```

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_skill_collection_registry'))")
linkml-validate -s "$SCHEMA" --target-class SkillCollectionRegistry registry.json
# No issues found
```

The registry IRI `https://w3id.org/holobiomicslab/asb-skill/registry` resolves to the catalog `catalogue.jsonld` of the collections repository, and each collection IRI `https://w3id.org/holobiomicslab/asb-skill/collection/<slug>/v<N>` to the release directory. The catalog is a schema.org view of the same list, with `name` and `description` and the collections as inline objects. `linkml-validate` selects its loader by file extension, so a `.jsonld` file is copied to `.json` before validation.

## See also

- [Skill bundle](skill-bundle.md)
- [Vocabularies and claims](../interop/vocabularies-and-claims.md)
- [Field reference: `asb_skill_collection.yaml`](../reference/index.md#file-asb_skill_collection) and [`asb_skill_collection_registry.yaml`](../reference/index.md#file-asb_skill_collection_registry)

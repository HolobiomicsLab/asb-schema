# About ASB Schema

ASB Schema is a set of LinkML schemas for scientific tasks extracted from published research and for the skills and releases built from them. It is maintained by the Holobiomics Lab (CNRS, Université Côte d'Azur) and distributed as the Python package `asb-schema`. The letters ASB come from the reference pipeline for which the schemas were first written; the standard was named SciTask until 2026-05-24.

<aside class="asb-infobox" markdown>

ASB Schema
{ .asb-infobox__title }

Maintainer
:   Holobiomics Lab, CNRS, Université Côte d'Azur

Former name
:   SciTask, until 2026-05-24

Package
:   `asb-schema` (module `asb_schema`)

Release
:   0.4.0

Language
:   LinkML, with generated JSON Schema and JSON-LD context

License
:   Apache-2.0 (package); CC-BY-4.0 (LinkML sources)

</aside>

## History { .asb-clear }

| Date | Event |
|------|-------|
| 2026-05-22 | Release 0.1.0 as `scitask-schema`: task card, capsule and skill bundle, with mappings to schema.org, Dublin Core, P-Plan, PROV, EDAM and RO-Crate. Release 0.1.1 adds JSON Schema generation. |
| 2026-05-24 | Release 0.2.0: the package becomes `asb-schema`, `SciTaskCard` becomes `ASBTaskCard`; skill collection and collection registry schemas are added. |
| 2026-06-09 | `task_kind` and `TaskKindEnum` added to the card; cards move to `schema_version` 0.18.0. |
| 2026-08-18 | Exploration trace schema `asb_trace.yaml` added. |
| 2026-09-14 | Release 0.3.0, the first release on the Python Package Index. |

Release 0.4.0 gives four card slots lists of JSON objects, declares the fourteen optional card slots that the reference pipeline writes, among them `execution_environment`, and moves the package to a standalone repository with its own documentation site and continuous integration. The full list of changes is in the [changelog](../changelog.md).

## Governance

The maintaining laboratory decides changes to the schema through changes to the repository and its release process; continuous integration decides whether a change passes the build. The public collections repository [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) has its own governance documents (maintainers, authorship, conflicts of interest, community skills, content and open-access policies, provenance and license tiers, dispute resolution and release rollback); they govern the collections, not the schema.

## Proposing a change

Changes are proposed as issues and pull requests on the [asb-schema repository](https://github.com/HolobiomicsLab/asb-schema). A complete change carries, in one pull request:

1. the LinkML change in `src/asb_schema/`;
2. the regenerated files, from `bash generate.sh` (JSON Schema files, `context.jsonld`, the [field reference](../reference/index.md));
3. tests in `tests/`, run with `python -m pytest`;
4. a `CHANGELOG.md` entry in the Keep a Changelog format[^kac], naming the class or slot that changed and whether previously valid data can fail.

| CI job | Python | Checks |
|---|---|---|
| `test` | 3.10 to 3.14 | `python -m pytest -q` |
| `lint` | 3.12 | `ruff check .`, `ruff format --check .` |
| `generated` | 3.12 | Installs the generator versions of `constraints/generate.txt`, regenerates and fails when `src/asb_schema` or `docs/reference/index.md` differs from the committed files (`generation_date` lines ignored) |
| `package` | 3.12 | Builds the distribution, `twine check --strict` |
| `docs` | 3.12 | `mkdocs build --strict` |

A release is a tag `v<version>`; the publish workflow checks that the tagged commit is on `main`, that the tag equals the version in `pyproject.toml`, `asb_schema.__version__` and `CITATION.cff`, and that `CHANGELOG.md` has a heading for it, runs the tests and uploads through PyPI Trusted Publishing. The [versioning policy](../reference/conformance.md#versioning-policy) and the [legacy identifiers](../reference/conformance.md#legacy-identifiers) are on the conformance page.

## Licenses

| Layer | License | Declared in |
|---|---|---|
| Python package | Apache-2.0 | `pyproject.toml`, `LICENSE`, `CITATION.cff` |
| LinkML sources | CC-BY-4.0 | `license:` key of each `src/asb_schema/*.yaml` |
| Released collection content | CC-BY-4.0 | `license:` of each `collection.yaml`; code of the collections repository is Apache-2.0 |

## Status

### Release state

This site documents release 0.4.0, a pre-1.0 release in which a minor release may change a schema so that data valid under the previous release fails; the notice in the top bar of every page says so. The Python Package Index lists release 0.3.0[^pypi]; release 0.4.0 installs from a checkout ([Getting started](../getting-started.md#install)). In asb-skill-collections, metabolomics v2 is the published collection; epigenomics v1, metabolomics v1 and transcriptomics v1 are staged and hold the 417 capsules and benchmark cards.

### Unverified points

| Point | State |
|---|---|
| Whether DOI `10.5281/zenodo.20794027` identifies metabolomics v2 | The Zenodo record carries the label `metabolomics-v0.1.0` |
| `rocrate-validator` on the capsule crates and the worked example | Not run |
| `astra-tools` validation of the exported `astra.yaml` | Not run |
| ARA tools on the exported exploration tree | Not run |
| `skills-ref validate` on released leaves | Not run; leaf counts come from a scan of the files |
| `harbor run --skill` over a released collection | Not run; the layout matches |
| Conformance of `mappings.sssom.tsv` to SSSOM | Not checked |
| Alignment of `landmark_outputs` with SUPER-style partial credit | Stated in the slot description only |
| How the TB-Science `novel` criterion treats a reproduction of a published answer | No published rule addresses it |

### Open decisions

1. Is conformance read as closed validation (`linkml-validate`) or open validation (the JSON Schema root)?
2. Does the card gain benchmark slots (canary, license, the environment a benchmark gives a solver, a pointer to a hidden answer)?
3. Is the versioning policy applied retroactively to `asb_capsule.yaml`, as release 0.4.0 applies it to `asb_card.yaml`, or amended?
4. Which license covers which layer, and where is that stated?
5. When is `asb_schema.compat` removed?

[^kac]: Keep a Changelog, "Keep a Changelog". <https://keepachangelog.com/en/1.1.0/>
[^pypi]: Python Package Index, "asb-schema". <https://pypi.org/project/asb-schema/>

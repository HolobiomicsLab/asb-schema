# Vocabularies and claims

Shared vocabularies give ASB slots a meaning outside the schema; claim and identifier formats carry evidence and releases beyond it.

## Term mappings

Each slot is aligned with external vocabularies through LinkML mappings: `exact_mappings` for terms of the same meaning and `close_mappings` for terms of similar meaning[^linkml-uris]. The seven LinkML files hold 72 exact and 120 close mappings.

| Vocabulary | Description | Mappings | Examples |
|---|---|---|---|
| schema.org | General web vocabulary for things, creative works and datasets[^schemaorg] | 92 | `title` to `schema:name`, `text` to `schema:text`, `registry_iri` to `schema:url` |
| PROV-O | W3C ontology of provenance: entities, activities, agents[^prov-o] | 45 | `source_doi` to `prov:wasDerivedFrom`, `generated_at` to `prov:generatedAtTime` |
| Dublin Core terms | Bibliographic metadata terms | 22 | `snippet_id` to `dcterms:identifier`, `collections` to `dcterms:hasPart` |
| EDAM | Ontology of data analysis in the sciences: topics, operations, data, formats[^edam] | 21 | `edam_operation`, `edam_topics`, `domain_topics` hold EDAM IRIs |
| P-Plan | Extension of PROV-O for plans, steps and variables[^pplan] | 11 | `evaluation_strategy` close to `pplan:Plan` |
| RO-Crate | Research object packaging | 1 | `ro_crate_version` |

Slots also carry an `importance` annotation: `must_have`, `should_have` or `nice_to_have`. Mappings are annotations; the generated JSON-LD context sets `@vocab` to the ASB Schema namespace, so a JSON-LD processor expands keys there (see [Conformance](../reference/conformance.md#json-ld-context)). Capsule crates use schema.org, PROV-O and P-Plan types directly.

bio.tools, the registry of bioinformatics software, identifies tools by `biotoolsID`; `ASBTool` reserves `bio_tools_id` for that link (<span class="asb-badge asb-badge--feasible">feasible</span>). A release gate can check EDAM IRIs against a pinned EDAM release[^edam-tsv].

## SSSOM

The Simple Standard for Sharing Ontological Mappings (SSSOM) exchanges mappings between semantic entities, most often as a TSV file with a metadata block[^sssom]. `asb export-sssom` writes skill-to-EDAM mappings to `mappings.sssom.tsv`.

<span class="asb-badge asb-badge--existing">existing</span>

## Claims and evidence

A card types the evidence for its task: `EvidenceSnippet` requires `snippet_id`, `source_path`, `reason` and `text`, so each verbatim passage travels with the reason it supports the card.

```json
{
  "snippet_id": "snip_001",
  "source_path": "paper/methods.md",
  "reason": "States the retention-time window that the task uses to align features across samples.",
  "text": "Features were aligned across samples within a retention-time window of 0.1 min."
}
```

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class EvidenceSnippet snippet.json
# No issues found
```

Two card slots link a card to the claim ledger it was built from: `linked_result_ids` (the results the card grades) and `section_provenance` (source sections taken from the anchors of the linked claims).

| Bridge | Description | Status |
|---|---|---|
| Claim ledger to `EvidenceSnippet` | Each claim keeps a verbatim excerpt and a character span; an adapter turns a claim into a snippet | <span class="asb-badge asb-badge--existing">existing</span> |
| Claim ledger to ASTRA findings | Claims become insights with quoted evidence in `astra.yaml` | <span class="asb-badge asb-badge--existing">existing</span> |
| Claim records to nanopublications | One `nanopubs/claim_NNN.jsonld` per claim, with head, assertion, provenance and publication-information graphs[^np-guidelines] | <span class="asb-badge asb-badge--existing">existing</span> |
| `EvidenceSnippet` to ASTRA `Evidence` | See [ASTRA](analyses-and-research-objects.md#astra) | <span class="asb-badge asb-badge--feasible">feasible</span> |

A slot on `EvidenceSnippet` holding the IRI of the supporting claim would connect card evidence to nanopublications built from the ledger.

## Archive and identifiers

| Format | Use in ASB | Status |
|---|---|---|
| w3id.org | Persistent namespaces for schemas, terms, collections and the registry[^w3id] | <span class="asb-badge asb-badge--existing">existing</span> |
| Zenodo and DataCite | A deposit per collection version, prepared in `.zenodo.json`; the DOI in `doi` and `zenodo_doi`. Zenodo registers one DOI per version and a concept DOI for all versions[^zenodo-versioning] | <span class="asb-badge asb-badge--existing">existing</span> |
| Citation File Format | `CITATION.cff` in this repository and in each released collection, which lists the source papers under `references`[^cff] | <span class="asb-badge asb-badge--existing">existing</span> |
| CodeMeta | Software metadata in JSON-LD, generated from `CITATION.cff` with cffconvert[^codemeta][^cffconvert] | <span class="asb-badge asb-badge--feasible">feasible</span> |
| Croissant | JSON-LD metadata for machine-learning datasets; a benchmark layer could be a `cr:FileSet` of cards with a `cr:RecordSet` of card slots[^croissant] | <span class="asb-badge asb-badge--feasible">feasible</span> |

## See also

- [Conformance](../reference/conformance.md): namespaces, JSON-LD context, identifiers.
- [Field reference](../reference/index.md): mappings of every slot.

[^linkml-uris]: LinkML, "URIs and mappings". <https://linkml.io/linkml/schemas/uris-and-mappings.html>
[^schemaorg]: schema.org, "About schema.org". <https://schema.org/docs/about.html>
[^prov-o]: W3C, "PROV-O: The PROV Ontology". <https://www.w3.org/TR/prov-o/>
[^edam]: EDAM, "edamontology" repository. <https://github.com/edamontology/edamontology>
[^pplan]: OPMW, "The P-Plan Ontology". <https://www.opmw.org/model/p-plan/>
[^edam-tsv]: EDAM, "EDAM.tsv". <https://edamontology.org/EDAM.tsv>
[^sssom]: Mapping Commons, "SSSOM: Simple Standard for Sharing Ontological Mappings". <https://mapping-commons.github.io/sssom/dev/>
[^np-guidelines]: Nanopublications, "Nanopublication Guidelines" (working draft). <https://nanopub.net/guidelines/working_draft/>
[^w3id]: w3id.org, "Permanent Identifiers for the Web". <https://w3id.org/>
[^zenodo-versioning]: Zenodo, "Versioning". <https://zenodo.org/help/versioning>
[^cff]: Citation File Format, "Citation File Format". <https://citation-file-format.github.io/>
[^codemeta]: CodeMeta, "CodeMeta". <https://codemeta.github.io/>
[^cffconvert]: cffconvert, "cffconvert" repository. <https://github.com/citation-file-format/cffconvert>
[^croissant]: MLCommons, "Croissant format specification". <https://docs.mlcommons.org/croissant/docs/croissant-spec.html>

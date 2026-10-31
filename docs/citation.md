# Citation

A citation of ASB Schema names the `asb-schema` package and its release version; a citation of a skill collection names the collection and its own version. Both carry their metadata in a `CITATION.cff` file, the Citation File Format for software and datasets[^cff].

## Citing the package

The repository root holds a `CITATION.cff` (`cff-version` 1.2.0, `type: software`):

| Key | Value |
|-----|-------|
| `title` | ASB Schema: LinkML schemas for the ASB standard |
| `authors` | Louis-Félix Nothias, ORCID `https://orcid.org/0000-0001-6711-6719`, Holobiomics Lab, CNRS, Université Côte d'Azur |
| `version` | 0.4.0 |
| `license` | Apache-2.0 |
| `repository-code` | `https://github.com/HolobiomicsLab/asb-schema` |
| `url` | `https://holobiomicslab.github.io/asb-schema/` |

GitHub reads this file and offers a "Cite this repository" link[^gh-cff].

```bibtex
@software{nothias_asb_schema_2026,
  author  = {Nothias, Louis-F{\'e}lix},
  title   = {{ASB Schema: LinkML schemas for the ASB standard}},
  version = {0.4.0},
  year    = {2026},
  url     = {https://holobiomicslab.github.io/asb-schema/}
}
```

## Citing a schema version

A record that conforms to one schema file cites the package version and the `id` of the file. For a task card validated with release 0.4.0: package 0.4.0 and `https://w3id.org/holobiomicslab/asb-schema/card/v0.3` (`asb_card.yaml` 0.3.0). The package version fixes the content of every schema file; the `id` and `version` of each file are listed under [Versions](reference/conformance.md#versions).

## Citing a collection

Each collection in [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) has its own `CITATION.cff` (`type: dataset`, `license: CC-BY-4.0`) that lists the source papers under `references`. Its `url` is the collection IRI, for example `https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2`.

| Collection | State | `version` | `doi` |
|------------|-------|-----------|-------|
| metabolomics v2 | published | 2 | `10.5281/zenodo.20794027` |
| epigenomics v1, metabolomics v1, transcriptomics v1 | staged | 1 | to be deposited |

A citation of a collection gives its title, version, IRI and, when deposited, its DOI. Zenodo assigns one DOI per version and a concept DOI for all versions[^zenodo].

## License

The code and the Python package are released under the Apache License 2.0; each LinkML file declares CC-BY-4.0; collection content is CC-BY-4.0. See [Licenses](about/index.md#licenses).

[^cff]: Citation File Format, "Citation File Format (CFF)". <https://citation-file-format.github.io/>
[^gh-cff]: GitHub Docs, "About CITATION files". <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files>
[^zenodo]: Zenodo, "Versioning". <https://zenodo.org/help/versioning>

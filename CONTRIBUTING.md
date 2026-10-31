# Contributing to ASB Schema

ASB Schema is a data standard: a change to a LinkML file can make data that
validated before fail. This guide describes how a schema change is made,
checked and proposed. For a large change, open an issue first so the approach
can be agreed before the work.

## Set up

```bash
git clone https://github.com/HolobiomicsLab/asb-schema.git
cd asb-schema
python -m pip install -c constraints/generate.txt -e ".[dev,docs]"
```

`constraints/generate.txt` pins the exact `linkml` versions that produced the
committed generated files.

## Changing a schema

1. Edit the LinkML source in `src/asb_schema/*.yaml`. Give every new slot or
   attribute a description that says what the field holds, an `importance`
   annotation (`must_have`, `should_have` or `nice_to_have`) and at least one
   ontology mapping. Descriptions name no internal plan, private path or
   pipeline command-line flag.
2. Regenerate with `bash generate.sh`. It writes the JSON Schema files,
   `context.jsonld` and `docs/reference/index.md`, and refuses to run with
   generator versions other than those in `constraints/generate.txt`. Commit
   the generated files in the same commit as the LinkML change: CI fails when
   they differ from the generator output.
3. Apply the version rule. A change to a LinkML file bumps that file's
   `version`. A change that can reject previously valid data also moves the
   `vX.Y` segment of its `id` and the `name` that encodes it. Before 1.0, such
   a change goes into a minor release of the package, never a patch release.
4. Add an entry to `CHANGELOG.md` under the next release (Added, Changed,
   Fixed or Removed), and say whether previously valid data can fail.
5. Update the documentation pages under `docs/schema/` and `docs/reference/`
   that describe the changed class.
6. Run the checks:

   ```bash
   python -m pytest
   make lint
   mkdocs build --strict
   ```

## Pull request

Keep one change per pull request and fill in this template in its
description:

```markdown
## Schema change

- Files and classes changed:
- Can previously valid data fail? yes / no
- File versions and ids (before -> after):
- Linked issue:

## Checklist

- [ ] `bash generate.sh` run with the pinned generator; generated files committed
- [ ] `version` bumped, and the `id` segment when previously valid data can fail
- [ ] `CHANGELOG.md` entry
- [ ] Documentation pages updated
- [ ] `python -m pytest`, `make lint` and `mkdocs build --strict` pass
- [ ] No secrets, credentials, personal data or machine-specific paths added
```

A maintainer reviews the pull request; CI passes before it is merged.
Contributions are made under the licences stated in the
[README](README.md#citation-and-licence).

## Releases

Maintainers make releases. A tag `v<version>` runs
`.github/workflows/publish.yml`, which checks the declared versions, runs the
tests and publishes the package to PyPI.

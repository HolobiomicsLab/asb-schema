# Getting started

Install the package, locate the schema files, validate a task card, a collection manifest and a trace, and regenerate the generated files.

## Install

```bash
pip install asb-schema
```

The package requires Python 3.10 or later and depends on `linkml`, `linkml-runtime` (both below 1.12) and `pyyaml`; installing it puts `linkml-validate` on the path. The Python Package Index lists release 0.3.0[^pypi]; to use release 0.4.0, documented here, run `pip install .` in a checkout of the repository. Release 0.4.0 changes four card slots to lists of JSON objects (see the [changelog](changelog.md)).

## Find the schema files

```python
from asb_schema import get_schema_path, get_json_schema_path, get_jsonld_context_path

get_schema_path("asb_card")            # LinkML source, asb_card.yaml
get_json_schema_path("asb_card")       # generated JSON Schema, asb_card.schema.json
get_jsonld_context_path()              # generated JSON-LD context, context.jsonld
```

The path functions accept `asb_card`, `asb_capsule`, `asb_skill_bundle`, `asb_skill_collection` and `asb_skill_collection_registry`. The trace schema is at `importlib.resources.files("asb_schema") / "asb_trace.yaml"`.

## Validate a task card

Save the minimal card of the [task card page](schema/task-card.md#example) as `task_card.json` and validate it against its own schema file:

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_card'))")
linkml-validate --schema "$SCHEMA" --target-class ASBTaskCard task_card.json
```

```text
No issues found
```

`linkml-validate` validates closed: an undeclared key is an error. With `source_package` removed and an extra key added, the command exits with status 1:

```text
[ERROR] [bad_card.json/0] Additional properties are not allowed ('unknown_key' was unexpected) in /
[ERROR] [bad_card.json/0] 'source_package' is a required property in /
```

Each artifact is validated against its own file, here `asb_card.yaml`, not the umbrella `asb.yaml` ([Conformance](reference/conformance.md#validation)).

## Validate a collection manifest

```bash
SCHEMA=$(python -c "from asb_schema import get_schema_path; print(get_schema_path('asb_skill_collection'))")
linkml-validate --schema "$SCHEMA" --target-class SkillCollection collections/metabolomics/v2/collection.yaml
# No issues found
```

The manifests of [asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) pass this check.

## Validate an exploration trace

```bash
SCHEMA=$(python -c "from importlib.resources import files; print(files('asb_schema') / 'asb_trace.yaml')")
linkml-validate --schema "$SCHEMA" --target-class ExplorationTree exploration_tree.yaml
```

A two-node trace that passes:

```yaml
schema_version: "0.1.0"
nodes:
  - id: N01
    type: question
    title: Which normalization keeps batch effects below the biological signal?
    support_level: explicit
    source_refs: ["Section 2"]
    children:
      - id: N02
        type: experiment
        title: Compare total-ion-current and quantile normalization on pooled QC samples
        support_level: inferred
        result: Quantile normalization reduced the QC coefficient of variation
```

Node identifiers match `^N\d{2,}$`.

## Validate with JSON Schema

The generated files follow draft 2019-09. Each class is a closed definition under `$defs`; validate against the class:

```python
import json

import jsonschema
from asb_schema import get_json_schema_path


def class_validator(schema_name, class_name):
    with open(get_json_schema_path(schema_name)) as f:
        schema = json.load(f)
    target = {"$schema": schema["$schema"], "$ref": f"#/$defs/{class_name}", "$defs": schema["$defs"]}
    return jsonschema.validators.validator_for(schema)(target)


with open("task_card.json") as f:
    card = json.load(f)
errors = [e.message for e in class_validator("asb_card", "ASBTaskCard").iter_errors(card)]
```

The root of each file and its intended class are listed under [JSON Schema roots](reference/conformance.md#json-schema-roots).

## Regenerate the generated files

After editing a LinkML file, in a checkout of the repository:

```bash
pip install -e ".[dev]"
bash generate.sh
python -m pytest
```

`generate.sh` writes the six JSON Schema files with `asb_schema.jsonschemagen`, `context.jsonld` from `asb_skill_bundle.yaml`, and the [field reference](reference/index.md) with `scripts/gen_reference.py` (also `make reference`). Continuous integration regenerates them and fails when the committed files differ, apart from the `generation_date` line of `context.jsonld`.

## Next steps

- [Worked example](schema/worked-example.md): a card packaged as a capsule, with a released skill leaf and manifest.
- [Authoring a task card](reuse/authoring-a-card.md).
- [Conformance](reference/conformance.md).

[^pypi]: Python Package Index, "asb-schema". <https://pypi.org/project/asb-schema/>

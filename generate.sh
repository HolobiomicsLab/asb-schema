#!/usr/bin/env bash
# Regenerate all LinkML-derived artefacts of ASB Schema.
# Run from anywhere: bash generate.sh (paths resolve from this file).
set -e
asb_schema_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${asb_schema_dir}/src${PYTHONPATH:+:${PYTHONPATH}}"
# The committed artefacts come from the generator versions pinned in
# constraints/generate.txt; refuse to regenerate with any other version.
python - "${asb_schema_dir}/constraints/generate.txt" <<'PY'
import sys
from importlib.metadata import version

wrong = []
for line in open(sys.argv[1], encoding="utf-8"):
    requirement = line.split("#", 1)[0].strip()
    if requirement:
        name, pinned = requirement.split("==")
        if version(name) != pinned:
            wrong.append(f"{name} {version(name)} (pinned {pinned})")
if wrong:
    sys.exit("generate.sh: " + ", ".join(wrong)
             + "; run: python -m pip install -c constraints/generate.txt -e .")
PY
cd "${asb_schema_dir}/src/asb_schema"
# Each file is written to a .tmp sibling and moved into place only when its
# generator succeeds, so a failed run leaves the committed file intact.
trap 'rm -f -- *.schema.json.tmp context.jsonld.tmp' EXIT
for schema in asb_card asb_capsule asb_trace asb_skill_bundle asb_skill_collection asb_skill_collection_registry; do
  python -m asb_schema.jsonschemagen "${schema}.yaml" > "${schema}.schema.json.tmp"
  mv -- "${schema}.schema.json.tmp" "${schema}.schema.json"
done
# JSON-LD @context for the skill-bundle terms (w3id.org/holobiomicslab/asb-skill/).
python -m linkml.generators.jsonldcontextgen asb_skill_bundle.yaml > context.jsonld.tmp
mv -- context.jsonld.tmp context.jsonld
# Field reference page of the documentation site (docs/reference/index.md).
python "${asb_schema_dir}/scripts/gen_reference.py"
echo "Done. Artefacts written next to the LinkML sources."

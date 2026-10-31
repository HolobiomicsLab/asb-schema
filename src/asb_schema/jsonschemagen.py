"""ASB JSON representation policy over the existing LinkML generator.

The upstream generator's optional enum reference omits null even though optional
scalar slots include it. A declarative marker also distinguishes an open JSON
object from LinkML Any's wider scalar union. Neither rule depends on a domain,
card ID or scientific vocabulary.
"""

from __future__ import annotations

import argparse
import sys

from linkml.generators.jsonschemagen import JsonSchemaGenerator


class ASBJsonSchemaGenerator(JsonSchemaGenerator):
    def after_generate_class(self, result, sv):
        annotation = (result.source.annotations or {}).get("json_schema_type")
        if annotation is not None:
            if str(annotation.value) != "object":
                raise ValueError("unsupported declared JSON schema type")
            result.schema_["type"] = "object"
            result.schema_["additionalProperties"] = True
        return result

    def after_generate_class_slot(self, result, cls, sv):
        slot = result.source
        if (self.include_null and not slot.required and not slot.multivalued
                and slot.range in sv.all_enums() and "$ref" in result.schema_):
            reference = result.schema_.pop("$ref")
            result.schema_["anyOf"] = [{"$ref": reference}, {"type": "null"}]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", help="LinkML schema YAML to render as JSON Schema.")
    args = parser.parse_args()
    # Match the upstream CLI's root openness; runtime-specific closure is a
    # separate profile, not an accidental consequence of calling its Python API.
    sys.stdout.write(ASBJsonSchemaGenerator(args.schema, not_closed=True).serialize() + "\n")


if __name__ == "__main__":
    main()

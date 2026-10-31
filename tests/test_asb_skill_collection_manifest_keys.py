"""SkillCollection v0.3: a released collection.yaml validates against the class.

Up to v0.2 the class declared fifteen slots while every manifest the
`asb-skill-collections` release writes carries ten more keys (JSON-LD framing,
lead curators, counts, catalogue topics, attribution roles, Zenodo DOI). Run
closed, as `linkml-validate` runs it, each of the four released manifests failed
on additional properties, so no manifest could ever pass the collection repo's
LinkML gate. The manifest below has the released key set with synthetic values.
"""
import copy
import json
from pathlib import Path

import pytest

pytest.importorskip("linkml.validator")
from linkml.validator import Validator  # noqa: E402
from linkml.validator.plugins import JsonschemaValidationPlugin  # noqa: E402

SRC = Path(__file__).resolve().parent.parent / "src" / "asb_schema"
SCHEMA = SRC / "asb_skill_collection.yaml"
JSON_SCHEMA = SRC / "asb_skill_collection.schema.json"

MANIFEST = {
    "@context": {
        "@vocab": "https://schema.org/",
        "asb": "https://w3id.org/holobiomicslab/asb-skill/",
        "edam": "http://edamontology.org/",
    },
    "@type": "asb:SkillCollection",
    "@id": "https://w3id.org/holobiomicslab/asb-skill/collection/example/v1",
    "iri": "https://w3id.org/holobiomicslab/asb-skill/collection/example/v1",
    "title": "Example skill collection",
    "slug": "example",
    "version": 1,
    "description": "Synthetic manifest carrying the released key set.",
    "license": "CC-BY-4.0",
    "doi": "10.5281/zenodo.1234567",
    "released_at": "2026-01-01T00:00:00Z",
    "roles": {
        "generator": "AgenticScienceBuilder",
        "promoter": "A. Promoter",
        "sponsor": "An institution",
        "curators": [],
        "zenodo_authors": ["AgenticScienceBuilder Community", "A. Promoter"],
    },
    "zenodo_doi": "10.5281/zenodo.1234567",
    "lead_curators": [
        {"name": "A. Curator", "orcid": "0000-0002-1825-0097", "github": "acurator"}
    ],
    "contributors": [
        {"name": "A. Curator", "orcid": "https://orcid.org/0000-0002-1825-0097"}
    ],
    "skills_count": 2,
    "tools_count": 1,
    "workflows_count": 0,
    "skills": ["first-skill", "second-skill"],
    "tools": ["a-tool"],
    "edam_topics": ["http://edamontology.org/topic_3172"],
    "domain_topics": ["http://edamontology.org/topic_3172"],
    "source_collections": ["10.1000/example"],
    "catalogue_membership": ["https://w3id.org/holobiomicslab/asb-skill/registry"],
}

TEN_KEYS = {
    "@context", "@type", "@id", "lead_curators", "skills_count", "tools_count",
    "workflows_count", "domain_topics", "roles", "zenodo_doi",
}


@pytest.fixture(scope="module")
def validator():
    # closed=True is what linkml-validate applies: undeclared keys are errors.
    return Validator(str(SCHEMA), validation_plugins=[JsonschemaValidationPlugin(closed=True)])


def _messages(validator, instance):
    return [r.message for r in validator.validate(instance, "SkillCollection").results]


def test_the_released_key_set_validates(validator):
    assert TEN_KEYS <= set(MANIFEST)
    assert _messages(validator, MANIFEST) == []


def test_each_of_the_ten_keys_is_optional(validator):
    for key in TEN_KEYS:
        instance = {k: v for k, v in MANIFEST.items() if k != key}
        assert _messages(validator, instance) == [], key


@pytest.mark.parametrize(
    "mutate, fragment",
    [
        (lambda m: m.pop("slug"), "'slug' is a required property"),
        (lambda m: m.__setitem__("undeclared", 1), "('undeclared' was unexpected) in /"),
        (lambda m: m.__setitem__("skills_count", "many"), "is not of type 'integer'"),
        (lambda m: m.__setitem__("workflows_count", -1), "less than the minimum of 0"),
        (lambda m: m["lead_curators"][0].pop("name"), "'name' is a required property"),
        (
            lambda m: m["lead_curators"][0].__setitem__("orcid", "https://orcid.org/0000-0002-1825-0097"),
            "does not match",
        ),
        (lambda m: m["roles"].__setitem__("undeclared", "x"), "('undeclared' was unexpected) in /roles"),
        (lambda m: m.__setitem__("zenodo_doi", "https://doi.org/10.5281/zenodo.1"), "does not match"),
    ],
    ids=[
        "missing-required", "undeclared-key", "count-type", "negative-count",
        "curator-without-name", "curator-orcid-as-uri", "undeclared-role", "zenodo-doi-as-url",
    ],
)
def test_the_class_still_refuses(validator, mutate, fragment):
    instance = copy.deepcopy(MANIFEST)
    mutate(instance)
    messages = _messages(validator, instance)
    assert any(fragment in m for m in messages), messages


def test_the_committed_json_schema_carries_the_aliases():
    """`generate.sh` output is committed; the JSON-LD keys must appear under their serialised names."""
    props = json.loads(JSON_SCHEMA.read_text())["$defs"]["SkillCollection"]["properties"]
    assert TEN_KEYS <= set(props), sorted(TEN_KEYS - set(props))

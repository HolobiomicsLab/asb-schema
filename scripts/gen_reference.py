#!/usr/bin/env python3
"""Generate the field reference page of the documentation site.

Reads the seven LinkML sources in src/asb_schema/ with PyYAML (no linkml
import) and writes one page, docs/reference/index.md, with one section per
schema file. The output is deterministic: source order throughout, no
timestamp, LF line endings and a trailing newline.

Usage: python scripts/gen_reference.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "asb_schema"
OUT = ROOT / "docs" / "reference" / "index.md"

FILES = [
    "asb",
    "asb_card",
    "asb_capsule",
    "asb_skill_bundle",
    "asb_skill_collection",
    "asb_skill_collection_registry",
    "asb_trace",
]

BUILTIN_TYPES = {
    "string", "integer", "float", "double", "decimal", "boolean", "uri",
    "uriorcurie", "curie", "ncname", "datetime", "date", "time",
}

FORMAT_PAGES = {
    "asb": ("The format", "../schema/index.md"),
    "asb_card": ("Task card", "../schema/task-card.md"),
    "asb_capsule": ("Capsule", "../schema/capsule.md"),
    "asb_skill_bundle": ("Skill bundle", "../schema/skill-bundle.md"),
    "asb_skill_collection": ("Skill collection", "../schema/skill-collection.md"),
    "asb_skill_collection_registry": ("Skill collection", "../schema/skill-collection.md#collection-registry"),
    "asb_trace": ("Exploration trace", "../schema/exploration-trace.md"),
}

# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------

_CODE_SPAN = re.compile(r"(`+)(.+?)\1", re.S)


def _escape_text(text: str, in_table: bool) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if in_table:
        text = text.replace("|", "\\|")
    return text


_EN_DASH_RANGE = re.compile(r"(\d)\s*\u2013\s*(\d)")
_EM_DASH = re.compile(r"\s*\u2014\s*")
_INTERNAL_PATH = re.compile(r"\s*See (?:\.\./)+docs/\S+\.md(?: \u00a7[\d.]+)?\.")
_PIPELINE_NAME = re.compile(r"\bAgenticScienceBuilder\b")


def normalize(text: str) -> str:
    """Normalize dashes and drop relative paths into unpublished documents.

    An en-dash between numbers becomes " to "; an em-dash becomes ": ".
    A sentence of the form "See ../../docs/<path>.md \u00a7N." is removed,
    because the path points into an unpublished document, and the name of
    the reference pipeline is written as "Reference pipeline".
    """
    text = _INTERNAL_PATH.sub("", text)
    text = _PIPELINE_NAME.sub("Reference pipeline", text)
    text = _EN_DASH_RANGE.sub(r"\1 to \2", text)
    return _EM_DASH.sub(": ", text)


def md_text(text, in_table: bool = False) -> str:
    """Escape free text from the sources, leaving code spans intact.

    Dashes are normalized and internal paths dropped (see `normalize`).
    """
    if text is None:
        return ""
    text = normalize(str(text).strip())
    parts = []
    pos = 0
    for m in _CODE_SPAN.finditer(text):
        parts.append(_escape_text(text[pos:m.start()], in_table))
        span = m.group(0)
        if in_table:
            span = span.replace("|", "\\|")
        parts.append(span)
        pos = m.end()
    parts.append(_escape_text(text[pos:], in_table))
    out = "".join(parts)
    if in_table:
        out = re.sub(r"\s*\n\s*\n\s*", "<br><br>", out)
        out = re.sub(r"\s*\n\s*", "<br>", out)
    return out


def code(value, in_table: bool = True) -> str:
    """Render a literal value as a code span."""
    s = str(value)
    ticks = "`"
    while ticks in s:
        ticks += "`"
    pad = " " if s.startswith("`") or s.endswith("`") else ""
    span = f"{ticks}{pad}{s}{pad}{ticks}"
    if in_table:
        span = span.replace("|", "\\|")
    return span


def fmt_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def load_schemas() -> dict[str, dict]:
    schemas = {}
    for name in FILES:
        path = SRC / f"{name}.yaml"
        with path.open(encoding="utf-8") as fh:
            schemas[name] = yaml.safe_load(fh) or {}
    return schemas


def import_closure(name: str, schemas: dict[str, dict]) -> list[str]:
    """asb_* files imported by `name`, directly or transitively, in order."""
    seen: list[str] = []
    stack = [i for i in (schemas[name].get("imports") or []) if i in schemas]
    while stack:
        current = stack.pop(0)
        if current in seen:
            continue
        seen.append(current)
        stack.extend(i for i in (schemas[current].get("imports") or []) if i in schemas)
    return seen


def counts(schema: dict) -> tuple[int, int, int, int]:
    classes = schema.get("classes") or {}
    n_attrs = sum(len((c or {}).get("attributes") or {}) for c in classes.values())
    return (
        len(classes),
        len(schema.get("slots") or {}),
        n_attrs,
        len(schema.get("enums") or {}),
    )


def tree_roots(schema: dict) -> list[str]:
    return [n for n, c in (schema.get("classes") or {}).items() if (c or {}).get("tree_root")]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def file_anchor(name: str) -> str:
    return f"file-{name}"


class RangeResolver:
    """Links a range to the anchor of its class or enumeration on the page."""

    def __init__(self, name: str, schemas: dict[str, dict]):
        self.default = schemas[name].get("default_range", "string")
        self.where: dict[str, str] = {}
        for src in [name] + import_closure(name, schemas):
            sch = schemas[src]
            for cls in sch.get("classes") or {}:
                self.where.setdefault(cls, "class")
            for enum in sch.get("enums") or {}:
                self.where.setdefault(enum, "enum")

    def link(self, target: str) -> str:
        if target in self.where:
            return f"[{code(target, False)}](#{self.where[target]}-{target})"
        return code(target)

    def render(self, rng) -> str:
        if rng is None:
            return code(self.default)
        if rng in BUILTIN_TYPES and rng not in self.where:
            return code(rng)
        return self.link(rng)


def cardinality(defn: dict) -> str:
    req = bool(defn.get("required"))
    multi = bool(defn.get("multivalued"))
    if multi:
        return "1..*" if req else "0..*"
    return "1" if req else "0..1"


def notes(defn: dict) -> str:
    frags = []
    if "alias" in defn:
        frags.append(f"alias (serialized key): {code(defn['alias'])}")
    if defn.get("identifier"):
        frags.append("identifier: true")
    if "pattern" in defn:
        frags.append(f"pattern: {code(defn['pattern'])}")
    for key in ("minimum_value", "maximum_value"):
        if key in defn:
            frags.append(f"{key}: {fmt_scalar(defn[key])}")
    for key in ("inlined", "inlined_as_list"):
        if key in defn:
            frags.append(f"{key}: {fmt_scalar(defn[key])}")
    if "slot_uri" in defn:
        frags.append(f"slot_uri: {code(defn['slot_uri'])}")
    annotations = defn.get("annotations") or {}
    ordered = sorted(annotations, key=lambda k: (k != "importance",))
    for key in ordered:
        value = annotations[key]
        if isinstance(value, dict) and "value" in value:
            value = value["value"]
        if isinstance(value, list):
            value = ", ".join(fmt_scalar(v) for v in value)
        frags.append(f"{md_text(key, True)}: {md_text(fmt_scalar(value), True)}")
    for key in ("exact_mappings", "close_mappings", "related_mappings",
                "narrow_mappings", "broad_mappings"):
        if defn.get(key):
            frags.append(f"{key}: " + ", ".join(code(v) for v in defn[key]))
    return "; ".join(frags)


def slot_row(slot_name: str, defn: dict, resolver: RangeResolver) -> str:
    defn = defn or {}
    cells = [
        code(slot_name),
        resolver.render(defn.get("range")),
        cardinality(defn),
        md_text(defn.get("description"), True),
        notes(defn),
    ]
    return "| " + " | ".join(cells) + " |"


SLOT_TABLE_HEAD = [
    '<div class="asb-ref" markdown>',
    "",
    "| Slot | Range | Cardinality | Description | Notes |",
    "| --- | --- | --- | --- | --- |",
]


def class_flags(cdef: dict) -> str:
    flags = []
    if cdef.get("tree_root"):
        flags.append("tree root")
    if cdef.get("abstract"):
        flags.append("abstract")
    if cdef.get("mixin"):
        flags.append("mixin")
    if cdef.get("is_a"):
        flags.append(f"is_a: {code(cdef['is_a'], False)}")
    if cdef.get("mixins"):
        flags.append("mixins: " + ", ".join(code(m, False) for m in cdef["mixins"]))
    if cdef.get("class_uri"):
        flags.append(f"class_uri: {code(cdef['class_uri'], False)}")
    for key, value in (cdef.get("annotations") or {}).items():
        if isinstance(value, dict) and "value" in value:
            value = value["value"]
        flags.append(f"{md_text(key)}: {md_text(fmt_scalar(value))}")
    return "; ".join(flags)


def render_classes(name: str, schema: dict, resolver: RangeResolver) -> list[str]:
    classes = schema.get("classes") or {}
    slots = schema.get("slots") or {}
    lines: list[str] = []
    for cname, cdef in classes.items():
        cdef = cdef or {}
        lines += [f"### {cname} {{ #class-{cname} }}", ""]
        if cdef.get("description"):
            lines += [md_text(cdef["description"]), ""]
        flags = class_flags(cdef)
        if flags:
            lines += [f"*Class of `{name}.yaml`; {flags}*", ""]
        else:
            lines += [f"*Class of `{name}.yaml`*", ""]
        rows = []
        for sname in cdef.get("slots") or []:
            if sname not in slots:
                print(f"warning: {name}.yaml: class {cname} lists slot {sname} "
                      "not defined in this file", file=sys.stderr)
            rows.append(slot_row(sname, slots.get(sname) or {}, resolver))
        for aname, adef in (cdef.get("attributes") or {}).items():
            rows.append(slot_row(aname, adef or {}, resolver))
        if not rows:
            lines += ["This class declares no slots or attributes.", ""]
            continue
        lines += [*SLOT_TABLE_HEAD, *rows, "", "</div>", ""]
    return lines


def render_enums(name: str, schema: dict) -> list[str]:
    enums = schema.get("enums") or {}
    lines: list[str] = []
    for ename, edef in enums.items():
        edef = edef or {}
        lines += [f"### {ename} {{ #enum-{ename} }}", ""]
        if edef.get("description"):
            lines += [md_text(edef["description"]), ""]
        lines += [f"*Enumeration of `{name}.yaml`*", ""]
        pvs = edef.get("permissible_values") or {}
        lines += [
            '<div class="asb-ref" markdown>',
            "",
            "| Value | Description |",
            "| --- | --- |",
        ]
        for pv, pdef in pvs.items():
            desc = (pdef or {}).get("description") if isinstance(pdef, dict) else None
            lines.append(f"| {code(pv)} | {md_text(desc, True)} |")
        lines += ["", "</div>", ""]
    return lines


def render_unused(name: str, schema: dict, resolver: RangeResolver) -> list[str]:
    slots = schema.get("slots") or {}
    used = set()
    for cdef in (schema.get("classes") or {}).values():
        used.update((cdef or {}).get("slots") or [])
    unused = [s for s in slots if s not in used]
    if not unused:
        return []
    return [
        f"### Slots of `{name}.yaml` used by no class {{ #unused-{name} }}",
        "",
        *SLOT_TABLE_HEAD,
        *(slot_row(s, slots[s] or {}, resolver) for s in unused),
        "",
        "</div>",
        "",
    ]


def render_file_section(name: str, schemas: dict[str, dict]) -> list[str]:
    schema = schemas[name]
    resolver = RangeResolver(name, schemas)
    title, page = FORMAT_PAGES[name]
    imports = ", ".join(
        f"[{code(i + '.yaml', False)}](#{file_anchor(i)})" if i in schemas else code(i, False)
        for i in (schema.get("imports") or [])
    )
    lines = [f"## {name}.yaml {{ #{file_anchor(name)} }}", ""]
    lines += [
        '<div class="asb-spec-meta">'
        f' <span class="asb-badge asb-badge--version">{name}.yaml {schema.get("version", "")}</span>'
        f' <code>{md_text(schema.get("id", ""))}</code>'
        f' <span>License: {md_text(schema.get("license", ""))}</span>'
        " </div>",
        "",
    ]
    lines += [f"{md_text(schema.get('description', ''))}", ""]
    lines += [f"Schema name {code(schema.get('name', ''), False)}. Imports: {imports}. "
              f"Format page: [{title}]({page}).", ""]
    lines += render_classes(name, schema, resolver)
    lines += render_enums(name, schema)
    lines += render_unused(name, schema, resolver)
    return lines


def render_page(schemas: dict[str, dict]) -> str:
    lines = [
        "# Field reference",
        "",
        "<!-- Generated by scripts/gen_reference.py from src/asb_schema/*.yaml. "
        "Do not edit by hand. -->",
        "",
        "This page lists every class, slot and enumeration of the seven LinkML "
        "files of ASB Schema, one section per file. It is generated from "
        "`src/asb_schema/*.yaml` by `scripts/gen_reference.py`, and CI checks "
        "that it matches the sources.",
        "",
        "## Reading this page",
        "",
        "- Each class has the anchor `#class-<ClassName>` and each enumeration "
        "the anchor `#enum-<EnumName>`; each file section has the anchor "
        "`#file-<file name>`.",
        "- The table of a class lists the slots named under its `slots` key, "
        "then its inline attributes.",
        "- Range is the declared range, or `string` when none is declared. "
        "Cardinality reads `1` (required), `0..1` (optional), `1..*` "
        "(required list) or `0..*` (optional list).",
        "- Notes give the serialized alias, pattern, bounds, `slot_uri`, "
        "annotations (including `importance`) and ontology mappings.",
        "- Descriptions are copied from the sources. An em-dash becomes a "
        "colon, an en-dash between numbers becomes \"to\", a pointer to an "
        "unpublished design note is left out, and the name of the reference "
        "pipeline is written as \"Reference pipeline\".",
        "- Slot names are global in LinkML: loading `asb.yaml` merges slots "
        "that share a name across files. Validate each artifact against its "
        "own file; see [Conformance](conformance.md).",
        "",
        "## Schema files",
        "",
        '<div class="asb-matrix" markdown>',
        "",
        "| File | id | version | Root class | Classes | Slots | Attributes | Enums |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name in FILES:
        sch = schemas[name]
        n_cls, n_slots, n_attrs, n_enums = counts(sch)
        roots = tree_roots(sch)
        root_cell = ", ".join(f"[{code(r, False)}](#class-{r})" for r in roots) or "none"
        lines.append(
            f"| [{code(name + '.yaml', False)}](#{file_anchor(name)}) "
            f"| {code(sch.get('id', ''))} | {md_text(sch.get('version', ''), True)} "
            f"| {root_cell} | {n_cls} | {n_slots} | {n_attrs} | {n_enums} |"
        )
    lines += ["", "</div>", ""]
    for name in FILES:
        lines += render_file_section(name, schemas)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main() -> int:
    schemas = load_schemas()
    write(OUT, render_page(schemas))
    for name in FILES:
        n_cls, n_slots, n_attrs, n_enums = counts(schemas[name])
        print(f"{name}.yaml: classes={n_cls} slots={n_slots} "
              f"attributes={n_attrs} enums={n_enums}")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

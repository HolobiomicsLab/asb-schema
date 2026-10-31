# Glossary

Terms used on this site. Schema terms take their meaning from the LinkML sources in `src/asb_schema/`; each term links to the page that treats it.

<div class="asb-glossary" markdown>

[Agent Skill](../interop/benchmarks-and-agents.md#agent-skills-and-mcp)
:   A directory with a `SKILL.md` file whose YAML front matter has `name` and `description`, followed by Markdown instructions[^as-spec]. Released skill leaves follow this layout.

[artifact family](../schema/index.md)
:   The six artifacts ASB Schema defines: task card, capsule, skill bundle, skill collection, collection registry and exploration trace.

[ASTRA analysis](../interop/analyses-and-research-objects.md#astra)
:   The unit of an ASTRA document (`astra.yaml`): inputs, outputs, decisions with named options and insights backed by evidence[^astra-spec]. A paper becomes a root analysis and each card a sub-analysis.

[bridge](../interop/index.md)
:   A connection from ASB Schema to another format, with a status: existing, feasible or needs new code.

[capsule](../schema/capsule.md)
:   A directory that packages one task card as a research object, with evidence, per-file provenance and an RO-Crate metadata file (`SciTaskCapsule`).

[closed validation](../reference/conformance.md#validation)
:   Validation that rejects keys the target class does not declare, as `linkml-validate` does.

[collection cut](../pipeline/index.md#release)
:   A candidate collection directory with a record `MANIFEST.gen.json` (`asb-cut/v0`) of its inputs, output tree and digests, marked `released: false`.

[collection registry](../schema/skill-collection.md#collection-registry)
:   The list of released skill collections by IRI (`SkillCollectionRegistry`).

[direct check](../pipeline/index.md#evaluation)
:   An automated, deterministic check, such as file existence or a value range, in `EvaluationStrategy.direct_checks`.

[evaluation strategy](../schema/task-card.md)
:   The required card slot that plans how an attempt is checked: `direct_checks` and `expert_review`.

[evidence snippet](../interop/vocabularies-and-claims.md#claims-and-evidence)
:   A verbatim passage from the source with the reason it supports the card (`EvidenceSnippet`).

[expert review](../pipeline/index.md#evaluation)
:   A criterion that needs human judgment, such as scientific validity, in `EvaluationStrategy.expert_review`.

[exploration trace](../schema/exploration-trace.md)
:   The research path behind a paper's outcome as a tree of question, experiment, decision, dead-end and pivot nodes (`ExplorationTree`).

[finding](../schema/task-card.md)
:   The source's answer or result for a task, in the required slot `finding`. A solver receives the task text; the evaluator keeps the finding.

[Harbor task](../interop/benchmarks-and-agents.md#harbor-and-terminal-bench)
:   An executable task directory: instruction, environment, verifier that writes a reward and, optionally, an oracle[^h-overview].

[mapping (exact, close)](../interop/vocabularies-and-claims.md#term-mappings)
:   A LinkML link from a slot to a term of another vocabulary: `exact_mappings` for the same meaning, `close_mappings` for a similar one[^linkml-exact][^linkml-close].

[MergeAuditRecord](../schema/skill-bundle.md)
:   One skill deduplication decision: alias, target slug, similarity evidence and a `MergeDecisionEnum` value.

[minimal conformance](../reference/conformance.md#minimal-conformance)
:   A `task_card.json` that validates against `ASBTaskCard` and a `ro-crate-metadata.json` that conforms to RO-Crate 1.1.

[open validation](../reference/conformance.md#json-schema-roots)
:   Validation against the root of a generated JSON Schema file, which accepts undeclared top-level keys.

[oracle](../interop/benchmarks-and-agents.md#harbor-and-terminal-bench)
:   In Harbor, a reference solution, `solution/solve.sh`, that shows a task can be solved[^h-solution]. The task author adds it to a task derived from a card.

[Process Run Crate](../interop/analyses-and-research-objects.md#ro-crate)
:   An RO-Crate profile for tool executions recorded as `CreateAction` entities with an `instrument`[^prc].

[reference pipeline](../pipeline/index.md)
:   The program maintained by the same laboratory that writes cards, capsules, skill bundles and traces from papers and releases skill collections. Writing cards does not require it.

[release gate](../pipeline/index.md#release)
:   A check run on a collection directory before publication, in the continuous integration of asb-skill-collections.

[reproducibility tier](../pipeline/index.md#evaluation)
:   How far a card's step re-executes: `certified`, `type-checked`, `bypassed`, `manual-only` or `experimental`.

[research question](../schema/task-card.md)
:   The scientific question a task addresses, in the required slot `research_question`.

[reuse readiness](../pipeline/index.md#release)
:   Whether a skill applies outside its source paper, reviewed by the rubric `reuse-readiness/v0`.

[RO-Crate](../interop/analyses-and-research-objects.md#ro-crate)
:   A specification for research-object packages described by one JSON-LD metadata file based on schema.org[^ro-about].

[SciTask](../reference/conformance.md#legacy-identifiers)
:   The name of the standard until 2026-05-24, kept in `SciTaskCapsule`, `scitask_version` and the aliases of `asb_schema.compat`.

[skill](../schema/skill-bundle.md)
:   A reusable, paper-grounded computational competency, deduplicated across papers (`ASBSkill`).

[skill bundle](../schema/skill-bundle.md)
:   A directory describing one skill: `skill.md` and structured sidecar files (`SkillBundle`). A bundle describes one skill; a collection releases many under one license.

[skill collection](../schema/skill-collection.md)
:   A curated, licensed and citable release of skills and tools, serialized as `collection.yaml` (`SkillCollection`).

[slim capsule](../schema/capsule.md)
:   A release copy of a capsule whose `artifact_provenance.json` records `"profile": "slim"`; its card sits in the collection's `benchmark/cards/`.

[slot](../reference/index.md)
:   A property a class can carry[^linkml-models]. `ASBTaskCard` has 64 slots, 15 required.

[support level](../schema/exploration-trace.md)
:   Whether a trace step is stated by the paper (`explicit`) or reconstructed (`inferred`).

[task card](../schema/task-card.md)
:   A structured record of one bounded task extracted from a paper (`ASBTaskCard`), serialized as `task_card.json`.

[task kind](../schema/task-card.md)
:   How a card relates to its source: `reproduction`, `analysis`, `component_reconstruction` or `extension`.

[tree root](../reference/conformance.md#json-schema-roots)
:   The class a LinkML file marks as the root of its documents[^linkml-tree-root].

[unverified](../about/index.md#unverified-points)
:   A point whose check has not been run; such points are listed under Status.

</div>

[^as-spec]: Agent Skills, "Specification". <https://agentskills.io/specification>
[^astra-spec]: ASTRA, "Specification". <https://astra-spec.org/latest/specification/>
[^h-overview]: Harbor documentation, "Tasks overview". <https://docs.harborframework.com/tasks/overview.md>
[^h-solution]: Harbor documentation, "Solution". <https://docs.harborframework.com/tasks/solution.md>
[^linkml-exact]: LinkML Model, "Slot: exact_mappings". <https://linkml.io/linkml-model/latest/docs/exact_mappings/>
[^linkml-close]: LinkML Model, "Slot: close_mappings". <https://linkml.io/linkml-model/latest/docs/close_mappings/>
[^prc]: Workflow Run RO-Crate, "Process Run Crate". <https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/>
[^ro-about]: Research Object Crate (RO-Crate), "About RO-Crate". <https://www.researchobject.org/ro-crate/about_ro_crate>
[^linkml-models]: LinkML, "Models". <https://linkml.io/linkml/schemas/models.html>
[^linkml-tree-root]: LinkML Model, "Slot: tree_root". <https://linkml.io/linkml-model/latest/docs/tree_root/>

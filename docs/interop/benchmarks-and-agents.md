# Benchmarks and agents

Benchmark formats turn a task into something an agent can be scored on; agent formats package skills an agent can load. A card supplies the paper-grounded part of such a task (question, reference result with its published origin, inputs, expected outputs, evaluation plan), and the skill collections supply ready-made skills.

When a card becomes an evaluation item, `finding` is kept out of what the agent sees, since it states the answer.

## Harbor and Terminal-Bench

Terminal-Bench measures how agents perform tasks in a command-line terminal; Harbor is the framework and task format it runs on since version 2.0[^harbor-readme]. Terminal-Bench-Science (TB-Science) applies the format to research workflows written by domain experts[^tbs-contrib].

A Harbor task is an executable directory[^h-overview]:

| Part | Content |
|---|---|
| `instruction.md` | Text passed to the agent at the start of a trial |
| `task.toml` | Configuration: `[task]` name, authors, description, keywords; `[metadata]`; `[verifier]`; `[agent]`; `[environment]`; a top-level `source` string[^h-config] |
| `environment/` | A `Dockerfile` or another environment specification |
| `tests/test.sh` | The verifier; writes a reward to `/logs/verifier/reward.txt` or `reward.json`[^h-verifier] |
| `solution/solve.sh` | The oracle, run to show that the task can be solved[^h-solution] |

TB-Science adds stricter conditions: a required oracle, a binary reward, a separate verifier without network access, an oracle that scores 1 and a nop agent that scores 0, cheat trials, an expert author, and a 39-criterion implementation rubric that includes `ground_truth_provenance` and `novel`[^tbs-contrib][^tbs-rubric].

ASB Schema is upstream of Terminal-Bench. The card supplies:

| Harbor part | From the card |
|---|---|
| Provenance (`source`, `[metadata]`, `authoring/provenance/`) | `crossref_doi`, `source_package`, `evidence_snippets`, `section_provenance` |
| Reference values with their published origin | `finding`, `evidence_snippets` and the claim ledger, which meet the intent of `ground_truth_provenance` |
| Draft `instruction.md` | `task_description`, `research_question`, `inputs`, `expected_outputs` |
| `[task]` name, description and keywords | capsule key `{doi_slug}__{task_id}`, `task_objective` or `title`, `keywords`, `techniques`, `tools` |
| Verifier checks | the typed checks of `eval.json`: `file_exists` and `contains_substring` map to RewardKit criteria[^rewardkit], value and reference checks to assertions, `llm_judge` to a judge |

The task author adds the oracle (from the paper's code repository, from reference outputs, or from a verified agent solution), discriminating thresholds, a pinned environment and the author list. After emission, `harbor lint`, an oracle run (reward 1), a nop run (reward 0) and `asb judge-trials` check the task.

!!! bridge "ASB Schema to Harbor tasks"
    <span class="asb-badge asb-badge--hard">needs new code</span>

    A `harbor` format of `asb export-workflow` writes `task.toml`, the draft instruction, the provenance folder and the derived verifier; the oracle and the verifier thresholds are authored per task. Task versions follow the continuous-benchmark rule of Terminal-Bench: metadata change is a patch, verifier change a minor version, environment or data change a major version[^tb-continuous].

The `leaves/` directory of a released collection, whose children each hold a `SKILL.md`, has the layout that `harbor run --skill` accepts and that a task bundles under `environment/skills/`[^h-jobs-skills] (<span class="asb-badge asb-badge--feasible">feasible</span>). Harbor trial artifacts map to a submission scored by `asb run-eval --submission` (<span class="asb-badge asb-badge--feasible">feasible</span>).

## ScienceAgentBench

ScienceAgentBench holds 102 data-driven tasks from 44 peer-reviewed publications, each answered by a self-contained Python program and checked by an evaluation program[^sab-repo].

!!! bridge "ASB Schema to the ScienceAgentBench annotation sheet"
    <span class="asb-badge asb-badge--existing">existing</span>

    `sab-export` writes one JSON Lines record per card with nine of the twelve annotation fields, `output_fname` from `expected_artifact_name`, and `source_paper_doi`, `source_paper_title` and `schema_version`. The executable layout adds per-task datasets from `data_accessions` and `available_artifacts`, a gold program for `certified` cards and evaluation programs from `eval.json`.

## PaperBench

PaperBench grades the replication of a whole paper with a weighted rubric tree of `TaskNode` entries, judged by a language model[^pb-repo].

!!! bridge "ASB Schema to and from PaperBench"
    <span class="asb-badge asb-badge--existing">existing</span>

    `export-paperbench` converts the runtime `eval.json` and `rubric.json` into `TaskNode` trees, and `import-paperbench` maps the judge's verdicts back to the check identifiers. A full paper directory adds the paper in PDF and Markdown, `addendum.md`, `blacklist.txt` and `config.yaml`.

## MLE-bench

MLE-bench evaluates agents on machine-learning competitions, each with `config.yaml`, `prepare.py`, `grade.py` and a leaderboard[^mle-comp].

!!! bridge "ASB Schema to MLE-bench"
    <span class="asb-badge asb-badge--hard">needs new code</span>

    An exporter writes `task_description.txt`, `submission_format.json`, `task_meta.json` and a grading stub. Cards that describe predictive modeling map; grading against a leaderboard needs the competition layout and reference scores.

## Inspect

Inspect, from the UK AI Security Institute, defines an evaluation as a `Task`: a dataset of `Sample` items, a solver and a scorer[^inspect-tasks].

!!! bridge "ASB Schema to Inspect"
    <span class="asb-badge asb-badge--feasible">feasible</span>

    One `Sample` per card: `id` from `task_id`, `input` from `task_description`, `inputs` and `workflow_description`, `target` from `finding` or `expected_outputs`, the other slots in `metadata`[^inspect-datasets]. A scorer from the `eval.json` checks, a judge scorer for `expert_review`, and `Task.version` from `schema_version`.

## Paper-derived benchmarks

Several benchmarks ask questions about published analyses. Each maps from a card with a short canonical answer distilled from `finding` and a data capsule.

| Benchmark | Description | Card mapping | Status |
|---|---|---|---|
| BixBench | Questions about bioinformatics analysis capsules from published notebooks[^bix-hf] | `research_question` to `question` and `hypothesis`, `crossref_doi` to `paper`, capsule data to `data_folder`; a short answer, distractors and a canary | <span class="asb-badge asb-badge--feasible">feasible</span> |
| CORE-Bench | Reproduction of CodeOcean capsules, answers within a prediction interval of three runs[^core-hf] | `task_description` to `task_prompt`, a code DOI to `capsule_doi`, `domain` to `field`, numeric values of `finding` to `results`; `certified` cards with a linked repository | <span class="asb-badge asb-badge--feasible">feasible</span> |
| DiscoveryBench | Data-driven hypothesis discovery tasks[^db-hf] | `research_question` to `question`, `finding` to `true_hypothesis`, `workflow_description` to the gold workflow, `techniques` to `workflow_tags`; dataset files and column descriptions | <span class="asb-badge asb-badge--feasible">feasible</span> |

## Agent Skills and MCP

Agent Skills is a format in which a skill is a directory with a `SKILL.md` file whose YAML front matter has a `name` (1 to 64 characters, equal to the directory name) and a `description` (up to 1,024 characters), with optional `license`, `compatibility`, `metadata` (string keys to string values) and `allowed-tools`; `skills-ref validate` checks a skill[^skills-spec][^skills-validator].

!!! bridge "ASB Schema to Agent Skills"
    <span class="asb-badge asb-badge--existing">existing</span>

    Every released skill is a `SKILL.md` leaf with `name`, a "Use when" `description`, `license` and `metadata` (EDAM operation and topics, tools), plus provenance keys `derived_from`, `evidence_spans`, `claims`, `provenance` and `attribution`. Strict conformance places the provenance keys under `metadata` as strings or in a sidecar file, keeps names within 64 characters, and adds `skills-ref validate` to the release gate.

The Skills extension of the Model Context Protocol (MCP) lets a server list and serve skills: `skills/list` and `skills/get` return the front matter, and a manifest gives each file's URI, SHA-256 digest and size[^mcp-skills].

!!! bridge "ASB Schema to the MCP Skills extension"
    <span class="asb-badge asb-badge--feasible">feasible</span>

    An MCP server over a released collection serves its leaves. Writing the collection's `skills` and `tools` as `.../asb-skill/<slug>@sha256:<hash>` IRIs, as the slot descriptions define, lets the collection pins and the MCP digests agree.

## See also

- [How the artifacts are produced](../pipeline/index.md#evaluation): `eval.json` and scores.
- [Skill bundle](../schema/skill-bundle.md) and [Skill collection](../schema/skill-collection.md)

[^harbor-readme]: GitHub, "harbor-framework/harbor" (README). <https://github.com/harbor-framework/harbor>
[^tbs-contrib]: GitHub, "terminal-bench-science/CONTRIBUTING.md". <https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/CONTRIBUTING.md>
[^tbs-rubric]: GitHub, "terminal-bench-science/rubrics/task-implementation.toml". <https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/rubrics/task-implementation.toml>
[^h-overview]: Harbor documentation, "Tasks overview". <https://docs.harborframework.com/tasks/overview.md>
[^h-config]: Harbor documentation, "Task configuration". <https://docs.harborframework.com/tasks/configuration.md>
[^h-verifier]: Harbor documentation, "Verifier". <https://docs.harborframework.com/tasks/verifier.md>
[^h-solution]: Harbor documentation, "Solution". <https://docs.harborframework.com/tasks/solution.md>
[^rewardkit]: Harbor, "Built-in criteria". <https://docs.harborframework.com/rewardkit/built-in-criteria.md>
[^tb-continuous]: Terminal-Bench, "Continuous Benchmarks". <https://www.tbench.ai/news/continuous-benchmarks>
[^h-jobs-skills]: Harbor documentation, "Skills" (jobs). <https://docs.harborframework.com/jobs/skills.md>
[^sab-repo]: GitHub, "OSU-NLP-Group/ScienceAgentBench". <https://github.com/OSU-NLP-Group/ScienceAgentBench>
[^pb-repo]: GitHub, "frontier-evals/project/paperbench". <https://github.com/openai/frontier-evals/tree/main/project/paperbench>
[^mle-comp]: GitHub, "openai/mle-bench, competitions/spaceship-titanic". <https://github.com/openai/mle-bench/tree/main/mlebench/competitions/spaceship-titanic>
[^inspect-tasks]: UK AI Security Institute, "Inspect: Tasks". <https://inspect.aisi.org.uk/tasks.html>
[^inspect-datasets]: UK AI Security Institute, "Inspect: Datasets". <https://inspect.aisi.org.uk/datasets.html>
[^bix-hf]: Hugging Face, "futurehouse/BixBench". <https://huggingface.co/datasets/futurehouse/BixBench>
[^core-hf]: Hugging Face, "siegelz/core-bench". <https://huggingface.co/datasets/siegelz/core-bench>
[^db-hf]: Hugging Face, "allenai/discoverybench". <https://huggingface.co/datasets/allenai/discoverybench>
[^skills-spec]: Agent Skills, "Specification". <https://agentskills.io/specification>
[^skills-validator]: GitHub, "skills-ref/src/skills_ref/validator.py". <https://github.com/agentskills/agentskills/blob/main/skills-ref/src/skills_ref/validator.py>
[^mcp-skills]: Model Context Protocol, "Skills" (extension overview). <https://modelcontextprotocol.io/extensions/skills/overview>

# hstack

hstack brings Lauren Tan's pstack engineering workflows to Cursor and Codex. It includes 45 distinctly named skills, two named agents, and 18 configurable model roles. For implementation in Cursor, hstack defaults to Cursor building and Codex reviewing, with one bounded Codex rescue for a confirmed code blocker. Existing model choices are preserved.

This repository publishes the generated packages. The [maintained source](https://github.com/huankoh/plugins/tree/feat/pstack-codex-support/pstack/hybrid) and [adaptation PR](https://github.com/huankoh/plugins/pull/1) show the changes from [upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). hstack is maintained by huankoh and is not an official Cursor or OpenAI release.

## Install

The namespaced release remains on `feat/namespaced-hstack-skills` for review; `main` still contains the earlier package. The live discovery checks used distribution commit `66b1ac1ac6ae2c190a9ff20a9f1db28f367c4977` and runtime source `bbe9d3e5d3f3531227e4c5d88da99a6394540bb1`.

**Cursor plugin:** Register the tested remote marketplace with Cursor Agent CLI:

```bash
agent plugin marketplace add https://github.com/huankoh/hstack.git --git-ref 66b1ac1ac6ae2c190a9ff20a9f1db28f367c4977
```

Then open native Cursor's **Customize → Add**, choose **hstack**, and install it. Registration alone does not install the plugin. If an older marketplace named hstack is registered, follow the [replacement procedure](cursor/plugins/hstack/hybrid/docs/cursor-local.md#install-the-pinned-remote-marketplace); preserve the original pstack marketplace.

**Codex CLI or desktop:** Clone this repository, then register its marketplace from the clone root:

```bash
git clone --branch feat/namespaced-hstack-skills https://github.com/huankoh/hstack.git
cd hstack
codex plugin marketplace add "$PWD"
codex plugin add hstack@hstack
```

**Cursor personal skills:** From a clone of this repository, export the complete generated Cursor package:

```bash
python3 -m venv .venv
.venv/bin/pip install -r cursor/plugins/hstack/hybrid/requirements.txt
.venv/bin/python cursor/plugins/hstack/hybrid/install-cursor-skills.py cursor/plugins/hstack
```

This manages only the generated `hstack-` directories under `~/.cursor/skills` and preserves original pstack and unrelated personal skills. It refuses unrecognized existing directories or local edits. Fresh Cursor cloud discovery passed with the pinned marketplace installed and **Sync Skills for Cloud Agents** enabled after personal export. The selected path was the native plugin cache. Both settings changed together, so the result does not isolate sync as the cause. Sync applies to the entire personal skills directory. Earlier startup exports did not establish discovery; use the [tested combined setup](cursor/plugins/hstack/hybrid/docs/cursor-cloud.md) and [invocation guide](cursor/plugins/hstack/hybrid/docs/invocation.md).

## Choose hstack explicitly

Open a new task after installation and use the full portable name:

| Host | hstack | Original pstack |
|---|---|---|
| Cursor | `/hstack-poteto-mode` | `/poteto-mode` |
| Codex qualified catalog, local or tested cloud | `$hstack:hstack-poteto-mode` | `$pstack:poteto-mode` |
| Codex unqualified catalog | `$hstack-poteto-mode` | `$poteto-mode` |
| Grok Bot | Ask the hstack-configured bot to use `hstack-poteto-mode` | Use the original bot and its pstack workflow |

All 45 generated skills have the prefix, including `hstack-how` and `hstack-setup-pstack`. Codex can add the package namespace even when skills are staged through `.agents/skills`; use the qualified or unqualified entry shown by the actual catalog. `hstack:poteto-mode` omits the renamed skill identifier. Setup uses `/hstack-setup-pstack` in Cursor and the matching `$hstack:hstack-setup-pstack` or `$hstack-setup-pstack` entry in Codex. You do not need to change models to start.

After hstack is selected, its `SKILL-MAP.json` resolves sibling workflows and delegated agents to exact files in that package. Missing hstack instructions are reported instead of silently selecting upstream pstack. Portable Cursor exports keep one discoverable wrapper per skill and store supporting workflow files as `WORKFLOW.md` inside the shared payload. The map is adjusted for those paths.

## Choose a host

| Host | Setup and observed limits |
|---|---|
| Cursor local | The native catalog exposed 45 hstack skills and two agents. Normal entrypoint loading passed without an explicit file path; the probe performed no Codex job or authentication. |
| Codex CLI / desktop | A fresh native catalog found 45 hstack skills alongside 45 original pstack skills, with distinct qualified names. This verified discovery and coexistence, not a model's completed review. |
| Codex cloud | [Fresh namespaced discovery](plugins/hstack/hybrid/docs/codex-cloud.md#verify-discovery-before-using-the-workflow) passed at runtime source `bbe9d3e`. The entrypoint, adapter, and mapped sibling instructions resolved. Native spawn was unavailable, so that run did not perform independent delegation. |
| Cursor cloud VM | [Fresh discovery](cursor/plugins/hstack/hybrid/docs/cursor-cloud.md#recorded-fresh-cloud-result) passed with the pinned marketplace plus personal sync. It loaded the native cache and same-package workflows. Normal authentication startup was restored separately; this discovery test did not run Codex. |
| Grok Bot | Dr. EggBot (hstack), configured separately at runtime source `bbe9d3e`, passed 21 namespace and preservation checks. Original bots, model preferences, and paused routines were preserved. This distribution contains no private bot profiles; Grok-side Codex execution remains unverified. |

The hybrid workflow is coordinated by the active agent. Installation does not start a daemon, select a cloud host, authorize external actions, or provide Codex login. A saved authentication seed was tested on one fresh Cursor VM; automatic renewal across fresh or concurrent VMs is not implemented. Keep credentials outside this repository.

## Source and updates

The live checks above used runtime source `bbe9d3e` and distribution `66b1ac1`.
Source `cee4295a3b8cf6f469a38685e2b52f43f2e815dd` adds six documentation updates
recording those results; it changes no runtime code. Packaging that documentation
refresh produces a new package fingerprint without changing the tested client or
cloud installations. See the [verification record](cursor/plugins/hstack/hybrid/docs/verification.md)
for the exact scope of each result.

- Source revision: `cee4295a3b8cf6f469a38685e2b52f43f2e815dd`.
- Source fingerprint: `7947aa059b0c4b91ad9c25ffb69b3a95e8e69e4e686bacde8c50441f20157626`.
- Each package retains its original `BUILD.json`; [DISTRIBUTION.json](DISTRIBUTION.json) records packaging changes separately.
- [UPDATE.md](UPDATE.md) explains how to build and review an update.
- [SANITIZATIONS.md](SANITIZATIONS.md) lists documentation files whose private execution references were replaced. Example-domain links are placeholders, not public evidence links.

The distribution preserves the generated source's namespaced skills, two agents, `SKILL-MAP.json`, runtime scripts, runner behavior, model defaults, and Codex default-prompt array. Distribution manifests identify this repository; private task, environment, build, worker, and CI-run references in copied documentation are sanitized. Source adapters and wrappers already differ from upstream pstack; packaging does not remove those changes.

## License

[MIT](LICENSE), retaining Lauren Tan's pstack copyright and attribution. Runtime-specific hstack additions are maintained by huankoh. The original pstack README and license remain inside each package.

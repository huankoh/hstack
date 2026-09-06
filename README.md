# hstack

hstack brings Lauren Tan's pstack engineering workflows to Cursor and Codex. It includes 45 distinctly named skills, two named agents, and 18 configurable model roles. For implementation in Cursor, hstack defaults to Cursor building and Codex reviewing, with one bounded Codex rescue for a confirmed code blocker. Existing model choices are preserved.

This repository publishes the generated packages. The [maintained source](https://github.com/huankoh/plugins/tree/feat/pstack-codex-support/pstack/hybrid) and [adaptation PR](https://github.com/huankoh/plugins/pull/1) show the changes from [upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). hstack is maintained by huankoh and is not an official Cursor or OpenAI release.

## Install

**Cursor plugin:** Open Customize → Add Marketplace → Import from GitHub, enter `https://github.com/huankoh/hstack`, then choose **hstack**. This repository puts the hstack marketplace on its default branch. Native import and discovery of the current generated version require verification in the actual client. Exported skill directories provide a separate installation route; the cloud startup export remains experimental.

**Codex CLI or desktop:** Clone this repository, then register its marketplace from the clone root:

```bash
git clone https://github.com/huankoh/hstack.git
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

This manages only the generated `hstack-` directories under `~/.cursor/skills` and preserves original pstack and unrelated personal skills. It refuses unrecognized existing directories or local edits. For cloud agents, **Sync Skills for Cloud Agents** is another route when available; personal sync applies to the entire personal skills directory. The documented startup export is experimental. The first fresh probe at source `8b2ed0c` exposed hstack setup but omitted its poteto entrypoint. This source removes the entrypoint's inherited Cursor mode restrictions; a fresh cloud test of that fix is pending. See [automatic discovery](cursor/plugins/hstack/hybrid/docs/invocation.md) and [cloud setup](cursor/plugins/hstack/hybrid/docs/cursor-cloud.md) before configuring that host.

## Choose hstack explicitly

Open a new task after installation and use the full portable name:

| Host | hstack | Original pstack |
|---|---|---|
| Cursor | `/hstack-poteto-mode` | `/poteto-mode` |
| Codex native plugin picker | `$hstack:hstack-poteto-mode` | Select the original pstack plugin entry |
| Codex portable skill installation | `$hstack-poteto-mode` | `$poteto-mode` |
| Grok Bot | Ask the hstack-configured bot to use `hstack-poteto-mode` | Use the original bot and its pstack workflow |

All 45 generated skills have the prefix, including `hstack-how` and `hstack-setup-pstack`. Codex's native plugin picker adds the plugin namespace, producing `$hstack:hstack-poteto-mode`; portable skill installation uses `$hstack-poteto-mode`. `hstack:poteto-mode` omits the renamed skill identifier. Setup uses `/hstack-setup-pstack` in Cursor, `$hstack:hstack-setup-pstack` in Codex's native plugin picker, or `$hstack-setup-pstack` for portable Codex skills. You do not need to change models to start.

After hstack is selected, its `SKILL-MAP.json` resolves sibling workflows and delegated agents to exact files in that package. Missing hstack instructions are reported instead of silently selecting upstream pstack. Portable Cursor exports keep one discoverable wrapper per skill and store supporting workflow files as `WORKFLOW.md` inside the shared payload. The map is adjusted for those paths.

## Choose a host

| Host | Setup and observed limits |
|---|---|
| Cursor local | Earlier plugin installation and real Codex review passed on the versions in the [verification record](cursor/plugins/hstack/hybrid/docs/verification.md). Check the renamed entrypoint in a fresh task after updating. |
| Codex CLI / desktop | Generated package validation and unique skill names can be checked locally. Direct Codex work uses its native adapter; client discovery must be verified after refresh. |
| Codex cloud | [Cloud setup](plugins/hstack/hybrid/docs/codex-cloud.md) stages a pinned source build. Earlier discovery tests used the previous names; independent delegation availability varied by task. |
| Cursor cloud VM | Startup skill-directory export in the [environment guide](cursor/plugins/hstack/hybrid/docs/cursor-cloud.md) is experimental. The first probe exposed hstack setup but omitted poteto. Its inherited mode restrictions are now removed; fresh cloud verification is pending. Earlier explicit-loading Codex review tests do not prove automatic activation. |
| Grok Bot | Follow the [Grok guide](cursor/plugins/hstack/hybrid/docs/grok-bot.md). The Dr. EggBot template adaptation was configured separately; this distribution contains no personal bot profiles. Grok-side Codex authentication and an actual coding run remain unverified. |

The hybrid workflow is coordinated by the active agent. Installation does not start a daemon, select a cloud host, authorize external actions, or provide Codex login. A saved authentication seed was tested on one fresh Cursor VM; automatic renewal across fresh or concurrent VMs is not implemented. Keep credentials outside this repository.

## Source and updates

- Source revision: `bbe9d3e5d3f3531227e4c5d88da99a6394540bb1`.
- Source fingerprint: `dc2ec751f51e2bba5a24770ed321447aea68f1aa14e25a9d4a5b4038b9fac868`.
- Each package retains its original `BUILD.json`; [DISTRIBUTION.json](DISTRIBUTION.json) records packaging changes separately.
- [UPDATE.md](UPDATE.md) explains how to build and review an update.
- [SANITIZATIONS.md](SANITIZATIONS.md) lists documentation files whose private execution references were replaced. Example-domain links are placeholders, not public evidence links.

The distribution preserves the generated source's namespaced skills, two agents, `SKILL-MAP.json`, runtime scripts, runner behavior, model defaults, and Codex default-prompt array. Distribution manifests identify this repository; private task, environment, build, worker, and CI-run references in copied documentation are sanitized. Source adapters and wrappers already differ from upstream pstack; packaging does not remove those changes.

## License

[MIT](LICENSE), retaining Lauren Tan's pstack copyright and attribution. Runtime-specific hstack additions are maintained by huankoh. The original pstack README and license remain inside each package.

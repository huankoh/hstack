# hstack

hstack brings Lauren Tan's pstack engineering workflows to Cursor and Codex. It includes 45 skills, 18 configurable model roles, and an optional workflow where Cursor builds, Codex reviews, and Codex may attempt one bounded rescue for a confirmed code blocker. Existing model choices are preserved.

This repository publishes the generated packages. The [maintained source](https://github.com/huankoh/plugins/tree/feat/pstack-codex-support/pstack/hybrid) and [adaptation PR](https://github.com/huankoh/plugins/pull/1) show the changes from [upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). hstack is maintained by huankoh and is not an official Cursor or OpenAI release.

## Install

**Cursor local:** Open Customize → Add Marketplace → Import from GitHub, enter `https://github.com/huankoh/hstack`, then choose **hstack**. This repository puts the hstack marketplace on its default branch. Import of this new repository still needs a live UI check; you can also clone the repository and select its folder through Import from Disk.

**Codex CLI or desktop:** Clone this repository, then register its marketplace from the clone root:

```bash
git clone https://github.com/huankoh/hstack.git
cd hstack
codex plugin marketplace add "$PWD"
codex plugin add hstack@hstack
```

Open a new task, select hstack's **poteto-mode**, and provide your engineering request. In Codex, use `$poteto-mode`; in Cursor, use `/poteto-mode`. Use the skill supplied by hstack when similarly named plugins are installed. `/setup-pstack` remains the inherited configuration command; you do not need to change models to start.

## Choose a host

| Host | Setup and observed limits |
|---|---|
| Cursor local | Plugin installation and real Codex review passed on the source version recorded in the [verification record](cursor/plugins/hstack/hybrid/docs/verification.md). Some native catalog entries and cached auxiliary assets varied. |
| Codex CLI / desktop | Native package validation and skill discovery passed; direct Codex work uses the Codex adapter. |
| Codex cloud | [Cloud setup](plugins/hstack/hybrid/docs/codex-cloud.md) stages a pinned source build. Poteto-mode discovery was verified; independent delegation availability varied by task. |
| Cursor cloud VM | Follow the [environment guide](cursor/plugins/hstack/hybrid/docs/cursor-cloud.md). Staged workflows and real Codex review passed. Native cloud plugin discovery remains unresolved. Local installation does not configure a cloud VM. |
| Grok Bot | Follow the [Grok guide](cursor/plugins/hstack/hybrid/docs/grok-bot.md). The Dr. EggBot template adaptation was configured separately; this distribution contains no personal bot profiles. Grok-side Codex authentication and an actual coding run remain unverified. |

The hybrid workflow is coordinated by the active agent. Installation does not start a daemon, select a cloud host, authorize external actions, or provide Codex login. A saved authentication seed was tested on one fresh Cursor VM; automatic renewal across fresh or concurrent VMs is not implemented. Keep credentials outside this repository.

## Source and updates

- Source revision: `f2af6ce3467a49c186d8eafe63646e31376ec7e8`.
- Source fingerprint: `f1d286441e5af845199f78f34051b72de276df38c96994a8797962d6e8a1e382`.
- Each package retains its original `BUILD.json`; [DISTRIBUTION.json](DISTRIBUTION.json) records packaging changes separately.
- [UPDATE.md](UPDATE.md) explains how to build and review an update.
- [SANITIZATIONS.md](SANITIZATIONS.md) lists documentation files whose private execution references were replaced. Example-domain links are placeholders, not public evidence links.

Runtime scripts, runner behavior, model defaults, and upstream skill bodies are unchanged from the generated source packages. Distribution manifests identify this repository; private task, environment, Build, worker and CI-run references in the copied documentation are sanitized.

## License

[MIT](LICENSE), retaining Lauren Tan's pstack copyright and attribution. Runtime-specific hstack additions are maintained by huankoh. The original pstack README and license remain inside each package.

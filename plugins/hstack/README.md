# pstack

i'm [poteto](https://x.com/poteto). i'm not a president or ceo, but i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler.

there's a growing sense that ai writes too much slop code. i agree. i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first. 

**pstack is my answer.** these are the same skills i use everyday to ship high quality code at Cursor. this turns cursor into a real engineering team. the goal is not to maximize loc, in fact it's the opposite. pstack helps you write less, but higher quality code.

**pstack gives you fearless parallelism.** when you can go deep on one agent and trust it to write good, verifiable code, you can truly parallelize with confidence. start multiple agents up with `hstack-poteto-mode` and trust that they'll apply rigorous engineering principles to their work.

**cursor gives you the best of all worlds.** every frontier model has its strengths and weaknesses. use any model with pstack. in fact, many of my skills use multi-model workflows to take advantage of each model's unique strengths.

fork it. improve it. make it yours. PRs are welcome! 

## install

```bash
/add-plugin pstack
```

## get started

two steps:

1. run [`/hstack-setup-pstack`](skills/hstack-setup-pstack/SKILL.md) and choose which models you want.
2. use [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) whenever you're doing anything that requires rigor.

new here? the [pstack guide](docs/guide/README.md) walks you through a first real task, from setup and prompting through verification and overnight runs.

that's it. the other skills are situational; the mode skill uses them for you as needed. out of the box the mode splits work by model strength: precisely-specified code, prose, and judgment go to fable 5.1, while fast mechanical code goes to grok. the default panel is fable 5.1 / sol / grok / opus 5. [`/hstack-setup-pstack`](skills/hstack-setup-pstack/SKILL.md) changes any of it.

## usage

use [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) at the start of a task. it reads your request, picks from a set of playbooks, and runs the other skills as the steps need them.

### just use [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md)

this skill is the main shortcut. i use it whenever i need the agent to do rigorous engineering work. it comes with twenty-two playbooks:

```
/hstack-poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro
first, then fix and verify.
```

```
/hstack-poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by
morning.
```

<details>
<summary>the twenty-two playbooks</summary>

| playbook | for |
|---|---|
| [investigation](skills/hstack-poteto-mode/playbooks/investigation.md) | a read-only question. how does x work, why was y built this way, are we sure. |
| [bug fix](skills/hstack-poteto-mode/playbooks/bug-fix.md) | reproduce a defect, root-cause it, and fix with runtime evidence. |
| [perf](skills/hstack-poteto-mode/playbooks/perf-issue.md) | trace a measured slowness and improve it against a baseline. |
| [hillclimb](skills/hstack-poteto-mode/playbooks/hillclimb.md) | sustained, scientific improvement of one metric against a target, looping hypotheses with before/after measurement and one commit per accepted win. |
| [runtime forensics](skills/hstack-poteto-mode/playbooks/runtime-forensics.md) | diagnose a live symptom (leak, idle-cpu spin, glitch) from instrumentation. |
| [trace forensics](skills/hstack-poteto-mode/playbooks/trace-forensics.md) | diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot). |
| [feature](skills/hstack-poteto-mode/playbooks/feature.md) | new or changed behavior, built from a named data shape. |
| [refactoring](skills/hstack-poteto-mode/playbooks/refactoring.md) | a behavior-preserving change to structure or shape. |
| [prototype](skills/hstack-poteto-mode/playbooks/prototype.md) | a throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it. |
| [visual parity](skills/hstack-poteto-mode/playbooks/visual-parity.md) | pixel-exact ui equivalence between two implementations. |
| [authoring a skill](skills/hstack-poteto-mode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md. |
| [eval](skills/hstack-poteto-mode/playbooks/eval.md) | test how a skill or prompt change affects agent behavior, blinded. |
| [babysit](skills/hstack-poteto-mode/playbooks/babysit.md) | drive a pr or a stack to merge-ready: conflicts, review threads, ci. |
| [shipping](skills/hstack-poteto-mode/playbooks/shipping.md) | independently verify a green stack, then land the contiguous verified run bottom-up through github by default or origin when available. |
| [autonomous run](skills/hstack-poteto-mode/playbooks/autonomous-run.md) | drive a long task to completion without stopping. |
| [orchestrate](skills/hstack-poteto-mode/playbooks/orchestrate.md) | a standing project handed to one coordinator chat: multi-day, many stacked prs, fleets of subagents. |
| [autopilot-full](skills/hstack-poteto-mode/playbooks/autopilot-full.md) | run independent prs to merged with one owner per pr and root verification of each merge-ready head. |
| [autopilot-stack](skills/hstack-poteto-mode/playbooks/autopilot-stack.md) | build and verify one linear base-branch stack for the operator to review and land. |
| [session pickup](skills/hstack-poteto-mode/playbooks/session-pickup.md) | resume or take over a prior agent's in-flight work. |
| [pause safely](skills/hstack-poteto-mode/playbooks/pause-safely.md) | suspend in-flight work cleanly so it can be resumed later. |
| [multi-phase plan](skills/hstack-poteto-mode/playbooks/multi-phase-plan.md) | work that spans phases or stacked PRs. |
| [worktree cleanup](skills/hstack-poteto-mode/playbooks/worktree-cleanup.md) | reclaim disk by pruning merged or abandoned worktrees and stale ios simulators, safety-gated. |

</details>



when invoked it:

1. opens a todo list. the first item is reading the inline principles index in the skill.
2. matches your task to a [playbook](skills/hstack-poteto-mode/playbooks) and copies the steps in verbatim.
3. routes to the other skills as the steps fire.
4. writes unslopped replies framed for the consumer and the maintainer.

the full rules and playbooks live in [`skills/hstack-poteto-mode/SKILL.md`](skills/hstack-poteto-mode/SKILL.md).

[`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) is also a sticky mode: once entered it stays on across turns, applying itself when a playbook matches or the task needs rigor and staying out of the way otherwise. opt out any time by saying so.

[`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) works extremely well with cursor's `/loop` command. you can make cursor work for many hours without sacrificing rigor.

## skills

[`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) runs most of these for you when a step needs them (`hstack-how`, `hstack-why`, `hstack-architect`, `hstack-arena`, `hstack-swarm`, `hstack-interrogate`, `hstack-unslop`, `hstack-no-comments`, `hstack-technical-writing`, `hstack-tdd`, and the principles). the table below is for when you want one directly:

```
/hstack-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
/hstack-interrogate review this pr.
```

<details>
<summary>all skills</summary>

| skill | use it when |
|---|---|
| [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) | default entry point for any non-trivial task. |
| [`/hstack-how`](skills/hstack-how/SKILL.md) | you want a walkthrough of how a subsystem works. |
| [`/hstack-why`](skills/hstack-why/SKILL.md) | you want to know why something was built this way. discovers available MCPs at run time and queries each evidence category in parallel (source control, issue tracker, long-form docs, real-time chat, infra observability, error tracking, analytics warehouse). |
| [`/hstack-recall`](skills/hstack-recall/SKILL.md) | you're starting or resuming work and want your recent context on a topic rebuilt from your own chat history and the shared record, handed back as a tight current-state brief. |
| [`/hstack-blast-radius`](skills/hstack-blast-radius/SKILL.md) | you have a small-looking change and want to know what else it could break, with the one fact it's safe because of proven by running code, not asserted. |
| [`/hstack-architect`](skills/hstack-architect/SKILL.md) | you're about to write code that crosses a function boundary and want the caller's usage, types, and module shape settled first. |
| [`/hstack-arena`](skills/hstack-arena/SKILL.md) | you want N parallel attempts at the same thing, then to grab the best parts of each. |
| [`/hstack-swarm`](skills/hstack-swarm/SKILL.md) | you want N parallel workers across different slices or races, then one aggregated report. |
| [`/hstack-interrogate`](skills/hstack-interrogate/SKILL.md) | you have a diff and want several different models to try to break it, including a strict code-quality lens. |
| [`/hstack-automate-me`](skills/hstack-automate-me/SKILL.md) | you want your own `-mode` skill, drafted from how you've actually worked. |
| [`/hstack-make-bot-ui`](skills/hstack-make-bot-ui/SKILL.md) | you want a page or dashboard whose buttons wake a Grok Bot over a webhook, including the sender-key handoff and Tailscale. |
| [`/hstack-setup-pstack`](skills/hstack-setup-pstack/SKILL.md) | you want to pick which models pstack uses per role. detects your models and writes a config rule. |
| [`/hstack-reflect`](skills/hstack-reflect/SKILL.md) | a long task landed and you want the recipe captured as a skill edit. |
| [`/hstack-teach`](skills/hstack-teach/SKILL.md) | you want to actually understand a change or subsystem, not just have it summarized. runs how + why and weaves one plain explanation, built up diagram by diagram. |
| [`/hstack-tdd`](skills/hstack-tdd/SKILL.md) | you're fixing a bug and there's a cheap local test path. write the failing test first, then the fix. |
| [`/hstack-no-comments`](skills/hstack-no-comments/SKILL.md) | strip comments before review; spawns hstack-comment-sicko, fixes accepted findings, offers encodings for claimed constraints. |
| [`/hstack-typescript-best-practices`](skills/hstack-typescript-best-practices/SKILL.md) | you're reading or editing typescript. grounds the type-system-discipline principle in syntax. |
| [`/hstack-figure-it-out`](skills/hstack-figure-it-out/SKILL.md) | no bundled playbook fits. designs a rigorous, auditable playbook for the task. |
| [`/hstack-show-me-your-work`](skills/hstack-show-me-your-work/SKILL.md) | you want a reviewable decision trail. logs decisions to a tsv you can commit. |
| [`/hstack-create-verification-skill`](skills/hstack-create-verification-skill/SKILL.md) | your project has no scripted way to prove app behavior. generates a project-local verify skill with a feature map, for any language or platform. |
| [`/hstack-maintain-verification-skill`](skills/hstack-maintain-verification-skill/SKILL.md) | your verify skill's feature map has drifted from the app. source wave + one live pass, at most one PR of proven corrections. |
| [`/hstack-unslop`](skills/hstack-unslop/SKILL.md) | you're cleaning up writing. removes AI tells. |
| [`/hstack-bro`](skills/hstack-bro/SKILL.md) | you want the last message restated in plain human language, no jargon. |
| [`/hstack-technical-writing`](skills/hstack-technical-writing/SKILL.md) | layered doc standard (Diátaxis + Google developer style + STE + Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |

</details>



### examples

mostly i type [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) at the start of a task and let it route to a playbook. the other skills fire as the steps need them. a few i reach for directly.


<details>
<summary>all the examples</summary>

```
bug fix:           /hstack-poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              /hstack-poteto-mode a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           /hstack-poteto-mode build a small feature behind a feature flag. verify it really works.
prototype:         /hstack-poteto-mode build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       /hstack-poteto-mode open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     /hstack-poteto-mode i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
babysit:           /hstack-poteto-mode check on pr 123. anything outstanding?
visual parity:     /hstack-poteto-mode the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     /hstack-poteto-mode i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               /hstack-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               /hstack-why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. /hstack-architect
                   this first.
arena:             /hstack-arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
swarm:             /hstack-swarm check every package under packages/ against its check.sh. one worker per
                   package. one report.
interrogate:       /hstack-interrogate review this pr.
tdd:               /hstack-tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           /hstack-reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
show-me-your-work: /hstack-show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       /hstack-automate-me
```

</details>

## the `hstack-poteto-agent` and hstack-comment-sicko subagents

pstack also ships a subagent that runs my style end to end. spawn it from a parent agent via [`subagent_type: "hstack-poteto-agent"`](agents/hstack-poteto-agent.md). it reads `hstack-poteto-mode` in full, including its inline principles index, before doing any work. substituting `generalPurpose` skips that read and drifts.

[`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) and [`subagent_type: "hstack-poteto-agent"`](agents/hstack-poteto-agent.md) route through the same wrapper.

pstack also ships [hstack-comment-sicko](agents/hstack-comment-sicko.md), a read-only comment reviewer available as `subagent_type: "hstack-comment-sicko"`. usually invoke it through [`/hstack-no-comments`](skills/hstack-no-comments/SKILL.md), not directly.

## principles

twenty-one short skills, one principle each. `hstack-poteto-mode` indexes them inline and reads that index at task start. the standalone files are there so other skills can reference a principle by name, and so the index can point at the full rule for each.

<details>
<summary>all twenty-one principles</summary>

| principle | group | rule |
|---|---|---|
| [laziness-protocol](skills/hstack-principle-laziness-protocol/SKILL.md) | core | Bias toward deletion and the smallest change that solves the problem. |
| [foundational-thinking](skills/hstack-principle-foundational-thinking/SKILL.md) | core | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [redesign-from-first-principles](skills/hstack-principle-redesign-from-first-principles/SKILL.md) | core | Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [subtract-before-you-add](skills/hstack-principle-subtract-before-you-add/SKILL.md) | core | Remove dead weight, redundant validators, and stub references first, then build on the simpler base. |
| [minimize-reader-load](skills/hstack-principle-minimize-reader-load/SKILL.md) | core | Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [outcome-oriented-execution](skills/hstack-principle-outcome-oriented-execution/SKILL.md) | core | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [experience-first](skills/hstack-principle-experience-first/SKILL.md) | core | Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [exhaust-the-design-space](skills/hstack-principle-exhaust-the-design-space/SKILL.md) | core | Build 2-3 competing prototypes and compare side by side before committing. |
| [build-the-lever](skills/hstack-principle-build-the-lever/SKILL.md) | core | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [model-the-domain](skills/hstack-principle-model-the-domain/SKILL.md) | architecture | Encode the domain in a structure instead of scattered conditionals. |
| [boundary-discipline](skills/hstack-principle-boundary-discipline/SKILL.md) | architecture | Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [type-system-discipline](skills/hstack-principle-type-system-discipline/SKILL.md) | architecture | Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, refuse to lie to the compiler, exhaust variants, derive from authoritative schemas. |
| [make-operations-idempotent](skills/hstack-principle-make-operations-idempotent/SKILL.md) | architecture | Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](skills/hstack-principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | architecture | Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [separate-before-serializing-shared-state](skills/hstack-principle-separate-before-serializing-shared-state/SKILL.md) | architecture | Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [prove-it-works](skills/hstack-principle-prove-it-works/SKILL.md) | verification | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'. |
| [fix-root-causes](skills/hstack-principle-fix-root-causes/SKILL.md) | verification | Trace each symptom to its root cause and fix it there; reproduce first, ask why until you reach it, resist nil-check guards that silence crashes. |
| [sequence-verifiable-units](skills/hstack-principle-sequence-verifiable-units/SKILL.md) | verification | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [guard-the-context-window](skills/hstack-principle-guard-the-context-window/SKILL.md) | delegation | Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [never-block-on-the-human](skills/hstack-principle-never-block-on-the-human/SKILL.md) | delegation | Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [encode-lessons-in-structure](skills/hstack-principle-encode-lessons-in-structure/SKILL.md) | meta | Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |

</details>

## not shipped here

a few things `hstack-poteto-mode` references but doesn't bundle:

- `/deslop` and the `deslop` skill ship in the `cursor-team-kit` plugin.
- `control-cli` (for CLIs and TUIs) and `control-ui` (for browser, Electron, web) ship in `cursor-team-kit` too.
- `/create-skill` is a cursor built-in. cursor also ships a built-in `/babysit`; inside `hstack-poteto-mode`, the [babysit playbook](skills/hstack-poteto-mode/playbooks/babysit.md) supersedes it for pr-status requests.

install `cursor-team-kit` alongside pstack if you want the full set.

## why are there no planning skills?

cursor already has a great plan mode which works great with pstack. but personally, i don't believe in planning. the best spec is code. if you do want to make a plan, [`/hstack-poteto-mode`](skills/hstack-poteto-mode/SKILL.md) covers it, but it's not a default. 

## make it yours

`hstack-poteto-mode` is my style. you may not want exactly that.

type [`/hstack-automate-me`](skills/hstack-automate-me/SKILL.md). it mines your recent transcripts, drafts a `<your-name>-mode` skill from how you've actually worked, and routes through pstack underneath. you keep pstack as the base and end up with your own routing skill alongside `hstack-poteto-mode`.

models are configurable too. type [`/hstack-setup-pstack`](skills/hstack-setup-pstack/SKILL.md). it detects the models you have access to and writes a small always-applied rule mapping each role (code, judgment, the review panels) to a model. every skill reads it and falls back to sensible defaults when the rule is absent, so you override only what you want.

## automations

pstack also ships a dormant [benny automation pack](automations/benny). benny triages slack issue reports, then reproduces and fixes confirmed bugs with real ui evidence. its files are not registered as slash skills.

to set it up, point cursor at [`FOR_AGENTS.md`](automations/benny/FOR_AGENTS.md). setup copies the pack into the target repository at `.cursor/automations/benny/`, enables pstack there for shared skills, and keeps user configuration outside the copied pack.

## license

MIT

## hstack: Cursor and Codex adaptation

This fork adds [hstack](hybrid/README.md), an opt-in distribution based on upstream pstack, with generated Cursor/Codex packages, a Codex review/rescue runner, and setup guides for local Cursor, Grok Bot and Cursor cloud VMs. Canonical upstream skills remain unchanged; runtime-specific instructions are added during packaging.

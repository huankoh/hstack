# Understand the code before changing it

Editing code you don't understand is how subtle regressions ship. pstack gives you four ways in. `/hstack-how` explains what the code does now. `/hstack-why` digs up the reasons it's shaped that way. `/hstack-teach` blends both into one explanation. `/hstack-recall` rebuilds your own recent context on a topic.

![A detective studies a machine blueprint with a magnifying glass while robots fetch case files; the evidence board behind her links clues under /hstack-how and /hstack-why.](images/understanding.jpg)

## Trace behavior with `/hstack-how`

```text
/hstack-how do we dedupe notifications? is there an n+1 when we look up subscribers?
```

Ask the question you actually have. [`/hstack-how`](../../skills/hstack-how/SKILL.md) reads the code and answers at the level of a senior engineer onboarding you onto the subsystem, with the runtime flow, the key types, and the non-obvious parts. For a big subsystem it fans out two to four read-only explorers first. For a narrow question it just reads and explains.

`/hstack-how` can also push back on the design. Ask for Critique mode when you suspect the structure itself:

```text
/hstack-how explain the sync service, then critique its ownership boundaries
```

The explanation comes first, so the critique stays grounded in how the thing really works.

## Dig up history with `/hstack-why`

```text
/hstack-why was the retry limit set to five? does the reason still hold?
```

[`/hstack-why`](../../skills/hstack-why/SKILL.md) works like a detective on a cold case. It starts from source control, then queries whatever evidence categories your MCPs expose, such as the issue tracker, long-form docs, team chat, observability, error tracking, and analytics, all in parallel. The report cites everything, separates direct evidence from inference, and says "appears to" when the record is thin. A null result gets reported too, because "nobody wrote down why" is itself an answer.

The two compose naturally. `do why first then how` is a perfectly good prompt when you suspect the history explains the mess.

## Actually understand it with `/hstack-teach`

```text
/hstack-teach me how this PR changes retries. convince me it fixes the cause and not the symptom.
```

[`/hstack-teach`](../../skills/hstack-teach/SKILL.md) is for when a summary isn't enough. It runs `/hstack-how` and `/hstack-why`, for a small change maybe just one of them, and weaves the findings into a plain explanation that builds up diagram by diagram. The "convince me" framing is worth stealing. It turns the explanation into an argument you can poke at instead of a tour.

## Rebuild your own context with `/hstack-recall`

```text
/hstack-recall catch me up on the export work from last week
```

[`/hstack-recall`](../../skills/hstack-recall/SKILL.md) mines your own recent chats plus the shared record (issues, prior fixes, errors still firing) and hands back a brief on where things stand and what's next. Use it when you're returning to a topic cold. If you want to resume one specific chat, that's the Session pickup playbook below, not `/hstack-recall`.

## Take over prior work with Session pickup

When another agent (or you, last week) left a branch mid-flight:

```text
/hstack-poteto-mode take over this branch. read the decision log, figure out what's done, and continue from there. don't redo finished work.
```

The [Session pickup playbook](../../skills/hstack-poteto-mode/playbooks/session-pickup.md) treats the prior trail as authoritative. It reconstructs the branch state and decisions, names the resume point, and verifies inherited claims against the original goal instead of re-deriving everything from scratch.

**Pitfall:** don't skip this page's skills because "the agent will read the code anyway." An agent that starts editing without a traced model tends to fix the symptom at the first plausible spot. `/hstack-how` first is cheaper than the second bug.

Next: [Design the change](04-design.md).

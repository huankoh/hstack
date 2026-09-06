# Build the change and clean the diff

The build playbooks share one discipline. Say what you observed, let the playbook demand the evidence. This page shows what to put in the prompt for each common build task, then the cleanup habit that keeps diffs reviewable.

## Prompt each build playbook with what you know

A bug prompt states the symptom and asks for a reproduction first:

```text
/hstack-poteto-mode this command emits two records after a retry. repro first, then fix and verify.
```

A feature prompt states the behavior and what must not change:

```text
/hstack-poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

A refactoring prompt pins behavior before structure moves:

```text
/hstack-poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

A perf prompt states the measurement, not a vibe:

```text
/hstack-poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, show me before and after.
```

Each of these routes to its playbook ([Bug fix](../../skills/hstack-poteto-mode/playbooks/bug-fix.md), [Feature](../../skills/hstack-poteto-mode/playbooks/feature.md), [Refactoring](../../skills/hstack-poteto-mode/playbooks/refactoring.md), [Perf issue](../../skills/hstack-poteto-mode/playbooks/perf-issue.md)), and the playbook supplies the steps you didn't type: reproduce before fixing, name the data shape before implementing, pin behavior before restructuring, profile before optimizing.

For sustained improvement of one number, there's the [Hillclimb playbook](../../skills/hstack-poteto-mode/playbooks/hillclimb.md). Give it the metric, a target, and a floor on attempts, and it loops one hypothesis at a time with a frozen measurement harness. It keeps wins and reverts everything else.

## Write the failing test first with `/hstack-tdd`

When a bug has a cheap local test path, the whole prompt can be two words:

```text
/hstack-tdd implement
```

In context, that's enough. [`/hstack-tdd`](../../skills/hstack-tdd/SKILL.md) writes the smallest test that fails for the intended reason, then the fix, then reruns the test. If a test would need broad harness setup or brittle mocks, the skill says so and uses the closest executable check instead. Don't force a test where a real command is stronger evidence.

## Let the TypeScript rules load themselves

[`hstack-typescript-best-practices`](../../skills/hstack-typescript-best-practices/SKILL.md) has no slash command in your workflow. It loads whenever the agent touches a `.ts` or `.tsx` file and turns the type-system principles into concrete rules: discriminated unions, `unknown` at boundaries, exhaustive variants, schema-derived types.

## Clean before you commit

The [Opening a PR playbook](../../skills/hstack-poteto-mode/playbooks/opening-a-pr.md) runs `/deslop` on the diff before each commit and applies [`/hstack-unslop`](../../skills/hstack-unslop/SKILL.md) to the PR description and commit bodies. `/deslop` ships in the `cursor-team-kit` plugin, not in pstack. If you don't have it, ask for the same outcome in plain words: remove narrating comments, unsupported guards, dead compatibility paths, and unrelated edits.

For prose, `/hstack-unslop` takes a target and any extra rules you have:

```text
/hstack-unslop the readme changes, no emdashes
```

You'll develop your own shorthand. The skill reads intent fine from terse prompts like `unslop that, tighten it`.

## Strip the comments with `/hstack-no-comments`

Comments need their own pass, and not from the agent that wrote them. An author defends its comments the way you'd defend yours. So before review, hand them to fresh eyes:

```text
/hstack-no-comments the diff
```

[`/hstack-no-comments`](../../skills/hstack-no-comments/SKILL.md) spawns [hstack-comment-sicko](../../agents/hstack-comment-sicko.md), a read-only reviewer with a short keep list: license headers, doc comments on a public API, links that explain what code can't, behavior forced by an external dependency you can't reshape. Everything else goes. A surprise in your own code gets no such pass. The comment comes back as a refactor flag, and `/hstack-no-comments` fixes the flags it accepts at the root cause. When a comment claims a constraint, "do not remove", the skill offers to encode the claim as a type, test, or lint. Either way, the comment comes out.

The division of labor is worth keeping straight. `/deslop` cleans slop out of the code, `/hstack-unslop` cleans it out of prose, and `/hstack-no-comments` hands the comments to a reviewer who didn't write them.

**Pitfall:** cleanup is not optional polish. A diff with narrating comments and defensive dead weight reads as unfinished to reviewers, and the extra code is where the next bug hides. If the diff feels padded, say `deslop it` before you commit, not after review calls it out.

Next: [Verify and ship](06-verify-and-ship.md).

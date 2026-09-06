#!/usr/bin/env python3
"""Build a reviewable hstack distribution in a new directory; never install or push."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

SOURCE_URL = 'https://github.com/huankoh/plugins'
DISTRIBUTION_URL = 'https://github.com/huankoh/hstack'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def verify_generated(package, runtime, source):
    """Reject incomplete or ambiguous generated packages before distribution metadata changes."""
    expected = {'hstack-' + path.parent.name
                for path in (source / 'pstack/skills').glob('*/SKILL.md')}
    actual = {path.parent.name for path in (package / 'skills').glob('*/SKILL.md')}
    if not expected or actual != expected:
        raise ValueError(f'{runtime} package does not preserve the namespaced source skills')
    expected_agents = {'hstack-' + path.stem for path in (source / 'pstack/agents').glob('*.md')}
    if {path.stem for path in (package / 'agents').glob('*.md')} != expected_agents:
        raise ValueError(f'{runtime} package does not preserve the namespaced source agents')
    mapping = json.loads((package / 'SKILL-MAP.json').read_text())
    for category, expected_names in (('skills', expected), ('agents', expected_agents)):
        entries = mapping.get(category, {})
        if {'hstack-' + name for name in entries} != expected_names:
            raise ValueError(f'{runtime} package has an incomplete {category} map')
        for name, relative in entries.items():
            expected_path = (f'skills/hstack-{name}/SKILL.md' if category == 'skills'
                             else f'agents/hstack-{name}.md')
            if relative != expected_path or not (package / relative).is_file():
                raise ValueError(f'{runtime} package has an invalid mapped path: {relative}')
    if runtime == 'codex':
        manifest = json.loads((package / '.codex-plugin/plugin.json').read_text())
        prompts = manifest.get('interface', {}).get('defaultPrompt')
        if not isinstance(prompts, list) or not prompts or not all(isinstance(p, str) for p in prompts):
            raise ValueError('Codex defaultPrompt must retain its source array shape')
        if not any('$hstack-poteto-mode' in prompt for prompt in prompts):
            raise ValueError('Codex defaultPrompt must select the namespaced hstack entrypoint')


def prepare(source, output):
    source, output = source.resolve(), output.resolve()
    if output.exists():
        raise ValueError('Output must be a new directory')
    if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip():
        raise ValueError('Source checkout must be clean')
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    with tempfile.TemporaryDirectory(prefix='hstack-distribution-') as temporary:
        generated = Path(temporary) / 'generated'
        subprocess.run([sys.executable, str(source / 'pstack/hybrid/build.py'), '--output', str(generated)], check=True)
        destinations = {'cursor': 'cursor/plugins/hstack', 'codex': 'plugins/hstack'}
        for runtime in destinations:
            verify_generated(generated / runtime / 'plugins/hstack', runtime, source)
        output.mkdir(parents=True)
        for runtime, relative in destinations.items():
            target = output / relative
            shutil.copytree(generated / runtime / 'plugins/hstack', target)
            manifest_path = target / ('.cursor-plugin/plugin.json' if runtime == 'cursor' else '.codex-plugin/plugin.json')
            manifest = json.loads(manifest_path.read_text())
            manifest['repository'] = DISTRIBUTION_URL
            manifest['homepage'] = DISTRIBUTION_URL
            write_json(manifest_path, manifest)
        cursor = json.loads((generated / 'cursor/.cursor-plugin/marketplace.json').read_text())
        cursor['plugins'][0]['source'] = './cursor/plugins/hstack'
        write_json(output / '.cursor-plugin/marketplace.json', cursor)
        codex = json.loads((generated / 'codex/.agents/plugins/marketplace.json').read_text())
        codex['interface'] = {'displayName': 'hstack'}
        write_json(output / '.agents/plugins/marketplace.json', codex)

    # Private run identifiers are replaced consistently across both packages.
    # Commit SHAs and source fingerprints remain unchanged for provenance.
    replacements = {}
    counters = {}
    patterns = [
        ('cursor-task', r'https://cursor\.com/agents/[^\s)"`]+'),
        ('codex-task', r'https://chatgpt\.com/codex/cloud/tasks/[^\s)"`]+'),
        ('codex-environment', r'https://chatgpt\.com/codex/cloud/settings/environment/[^\s)"`]+'),
        ('ci-run', r'https://github\.com/huankoh/plugins/actions/runs/\d+'),
        ('build', r'\bbld-\d{8}-[0-9a-f-]{36}\b'),
        ('environment', r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'),
        ('worker', r'\b[0-9a-f]{32}\b'),
        ('handoff', r'\bhstack-(?:activation-review|unattended-auth)-20260906\b'),
    ]
    sanitized = []
    for relative in destinations.values():
        hybrid = output / relative / 'hybrid'
        for path in sorted(list((hybrid / 'docs').glob('*.md')) + list((hybrid / 'examples').glob('*.json'))):
            original = text = path.read_text()
            for kind, pattern in patterns:
                def replace(match):
                    key = match.group(0)
                    if key not in replacements:
                        counters[kind] = counters.get(kind, 0) + 1
                        label = f'private-{kind}-{counters[kind]:02d}'
                        replacements[key] = 'https://example.invalid/' + label if key.startswith('https://') else label
                    return replacements[key]
                text = re.sub(pattern, replace, text)
            if text != original:
                path.write_text(text)
                sanitized.append(str(path.relative_to(output)))

    identity = json.loads((output / 'plugins/hstack/BUILD.json').read_text())
    shutil.copy2(source / 'pstack/LICENSE', output / 'LICENSE')
    (output / '.gitignore').write_text('.DS_Store\n__pycache__/\n*.py[cod]\n.venv/\n.env\n.env.*\n*.local.json\n')
    (output / 'README.md').write_text(f'''# hstack

hstack brings Lauren Tan's pstack engineering workflows to Cursor and Codex. It includes 45 distinctly named skills, two named agents, and 18 configurable model roles. For implementation in Cursor, hstack defaults to Cursor building and Codex reviewing, with one bounded Codex rescue for a confirmed code blocker. Existing model choices are preserved.

This repository publishes the generated packages. The [maintained source]({SOURCE_URL}/tree/feat/pstack-codex-support/pstack/hybrid) and [adaptation PR]({SOURCE_URL}/pull/1) show the changes from [upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). hstack is maintained by huankoh and is not an official Cursor or OpenAI release.

## Install

The namespaced release remains on `feat/namespaced-hstack-skills` for review; `main` still contains the earlier package. The live discovery checks used distribution commit `66b1ac1ac6ae2c190a9ff20a9f1db28f367c4977` and runtime source `bbe9d3e5d3f3531227e4c5d88da99a6394540bb1`.

**Cursor plugin:** Register the tested remote marketplace with Cursor Agent CLI:

```bash
agent plugin marketplace add {DISTRIBUTION_URL}.git --git-ref 66b1ac1ac6ae2c190a9ff20a9f1db28f367c4977
```

Then open native Cursor's **Customize → Add**, choose **hstack**, and install it. Registration alone does not install the plugin. If an older marketplace named hstack is registered, follow the [replacement procedure](cursor/plugins/hstack/hybrid/docs/cursor-local.md#install-the-pinned-remote-marketplace); preserve the original pstack marketplace.

**Codex CLI or desktop:** Clone this repository, then register its marketplace from the clone root:

```bash
git clone --branch feat/namespaced-hstack-skills {DISTRIBUTION_URL}.git
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

- Source revision: `{revision}`.
- Source fingerprint: `{identity['source_sha256']}`.
- Each package retains its original `BUILD.json`; [DISTRIBUTION.json](DISTRIBUTION.json) records packaging changes separately.
- [UPDATE.md](UPDATE.md) explains how to build and review an update.
- [SANITIZATIONS.md](SANITIZATIONS.md) lists documentation files whose private execution references were replaced. Example-domain links are placeholders, not public evidence links.

The distribution preserves the generated source's namespaced skills, two agents, `SKILL-MAP.json`, runtime scripts, runner behavior, model defaults, and Codex default-prompt array. Distribution manifests identify this repository; private task, environment, build, worker, and CI-run references in copied documentation are sanitized. Source adapters and wrappers already differ from upstream pstack; packaging does not remove those changes.

## License

[MIT](LICENSE), retaining Lauren Tan's pstack copyright and attribution. Runtime-specific hstack additions are maintained by huankoh. The original pstack README and license remain inside each package.
''')
    (output / 'UPDATE.md').write_text('''# Update the distribution

Make engineering changes in the maintained `huankoh/plugins` fork and review them through its PR. Keep that full fork connected to `cursor/plugins` for upstream merges. This repository holds generated distribution packages, so do not edit runtime scripts or skill bodies here.

1. Select a reviewed, tested source commit. Check out that exact commit in a clean local clone of `https://github.com/huankoh/plugins.git`.
2. Use Python 3.9+ with the source's `pstack/hybrid/requirements.txt` installed. Run the source's package tests and required CI checks before staging a release.
3. Run `python tools/prepare-distribution.py /absolute/path/to/source /absolute/path/to/new-staging-directory` from this distribution checkout. The destination must not exist. This command builds packages, checks the namespaced skill and agent sets and their map, preserves source identity and default prompts, adjusts marketplace metadata, and sanitizes private documentation references. It does not install, authenticate, commit, or push.
4. Review the staged root README and evidence for new private references or changed host limitations. The automatic sanitizer covers known identifier formats; review new formats before publication. Review `SANITIZATIONS.md` and `DISTRIBUTION.json`, verify every package checksum, and validate both marketplace paths and plugin manifests. Each package must contain the source's 45 `hstack-` skills, two `hstack-` agents, and a complete `SKILL-MAP.json`. Codex's `defaultPrompt` must retain the source array and select `$hstack-poteto-mode`; do not replace it with the old unprefixed command.
5. Compare the staged tree with this repository. Replace the two generated package directories with the reviewed versions on a dedicated update branch, preserving this repository's Git history, then copy marketplace manifests and release documentation. Do not overlay the new files onto old packages: obsolete unprefixed skill and agent directories must disappear from hstack, while the original pstack installation remains untouched. Open a PR and publish only after checks pass.
6. Refresh the marketplace in each intended client and open a new task to verify the loaded `BUILD.json`, unique entrypoint, and original pstack coexistence. For portable Cursor skills, rerun the exporter from the new package and verify that it exposes exactly 45 public `SKILL.md` wrappers and resolves the mapped internal `WORKFLOW.md` files. Configure cloud environments separately using their documented pinned-source procedure. Publishing this repository does not update installed plugins or existing VM builds automatically. Earlier evidence using unprefixed names does not verify a renamed installation.

The source's `pstack/hybrid/update-upstream.sh` belongs in the full source fork. Do not run it in this distribution repository. Existing source clone URLs and tested source commit SHAs inside the generated guides remain intentional.
''')
    (output / 'SANITIZATIONS.md').write_text('# Sanitized files\n\n' + '\n'.join('- `' + p + '`' for p in sanitized) + '\n')
    (output / 'tools').mkdir()
    shutil.copy2(Path(__file__), output / 'tools/prepare-distribution.py')
    files = {}
    for relative in destinations.values():
        for path in sorted((output / relative).rglob('*')):
            if path.is_file():
                files[str(path.relative_to(output))] = hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(output / 'DISTRIBUTION.json', {
        'name': 'hstack', 'repository': DISTRIBUTION_URL,
        'source_repository': SOURCE_URL, 'source_pull_request': SOURCE_URL + '/pull/1',
        'source_revision': revision, 'source_sha256': identity['source_sha256'],
        'upstream_version': identity['upstream_version'],
        'packages': destinations,
        'packaging_changes': ['Root marketplaces address their separate runtime packages.',
                              'Plugin repository and homepage identify the distribution.',
                              'Private execution references are replaced in copied documentation and examples.'],
        'sanitized_paths': sanitized,
        'package_sha256': files,
    })
    print(json.dumps({'output': str(output), 'package_files': len(files), 'sanitized_files': len(sanitized),
                      'bytes': sum(p.stat().st_size for p in output.rglob('*') if p.is_file())}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    prepare(args.source, args.output)

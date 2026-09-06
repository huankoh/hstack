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
        output.mkdir(parents=True)
        destinations = {'cursor': 'cursor/plugins/hstack', 'codex': 'plugins/hstack'}
        for runtime, relative in destinations.items():
            target = output / relative
            shutil.copytree(generated / runtime / 'plugins/hstack', target)
            manifest_path = target / ('.cursor-plugin/plugin.json' if runtime == 'cursor' else '.codex-plugin/plugin.json')
            manifest = json.loads(manifest_path.read_text())
            manifest['repository'] = DISTRIBUTION_URL
            manifest['homepage'] = DISTRIBUTION_URL
            if runtime == 'codex':
                manifest['interface']['defaultPrompt'] = ['Use $poteto-mode for this engineering task.']
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

hstack brings Lauren Tan's pstack engineering workflows to Cursor and Codex. It includes 45 skills, 18 configurable model roles, and an optional workflow where Cursor builds, Codex reviews, and Codex may attempt one bounded rescue for a confirmed code blocker. Existing model choices are preserved.

This repository publishes the generated packages. The [maintained source]({SOURCE_URL}/tree/feat/pstack-codex-support/pstack/hybrid) and [adaptation PR]({SOURCE_URL}/pull/1) show the changes from [upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). hstack is maintained by huankoh and is not an official Cursor or OpenAI release.

## Install

**Cursor local:** Open Customize → Add Marketplace → Import from GitHub, enter `{DISTRIBUTION_URL}`, then choose **hstack**. This repository puts the hstack marketplace on its default branch. Import of this new repository still needs a live UI check; you can also clone the repository and select its folder through Import from Disk.

**Codex CLI or desktop:** Clone this repository, then register its marketplace from the clone root:

```bash
git clone {DISTRIBUTION_URL}.git
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

- Source revision: `{revision}`.
- Source fingerprint: `{identity['source_sha256']}`.
- Each package retains its original `BUILD.json`; [DISTRIBUTION.json](DISTRIBUTION.json) records packaging changes separately.
- [UPDATE.md](UPDATE.md) explains how to build and review an update.
- [SANITIZATIONS.md](SANITIZATIONS.md) lists documentation files whose private execution references were replaced. Example-domain links are placeholders, not public evidence links.

Runtime scripts, runner behavior, model defaults, and upstream skill bodies are unchanged from the generated source packages. Distribution manifests identify this repository; private task, environment, Build, worker and CI-run references in the copied documentation are sanitized.

## License

[MIT](LICENSE), retaining Lauren Tan's pstack copyright and attribution. Runtime-specific hstack additions are maintained by huankoh. The original pstack README and license remain inside each package.
''')
    (output / 'UPDATE.md').write_text('''# Update the distribution

Make engineering changes in the maintained `huankoh/plugins` fork and review them through its PR. Keep that full fork connected to `cursor/plugins` for upstream merges. This repository holds generated distribution packages, so do not edit runtime scripts or skill bodies here.

1. Select a reviewed, tested source commit. Check out that exact commit in a clean local clone of `https://github.com/huankoh/plugins.git`.
2. Use Python 3.9+ with the source's `pstack/hybrid/requirements.txt` installed. Run the source's package tests and required CI checks before staging a release.
3. Run `python tools/prepare-distribution.py /absolute/path/to/source /absolute/path/to/new-staging-directory` from this distribution checkout. The destination must not exist. This command builds packages, preserves source identity, adjusts marketplace metadata, and sanitizes private documentation references. It does not install, authenticate, commit, or push.
4. Review the staged root README and evidence for new private references or changed host limitations. The automatic sanitizer covers known identifier formats; review new formats before publication. Review `SANITIZATIONS.md` and `DISTRIBUTION.json`, and validate both marketplace paths and plugin manifests.
5. Compare the staged tree with this repository. Copy the reviewed generated packages, marketplace manifests and release documentation into a dedicated update branch, preserving this repository's Git history. Open a PR and publish only after checks pass.
6. Refresh the marketplace in each intended client and open a new task to verify the loaded `BUILD.json`. Configure cloud environments separately using their documented pinned-source procedure. Publishing this repository does not update installed plugins or existing VM builds automatically.

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
                              'Codex defaultPrompt uses the documented array shape.',
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

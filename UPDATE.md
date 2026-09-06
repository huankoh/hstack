# Update the distribution

Make engineering changes in the maintained `huankoh/plugins` fork and review them through its PR. Keep that full fork connected to `cursor/plugins` for upstream merges. This repository holds generated distribution packages, so do not edit runtime scripts or skill bodies here.

1. Select a reviewed, tested source commit. Check out that exact commit in a clean local clone of `https://github.com/huankoh/plugins.git`.
2. Use Python 3.9+ with the source's `pstack/hybrid/requirements.txt` installed. Run the source's package tests and required CI checks before staging a release.
3. Run `python tools/prepare-distribution.py /absolute/path/to/source /absolute/path/to/new-staging-directory` from this distribution checkout. The destination must not exist. This command builds packages, preserves source identity, adjusts marketplace metadata, and sanitizes private documentation references. It does not install, authenticate, commit, or push.
4. Review the staged root README and evidence for new private references or changed host limitations. The automatic sanitizer covers known identifier formats; review new formats before publication. Review `SANITIZATIONS.md` and `DISTRIBUTION.json`, and validate both marketplace paths and plugin manifests.
5. Compare the staged tree with this repository. Copy the reviewed generated packages, marketplace manifests and release documentation into a dedicated update branch, preserving this repository's Git history. Open a PR and publish only after checks pass.
6. Refresh the marketplace in each intended client and open a new task to verify the loaded `BUILD.json`. Configure cloud environments separately using their documented pinned-source procedure. Publishing this repository does not update installed plugins or existing VM builds automatically.

The source's `pstack/hybrid/update-upstream.sh` belongs in the full source fork. Do not run it in this distribution repository. Existing source clone URLs and tested source commit SHAs inside the generated guides remain intentional.

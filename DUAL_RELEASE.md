# Two-edition maintenance and combined Releases

This repository maintains two separate UI implementations:

| Edition | Source branch | UI stack | Existing data |
|---|---|---|---|
| Tk | `main` | CustomTkinter | Original project directory, `tasks.json` |
| Flet | `flet-version` | Flet 1.1.x / Flutter | Per-user data directory; one-time legacy JSON import |

Both editions are maintained independently. **Do not merge the Flet branch
into main merely to publish a release.** The release workflow checks out
each branch's latest commit directly and records both SHA values in the notes.

## Combined release

Open [Actions → Build and Release (Tk + Flet)](https://github.com/SDCOM-0415/To-do.app/actions/workflows/build-release.yml)
on the **main** branch and select **Run workflow**.

1. Enter the **base version**, e.g. `v0.4.0` (do not include a date or sequence). When **Prerelease** is checked, CI automatically creates a tag like `v0.4.0-2026-11-09-1`, then `v0.4.0-2026-11-09-2` for the next prerelease on that date. The date follows China Standard Time (UTC+08:00). Sequences reset to `1` for a new date or base version. When **Prerelease** is unchecked, the tag is exactly `v0.4.0`. Existing tags are never overwritten.
2. Leave **Publish** unchecked to test the full eight-build matrix. This
   uploads CI artifacts but does **not** create a Release or reserve a version number. Only already-created Git tags determine the next prerelease sequence.
3. When the matrix is known to work, run it again with **Publish** checked.
   Choose **Prerelease** to generate the dated incrementing tag automatically, or uncheck it for a stable release.

Each run freezes the current commit SHA of both branches before building.
The eight CI jobs cover Windows x64, Linux x64, macOS Intel x86_64 and
macOS Apple Silicon arm64 for **both** editions.

The release is created **only after all eight packages have succeeded**.
If any platform fails, no partial Release is created.

## Asset naming

A stable release tagged `v0.4.0` contains:

- `Todo-App-v0.4.0-Tk-Windows-x64.zip`
- `Todo-App-v0.4.0-Tk-Linux-x64.tar.gz`
- `Todo-App-v0.4.0-Tk-macOS-x64.zip`
- `Todo-App-v0.4.0-Tk-macOS-arm64.zip`
- `Todo-App-v0.4.0-Flet-Windows-x64.zip`
- `Todo-App-v0.4.0-Flet-Linux-x64.tar.gz`
- `Todo-App-v0.4.0-Flet-macOS-x64.zip`
- `Todo-App-v0.4.0-Flet-macOS-arm64.zip`
- `SHA256SUMS.txt`

The macOS archives contain .app bundles; their app may need signing and
notarization for a smooth user experience. Both editions have different
packaging dependencies and sizes.

## Version semantics and safety

The tag is a **distribution version**, not a guarantee that the two
application UIs display the same internal version. Update their UI versions
separately as appropriate.

Flet stores its data under the user's data directory and can import an old
`tasks.json` on first run. Back up existing tasks before switching editions.
There is no automatic bidirectional synchronization.

The previous single-edition workflow was replaced by the combined-release
workflow. The separate Flet preview workflow remains available on the Flet
branch. No Release is published by pushes to either development branch.

> CI packaging success is not a guarantee that all UI paths work. Test each
> resulting package on its target operating system before a stable release.

For prereleases, the full generated tag is included in **all eight artifact names** and in the Release title. For example: `Todo-App-v0.4.0-2026-11-09-1-Flet-Windows-x64.zip`. The first prerelease of each base version each day ends with `-1`. Builds that do not publish do not consume an index.

The Flet edition is maintained on `flet-version`. The old `feature/flet-port` branch is removed automatically after the renamed branch receives its first push.

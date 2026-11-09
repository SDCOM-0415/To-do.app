# TodoApp Flet 0.3.2

This is the separately packaged **Flet edition** of TodoApp.
The original **TodoApp (CustomTkinter)** is maintained on `main`.

## Three live appearance themes

Open **应用设置 → 外观 → 界面风格** to select:
- **Graphite Focus:** graphite dark + muted violet
- **Paper & Ink:** warm light + subdued green
- **Blue Hour:** midnight blue + cool cyan

Choose **应用** or **确定** to persist the theme. The selected
appearance applies to the window, sidebar, selected navigation and task
workspace, and remains selected after restart.

Old Flet preferences `dark` / `light` / `system` migrate to
`graphite` / `paper` / `graphite`, respectively. Theme preferences
are independent of the original Tk edition.

## Run

Python 3.12:

```bash
python -m pip install -r flet_port/requirements.txt
python flet_port/main.py
```

## Application names and storage

- Tk: **TodoApp** (original executable and macOS bundle name).
- Flet: **TodoApp Flet** (separate executable/macOS bundle identifier).
- Shared tasks: `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`.
- Tk preferences: `tk-config.json`.
- Flet preferences: `flet-settings.json`.

Both editions can be installed independently; they do not have to
overwrite each other's applications. They read the same tasks JSON,
so do not edit the same task concurrently in both apps.

Flet can migrate an old tasks.json once if the shared destination does not exist.
Legacy originals are not modified. Back up important data before upgrading.

## CI and publishing

The [Flet Build workflow](https://github.com/SDCOM-0415/To-do.app/actions/workflows/flet-preview.yml)
builds independent Windows x64, Linux x64, macOS Intel and macOS ARM64 artifacts,
without creating Releases.

The [combined release workflow](https://github.com/SDCOM-0415/To-do.app/actions/workflows/build-release.yml)
on `main` builds both editions from their independent branches and
publishes eight named artifacts only if every job passes.

# Todo App — Flet migration preview

This is an **experimental Flet 1.1** desktop UI for Todo App v0.3.1.
The original CustomTkinter application remains untouched on the main branch.
No release is implied by the existence of this branch.

## Features
- Create, edit, complete, delete tasks (including notes, priority, due date and tags).
- Search, show/hide completed tasks, sort and view completion/overdue statistics.
- System / light / dark themes.
- JSON-compatible persistence and one-time legacy task migration.
- Manual JSON export and import through native desktop file dialogs.

## Run

From the repository root, on Python 3.12+:

```bash
python -m pip install -r flet_port/requirements.txt
python flet_port/main.py
```

Flet desktop requires supported OS and dependencies; see https://flet.dev/docs/getting-started/installation/ .

## Storage and migration

The UI preserves the structure of the existing `models.Task` JSON data.
Files are written to the OS-specific user-data directory obtained from `platformdirs`:
`TodoApp/SDCOM/tasks.json` and `flet-settings.json`.

The first run copies `tasks.json` from the old repository/application directory **only when no new task file exists**. The original file is never modified by the migration. Make your own backup before testing with important data. JSON import replaces in-memory tasks only after validation and explicit confirmation.

If the old packaged app stored its data elsewhere, use the new app's Import JSON feature. The old CustomTkinter version still uses its old storage path.

## Packaging

The experimental `flet-preview.yml` workflow runs a smoke test, then can build separate Windows x64, Linux x64 and macOS Intel artifacts from their native GitHub runners. This is **native CI matrix building, not cross-compilation**.

Flet CLI packaging uses Flutter; it is not the same as PyInstaller. For local builds, see https://flet.dev/docs/publish/ . The preview workflow does not publish a Release or modify production tags.

## Notes

- This preview is a desktop-first application; web deployment requires separate file-storage and multi-user design.
- Real GUI launch and packaged artifacts need validation on the target OS before a release.
- Flet 1.x is API-incompatible with older Flet 0.2x examples; the implementation uses the 1.1 API.

# Governance

Operating rules for any agent working in this repository. Read this file before changing the project. Then read `PROJECT_CONTEXT.md`, `AI_REQUIREMENTS.md`, `WORK_ITEMS.md`, and `HANDOFF.md`.

## Evidence rules

Label every claim with one of these sources:

| Label | Meaning |
| --- | --- |
| Verified | Confirmed from a file in this repository. |
| Stated | Given by the project owner or by the course rubric `FE-OV 1.docx`. Not confirmed inside a Blueprint graph. |
| Decision | A tuning or structure choice the owner left to the agent on 2026-10-11. Use it. Do not replace it with another number. |
| Unknown | Not in the repository, the brief, the rubric, or the locked decisions. |

Do not turn an asset file name into a behavior claim. `.uasset` files are binary. A task named `BTTask_Attack` only proves that the asset exists.

A Blueprint or Behavior Tree behavior is Verified only after the open editor exports that asset to text (T3D) through the Python remote connection, or after Play In Editor shows it. A screenshot reading is not Verified. Python can add Blackboard keys and export assets. It cannot link graph pins or set most Behavior Tree node properties. When a pin must change, give the owner one click sequence that names the nodes already in the exported graph. Disconnect a wire with Alt+left click. Selector child order follows the Sequence box X position, left to right. Dragging a task inside the canvas does not reorder the Selector.

Locked numbers live in `AI_REQUIREMENTS.md`. Do not add distances, timers, spawn counts, or debug text beyond those decisions. If a new value is Unknown, stop and record it in `HANDOFF.md`.

## Behavior trees are mandatory

The professor requires decision trees. In this project that means an Unreal **Behavior Tree** plus a **Blackboard** for every AI character.

- The tree decides what the character does next, using Selectors, Sequences, Decorators, Services, and Tasks.
- One task does one action. A service only writes Blackboard keys.
- Overlap events and damage events may write Blackboard keys. They must not contain the chase, orbit, defend, flee, or follow decision.
- A stack of Branch nodes on Tick does not pass, even if the result looks right.
- Each different behavior gets its own tree. Reusing one tree on two meshes does not count as two AIs.

## Scope fence

- The assigned area is enemy AI and hostage escort AI. See `AI_REQUIREMENTS.md`.
- The course rubric also requires two enemies with different advanced AI. The hostage is not one of those two enemies. The second enemy is the charger in `AI_REQUIREMENTS.md`.
- Finish the work items already listed before adding extra systems.
- The stated game loop includes a second weapon, character progression, and a timed survival section. Those are context. They are not implementation tasks unless a work item says so.
- Do not add a C++ module. No `Source/` tree was present on 2026-10-11. This project is Blueprint-only.
- Do not edit marketplace or sample packs as if they were game systems. Those packs are listed in `PROJECT_CONTEXT.md`.
- Do not retarget the default map or game mode unless a work item requires it.

## Change rules

- Prefer the existing enemy assets under `Content/ThirdPerson/Blueprints/EnemigoIA/`.
- Keep new gameplay assets under `Content/ThirdPerson/` unless an existing folder already owns that feature.
- Debug output required by the brief must use Unreal **Print String** nodes. Do not replace that requirement with another logger.
- After a behavior change, update the matching work item and add a dated entry to `HANDOFF.md`.
- When a slice becomes playable, set its Editor test row in `WORK_ITEMS.md` to Ready. When the owner reports Play In Editor, write that result in the log. Do not set Passed from an export.
- Do not commit, push, or rewrite git history unless the project owner asks.

## Agent workflow (the loop every step follows)

The agent cannot click in the editor. It can only read assets (export), run Play In Editor, and read logs. One step looks like this:

1. The agent gives the owner one short click sequence from `HANDOFF.md` → "Pending work". It names the asset, the node, and the pin.
2. The owner edits, presses **Compilar** and then **Guardar**, and says "done".
3. The agent runs `ping.py` and checks that the DIRTY line reads `(none)`. If not, it asks the owner to save.
4. The agent runs `export_ai.py`, then `summarize.py <Asset>` (Blueprints) or `bt_structure.py BT_EnemyIA` (trees). It confirms the change is in the export.
5. Optionally, it runs an agent PIE (`pie_start.py`, wait, `pie_sample.py`, `pie_stop.py`) and reads `Saved/Logs/Terreno.log` for `Enemigo:` lines and `Accessed None`.
6. It updates `WORK_ITEMS.md` and `HANDOFF.md`, then gives the next step.

Never give the owner more than one asset's changes at a time without re-exporting in between.

## Agent tooling

Scripts live in `Tools/UnrealPython/` (tracked). `Intermediate/` is git-ignored, so outputs go to `Intermediate/inspect/live/`.

Requirements:
- The editor is open with `Terreno.uproject` loaded.
- Remote execution is on: `Config/DefaultEngine.ini` → `[/Script/PythonScriptPlugin.PythonScriptPluginSettings] bRemoteExecution=True`. It is already set.
- The runner imports `remote_execution` from `C:\Program Files\Epic Games\UE_5.6\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python`. Override that path with the `UE_REMOTE_PYTHON` environment variable.

| Script | Where it runs | What it does |
| --- | --- | --- |
| `run.py <script>` | local | Sends an editor-side script to the editor and prints its log lines. Every editor-side script below is run through it. |
| `ping.py` | editor | Prints the editor/game world and unsaved (dirty) packages. |
| `export_ai.py` | editor | Exports all AI assets to T3D. Add new asset paths, one per line, in `Intermediate/inspect/extra_paths.txt`. |
| `summarize.py <Name...>` | local | Turns `<Name>.t3d` into `_<Name>.txt`: each node, its pins, defaults, and wires. `-> <none>` on an exec output means nothing is connected. |
| `bt_structure.py <BT>` | local | Prints Selector/Sequence children in execution order, with decorators and their settings. |
| `pie_start.py` / `pie_stop.py` | editor | Starts and stops Play In Editor. |
| `pie_sample.py` | editor | During PIE, logs each enemy's location, speed, path status, BT running, executing Blueprint task, and Blackboard values. Create the empty file `Intermediate/inspect/teleport.flag` first to teleport the player 450 units from enemy 0. |
| `pie_force_move.py` | editor | During PIE, orders enemy 0 to walk 600 units without the tree. If it walks, the navmesh and pawn are fine and the bug is in the tree. |

Example (PowerShell, repo root):

```
python Tools\UnrealPython\run.py Tools\UnrealPython\export_ai.py
python Tools\UnrealPython\summarize.py BTTask_Roam
```

Shell notes:
- In Cursor the sandbox blocks the editor connection, so shell calls need full permissions.
- Do not use `python -c "..."` in PowerShell, because quotes and brackets break. Write a `.py` file and run it.
- PIE started by the agent while the editor window is not focused ticks at about 3 FPS. Wait 10 seconds or more after `pie_start.py`.

Python API facts for UE 5.6:
- `AIBlueprintHelperLibrary` is not usable from Python. Get the blackboard with `controller.get_component_by_class(unreal.BlackboardComponent)`.
- Use `set_actor_location`, not `k2_set_actor_location`.
- Use `project_point_to_navigation`, not the `k2_` name.
- `ReceiveMoveCompleted.add_callable` never fired, and `vislog record` wrote nothing. Do not rely on either.
- Python cannot wire Blueprint pins or set most Behavior Tree node properties. The owner does those edits.

**Never run these. They crashed or asserted the editor on 2026-10-13:**
- `unreal.ObjectIterator` over all objects.
- Reading properties of the `NavigationSystemV1` class default object.

## Unreal pitfalls already hit in this project

1. **Force Success under a Selector.** Force Success also converts a failing sibling decorator into success, so the Selector stops there and lower branches never run. This was the "enemies do not walk" bug on 2026-10-14. Never put Force Success on a direct child of a Selector. If a task must not fail a Sequence, put the Force Success inside that Sequence instead.
2. **Blueprint BT task without Finish Execute.** A task that does not call Finish Execute on **every** exec path (including Is Not Valid, On Fail, and Branch False) runs forever, and the enemy freezes. Check every exec end in the summary for `-> <none>` before saying a task is done.
3. **Copy-pasted nodes share pin IDs** in T3D. Resolve wires by node name plus pin ID. `summarize.py` already does this. The player's light and heavy chains are copies, so never trust a pin-only match there.
4. **Selector order** is the X position of the child boxes, left to right. It is not creation order. Check it with `bt_structure.py`.
5. **Bool Blackboard decorator:** Is Set means true. The key query only offers Is Set and Is Not Set for bool keys.
6. **Key selectors on a Blueprint service or task** appear on the tree node only when the variable is Editable en instancia (Instance Editable).
7. **Cooldown decorator** starts counting when the branch deactivates, not when it starts.
8. **Agent height is not the problem.** `SupportedAgents` is empty, so every pawn uses `RecastNavMesh-Default`.
9. **Accented text** (`á`, `ñ`) shows as `��` in the export summary because of encoding. That is not a bug in the asset. To check an accent, look in `Saved/Logs/Terreno.log` or on screen.
10. **Spanish editor names:**
    - Compile = Compilar
    - Save = Guardar
    - Override = Anular
    - Branch = Rama
    - Add decorator = Añadir decorador
    - Instance editable = Editable en instancia
    - The toolbar button Nuevo decorador creates a new decorator asset. To decorate an existing node, right-click that node instead.

## When to escalate

A low-cost agent should hand the problem to a stronger model (and write what it saw in `HANDOFF.md`) when any of these happen:

- After an edit, behavior in PIE differs from what `HANDOFF.md` predicts, and the export shows the edit was saved correctly.
- An `Accessed None`, `Infinite loop`, or crash appears in `Saved/Logs/Terreno.log`.
- A step needs a number not in `AI_REQUIREMENTS.md`.
- Two steps of the recipe contradict each other or the asset graph.
- The same fix has failed twice.

Before escalating, collect:
- The relevant `_<Asset>.txt` summaries.
- `bt_structure.py` output.
- Three or more `pie_sample.py` lines.
- The last 50 lines of the log that mention `LogBlueprintUserMessages`, `LogScript`, or `LogBehaviorTree`.

## Handoff between agents

An agent that stops work, even mid-task, must update `HANDOFF.md` before ending:

1. What changed, with asset paths.
2. What was verified in the editor, and what was only inferred.
3. The next concrete step.
4. Any new Unknown that blocks the next step.

The next agent treats `HANDOFF.md` as newer than these governance files when they disagree, and treats the repository as newer than the handoff when they disagree.

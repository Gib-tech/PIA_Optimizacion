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

## Handoff between agents

An agent that stops work, even mid-task, must update `HANDOFF.md` before ending:

1. What changed, with asset paths.
2. What was verified in the editor, and what was only inferred.
3. The next concrete step.
4. Any new Unknown that blocks the next step.

The next agent treats `HANDOFF.md` as newer than these governance files when they disagree, and treats the repository as newer than the handoff when they disagree.

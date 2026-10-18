# Project context

Facts below are separated from the assignment brief. Do not merge the two.

## Verified repository facts

Checked on 2026-10-11.

| Fact | Source |
| --- | --- |
| Workspace folder | `PIA_Optimizacion` |
| Unreal project file | `Terreno.uproject` |
| Engine | Unreal Engine 5.6 (`EngineAssociation`: `5.6`) |
| Code | No `.h`, `.cpp`, or `.cs` gameplay source files were found. Blueprint project. |
| Editor startup map | `/Game/ThirdPerson/Maps/ThirdPersonMap` |
| Default game map | `/Game/ThirdPerson/Maps/ThirdPersonMap` |
| Default game mode | `/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode` |
| Other project map found | `/Game/LevelMenu/MainMenuLevel` |

Enabled plugins in `Terreno.uproject`: ModelingToolsEditorMode, MotionTrajectory, PoseSearch, MotionWarping, AnimationWarping, Chooser, AnimationLocomotionLibrary.

### Gameplay assets that exist

Enemy AI folder: `Content/ThirdPerson/Blueprints/EnemigoIA/`

- `BP_BaseEnemy`
- `BP_IAController`
- `BPI_Enemy`
- `BB_EnemyIA`
- `BT_EnemyIA`
- `BTService_LocatePlayer`
- `BTTask_Attack`
- `BTTask_Defend`
- `BTTask_HitSun` (the hit-stun task; the asset name is spelled HitSun)
- `BTTask_Roam`
- `Enemy_Death`
- `Enemy_Death_Montage`

Related gameplay assets under `Content/ThirdPerson/Blueprints/`:

- `BP_ThirdPersonCharacter`
- `BP_ThirdPersonGameMode`
- `BP_TargetDummy`
- `Enums/E_States`
- `AnimNotifies/SaveLightAttack_AN`
- `AnimNotifies/BPC_Health`
- `AnimNotifies/Enemy_Health/BPC_E_Health`
- `AnimNotifies/ResetState_AN`
- `AnimNotifies/Health`
- `DañoDes`
- `PSD_Player`
- `PSS_Player`

Attack content that exists as assets, with no graph behavior confirmed:

- `Content/ThirdPerson/Animations/Fast_attacks/sword/`
- `Content/ThirdPerson/Animations/Heavy_attacks/Sword/`
- `Content/ThirdPerson/Input/Actions/IA_Heavy_Attack`

No asset whose file name identifies a hostage, escort follower, zone lock, conditional spawn, hammer, or wave manager was found. Absence of a matching file name is not proof that the feature is absent inside an unnamed Blueprint.

### Third-party content present

These folders are packaged content, not the assigned AI feature: `ParagonKallari`, `SciFiCharacterPack`, `SciFITrooper_Man_03`, `SciFiWarrior02`, `FreeAnimationLibrary`, `RamsterZ_FreeAnims_Volume1`, `Survival_Character`, `Fab`, `Characters`, `LevelPrototyping`.

## Stated premise

The protagonist is a time traveler who fights other time travelers to rescue a hostage. Environment models are justified by that premise. No further lore, character names, or faction names were provided.

## Stated game loop

This is a fast action game. The stated sequence is:

1. The player searches for the hostage and defeats enemies.
2. The player must find a second weapon, the hammer, before progressing.
3. The player reunites with the hostage and escorts the hostage to the final area.
4. The hostage escapes. The player must survive enemy waves. The wave size depends on how many enemies remain in the level, and the section has a time limit.
5. A progression system strengthens the character during the level.

Numeric values for the time limit, wave counts, hammer location, and progression rewards were not provided.

## Stated schedule and scope

- AI work is documented against Week 7 of the course schedule. The week-by-week calendar itself is not in the repository.
- The final delivery is Week 12, 19–25 October 2026.
- Extras wait until the essential work items are done.
- On the owner's board, the first AI is marked Done and still needs the combat integrations in `AI_REQUIREMENTS.md`. The second AI is To Do.

## Course rubric

Source: `FE-OV 1.docx`, supplied by the owner on 2026-10-11. The file header says the course is Optimización de Videojuegos, semester January–June 2025. The owner separately set the final delivery to 19–25 October 2026. Advertising, social networks, and the promo site are out of scope for this agent.

Development items marked as requirements on the final checklist:

- Two different attack types.
- Death message and return to the startup menu.
- At least three different objectives required to win.
- Two enemies with different advanced AI. Different behavior, not a different mesh on the same behavior.
- Local save of health, ammo, money, and position.
- At least two custom macros, two custom events, and two custom functions in the level, none of them engine defaults.
- Interface, Nanite, World Partition or World Composition, lighting, LODs, 15 models, 6 destructibles, 8 particle systems, and a working graphics options menu.

The full project text also asks for keyboard, mouse, and gamepad with matching actions, first- and third-person camera, a health bar, inventory, two NPCs with dialogue, day and night, and audio. Water is listed in the full text, and the final checklist marks the water body as not required.

Only the AI items are in the current work queue. The rest stay recorded so another agent does not treat them as invented extras or as this queue.

## Locked decisions

Orbit distances, defend timing, Print String text, hostage spacing, zone lock, conditional spawn, and the second enemy behavior are Decisions in `AI_REQUIREMENTS.md`. The owner delegated those choices on 2026-10-11. On 2026-10-14 the owner changed the orbit to radius 180 (band 150–210) and light damage to 25. On 2026-10-18 the owner changed light damage again, to combo 15 / 15 / 19.

## Verified graph facts

Exported from the open editor on 2026-10-14. The full per-asset state is in `HANDOFF.md` → "Saved asset state".

- Git: branch `main` (commit `7198fa9`) is the original project. Branch `feat/ai` holds the AI work. Assets are in Git LFS, so `git diff` on a `.uasset` only shows pointers. Compare behavior by exporting both versions.
- `BT_EnemyIA` is the five-branch Selector in `HANDOFF.md`. `BTService_LocatePlayer` sits on that Selector. On `main` the tree was smaller: a Selector containing a chase Sequence (Rotate to face → Move To `TargetActor` → Attack with Cooldown and Force Success) and Roam → Wait.
- Agent PIE on 2026-10-14 showed roam, orbit, defend, and attack running.
- `BP_ThirdPersonCharacter` has no Event AnyDamage. Player health (`BPC_Health.Decrease_Health`) is called only from a debug key with Damage 25. Enemy Apply Damage does not reach the player yet.
- `E_States` has two values: Nothing and Attack. `ResetState` calls `SetState` with Nothing.
- `SaveLightAttack_AN` calls `SaveLightAttack`. `bSaveLightAttack` buffers the next light-combo input.
- `BPC_E_Health.E_Decrease_Health` subtracts the Damage argument and fires `E_Dead` at 0 or below. BeginPlay and Tick on that component do not continue.
- `BP_BaseEnemy` Attack binds `E_Dead` (this belongs on BeginPlay), sphere-traces with radius 200, and applies damage 10 to the hit actor, then plays a montage with no asset set. `E_Dead` calls `Enemy_Death`, which only plays `Enemy_Death_Montage`.
- `BP_IAController` writes Blackboard `DetectionRadius` as 1500 on BeginPlay. That matches the locked value.
- The player weapon overlap casts to `BP_BaseEnemy`, prints `Hitbox detectada`, and does not execute `E_Decrease_Health`. That call is on the graph with Damage 100 and an empty execute pin.

## Unknown

- Walkable coordinates in `ThirdPersonMap`. Place new zones in reachable space and record the actor labels in `HANDOFF.md`. Do not invent landmark names.
- Hammer effect, progression rewards, survival time limit, and the wave-count formula.
- Which existing montage fits the enemy attack. The `BP_BaseEnemy` Play Montage node is empty.

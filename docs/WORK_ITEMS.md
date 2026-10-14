# Work items

Status values: `Todo`, `In progress`, `Blocked`, `Done`.

`Done` requires the acceptance check in `AI_REQUIREMENTS.md`. The owner's board says AI 1 is Done. These rows stay `In progress` or `Todo` until Play In Editor on `ThirdPersonMap` shows the behavior. `In progress` means the saved asset already contains that work.

Numbers and tree order are locked in `AI_REQUIREMENTS.md`. The exact click steps for every open row are in `HANDOFF.md` → "Pending work, in order".

## AI 1 — Orbiter

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI1-01 | In progress | Rebuild `BT_EnemyIA` into the five-branch tree: hit stun, defend, attack, orbit, roam. | Saved. Agent PIE on 2026-10-14 showed roam, orbit, defend, and attack running. Force Success was removed from Attack on 2026-10-14. That decorator was the "does not walk" bug. Hit stun is untested until AI1-03. Done after the owner's AI1-T1, AI1-T2, AI1-T3, and AI1-T6 pass. |
| AI1-02 | In progress | Add an orbit task that holds the 150–210 band around a 180 unit radius (owner decision 2026-10-14; was 320–480 / 400). | The old 400 orbit worked in agent PIE (387–464 units). The service still holds the old numbers. Change them with `HANDOFF.md` Step 0 (150 / 210 / 180 / 40°). Controller writes `DetectionRadius` 1500. Done after the owner's AI1-T2 and AI1-T5 pass. |
| AI1-03 | Todo | Apply damage only from a player light attack, and set `bReceivingDamage` only when health actually drops. | Not wired. Click steps: `HANDOFF.md` step 4. Light damage changes from 100 to 25 (owner decision 2026-10-14), so it takes 4 hits to kill. |
| AI1-04 | In progress | Print String on attack start, defend start, and hit-stun end, using the three Spanish lines. | Attack and defend lines were seen in the log during agent PIE. The defend text is missing the accent (`se esta`): `HANDOFF.md` step 1. The hit-stun line is untested until AI1-03. |
| AI1-05 | Todo | Cleanup: remove the `BTTask_Roam` debug prints and the orphan Branch. Clear the `BTTask_HitSun` error badge. | `HANDOFF.md` steps 2 and 3. |
| AI1-06 | Todo | Enemy death: bind `E_Dead` on BeginPlay, and stop the tree, movement, and collision on death. Add `bIsDead` and a health guard. | `HANDOFF.md` steps 5 and 7. Required before AI 2 can count living enemies. |
| AI1-07 | Todo | Player receives enemy damage (Event AnyDamage → `BPC_Health.Decrease_Health`). | `HANDOFF.md` step 8. Ask the owner first, because it edits the player. Needed for AI 3 contact damage. |

## AI 2 — Hostage escort

Build recipe: `HANDOFF.md` → "After AI 1: AI 2 hostage build recipe".

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI2-01 | Todo | Create `BP_Hostage`, `BB_Hostage`, `BT_Hostage`, and a controller that runs only that tree. | Follow, hold, and idle use the distances in the requirements. |
| AI2-02 | Todo | Create `BP_CombatZone` with an entrance blocker and a flee-point reference. Place one in reachable space on `ThirdPersonMap`. | Record the actor label in `HANDOFF.md`. Needs AI1-06 (`bIsDead`, `E_Dead` bound on BeginPlay). |
| AI2-03 | Todo | Create `BP_HostageSpawnZone`. Spawn 2 enemies once, only while the hostage is accompanying. | First zone uses `BP_BaseEnemy`. |
| AI2-04 | Todo | After the zone is clear, release the blocker and resume escort when the player comes within 400 units. | Depends on AI2-01 and AI2-02. |

## AI 3 — Charger

Required by the course rubric. Different tree from the orbiter. Not a second mesh on `BT_EnemyIA`. Build recipe: `HANDOFF.md` → "After AI 2: AI 3 charger build recipe".

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI3-01 | Todo | Create `BP_ChargerEnemy`, `BB_Charger`, `BT_Charger`, and a controller for that tree. | Chase, windup, charge, retreat, roam. |
| AI3-02 | Todo | Charge contact damages the player. Light and heavy attacks both damage the charger. | Existing enemy-hit damage is 10 (`BP_BaseEnemy` Apply Damage), so use 10, not the 15 fallback. Needs AI1-07 so the player actually loses health. |

## Order

1. `HANDOFF.md` Step 0 (new orbit numbers), AI1-04 accent, AI1-05 cleanup (10 minutes).
2. AI1-03 light damage (Damage 25).
3. AI1-06 death, AI1-07 player damage.
4. Owner PIE checks AI1-T1 to AI1-T6. Set AI1 rows Done.
5. AI2-01 through AI2-04.
6. AI3-01 and AI3-02. A second spawn zone may use `BP_ChargerEnemy` after AI3-01 exists.

## Not in this queue

| ID | Status | Item |
| --- | --- | --- |
| LOOP-01 | Not scheduled | Hammer as the required second weapon. |
| LOOP-02 | Not scheduled | Character progression during the level. |
| LOOP-03 | Not scheduled | Post-escape survival waves and time limit. |
| RUBRIC-01 | Not scheduled | Non-AI course rows: menus, save, dialogue NPCs, objectives, camera, gamepad parity, Nanite, World Partition, LODs, particles, destructibles. |

Advertising and social networks are out of scope.

## Editor tests

These are partial Play In Editor checks on `ThirdPersonMap`. Run one when its row says `Ready`. A pass here shows the behavior saved so far. It does not set a work item to `Done`; `Done` still requires the acceptance checks in `AI_REQUIREMENTS.md`.

Test status values: `Not ready`, `Ready`, `Passed`, `Failed`. A test is `Passed` (**Verified**) only after the owner sees it in Play In Editor and the result is written in the log below. Neither an export nor an agent-run PIE counts as a pass.

How to run: open `ThirdPersonMap` and press Play. Press `'` (apostrophe) for the gameplay debugger, then the Behavior Tree category (numpad 2 by default), to see which branch is active. The enemies start about 3700 units from `PlayerStart` toward −Y. Walk toward them.

| ID | Status | Becomes ready | Check |
| --- | --- | --- | --- |
| AI1-T1 | Ready | — | Walk toward an enemy. Inside 1500 units it leaves roam and starts orbit, defend, or attack. Far away, it wanders and pauses about 3 seconds between walks. |
| AI1-T2 | Not ready | After `HANDOFF.md` Step 0. | After it detects you, stand still. It circles close, near 180 units, and does not walk onto your capsule. It prints `Enemigo: va a atacar` about every 3 s while circling. Step back past 210 (still inside 1500) and it follows. Walk into it, inside 150, and it backs out. |
| AI1-T3 | Ready | After step 1 (accent), to check the exact text. | Inside 220, with the 3 second cooldown ready, the screen shows `Enemigo: va a atacar` for about 2 seconds. Inside 600, at least 6 seconds after the last defend, it shows `Enemigo: se está defendiendo` for about 2 seconds, and the enemy faces you without moving for 1.5 seconds. |
| AI1-T4 | Not ready | After `HANDOFF.md` step 4. | A light attack drops the orbiter's health. About 0.6 seconds later the screen shows `Enemigo: ya no recibe daño`. The 4th light hit kills it (25 × 4 = 100). A heavy attack does not drop that health and does not show that line. |
| AI1-T5 | Ready | — | Stand between 1000 and 1500 units from an enemy. It detects you and comes in to orbit. |
| AI1-T6 | Not ready | After `HANDOFF.md` step 5. | Kill an enemy. It plays the death montage, stops moving, stops printing, and disappears after a few seconds. |

### Result log

| Date | Test | Result | What was seen |
| --- | --- | --- | --- |
| 2026-10-13 | AI1-T1, AI1-T2, AI1-T3 | Failed | Play In Editor on `ThirdPersonMap`. The enemy did not orbit, defend, or attack. The log repeated `BTService_LocatePlayer`: Accessed None reading `K2Node_DynamicCast_AsBP_Third_Person_Character` from Set Blackboard Value as Float, Branch, and Set Blackboard Value as Vector. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Fourth play. The startup attack line is gone. Both enemies printed defend about 9 seconds into the play and did not walk. (The agent-height explanation logged at the time was wrong. The cause was Force Success on Attack plus Defend never finishing.) |
| 2026-10-13 | AI1-T1 | Failed | After the editor closed at 21:56, the next play brought back the `BTService_LocatePlayer` Accessed None error. `BTTask_Defend` printed `Hello`. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Agent-run PIE, not the owner. No Accessed None. No movement during 60 s of roam. When the player was teleported 450 units from an enemy, the Blackboard got the target, distance, and orbit point. Both enemies printed defend once and froze, because `BTTask_Defend` had no Finish Execute. |
| 2026-10-14 | (informal) | Owner report | After Force Success was removed, the owner reported "now they're moving". This is not a formal check of any row. |
| 2026-10-14 | AI1-T1, AI1-T2, AI1-T3 | Agent PIE, not a pass | Roam: both enemies walked, then waited. When the player was teleported 450 units away, the enemy orbited at 387–719 units (mostly 387–464) without touching the capsule. Defend printed every 8–10 s and finished. Attack printed once. No errors in the log. The owner must still run these for a pass. |

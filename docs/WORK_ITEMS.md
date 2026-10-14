# Work items

Status values: `Todo`, `In progress`, `Blocked`, `Done`.

`Done` requires the acceptance check in `AI_REQUIREMENTS.md`. The owner's board says AI 1 is Done. These rows stay `In progress` or `Todo` until Play In Editor on `ThirdPersonMap` shows the behavior. `In progress` means the saved asset already contains that work.

Numbers and tree order are locked in `AI_REQUIREMENTS.md`.

## AI 1 — Orbiter

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI1-01 | In progress | Rebuild `BT_EnemyIA` into the five-branch tree: hit stun, defend, attack, orbit, roam. | Saved and exported on 2026-10-13. Order, left to right: `BTTask_HitSun` (`bReceivingDamage` Is Set, abort Self), defend sequence (distance <= 600, cooldown 6), `BTTask_Attack` (cooldown 3, Force Success, distance <= 220), orbit sequence (`TargetActor` Is Set), roam sequence. Play In Editor has not been run. Do not rename `BTTask_HitSun`. |
| AI1-02 | In progress | Add an orbit task that holds the 320–480 band around a 400 unit radius. | `BTService_LocatePlayer` writes `OrbitLocation` and `DistanceToTarget`. Move To uses `OrbitLocation`. Both Rotate to face tasks use `TargetActor`. Inside the band the point rotates 18 degrees. `BP_IAController` still writes `DetectionRadius` 1000, while the locked detect distance is 1500. |
| AI1-03 | Todo | Apply damage only from a player light attack, and set `bReceivingDamage` only when health actually drops. | The overlap prints `Hitbox detectada` and stops. `E_Decrease_Health` is on the graph with Damage 100, and its execute pin is empty. `bSaveLightAttack` is a combo buffer. Do not use it, or `IsAttacking`, as the light-hit gate. Next step is in `HANDOFF.md`. |
| AI1-04 | In progress | Print String on attack start, defend start, and hit-stun end, using the three Spanish lines. | All three strings are in the task graphs, duration 2, print to screen on. They are Development Only, which still runs in editor Play In Editor. They have not been seen on screen. |

## AI 2 — Hostage escort

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI2-01 | Todo | Create `BP_Hostage`, `BB_Hostage`, `BT_Hostage`, and a controller that runs only that tree. | Follow, hold, and idle use the distances in the requirements. |
| AI2-02 | Todo | Create `BP_CombatZone` with an entrance blocker and a flee-point reference. Place one in reachable space on `ThirdPersonMap`. | Record the actor label in `HANDOFF.md`. |
| AI2-03 | Todo | Create `BP_HostageSpawnZone`. Spawn 2 enemies once, only while the hostage is accompanying. | First zone uses `BP_BaseEnemy`. |
| AI2-04 | Todo | After the zone is clear, release the blocker and resume escort when the player comes within 400 units. | Depends on AI2-01 and AI2-02. |

## AI 3 — Charger

Required by the course rubric. Different tree from the orbiter. Not a second mesh on `BT_EnemyIA`.

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI3-01 | Todo | Create `BP_ChargerEnemy`, `BB_Charger`, `BT_Charger`, and a controller for that tree. | Chase, windup, charge, retreat, roam. |
| AI3-02 | Todo | Charge contact damages the player. Light and heavy attacks both damage the charger. | If no existing enemy-hit damage exists, use 15 and record it. |

## Order

1. AI1-01 through AI1-04.
2. AI2-01 through AI2-04.
3. AI3-01 and AI3-02. A second spawn zone may use `BP_ChargerEnemy` after AI3-01 exists.

## Not in this queue

| ID | Status | Item |
| --- | --- | --- |
| LOOP-01 | Not scheduled | Hammer as the required second weapon. |
| LOOP-02 | Not scheduled | Character progression during the level. |
| LOOP-03 | Not scheduled | Post-escape survival waves and time limit. |
| RUBRIC-01 | Not scheduled | Non-AI course rows: menus, save, dialogue NPCs, objectives, camera, gamepad parity, Nanite, World Partition, LODs, particles, destructibles. |

Advertising and social networks are out of scope.

## Editor tests

Partial Play In Editor checks on `ThirdPersonMap`. Run one when its row says `Ready`. A pass here shows the behavior saved so far. It does not set a work item to `Done`. `Done` still requires the acceptance checks in `AI_REQUIREMENTS.md`.

Test status values: `Not ready`, `Ready`, `Passed`, `Failed`. `Passed` is **Verified** only after you see it in Play In Editor and the result is written in the log below. An export is not a pass.

`Failed` on 2026-10-13 uses the saved orbiter. The service errors before it can write the player, so AI1-T1, AI1-T2, and AI1-T3 cannot pass until that cast read is fixed. `BP_IAController` still writes `DetectionRadius` 1000, so the rerun stays inside 1000 units. The locked detect distance of 1500 is AI1-T5, and it is not ready. Light damage is not wired, so AI1-T4 is not ready.

| ID | Status | Becomes ready | Check |
| --- | --- | --- | --- |
| AI1-T1 | Failed | Again, after the `BTService_LocatePlayer` cast read is fixed and the owner compiles and saves. | Walk to the existing enemy until you are inside 1000 units. It leaves roam and starts orbit, defend, or attack. |
| AI1-T2 | Failed | Same as AI1-T1. | After it detects you, stand still. It circles near 400 units and does not walk onto your capsule. Past 480, and still inside 1000, it moves in. Inside 320, it moves out. |
| AI1-T3 | Failed | Same as AI1-T1. | Within 220, and when the 3 second cooldown is ready, the screen shows `Enemigo: va a atacar` for about 2 seconds. Within 600, and when 6 seconds have passed since the last defend, it shows `Enemigo: se está defendiendo` for about 2 seconds. |
| AI1-T4 | Not ready | After `bLightAttackActive` is saved, the weapon overlap runs `E_Decrease_Health` only while that bool is true, and that call sets `bReceivingDamage`. | A light attack drops the orbiter's health. About 0.6 seconds later the screen shows `Enemigo: ya no recibe daño`. A heavy attack does not drop that health and does not show that line. |
| AI1-T5 | Not ready | After the controller writes `DetectionRadius` 1500. | Stand between 1000 and 1500 units. The enemy detects you and orbits. |

### Result log

| Date | Test | Result | What was seen |
| --- | --- | --- | --- |
| 2026-10-13 | AI1-T1, AI1-T2, AI1-T3 | Failed | Play In Editor on `ThirdPersonMap`. The enemy did not orbit, defend, or attack. The log repeated `BTService_LocatePlayer`: Accessed None reading `K2Node_DynamicCast_AsBP_Third_Person_Character` from Set Blackboard Value as Float, Branch, and Set Blackboard Value as Vector. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Fourth play. Startup attack line is gone. Both enemies printed defend about 9 seconds into the play and did not walk. Navmesh agent height is 144. Enemy nav agent height is 176, so Move To has no matching nav data. |
| 2026-10-13 | AI1-T1 | Failed | After the editor closed at 21:56, the next play brought back the `BTService_LocatePlayer` Accessed None error. `BTTask_Defend` printed `Hello`. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Agent-run PIE, not the owner. No Accessed None. No movement during 60 s of roam. Player teleported 450 units from an enemy: the Blackboard got the target, distance, and orbit point. Both enemies printed `Enemigo: se esta defendiendo` once and froze, because `BTTask_Defend` has no Finish Execute. |

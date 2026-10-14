# Handoff

Living note for the next agent. Replace the "Current handoff" section when work changes. Keep older entries under History.

Read order: `GOVERNANCE.md`, `PROJECT_CONTEXT.md`, `AI_REQUIREMENTS.md`, `WORK_ITEMS.md`, this file.

## Current handoff

- Date: 2026-10-13
- Author: AI1 orbiter wiring, verified by T3D export from the open Terreno editor
- Area: AI 1 orbiter
- Editor: Unreal Engine 5.6.1, Spanish UI. Remote Python execution is on in `Config/DefaultEngine.ini` (`bRemoteExecution=True`). The editor must be open. Run `python Intermediate\_run_remote.py` after pointing that runner at an export script. Do not pass Python through `python -c`; PowerShell eats the quotes.
- Audit: 2026-10-13 ~23:00. Re-exported every orbiter asset from the open editor (no dirty packages) and ran agent-driven Play In Editor sessions through Python. No asset was modified.
- Verified on disk now: `BTService_LocatePlayer` reads Get Actor Location from the `PlayerCharacter` variable, not the cast pin. The Accessed None error is gone. `DistanceToTarget` default is 100000. In PIE, after the player was teleported 450 units from an enemy, `TargetActor`, `DistanceToTarget`, and `OrbitLocation` were all written correctly.
- Verified on disk now: `BTTask_Defend` is only Event Receive Execute AI → Print String `Enemigo: se esta defendiendo` (no accent). There is no Delay and no Finish Execute. In PIE both enemies printed it once and never moved again. This is the freeze.
- Verified: agent height is not a blocker. `SupportedAgents` is empty, so every pawn uses `RecastNavMesh-Default`. A path query with the enemy as querier is valid, and a direct Move To Location from Python walked an enemy about 530 units in PIE. Do not change Agent Height.
- Verified in PIE: with no player in range for 60 seconds, the tree was running, path following stayed Idle, and neither enemy moved. Roam is not producing movement. Cause not isolated. Unknown.
- The editor crashed once at 23:02 from an agent Python probe (object iterator), not from project content. It restarted clean.

### What the saved orbiter does

`BT_EnemyIA` uses `BB_EnemyIA`. The root Selector children, left to right, are:

1. Sequence. Decorator: `bReceivingDamage` Is Set, Observer Aborts = Self. Child: `BTTask_HitSun`.
2. Sequence. Decorators: `DistanceToTarget` Is Less Than Or Equal To 600, abort Lower Priority, and Cooldown 6. Children: Rotate to face `TargetActor`, then `BTTask_Defend`.
3. `BTTask_Attack` directly on the Selector. Decorators: Cooldown 3, Force Success, `DistanceToTarget` Is Less Than Or Equal To 220, abort Lower Priority. The task Target key is `TargetActor`.
4. Sequence. Decorator: `TargetActor` Is Set, abort Lower Priority. Children: Rotate to face `TargetActor`, then Move To `OrbitLocation`.
5. Sequence with no decorator: `BTTask_Roam`, then Wait 3 ± 0.5.

`BTService_LocatePlayer` is on the Selector. Its key selectors are Search Radius = `DetectionRadius`, Target Actor = `TargetActor`, Distance To Target Key = `DistanceToTarget`, Orbit Location Key = `OrbitLocation`. The service interval is not overridden, so it uses the engine default 0.5 seconds.

On a hit, the service writes the player into `TargetActor` and the distance into `DistanceToTarget`. On a miss it clears `TargetActor` and sets `DistanceToTarget` to 100000. Outside the 320–480 band, `OrbitLocation` is the player location plus the normalized enemy-minus-player vector times 400. Inside the band, that same offset is rotated 18 degrees around world up. The 18 degree step is the 250 cm/s strafe at radius 400 over a 0.5 second tick.

`BTTask_HitSun`: Receive Execute AI, Delay 0.6, Set Value as Bool `bReceivingDamage` false through Make Literal Name, Print String `Enemigo: ya no recibe daño` for 2 seconds, Finish Execute success. The Set Value as Bool node is saved with `ErrorType=1`. Compile this task before Play In Editor if that node shows an error.

`BTTask_Attack` prints `Enemigo: va a atacar` for 2 seconds, then calls `BPI_Enemy.Attack` when the target is valid, then finishes success.

`BTTask_Defend` prints `Enemigo: se esta defendiendo` (missing the accent) for 2 seconds and stops. The Delay 1.5 and Finish Execute nodes are not in the saved asset, so the task never ends.

`BTTask_Attack` has no Finish Execute on the Is Valid → Is Not Valid pin, so it hangs if the target is invalid.

`BP_BaseEnemy` binds `E_Dead` to `Enemy_Death` inside the Attack event, not on BeginPlay, so an enemy that has not attacked yet cannot play its death. The Attack Play Montage node has no montage asset. `Enemy_Death` does not stop the Behavior Tree.

All three Print String nodes are Development Only. They still run in editor Play In Editor.

Blackboard keys: `SelfActor`, `DetectionRadius`, `TargetActor`, `bReceivingDamage`, `DistanceToTarget`, `OrbitLocation`.

`BP_IAController` still writes `DetectionRadius` 1000. The locked detect distance is 1500. Do not treat 1000 as a new decision.

### What is not done

Light-only damage is not wired. On `BP_ThirdPersonCharacter`, the weapon-hitbox overlap casts to `BP_BaseEnemy` and prints `Hitbox detectada`. That Print String then pin is empty. `E_Decrease_Health` is already on the graph, its target is the enemy `BPC_E_Health`, Damage is 100, and its execute pin is empty.

`bSaveLightAttack` is the combo buffer. `IsAttacking` is set for more than the light attack. Neither one is the light-hit gate. `bLightAttackActive` does not exist yet.

`BP_BaseEnemy` Attack applies 10 damage to whoever the sphere trace hits. That is the enemy hitting another actor. AI 3 will reuse 10. Do not change it for the orbiter.

AI 2 and AI 3 have not been started. No hostage, combat zone, spawn zone, or charger asset was created.

### What the next agent should do

The agent height step is withdrawn (see the audit lines above). The current click is `BTTask_Defend`: after Print String, add Delay 1.5, then Finish Execute with Success checked, and add the accent to the string. Then wire `BTTask_Attack` Is Not Valid to a Finish Execute with Success unchecked. Then diagnose Roam: in PIE press the apostrophe key for the gameplay debugger and read the active Behavior Tree node while no player is in range.

On the player, the light and heavy input chains are separate copies. Light is `IA_Light_Attack` at graph Y ≈ −2672. Heavy is `IA_Heavy_Attack` at Y ≈ −1760. Edit only the light one in step 2.

Unknown for the owner: the orbit band (320–480) keeps the enemy outside the attack range (220), so attack only fires when the player walks in. Also `E_Health` is 100 and the light damage is 100, so the first light hit kills and the hit-stun branch never shows on a living enemy. Both numbers are locked. Do not change them without the owner.

Finish AI1-03 on `BP_ThirdPersonCharacter`, then ask the owner to compile, save, and play. Re-export the character after they say it is saved, before giving the next click.

1. Add a bool `bLightAttackActive`, default false.
2. On the `IA_Light_Attack` event, the Started pin enters a Branch. The false output sets `IsAttacking` and then goes to Weapon to Hand. Break that wire with Alt+left click and insert Set `bLightAttackActive` checked.
3. On custom event `ResetState`, the then pin goes to `SetState` (Nothing). Break that wire and insert Set `bLightAttackActive` unchecked.
4. From Print String `Hitbox detectada` then, add a Branch. Condition is Get `bLightAttackActive`. The true output enters the existing `E_Decrease_Health` execute. Leave Damage at 100.
5. From `E_Decrease_Health` then, Cast to AIController. The object is Get Controller from the `BP_BaseEnemy` cast. From As AIController, Get Blackboard, then Set Value as Bool. Key name is Make Literal Name `bReceivingDamage`, checkbox on.

A heavy attack must not set `bLightAttackActive`. Do not edit the heavy-attack graph until it is exported. Do not gate this on `bSaveLightAttack`.

After that, set the controller float that writes `DetectionRadius` from 1000 to 1500, then run Play In Editor on `ThirdPersonMap` for the four AI 1 checks. Only then mark AI1-01 through AI1-04 Done.

Editor UI is Spanish. Blueprint override is Anular. A Blackboard Key Selector appears on the green service node only when the variable is Editable en instancia. The toolbar button Nuevo decorador creates an asset. Right-click the node, Añadir decorador, Blackboard, to decorate that node. On a bool key the only queries are Is Set and Is Not Set. Is Set passes when the bool is true. Set the key before the query, or a bool key only shows those two.

Empty decorator graph objects may remain inside `BT_EnemyIA` from the add-decorator menu. Leave them unless they are visible and blocking the owner.

### Files touched in this pass

Behavior assets, saved by the owner in the editor on 2026-10-13:

- `Content/ThirdPerson/Blueprints/EnemigoIA/BB_EnemyIA`
- `Content/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA`
- `Content/ThirdPerson/Blueprints/EnemigoIA/BTService_LocatePlayer`
- `Content/ThirdPerson/Blueprints/EnemigoIA/BTTask_Attack`
- `Content/ThirdPerson/Blueprints/EnemigoIA/BTTask_Defend`
- `Content/ThirdPerson/Blueprints/EnemigoIA/BTTask_HitSun`

Docs updated for the next agent:

- `docs/GOVERNANCE.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/AI_REQUIREMENTS.md`
- `docs/WORK_ITEMS.md`
- `docs/HANDOFF.md`

## History

### 2026-10-13 — Full orbiter audit with agent-run PIE

Re-exported all orbiter assets and the player character. Ran short Play In Editor sessions from Python. Found the Defend task never finishes, Roam never moves, and agent height is not a blocker. No asset changed.

### 2026-10-13 — Orbiter tree saved, damage gate still open

Re-exported the Selector, the service, the three tasks, the health component, the enemy, and the player character. The five branches, orbit math, and three Spanish prints are in the assets. Player damage still does not execute. No Play In Editor test.

### 2026-10-11 — Enemy tree inspected, blackboard keys added

Connected to the open Terreno editor. Recorded the live `BT_EnemyIA` structure. Saved `bReceivingDamage`, `DistanceToTarget`, and `OrbitLocation` on `BB_EnemyIA`. No behavior-tree branches were rewired.

### 2026-10-11 — Decisions locked

The owner delegated the open choices and supplied `FE-OV 1.docx`. Locked Behavior Trees, the orbiter tuning, the hostage zone rules, and a second enemy (charger) required by the rubric. No Blueprint, map, or config asset was modified.

### 2026-10-11 — Governance created

Created the English agent docs from the owner brief and from files present in the repository. No Blueprint, map, or config asset was modified.

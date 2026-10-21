# Handoff

Living note for the next agent. Replace the "Current handoff" section when work changes. Keep older entries under History.

Read order: `GOVERNANCE.md`, `PROJECT_CONTEXT.md`, `AI_REQUIREMENTS.md`, `WORK_ITEMS.md`, this file.

This file is written so a smaller model can continue without re-auditing. Every step below names the exact asset, node, and pin. Follow the steps in order. When a step's result does not match what is written here, stop and use the escalation rule in `GOVERNANCE.md` ("When to escalate").

## Current handoff

- Date: 2026-10-18
- Branch: `feat/ai`. `main` is the untouched original project and is the reference for "how it was before".
- Uncommitted: `Content/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA.uasset` (Force Success removed), the docs, and `Tools/UnrealPython/`. Only the owner commits.
- Area: AI 1 orbiter. Its movement works. Combat integration and cleanup are still open.
- Editor: Unreal Engine 5.6.1, Spanish UI, project `Terreno.uproject`, map `ThirdPersonMap`.

### TL;DR

On 2026-10-14 the owner resolved both open decisions: orbit at 180 (band 150–210) and light damage 25. On 2026-10-18 the owner replaced the flat 25 with combo damage **15 / 15 / 19** (swings 1 and 2, then the finisher). That Select is saved, and `FA_1_Montage` now has the hit window. Step 0, Step 0b, and the light hitbox switch are saved. Agent PIE after Step 0b showed both enemies inside 150–210 (distances 150–170), orbit points moving between samples, and `Enemigo: va a atacar` about every 3 seconds. The remaining AI 1 work is the owner's PIE checks. The player damage wire is saved. The owner finished the defend accent and the Roam debug cleanup on 2026-10-14 and asked not to play-test either. AI 2 and AI 3 have not started.

### What fixed movement (read this before touching any tree)

`BTTask_Attack` sat directly on the root Selector with a **Force Success** decorator. Force Success turns *any* result into success, including the result of its sibling Blackboard decorator failing. A Selector stops at the first child that succeeds, so every pass through the tree ended at Attack, and Orbit and Roam never ran. The enemy only rotated (the Defend branch faces the player). Removing Force Success fixed it.

Rule: never put Force Success on a direct child of a Selector. See the pitfalls list in `GOVERNANCE.md`.

### Verified in agent PIE on 2026-10-14

These were run through `Tools/UnrealPython/` (see `GOVERNANCE.md` → Agent tooling).

- Roam: with the player at spawn (about 3500 units away), both enemies walked (path status MOVING, speed up to 600), then stood for the Wait. `TargetActor` = None, `DistanceToTarget` = 100000, `DetectionRadius` = 1500.
- Orbit: the player was teleported 450 units from enemy 0. Over 30 seconds the enemy stayed 387–719 units away (mostly 387–464). Its position and `OrbitLocation` kept changing around the player. It never touched the capsule.
- Defend: `Enemigo: se esta defendiendo` printed about every 8–10 seconds (6 s cooldown + 1.5 s task). The task now finishes.
- Attack: `Enemigo: va a atacar` printed once when the distance briefly dropped to 220 or less.
- No `Accessed None` errors in `Saved/Logs/Terreno.log`.
- Hit stun is not tested. Nothing sets `bReceivingDamage` yet (that is AI1-03).

### Saved asset state (exported 2026-10-14, no dirty packages)

`BT_EnemyIA`, blackboard `BB_EnemyIA`. Root Selector, service `BTService_LocatePlayer` (interval 0.5 default). Children left to right:

1. `Sequence_0`. Decorator: Blackboard `bReceivingDamage` Is Set, Observer aborts Self. Child: `BTTask_HitSun`.
2. `Sequence_1`. Decorators: Blackboard `DistanceToTarget` <= 600 with abort Lower Priority, and Cooldown 6. Children: Rotate to face BB entry `TargetActor`, then `BTTask_Defend`.
3. `BTTask_Attack` (Target = `TargetActor`). Decorators: Cooldown 3, and Blackboard `DistanceToTarget` <= 220 with abort Lower Priority. No Force Success.
4. `Sequence_3`. Decorator: Blackboard `TargetActor` Is Set, abort Lower Priority. Children: Rotate to face `TargetActor`, then Move To `OrbitLocation`. Move To settings: Allow Strafe on, Observe Blackboard Value on, Reach Test Includes Agent Radius **off** (Step 0b, 2026-10-14), Acceptable Radius still the default 5, plus the service "Set default focus" with key `TargetActor`.
5. `Sequence_2`, no decorator. Children: `BTTask_Roam`, then Wait 3 ± 0.5.

`BB_EnemyIA` keys: `SelfActor`, `DetectionRadius` (float, default 1500), `TargetActor` (object), `bReceivingDamage` (bool), `DistanceToTarget` (float, default 100000), `OrbitLocation` (vector).

`BP_IAController`: BeginPlay → Run Behavior Tree `BT_EnemyIA` → Get Blackboard → Set Value as Float `DetectionRadius` = 1500.

`BTService_LocatePlayer` (correct, do not rework):
1. It sets `PlayerCharacter` to None.
2. It runs a Sphere Trace Multi for Objects at the pawn location with radius = BB `DetectionRadius` and object type Pawn, ignoring self.
3. For each hit, it casts to `BP_ThirdPersonCharacter` and stores the result in `PlayerCharacter`.
4. If `PlayerCharacter` is valid, it sets BB `TargetActor` and BB `DistanceToTarget`, then writes BB `OrbitLocation`:
   - Distance below 320 or above 480: player + Normalize(enemy − player) × 400.
   - Distance from 320 to 480: player + (enemy − player) rotated 18° around Z.
   - Saved values as of 2026-10-14 after Step 0: 150 / 210 / 180 / 40°. Export check passed (`=320`, `=480`, `=400`, `=18.` had no hits).
5. If it is not valid, it clears `TargetActor` and sets `DistanceToTarget` to 100000.

`BTTask_Defend`: Receive Execute AI → Print String `Enemigo: se está defendiendo` (2 s) → Delay 1.5 → Finish Execute (Success on). The owner added the accent on 2026-10-14. Not re-exported. The package was not dirty.

`BTTask_Attack`: Receive Execute AI → Print String `Enemigo: va a atacar` (2 s) → Is Valid (Get Blackboard Value as Actor, key `Target`).
- Is Valid → `BPI_Enemy` Attack (message) on the controlled pawn → Finish Execute (Success on).
- Is Not Valid → Finish Execute (Success off).

`BTTask_HitSun`: Receive Execute AI → Delay 0.6 → Set Value as Bool (target: Get Blackboard of Owner Controller, Key Name: Make Literal Name `bReceivingDamage`, value off) → Print String `Enemigo: ya no recibe daño` (2 s) → Finish Execute (Success on). That node is the only Set Value as Bool in the Event Graph node list, and it has no `ErrorType`. The owner moved it to about (880, −352) on 2026-10-14. Two old objects (`SetValueAsBool` with `ErrorType=1`, and an unwired `SetBlackboardValueAsBool`) are still in the asset text but are not in the Event Graph `Nodes` list, so they do not appear in the editor. Do not ask the owner to delete them.

`BTTask_Roam`: Receive Execute AI → AI MoveTo (pawn = Controlled Pawn, destination = Get Random Reachable Point In Radius around the pawn location, radius = variable `RoamRadius` 1000, acceptance radius 5).
- On Success → Finish Execute (Success on).
- On Fail → Finish Execute (Success off).
- The owner removed the debug prints and the orphan Branch on 2026-10-14. Not re-exported. The package was not dirty.

`BP_BaseEnemy` (death chain saved 2026-10-18, Reason `Dead`):
- Event BeginPlay → Bind Event to E_Dead. Target is `BPC_E_Health`. Event is custom event `Enemy_Death`.
- Event `Attack` (from `BPI_Enemy`, input `TargetActor`) goes straight to Sphere Trace Multi for Objects at its own location, radius 200, Pawn. The bind is no longer in this chain.
- For Each with Break. If Hit Actor == `TargetActor`, it calls Apply Damage 10 and then Play Montage (mesh `Mesh`). **Montage To Play is empty**, then the loop breaks.
- Custom event `Enemy_Death` → Set `bIsDead` true → Play Anim Montage `Enemy_Death_Montage` → Get Controller → Cast To AIController → Get Brain Component → Stop Logic (Reason `Dead`) → Disable Movement → Set Collision Enabled No Collision on the capsule → Set Life Span 3.
- Attack Play Montage still has Montage To Play empty. The mesh is `SK_SciFiWarrior02` (skeleton `UE4_Mannequin_Skeleton`). None of the 20 montages in the project use that skeleton, so Step 6 left the pin empty. `Enemy_Death_Montage` uses the SciFi trooper skeleton.
- Pawn defaults: capsule radius 34, half height 88. Max walk speed 600. Orient Rotation to Movement off. Use Controller Rotation Yaw on. Auto Possess AI = Placed in World or Spawned. AI Controller Class = `BP_IAController`.

`BPC_E_Health`: `E_Decrease_Health(Damage)` does these steps in order:
1. Branch: `E_Health` > 0. False ends. True continues. The greater-than B pin has no serialized number, which is the float default 0, same as the existing less-or-equal pin below.
2. `E_Health` −= Damage. `E_Health` defaults to 100.
3. Calls `E_Updated_Heatlh` (the typo is in the asset).
4. If `E_Health` <= 0, calls `E_Dead`.

`BP_ThirdPersonCharacter` (relevant parts):
- WeaponHitbox On Component Begin Overlap → Cast to `BP_BaseEnemy` → Print String `Hitbox detectada` → Branch on `bLightAttackActive`.
- The node `E_Decrease_Health` (target: the cast enemy's `BPC_E_Health`) runs from the hitbox Branch's True pin. Its Damage pin is the 15 / 15 / 19 Select. Its `then` pin goes to the object Cast To AIController.
- The light and heavy attack chains are separate copies. Light starts at event `IA_Light_Attack` (graph Y ≈ −2672). Heavy starts at `IA_Heavy_Attack` (Y ≈ −1760).
  - Light: Started → Branch → (False) Set `IsAttacking` → Set `bLightAttackActive` → Weapon to Hand → Play Montage `LightAttackCombo[AttackIndex]` at (4144, −2624). That node's white `then` goes to a Branch at (4416, −2160) which sets `AttackIndex` to `AttackIndex + 1`, or to 0 on the last swing. On Completed → `IsAttacking` false → `bLightAttackActive` false → `AttackIndex` 0 → Weapon to Back.
  - That same Play Montage's On Notify Begin feeds Switch on Name at (4672, −2896). `EnableHitbox` sets `WeaponHitbox` collision to Query Only. `DisableHitbox` sets it to No Collision. Saved 2026-10-18.
- `ResetState` → `SetState` (Nothing) → `AttackIndex` 0 → `bSaveLightAttack` false.
- `bLightAttackActive` exists (bool, default false). Light start sets it true, light On Completed and `ResetState` set it false. WeaponHitbox overlap → Cast to `BP_BaseEnemy` → Print String → Branch on `bLightAttackActive`. True calls `E_Decrease_Health`. Its Damage pin is a Select: Index = `LightSwingIndex`, Option 0 = 15, Option 1 = 15, Option 2 = 19. Then Cast To AIController (object) fed by Get Controller, then Get Blackboard → Set Value as Bool `bReceivingDamage` checked. Heavy attack was not changed.
- `LightSwingIndex` is set from `AttackIndex` on the live Play Montage's `then` pin, before the Branch that increments `AttackIndex`. `LightAttackCombo` order is `FA_1_Montage`, `FA_2_Montage`, `L_FA_3_Montage`.
- The player has Event AnyDamage (`ReceiveAnyDamage`). Its `then` calls `BPC_Health.Decrease_Health`, and the event's Damage pin feeds that node's Damage pin. Damage Type, Instigated By, and Damage Causer are empty. The debug key still calls Decrease Health with 25. Saved 2026-10-18. Enemy Apply Damage 10 now reaches the player.

Placed actors on `ThirdPersonMap`:

| Actor | Location |
| --- | --- |
| `BP_BaseEnemy` | (1140, 1970, 198) |
| `BP_BaseEnemy2` | (1490, 1980, 198) |
| `PlayerStart` | (1380, 5670, 212) |
| `NavMeshBoundsVolume` | origin (1330, 2300, 250), extent (1725, 1250, 250) |

Nav: `SupportedAgents` is empty, so every pawn uses `RecastNavMesh-Default` (height 144, radius 35). Do not change agent height. It is not a problem.

### Pending work, in order

**Playtest block.** Combo damage is saved: Select Option 0 = 15, Option 1 = 15, Option 2 = 19. All three light montages open the hitbox. Event AnyDamage is saved and forwards the incoming Damage pin to `BPC_Health.Decrease_Health`. The enemy still sends 10. AI1-T1 through AI1-T6 are ready for the owner. An export is not a pass.

**Next — Step 9, owner play.** No more Blueprint edits until the play result is written down. Open `ThirdPersonMap`, press Play, and check:

1. A light combo deals 15, then 15, then 19. About 0.6 seconds after each hit the screen shows `Enemigo: ya no recibe daño`. A heavy attack does not drop that health.
2. Two full light combos leave the enemy at 2 health. The next light hit kills it. It plays the death montage, stops moving, stops printing, and disappears after a few seconds.
3. While an enemy is in range, its attack lowers the player's health by 10. The debug key is still a separate 25.

If one swing removes 30 or 38, the hitbox overlapped twice. Record what was seen. Do not add a new number.

Each step: the owner (or an agent instructing the owner) makes the edit, presses **Compilar**, then **Guardar**. Then re-export with `Tools/UnrealPython/export_ai.py` and confirm the change in the summary before going to the next step. Spanish UI names are given in parentheses.

**Step 1 — Defend accent (AI1-04).** Done 2026-10-14. Owner edited the Print String and asked not to play-test it. Dirty packages were none. Original click: open `BTTask_Defend`, set `In String` to `Enemigo: se está defendiendo`, compile, save.

**Step 2 — Remove Roam debug nodes.** Done 2026-10-14. Owner removed both debug Print Strings and the orphan Branch, and wired AI MoveTo On Fail to Finish Execute with Success off. Asked not to play-test it. Dirty packages were none.

**Step 3 — Clear the HitSun error badge.** Done 2026-10-14. The node on the graph is wired Delay → Set Value as Bool → Print String → Finish Execute, with no `ErrorType`. A second export after the owner moved that node confirmed it is the only Set Value as Bool in the Event Graph `Nodes` list. An `ErrorType=1` object remains in the asset text and is not a graph node, so it is not visible and is not part of this step.

Original rewire, already applied on the live node:
  - exec in from Delay `then`, exec out to the Print String.
  - Target from Get Blackboard (whose Target is the event's Owner Controller).
  - Key Name from Make Literal Name `bReceivingDamage`.
  - Bool Value unchecked.
- Compile, save.

**Step 4 — Light-only damage (AI1-03).** Done 2026-10-18. Export confirms `bLightAttackActive`, Damage 25, and Set Value as Bool `bReceivingDamage` true on the object cast path. Original clicks, already applied:
1. My Blueprint → Variables → + → name `bLightAttackActive`, type Boolean, default unchecked. Compile once so the variable appears.
2. Find event `IA_Light_Attack` (Y ≈ −2672). Its Started pin goes into a Branch. That Branch's False output goes to Set `IsAttacking`. Alt+left click the wire from Set `IsAttacking` `then` to Weapon to Hand. Insert Set `bLightAttackActive` (checked) between them.
3. On that same chain, find the light Play Montage's On Completed path. Set `IsAttacking` false → Set `AttackIndex` 0 → Weapon to Back. Insert Set `bLightAttackActive` (unchecked) right after Set `IsAttacking` false.
4. Find custom event `ResetState`. Alt+click the wire from its `then` to `SetState`. Insert Set `bLightAttackActive` (unchecked) between them.
5. Find the WeaponHitbox overlap → Cast to `BP_BaseEnemy` → Print String `Hitbox detectada`. From that Print String's `then`, add a Branch (Rama). Condition = Get `bLightAttackActive`. Wire True → the existing `E_Decrease_Health` execute. **Change its Damage from 100 to 25** (decision B). Leave False empty.
6. From `E_Decrease_Health` `then`: Cast To AIController. Its Object input is the `BP_BaseEnemy` cast's As BP Base Enemy → Get Controller. From As AIController → Get Blackboard → Set Value as Bool. Key Name = Make Literal Name `bReceivingDamage`, Bool Value checked.
7. Compile, save.

Do not use `bSaveLightAttack` or `IsAttacking` as the gate. Those are a combo buffer and a shared state, and both are true for heavy attacks too. Do not touch the `IA_Heavy_Attack` chain.

Step 4 saved the flat 25. The owner replaced that on 2026-10-18 with 15 / 15 / 19, and that Select is saved. The enemy still stops for 0.6 s, then prints `Enemigo: ya no recibe daño`, after each hit that removes health. Two full combos leave 2 health. The next light hit kills.

**Step 5 — Enemy death (AI1 cleanup, needed before AI 2 counts living enemies).** Done 2026-10-18. Export confirms BeginPlay binds `E_Dead`, Attack goes to the sphere trace, `bIsDead` is set true, and Stop Logic Reason is `Dead`. Original clicks:
1. Add Event BeginPlay (Evento BeginPlay). Move the existing **Bind Event to E_Dead** node there: BeginPlay → Bind Event to E_Dead. Its Target stays `BPC_E_Health`, and its Event stays the `Enemy_Death` red pin.
2. In Event `Attack`, wire the event's `then` directly to the Sphere Trace node. The bind is no longer in this chain.
3. On `Enemy_Death`, after Play Anim Montage add these nodes in order:
   - Get Controller → Cast To AIController → Get Brain Component → Stop Logic (Reason: `Dead`).
   - Get Character Movement → Disable Movement.
   - Get Capsule Component → Set Collision Enabled (No Collision).
   - Set Life Span 3 on self.

   These are engine nodes. No new numbers are locked, except that the life span is a cleanup choice and not gameplay. Record it if you use a different value.
4. Add a boolean `bIsDead` on `BP_BaseEnemy`. Set it true at the start of `Enemy_Death`. AI 2 uses it to count living enemies.
5. Compile, save.

**Step 6 — Attack montage (cosmetic).** Closed 2026-10-18 with Montage To Play left empty. The enemy mesh `SK_SciFiWarrior02` uses `UE4_Mannequin_Skeleton`. No montage in the project uses that skeleton.

**Step 7 — Health component guard.** Done 2026-10-18. `E_Decrease_Health` starts with a Branch whose condition is Get `E_Health` > 0. True goes to the existing subtract. False is empty.

**Step 8 — Player receives enemy damage (needed for AI 3 and for AI 1's attack to matter).** Done 2026-10-18. Export: Event AnyDamage `then` calls `BPC_Health.Decrease_Health`, and the event Damage pin feeds that Damage pin. The debug key remains 25. The light Select remains 15 / 15 / 19. The number that arrives is the 10 `BP_BaseEnemy` already sends.

**Step 9 — Owner PIE checks.** Run the editor tests in `WORK_ITEMS.md` that say Ready. Write each result in the result log. Set an AI1 row to Done only after its checks pass.

### Owner decisions (resolved 2026-10-14)

The owner chose to shrink the orbit and lower the damage. `AI_REQUIREMENTS.md` already holds the new numbers, which are locked from now on.

- **A. Orbit vs attack range.** The old band 320–480 kept the enemy outside the attack distance of 220, so it almost never attacked. New values:
  - Preferred orbit radius: **180**.
  - Inner limit: **150**.
  - Outer limit: **210**.
  - Rotation step: **40°** per service tick. That is still the locked strafe of 250 units/s: 250 × 0.5 s = 125 units of arc, and 125 / 180 rad ≈ 40°.
  - Unchanged: attack distance 220, cooldown 3, defend 600, detection 1500.

  Result: while orbiting, the enemy is always inside attack range, so it attacks each time the 3 second cooldown is ready. Defend still has higher priority, so roughly every 7.5 s it defends instead. Spacing check: at 150 units between centers, the two capsules (34 + 35) leave about 80 units of gap, so it does not touch the player. `BP_BaseEnemy` Attack traces 200 from the enemy center, which reaches the player capsule at up to about 234, so attacks at 210 still connect.
- **B. One-hit kill.** The light damage on the player's `E_Decrease_Health` call changed from 100 to **25** on 2026-10-14. Enemy `E_Health` stays 100. On 2026-10-18 the owner replaced that flat 25 with combo damage **15 / 15 / 19** (the finisher was going to be 20; the owner set 19 so two combos do not kill). Two full combos leave 2 health. The next light hit kills. The 0.6 s hit stun still shows after each hit that removes health. The Select is saved.

**Step 0b — Let Move To reach the 180 point.** Done 2026-10-14. Export shows `bReachTestIncludesAgentRadius=(DefaultValue=False)` on `BTTask_MoveTo_0`. Agent PIE: at game time 98 s distances were 170 and 154; at 152 s they were 161 and 170, and both positions and `OrbitLocation` had changed. Attack lines continued. No `Accessed None`. Original click sequence, already applied:
1. Open `BT_EnemyIA`. Select the **Move To** whose Blackboard Key is `OrbitLocation` (orbit sequence, the fourth Selector child). Do not select the roam task.
2. In Details, uncheck **Reach Test Includes Agent Radius**. Leave Acceptable Radius at `5`. Leave Allow Strafe and Observe Blackboard Value on.
3. Compile, save.
4. Agent check: `export_ai.py`, then confirm `BT_EnemyIA.t3d` `BTTask_MoveTo_0` has `bReachTestIncludesAgentRadius` false (or the property serialized off). Then PIE with `teleport.flag` and `pie_sample.py`. `DistanceToTarget` should move into 150–210, and `OrbitLocation` should change between samples. `Enemigo: va a atacar` should still appear about every 3 s per enemy.

**Step 0 — Apply decision A (orbit numbers).** Done 2026-10-14. Export confirmed 150 / 210 / 180 / 40. PIE did not pass; see Step 0b. Original click sequence, already applied:
1. Open `BTService_LocatePlayer` (Content/ThirdPerson/Blueprints/EnemigoIA). In the Event Graph, find the orbit math after Set Blackboard Value as Float (`DistanceToTargetKey`).
2. On the **Less** node (`<`), where the distance is pin A, change pin B from `320` to `150`.
3. On the **Greater** node (`>`), where the distance is pin A, change pin B from `480` to `210`.
4. On the **Multiply** node (vector × float, after Normalize), change the float from `400` to `180`.
5. On the **Rotate Angle Axis** node, change Angle Deg from `18` to `40`. Leave Axis at (0, 0, 1).
6. Compile, save.
7. Agent check: run `export_ai.py`, then `summarize.py BTService_LocatePlayer`. Then confirm with `Select-String -Path Intermediate\inspect\live\_BTService_LocatePlayer.txt -Pattern "=150|=210|=180|=40"`: you should see each of the four new values. Search again for `=320|=480|=400|=18\.` and expect no hits.
8. PIE check: teleport the player with `teleport.flag`, then `pie_sample.py`. `DistanceToTarget` should settle around 150–210, with `Enemigo: va a atacar` in the log about every 3 s.

Decision B's flat 25 was replaced on 2026-10-18 by the Select 15 / 15 / 19.

If PIE shows the enemy pushing the player or jittering at 150–210, do not tune further. Record what you saw and escalate.

### After AI 1: AI 2 hostage build recipe

The specs and numbers are in `AI_REQUIREMENTS.md` → AI 2. Create all assets in `Content/ThirdPerson/Blueprints/Hostage/` (new folder).

1. `BB_Hostage` (Blackboard). Keys:
   - `SelfActor` (Object)
   - `PlayerActor` (Object, base class Actor)
   - `DistanceToPlayer` (Float)
   - `bMustFlee` (Bool)
   - `bWaiting` (Bool)
   - `bEnemyNear` (Bool)
   - `FleeLocation` (Vector)
2. `BP_HostageController` (parent AIController). BeginPlay → Run Behavior Tree `BT_Hostage`.
3. `BP_Hostage` (parent Character). Use any existing humanoid mesh from `Characters/` with the Mannequin anim blueprint.
   - Set AI Controller Class to `BP_HostageController` and Auto Possess AI to Placed in World or Spawned.
   - Turn on Orient Rotation to Movement.
   - Add a boolean `bAccompanying` (the zones read it). Also add the function `IsAccompanying` → returns `not bMustFlee and not bWaiting and DistanceToPlayer <= 600`. Read those keys from its own blackboard.
4. `BTService_HostageSense` (Blueprint, parent BTService_BlueprintBase). Variables: Blackboard Key Selectors `PlayerKey`, `DistanceKey`, `EnemyNearKey`, all Editable en instancia. On Receive Tick AI:
   1. Get Player Character 0 → set `PlayerKey`.
   2. Distance (pawn, player) → set `DistanceKey`.
   3. Get All Actors Of Class `BP_BaseEnemy` (and `BP_ChargerEnemy` once it exists). If any one is not `bIsDead` and within 800 of the pawn, set `EnemyNearKey` true; otherwise false.
5. `BT_Hostage`, a root Selector with `BTService_HostageSense`. Children left to right:
   1. Sequence [BB `bMustFlee` Is Set, abort Self]: Move To `FleeLocation` → `BTTask_HostageArrive`. That task sets `bMustFlee` false and `bWaiting` true, then Finish Execute success.
   2. Sequence [BB `bWaiting` Is Set, and BB `DistanceToPlayer` <= 400, abort Lower Priority]: `BTTask_ClearWaiting`. That task sets `bWaiting` false, then Finish Execute success.
   3. Sequence [BB `bWaiting` Is Set, abort Self]: Rotate to face `PlayerActor` → Wait 0.5. The hostage stays at the flee point until branch 2 fires.
   4. Sequence [BB `bEnemyNear` Is Set, abort Both]: Rotate to face `PlayerActor` → Wait 0.5.
   5. Sequence [BB `DistanceToPlayer` > 500, abort Lower Priority]: Move To `PlayerActor` with Acceptable Radius 300.
   6. Wait 0.5 (idle).

   Branch order matches the spec: flee, wait (branches 2 and 3), hold, follow, idle.

   **No Force Success under the Selector.** Every Blueprint task must call Finish Execute on every path.
6. `BP_CombatZone` (Actor). Components:
   - Box `Trigger`.
   - Box or static mesh `EntranceBlocker` with collision disabled at start.
   - Variable `FleePoint` (Target Point, instance editable).
   - Variable `LivingEnemies` (Integer).

   Behavior:
   - BeginPlay: count overlapping `BP_BaseEnemy` actors and store the count. Bind each enemy's `BPC_E_Health` `E_Dead` to a custom event that decrements the count. When the count reaches 0, disable the blocker and set the hostage's `bWaiting` true.
   - Player Begin Overlap with count > 0: enable the blocker collision. If the hostage `IsAccompanying`, set the hostage BB `FleeLocation` = `FleePoint` location and `bMustFlee` true.
7. `BP_HostageSpawnZone` (Actor). Components and variables:
   - Box `Trigger`.
   - `EnemyClass` (class of Character, default `BP_BaseEnemy`).
   - `SpawnCount` (int 2).
   - `bSpawned` (bool).
   - Optional `TargetZone` (`BP_CombatZone`) to register the spawned enemies.

   On player overlap, if not `bSpawned` and the hostage `IsAccompanying`: spawn `SpawnCount` enemies at points inside the box on the navmesh, then set `bSpawned`.
8. Place the actors inside the `NavMeshBoundsVolume` (origin 1330, 2300; extent 1725 × 1250): one hostage near `PlayerStart`, one `BP_CombatZone` with a Target Point outside it, and one `BP_HostageSpawnZone`. **Write their actor labels in this file.**
9. Add the new asset paths to `Intermediate/inspect/extra_paths.txt`, so `export_ai.py` exports them.

### After AI 2: AI 3 charger build recipe

The specs are in `AI_REQUIREMENTS.md` → AI 3. Put the assets in `Content/ThirdPerson/Blueprints/Charger/`.

1. `BB_Charger` keys:
   - `SelfActor`
   - `TargetActor` (Object)
   - `DistanceToTarget` (Float, default 100000)
   - `bCharging` (Bool)
   - `bRetreat` (Bool)
   - `RetreatLocation` (Vector)
   - `ChargeLocation` (Vector)
2. `BP_ChargerController`: BeginPlay → Run Behavior Tree `BT_Charger`.
3. `BP_ChargerEnemy`: a child Blueprint of `BP_BaseEnemy`, so it inherits health and death. Override AI Controller Class to `BP_ChargerController`. Its damage takes light **and** heavy hits, so the player hitbox needs a second cast. Escalate before editing the player again.
4. Service: reuse `BTService_LocatePlayer` with the radius key bound to a `DetectionRadius` key (1800), or copy it without the orbit math.
5. `BT_Charger` root Selector, left to right:
   1. Sequence [`bCharging` Is Set, abort Self]: `BTTask_Charge`. It sets max walk speed 900 and moves to `ChargeLocation` with acceptance 180. A time limit decorator of 1.0 s goes on this task. On end it restores speed 600, clears `bCharging`, sets `bRetreat`, then Finish Execute. Contact damage: during the charge, sphere trace 200 → Apply Damage to the player once per charge. The existing amount is 10, so use 10 and not 15.
   2. Sequence [`DistanceToTarget` in 250–700 (two Blackboard decorators: >= 250 and <= 700), Cooldown 2]: Rotate to face → Wait 0.8 → a task that sets `ChargeLocation` = player location and `bCharging` true.
   3. Sequence [`bRetreat` Is Set, abort Self]: a task that computes `RetreatLocation` = player + Normalize(self − player) × 1000 → Move To `RetreatLocation` → Wait 2 → a task that clears `bRetreat`.
   4. Sequence [`TargetActor` Is Set and `DistanceToTarget` > 700]: Move To `TargetActor` with Allow Strafe off.
   5. Roam: reuse `BTTask_Roam` → Wait 3.
6. Place one `BP_ChargerEnemy` in the navmesh area and record its label here.

### Files touched in this pass

- `Content/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA` (owner removed Force Success from Attack, 2026-10-14)
- Owner edits saved earlier on 2026-10-13/14:
  - `BTTask_Defend` (Delay + Finish Execute)
  - `BTTask_Attack` (Is Not Valid → Finish Execute false)
  - `BP_IAController` (1500)
  - `BTTask_Roam` (debug prints)
- `Tools/UnrealPython/*.py` (new; agent tooling, tracked because `Intermediate/` is git-ignored)
- `docs/GOVERNANCE.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/AI_REQUIREMENTS.md`
- `docs/WORK_ITEMS.md`
- `docs/HANDOFF.md`

## History

### 2026-10-18 — Player AnyDamage saved

Export, dirty packages none. Event AnyDamage calls `BPC_Health.Decrease_Health`. The event's Damage pin is wired to that node's Damage pin. Damage Type, Instigated By, and Damage Causer are empty. The debug key is still 25. The light Select is still 15 / 15 / 19. Next step is the owner's play on `ThirdPersonMap`.

### 2026-10-18 — FA_1 hit window saved

Export, dirty packages none. `FA_1_Montage` Montage Notify `EnableHitbox` triggers at 0.08 s. `DisableHitbox` triggers at 0.34 s. EdAttack stays at 0.39 s and AttackFinished stays at the end. Swing 1 can now connect for 15 damage. Next decision is Step 8, player AnyDamage. Ask the owner before editing the player.

### 2026-10-18 — Combo damage saved as 15 / 15 / 19

Export, dirty packages none. Live Play Montage `then` sets `LightSwingIndex` from `AttackIndex`, then the Branch increments `AttackIndex`. Select Index is `LightSwingIndex`. Option 0 = 15, Option 1 = 15, Option 2 = 19. That return value is the Damage pin of `E_Decrease_Health`. The owner set 19 instead of 20 so two full combos leave the enemy at 2 health. `FA_1_Montage` still has no EnableHitbox. Next click is that montage.

### 2026-10-18 — Light hitbox enable saved, combo damage chosen

Export: the live light Play Montage On Notify Begin feeds Switch on Name at (4672, −2896). `EnableHitbox` sets `WeaponHitbox` to Query Only. `DisableHitbox` sets No Collision. Dirty packages were none. The owner chose light combo damage 15 / 15 / 20. `E_Decrease_Health` still has Damage 25. `FA_1_Montage` still has no EnableHitbox notify. Next click is `LightSwingIndex` plus Select on that Damage pin.

### 2026-10-18 — Light notify switch saved without the enable branch

Export: light Play Montage On Notify Begin and Notify Name feed a new Switch on Name at (4672, −2896) with pins `EnableHitbox` and `DisableHitbox`. `DisableHitbox` goes to Set Collision Enabled No Collision on `WeaponHitbox`. `EnableHitbox` has no wire and there is no Query Only node in that chain, so the hitbox still never turns on. Next click: add that node.

### 2026-10-18 — Light attack never enables the hitbox

`Weapon` is No Collision now and the owner still saw no `Hitbox detectada`. The light Play Montage's On Notify Begin is unwired. The old Switch on Name chain that enables `WeaponHitbox` has no exec input. `FA_1_Montage` has no EnableHitbox notify. `FA_2_Montage` and `L_FA_3_Montage` have one. No asset changed.

### 2026-10-18 — Sword mesh blocks the enemy

Playtest: the longsword pushes the enemy and the hit does not register. `Weapon` is Query and Physics, Block All Dynamic, Block on Pawn. `WeaponHitbox` is a 32-unit box, Overlap on Pawn, and No Collision until the `EnableHitbox` notify. The pasted `RigHierarchy.GetController` node has no wires and is not the hit path.

### 2026-10-18 — Health guard saved

`BPC_E_Health` export: `E_Decrease_Health` starts with a Branch on `E_Health` > 0. True continues to the subtract. False is empty. Next decision is whether to add Event AnyDamage on the player.

### 2026-10-18 — Death reason saved, attack montage left empty

Stop Logic Reason is `Dead`. Montage To Play stays empty: `SK_SciFiWarrior02` uses `UE4_Mannequin_Skeleton`, and no project montage uses that skeleton. Next click is the health guard on `BPC_E_Health`.

### 2026-10-18 — Enemy death chain saved, Reason empty

`BP_BaseEnemy` export: BeginPlay binds `E_Dead` to `Enemy_Death`. Attack goes straight to the sphere trace. `Enemy_Death` sets `bIsDead`, plays the death montage, stops the brain, disables movement, turns capsule collision off, and sets life span 3. Stop Logic's Reason pin has no text.

### 2026-10-18 — Light damage wire saved

`BP_ThirdPersonCharacter` export: light attack sets `bLightAttackActive`, the hitbox Branch calls `E_Decrease_Health` with Damage 25, then an object Cast To AIController (Get Controller from the enemy) writes blackboard `bReceivingDamage` true. Heavy attack is unchanged. Next click is Step 5.

### 2026-10-14 — HitSun error object is not on the graph

A fresh export after the owner moved Set Value as Bool to (880, −352) shows that node in the Event Graph `Nodes` list with no `ErrorType`. The `ErrorType=1` Set Value as Bool and the extra Set Blackboard Value as Bool are serialized objects that are absent from that list, which is why they are not behind the node in the editor. Step 3 is done. Next click is Step 4.

### 2026-10-14 — HitSun rewire is live, old error node remains

The owner added a new Set Value as Bool and wired Delay → that node → Print String → Finish Execute. Export shows no `ErrorType` on that node. The old Set Value as Bool is still in the graph with `ErrorType=1` and no wires, plus an unwired Set Blackboard Value as Bool. Next click is to delete those two nodes.

### 2026-10-14 — HitSun compile did not clear the badge

The owner compiled and saved `BTTask_HitSun`. Dirty packages were none. The export still has `ErrorType=1` on Set Value as Bool and no `ErrorMsg`. Wiring is unchanged. Next click is the Step 3 rewire.

### 2026-10-14 — Roam debug nodes removed, not play-tested

The owner cleaned `BTTask_Roam` and asked the agent not to test it. `ping.py` reported no dirty packages. Next click is Step 3.

### 2026-10-14 — Defend accent saved, not play-tested

The owner set `BTTask_Defend` Print String to `Enemigo: se está defendiendo` and asked the agent not to test it. `ping.py` reported no dirty packages. Next click is Step 2.

### 2026-10-14 — Step 0b: enemies enter the band and circle

The orbit Move To now has Reach Test Includes Agent Radius off. Agent PIE after teleport: both enemies stayed in 150–170, moved around the player, and the orbit point changed between samples 54 seconds apart. Attack and defend lines kept printing. No `Accessed None`. Next click is Step 1.

### 2026-10-14 — Step 0 saved, orbit does not enter the band

`BTService_LocatePlayer` export has Less 150, Greater 210, Multiply 180, Rotate Angle Axis 40. Old pins are gone. Dirty packages were none. Agent PIE with the player teleported 450 units from enemy 0: both enemies closed in, then froze. Samples at game time 87s and 133s were identical: distances 213 and 145, speeds 0, `OrbitLocation` on the 180 circle `(2265,3486)` and `(2246,3465)`. Attack and defend lines kept printing (about every 3 s per enemy). No `Accessed None`. The 40° branch never ran because Move To already counted them as arrived. Next edit is Step 0b, not a new radius.

### 2026-10-14 — Owner decisions A and B resolved

The owner chose a smaller orbit (radius 180, band 150–210, 40° step at the same 250 u/s strafe) so the enemy orbits inside the attack range of 220. The owner also chose light damage 25 against health 100, so it takes 4 hits and hit stun is visible. Only docs changed. The assets still hold the old values until Step 0 and Step 4 are done.

### 2026-10-14 — Root cause of "enemies do not walk" found and fixed

Comparing with `main`'s original tree showed the Force Success decorator on `BTTask_Attack` directly under the Selector. It ended every pass through the tree at Attack, so Orbit and Roam never ran. The owner removed it. Agent PIE then verified that roam, orbit, defend, and attack all work. Earlier the owner added Delay + Finish Execute to Defend, Finish Execute false on Attack's Is Not Valid path, and set the controller to 1500. The tooling scripts moved to `Tools/UnrealPython/`.

### 2026-10-13 — Full orbiter audit with agent-run PIE

Re-exported all orbiter assets and the player character. Ran short Play In Editor sessions from Python. Found that the Defend task never finishes. Agent height turned out not to be a blocker. No asset changed. (The claim "Roam never moves" from this audit was caused by Force Success, found on 2026-10-14.)

### 2026-10-13 — Orbiter tree saved, damage gate still open

Re-exported the Selector, the service, the three tasks, the health component, the enemy, and the player character. The five branches, the orbit math, and the three Spanish prints are in the assets. Player damage still does not execute. No Play In Editor test.

### 2026-10-11 — Enemy tree inspected, blackboard keys added

Connected to the open Terreno editor. Recorded the live `BT_EnemyIA` structure. Saved `bReceivingDamage`, `DistanceToTarget`, and `OrbitLocation` on `BB_EnemyIA`. No behavior-tree branches were rewired.

### 2026-10-11 — Decisions locked

The owner delegated the open choices and supplied `FE-OV 1.docx`. Locked Behavior Trees, the orbiter tuning, the hostage zone rules, and a second enemy (charger) required by the rubric. No Blueprint, map, or config asset was modified.

### 2026-10-11 — Governance created

Created the English agent docs from the owner brief and from files present in the repository. No Blueprint, map, or config asset was modified.

# AI requirements

Distances are Unreal units (centimeters). Every numeric value in "Locked decisions" is a **Decision** the owner delegated on 2026-10-11. Expose each one as an editable variable on the Blackboard or the actor, initialized to the value below.

Existing enemy assets are listed in `PROJECT_CONTEXT.md`. What is already saved is in `HANDOFF.md`, which was exported on 2026-10-14. The numbers below stay the target.

Agent PIE showed the orbiter's movement branches working, but the owner has not run the acceptance checks, so none is done yet. Inspect the current graph before adding a second damage path or a second task that does the same job.

On 2026-10-14 the owner changed two orbiter values. Both are **Decisions** now (see `HANDOFF.md` → Owner decisions):
- Orbit: radius 180, band 150–210 (was 400, band 320–480). The old band kept the enemy outside the attack distance of 220.
- Light damage: combo **15 / 15 / 19** (owner choice 2026-10-18; the finisher was drafted as 20, then set to 19 so two combos do not kill). Was a flat 25, and before that 100. With health 100, one full combo leaves 51. Two full combos leave 2. The next light hit kills.

The AI 3 contact damage resolves to 10, the existing `BP_BaseEnemy` hit. The 15 fallback below does not apply.

The professor's rule: each AI is a Behavior Tree, not a pile of conditionals. Tree shape is specified under each AI.

## AI 1 — Orbiter

Asset base: `BP_BaseEnemy`, `BP_IAController`, `BB_EnemyIA`, `BT_EnemyIA`.

Board status stated by the owner: Done. The integrations below stay open until an editor test checks them off.

This is enemy one of the two required by the rubric. It orbits at melee range and takes damage only from light attacks.

### Tree

`BT_EnemyIA`, highest priority first:

1. Hit stun, while Blackboard `bReceivingDamage` is true. Task lasts 0.6 seconds. On finish, print the damage-end line and clear the key.
2. Defend, when the player is within 600 units, the enemy is not attacking, and at least 6 seconds passed since the last defend. Task lasts 1.5 seconds.
3. Attack, when the player is within 220 units and the attack cooldown of 3 seconds is ready.
4. Orbit, when the player is detected inside 1500 units.
5. Roam, using the existing `BTTask_Roam` if it already wanders. If it does something else, keep that task and add a new orbit task. Do not delete roam until the editor shows what it does.

`BTService_LocatePlayer` writes the player actor and the distance. It does not choose the branch.

### Orbit

- Preferred radius: 180. (Owner decision 2026-10-14; was 400.)
- Inner limit: 150. Closer than this, strafe outward. (Was 320.)
- Outer limit: 210. Farther than this, and still detected, move inward. (Was 480.)
- The whole band sits inside the attack distance of 220, so the orbiter attacks whenever the cooldown allows.
- Strafe speed while inside the band: 250 units per second. With the service's 0.5 s tick, this is a 40° rotation step at radius 180 (it was 18° at radius 400).
- Face the player while orbiting.
- Do not stop on the player's capsule.

No defend animation was found. The defend task faces the player and does not move. If a defend montage is added later, play it from that task only.

### Damage

Only a player light attack reduces this enemy's health. Heavy attacks and any other damage source are ignored.

Use the existing path. `SaveLightAttack_AN` calls `SaveLightAttack` on `BP_ThirdPersonCharacter`. `bSaveLightAttack` is a combo-input buffer, not a light-hit window. `ResetState_AN` calls `ResetState`, and that event currently goes to `SetState`. `BPC_E_Health.E_Decrease_Health` subtracts its Damage argument and fires `E_Dead` when health reaches 0 or less. The light-attack window uses `bLightAttackActive`, set when the light attack starts and cleared from the light montage's On Completed and from `ResetState`. Do not add a second health system. `BP_BaseEnemy` Attack applies 10 damage with a sphere of radius 200. That is this enemy hitting another actor. AI 3 contact damage reuses 10. Do not change it while building the orbiter.

Light combo damage (owner choice 2026-10-18), by the swing that is playing, not by the already-incremented `AttackIndex`:

| Swing | `LightSwingIndex` | Damage |
| --- | --- | --- |
| 1 | 0 | 15 |
| 2 | 1 | 15 |
| 3 | 2 | 19 |

One full combo removes 49. Two full combos remove 98 and leave 2 health. The next light hit kills. A heavy hit is still ignored.

A light hit that actually removes health sets `bReceivingDamage` for the hit-stun branch. A rejected heavy hit does not.

Do not change max health (100). Do not invent a damage number other than 15, 15, and 19.

### Print String

Print String nodes, 2 second duration, in Spanish:

| Moment | Text |
| --- | --- |
| Attack task starts | `Enemigo: va a atacar` |
| Defend task starts | `Enemigo: se está defendiendo` |
| Hit-stun task finishes | `Enemigo: ya no recibe daño` |

These three lines are required. Do not add more required lines on this enemy.

## AI 2 — Hostage escort

No hostage asset was found by file name. Create `BP_Hostage`, `BB_Hostage`, `BT_Hostage`, and an AI controller that runs that tree only.

The hostage is not the rubric's second enemy.

### Tree

`BT_Hostage`, highest priority first:

1. Flee, while `bMustFlee` is true. Move to the zone's flee point, then stay there and set `bWaiting`.
2. Wait, while `bWaiting` is true. Clear it when the player comes within 400 units, then go back to follow.
3. Hold, when any living enemy is within 800 units of the hostage. Stay put and face the player. Do not follow into the fight.
4. Follow, when the player is farther than 500 units. Move until within 300 units, then stop.
5. Idle, while the player stays between 300 and 500 units and no higher branch is active.

### Zones

Create `BP_CombatZone` as a box trigger. A zone is populated while its living enemy count is greater than 0. Count enemies that start inside it and enemies spawned for it.

When the player begins overlap and the zone is populated, enable that zone's entrance blocker so the player cannot leave. Disable the blocker when the living count reaches 0.

If the hostage is accompanying at that moment, set `bMustFlee`. Accompanying means the escort is not already fleeing or waiting, and the hostage is within 600 units of the player.

The flee point is a Target Point referenced by the zone, placed outside the volume. There is no named landmark yet. Place at least one `BP_CombatZone` in reachable space on `ThirdPersonMap` and record its label in `HANDOFF.md`.

### Conditional spawn

Create `BP_HostageSpawnZone` as a box trigger.

On player begin overlap, spawn only when the hostage is accompanying. Spawn once per zone. Default count is 2, using the enemy class set on the zone.

- First zone class: `BP_BaseEnemy`.
- Second zone class, if a second volume is placed: `BP_ChargerEnemy`.

If the player enters without the hostage, spawn nothing. Place at least the first zone and record its label.

## AI 3 — Charger

Course requirement: two enemies with different advanced AI. This is the second enemy. New assets: `BP_ChargerEnemy`, `BB_Charger`, `BT_Charger`, and a controller that runs that tree only.

It does not orbit. It takes both light and heavy damage, so the player's two attack types both matter. It does not use the three orbiter Print Strings.

### Tree

`BT_Charger`, highest priority first:

1. Charge, while `bCharging` is true. Move at 900 units per second for at most 1 second, or until within 180 units. Then clear the charge and set retreat.
2. Windup, when the player is between 250 and 700 units and the 2 second cooldown is ready. Face the player and wait 0.8 seconds, then set `bCharging`.
3. Retreat, while `bRetreat` is true. Move away until the player is at least 1000 units away, then clear retreat and wait 2 seconds before another chase.
4. Chase, when the player is detected inside 1800 units and farther than 700 units. Run straight at the player. No strafe orbit.
5. Roam, when the player is outside detection.

Contact during the charge applies damage to the player. Use the damage amount this project already uses for an enemy hit. If no such amount exists, use 15 and record that in the handoff.

## Out of this AI assignment

Do not implement these unless a work item is added:

- Hammer pickup and the gate that requires it.
- Character progression.
- The post-escape survival timer and the formula that turns remaining enemies into waves.
- Dialogue NPCs, menus, save games, and the other non-AI rubric rows.
- Player combat animations, except the light-attack flag the orbiter must read.

## Acceptance checks

An item is done only after Play In Editor on `ThirdPersonMap` shows the behavior. Updating a document is not acceptance. Partial checks while a slice is still open are in `WORK_ITEMS.md` under Editor tests. A pass there does not set Done.

| Check | Pass condition |
| --- | --- |
| Tree | Stopping the Behavior Tree stops the decision. The character Blueprint has no Tick branch that chooses orbit, attack, defend, chase, flee, or follow. |
| Orbit | After detection, the orbiter stays near 180 units (150–210) and circles. It does not overlap the player capsule. It attacks about every 3 seconds while orbiting. |
| Light damage | A light attack reduces orbiter health. A heavy attack does not. |
| Prints | The three Spanish lines appear on attack start, defend start, and hit-stun end. |
| Calm follow | With no enemy inside 800 units, the hostage stops around 300 units from the player. |
| Zone | Entering a populated `BP_CombatZone` turns on the entrance blocker, and the hostage runs to that zone's flee point. |
| Return | After the zone count hits 0, the blocker turns off. The hostage waits until the player is within 400 units, then follows again. |
| Spawn | The hostage spawn zone spawns only while the hostage is accompanying. A pass without the hostage spawns nothing. |
| Second enemy | The charger uses `BT_Charger`, rushes in a line, retreats, and still takes heavy-attack damage. |

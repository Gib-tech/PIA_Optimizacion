"""Negative controls: sealed door, unpowered hammer and light hit cannot create cracks."""
import unreal,json,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
door=d.get_editor_property('Baliza1').get_editor_property('Door')
def flag(a,k,v):lib.call_method('SetBoolPropertyByName',(a,k,v))
for k,v in [('IsAttacking',True),('bLightAttackActive',False),('bIsHammerEquipped',True),('bHammerUpgraded',True)]:flag(p,k,v)
initial=door.static_mesh_component.get_material(0)
def unchanged():
 assert door.get_editor_property('Health')==50 and not door.get_editor_property('bCracked') and door.static_mesh_component.get_material(0)==initial
unreal.GameplayStatics.apply_damage(door,25,None,p,None);unchanged()
flag(door,'bUnlocked',True);flag(p,'bHammerUpgraded',False);unreal.GameplayStatics.apply_damage(door,25,None,p,None);unchanged()
flag(p,'bHammerUpgraded',True);flag(p,'bLightAttackActive',True);unreal.GameplayStatics.apply_damage(door,25,None,p,None);unchanged()
flag(door,'bUnlocked',False)
for k,v in [('IsAttacking',False),('bLightAttackActive',False),('bIsHammerEquipped',False),('bHammerUpgraded',False),('bIsSwordEquipped',True)]:flag(p,k,v)
result={'passed':True,'sealed_door_does_not_crack':True,'unpowered_hammer_does_not_crack':True,'light_hit_does_not_crack':True}
with open(os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/door_crack_guard_assertions.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('DOOR_CRACK_GUARDS_PASSED')

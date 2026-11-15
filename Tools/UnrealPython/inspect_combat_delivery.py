import unreal
root='/Game/ThirdPerson/Blueprints/EnemigoIA/'
for path in [root+'ataque_enemigo',root+'enemigo_lastimado',root+'enemigo_lastimado1',root+'Enemy_Death',root+'Enemy_Death_Montage']:
    asset=unreal.load_asset(path)
    unreal.log('COMBAT_ANIMATION '+path+' '+asset.get_class().get_name()+' length='+str(asset.get_play_length())+' skeleton='+str(asset.get_editor_property('skeleton').get_path_name()))
enemy=unreal.get_default_object(unreal.load_class(None,root+'BP_BaseEnemy.BP_BaseEnemy_C'))
unreal.log('COMBAT_MESH '+enemy.mesh.skeletal_mesh.get_path_name()+' anim='+str(enemy.mesh.anim_class))
unreal.log('COMBAT_SKELETON '+enemy.mesh.skeletal_mesh.get_editor_property('skeleton').get_path_name())
player=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C'))
for c in player.get_components_by_class(unreal.PrimitiveComponent):
    unreal.log('PLAYER_COMPONENT '+c.get_name()+' '+c.get_class().get_name())
for asset in unreal.EditorAssetLibrary.list_assets('/Game/ThirdPerson',recursive=True):
    if 'abp' in asset.lower() or 'animblueprint' in asset.lower():unreal.log('ANIMBP '+asset)

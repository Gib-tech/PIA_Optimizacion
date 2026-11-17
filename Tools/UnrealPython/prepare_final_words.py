"""Add the final horde and presentation fields, preserving the existing map."""
import unreal,os,sys
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());sys.path.insert(0,os.path.join(root,'Tools/UnrealPython'))
from delivery_save_schema import FIELDS
from generate_progression_graphs import DIRECTOR,ZONE,HERO,HOSTAGE
from generate_combat_graphs import BASE,CHARGER
from generate_cinematic_graphs import CINEMA,HUD
lib=unreal.BlueprintEditorLibrary
def asset(cls):return unreal.load_asset(cls.rsplit('.',1)[0])
def add(bp,name,kind,editable=False):
    try:unreal.get_default_object(bp.generated_class()).get_editor_property(name)
    except Exception:
        if kind.startswith('class:'):typ=lib.get_class_reference_type(unreal.load_class(None,kind[6:]))
        elif kind.startswith('/'):typ=lib.get_object_reference_type(unreal.load_class(None,kind))
        elif kind in ['vector','rotator']:typ=lib.get_struct_type(unreal.load_object(None,'/Script/CoreUObject.'+kind.title()))
        else:typ=lib.get_basic_type_by_name(kind)
        assert lib.add_member_variable(bp,name,typ),(name,kind)
    if editable:lib.set_blueprint_variable_instance_editable(bp,name,True)
specs={
 DIRECTOR:{'Zona3':ZONE,'bOrderRevealed':'bool','bNarrativePaused':'bool'},
 ZONE:{'RequiredZone':ZONE,'AlternateEnemyClass':'class:'+BASE,'bMixedEnemies':'bool','bFinalStand':'bool','bRevelationStarted':'bool'},
 BASE:{'bFinalWordsPending':'bool','FinalPeersAlive':'int','EncounterZone':ZONE},
 CINEMA:{'RevealEnemy':BASE,'RevealedSequence':'string'},
 HUD:{'LastStatusText':'string','LastStatusSerial':'int','StatusUntil':'real','StatusNoticeVisible':'bool','DisplayedOrder':'string'},
 '/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager.BP_DeliverySaveManager_C':{'StatusSerial':'int'},
 '/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave.BP_DeliverySave_C':FIELDS,
}
for cls,fields in specs.items():
    bp=asset(cls)
    for name,kind in fields.items():add(bp,name,kind,name in ['Zona3','RequiredZone','AlternateEnemyClass','bMixedEnemies','bFinalStand'])
    lib.compile_blueprint(bp)
    if cls==ZONE:unreal.get_default_object(bp.generated_class()).set_editor_property('AlternateEnemyClass',unreal.load_class(None,CHARGER))
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def find(label):return next((a for a in sub.get_all_level_actors() if a.get_actor_label()==label),None)
def place(cls,label,pos):
    a=find(label) or sub.spawn_actor_from_class(cls,unreal.Vector(*pos))
    a.modify();a.set_actor_location(unreal.Vector(*pos),False,True);a.set_actor_label(label);a.set_folder_path('Mision/GuardiaFinal');a.set_editor_property('is_spatially_loaded',False)
    return a
z=place(unreal.load_class(None,ZONE),'Zona_03_GuardiaFinal',(0,-7550,150))
points=[place(unreal.TargetPoint,'Spawn_GuardiaFinal_'+str(i+1),pos) for i,pos in enumerate([(-350,-7700,100),(350,-7700,100)])]
z=find('Zona_03_GuardiaFinal')
for name,value in [('EnemyClass',unreal.load_class(None,BASE)),('AlternateEnemyClass',unreal.load_class(None,CHARGER)),('bMixedEnemies',True),('bFinalStand',True),('WaveCount',2),('RequiredZone',find('Zona_02_Embestidores')),('SpawnPoint1',points[0]),('SpawnPoint2',points[1]),('RefugePoint',find('Refugio_Rehen_08'))]:
    z.modify();z.set_editor_property(name,value)
z.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(950,400,240),False)
d=find('Director_Entrega');assert d;d.modify();d.set_editor_property('Zona3',z)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('FINAL_WORDS_FIELDS_AND_HORDE_READY')

import unreal,json
world_read=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs_read=unreal.GameplayStatics
for name_read in ['BP_DirectorEntrega','BP_SistemasComplementarios']:
 obj_read=gs_read.get_actor_of_class(world_read,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/'+name_read+'.'+name_read+'_C'))
 fields_read=['Zona1','Zona2','Zona3','Baliza1','Baliza2','Baliza3'] if name_read=='BP_DirectorEntrega' else ['Suministro1','Suministro2','Suministro3','Suministro4']
 for key_read in fields_read:
  act_read=obj_read.get_editor_property(key_read);unreal.log('MISSION_LOCATION '+key_read+' '+str(act_read.get_actor_location()))
host_read=gs_read.get_actor_of_class(world_read,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'));bb_read=host_read.get_controller().get_component_by_class(unreal.BlackboardComponent)
unreal.log('HOST_STATE '+str(host_read.get_actor_location())+' '+str(host_read.get_velocity())+' '+json.dumps({k:bb_read.get_value_as_bool(k) for k in ['bRescued','bAccompanying','bWaiting','bMustFlee']}))

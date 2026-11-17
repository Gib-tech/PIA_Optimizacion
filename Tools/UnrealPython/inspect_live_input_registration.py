import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world() or unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
for name in ['BP_DeliveryInterface','BP_SistemasComplementarios','BP_PlayerEntrega']:
 cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/'+name+'.'+name+'_C');cdo=unreal.get_default_object(cls);actor=unreal.GameplayStatics.get_actor_of_class(w,cls)
 for label,obj in [('cdo',cdo),('actor',actor)]:
  if not obj:continue
  values={}
  for key in ['auto_receive_input','input_priority','block_input','input_component','bInitialized','InventoryOpen','CamaraPrimera']:
   try:values[key]=str(obj.get_editor_property(key))
   except Exception:pass
  unreal.log('INPUT_REG '+name+' '+label+' '+json.dumps(values))
pc=unreal.GameplayStatics.get_player_controller(w,0)
if pc:unreal.log('INPUT_IGNORED '+str(pc.is_move_input_ignored())+' '+str(pc.is_look_input_ignored()))

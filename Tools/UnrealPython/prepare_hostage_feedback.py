"""Prepare original voice cues, cracked door material and Blackboard fixation memory."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/';E='/Game/ThirdPerson/Blueprints/EnemigoIA/';ART='/Game/ThirdPerson/Environment/Progression'
lib=unreal.BlueprintEditorLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
for path,fields in {R+'BP_DestructibleDoor':{'bCracked':'bool'},R+'BP_HUD_Entrega':{'HostageSpeaking':'bool','HostagePromptVisible':'bool','HostagePromptInRange':'bool','CurrentVoiceCue':unreal.SoundBase}}.items():
 bp=unreal.load_asset(path);cdo=unreal.get_default_object(bp.generated_class())
 for name,typ in fields.items():
  try:cdo.get_editor_property(name);continue
  except Exception:pass
  assert lib.add_member_variable(bp,name,lib.get_basic_type_by_name(typ) if isinstance(typ,str) else lib.get_object_reference_type(typ))
 lib.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp)
for name in ['BB_EnemyIA','BB_Charger']:
 bb=unreal.load_asset(E+name);entries=list(bb.get_editor_property('keys'))
 if not any(str(k.get_editor_property('entry_name'))=='bHostageLocked' for k in entries):
  entry=unreal.BlackboardEntry();entry.set_editor_property('entry_name','bHostageLocked');entry.set_editor_property('key_type',unreal.new_object(unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_Bool'),outer=bb));entries.append(entry);bb.set_editor_property('keys',entries)
 unreal.EditorAssetLibrary.save_loaded_asset(bb,only_if_is_dirty=False)
tasks=[]
for i in [1,2,3]:
 t=unreal.AssetImportTask();t.filename=os.path.join(project,'Tools/AudioSource/SW_HostageVoice_'+str(i)+'.wav');t.destination_path='/Game/ThirdPerson/Audio';t.destination_name='SW_HostageVoice_'+str(i);t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
t=unreal.AssetImportTask();t.filename=os.path.join(project,'Tools/ArtSource/UI/T_DoorCracks.tga');t.destination_path=ART;t.destination_name='T_DoorCracks';t.automated=True;t.replace_existing=True;t.save=True;tasks.append(t)
tools.import_asset_tasks(tasks)
texture=unreal.load_asset(ART+'/T_DoorCracks');texture.set_editor_property('srgb',False);texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);unreal.EditorAssetLibrary.save_loaded_asset(texture,only_if_is_dirty=False)
m=unreal.load_asset(ART+'/M_DoorCracked') or tools.create_asset('M_DoorCracked',ART,unreal.Material,unreal.MaterialFactoryNew())
ml=unreal.MaterialEditingLibrary;ml.delete_all_material_expressions(m)
def expr(cls,x,y):return ml.create_material_expression(m,cls,x,y)
def color(v,x,y):
 n=expr(unreal.MaterialExpressionConstant3Vector,x,y);n.constant=unreal.LinearColor(*v,1);return n
world=expr(unreal.MaterialExpressionWorldPosition,-1000,0)
mask=expr(unreal.MaterialExpressionComponentMask,-800,0);mask.set_editor_property('r',True);mask.set_editor_property('g',False);mask.set_editor_property('b',True);mask.set_editor_property('a',False);assert ml.connect_material_expressions(world,'',mask,'')
scale=expr(unreal.MaterialExpressionMultiply,-600,0);scale.set_editor_property('const_b',.003);ml.connect_material_expressions(mask,'',scale,'A')
offset=expr(unreal.MaterialExpressionConstant2Vector,-600,200);offset.set_editor_property('r',.5);offset.set_editor_property('g',0)
uv=expr(unreal.MaterialExpressionAdd,-400,0);ml.connect_material_expressions(scale,'',uv,'A');ml.connect_material_expressions(offset,'',uv,'B')
sample=expr(unreal.MaterialExpressionTextureSample,-200,0);sample.texture=texture;sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS);assert ml.connect_material_expressions(uv,'',sample,'UVs')
steel=color((.075,.095,.115),-200,400);black=color((.005,.004,.003),-200,600)
blend=expr(unreal.MaterialExpressionLinearInterpolate,100,100);ml.connect_material_expressions(steel,'',blend,'A');ml.connect_material_expressions(black,'',blend,'B');ml.connect_material_expressions(sample,'R',blend,'Alpha');ml.connect_material_property(blend,'',unreal.MaterialProperty.MP_BASE_COLOR)
edge=expr(unreal.MaterialExpressionSubtract,100,-200);ml.connect_material_expressions(sample,'R',edge,'A');ml.connect_material_expressions(sample,'G',edge,'B')
gold=color((.45,.07,.006),100,-400);glow=expr(unreal.MaterialExpressionMultiply,400,-200);ml.connect_material_expressions(edge,'',glow,'A');ml.connect_material_expressions(gold,'',glow,'B');ml.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
for value,prop in [(.65,unreal.MaterialProperty.MP_METALLIC),(.8,unreal.MaterialProperty.MP_ROUGHNESS)]:
 n=expr(unreal.MaterialExpressionConstant,400,400);n.r=value;ml.connect_material_property(n,'',prop)
ml.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
unreal.log('HOSTAGE_FEEDBACK_PREPARED')

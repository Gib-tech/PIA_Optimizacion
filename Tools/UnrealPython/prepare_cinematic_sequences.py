"""Author the three editable Sequencer assets and their original audio tracks."""
import unreal, os, json, shutil
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not ues.get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
folder='/Game/ThirdPerson/Cinematics'
unreal.EditorAssetLibrary.make_directory(folder)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
tools=unreal.AssetToolsHelpers.get_asset_tools()
manifest=[]

def extraction_material():
    path=folder+'/M_ExtractionShell';m=unreal.load_asset(path)
    if m:
        col=unreal.find_object(None,m.get_path_name()+':MaterialExpressionConstant3Vector_0')
        assert col
        col.set_editor_property('constant',unreal.LinearColor(.1,500,1400,1))
        unreal.MaterialEditingLibrary.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
        return m
    m=tools.create_asset('M_ExtractionShell',folder,unreal.Material,unreal.MaterialFactoryNew())
    m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_ADDITIVE)
    m.set_editor_property('two_sided',True)
    m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
    edit=unreal.MaterialEditingLibrary
    f=edit.create_material_expression(m,unreal.MaterialExpressionFresnel,-600,0)
    f.set_editor_property('exponent',3)
    col=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-600,180)
    col.set_editor_property('constant',unreal.LinearColor(.1,500,1400,1))
    mul=edit.create_material_expression(m,unreal.MaterialExpressionMultiply,-300,0)
    edit.connect_material_expressions(f,'',mul,'A');edit.connect_material_expressions(col,'',mul,'B')
    edit.connect_material_property(mul,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    edit.connect_material_property(f,'',unreal.MaterialProperty.MP_OPACITY)
    edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
    return m

def extraction_pulse(seq,duration):
    a=sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,-11400,110))
    c=a.static_mesh_component;c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Sphere'));c.set_material(0,extraction_material())
    c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_cast_shadow(False)
    b=seq.add_spawnable_from_instance(a);b.set_display_name('FX | Pulso de extracción temporal')
    tr=b.add_track(unreal.MovieScene3DTransformTrack);s=tr.add_section();s.set_range(0,frames(duration));s.set_completion_mode(unreal.MovieSceneCompletionMode.RESTORE_STATE)
    animate(s,[(0,[0,-11400,110,0,0,0,.01,.01,.01]),(3,[0,-11400,110,0,0,0,.1,.1,.1]),(6,[0,-11400,110,0,0,0,3.5,3.5,4.5]),(10,[0,-11400,110,0,0,0,5,5,6]),(14,[0,-11400,110,0,0,0,8,8,9])])
    sub.destroy_actor(a)

def frames(seconds):return round(seconds*30)
def animate(section,samples):
    channels=section.get_all_channels()
    for at,values in samples:
        for channel,value in zip(channels,values):
            channel.add_key(unreal.FrameNumber(frames(at)),value,interpolation=unreal.MovieSceneKeyInterpolation.LINEAR)
    return channels
def camera(seq,cut,start,end,pos0,pos1,target,focal=28):
    a=sub.spawn_actor_from_class(unreal.CineCameraActor,unreal.Vector(*pos0))
    c=a.get_cine_camera_component();c.set_editor_property('current_focal_length',focal)
    c.set_editor_property('current_aperture',16)
    c.set_editor_property('constrain_aspect_ratio',False)
    if seq.get_name()=='LS_Derrota':
        pp=c.get_editor_property('post_process_settings')
        pp.set_editor_property('override_color_saturation',True);pp.set_editor_property('color_saturation',unreal.Vector4(.25,.25,.25,1))
        pp.set_editor_property('override_vignette_intensity',True);pp.set_editor_property('vignette_intensity',.5)
        c.set_editor_property('post_process_settings',pp);c.set_editor_property('post_process_blend_weight',1)
    focus=c.get_editor_property('focus_settings');focus.set_editor_property('focus_method',unreal.CameraFocusMethod.DISABLE);c.set_editor_property('focus_settings',focus)
    rot0=unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos0),unreal.Vector(*target))
    rot1=unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos1),unreal.Vector(*target))
    a.set_actor_rotation(rot0,False)
    binding=seq.add_spawnable_from_instance(a);binding.set_display_name('CAM %02d | %.0f-%.0f s'%(len(cut.get_sections())+1,start,end))
    tr=binding.add_track(unreal.MovieScene3DTransformTrack);sec=tr.add_section();sec.set_range(frames(start),frames(end));sec.set_completion_mode(unreal.MovieSceneCompletionMode.RESTORE_STATE)
    def vals(pos,rot):return list(pos)+[rot.roll,rot.pitch,rot.yaw]+[1,1,1]
    animate(sec,[(start,vals(pos0,rot0)),(end,vals(pos1,rot1))])
    spawn=next((t for t in binding.get_tracks() if isinstance(t,unreal.MovieSceneSpawnTrack)),None)
    if spawn:
        for s in spawn.get_sections():s.set_range(frames(start),frames(end))
    cs=cut.add_section();cs.set_range(frames(start),frames(end))
    bid=unreal.MovieSceneObjectBindingID();bid.set_editor_property('guid',binding.get_id());cs.set_camera_binding_id(bid)
    sub.destroy_actor(a)
    return {'range':[start,end],'start':pos0,'end':pos1,'target':target,'focal_mm':focal}

specs=[
('LS_Intro',18,'SW_CinemaIntro',[
 (0,6,(650,-2100,240),(350,-1900,210),(0,-1430,160),24),
 (6,12,(-150,-390,185),(30,-470,165),(300,-800,165),28),
 (12,18,(350,-1050,180),(250,-960,165),(0,-560,145),26)]),
('LS_Derrota',8,'SW_CinemaDefeat',[
 (0,8,(-280,250,140),(-400,360,250),(0,150,-50),24)]),
('LS_Victoria',14,'SW_CinemaVictory',[
 (0,5,(390,-10900,310),(310,-10970,245),(0,-11400,110),28),
 (5,10,(-460,-11100,360),(-700,-10950,640),(0,-11400,170),26),
 (10,14,(0,-10500,920),(0,-10300,1250),(0,-11400,60),26)]),
('LS_Revelacion',12,'SW_CinemaRevelation',[
 (0,4,(260,100,90),(220,80,80),(0,0,50),32),
 (4,9,(180,-80,75),(150,-50,70),(0,0,50),38),
 (9,12,(230,100,105),(310,160,150),(0,0,45),30)])]
selection=os.path.join(root,'Intermediate/inspect/cinematics/sequence_selection.txt')
selected=set(open(selection,encoding='utf-8-sig').read().split()) if os.path.exists(selection) else None
for name,duration,sound,shots in specs:
    if selected is not None and name not in selected:continue
    task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Cinematics',sound+'.wav');task.destination_path=folder+'/Audio';task.automated=True;task.save=True;task.replace_existing=True;tools.import_asset_tasks([task])
    audio=unreal.load_asset(folder+'/Audio/'+sound);assert audio
    audio.set_editor_property('sound_class_object',unreal.load_asset('/Engine/EngineSounds/Master.Master'))
    unreal.EditorAssetLibrary.save_loaded_asset(audio)
    path=folder+'/'+name
    seq=unreal.load_asset(path)
    if seq:
        for b in list(seq.get_bindings()):b.remove()
        for t in list(seq.get_tracks()):seq.remove_track(t)
    else:seq=tools.create_asset(name,folder,unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(30,1));seq.set_playback_start(0);seq.set_playback_end(frames(duration))
    seq.set_work_range_start(0);seq.set_work_range_end(duration)
    cut=seq.add_track(unreal.MovieSceneCameraCutTrack)
    shotinfo=[camera(seq,cut,*s) for s in shots]
    if name=='LS_Victoria':extraction_pulse(seq,duration)
    fade=seq.add_track(unreal.MovieSceneFadeTrack).add_section();fade.set_range(0,frames(duration));fade.set_completion_mode(unreal.MovieSceneCompletionMode.RESTORE_STATE)
    animate(fade,[(0,[1]),(.7,[0]),(duration-1,[0]),(duration,[1])])
    track=seq.add_track(unreal.MovieSceneAudioTrack);section=track.add_section();section.set_sound(audio);section.set_range(0,frames(duration));section.set_looping(False)
    unreal.EditorAssetLibrary.set_metadata_tag(seq,'TimeOut.Story',{'LS_Intro':'Una señal entre épocas','LS_Derrota':'La señal se apaga','LS_Victoria':'Volver juntos','LS_Revelacion':'El último guardián'}[name])
    unreal.EditorAssetLibrary.save_loaded_asset(seq,only_if_is_dirty=False)
    manifest.append({'asset':path,'duration':duration,'fps':30,'shots':shotinfo,'audio':audio.get_path_name()})
    unreal.log('CINEMA_SEQUENCE_READY '+name)
os.makedirs(os.path.join(root,'Intermediate/inspect/cinematics'),exist_ok=True)
with open(os.path.join(root,'Intermediate/inspect/cinematics/sequences.json'),'w',encoding='utf-8') as f:json.dump(manifest,f,indent=2,ensure_ascii=False)
unreal.log('CINEMA_SEQUENCES_READY')

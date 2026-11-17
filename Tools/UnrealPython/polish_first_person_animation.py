"""Recuperación visual de ataques FP hacia una guardia coherente.

Solo modifica las copias AFP sin notifies. Las secuencias originales y el daño
de tercera persona permanecen como autoridad de combate.
"""
import unreal,os,json,math
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
sources=json.load(open(os.path.join(root,'Intermediate/inspect/player_animations/sources.json')))
copies=json.load(open(os.path.join(root,'Tools/ArtSource/FirstPerson/animation_manifest.json')))
lookup={r['montage']:r['sequences'][0] for r in sources if len(r['sequences'])==1}
lib=unreal.AnimationLibrary
sword=unreal.load_asset(next(v for k,v in lookup.items() if k.endswith('/FA_1_Montage.FA_1_Montage')))
hammer=unreal.load_asset(next(v for k,v in lookup.items() if k.endswith('/HA_1_Montage.HA_1_Montage')))
def blend(a,b,t):
 return unreal.Vector(a.x+(b.x-a.x)*t,a.y+(b.y-a.y)*t,a.z+(b.z-a.z)*t)
def quat(a,b,t):
 sign=1 if a.x*b.x+a.y*b.y+a.z*b.z+a.w*b.w>=0 else -1
 q=[getattr(a,k)+(getattr(b,k)*sign-getattr(a,k))*t for k in ('x','y','z','w')]
 n=math.sqrt(sum(x*x for x in q));return unreal.Quat(*(x/n for x in q))
report=[]
for row in copies:
 original=unreal.load_asset(lookup[row['montage']]);copy=unreal.load_asset(row['sequence'])
 is_hammer='/Hammer/' in row['montage'] or any('/'+x+'_Montage.' in row['montage'] for x in ('Attack_1','Attack_2','Attack_3'))
 ready=hammer if is_hammer else sword;ready_time=.65 if is_hammer else .33
 length=original.get_play_length();frames=lib.get_num_frames(original);keys=frames+1
 end=length
 for name,cut in [('H_attack_1',1.18),('H_attack_2',1.05),('H_attack_3',1.70)]:
  if '/'+name+'_Montage.' in row['montage']:end=min(end,cut)
 controller=copy.get_editor_property('controller');controller.open_bracket('Guardia y recuperación FP',False)
 tracks=lib.get_animation_track_names(original)
 for bone in tracks:
  guard=lib.get_bone_pose_for_time(ready,bone,ready_time,False)
  ps=[];qs=[];ss=[]
  for i in range(keys):
   t=length*i/frames if frames else 0
   pose=lib.get_bone_pose_for_time(original,bone,t,False)
   weight=max(0,min(1,t/.12,(end-t)/.18));weight=weight*weight*(3-2*weight)
   ps.append(blend(guard.translation,pose.translation,weight));qs.append(quat(guard.rotation,pose.rotation,weight));ss.append(blend(guard.scale3d,pose.scale3d,weight))
  assert controller.set_bone_track_keys(bone,ps,qs,ss,False),str(bone)
 controller.close_bracket(False)
 lib.remove_all_animation_notify_tracks(copy)
 unreal.EditorAssetLibrary.save_loaded_asset(copy,only_if_is_dirty=False)
 report.append({'asset':row['sequence'],'keys':keys,'tracks':len(tracks),'recovery_end':end,'guard_source':ready.get_path_name(),'guard_time':ready_time})
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega');cdo=unreal.get_default_object(bp.generated_class())
cdo.set_editor_property('FPIdleSwordPosition',0);cdo.set_editor_property('FPIdleHammerPosition',0)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
with open(os.path.join(root,'Tools/ArtSource/FirstPerson/pose_manifest.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False)
unreal.log('FIRST_PERSON_RECOVERY_POLISHED '+str(len(report)))

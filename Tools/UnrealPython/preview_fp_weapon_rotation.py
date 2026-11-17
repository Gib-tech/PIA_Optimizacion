import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_character(w,0);sword=p.get_editor_property('EspadaFP')
p.stop_anim_montage(p.get_current_montage());p.call_method('ResetState')
lib=unreal.get_default_object(unreal.SystemLibrary)
for k,v in [('bIsSwordEquipped',True),('bIsHammerEquipped',False),('IsAttacking',False)]:lib.call_method('SetBoolPropertyByName',(p,k,v))
unreal.log('SWORD_TRANSFORMS '+str(sword.get_local_bounds())+' world '+str(sword.get_world_rotation())+' socket '+str(p.get_editor_property('BrazosFP').get_socket_transform('WeaponSocket',unreal.RelativeTransformSpace.RTS_COMPONENT)))
folder=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/fp_polish');os.makedirs(folder,exist_ok=True)
s={'index':0,'at':0,'handle':None}
def tick(dt,state=s):
 now=unreal.GameplayStatics.get_time_seconds(w)
 if now-state['at']<.6:return
 i=state['index']
 if i%2==0:
  angle=(i//2)*30
  sword.set_relative_rotation(unreal.Rotator(roll=angle),False,True)
 else:
  angle=(i//2)*30
  unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,'sword-roll-'+str(angle)+'.png').replace('\\','/')+'"')
 state['index']+=1;state['at']=now
 if state['index']==8:unreal.unregister_slate_post_tick_callback(state['handle'])
s['handle']=unreal.register_slate_post_tick_callback(tick)

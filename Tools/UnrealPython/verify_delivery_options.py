"""Exercise actual UMG event delegates and native settings; agent test, not owner acceptance."""
import unreal,json,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
ui=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C'))
widget=ui.get_editor_property('OptionsWidget');assert ui.get_editor_property('bOptionsOpen')
s=unreal.GameUserSettings.get_game_user_settings();results=[]
def click(field,index):
 widget.call_method('BndEvt__Menu_Opciones_'+field+'_Control_'+str(index)+'_OnButtonClickedEvent__DelegateSignature')
 assert str(widget.get_editor_property('SettingsStatus').get_text())
index=0
for group,getter,values in [('viewdistance',s.get_view_distance_quality,[0,1,3]),('antialiasing',s.get_anti_aliasing_quality,[0,1,2,3]),('shadow',s.get_shadow_quality,[0,1,2,3]),('texture',s.get_texture_quality,[0,1,2,3])]:
 for i,value in enumerate(values,1):
  click('btn_'+group+str(i)+'_O',index);index+=1
  assert getter()==value
 results.append(group)
for i,(x,y) in enumerate([(1280,720),(1600,900),(1920,1080),(2560,1440)],1):
 click('btn_resolucion'+str(i)+'_O',index);index+=1
 actual=s.get_screen_resolution();assert actual.x==x and actual.y==y
results.append('four_resolutions')
for i,mode in enumerate([unreal.WindowMode.WINDOWED,unreal.WindowMode.WINDOWED_FULLSCREEN,unreal.WindowMode.FULLSCREEN]):
 click('btn_display'+str(i),index);index+=1
 assert s.get_fullscreen_mode()==mode
results.append('three_display_modes')
for i,value in enumerate([0,.25,.5,1]):
 click('btn_volume'+str(i),index);index+=1
 assert ui.get_editor_property('MasterVolume')==value
 data=unreal.GameplayStatics.load_game_from_slot('TimeOut_Options_v1',0)
 assert data.get_editor_property('Version')==1 and data.get_editor_property('MasterVolume')==value
results.append('four_volume_presets_saved')
# Leave modest settings for a repeated PIE and packaged smoke test.
s.set_view_distance_quality(1);s.set_anti_aliasing_quality(2);s.set_shadow_quality(1);s.set_texture_quality(2)
s.set_screen_resolution(unreal.IntPoint(1280,720));s.set_fullscreen_mode(unreal.WindowMode.WINDOWED)
s.apply_settings(False);s.confirm_video_mode();s.save_settings()
click('btn_volume1',23)
out={'passed':True,'agent_test_not_owner_acceptance':True,'method':'UMG bound OnClicked event functions, native getter and disk save readback','checks':results,'restart_expected':{'qualities':[1,2,1,2],'resolution':[1280,720],'mode':'Windowed','volume':.25}}
path=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/delivery_options_assertions.json')
with open(path,'w',encoding='utf-8') as f:json.dump(out,f,indent=2)
unreal.log('OPTIONS_REGRESSION '+json.dumps(out))

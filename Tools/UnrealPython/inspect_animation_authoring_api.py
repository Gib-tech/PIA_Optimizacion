import unreal
for cls,name in [(unreal.AnimationLibrary,'get_bone_pose_for_time'),(unreal.AnimationDataController,'set_bone_track_keys'),(unreal.AnimationLibrary,'get_num_frames'),(unreal.AnimationLibrary,'get_animation_track_names')]:
 unreal.log('ANIMATION_API '+cls.__name__+'.'+name+' '+str(getattr(cls,name,None).__doc__))
a=unreal.load_asset('/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_FA_1')
unreal.log('ANIMATION_METHODS '+str([n for n in dir(a) if any(t in n for t in ['controller','length','frame'])]))

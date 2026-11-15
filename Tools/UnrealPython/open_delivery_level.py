"""Open the delivery map and frame the start; does not modify or save assets."""
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
if world.get_name()!='Nivel_Entrega':
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/ThirdPerson/Maps/Nivel_Entrega')
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(0,-100,300),unreal.Rotator(pitch=-15,yaw=-90,roll=0))
unreal.log('DELIVERY_READY_FOR_REVIEW')

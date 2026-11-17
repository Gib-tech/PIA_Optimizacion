"""Desactiva temporalmente throttle de segundo plano para muestrear ventanas reales."""
import unreal,json,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());path=os.path.join(root,'Intermediate/inspect/daynight-attacks/editor-performance.json')
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
if not os.path.isfile(path):
 with open(path,'w') as f:json.dump({'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground')},f)
settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 60')

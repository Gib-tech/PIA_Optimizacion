"""Actualiza comentarios sólo en los Blueprints propios de esta revisión."""
import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());script=os.path.join(root,'Tools/UnrealPython/install_spanish_blueprint_comments.py')
ns={'__file__':script,'__name__':'revision_documentation','BLUEPRINT_DOCUMENTATION_FILTER':{'/Game/ThirdPerson/Blueprints/Entrega/'+n for n in ['BP_TecnicoTemporal','BP_SistemasComplementarios','BP_HUD_Entrega','BP_DeliverySaveManager','BP_DestruibleEntrega','BP_PulsoTemporalVisual']}}
exec(compile(open(script,encoding='utf-8').read(),script,'exec'),ns)

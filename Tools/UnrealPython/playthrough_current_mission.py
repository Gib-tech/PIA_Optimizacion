"""Partida completa con tres encuentros y suministros, sin preparar salud/posiciones.

Reutiliza el operador de movimiento físico ya probado y adapta su recorrido a la
tercera horda. Las curaciones pasan por el evento de consumo del inventario.
"""
import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
source=open(os.path.join(root,'Tools/UnrealPython/playthrough_fluid_combat.py'),encoding='utf-8').read()
changes=[
 ('for i in (1,2)]','for i in (1,2,3)]'),
 ("Intermediate/inspect/fluid_mission_playthrough.json","docs/validation/partida-completa-2026-11-17.json"),
 ("state={'stage':'rescue'","state={'stage':'supplies'"),
 ("'no_health_or_damage_overrides':True,","'no_health_or_damage_overrides':True,'healing_uses_consumable_inventory':True,"),
 ("        current=s['stage']\n", "        if prop(d,'bNarrativePaused'):return\n        extras=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C'))\n        if prop(prop(p,'BPC_Health'),'Health')<=65 and prop(extras,'Botiquines')>0:extras.call_method('UsarBotiquin')\n        current=s['stage']\n"),
 ("        if current in ('rescue','recover'):","        if current=='supplies':\n            move(prop(extras,'Suministro1').get_actor_location(),now)\n            if prop(extras,'Recogido1'):stage('rescue',now)\n        elif current in ('rescue','recover'):"),
 ("stage('enter' if current=='rescue' else 'door',now)","stage('enter' if current=='rescue' else 'beacon' if i==2 else 'door',now)"),
 ("stage('enter' if s['index']==1 else 'beacon' if s['index']==2 else 'extract',now)","stage('enter' if s['index']<3 else 'extract',now)"),
 ("            zone=zones[i]\n            move(zone.get_actor_location(),now)","            zone=zones[i]\n            if prop(zone,'Phase')>0:\n                stage('combat',now)\n                return\n            if i>0 and not prop(extras,'Recogido'+str(i+1)):\n                move(prop(extras,'Suministro'+str(i+1)).get_actor_location(),now)\n                return\n            move(zone.get_actor_location(),now)"),
 ("            zone=zones[i]\n            enemies=", "            zone=zones[i]\n            if prop(p,'bIsHammerEquipped') and not prop(p,'IsAttacking'):\n                p.call_method('InpActEvt_IA_SwitchToSword_K2Node_EnhancedInputActionEvent_2',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_SwitchToSword')))\n            enemies="),
 ("                distance=p.get_distance_to(target)\n", "                distance=p.get_distance_to(target)\n                if distance<750 and prop(extras,'Cargas')>0:extras.call_method('DispararPulso')\n"),
 ("            door=doors[i];", "            if prop(p,'bIsSwordEquipped') and not prop(p,'IsAttacking'):\n                p.call_method('InpActEvt_IA_SwitchToHammer_K2Node_EnhancedInputActionEvent_3',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_SwitchToHammer')))\n            door=doors[i];"),
]
for old,new in changes:
 assert source.count(old)==1,(old,source.count(old))
 source=source.replace(old,new)
script=os.path.join(root,'Tools/UnrealPython/playthrough_current_mission.py')
namespace={'__name__':'current_mission_playthrough','__file__':script}
exec(compile(source,script,'exec'),namespace)
w=namespace['w']
# Capturas reales de hitos; no se preparan ni teletransportan actores.
original_stage=namespace['stage']
def captured_stage(name,now,s=namespace['state']):
 original_stage(name,now,s)
 folder=os.path.join(root,'docs/validation/partida-completa');os.makedirs(folder,exist_ok=True)
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,str(len(s['events'])).zfill(2)+'-'+name+'.png').replace('\\','/')+'"')
namespace['stage']=captured_stage

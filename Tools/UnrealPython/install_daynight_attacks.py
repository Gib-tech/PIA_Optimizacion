"""Instala exclusivamente cielo/inventario, contacto, prop y su leyenda; documenta los grafos."""
import unreal,os,json,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/'
folder=os.path.join(root,'docs/validation/ciclo-luces-ataques');os.makedirs(folder,exist_ok=True)
rows=[]
notes={
 'BP_SistemasComplementarios':'CICLO SOLAR Y PULSO\nDayCycleDuration=1200 s. Smoothstep en ambas transiciones.\nWorldSeconds persistido; pausa y escena suspenden avance.\nPulso: primer enemigo o destruible visible, 20 de daño, 8 m.\nConsume una carga y respeta 0,8 s de recuperación.\nVer docs/CICLO_LUCES_Y_ATAQUES.md.',
 'BP_PlayerEntrega':'CONTACTO CON DESTRUIBLES\nEspada y martillo: ligero 15 / pesado 25. Sin exigir mejora.\nWeaponHitbox conserva las ventanas reales del montaje.\nBarrido de props bajos: 220 cm / radio 30; sólo en ventana.\nPrimer bloqueo Visibility; deduplicación con HeavyHitActors.\nPuertas: conservan desbloqueo y martillo cargado.\nVer docs/CICLO_LUCES_Y_ATAQUES.md.',
 'BP_DestruibleEntrega':'DESTRUCCIÓN CON TODOS LOS ATAQUES\nSólo daño positivo cuyo DamageCauser sea BP_PlayerEntrega.\nAcepta espada, martillo y pulso; no depende de IsAttacking.\nHealth=0 dispara Chaos una sola vez (bBroken).\nRestos ignoran Pawn/Camera y expiran tras 8 s.\nVer docs/CICLO_LUCES_Y_ATAQUES.md.',
 'BP_HUD_Entrega':'LEYENDA DE DESTRUIBLES\nEl objetivo apuntado ofrece ligero / pesado / pulso.\nEl HUD lee estado y dibuja; nunca aplica daño.\nVer docs/CICLO_LUCES_Y_ATAQUES.md.'}
for name,note in notes.items():
 bp=unreal.load_asset(R+name);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 assert unreal.DeliveryBlueprintBuilder.add_layout_comment(bp,'DocumentacionCicloAtaques',note,unreal.Vector2D(-1000,-550),unreal.Vector2D(850,480),unreal.LinearColor(.10,.22,.30,1))
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
names=list(notes)+['BP_DeliverySaveManager','BP_DirectorEntrega','BP_LuminariaPared']
# La sustitución temporal del grafo vacía GrantHammerUpgrade; recompilar todos
# sus consumidores antes de inspeccionar evita conservar ese error transitorio.
for _ in range(2):
 for name in names:unreal.BlueprintEditorLibrary.compile_blueprint(unreal.load_asset(R+name))
for name in names:
 bp=unreal.load_asset(R+name);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/daynight-attacks',name+'-after.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
 data=open(task.filename,'rb').read();source=data.decode('utf-16' if data.startswith(b'\xff\xfe') else 'utf-8-sig')
 status=re.search(r'^   Status=(.*)',source,re.M);status=status.group(1).strip() if status else 'no serializado'
 diagnostics=re.findall(r'ErrorMsg="([^"]+)"',source)
 try:status=str(bp.get_editor_property('status'))
 except Exception:pass
 # Los exports también incluyen subobjetos antiguos con diagnósticos retenidos.
 # La compilación de InstallGraph y el estado del BP son la autoridad actual.
 fatal='BS_Error' in status or 'BS_ERROR' in status
 rows.append({'blueprint':bp.get_path_name(),'status':status,'fatal_errors':fatal,'diagnostics':diagnostics})
 assert status!='BS_Error' and not fatal,(name,status,diagnostics)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
with open(os.path.join(folder,'compilacion.json'),'w',encoding='utf-8') as f:json.dump({'passed':True,'blueprints':rows},f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_ATTACKS_INSTALLED_AND_COMPILED')

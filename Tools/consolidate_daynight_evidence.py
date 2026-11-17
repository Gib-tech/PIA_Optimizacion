"""Consolida evidencias ya observadas del paquete y verifica la revisión antes de archivarla."""
from pathlib import Path
import json,re,shutil,hashlib
root=Path(__file__).resolve().parents[1];folder=root/'docs/validation/ciclo-luces-ataques'
raw=(root/'Deliverables/build.log').read_bytes();log=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig',errors='replace')
assert 'BUILD SUCCESSFUL' in log
summary=re.search(r'Success - (\d+) error\(s\), (\d+) warning\(s\)',log);assert summary and int(summary[1])==0
duration=float(re.search(r'BuildCookRun time: ([\d.]+) s',log)[1])
runtime=(root/'Intermediate/inspect/daynight-attacks/package-smoke.log').read_text(encoding='utf-8',errors='replace');assert 'LogExit: Exiting.' in runtime and 'Fatal error' not in runtime
shots=root/'Intermediate/inspect/daynight-attacks/native-user/Saved/Screenshots/Windows'
for source,name in [('ScreenShot00000.png','paquete-inicio.png'),('ScreenShot00001.png','paquete-caja-destruida.png')]:shutil.copy2(shots/source,folder/name)
cold=json.loads((folder/'recarga-fria.json').read_text(encoding='utf-8'));assert cold['passed'] and cold['native_save_read_by_unreal']['Cargas']==2
report={'passed':True,'build_cook_run_seconds':duration,'cook_errors':int(summary[1]),'cook_warnings':int(summary[2]),'existing_warning':'Pin Scale de SpawnSystemAttached, previo a esta revisión.','method':'Win64 Development, UserDir aislado y checkpoint nocturno preparado. Continuar por clic; clic central, dos clics izquierdos, Enter, F5 y P por teclado/ratón reales. Sin comandos de daño ni helper. No es otra partida natural ni prueba con mando físico.','observed':{'continue_restores_prepared_night':True,'floor_walls_and_characters_visible':True,'pulse_charges':[3,2],'crate_fractured_after_pulse_and_two_light_sword_attacks':True,'pause_and_resume_work':True,'F5_save_read_in_cold_editor':cold['native_save_read_by_unreal']},'isolated_user_dir':'Intermediate/inspect/daynight-attacks/native-user','game_closed_cleanly':True}
(folder/'paquete-final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(folder/'paquete-log.txt').write_text('\n'.join(line for line in log.splitlines() if any(key in line for key in ['Success -','BuildCookRun time:','BUILD SUCCESSFUL','AutomationTool exiting with ExitCode=']))+'\n',encoding='utf-8')
for name in ['destruibles-espada_ligero','destruibles-espada_pesado','destruibles-martillo_ligero','destruibles-martillo_pesado','destruibles-pulso','ciclo-runtime','guardado-y-guardas','compilacion','partida-nocturna','recarga-fria','paquete-final','datos-usuario-restaurados']:
 assert json.loads((folder/(name+'.json')).read_text(encoding='utf-8'))['passed'],name
for row in json.loads((folder/'datos-usuario-restaurados.json').read_text(encoding='utf-8'))['files']:
 assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
print('DAYNIGHT_EVIDENCE_VERIFIED',duration,'seconds;',summary[1],'errors;',summary[2],'warnings')

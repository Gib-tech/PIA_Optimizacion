"""Ejecuta cinco sesiones PIE independientes y exige seis fracturas por sesión."""
from pathlib import Path
import json,subprocess,sys,time
root=Path(__file__).resolve().parents[2]
def editor(script):
 result=subprocess.run([sys.executable,str(root/'Tools/UnrealPython/run.py'),str(root/'Tools/UnrealPython'/script)],cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if result.returncode:raise RuntimeError(result.stdout+result.stderr)
 print(result.stdout,flush=True)
for mode in sys.argv[1:] or ['espada_ligero','espada_pesado','martillo_ligero','martillo_pesado','pulso']:
 editor('pie_stop.py');time.sleep(1)
 (root/'Intermediate/inspect/daynight-attacks/test-mode.json').write_text(json.dumps({'mode':mode}),encoding='utf-8')
 editor('pie_start.py');time.sleep(3)
 started=time.time();editor('verify_destructibles_all_attacks.py')
 report=root/'docs/validation/ciclo-luces-ataques'/('destruibles-'+mode+'.json')
 while time.time()-started<160:
  if report.exists() and report.stat().st_mtime>=started:
   result=json.loads(report.read_text(encoding='utf-8'))
   assert result['passed'],result
   assert len(result['objects'])==6
   print('PASSED',mode,flush=True);break
  time.sleep(1)
 else:raise TimeoutError(mode)
editor('pie_stop.py')

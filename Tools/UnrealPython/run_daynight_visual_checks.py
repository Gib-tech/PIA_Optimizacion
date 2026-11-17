"""Ejecuta verificaciones solares y capturas esperando evidencia nueva de cada callback."""
from pathlib import Path
import json,time,subprocess,sys
root=Path(__file__).resolve().parents[2];folder=root/'docs/validation/ciclo-luces-ataques'
def editor(script):
 result=subprocess.run([sys.executable,str(root/'Tools/UnrealPython/run.py'),str(root/'Tools/UnrealPython'/script)],cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
 assert result.returncode==0,result.stdout+result.stderr
 print(result.stdout,flush=True)
editor('pie_start.py');time.sleep(3)
for script,report in [('verify_daynight_runtime.py','ciclo-runtime.json'),('capture_daynight_wall_lights.py','capturas.json')]:
 started=time.time();editor(script)
 for _ in range(110):
  path=folder/report
  if path.exists() and path.stat().st_mtime>=started:
   result=json.loads(path.read_text(encoding='utf-8'));assert result.get('passed',True),result
   print('PASSED',report,flush=True);break
  time.sleep(1)
 else:raise TimeoutError(report)
editor('pie_stop.py')

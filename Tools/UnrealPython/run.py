"""Send one editor-side script to the open Unreal Editor and print its log output.

Usage (from the repository root, PowerShell):
    python Tools\\UnrealPython\\run.py Tools\\UnrealPython\\ping.py

The editor must be open with remote execution enabled
(Config/DefaultEngine.ini -> [/Script/PythonScriptPlugin.PythonScriptPluginSettings] bRemoteExecution=True).
"""
import os
import sys
import time

ENGINE_PYTHON = r"C:\Program Files\Epic Games\UE_5.6\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python"
sys.path.append(os.environ.get("UE_REMOTE_PYTHON", ENGINE_PYTHON))
import remote_execution as rex  # noqa: E402

if len(sys.argv) < 2:
    raise SystemExit("usage: python Tools\\UnrealPython\\run.py <editor_script.py>")

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    command = handle.read()

remote = rex.RemoteExecution()
remote.start()
deadline = time.time() + 8
nodes = []
while time.time() < deadline:
    nodes = remote.remote_nodes
    if nodes:
        break
    time.sleep(0.5)
if not nodes:
    remote.stop()
    raise SystemExit("no editor (open Terreno.uproject and wait for it to finish loading)")

remote.open_command_connection(nodes[0]["node_id"])
result = remote.run_command(command, exec_mode=rex.MODE_EXEC_FILE)
remote.stop()
print("SUCCESS", result.get("success"))
for item in result.get("output") or []:
    print(item.get("type"), item.get("output"))
if not result.get("success"):
    print(result.get("result"))

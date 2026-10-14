"""Local (not editor). Prints the runtime structure of a Behavior Tree T3D export.

Usage:
    python Tools\\UnrealPython\\bt_structure.py BT_EnemyIA

Read the BTComposite_Selector_0 / BTComposite_Sequence_N "Children(i)" lines for the
real execution order (left to right = index 0, 1, 2...). Each child lists its decorators.
Then read each decorator/task object for its settings (key, value, abort mode, cooldown).
Settings left at engine default are NOT printed by the exporter.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
name = sys.argv[1] if len(sys.argv) > 1 else "BT_EnemyIA"
path = os.path.join(ROOT, "Intermediate", "inspect", "live", name + ".t3d")
data = open(path, "rb").read()
text = data.decode("utf-16") if data[:2] == b"\xff\xfe" else data.decode("utf-8", "replace")
pattern = re.compile(r'\s*(Children\(|Services\(|Begin Object Name="BT(Composite|Decorator|Task|Service)|FloatValue|'
                     r'IntValue|StringValue|OperationType|ArithmeticOperation|BasicOperation|FlowAbortMode|'
                     r'BlackboardKey=|CoolDownTime|WaitTime|RandomDeviation|CachedDescription|bAllowStrafe|'
                     r'bObserve|AcceptableRadius|RootNode|NodeName|bInverseCondition|ParentNode|[A-Za-z]+Key=\()')
for line in text.splitlines():
    if pattern.match(line):
        s = line.strip()
        s = re.sub(r"/Script/AIModule\.|/Game/[A-Za-z0-9_/]+/[A-Za-z0-9_]+\.", "", s)
        s = re.sub(r'ExportPath="[^"]+"', "", s)
        print(s[:300])

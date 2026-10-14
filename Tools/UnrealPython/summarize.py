"""Local (not editor). Turns a Blueprint T3D export into a readable node/pin/wire list.

Usage:
    python Tools\\UnrealPython\\summarize.py BTTask_Roam BP_BaseEnemy
Reads  Intermediate/inspect/live/<Name>.t3d
Writes Intermediate/inspect/live/_<Name>.txt

Output format per node:
    [GraphName] NodeName (Class)
       . FunctionReference/VariableReference/... (what the node is)
       IN  PinName[category] =default -> OtherNode.OtherPin
       OUT then[exec] -> <none>          (an exec output with no wire)

Links are resolved by (node name, pin id). Copy-pasted nodes share pin ids, so never
resolve by pin id alone. Function graphs reuse node names like K2Node_FunctionEntry_0,
so trust links inside [EventGraph] first.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = os.path.join(ROOT, "Intermediate", "inspect", "live")
KEEP = ("FunctionReference", "EventReference", "VariableReference", "CustomFunctionName", "TargetType",
        "NodeComment", "ErrorType", "ErrorMsg", "EnabledState", "DelegateReference")


def load(path):
    data = open(path, "rb").read()
    return data.decode("utf-16") if data.startswith(b"\xff\xfe") else data.decode("utf-8", errors="replace")


def summarize(name):
    lines = load(os.path.join(BASE, name + ".t3d")).splitlines()
    blocks, stack = [], []
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("Begin Object"):
            stack.append((i, s))
        elif s == "End Object" and stack:
            start, header = stack.pop()
            blocks.append((start, i, header))
    pin_owner, nodes = {}, []
    for start, end, header in blocks:
        if "CustomProperties Pin" not in "\n".join(lines[start:end]):
            continue
        nm = re.search(r'Name="([^"]+)"', header)
        cls = re.search(r"Class=([^ ]+)", header)
        if not nm:
            continue
        ep = re.search(r"ExportPath=\"[^']*'[^:]*:([^']*)'", header)
        graph = ep.group(1).rsplit(".", 1)[0] if ep else "?"
        own, depth = [], 0
        for l in lines[start + 1:end]:
            st = l.strip()
            if st.startswith("Begin Object"):
                depth += 1
            elif st == "End Object":
                depth -= 1
            elif depth == 0:
                own.append(st)
        nodes.append((graph, nm.group(1), cls.group(1) if cls else "", own))
        for l in own:
            m = re.search(r'PinId=([0-9A-F]{32}),PinName="([^"]+)"', l)
            if m:
                pin_owner[(nm.group(1), m.group(1))] = (nm.group(1), m.group(2))
    out, seen = [], set()
    for graph, node, cls, own in nodes:
        if (graph, node) in seen:
            continue
        seen.add((graph, node))
        out.append("\n[%s] %s (%s)" % (graph, node, cls.rsplit(".", 1)[-1]))
        for l in own:
            if l.startswith(KEEP):
                out.append("   . " + l[:260])
        for l in own:
            if not l.startswith("CustomProperties Pin"):
                continue
            pn = re.search(r'PinName="([^"]+)"', l)
            if not pn or ("bHidden=True" in l and "LinkedTo" not in l):
                continue
            direction = "OUT" if 'Direction="EGPD_Output"' in l else "IN "
            cat = re.search(r'PinType\.PinCategory="([^"]*)"', l)
            default = re.search(r'DefaultValue="([^"]*)"', l)
            dobj = re.search(r'DefaultObject="([^"]*)"', l)
            links = []
            lm = re.search(r"LinkedTo=\(([^)]*)\)", l)
            if lm:
                for nn, pid in re.findall(r"([A-Za-z0-9_]+) ([0-9A-F]{32})", lm.group(1)):
                    o = pin_owner.get((nn, pid))
                    links.append("%s.%s" % o if o else nn + "?")
            if not links and not default and not dobj and cat and cat.group(1) == "exec":
                links = ["<none>"]
            extra = (" =" + default.group(1) if default else "") + (" obj=" + dobj.group(1) if dobj else "")
            out.append("   %s %s[%s]%s -> %s" % (direction, pn.group(1), cat.group(1) if cat else "", extra,
                                                  ", ".join(links)))
    dest = os.path.join(BASE, "_" + name + ".txt")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    print(name, len(nodes), "nodes ->", dest)


for n in sys.argv[1:]:
    summarize(n)

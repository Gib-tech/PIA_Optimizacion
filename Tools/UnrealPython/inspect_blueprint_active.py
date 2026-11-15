"""Inspect active graph nodes, excluding stale orphan objects retained in T3D exports."""
from pathlib import Path
import re
import sys

def read(path):
    data=path.read_bytes()
    return data.decode('utf-16') if data.startswith(b'\xff\xfe') else data.decode('utf-8',errors='replace')

def inspect(name):
    path=Path('Intermediate/inspect/live')/(name+'.t3d')
    stack=[];blocks=[]
    for line in read(path).splitlines():
        s=line.strip()
        if s.startswith('Begin Object'):
            m=re.search(r'Name="([^"]+)"',s)
            stack.append({'name':m.group(1) if m else '?','own':[],'children':[]})
        elif s=='End Object':
            b=stack.pop();blocks.append(b)
            if stack:stack[-1]['children'].append(b)
        elif stack:stack[-1]['own'].append(s)
    errors=0
    for graph in blocks:
        names=[]
        for line in graph['own']:
            m=re.match(r'Nodes\(\d+\)="[^\']*\'([^\']*)\'"',line)
            if m:names.append(m.group(1).rsplit('.',1)[-1])
        if not names:continue
        print('ACTIVE_GRAPH',name,graph['name'],len(names))
        for child in graph['children']:
            if child['name'] not in names:continue
            body='\n'.join(child['own'])
            if 'ErrorType=1' in body and 'bHasCompilerMessage=True' in body:
                errors+=1
                print('ERROR',child['name'],next((l for l in child['own'] if l.startswith('ErrorMsg=')),''))
            for prop in child['own']:
                if prop.startswith(('CustomFunctionName=','EventReference=')):
                    print('ENTRY',child['name'],prop)
    print('ACTIVE_ERRORS',errors)
    return errors

if __name__=='__main__':sys.exit(1 if sum(inspect(n) for n in sys.argv[1:]) else 0)

"""Read public Fab metadata; never uses browser session cookies or credentials."""
import urllib.request,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent;out=root/'Intermediate/inspect/team-models'
uid='28820c60-aebe-441d-afbe-2113741b451c'
for suffix in ['', '/asset-formats']:
 url='https://www.fab.com/i/listings/'+uid+suffix
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response:data=json.load(response)
  name='fab-tree'+('-formats' if suffix else '')+'.json';(out/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
  print(name,str(data)[:2200])
 except Exception as e:print(url,e)
url='https://www.fab.com/i/listings/'+uid+'/asset-formats/converted-files/files/ec324282-27c6-47d7-b9dd-b6b8a90dbd71/download-info'
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response:data=json.load(response)
 (out/'fab-tree-download-info.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 print('Public tree download metadata received',list(data) if isinstance(data,dict) else type(data).__name__)
 info=next(i for i in data['downloadInfo'] if i.get('downloadUrl'))
 target=out/'realistic_tree.glb'
 if not target.exists():
  import shutil
  with urllib.request.urlopen(info['downloadUrl'],timeout=90) as response,open(target,'wb') as f:shutil.copyfileobj(response,f)
 print('TREE_DOWNLOADED',target.stat().st_size)
except Exception as e:print('Public download metadata:',e)

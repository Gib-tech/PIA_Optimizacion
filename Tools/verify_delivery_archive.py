"""Valida ZIP final y genera comprobante/checksum externo al propio ZIP."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json
root=Path(__file__).resolve().parents[1];delivery=root/'Deliverables';path=delivery/'TimeOut_Avance_18Nov2026.zip'
with ZipFile(path) as z:
 names=z.namelist();assert len(names)==len(set(names))
 assert not any(n.lower().endswith('.pdb') or '/Saved/' in n or 'BlueprintBuildBridge' in n for n in names)
 expected_fiches=len(list((root/'docs/blueprints').glob('*.md')))
 assert sum(n.startswith('docs/blueprints/') and n.endswith('.md') for n in names)==expected_fiches
 assert all(n in names for n in ['Windows/Terreno.exe','docs/LEEME_EQUIPO.md','docs/IA_Y_COMBATE.md','docs/validation/robot-cielo-inventario/energia-runtime.json','docs/validation/cinematic-layout.json'])
 assert 'docs/ITEMS_Y_DESTRUIBLES.md' in names
 for report in ['efectos-runtime','seis-destruibles','energia-runtime','paquete-final','recarga-fria','datos-usuario-restaurados']:
  assert json.loads(z.read('docs/validation/items-colisiones/'+report+'.json'))['passed'],report
 assert not any(n.startswith(('Promocional/','docs/academica/')) for n in names)
 assert z.testzip() is None
digest=hashlib.sha256()
with path.open('rb') as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b''):digest.update(chunk)
h=digest.hexdigest()
(delivery/'TimeOut_Avance_18Nov2026.sha256').write_text(h+'  '+path.name+'\n',encoding='ascii')
(delivery/'VALIDACION_ENTREGA.json').write_text(json.dumps({'passed':True,'zip':path.name,'size_bytes':path.stat().st_size,'sha256':h,'crc_all_entries_passed':True,'entry_count':len(names),'blueprint_fiches':expected_fiches,'no_saved_debug_symbols_or_editor_helper':True,'includes_spanish_technical_docs':True,'scope':'Sólo Unreal, sin redes sociales ni promoción'},ensure_ascii=False,indent=2),encoding='utf-8')
print('ZIP_VERIFICADO',path.stat().st_size,h)

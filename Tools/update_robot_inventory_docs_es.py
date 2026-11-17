"""Actualiza el estado técnico y el alcance vigente solicitado por el propietario."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];docs=ROOT/'docs'
for file in ['LEEME_EQUIPO.md','PROJECT_CONTEXT.md','HANDOFF.md','WORK_ITEMS.md','PENDIENTES_ENTREGA_FINAL.md','GOVERNANCE.md']:
 p=docs/file;s=p.read_text(encoding='utf-8')
 s=s.replace('comercio con Bruno E/RB','conversión de energía con BRUNO E/RB').replace('Bruno vende por créditos','BRUNO convierte créditos en energía').replace('Bruno técnico','BRUNO robot de apoyo').replace('hablar/comprar','hablar/convertir energía')
 s=s.replace('Cerca de Bruno, E/RB inicia la conversación; repetir durante ella compra un botiquín por tres créditos si hay saldo.','Cerca de BRUNO, E/RB explica que es un robot anclado a la red. Repetir convierte tres créditos en energía y fabrica un botiquín en tres segundos. Un trabajo activo no admite otro consumo. La pausa detiene proceso y animación; el checkpoint conserva energía y progreso. No cobra por ayudar ni puede abandonar su pedestal.')
 s=s.replace('compra al técnico','conversión con el robot')
 banner='> **Estado vigente, 17/11 — revisión de BRUNO, cielo e inventario.** Alcance: requisitos de Unreal y documentación técnica en español. Redes, campaña, video promocional y documentos administrativos quedan fuera por indicación expresa del propietario. Se conserva el diseño de los menús; se rediseña el inventario. BRUNO usa modelo mecánico original, convierte 3 créditos en energía y fabrica 1 botiquín en 3 s. Ver [ROBOT_CIELO_INVENTARIO.md](ROBOT_CIELO_INVENTARIO.md). El texto posterior conserva historial cuando describe otra revisión.\n\n'
 s=re.sub(r'^> \*\*Estado vigente, 17/11 — revisión de BRUNO.*?\n\n','',s,flags=re.S)
 lines=s.splitlines(keepends=True);lines.insert(2,banner);p.write_text(''.join(lines),encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s='\n'.join(line for line in s.splitlines() if not any(x in line for x in ['Documentación académica','Campaña publicitaria','Video local:']))+'\n';s+='\nLa revisión actual conserva los menús y mejora el inventario. BRUNO es un robot original con conversión de energía y fabricación persistente. El ciclo solar corrige las unidades de intensidad y añade noche estrellada/luna. [Cambios, flujo y pruebas](docs/ROBOT_CIELO_INVENTARIO.md). Los requisitos ajenos a Unreal quedan fuera del alcance solicitado.\n';p.write_text(s,encoding='utf-8')
p=docs/'REVISION_REQUISITOS_2026-11-16.md';s=p.read_text(encoding='utf-8');lines=s.splitlines();result=[]
for line in lines:
 if line.startswith('**Cierre técnico del 17/11.**'):
  line='**Revisión vigente del 17/11.** Se mantienen las pruebas previas de primera persona, diez montajes, rehén, doce enemigos, balizas, destrucción y extracción. Esta revisión añade inventario con tarjetas/iconos y tipografía propia; robot BRUNO original, conversión persistente y cielo en lux con luna/estrellas. BP_CinematicDirector conserva exactamente la lógica de sus 207 nodos. Evidencia nueva en `validation/robot-cielo-inventario/` y `validation/cinematic-layout.json`. Las evidencias previas describen su fecha y condiciones; no se presentan como pruebas nuevas. El informe de empaquetado se actualiza después de construir.'
 elif re.match(r'\d+\. \*\*',line):
  title=line.split('**')[1]
  if any(x in title.lower() for x in ['campaña','redes','cronograma con','revisión del avance','video promocional','temática, diseño']):line=line.split('**',2)[0]+'**'+title+'** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.'
  elif 'Documentación completa con cronograma' in title:line='7. **Documentación técnica completa.** Guía española, catálogo por asset, contratos, herramientas y pruebas reproducibles. El estado de desarrollo se mantiene en WORK_ITEMS; cronograma académico/nominal fuera del alcance.'
 line=line.replace('Bruno vende por créditos','BRUNO convierte tres créditos en energía y fabrica un botiquín en tres segundos').replace('Bruno técnico','BRUNO robot').replace('conversación/compra','conversación/conversión').replace('antes de comprar','antes de convertir')
 result.append(line)
s='\n'.join(result)+'\n';s=s[:s.index('## Lo que requiere evidencia externa')]+'''## Límites que corresponden a Unreal

Hace falta mando físico y prueba en la PC de exposición para acreditar esos dispositivos. La valoración estética y la autoría académica pertenecen al equipo/evaluador. El funcionamiento comprobado y los fuentes asistidos no acreditan por sí solos la autoría de un estudiante. Publicaciones, cuentas, presupuestos, video y cronograma administrativo están fuera de esta intervención por indicación del propietario.
''';p.write_text(s,encoding='utf-8')
print('ROBOT_INVENTORY_DOCS_SCOPE_UPDATED')

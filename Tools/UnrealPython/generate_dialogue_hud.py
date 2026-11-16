"""Reviewable Blueprint source: contextual retro dialogue, typewriter, dismiss/reveal and audio.

Presentation only: reads existing mission/Blackboard state, never changes AI or objectives.
"""
import textwrap
from generate_combat_graphs import CombatGraph,ACTOR,OBJECT,ref,q
from generate_wave_graphs import ZONE,HOSTAGE
from generate_delivery_graphs import DIRECTOR,HEALTH
HUD='/Script/Engine.HUD'
MATH='/Script/Engine.KismetMathLibrary'
STRING='/Script/Engine.KismetStringLibrary'
AUDIO='/Game/ThirdPerson/Audio/'
FONT='/Game/ThirdPerson/Blueprints/Entrega/F_DialogueMono.F_DialogueMono'
MESSAGES=[
 ('','', ''),
 ('TIME OUT','Hay alguien que necesita tu ayuda. Acércate al rehén para rescatarlo.','[E / RB] Interactuar al acercarte'),
 ('REHÉN','Por favor, sácame de aquí. No puedo salir solo.','[E / RB] Rescatar'),
 ('REHÉN','Te seguiré. Si veo enemigos, buscaré un refugio. Cuando esté a salvo, tendrás que volver a llamarme.','WASD: moverte   Ratón: cámara'),
 ('REHÉN','¡Enemigos! Buscaré un lugar seguro. Despeja la zona y después vuelve por mí.','Despeja la zona y recupera al rehén'),
 ('REHÉN','El rehén espera en su refugio. Acércate cuando no haya enemigos para que vuelva a seguirte.','[E / RB] Llamarlo al acercarte'),
 ('REHÉN','Ya estoy a salvo. ¿Seguimos?','[E / RB] Volver a seguir'),
 ('REHÉN','Todavía hay enemigos cerca. No es seguro salir.','Elimina las amenazas cercanas'),
 ('ALERTA','Estás por entrar en una zona de combate. Entrar con el rehén cerca activa 2 oleadas de 2 enemigos.','Prepárate antes de entrar'),
 ('ALERTA','Esta zona necesita al rehén para activarse. Entra con él siguiéndote a menos de 6 metros.','Recupera al rehén y vuelve con él'),
 ('OLEADA 1 / 2','El rehén busca refugio cerca. Combina golpes rápidos y pesados para despejar la zona.','Clic izquierdo: ligero   Clic derecho: pesado'),
 ('OLEADA 2 / 2','Otro par de orbitadores. Despeja el área para abrir la barrera.','Clic izquierdo: ataque ligero'),
 ('OLEADA 1 / 2','El rehén busca refugio. Los embestidores reciben ataques ligeros y pesados.','Clic izquierdo: ligero   Clic derecho: pesado'),
 ('OLEADA 2 / 2','Cuidado con las cargas. Ataca durante su preparación o su retirada.','Clic izquierdo: ligero   Clic derecho: pesado'),
 ('UNA BREVE CALMA','La siguiente oleada llega en 3 segundos. Aprovecha para tomar distancia.','Prepárate para la siguiente oleada'),
 ('ZONA DESPEJADA','No quedan enemigos en esta zona. Recupera al rehén y activa la primera baliza.','[E / RB] Interactuar al acercarte'),
 ('ZONA DESPEJADA','No quedan enemigos en esta zona. Recupera al rehén y activa la segunda baliza.','[E / RB] Interactuar al acercarte'),
 ('BALIZA 1','Esta baliza ya puede activarse. Su señal te permitirá avanzar hacia la salida.','[E / RB] Activar baliza'),
 ('BALIZA 2','Esta baliza ya puede activarse. Su señal te permitirá avanzar hacia la salida.','[E / RB] Activar baliza'),
 ('BALIZA 3','La última baliza está lista. Actívala para preparar la extracción.','[E / RB] Activar baliza'),
 ('BALIZA ACTIVADA','Primera baliza activada. Lleva al rehén a la siguiente zona.','Continúa con el rehén'),
 ('BALIZA ACTIVADA','Segunda baliza activada. Encuentra la última baliza y mantén al rehén contigo.','Continúa con el rehén'),
 ('EXTRACCIÓN','Las tres balizas responden. Llega a la salida azul junto con el rehén.','Llegar solo no completa la misión'),
 ('FALTA ALGUIEN','No puedes dejarlo atrás. Reúnete con el rehén y entra con él a la salida.','[E / RB] Recuperar al rehén'),
 ('A SALVO','Lo lograron. El rehén está a salvo.','[R] Reintentar    [ENTER] Menú'),
 ('OTRA OPORTUNIDAD','Esta vez no pudo ser. Todavía puedes volver a intentarlo.','[R] Reintentar    [ENTER] Menú'),
 ('REHÉN PERDIDO','El rehén no sobrevivió. Mantente cerca y protege su retirada.','[R] Reintentar    [ENTER] Menú'),
 ('REHÉN','Estoy activando la baliza. Dame tres segundos y cuida mi espalda.','Activación en curso'),
 ('MARTILLO MEJORADO','La baliza cargó tu martillo. Ya está equipado: úsalo para destruir la puerta de esta zona.','Clic derecho: golpear la puerta'),
 ('PUERTA SELLADA','Sólo el rehén puede cargar la baliza. Primero despeja sus oleadas y luego llévalo hasta ella.','Recupera al rehén y escolta su avance'),
 ('ABRE EL CAMINO','El sello está debilitado. Dos golpes pesados con el martillo abrirán el paso.','Clic derecho: destruir la puerta')]
MESSAGES[11]=('OLEADA 2 / 2','Otro par de orbitadores. Despeja el área para cargar el martillo y abrir la puerta.','Clic izquierdo: ligero   Clic derecho: pesado')
for i in [15,16]:MESSAGES[i]=('ZONA DESPEJADA','No quedan enemigos. Recupera al rehén y llévalo a la baliza; él la activará al acercarse.','[E / RB] Llamar al rehén cerca')
for i in [17,18,19]:MESSAGES[i]=('BALIZA','Sólo el rehén puede usarla. Acércalo después de despejar la horda y espera tres segundos.','Escolta al rehén hasta la baliza')
for i in [20,21,22]:MESSAGES[i]=('SIGUE AVANZANDO','Protege al rehén y acompáñalo hasta la siguiente baliza. Las puertas requieren su carga.','Continúa con el rehén')
for i in [15,16]:MESSAGES[i]=('ZONA DESPEJADA','El martillo está cargado. Rompe la puerta con dos golpes pesados y continúa con el rehén.','Clic derecho: golpear la puerta')
for i in [17,18,19]:MESSAGES[i]=('SECUENCIA DE BALIZAS','Sigue el orden de la pantalla. Sólo la baliza indicada acepta la canalización del rehén.','Llévalo a la señal azul y espera tres segundos')
for i in [20,21]:MESSAGES[i]=('BALIZA ACTIVADA','Sigue la secuencia indicada en pantalla. Lleva al rehén hasta la siguiente señal azul.','Las balizas verdes ya están activadas')
MESSAGES[22]=('EXTRACCIÓN','Secuencia completada. Rompe la última puerta y llega a la salida azul con el rehén.','Clic derecho: romper la puerta final')
MESSAGES[25]=('OTRA OPORTUNIDAD','Esta vez no pudo ser. Un nuevo intento sortea otra secuencia y reinicia el cronómetro.','[R] Nuevo intento    [ENTER] Menú')
MESSAGES[26]=('REHÉN PERDIDO','El rehén no sobrevivió. Mantente cerca y protege su retirada.','[R] Nuevo intento    [ENTER] Menú')
MESSAGES[28]=('MARTILLO CARGADO','Tu martillo está equipado. Dos golpes pesados abren la puerta habilitada.','Clic derecho: golpear la puerta')
class DialogueGraph(CombatGraph):
    def node(self,kind,props=(),**pos):
        i=len(self.nodes);pos.setdefault('x',(i%9)*380);pos.setdefault('y',(i//9)*310)
        return super().node(kind,props,**pos)
g=DialogueGraph()
KINDS={**dict.fromkeys(['CurrentDialog','LastDialog','DismissedDialog','VisibleCharacters','LastHostageHitSerial'],'int'),**dict.fromkeys(['DialogStarted','LastBeepAt','LastHealth','CharactersPerSecond','HoldSeconds','UIAudioVolume','HurtPulseUntil','HostageHurtUntil','HostageAlertCooldown','EnemyHitUntil','LastEnemyDamage'],'real'),**dict.fromkeys(['ForceReveal','DialogueVisible','HostageSpeaking','HostagePromptVisible','HostagePromptInRange'],'bool'),**dict.fromkeys(['FullText','VisibleText','Speaker','ActionHint'],'string')}
def v(name):
    cat=KINDS[name];return (g.get(name,cat,sub='double' if cat=='real' else ''),name)
def wire(value,node,pin):
    if isinstance(value,tuple):
        if value[0].pins[value[1]]['cat']=='int' and node.pins[pin]['cat']=='real':
            value=call(MATH,'Conv_IntToDouble',[('InInt','int',value)])
        g.wire(*value,node,pin)
    else:node.pins[pin]['default']=str(value).lower() if isinstance(value,bool) else str(value)
def call(owner,name,inputs,output='ReturnValue',cat='real',obj=None,pure=True,static=True):
    n=g.call(owner,name,pure=pure,static=static)
    for pin,typ,value in inputs:
        n.pin(pin,typ,sub='double' if typ=='real' else '')
        wire(value,n,pin)
    n.pin(output,cat,obj=obj,sub='double' if cat=='real' else '',out=True)
    return n,output
def calc(fn,a,b,cat='real'):
    return call(MATH,fn,[('A',cat,a),('B',cat,b)],cat=cat)
def cmp(fn,a,b,cat='int'):
    return call(MATH,fn,[('A',cat,a),('B',cat,b)],cat='bool')
def both(a,b):return calc('BooleanAND',a,b,'bool')
def either(a,b):return calc('BooleanOR',a,b,'bool')
def neg(a):return call(MATH,'Not_PreBool',[('A','bool',a)],cat='bool')
def pick(cond,a,b,cat='int'):
    return call(MATH,'SelectInt' if cat=='int' else 'SelectFloat',[('A',cat,a),('B',cat,b),('bPickA','bool',cond)],cat=cat)
def table(index,values,cat='string',obj=None):
    n=g.node('K2Node_Select',['NumOptionPins='+str(len(values)),'IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue',cat,obj=obj,out=True);wire(index,n,'Index')
    for i,value in enumerate(values):
        n.pin('Option '+str(i),cat,obj=obj)
        if cat=='object':n.pins['Option '+str(i)]['default_obj']=value
        else:wire(value,n,'Option '+str(i))
    return n,'ReturnValue'
def save(prev,name,value,pin='then'):
    cat=KINDS[name];n=g.set(name,cat,None,sub='double' if cat=='real' else '');g.chain(prev,n,pin);wire(value,n,name);return n
def branch(prev,condition,pin='then'):
    n=g.branch();g.chain(prev,n,pin);wire(condition,n,'Condition');return n
def sound(prev,name,volume=None,pin='then',spawn=False):
    n=g.call('/Script/Engine.GameplayStatics','SpawnSound2D' if spawn else 'PlaySound2D',static=True).pin('Sound','object',obj='/Script/Engine.SoundBase').pin('VolumeMultiplier','real',sub='float',default='.32').pin('PitchMultiplier','real',sub='float',default='1').pin('StartTime','real',sub='float',default='0').pin('ConcurrencySettings','object',obj='/Script/Engine.SoundConcurrency').pin('bIsUISound','bool',default='true')
    if isinstance(name,tuple):wire(name,n,'Sound')
    else:n.pins['Sound']['default_obj']=AUDIO+'SW_'+name+'.SW_'+name
    if volume is not None:wire(volume,n,'VolumeMultiplier')
    if spawn:
        del n.pins['bIsUISound']
        n.pin('bPersistAcrossLevelTransition','bool',default='false').pin('bAutoDestroy','bool',default='true').pin('ReturnValue','object',obj='/Script/Engine.AudioComponent',out=True)
    else:n.pin('OwningActor','object',obj=ACTOR)
    g.chain(prev,n,pin);return n
# Cache actors once; gameplay remains entirely in existing director and behavior trees.
begin=g.event(ACTOR,'ReceiveBeginPlay');prev=begin
for name,cls in [('CachedDirector',DIRECTOR),('CachedHostage',HOSTAGE)]:
    n=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=cls).pin('ReturnValue','object',obj=cls,out=True);g.chain(prev,n)
    s=g.set(name,'object',None,obj=cls);g.chain(n,s);g.wire(n,'ReturnValue',s,name);prev=s
initial_host_hit=g.get('DamageNoticeSerial','int',owner=HOSTAGE);g.wire(s,'Output_Get',initial_host_hit,'self')
prev=save(prev,'LastHostageHitSerial',(initial_host_hit,'DamageNoticeSerial'))
for beacon_i in [1,2,3]:
    beacon_class='/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C'
    raw_beacon=g.get('Baliza'+str(beacon_i),'object',owner=DIRECTOR,obj='/Script/Engine.StaticMeshActor');director_cache=g.get('CachedDirector','object',obj=DIRECTOR);g.wire(director_cache,'CachedDirector',raw_beacon,'self')
    cast_beacon=g.cast(beacon_class);g.chain(prev,cast_beacon);g.wire(raw_beacon,'Baliza'+str(beacon_i),cast_beacon,'Object')
    cache_beacon=g.set('CachedBeacon'+str(beacon_i),'object',None,obj=beacon_class);g.chain(cast_beacon,cache_beacon);g.wire(cast_beacon,'AsBP_BeaconEntrega',cache_beacon,'CachedBeacon'+str(beacon_i));prev=cache_beacon
ambient=sound(prev,'Ambience',.18,spawn=True)
cache=g.set('AmbientAudio','object',None,obj='/Script/Engine.AudioComponent');g.chain(ambient,cache);g.wire(ambient,'ReturnValue',cache,'AmbientAudio')
# Enter reveals the sentence immediately; a second press dismisses this context.
key=g.key('Enter');length=call(STRING,'Len',[('S','string',v('FullText'))],cat='int')
reading=branch(key,cmp('Less_IntInt',v('VisibleCharacters'),length),'Pressed')
save(reading,'ForceReveal',True)
save(reading,'DismissedDialog',v('CurrentDialog'),'else')
draw=g.event(HUD,'ReceiveDrawHUD').pin('SizeX','int',out=True).pin('SizeY','int',out=True)
director=g.get('CachedDirector','object',obj=DIRECTOR);hostage=g.get('CachedHostage','object',obj=HOSTAGE);player=g.player()
ready=both((g.valid(director,'CachedDirector'),'ReturnValue'),(g.valid(hostage,'CachedHostage'),'ReturnValue'))
valid=branch(draw,ready)
step=g.get('Paso','int',owner=DIRECTOR);g.wire(director,'CachedDirector',step,'self');step=(step,'Paso')
bb=g.blackboard(hostage,'CachedHostage')
following=(g.bbget(bb,'bAccompanying'),'ReturnValue');rescued=(g.bbget(bb,'bRescued'),'ReturnValue')
unsafe=either((g.bbget(bb,'bMustFlee'),'ReturnValue'),(g.bbget(bb,'bEnemyNear'),'ReturnValue'))
hdist=(g.dist(hostage,'CachedHostage',player,'ReturnValue'),'ReturnValue');nearhostage=cmp('LessEqual_DoubleDouble',hdist,400,'real')
zones=[]
for i in [1,2]:
    z=g.get('Zona'+str(i),'object',owner=DIRECTOR,obj=ZONE);g.wire(director,'CachedDirector',z,'self');zones.append((z,'Zona'+str(i)))
cleared=[]
for z in zones:
    n=g.get('bCleared','bool',owner=ZONE);wire(z,n,'self');cleared.append((n,'bCleared'))
zoneindex=pick(cleared[0],1,0)
zone=table(zoneindex,[None,None],'object',ZONE)
for i,z in enumerate(zones):wire(z,zone[0],'Option '+str(i))
def zget(name):
    n=g.get(name,'int',owner=ZONE);wire(zone,n,'self');return n,name
phase=zget('Phase');wave=zget('CurrentWave');living=zget('LivingCount')
relevant=both(cmp('Less_IntInt',step,4),neg(both(*cleared)))
zdist=(g.dist(zone[0],zone[1],player,'ReturnValue'),'ReturnValue')
nearzone=cmp('LessEqual_DoubleDouble',zdist,1700,'real')
overlap=g.call(ACTOR,'IsOverlappingActor',pure=True).pin('Other','object',obj=ACTOR).pin('ReturnValue','bool',out=True);wire(zone,overlap,'self');g.wire(player,'ReturnValue',overlap,'Other')
# Context priorities: escort, nearby entry, wave, clear, safe interaction, beacon, outcome.
default=table(step,[3,20,21,22,24,25,26],'int')
context=pick(following,default,pick(rescued,pick(nearhostage,6,5),pick(nearhostage,2,1)))
context=pick(both(unsafe,rescued),4,context)
idlezone=both(relevant,cmp('EqualEqual_IntInt',phase,0))
context=pick(both(idlezone,both(following,nearzone)),8,context)
context=pick(both(idlezone,both((overlap,'ReturnValue'),neg(following))),9,context)
waveid=calc('Add_IntInt',10,calc('Add_IntInt',calc('Multiply_IntInt',zoneindex,2,'int'),calc('Subtract_IntInt',wave,1,'int'),'int'),'int')
context=pick(both(relevant,cmp('EqualEqual_IntInt',phase,1)),waveid,context)
context=pick(both(relevant,cmp('EqualEqual_IntInt',phase,2)),14,context)
context=pick(both(relevant,cmp('EqualEqual_IntInt',phase,3)),calc('Add_IntInt',15,zoneindex,'int'),context)
context=pick(both(nearhostage,both(neg(following),neg(unsafe))),pick(rescued,6,2),context)
beacons=[]
for i in [1,2,3]:
    b=g.get('Baliza'+str(i),'object',owner=DIRECTOR,obj='/Script/Engine.StaticMeshActor');g.wire(director,'CachedDirector',b,'self');beacons.append((b,'Baliza'+str(i)))
beacon_node=g.get('CurrentBeacon','object',owner=DIRECTOR,obj='/Script/Engine.StaticMeshActor');g.wire(director,'CachedDirector',beacon_node,'self')
beacon=(beacon_node,'CurrentBeacon')
bdist=(g.dist(beacon[0],beacon[1],player,'ReturnValue'),'ReturnValue')
beaconready=both(cmp('Less_IntInt',step,3),both(*cleared))
context=pick(both(beaconready,cmp('LessEqual_DoubleDouble',bdist,250,'real')),calc('Add_IntInt',17,step,'int'),context)
exit=g.get('Salida','object',owner=DIRECTOR,obj='/Script/Engine.StaticMeshActor');g.wire(director,'CachedDirector',exit,'self')
edist=(g.dist(exit,'Salida',player,'ReturnValue'),'ReturnValue')
alone=both(cmp('EqualEqual_IntInt',step,3),both(cmp('LessEqual_DoubleDouble',edist,300,'real'),either(neg(following),cmp('Greater_DoubleDouble',hdist,600,'real'))))
context=pick(alone,23,context)
hero_class='/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C'
hero=g.cast(hero_class);g.chain(valid,hero)
g.wire(player,'ReturnValue',hero,'Object')
pending=g.get('bDoorPending','bool',owner=hero_class);g.wire(hero,'AsBP_PlayerEntrega',pending,'self');pending=(pending,'bDoorPending')
upuntil=g.get('UpgradeUntil','real',owner=hero_class,sub='double');g.wire(hero,'AsBP_PlayerEntrega',upuntil,'self')
game_now=call('/Script/Engine.GameplayStatics','GetTimeSeconds',[])
context=pick(pending,30,context)
context=pick(cmp('Greater_DoubleDouble',(upuntil,'UpgradeUntil'),game_now,'real'),28,context)
using=g.get('bUsingBeacon','bool',owner=HOSTAGE);g.wire(hostage,'CachedHostage',using,'self')
context=pick((using,'bUsingBeacon'),27,context)
context=pick(cmp('GreaterEqual_IntInt',step,4),calc('Add_IntInt',20,step,'int'),context)
current=save(hero,'CurrentDialog',context)
texts=['\n'.join('* '+line for line in textwrap.wrap(m[1],width=58)) for m in MESSAGES]
prev=current
for name,values in [('FullText',texts),('Speaker',[m[0] for m in MESSAGES]),('ActionHint',[m[2] for m in MESSAGES])]:prev=save(prev,name,table(v('CurrentDialog'),values))
now=call('/Script/Engine.GameplayStatics','GetRealTimeSeconds',[])
changed=branch(prev,cmp('NotEqual_IntInt',v('CurrentDialog'),v('LastDialog')))
prev=save(changed,'LastDialog',v('CurrentDialog'));prev=save(prev,'DialogStarted',now);prev=save(prev,'ForceReveal',False);prev=save(prev,'DismissedDialog',-1);prev=save(prev,'LastBeepAt',now)
names=['Open']*len(MESSAGES)
for i in [3]:names[i]='Rescue'
for i in [4,8,10,11,12,13,14]:names[i]='Alert'
for i in [15,16,20,21,22]:names[i]='Clear'
names[24]='Victory';names[25]='Defeat'
notification=table(v('CurrentDialog'),[AUDIO+'SW_'+name+'.SW_'+name for name in names],'object','/Script/Engine.SoundBase')
played=sound(prev,notification,v('UIAudioVolume'))
age=calc('Subtract_DoubleDouble',now,v('DialogStarted'))
rate=v('CharactersPerSecond');progress=calc('Multiply_DoubleDouble',age,rate)
count=call(MATH,'FFloor',[('A','real',progress)],cat='int')
count=pick(v('ForceReveal'),length,calc('Min',length,count,'int'))
substring=call(STRING,'Left',[('SourceString','string',v('FullText')),('Count','int',count)],cat='string')
update=save(played,'VisibleText',substring);g.chain(changed,update,'else')
duration=calc('Add_DoubleDouble',calc('Divide_DoubleDouble',length,rate),v('HoldSeconds'))
pers=table(v('CurrentDialog'),[i in [2,6,17,18,19,23,24,25,26,27,28,30] for i in range(len(MESSAGES))],'bool')
visible=both(cmp('NotEqual_IntInt',v('DismissedDialog'),v('CurrentDialog')),either(pers,cmp('Less_DoubleDouble',age,duration,'real')))
visible_set=save(update,'DialogueVisible',visible)
typing=both(v('DialogueVisible'),both(neg(v('ForceReveal')),both(cmp('Greater_IntInt',count,v('VisibleCharacters')),cmp('Greater_DoubleDouble',calc('Subtract_DoubleDouble',now,v('LastBeepAt')),.07,'real'))))
is_hostage=call(STRING,'EqualEqual_StrStr',[('A','string',v('Speaker')),('B','string','REHÉN')],cat='bool')
voice_state=save(visible_set,'HostageSpeaking',is_hostage)
typebranch=branch(voice_state,typing)
voice_index=calc('Percent_IntInt',v('VisibleCharacters'),3,'int')
host_voice=table(voice_index,[AUDIO+'SW_HostageVoice_'+str(i)+'.SW_HostageVoice_'+str(i) for i in [1,2,3]],'object','/Script/Engine.SoundBase')
voice=table(pick(is_hostage,1,0),[AUDIO+'SW_Text.SW_Text',None],'object','/Script/Engine.SoundBase');wire(host_voice,voice[0],'Option 1')
cue=g.set('CurrentVoiceCue','object',None,obj='/Script/Engine.SoundBase');wire(voice,cue,'CurrentVoiceCue');g.chain(typebranch,cue)
beep=sound(cue,voice,calc('Multiply_DoubleDouble',v('UIAudioVolume'),pick(is_hostage,.75,.36,'real')))
pitch=call(MATH,'RandomFloatInRange',[('Min','real',.94),('Max','real',1.08)]);wire(pitch,beep,'PitchMultiplier')
last=save(beep,'LastBeepAt',now)
chars=save(last,'VisibleCharacters',count);g.chain(typebranch,chars,'else')
# Damage feedback reads the existing player health component.
health=g.call(ACTOR,'GetComponentByClass',pure=True).pin('ComponentClass','class',obj='/Script/Engine.ActorComponent',default_obj=HEALTH).pin('ReturnValue','object',obj=HEALTH,out=True);g.wire(player,'ReturnValue',health,'self')
hp=g.get('Health','real',owner=HEALTH,sub='double');g.wire(health,'ReturnValue',hp,'self');hp=(hp,'Health')
hurt=branch(chars,cmp('Less_DoubleDouble',hp,v('LastHealth'),'real'))
impact=sound(hurt,'PlayerHurt',calc('Multiply_DoubleDouble',v('UIAudioVolume'),2))
pulse=save(impact,'HurtPulseUntil',calc('Add_DoubleDouble',now,.38))
health_save=save(pulse,'LastHealth',hp);g.chain(hurt,health_save,'else')
# Actual hostage damage renews the warning; the audible alert has its own cooldown.
host_damage_hp=g.get('Health','real',owner=HOSTAGE,sub='double');g.wire(hostage,'CachedHostage',host_damage_hp,'self');host_damage_hp=(host_damage_hp,'Health')
host_hit_serial=g.get('DamageNoticeSerial','int',owner=HOSTAGE);g.wire(hostage,'CachedHostage',host_hit_serial,'self');host_hit_serial=(host_hit_serial,'DamageNoticeSerial')
host_hurt=branch(health_save,cmp('Greater_IntInt',host_hit_serial,v('LastHostageHitSerial')))
host_pulse=save(host_hurt,'HostageHurtUntil',calc('Add_DoubleDouble',now,2.4))
host_sound_ready=branch(host_pulse,cmp('GreaterEqual_DoubleDouble',now,v('HostageAlertCooldown'),'real'))
host_alarm=sound(host_sound_ready,'Alert',calc('Multiply_DoubleDouble',v('UIAudioVolume'),.8))
host_cooldown=save(host_alarm,'HostageAlertCooldown',calc('Add_DoubleDouble',now,1.2))
host_health_save=save(host_cooldown,'LastHostageHitSerial',host_hit_serial);g.chain(host_sound_ready,host_health_save,'else');g.chain(host_hurt,host_health_save,'else')
# Adaptive 900px frame at 1280; monospaced font, white border, no world-space text.
width=(draw,'SizeX');height=(draw,'SizeY')
ratio=calc('Divide_DoubleDouble',width,1280)
scale=call(MATH,'FClamp',[('Value','real',ratio),('Min','real',.65),('Max','real',1.35)])
def mul(a,b):return calc('Multiply_DoubleDouble',a,b)
def add(a,b):return calc('Add_DoubleDouble',a,b)
def sub(a,b):return calc('Subtract_DoubleDouble',a,b)
bw=call(MATH,'FMin',[('A','real',mul(900,scale)),('B','real',sub(width,40))]);bh=mul(180,scale)
x=mul(sub(width,bw),.5);y=sub(sub(height,bh),mul(24,scale))
def rect(prev,x,y,w,h,color):
    n=g.call(HUD,'DrawRect').pin('RectColor','struct',obj='/Script/CoreUObject.LinearColor')
    wire(color,n,'RectColor')
    for pin,value in [('ScreenX',x),('ScreenY',y),('ScreenW',w),('ScreenH',h)]:n.pin(pin,'real',sub='float');wire(value,n,pin)
    g.chain(prev,n);return n
def text(prev,value,x,y,size=1,color='(R=1,G=1,B=1,A=1)'):
    n=g.call(HUD,'DrawText').pin('Text','string').pin('TextColor','struct',obj='/Script/CoreUObject.LinearColor',default=color).pin('Font','object',obj='/Script/Engine.Font',default_obj=FONT).pin('bScalePosition','bool',default='false')
    wire(value,n,'Text')
    for pin,value in [('ScreenX',x),('ScreenY',y),('Scale',mul(size*.85,scale))]:n.pin(pin,'real',sub='float');wire(value,n,pin)
    g.chain(prev,n);return n
chipx=sub(width,mul(440,scale));chipy=mul(22,scale)
incombat=both(relevant,either(cmp('EqualEqual_IntInt',phase,1),cmp('EqualEqual_IntInt',phase,2)))
# Smooth transparent corners, immediate onset and a short squared fade; center stays clear.
fade=call(MATH,'FClamp',[('Value','real',calc('Divide_DoubleDouble',sub(v('HurtPulseUntil'),now),.38)),('Min','real',0),('Max','real',1)])
color=call(MATH,'MakeColor',[('R','real',.8),('G','real',.015),('B','real',.015),('A','real',mul(.3,mul(fade,fade)))],cat='struct',obj='/Script/CoreUObject.LinearColor')
overlay=g.call(HUD,'DrawTexture').pin('Texture','object',obj='/Script/Engine.Texture',default_obj='/Game/ThirdPerson/Blueprints/Entrega/FX/T_DamageCorners.T_DamageCorners').pin('TintColor','struct',obj='/Script/CoreUObject.LinearColor').pin('BlendMode','byte',obj='/Script/Engine.EBlendMode',default='BLEND_Translucent').pin('bScalePosition','bool',default='false')
wire(color,overlay,'TintColor')
for pin,value in [('ScreenX',0),('ScreenY',0),('ScreenW',width),('ScreenH',height),('TextureU',0),('TextureV',0),('TextureUWidth',1),('TextureVHeight',1),('Scale',1),('Rotation',0)]:overlay.pin(pin,'real',sub='float');wire(value,overlay,pin)
overlay.pin('RotPivot','struct',obj='/Script/CoreUObject.Vector2D',default='(X=0,Y=0)');g.chain(host_health_save,overlay)
chip=rect(overlay,chipx,chipy,mul(418,scale),mul(pick(incombat,142,112),scale),'(R=0,G=0,B=0,A=.8)')
objectives=table(pick(both(*cleared),1,0),['DESPEJA LAS DOS ZONAS','ACTIVA LA SECUENCIA DE BALIZAS'])
objectives=table(pick(cmp('GreaterEqual_IntInt',step,3),1,0),[objectives,table(step,['','','','ESCOLTA A LA EXTRACCIÓN','REHÉN A SALVO','FIN DEL INTENTO','REHÉN PERDIDO'])])
objectives=table(pick(pending,1,0),[objectives,'MARTILLO: ABRE EL PASO'])
hpnode=g.get('Health','real',owner=HOSTAGE,sub='double');g.wire(hostage,'CachedHostage',hpnode,'self');host_hp=(hpnode,'Health')
maxnode=g.get('MaxHealth','real',owner=HOSTAGE,sub='double');g.wire(hostage,'CachedHostage',maxnode,'self');maxhp=(maxnode,'MaxHealth')
ratiohp=call(MATH,'FClamp',[('Value','real',calc('Divide_DoubleDouble',host_hp,call(MATH,'FMax',[('A','real',maxhp),('B','real',1)]))),('Min','real',0),('Max','real',1)])
bar=rect(chip,mul(24,scale),mul(78,scale),mul(224,scale),mul(49,scale),'(R=0,G=0,B=0,A=.8)')
bar=rect(bar,mul(34,scale),mul(108,scale),mul(204,scale),mul(9,scale),'(R=.12,G=.12,B=.12,A=1)')
hpcolor=call(MATH,'SelectColor',[('A','struct','(R=1,G=.15,B=.1,A=1)'),('B','struct','(R=.1,G=.75,B=.9,A=1)'),('bPickA','bool',cmp('LessEqual_DoubleDouble',ratiohp,.3,'real'))],cat='struct',obj='/Script/CoreUObject.LinearColor')
for pin in ['A','B']:hpcolor[0].pins[pin]['obj']='/Script/CoreUObject.LinearColor'
bar=rect(bar,mul(34,scale),mul(108,scale),mul(calc('Multiply_DoubleDouble',204,ratiohp),scale),mul(9,scale),hpcolor)
hpstr=call(STRING,'Conv_IntToString',[('InInt','int',call(MATH,'FFloor',[('A','real',host_hp)],cat='int'))],cat='string')
maxstr=call(STRING,'Conv_IntToString',[('InInt','int',call(MATH,'FFloor',[('A','real',maxhp)],cat='int'))],cat='string')
label=call(STRING,'Concat_StrStr',[('A','string','REHÉN   '),('B','string',hpstr)],cat='string')
label=call(STRING,'Concat_StrStr',[('A','string',label),('B','string',' / ')],cat='string')
label=call(STRING,'Concat_StrStr',[('A','string',label),('B','string',maxstr)],cat='string')
bar=text(bar,label,mul(34,scale),mul(85,scale),1.1)
# Screen-projected floating key: compact, camera facing, and hidden while following,
# fleeing, using a beacon, dead, behind the camera or occluded by a wall.
pos=g.location(hostage,'CachedHostage')
above=g.call(MATH,'Add_VectorVector',pure=True,static=True).pin('A','struct',obj='/Script/CoreUObject.Vector').pin('B','struct',obj='/Script/CoreUObject.Vector',default='0,0,130').pin('ReturnValue','struct',obj='/Script/CoreUObject.Vector',out=True);g.wire(pos,'ReturnValue',above,'A')
project=g.call(HUD,'Project',pure=True).pin('Location','struct',obj='/Script/CoreUObject.Vector').pin('bClampToZeroPlane','bool',default='false').pin('ReturnValue','struct',obj='/Script/CoreUObject.Vector',out=True);g.wire(above,'ReturnValue',project,'Location')
split=g.call(MATH,'BreakVector',pure=True,static=True).pin('InVec','struct',obj='/Script/CoreUObject.Vector').pin('X','real',sub='double',out=True).pin('Y','real',sub='double',out=True).pin('Z','real',sub='double',out=True);g.wire(project,'ReturnValue',split,'InVec')
pc=g.call('/Script/Engine.GameplayStatics','GetPlayerController',pure=True,static=True).pin('PlayerIndex','int',default='0').pin('ReturnValue','object',obj='/Script/Engine.PlayerController',out=True)
sight=g.sight(pc,'ReturnValue',hostage,'CachedHostage')
dead=g.get('bIsDead','bool',owner=HOSTAGE);g.wire(hostage,'CachedHostage',dead,'self')
eligible=both(neg(following),both(neg(unsafe),both(neg((dead,'bIsDead')),neg((using,'bUsingBeacon')))))
eligible=both(eligible,both(cmp('Less_IntInt',step,4),cmp('LessEqual_DoubleDouble',hdist,1200,'real')))
onscreen=both(cmp('Greater_DoubleDouble',(split,'Z'),0,'real'),both(cmp('Greater_DoubleDouble',(split,'X'),60,'real'),cmp('Less_DoubleDouble',(split,'X'),sub(width,60),'real')))
onscreen=both(onscreen,both(cmp('Greater_DoubleDouble',(split,'Y'),35,'real'),cmp('Less_DoubleDouble',(split,'Y'),sub(height,70),'real')))
show=both(eligible,both(onscreen,(sight,'ReturnValue')))
prompt_state=save(bar,'HostagePromptVisible',show);prompt_state=save(prompt_state,'HostagePromptInRange',both(show,nearhostage))
prompt=branch(prompt_state,show)
px=sub((split,'X'),mul(52,scale));py=sub((split,'Y'),mul(22,scale))
badge=rect(prompt,px,py,mul(104,scale),mul(38,scale),'(R=1,G=1,B=1,A=.95)')
badge=rect(badge,add(px,mul(2,scale)),add(py,mul(2,scale)),mul(100,scale),mul(34,scale),'(R=0,G=0,B=0,A=.9)')
badge=text(badge,'E / RB',add(px,mul(12,scale)),add(py,mul(9,scale)),1.5)
channel=branch(badge,(using,'bUsingBeacon'));g.chain(prompt,channel,'else')
channelvalue=g.get('ActivationProgress','real',owner=HOSTAGE,sub='double');g.wire(hostage,'CachedHostage',channelvalue,'self')
channelbar=rect(channel,mul(24,scale),mul(134,scale),mul(224,scale),mul(7,scale),'(R=.12,G=.12,B=.12,A=1)')
channelbar=rect(channelbar,mul(24,scale),mul(134,scale),mul(calc('Multiply_DoubleDouble',224,(channelvalue,'ActivationProgress')),scale),mul(7,scale),'(R=.9,G=.7,B=.15,A=1)')
title=text(channelbar,objectives,add(chipx,mul(12,scale)),add(chipy,mul(9,scale)),1.05);g.chain(channel,title,'else')
from generate_beacon_sequence import ORDERS
order_node=g.get('OrderCode','int',owner=DIRECTOR);g.wire(director,'CachedDirector',order_node,'self');order_code=(order_node,'OrderCode')
order_string=table(order_code,['ORDEN: '+' > '.join('ABC'[i] for i in p) for p in ORDERS])
orderline=text(title,order_string,add(chipx,mul(12,scale)),add(chipy,mul(34,scale)),1.2,'(R=.35,G=.85,B=1,A=1)')
elapsed_node=g.get('MissionElapsed','real',owner=DIRECTOR,sub='double');g.wire(director,'CachedDirector',elapsed_node,'self')
seconds=call(MATH,'FFloor',[('A','real',(elapsed_node,'MissionElapsed'))],cat='int')
minutes=calc('Divide_IntInt',seconds,60,'int');remainder=calc('Percent_IntInt',seconds,60,'int')
def catstr(a,b):return call(STRING,'Concat_StrStr',[('A','string',a),('B','string',b)],cat='string')
def padtime(value):
    s=call(STRING,'Conv_IntToString',[('InInt','int',value)],cat='string')
    return table(pick(cmp('Less_IntInt',value,10),1,0),[s,catstr('0',s)])
clock=catstr('TIEMPO DE MISIÓN: ',catstr(padtime(minutes),catstr(':',padtime(remainder))))
clockline=text(orderline,clock,add(chipx,mul(12,scale)),add(chipy,mul(60,scale)),1.1)
beacon_count=0
for beacon_i in [1,2,3]:
    beacon_class='/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C'
    beacon_node=g.get('CachedBeacon'+str(beacon_i),'object',obj=beacon_class)
    active_node=g.get('bActivated','bool',owner=beacon_class);g.wire(beacon_node,'CachedBeacon'+str(beacon_i),active_node,'self')
    active_int=call(MATH,'Conv_BoolToInt',[('InBool','bool',(active_node,'bActivated'))],cat='int')
    beacon_count=calc('Add_IntInt',beacon_count,active_int,'int')
countstr=call(STRING,'Conv_IntToString',[('InInt','int',beacon_count)],cat='string')
nextname=table(calc('Min',beacon_count,2,'int'),[table(order_code,['ABC'[p[i]] for p in ORDERS]) for i in range(3)])
nextstr=table(pick(cmp('Less_IntInt',beacon_count,3),1,0),['SECUENCIA COMPLETA',catstr('SIGUIENTE: ',nextname)])
nextline=text(clockline,catstr(catstr(catstr('BALIZAS: ',countstr),' / 3   |   '),nextstr),add(chipx,mul(12,scale)),add(chipy,mul(87,scale)),1.05)
active=branch(nextline,incombat)
wc=call(STRING,'Conv_IntToString',[('InInt','int',wave)],cat='string');lc=call(STRING,'Conv_IntToString',[('InInt','int',living)],cat='string')
def concat(a,b):return call(STRING,'Concat_StrStr',[('A','string',a),('B','string',b)],cat='string')
counters=concat(concat(concat('OLEADA ',wc),' / 2    VIVOS '),lc)
counter=text(active,counters,add(chipx,mul(12,scale)),add(chipy,mul(119,scale)),1.0)
box=branch(counter,v('DialogueVisible'));g.chain(active,box,'else')
outer=rect(box,x,y,bw,bh,'(R=1,G=1,B=1,A=1)')
inner=rect(outer,add(x,mul(3,scale)),add(y,mul(3,scale)),sub(bw,mul(6,scale)),sub(bh,mul(6,scale)),'(R=0,G=0,B=0,A=1)')
speaker=text(inner,v('Speaker'),add(x,mul(28,scale)),add(y,mul(15,scale)),1.1)
body=text(speaker,v('VisibleText'),add(x,mul(28,scale)),add(y,mul(43,scale)),1.8)
action=text(body,v('ActionHint'),add(x,mul(28,scale)),add(y,mul(150,scale)),1.1)
end=cmp('Less_IntInt',step,4)
hint=branch(action,end)
text(hint,'ENTER: leer / cerrar',sub(add(x,bw),mul(218,scale)),add(y,mul(150,scale)),1.1)
# A checkpoint status line shares the existing HUD, outside the dialogue box.
from delivery_save_schema import MANAGER
old=list(draw.pins['then']['links']);draw.pins['then']['links']=[]
seq=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True).pin('then_2',out=True).pin('then_3',out=True)
g.chain(draw,seq)
for name,pid in old:
    node=next(n for n in g.nodes if n.name==name)
    pin=next(p for p in node.pins.values() if p['id']==pid)
    pin['links'].remove((draw.name,draw.pins['then']['id']))
    g.chain(seq,node,'then_0',pin['name'])
manager=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True).pin('ActorClass','class',obj='/Script/Engine.Actor',default_obj=MANAGER).pin('ReturnValue','object',obj='/Script/Engine.Actor',out=True)
g.chain(seq,manager,'then_1')
cast=manager
status=g.get('StatusText','string',owner=MANAGER);g.wire(manager,'ReturnValue',status,'self')
line=rect(cast,mul(20,scale),mul(154,scale),mul(720,scale),mul(30,scale),'(R=0,G=0,B=0,A=.82)')
text(line,(status,'StatusText'),mul(28,scale),mul(162,scale),.95)
hit_visible=branch(seq,cmp('Greater_DoubleDouble',v('EnemyHitUntil'),now,'real'),'then_2')
hit_marker=text(hit_visible,'X',sub(mul(width,.5),mul(5,scale)),sub(mul(height,.5),mul(8,scale)),1.2,'(R=1,G=.65,B=.2,A=1)')
hit_damage=call(STRING,'Conv_IntToString',[('InInt','int',call(MATH,'FFloor',[('A','real',v('LastEnemyDamage'))],cat='int'))],cat='string')
text(hit_marker,concat('-',hit_damage),add(mul(width,.5),mul(12,scale)),add(mul(height,.5),mul(8,scale)),.95,'(R=1,G=.8,B=.45,A=1)')
host_warning_ready=branch(seq,(g.valid(hostage,'CachedHostage'),'ReturnValue'),'then_3')
host_warning=branch(host_warning_ready,both(cmp('Greater_DoubleDouble',v('HostageHurtUntil'),now,'real'),cmp('Greater_DoubleDouble',host_damage_hp,0,'real')))
warning=rect(host_warning,mul(20,scale),mul(194,scale),mul(430,scale),mul(53,scale),'(R=.36,G=.025,B=.015,A=.94)')
warning=text(warning,'REHÉN: ¡ME ESTÁN ATACANDO!',mul(30,scale),mul(203,scale),1.15,'(R=1,G=.85,B=.4,A=1)')
text(warning,'¡Ayúdame! Protege mi retirada.',mul(30,scale),mul(224,scale),1.05)
g.write('BP_HUD_Entrega')

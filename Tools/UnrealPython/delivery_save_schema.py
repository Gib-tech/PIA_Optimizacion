"""Versioned Blueprint-only checkpoint schema shared by the authoring tools."""
ROOT = '/Game/ThirdPerson/Blueprints/Entrega/'
SAVE = ROOT + 'BP_DeliverySave.BP_DeliverySave_C'
MANAGER = ROOT + 'BP_DeliverySaveManager.BP_DeliverySaveManager_C'
GI = '/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C'
SLOT = 'TimeOut_Delivery_v1'
VERSION = 2
ROT = '/Script/CoreUObject.Rotator'
VEC = '/Script/CoreUObject.Vector'

# Values are scalars/structs. No level actor pointers are serialized.
FIELDS = {
    'Version': 'int', 'Paso': 'int', 'PlayerHealth': 'real',
    'OrderCode': 'int', 'MissionElapsed': 'real',
    'FinalStandRevision': 'int', 'OrderRevealed': 'bool',
    'PlayerLocation': 'vector', 'PlayerRotation': 'rotator', 'ControlRotation': 'rotator',
    'HammerUpgraded': 'bool', 'HammerEquipped': 'bool',
    'FirstPerson': 'bool', 'ExtrasRevision': 'int',
    'Botiquines': 'int', 'Cargas': 'int', 'Creditos': 'int', 'WorldSeconds': 'real',
    'RobotEnergy': 'int', 'bFabricating': 'bool', 'FabricationProgress': 'real',
    'HostageHealth': 'real', 'HostageLocation': 'vector', 'HostageRotation': 'rotator',
    'Rescued': 'bool', 'Accompanying': 'bool', 'Waiting': 'bool',
}
for i in (1,2,3,4):FIELDS['Recogido'+str(i)]='bool'
for i in (1,2,3):FIELDS['MesaRecogido'+str(i)]='bool'
for i in (1, 2, 3):
    for name, kind in [('Cleared', 'bool'), ('Wave', 'int'), ('Phase', 'int'), ('Spawned', 'int')]:
        FIELDS['Zone%d%s' % (i, name)] = kind
for i in (1, 2, 3):
    for name, kind in [('Health', 'real'), ('Unlocked', 'bool'), ('Destroyed', 'bool'), ('Cracked', 'bool')]:
        FIELDS['Door%d%s' % (i, name)] = kind
    FIELDS['Beacon%dActivated' % i] = 'bool'

# Nivel_Entrega.Nivel_Entrega:PersistentLevel.Nivel_Entrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Maps/Nivel_Entrega.Nivel_Entrega:PersistentLevel.Nivel_Entrega`. **Tipo:** LevelScriptBlueprint.
**Clase padre:** `/Script/Engine.LevelScriptActor`.

Blueprint del nivel entregable. Inicializa referencias de jugador, rehén, director y señal; consulta vida y secuencia mediante funciones propias y combina sus condiciones con macros antes de sincronizar la extracción. InicializarSenales y SincronizarExtraccion son eventos reales del nivel; los contadores permiten comprobar su ejecución.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `PersistentLevel.Nivel_Entrega.EventGraph`. Operaciones alcanzables desde `then`: `K2_SetTimerDelegate`, `K2_SetTimerDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InicializarSenales`** en `PersistentLevel.Nivel_Entrega.EventGraph`. Operaciones alcanzables desde `then`: `Asignar Inicializaciones`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Jugador`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Rehen`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Director`, `GetActorOfClass`, `Asignar SenalExtraccion`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SincronizarExtraccion`** en `PersistentLevel.Nivel_Entrega.EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar Sincronizaciones`, `ConsultarAliados`, `ConsultarSecuencia`, `Condición`, `SetActorHiddenInGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ConsultarAliados`** en `PersistentLevel.Nivel_Entrega.ConsultarAliados`. Operaciones alcanzables desde `then`: `ConsultarAliados`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ConsultarSecuencia`** en `PersistentLevel.Nivel_Entrega.ConsultarSecuencia`. Operaciones alcanzables desde `then`: `ConsultarSecuencia`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PersistentLevel.Nivel_Entrega.SincronizarExtraccion`** en `PersistentLevel.Nivel_Entrega.SincronizarExtraccion`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Nivel_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PersistentLevel.Nivel_Entrega.InicializarSenales`** en `PersistentLevel.Nivel_Entrega.InicializarSenales`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Nivel_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `PersistentLevel.Nivel_Entrega.ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Nivel_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Jugador` — tipo `object`.
- `Rehen` — tipo `object`.
- `Director` — tipo `object`.
- `SenalExtraccion` — tipo `object`.
- `Inicializado` — tipo `bool`.
- `Inicializaciones` — tipo `int`.
- `Sincronizaciones` — tipo `int`.

## Operaciones y dependencias verificadas

La exportación contiene 62 nodos con pines. Funciones referenciadas: `Add_IntInt`, `BooleanAND`, `ConsultarAliados`, `ConsultarSecuencia`, `GetActorOfClass`, `GreaterEqual_IntInt`, `Greater_DoubleDouble`, `InicializarSenales`, `IsValid`, `K2_SetTimerDelegate`, `LessEqual_IntInt`, `Not_PreBool`, `ReceiveBeginPlay`, `SetActorHiddenInGame`, `SincronizarExtraccion`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_SenalExtraccion.BP_SenalExtraccion_C`
- `/Game/ThirdPerson/Maps/Nivel_Entrega.Nivel_Entrega_C`
- `/Game/ThirdPerson/Maps/Nivel_Entrega.SKEL_Nivel_Entrega_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `a02d767e57411058e9aa332d533ee906d5f37064c38de447a9f82f21c7abca3d`.

# BP_RafagaRotura

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/FX/BP_RafagaRotura`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Niagara.NiagaraActor'"`.

Efecto de rotura de vida limitada a 0,65 s. El sistema Niagara y las motas emisivas pertenecen al mismo actor. BeginPlay comunica al material la hora de inicio para animar y desvanecer las motas de forma independiente.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_RafagaRotura`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetCustomPrimitiveDataFloat`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 7 nodos con pines. Funciones referenciadas: `GetTimeSeconds`, `ReceiveBeginPlay`, `SetCustomPrimitiveDataFloat`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `a36e6906b6f64d85d55cfa846deb7a166461b1a1a972b6f4f5da6dad6f5849d4`.

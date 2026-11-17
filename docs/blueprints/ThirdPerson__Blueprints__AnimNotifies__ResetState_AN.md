# ResetState_AN

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/AnimNotifies/ResetState_AN`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimNotify'"`.

Notify de recuperación que devuelve el estado de ataque a Nothing. Debe coordinarse con interrupción y limpieza de hitbox del personaje especializado.

## Entradas y responsabilidades del grafo

- **`Received_Notify`** en `Received_Notify`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `ResetState`, `Received_Notify`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 5 nodos con pines. Funciones referenciadas: `GetOwner`, `Received_Notify`, `ResetState`.

- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `00b25a84045de06b2d0db88a6458ee826379fe61dd4ab87a089374930a013d00`.

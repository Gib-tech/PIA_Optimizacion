# SaveLightAttack_AN

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/AnimNotifies/SaveLightAttack_AN`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimNotify'"`.

Notify del montage que habilita/consume buffer del siguiente golpe ligero. Se ejecuta únicamente en la malla real del jugador.

## Entradas y responsabilidades del grafo

- **`Received_Notify`** en `Received_Notify`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `SaveLightAttack`, `Received_Notify`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 5 nodos con pines. Funciones referenciadas: `GetOwner`, `Received_Notify`, `SaveLightAttack`.

- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `60d8ef9e99445ef4bfe6db8f183cd2ec465324ce364c9552db586b93233526a9`.

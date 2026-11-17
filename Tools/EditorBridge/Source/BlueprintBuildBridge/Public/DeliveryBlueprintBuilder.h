#pragma once
#include "Kismet/BlueprintFunctionLibrary.h"
#include "DeliveryBlueprintBuilder.generated.h"
UCLASS()
class BLUEPRINTBUILDBRIDGE_API UDeliveryBlueprintBuilder : public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool InstallGraph(UBlueprint* Blueprint, const FString& Filename);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool ConnectTreeRoot(UObject* Tree);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool SetPropertyText(UObject* Object, FName PropertyName, const FString& Value);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static int32 RemoveGraphNodes(UBlueprint* Blueprint, const TArray<FName>& NodeNames);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool AddLayoutComment(UBlueprint* Blueprint, FName Identifier, const FString& Title, FVector2D Position, FVector2D Size, FLinearColor Color);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool IsPartitioned(UWorld* World);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static UBlueprint* GetLevelBlueprint(UWorld* World);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static class ALandscape* CreateEvaluationLandscape(UWorld* World, class UMaterialInterface* Material, const TArray<class ULandscapeLayerInfoObject*>& Layers);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool InstallNamedGraph(UBlueprint* Blueprint, FName Name, bool IsMacro, const FString& Filename);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static TArray<FIntPoint> GetLODGeometry(class UStaticMesh* Mesh);
 UFUNCTION(BlueprintCallable, Category="Delivery|Editor") static bool LoadEditorRegion(UWorld* World, FVector Min, FVector Max);
};

#include "DeliveryBlueprintBuilder.h"
#include "Modules/ModuleManager.h"
#include "Misc/FileHelper.h"
#include "Engine/Blueprint.h"
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphSchema.h"
#include "EdGraphUtilities.h"
#include "EdGraphNode_Comment.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "BehaviorTree/BehaviorTree.h"
#include "BehaviorTreeGraph.h"
#include "BehaviorTreeGraphNode_Root.h"
#include "BehaviorTreeGraphNode_Composite.h"
#include "UObject/UnrealType.h"
#include "Engine/World.h"
#include "Engine/Level.h"
#include "Engine/LevelScriptBlueprint.h"
#include "Landscape.h"
#include "LandscapeLayerInfoObject.h"
#include "EdGraphSchema_K2.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "WorldPartition/WorldPartition.h"
#include "WorldPartition/LoaderAdapter/LoaderAdapterShape.h"
IMPLEMENT_MODULE(FDefaultModuleImpl, BlueprintBuildBridge)
bool UDeliveryBlueprintBuilder::InstallGraph(UBlueprint* BP,const FString& Filename) {
 FString Source;
 if(!BP || !FFileHelper::LoadFileToString(Source,*Filename) || BP->UbergraphPages.IsEmpty()) return false;
 UEdGraph* Graph=BP->UbergraphPages[0];
 BP->Modify();Graph->Modify();
 const auto OldNodes=Graph->Nodes;
 for(UEdGraphNode* Node:OldNodes) FBlueprintEditorUtils::RemoveNode(BP,Node,true);
 FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(BP);
 FKismetEditorUtilities::CompileBlueprint(BP);
 TSet<UEdGraphNode*> Imported;
 FEdGraphUtilities::ImportNodesFromText(Graph,Source,Imported);
 for(UEdGraphNode* Node:Imported) Node->CreateNewGuid();
 FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(BP);
 FKismetEditorUtilities::CompileBlueprint(BP);
 Graph->NotifyGraphChanged();BP->MarkPackageDirty();
 return BP->Status!=BS_Error && Imported.Num()>0;
}
bool UDeliveryBlueprintBuilder::ConnectTreeRoot(UObject* Object) {
 UBehaviorTree* Tree=Cast<UBehaviorTree>(Object);
 UBehaviorTreeGraph* Graph=Tree?Cast<UBehaviorTreeGraph>(Tree->BTGraph):nullptr;
 if(!Graph) return false;
 UBehaviorTreeGraphNode_Root* Root=nullptr;
 UBehaviorTreeGraphNode_Composite* Top=nullptr;
 for(UEdGraphNode* Node:Graph->Nodes) {
  if(auto* R=Cast<UBehaviorTreeGraphNode_Root>(Node))Root=R;
  if(auto* C=Cast<UBehaviorTreeGraphNode_Composite>(Node)) {
   UEdGraphPin* In=C->FindPin(TEXT("In"));
   if(In && In->LinkedTo.IsEmpty())Top=C;
  }
 }
 if(!Root || !Top)return false;
 Graph->Modify();Root->Modify();Top->Modify();
 UEdGraphPin* Output=Root->FindPin(TEXT("In"));
 UEdGraphPin* Input=Top->FindPin(TEXT("In"));
 if(!Output || !Input)return false;
 bool Connected=Graph->GetSchema()->TryCreateConnection(Output,Input);
 Graph->UpdateAsset();Tree->MarkPackageDirty();Graph->NotifyGraphChanged();
 return Connected && Tree->RootNode!=nullptr;
}
bool UDeliveryBlueprintBuilder::SetPropertyText(UObject* Object,FName Name,const FString& Value) {
 if(!Object)return false;
 FProperty* Property=Object->GetClass()->FindPropertyByName(Name);
 if(!Property)return false;
 Object->Modify();
 bool Ok=Property->ImportText_Direct(*Value,Property->ContainerPtrToValuePtr<void>(Object),Object,PPF_None)!=nullptr;
 if(Ok){Object->PostEditChange();Object->MarkPackageDirty();}
 return Ok;
}

bool UDeliveryBlueprintBuilder::IsPartitioned(UWorld* World) { return World && World->IsPartitionedWorld(); }
bool UDeliveryBlueprintBuilder::AddLayoutComment(UBlueprint* BP,FName Identifier,const FString& Title,FVector2D Position,FVector2D Size,FLinearColor Color) {
 if(!BP || BP->UbergraphPages.IsEmpty())return false;
 UEdGraph* Graph=BP->UbergraphPages[0];BP->Modify();Graph->Modify();
 UEdGraphNode_Comment* Comment=FindObject<UEdGraphNode_Comment>(Graph,*Identifier.ToString());
 if(!Comment){Comment=NewObject<UEdGraphNode_Comment>(Graph,Identifier,RF_Transactional);Comment->CreateNewGuid();Graph->AddNode(Comment,false,false);}
 Comment->Modify();Comment->NodeComment=Title;Comment->NodePosX=FMath::RoundToInt(Position.X);Comment->NodePosY=FMath::RoundToInt(Position.Y);
 Comment->NodeWidth=FMath::RoundToInt(Size.X);Comment->NodeHeight=FMath::RoundToInt(Size.Y);Comment->CommentColor=Color;Comment->FontSize=26;
 Graph->NotifyGraphChanged();BP->MarkPackageDirty();return true;
}
int32 UDeliveryBlueprintBuilder::RemoveGraphNodes(UBlueprint* BP,const TArray<FName>& Names) {
 if(!BP)return 0;
 BP->Modify();int32 Removed=0;
 for(UEdGraph* Graph:BP->UbergraphPages) {
  const auto Nodes=Graph->Nodes;
  for(UEdGraphNode* Node:Nodes)if(Node && Names.Contains(Node->GetFName())) {
   Graph->Modify();FBlueprintEditorUtils::RemoveNode(BP,Node,true);++Removed;
  }
  Graph->NotifyGraphChanged();
 }
 if(Removed){FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(BP);FKismetEditorUtilities::CompileBlueprint(BP);BP->MarkPackageDirty();}
 return Removed;
}
UBlueprint* UDeliveryBlueprintBuilder::GetLevelBlueprint(UWorld* World) { return World ? World->PersistentLevel->GetLevelScriptBlueprint(false) : nullptr; }
ALandscape* UDeliveryBlueprintBuilder::CreateEvaluationLandscape(UWorld* World, UMaterialInterface* Material, const TArray<ULandscapeLayerInfoObject*>& Layers) {
 if(!World || !Material || Layers.Num()<4) return nullptr;
 constexpr int32 Size=127;
 ALandscape* Land=World->SpawnActor<ALandscape>(FVector(-6300,-12000,-2),FRotator::ZeroRotator);
 if(!Land)return nullptr;
 Land->SetActorScale3D(FVector(100,100,100));Land->LandscapeMaterial=Material;
 TMap<FGuid,TArray<uint16>> Heights;
 Heights.Add(FGuid(),TArray<uint16>());Heights[FGuid()].Init(32768,Size*Size);
 TArray<FLandscapeImportLayerInfo> Infos;
 const float Boundaries[]={-9200,-6600,-4500,-2800};
 for(int32 Layer=0;Layer<Layers.Num();++Layer) {
  FLandscapeImportLayerInfo Info(Layers[Layer]->LayerName);Info.LayerInfo=Layers[Layer];Info.LayerData.Init(0,Size*Size);
  for(int32 Y=0;Y<Size;++Y)for(int32 X=0;X<Size;++X) {
   float WY=-12000+Y*100;
   // Five material regions along the actual mission route. Smooth transitions
   // use vertex weights, not overlaid coplanar planes.
   int32 Region=0;while(Region<4 && WY>Boundaries[Region])++Region;
   int32 Chosen=FMath::Min(Region,Layers.Num()-1);
   Info.LayerData[Y*Size+X]=(Chosen==Layer)?255:0;
  }
  Infos.Add(MoveTemp(Info));
 }
 TMap<FGuid,TArray<FLandscapeImportLayerInfo>> Weights;Weights.Add(FGuid(),MoveTemp(Infos));
 Land->Import(FGuid::NewGuid(),0,0,Size-1,Size-1,1,63,Heights,nullptr,Weights,ELandscapeImportAlphamapType::Additive);
 Land->SetActorLabel(TEXT("Landscape_Multitextura_Entrega"));Land->PostEditChange();Land->MarkPackageDirty();return Land;
}
bool UDeliveryBlueprintBuilder::InstallNamedGraph(UBlueprint* BP,FName Name,bool IsMacro,const FString& Filename) {
 if(!BP)return false;FString Text;if(!FFileHelper::LoadFileToString(Text,*Filename))return false;
 UEdGraph* Graph=nullptr;
 auto& Graphs=IsMacro?BP->MacroGraphs:BP->FunctionGraphs;
 for(UEdGraph* Existing:Graphs)if(Existing->GetFName()==Name){Graph=Existing;break;}
 if(!Graph) {
  Graph=FBlueprintEditorUtils::CreateNewGraph(BP,Name,UEdGraph::StaticClass(),UEdGraphSchema_K2::StaticClass());
  if(IsMacro)FBlueprintEditorUtils::AddMacroGraph(BP,Graph,true,nullptr);
  else FBlueprintEditorUtils::AddFunctionGraph<UClass>(BP,Graph,true,nullptr);
 }
 const auto Old=Graph->Nodes;for(UEdGraphNode* Node:Old)FBlueprintEditorUtils::RemoveNode(BP,Node,true);
 TSet<UEdGraphNode*> Imported;FEdGraphUtilities::ImportNodesFromText(Graph,Text,Imported);
 for(UEdGraphNode* Node:Imported)Node->CreateNewGuid();
 FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(BP);
 FKismetEditorUtilities::CompileBlueprint(BP);BP->MarkPackageDirty();return BP->Status!=BS_Error && Imported.Num()>0;
}
TArray<FIntPoint> UDeliveryBlueprintBuilder::GetLODGeometry(UStaticMesh* Mesh) {
 TArray<FIntPoint> Result;if(!Mesh || !Mesh->GetRenderData())return Result;
 for(const FStaticMeshLODResources& LOD:Mesh->GetRenderData()->LODResources)Result.Add(FIntPoint(LOD.GetNumVertices(),LOD.GetNumTriangles()));
 return Result;
}
bool UDeliveryBlueprintBuilder::LoadEditorRegion(UWorld* World,FVector Min,FVector Max) {
 if(!World || !World->GetWorldPartition())return false;
 auto* Adapter=World->GetWorldPartition()->CreateEditorLoaderAdapter<FLoaderAdapterShape>(World,FBox(Min,Max),TEXT("Mission art review"));
 Adapter->GetLoaderAdapter()->SetUserCreated(true);Adapter->GetLoaderAdapter()->Load();return true;
}

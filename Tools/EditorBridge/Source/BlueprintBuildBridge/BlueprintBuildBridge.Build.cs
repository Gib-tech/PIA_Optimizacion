using UnrealBuildTool;
public class BlueprintBuildBridge : ModuleRules {
 public BlueprintBuildBridge(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine"});
  PrivateDependencyModuleNames.AddRange(new string[]{"UnrealEd","BlueprintGraph","KismetCompiler","AIModule","AIGraph","BehaviorTreeEditor","Landscape"});
 }
}

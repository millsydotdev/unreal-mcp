#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Handler class for Enhanced Input Action MCP commands
 * Provides comprehensive input mapping, axis handling, presets, and validation
 */
class UNREALMCP_API FUnrealMCPEnhancedInputCommands
{
public:
    FUnrealMCPEnhancedInputCommands();

    // Handle enhanced input commands
    TSharedPtr<FJsonObject> HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params);

private:
    // Input Action Mapping Commands
    TSharedPtr<FJsonObject> HandleCreateEnhancedInputActionMapping(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleCreateInputAxisMapping(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleAddAlternativeKeyBinding(const TSharedPtr<FJsonObject>& Params);
    
    // Input Action Management Commands
    TSharedPtr<FJsonObject> HandleListInputActions(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleUpdateInputActionMapping(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleRemoveInputActionMapping(const TSharedPtr<FJsonObject>& Params);
    
    // Input Presets and Templates
    TSharedPtr<FJsonObject> HandleCreateInputPreset(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleApplyInputPreset(const TSharedPtr<FJsonObject>& Params);
    
    // Enhanced Blueprint Input Tools
    TSharedPtr<FJsonObject> HandleCreateEnhancedInputActionBlueprintNode(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleCreateInputAxisBlueprintNode(const TSharedPtr<FJsonObject>& Params);
    
    // Input Validation and Testing
    TSharedPtr<FJsonObject> HandleValidateInputMappings(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleTestInputAction(const TSharedPtr<FJsonObject>& Params);
    
    // Input Import/Export
    TSharedPtr<FJsonObject> HandleExportInputMappings(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleImportInputMappings(const TSharedPtr<FJsonObject>& Params);
    
    // Advanced Input Features
    TSharedPtr<FJsonObject> HandleCreateInputContext(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleCreateInputTrigger(const TSharedPtr<FJsonObject>& Params);
    
    // Helper functions
    TSharedPtr<FJsonObject> CreateInputPreset(const FString& PresetName, const FString& PresetType);
    TArray<TSharedPtr<FJsonObject>> GetInputMappingsForCategory(const FString& Category);
    bool ValidateKeyBinding(const FString& KeyName);
    FString GetInputPresetTemplate(const FString& PresetType);
};

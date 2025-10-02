#include "Commands/UnrealMCPEnhancedInputCommands.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "GameFramework/InputSettings.h"
#include "Engine/Engine.h"
#include "HAL/PlatformFilemanager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Blueprint/BlueprintSupport.h"
#include "Engine/Blueprint.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphNode.h"
#include "K2Node_InputAction.h"
#include "K2Node_InputAxisEvent.h"
// #include "K2Node_InputAxis.h" // Not available in all UE versions

FUnrealMCPEnhancedInputCommands::FUnrealMCPEnhancedInputCommands()
{
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params)
{
    // Input Action Mapping Commands
    if (CommandType == TEXT("create_enhanced_input_action_mapping"))
    {
        return HandleCreateEnhancedInputActionMapping(Params);
    }
    else if (CommandType == TEXT("create_input_axis_mapping"))
    {
        return HandleCreateInputAxisMapping(Params);
    }
    else if (CommandType == TEXT("add_alternative_key_binding"))
    {
        return HandleAddAlternativeKeyBinding(Params);
    }
    
    // Input Action Management Commands
    else if (CommandType == TEXT("list_input_actions"))
    {
        return HandleListInputActions(Params);
    }
    else if (CommandType == TEXT("update_input_action_mapping"))
    {
        return HandleUpdateInputActionMapping(Params);
    }
    else if (CommandType == TEXT("remove_input_action_mapping"))
    {
        return HandleRemoveInputActionMapping(Params);
    }
    
    // Input Presets and Templates
    else if (CommandType == TEXT("create_input_preset"))
    {
        return HandleCreateInputPreset(Params);
    }
    else if (CommandType == TEXT("apply_input_preset"))
    {
        return HandleApplyInputPreset(Params);
    }
    
    // Enhanced Blueprint Input Tools
    else if (CommandType == TEXT("create_enhanced_input_action_blueprint_node"))
    {
        return HandleCreateEnhancedInputActionBlueprintNode(Params);
    }
    else if (CommandType == TEXT("create_input_axis_blueprint_node"))
    {
        return HandleCreateInputAxisBlueprintNode(Params);
    }
    
    // Input Validation and Testing
    else if (CommandType == TEXT("validate_input_mappings"))
    {
        return HandleValidateInputMappings(Params);
    }
    else if (CommandType == TEXT("test_input_action"))
    {
        return HandleTestInputAction(Params);
    }
    
    // Input Import/Export
    else if (CommandType == TEXT("export_input_mappings"))
    {
        return HandleExportInputMappings(Params);
    }
    else if (CommandType == TEXT("import_input_mappings"))
    {
        return HandleImportInputMappings(Params);
    }
    
    // Advanced Input Features
    else if (CommandType == TEXT("create_input_context"))
    {
        return HandleCreateInputContext(Params);
    }
    else if (CommandType == TEXT("create_input_trigger"))
    {
        return HandleCreateInputTrigger(Params);
    }
    
    return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Unknown enhanced input command: %s"), *CommandType));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateEnhancedInputActionMapping(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ActionName;
    if (!Params->TryGetStringField(TEXT("action_name"), ActionName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'action_name' parameter"));
    }

    FString PrimaryKey;
    if (!Params->TryGetStringField(TEXT("primary_key"), PrimaryKey))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'primary_key' parameter"));
    }

    // Get optional parameters
    FString SecondaryKey = Params->GetStringField(TEXT("secondary_key"));
    FString InputType = Params->GetStringField(TEXT("input_type"));
    bool bShift = Params->GetBoolField(TEXT("shift"));
    bool bCtrl = Params->GetBoolField(TEXT("ctrl"));
    bool bAlt = Params->GetBoolField(TEXT("alt"));
    bool bCmd = Params->GetBoolField(TEXT("cmd"));
    FString Category = Params->GetStringField(TEXT("category"));
    FString Description = Params->GetStringField(TEXT("description"));

    // Get the input settings
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    TArray<FInputActionKeyMapping> CreatedMappings;

    // Create primary key mapping
    FInputActionKeyMapping PrimaryMapping;
    PrimaryMapping.ActionName = FName(*ActionName);
    PrimaryMapping.Key = FKey(*PrimaryKey);
    PrimaryMapping.bShift = bShift;
    PrimaryMapping.bCtrl = bCtrl;
    PrimaryMapping.bAlt = bAlt;
    PrimaryMapping.bCmd = bCmd;
    
    InputSettings->AddActionMapping(PrimaryMapping);
    CreatedMappings.Add(PrimaryMapping);

    // Create secondary key mapping if provided
    if (!SecondaryKey.IsEmpty())
    {
        FInputActionKeyMapping SecondaryMapping;
        SecondaryMapping.ActionName = FName(*ActionName);
        SecondaryMapping.Key = FKey(*SecondaryKey);
        SecondaryMapping.bShift = bShift;
        SecondaryMapping.bCtrl = bCtrl;
        SecondaryMapping.bAlt = bAlt;
        SecondaryMapping.bCmd = bCmd;
        
        InputSettings->AddActionMapping(SecondaryMapping);
        CreatedMappings.Add(SecondaryMapping);
    }

    // Save the settings
    InputSettings->SaveConfig();

    // Create response
    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("action_name"), ActionName);
    ResultObj->SetStringField(TEXT("primary_key"), PrimaryKey);
    ResultObj->SetStringField(TEXT("secondary_key"), SecondaryKey);
    ResultObj->SetStringField(TEXT("input_type"), InputType);
    ResultObj->SetStringField(TEXT("category"), Category);
    ResultObj->SetStringField(TEXT("description"), Description);
    ResultObj->SetNumberField(TEXT("created_mappings"), CreatedMappings.Num());
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateInputAxisMapping(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString AxisName;
    if (!Params->TryGetStringField(TEXT("axis_name"), AxisName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'axis_name' parameter"));
    }

    FString PositiveKey;
    if (!Params->TryGetStringField(TEXT("positive_key"), PositiveKey))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'positive_key' parameter"));
    }

    // Get optional parameters
    FString NegativeKey = Params->GetStringField(TEXT("negative_key"));
    float Scale = Params->GetNumberField(TEXT("scale"));
    FString Category = Params->GetStringField(TEXT("category"));
    FString Description = Params->GetStringField(TEXT("description"));

    if (Scale == 0.0f) Scale = 1.0f;

    // Get the input settings
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    TArray<FInputAxisKeyMapping> CreatedMappings;

    // Create positive axis mapping
    FInputAxisKeyMapping PositiveMapping;
    PositiveMapping.AxisName = FName(*AxisName);
    PositiveMapping.Key = FKey(*PositiveKey);
    PositiveMapping.Scale = Scale;
    
    InputSettings->AddAxisMapping(PositiveMapping);
    CreatedMappings.Add(PositiveMapping);

    // Create negative axis mapping if provided
    if (!NegativeKey.IsEmpty())
    {
        FInputAxisKeyMapping NegativeMapping;
        NegativeMapping.AxisName = FName(*AxisName);
        NegativeMapping.Key = FKey(*NegativeKey);
        NegativeMapping.Scale = -Scale; // Negative scale for opposite direction
        
        InputSettings->AddAxisMapping(NegativeMapping);
        CreatedMappings.Add(NegativeMapping);
    }

    // Save the settings
    InputSettings->SaveConfig();

    // Create response
    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("axis_name"), AxisName);
    ResultObj->SetStringField(TEXT("positive_key"), PositiveKey);
    ResultObj->SetStringField(TEXT("negative_key"), NegativeKey);
    ResultObj->SetNumberField(TEXT("scale"), Scale);
    ResultObj->SetStringField(TEXT("category"), Category);
    ResultObj->SetStringField(TEXT("description"), Description);
    ResultObj->SetNumberField(TEXT("created_mappings"), CreatedMappings.Num());
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleAddAlternativeKeyBinding(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ActionName;
    if (!Params->TryGetStringField(TEXT("action_name"), ActionName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'action_name' parameter"));
    }

    FString AlternativeKey;
    if (!Params->TryGetStringField(TEXT("alternative_key"), AlternativeKey))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'alternative_key' parameter"));
    }

    // Get optional parameters
    bool bShift = Params->GetBoolField(TEXT("shift"));
    bool bCtrl = Params->GetBoolField(TEXT("ctrl"));
    bool bAlt = Params->GetBoolField(TEXT("alt"));
    bool bCmd = Params->GetBoolField(TEXT("cmd"));

    // Get the input settings
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    // Create the alternative key mapping
    FInputActionKeyMapping AlternativeMapping;
    AlternativeMapping.ActionName = FName(*ActionName);
    AlternativeMapping.Key = FKey(*AlternativeKey);
    AlternativeMapping.bShift = bShift;
    AlternativeMapping.bCtrl = bCtrl;
    AlternativeMapping.bAlt = bAlt;
    AlternativeMapping.bCmd = bCmd;

    // Add the mapping
    InputSettings->AddActionMapping(AlternativeMapping);
    InputSettings->SaveConfig();

    // Create response
    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("action_name"), ActionName);
    ResultObj->SetStringField(TEXT("alternative_key"), AlternativeKey);
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleListInputActions(const TSharedPtr<FJsonObject>& Params)
{
    // Get optional parameters
    FString Category = Params->GetStringField(TEXT("category"));
    bool bIncludeAxes = Params->GetBoolField(TEXT("include_axes"));

    // Get the input settings
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    TArray<TSharedPtr<FJsonValue>> ActionArray;
    TArray<TSharedPtr<FJsonValue>> AxisArray;

    // List action mappings
    for (const FInputActionKeyMapping& ActionMapping : InputSettings->GetActionMappings())
    {
        TSharedPtr<FJsonObject> ActionObj = MakeShared<FJsonObject>();
        ActionObj->SetStringField(TEXT("action_name"), ActionMapping.ActionName.ToString());
        ActionObj->SetStringField(TEXT("key"), ActionMapping.Key.ToString());
        ActionObj->SetBoolField(TEXT("shift"), ActionMapping.bShift);
        ActionObj->SetBoolField(TEXT("ctrl"), ActionMapping.bCtrl);
        ActionObj->SetBoolField(TEXT("alt"), ActionMapping.bAlt);
        ActionObj->SetBoolField(TEXT("cmd"), ActionMapping.bCmd);
        
        ActionArray.Add(MakeShared<FJsonValueObject>(ActionObj));
    }

    // List axis mappings if requested
    if (bIncludeAxes)
    {
        for (const FInputAxisKeyMapping& AxisMapping : InputSettings->GetAxisMappings())
        {
            TSharedPtr<FJsonObject> AxisObj = MakeShared<FJsonObject>();
            AxisObj->SetStringField(TEXT("axis_name"), AxisMapping.AxisName.ToString());
            AxisObj->SetStringField(TEXT("key"), AxisMapping.Key.ToString());
            AxisObj->SetNumberField(TEXT("scale"), AxisMapping.Scale);
            
            AxisArray.Add(MakeShared<FJsonValueObject>(AxisObj));
        }
    }

    ResultObj->SetArrayField(TEXT("actions"), ActionArray);
    ResultObj->SetArrayField(TEXT("axes"), AxisArray);
    ResultObj->SetNumberField(TEXT("total_actions"), ActionArray.Num());
    ResultObj->SetNumberField(TEXT("total_axes"), AxisArray.Num());
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateInputPreset(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString PresetName;
    if (!Params->TryGetStringField(TEXT("preset_name"), PresetName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'preset_name' parameter"));
    }

    FString PresetType;
    if (!Params->TryGetStringField(TEXT("preset_type"), PresetType))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'preset_type' parameter"));
    }

    return CreateInputPreset(PresetName, PresetType);
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::CreateInputPreset(const FString& PresetName, const FString& PresetType)
{
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    TArray<FInputActionKeyMapping> CreatedMappings;
    TArray<FInputAxisKeyMapping> CreatedAxes;

    // Create preset based on type
    if (PresetType.Equals(TEXT("FPS"), ESearchCase::IgnoreCase))
    {
        // FPS Controls
        FInputActionKeyMapping FireAction;
        FireAction.ActionName = FName(TEXT("Fire"));
        FireAction.Key = FKey(TEXT("LeftMouseButton"));
        InputSettings->AddActionMapping(FireAction);
        CreatedMappings.Add(FireAction);

        FInputActionKeyMapping AimAction;
        AimAction.ActionName = FName(TEXT("Aim"));
        AimAction.Key = FKey(TEXT("RightMouseButton"));
        InputSettings->AddActionMapping(AimAction);
        CreatedMappings.Add(AimAction);

        FInputActionKeyMapping ReloadAction;
        ReloadAction.ActionName = FName(TEXT("Reload"));
        ReloadAction.Key = FKey(TEXT("R"));
        InputSettings->AddActionMapping(ReloadAction);
        CreatedMappings.Add(ReloadAction);

        // Movement axes
        FInputAxisKeyMapping MoveForward;
        MoveForward.AxisName = FName(TEXT("MoveForward"));
        MoveForward.Key = FKey(TEXT("W"));
        MoveForward.Scale = 1.0f;
        InputSettings->AddAxisMapping(MoveForward);
        CreatedAxes.Add(MoveForward);

        FInputAxisKeyMapping MoveBackward;
        MoveBackward.AxisName = FName(TEXT("MoveForward"));
        MoveBackward.Key = FKey(TEXT("S"));
        MoveBackward.Scale = -1.0f;
        InputSettings->AddAxisMapping(MoveBackward);
        CreatedAxes.Add(MoveBackward);

        FInputAxisKeyMapping MoveRight;
        MoveRight.AxisName = FName(TEXT("MoveRight"));
        MoveRight.Key = FKey(TEXT("D"));
        MoveRight.Scale = 1.0f;
        InputSettings->AddAxisMapping(MoveRight);
        CreatedAxes.Add(MoveRight);

        FInputAxisKeyMapping MoveLeft;
        MoveLeft.AxisName = FName(TEXT("MoveRight"));
        MoveLeft.Key = FKey(TEXT("A"));
        MoveLeft.Scale = -1.0f;
        InputSettings->AddAxisMapping(MoveLeft);
        CreatedAxes.Add(MoveLeft);
    }
    else if (PresetType.Equals(TEXT("ThirdPerson"), ESearchCase::IgnoreCase))
    {
        // Third Person Controls
        FInputActionKeyMapping AttackAction;
        AttackAction.ActionName = FName(TEXT("Attack"));
        AttackAction.Key = FKey(TEXT("LeftMouseButton"));
        InputSettings->AddActionMapping(AttackAction);
        CreatedMappings.Add(AttackAction);

        FInputActionKeyMapping JumpAction;
        JumpAction.ActionName = FName(TEXT("Jump"));
        JumpAction.Key = FKey(TEXT("SpaceBar"));
        InputSettings->AddActionMapping(JumpAction);
        CreatedMappings.Add(JumpAction);

        FInputActionKeyMapping DodgeAction;
        DodgeAction.ActionName = FName(TEXT("Dodge"));
        DodgeAction.Key = FKey(TEXT("LeftShift"));
        InputSettings->AddActionMapping(DodgeAction);
        CreatedMappings.Add(DodgeAction);
    }
    else if (PresetType.Equals(TEXT("Platformer"), ESearchCase::IgnoreCase))
    {
        // Platformer Controls
        FInputActionKeyMapping JumpAction;
        JumpAction.ActionName = FName(TEXT("Jump"));
        JumpAction.Key = FKey(TEXT("SpaceBar"));
        InputSettings->AddActionMapping(JumpAction);
        CreatedMappings.Add(JumpAction);

        FInputActionKeyMapping DashAction;
        DashAction.ActionName = FName(TEXT("Dash"));
        DashAction.Key = FKey(TEXT("LeftShift"));
        InputSettings->AddActionMapping(DashAction);
        CreatedMappings.Add(DashAction);

        FInputActionKeyMapping InteractAction;
        InteractAction.ActionName = FName(TEXT("Interact"));
        InteractAction.Key = FKey(TEXT("E"));
        InputSettings->AddActionMapping(InteractAction);
        CreatedMappings.Add(InteractAction);
    }

    // Save the settings
    InputSettings->SaveConfig();

    // Create response
    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("preset_name"), PresetName);
    ResultObj->SetStringField(TEXT("preset_type"), PresetType);
    ResultObj->SetNumberField(TEXT("actions_created"), CreatedMappings.Num());
    ResultObj->SetNumberField(TEXT("axes_created"), CreatedAxes.Num());
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleValidateInputMappings(const TSharedPtr<FJsonObject>& Params)
{
    // Get optional parameters
    bool bCheckConflicts = Params->GetBoolField(TEXT("check_conflicts"));
    bool bCheckMissingActions = Params->GetBoolField(TEXT("check_missing_actions"));
    bool bCheckUnusedActions = Params->GetBoolField(TEXT("check_unused_actions"));

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    TArray<TSharedPtr<FJsonValue>> Conflicts;
    TArray<TSharedPtr<FJsonValue>> MissingActions;
    TArray<TSharedPtr<FJsonValue>> UnusedActions;

    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    // Check for key binding conflicts
    if (bCheckConflicts)
    {
        TMap<FString, TArray<FString>> KeyToActions;
        
        for (const FInputActionKeyMapping& ActionMapping : InputSettings->GetActionMappings())
        {
            FString KeyString = ActionMapping.Key.ToString();
            if (ActionMapping.bShift) KeyString += TEXT("+Shift");
            if (ActionMapping.bCtrl) KeyString += TEXT("+Ctrl");
            if (ActionMapping.bAlt) KeyString += TEXT("+Alt");
            if (ActionMapping.bCmd) KeyString += TEXT("+Cmd");
            
            if (!KeyToActions.Contains(KeyString))
            {
                KeyToActions.Add(KeyString, TArray<FString>());
            }
            KeyToActions[KeyString].Add(ActionMapping.ActionName.ToString());
        }

        for (const auto& Pair : KeyToActions)
        {
            if (Pair.Value.Num() > 1)
            {
                TSharedPtr<FJsonObject> ConflictObj = MakeShared<FJsonObject>();
                ConflictObj->SetStringField(TEXT("key"), Pair.Key);
                TArray<TSharedPtr<FJsonValue>> ActionArray;
                for (const FString& Action : Pair.Value)
                {
                    ActionArray.Add(MakeShared<FJsonValueString>(Action));
                }
                ConflictObj->SetArrayField(TEXT("actions"), ActionArray);
                Conflicts.Add(MakeShared<FJsonValueObject>(ConflictObj));
            }
        }
    }

    ResultObj->SetArrayField(TEXT("conflicts"), Conflicts);
    ResultObj->SetArrayField(TEXT("missing_actions"), MissingActions);
    ResultObj->SetArrayField(TEXT("unused_actions"), UnusedActions);
    ResultObj->SetNumberField(TEXT("conflict_count"), Conflicts.Num());
    ResultObj->SetNumberField(TEXT("missing_count"), MissingActions.Num());
    ResultObj->SetNumberField(TEXT("unused_count"), UnusedActions.Num());
    ResultObj->SetBoolField(TEXT("validation_passed"), Conflicts.Num() == 0 && MissingActions.Num() == 0);
    
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleExportInputMappings(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString FilePath;
    if (!Params->TryGetStringField(TEXT("file_path"), FilePath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'file_path' parameter"));
    }

    FString Format = Params->GetStringField(TEXT("format"));
    bool bIncludeAxes = Params->GetBoolField(TEXT("include_axes"));
    bool bIncludeCategories = Params->GetBoolField(TEXT("include_categories"));

    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    TSharedPtr<FJsonObject> ExportObj = MakeShared<FJsonObject>();
    TArray<TSharedPtr<FJsonValue>> ActionArray;
    TArray<TSharedPtr<FJsonValue>> AxisArray;

    // Export action mappings
    for (const FInputActionKeyMapping& ActionMapping : InputSettings->GetActionMappings())
    {
        TSharedPtr<FJsonObject> ActionObj = MakeShared<FJsonObject>();
        ActionObj->SetStringField(TEXT("action_name"), ActionMapping.ActionName.ToString());
        ActionObj->SetStringField(TEXT("key"), ActionMapping.Key.ToString());
        ActionObj->SetBoolField(TEXT("shift"), ActionMapping.bShift);
        ActionObj->SetBoolField(TEXT("ctrl"), ActionMapping.bCtrl);
        ActionObj->SetBoolField(TEXT("alt"), ActionMapping.bAlt);
        ActionObj->SetBoolField(TEXT("cmd"), ActionMapping.bCmd);
        
        ActionArray.Add(MakeShared<FJsonValueObject>(ActionObj));
    }

    ExportObj->SetArrayField(TEXT("actions"), ActionArray);

    // Export axis mappings if requested
    if (bIncludeAxes)
    {
        for (const FInputAxisKeyMapping& AxisMapping : InputSettings->GetAxisMappings())
        {
            TSharedPtr<FJsonObject> AxisObj = MakeShared<FJsonObject>();
            AxisObj->SetStringField(TEXT("axis_name"), AxisMapping.AxisName.ToString());
            AxisObj->SetStringField(TEXT("key"), AxisMapping.Key.ToString());
            AxisObj->SetNumberField(TEXT("scale"), AxisMapping.Scale);
            
            AxisArray.Add(MakeShared<FJsonValueObject>(AxisObj));
        }
        ExportObj->SetArrayField(TEXT("axes"), AxisArray);
    }

    // Convert to string based on format
    FString ExportString;
    if (Format.Equals(TEXT("json"), ESearchCase::IgnoreCase))
    {
        TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&ExportString);
        FJsonSerializer::Serialize(ExportObj.ToSharedRef(), Writer);
    }

    // Write to file
    IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
    if (FFileHelper::SaveStringToFile(ExportString, *FilePath))
    {
        TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
        ResultObj->SetStringField(TEXT("file_path"), FilePath);
        ResultObj->SetStringField(TEXT("format"), Format);
        ResultObj->SetNumberField(TEXT("actions_exported"), ActionArray.Num());
        ResultObj->SetNumberField(TEXT("axes_exported"), AxisArray.Num());
        
        return ResultObj;
    }
    else
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to write file: %s"), *FilePath));
    }
}

// Placeholder implementations for remaining methods
TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleUpdateInputActionMapping(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Update input action mapping not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleRemoveInputActionMapping(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Remove input action mapping not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleApplyInputPreset(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Apply input preset not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateEnhancedInputActionBlueprintNode(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Create enhanced input action blueprint node not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateInputAxisBlueprintNode(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Create input axis blueprint node not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleTestInputAction(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Test input action not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleImportInputMappings(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Import input mappings not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateInputContext(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Create input context not implemented yet"));
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCreateInputTrigger(const TSharedPtr<FJsonObject>& Params)
{
    return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Create input trigger not implemented yet"));
}

TArray<TSharedPtr<FJsonObject>> FUnrealMCPEnhancedInputCommands::GetInputMappingsForCategory(const FString& Category)
{
    return TArray<TSharedPtr<FJsonObject>>();
}

bool FUnrealMCPEnhancedInputCommands::ValidateKeyBinding(const FString& KeyName)
{
    return FKey(*KeyName).IsValid();
}

FString FUnrealMCPEnhancedInputCommands::GetInputPresetTemplate(const FString& PresetType)
{
    return TEXT("");
}

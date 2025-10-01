@echo off
setlocal enabledelayedexpansion

REM Universal UE 5.6 Project Build Script
REM Automatically detects project type and builds accordingly
REM Supports: Regular projects, Plugin projects, and Plugin-only builds

set VERSION=5.6
set "UE_ROOT=C:\Program Files\Epic Games\UE_%VERSION%"
set "RUNUAT_PATH=%UE_ROOT%\Engine\Build\BatchFiles\RunUAT.bat"
set "UNREALBUILDTOOL_PATH=%UE_ROOT%\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe"
set PROJECT_NAME=
set PROJECT_FILE=
set PLUGIN_PATH=
set BUILD_TYPE=

REM Detect project type and files
echo.
echo ========================================
echo Universal UE 5.6 Project Builder
echo ========================================
echo.

REM Check if we're in a UE project directory
if exist "*.uproject" (
    for %%f in (*.uproject) do (
        set PROJECT_FILE=%%f
        set PROJECT_NAME=%%~nf
        set BUILD_TYPE=PROJECT
        goto :found_project
    )
)

REM Check if we're in a plugin directory or have plugins to build
if exist "Plugins\*.uplugin" (
    set BUILD_TYPE=PLUGIN
    goto :found_plugin
)

REM Check if current directory contains a .uplugin file
if exist "*.uplugin" (
    for %%f in (*.uplugin) do (
        set PLUGIN_PATH=%%f
        set BUILD_TYPE=SINGLE_PLUGIN
        goto :found_single_plugin
    )
)

echo ERROR: No valid UE project or plugin found in current directory
echo.
echo This script looks for:
echo - *.uproject files for project builds
echo - Plugins\*.uplugin for plugin builds
echo - *.uplugin for single plugin builds
echo.
echo Current directory: %cd%
echo.
pause
exit /b 1

:found_project
echo Found UE Project: %PROJECT_NAME%
echo Project File: %PROJECT_FILE%
echo.

REM Generate solution files if they don't exist
if not exist "%PROJECT_NAME%.sln" (
    echo Generating Visual Studio solution files...
    "%UNREALBUILDTOOL_PATH%" -projectfiles -project="%cd%\%PROJECT_FILE%" -game -rocket -progress
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to generate solution files
        pause
        exit /b 1
    )
    echo Solution files generated successfully!
    echo.
)

REM Check if this project has plugins to build
set HAS_PLUGINS=0
if exist "Plugins\*.uplugin" (
    set HAS_PLUGINS=1
    echo This project contains plugins - building both project and plugins
    echo.
)

REM Build the project
if exist "Source" (
    echo Building project: %PROJECT_NAME%
    echo.
    
    "%UNREALBUILDTOOL_PATH%" %PROJECT_NAME%Editor Win64 Development -Project="%cd%\%PROJECT_FILE%" -WaitMutex -FromMsBuild
    
    if %ERRORLEVEL% EQU 0 (
        echo SUCCESS: Project %PROJECT_NAME% built successfully!
        echo.
    ) else (
        echo ERROR: Project build failed with error code %ERRORLEVEL%
        echo.
    )
) else (
    echo No Source directory found - skipping project build (plugin-only project)
    echo.
)

REM Build plugins if they exist
if %HAS_PLUGINS%==1 (
    echo Building project plugins...
    echo.
    
    for /r Plugins %%f in (*.uplugin) do (
        set PLUGIN_FILE=%%f
        set PLUGIN_NAME=%%~nf
        echo Building plugin: !PLUGIN_NAME!
        echo Plugin File: !PLUGIN_FILE!
        echo.
        
        "%RUNUAT_PATH%" BuildPlugin -Plugin="!PLUGIN_FILE!" -Package="%TEMP%\!PLUGIN_NAME!_%VERSION%" -HostPlatforms=Win64 -NoTargetPlatforms -StrictIncludes
        
        if %ERRORLEVEL% EQU 0 (
            echo SUCCESS: Plugin !PLUGIN_NAME! built successfully!
        ) else (
            echo ERROR: Plugin !PLUGIN_NAME! build failed with error code %ERRORLEVEL%
        )
        echo.
    )
)
goto :end

:found_plugin
echo Found Plugin Directory
echo.

REM Build all plugins in the Plugins directory
for /r Plugins %%f in (*.uplugin) do (
    set PLUGIN_FILE=%%f
    set PLUGIN_NAME=%%~nf
    echo Building plugin: !PLUGIN_NAME!
    echo Plugin File: !PLUGIN_FILE!
    echo.
    
    "%RUNUAT_PATH%" BuildPlugin -Plugin="!PLUGIN_FILE!" -Package="%TEMP%\!PLUGIN_NAME!_%VERSION%" -HostPlatforms=Win64 -NoTargetPlatforms -StrictIncludes
    
    if %ERRORLEVEL% EQU 0 (
        echo SUCCESS: Plugin !PLUGIN_NAME! built successfully!
    ) else (
        echo ERROR: Plugin !PLUGIN_NAME! build failed with error code %ERRORLEVEL%
    )
    echo.
)
goto :end

:found_single_plugin
echo Found Single Plugin: %PLUGIN_PATH%
echo.

"%RUNUAT_PATH%" BuildPlugin -Plugin="%PLUGIN_PATH%" -Package="%TEMP%\Plugin_%VERSION%" -HostPlatforms=Win64 -NoTargetPlatforms -StrictIncludes

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: Plugin built successfully!
    echo Build package created at: %TEMP%\Plugin_%VERSION%
    echo.
) else (
    echo.
    echo ERROR: Plugin compilation failed with error code %ERRORLEVEL%
    echo.
)
goto :end

:end
echo ========================================
echo Build process completed
echo ========================================
echo.
pause

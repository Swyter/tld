@echo off
set OLDPATH=%PATH%
set PATH="C:\Python24";"C:\Python26";%PATH%

python process_init.py
python process_global_variables.py
python process_strings.py
python process_skills.py
python process_music.py
python process_animations.py
python process_meshes.py
python process_sounds.py
python process_skins.py
python process_map_icons.py
python process_factions.py
python process_items.py
python process_scenes.py
python process_troops.py
python process_particle_sys.py
python process_scene_props.py
python process_tableau_materials.py
python process_presentations.py
python process_party_tmps.py
python process_parties.py
python process_quests.py
python process_scripts.py
python process_mission_tmps.py
python process_game_menus.py
python process_simple_triggers.py
python process_dialogs.py
python process_global_variables_unused.py
set PATH=%OLDPATH%
@del *.pyc
REM
REM adding scripts on map with mapscribbler... (mtarini)
echo Adding text map-icons with MapScribbler...
copy /Y ..\parties.txt ..\parties.orig.txt  >nul
copy /Y ..\map_icons.txt ..\map_icons.orig.txt >nul
cd mapScribbler_0.7
mapScribbler.exe -b
type stderr.txt
cd ..
REM
REM count objects... (mtarini)
set /a cnt=0
set /a max=915
for /f %%a in ('type "ID_items.py"^|find "" /v /c') do set /a cnt=%%a
set /a cnt = cnt-1 
IF /I %cnt% LSS %max% ( 
echo Item count: %cnt%/%max% ... ok.
) ELSE ( 
echo Item count: %cnt%/%max% ... ERROR ERROR ERROR TOO MANY!!!.
)
REM
REM 
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key . . .
pause>nul
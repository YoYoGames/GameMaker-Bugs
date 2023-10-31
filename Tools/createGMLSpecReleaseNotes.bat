set LOCALGM=c:/source/GameMaker
set RUNTIMEGM=C:\ProgramData\GameMakerStudio2\Cache\runtimes\runtime-2023.8.2.152
python "compareGMLSpec.py"  "%LOCALGM%/Zeus/compiler/GMLSpec.xml" "%RUNTIMEGM%/GmlSpec.xml" >c:\temp\output.md
python "compareGmlSpec.py"  "%LOCALGM%/Zeus/compiler/PS4/GMLSpec.xml" "%RUNTIMEGM%/PS4/GmlSpec.xml" >>c:\temp\output.md
python "compareGmlSpec.py"  "%LOCALGM%/Zeus/compiler/PS5/GMLSpec.xml" "%RUNTIMEGM%/PS5/GmlSpec.xml" >>c:\temp\output.md
python "compareGmlSpec.py"  "%LOCALGM%/Zeus/compiler/Switch//GMLSpec.xml" "%RUNTIMEGM%/Switch/GmlSpec.xml" >>c:\temp\output.md
python "compareGmlSpec.py"  "%LOCALGM%/Zeus/compiler/XboxSeriesXS//GMLSpec.xml" "%RUNTIMEGM%/XboxSeriesXS/GmlSpec.xml" >>c:\temp\output.md
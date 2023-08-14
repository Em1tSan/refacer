@echo off
set pypath=home = %~dp0python
set venvpath=_ENV=%~dp0venv
if exist venv (powershell -command "$text = (gc venv\pyvenv.cfg) -replace 'home = .*', $env:pypath; $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False);[System.IO.File]::WriteAllLines('venv\pyvenv.cfg', $text, $Utf8NoBomEncoding);$text = (gc venv\scripts\activate.bat) -replace '_ENV=.*', $env:venvpath; $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False);[System.IO.File]::WriteAllLines('venv\scripts\activate.bat', $text, $Utf8NoBomEncoding);")

for /d %%i in (tmp\tmp*,tmp\pip*) do rd /s /q "%%i" 2>nul || ("%%i" && exit /b 1) & del /q tmp\tmp* > nul 2>&1 & rd /s /q pip\cache 2>nul

set appdata=tmp
set userprofile=tmp
set temp=tmp
set PATH=git\cmd;python;venv\scripts;ffmpeg;cuda;cuda\bin;cuda\lib;tensorrt;tensorrt\bin;tensorrt\lib

set PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:512
set CUDA_MODULE_LOADING=LAZY
set CUDA_PATH=cuda

call venv\Scripts\activate.bat
python app_en.py --gpu-threads 8 --max-memory 16000 --use_video_path --frame_limit 2000 --video_quality 40 --autolaunch
pause

REM Packaged and assembled by Neutogen News Telegram channel: https://t.me/neurogen_news

REM --gpu-threads N - Number of threads for your video card. Too high a value can cause errors or conversely, reduce performance. 4 threads consume about 5.5-6 Gb VRAM, 8 threads consume 10 Gb VRAM, but peak consumption can be higher. 
REM --tensorrt to enable TensorRT acceleration (Nvidia RTX 20xx, 30xx, 40xx) (experimental, most often crashes)
REM --autolaunch to enable/disable UI autolaunch
REM --share_gradio which generates a link for access from the network
REM --max_num_faces N - to set the maximum number of faces to replace. 
REM --max-memory 8000 - the amount of allocated RAM in megabytes
REM --frame_limit 2000 - how many frames we process at a time


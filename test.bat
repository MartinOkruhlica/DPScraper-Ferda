@echo off

cd /d "C:\Users\Fujitsu\OneDrive\Projects\DPScraper Ferda"

where python
python --version
python -c "import helper; print(helper.__file__); print(dir(helper))"

pause
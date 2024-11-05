@echo off
e:
cd "\PATH TO PDF MERGE PYTHON SCRIPT\PDF Merge"
call "\PATH TO PDF MERGE PYTHON SCRIPT\PDF Merge\venv\Scripts\activate.bat"
start /min python merge.py

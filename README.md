# PDscripting
Design and integration of custom scripting nodes into the software Proteome Discoverer

Hi all, in this repository I'll be sharing my efforts to integrate custom Python scripts into the software Proteome Discoverer.

# Contents of this File

- Introduction
- Background
- Files
  - Pulldown
    - Code
    - Usage
    - Examples
  - Calib_Log
    - Code
    - Usage
    - Examples
  - MixRatio_pd
    - Code
    - Usage
    - Examples

# Background

These nodes can be useful for optimizing the efficiency and replicability of experiments and analysis done using the proteome discoverer suite. All of these nodes were written in python and executed on a computer WITHOUT the python interpreter present. To do this, I installed a Python package called pyinstaller (pip install pyinstaller) from the spyder console. From there, one can use windows powershell to navigate to the directory where your python file is and use a pyinstaller command to convert a python file to an exe, that can run in a single click and on any computer with or without a python interpreter. There are two main options for this command, (pyinstaller file.py) and (pyinstaller file.py --onefile). The advantage of the second is that the exe will be written as a single large file, ~350 MB. If you are building multiple exes, though, I recommend using the first, which ports out the necessary python files (~800 MB, somehow) and the exe will reference them. In this case, the whole folder of supporting files must be moved to the workstation. From there, all one has to do is store the exe files on the local drive of the computer using PD. Their direct location can be called from PD's Scripting Node. The Scripting Node requests 5 parameters.

1. Path to executable
  Simple enough. The path to your .exe file stored on the PD computer local drive.
2. Command line arguments.
  Data that gets passed to your script. The first parameter should always be %NODEARGS%. This is the location of the information about your requested tables, which     will be important for any data processing. Other than that, you can pass any information you want as a string in this section. These values can be changed at runtime   by the user.
3. Requested Tables. 
  Format : (Table1; Table2:Column1, Column2, Column3; Table3). These need to be the exact name of the tables that you need.
4. Use R-friendly columns. 
  I believe this changes column names to remove characters that cause issues in R. I generally do True anyway.
5. Archive Datafiles. 
  Writes an archive of JSON files and txt files. Useful sometimes when testing.

# Files

# Pulldown

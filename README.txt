Python files:
1. IntroWindowInterface.py - interface for the intro window, main assembly.
2. ConfigWindowInterface.py - interface for the creating configuration window, 
				function of creating configuration file
3. TabWindowInterface.py - interface for the results' window. Includes Signal, Harmonic, 
				Displacement and Poles' Geometry tabs. Puts together the 
				mathematical processes.
4. SignalTavInterface.py - interface for the signal tab. Includes a graph and buttons to 
				switch between the coils.
5. Harmonics.py - interface for the harmonics tab. Includes a bar chart, a table to represent
				the math process and buttons to switch between the coils.
6. DisplacementTabInterface.py - interface for the displacement tab. Includes a chart and a table.
7. Poles.py - interface for the poles' geometry tab. Includes a table of the poles' geometry 
				deviation and a chart of the real geometry.
8. Get_Data.py - contains functions to parse files with data.
9. Libs.py - imports neceessary libraries.
10. Mathematics.py - contains all the mathematical processes.
11. save_data.py - contains the function to save certain data.
12. Style.py - contains the style methods.
13. ui_form.py - interface for the configuration creator, made in QtCreator.
14. ui_mainwindow.py - interface for the intro window, made in QtCreator.

Other files:
1. Configuration.cfg - configuration file for the programm. Takes pathes of the external files.
2. leftarrow.png and rightarrow.png - icons for buttons.
3. NewConfid.cfg - a new configuration file for a coil system made in configuration creator.
4. Template.cfg - a template for a new configuration file.
5. winIcon.png - the programme window icon.
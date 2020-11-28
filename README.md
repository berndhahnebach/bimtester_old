# BIMTester
### BIMTester code in FreeCAD
+ ATM bimtester code is copied into the FreeCAD bimtester module for for the sake of convenience
+ TODO bimtester should be installed in conjunction with ifcopenshell
+ to /urs/local by make install

### Generall information
+ This applies to BlenderBIM BIMTester and FreeCAD BIMTester.
+ Neither the ifc nor the ifc path should contain special character like German Umlaute.
+ Neither import nor open a ifc in FreeCAD or BlenderBIM. There is no need for this to run BIMTester.
+ Get Schependomlaan from https://github.com/buildingSMART/Sample-Test-Files/blob/master/IFC%202x3/Schependomlaan/Design%20model%20IFC/IFC%20Schependomlaan.ifc


### BIMTester in FreeCAD:
+ Install module
+ Install missing dependencies on Linux.
    + Do not use behave from Debian buster repo (it is to old)
    + install behave with pip3
+ Install missing dependencies on Windows.
    + copy behave and pystache from BlenderBIM AddOn to FreCAD_xxx/bin/Lib/ 
    + behave could be installed with pip from FreeCAD
    + pystache install with FreeCAD pip results in an error
+ start FreeCAD, switch to BIMTester, the Gui will start
+ choose ifc file (the feature file directory is set to a very simple included example feature file)
+ click on run
+ :-)


### BIMTester in BlenderBIM
+ Install Blender and install BlenderBIM (see my blender notes)
+ Start Blender
+ Set path to feature files (set the path not the file)
+ choose the feature file to run with
   + either the ifc must be in the same directory as the feature file,
   + or the full path to the ifc has to be in the feature file
   + find a simple example in FreeCAD BIMTester module directory features_bimtester/fea_min/features/
   + or use these ones: https://wiki.osarch.org/index.php?title=Category:BIMTester
+ click execute
+ no matter which scenario is choosen, all scenarios will run (TODO)


### Behave code examples
+ directly run behave
+ TODO: add from my local machine


### Remaining issues
+ https://github.com/behave/behave/issues/264
+ https://github.com/behave/behave/issues/549

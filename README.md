### Generall information
+ the ifc should not be on a windows network resource
+ ATM it has to be locally


### BIMTester in BlenderBIM
+ install Blender and install BlenderBIM (see my blender notes)
+ get Schependomlaan from https://github.com/buildingSMART/Sample-Test-Files/blob/master/IFC%202x3/Schependomlaan/Design%20model%20IFC/IFC%20Schependomlaan.ifc
+ get feature file from https://gitlab.com/wartburgritter/fcusermod/-/tree/master/bimtester/features
+ open Blender
+ do not import a ifc, there is no need
+ set path to feature files (set the path not the file)
+ choose the feature file to run with
   + either the ifc must be in the same directory as the feature file,
   + or the full path to the ifc has to be in the feature file
+ click execute
+ no matter which scenario is choosen, all szenarios will run (TODO)
+ it does not work from netzwerkpfad im buero, copy to desktop


### BIMTester in FreeCAD - This workbench
+ get my workbench bimtester
+ on linux install missing dependencies from Debian repo
+ on windows copy behave and pystache from BlenderBIM AddOn to FreCAD_xxx/bin/Lib/ (pystache install with pip results in an error)
+ open ifc ... :-)


### Code examples
+ TODO: add from my local machine

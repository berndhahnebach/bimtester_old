Feature: Building Elements, Attributes and PSets

In order to correctly analyse objects
As any interested stakeholder analyses properties and thier values
All IFC elements must have the appropriate properties and psets

Scenario: Receiving a file
 * The IFC file "myifc.ifc" must be provided
 * IFC data must use the IFC2X3 schema


Scenario: Ensure my test
# * All parts have an {property} attribute in the {pset} attributeset
 * All parts have an Umbaukategorie attribute in the AllplanAttributes attributeset

# wobei ja normal einfach alle IfcBuildingElementProxy bei uns die Attribute nicht haben ...
# da brauch ich keinen super test, wobei man muss explizit schauen, der test macht es automatisch
# aber schon der IfcBuildingElement Proxy test sollte etwas ausgeben
# der smartview muss im dateinamen den test haben, je failed test ein smartview
# naja man kann nie wissen

# a building element is a IfcBuildingElement and all its childs

# AUFPASSEN Es gibt AllplanAttributes und Allplan Attributes psets ...
# neuer export 2x3, Allplan 2018 mit Leerzeichen, Allplan 2020 ohne Leerzeichen

# TODO: uebersicht ueber das projekt und die anzahl der element class elemente in jedem test mit ausgeben.
# zumindest im Logfile ...
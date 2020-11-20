Feature: Element classes

In order to correctly display and use objects
As any interested stakeholder
All IFC elements must have the correct geometric representation

Scenario: Receiving a file
 * The IFC file "myifc.ifc" must be provided
 * IFC data must use the IFC2X3 schema


Scenario: No Proxies
# * There are no {ifc_class} elements because {reason}
 * There are no IfcBuildingElementProxy elements because Bernd does not like them


Scenario: Ensure all IFC type elements use the correct IFC class
 * The element 3p_tA_ccLEYuxpPgwzi8pH is an IfcSpace
 * The element 1234567891234567891234 is an IfcSpace
# * The element 3qlbUuWS9A88oE2tMvG66y is an IfcSlab

# * The element 3qlbUuWS9A88oE2tMvG66y is further defined as a .FLOOR.

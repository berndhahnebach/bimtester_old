Feature: Geometric Representations

In order to correctly identify objects
As any interested stakeholder filtering objects for a particular purpose
All IFC elements must belong to the appropriate IFC class

Scenario: Receiving a file
 * The IFC file "myifc.ifc" must be provided
 * IFC data must use the IFC2X3 schema


Scenario: Ensure all IFC type elements have correct representation
# * All {ifc_class} elements have an {representation_class} representation
 * All IfcColumn elements have an IfcFacetedBrep representation
 * All IfcSlab elements have an IfcFacetedBrep representation


Scenario: Ensure all elements have correct geometry
 * All elements must have a shape without errors

Feature: Attributes and PSets

In order to correctly analyse objects
As any interested stakeholder analyses properties and thier values
All IFC elements must have the appropriate properties and psets

Scenario: Receiving a file
 * The IFC file "myifc.ifc" must be provided
 * IFC data must use the IFC2X3 schema


Scenario: Ensure all IFC type elements have correct properties attached
# * All (?P<ifc_class>.*) elements have an? (?P<property_path>.*\..*) property
# * All IfcColumn elements have an "AllplanAttributes.Umbaukategorie" property

# * All {ifc_class} elements have an {property} property in the {pset} pset
# * All IfcSpace elements have an Reference property in the Pset_SpaceCommon pset
 * All IfcSpace elements have an Category property in the Pset_SpaceCommon pset
 * All IfcSpace elements have an OccupancyNumber property in the Pset_SpaceOccupancyRequirements pset
 * All IfcSpace elements have an Illuminance property in the Pset_SpaceLightingRequirements pset
 * All IfcSpace elements have an Renovation Status property in the AC_Pset_RenovationAndPhasing pset
 * All IfcSpace elements have an FloorCovering property in the Pset_SpaceCoveringRequirements pset
 * All IfcSpace elements have an CeilingCovering property in the Pset_SpaceCoveringRequirements pset
 * All IfcSpace elements have an WallCovering property in the Pset_SpaceCoveringRequirements pset
 * All IfcSpace elements have an Raumnutzung_nach_SIA_2024 property in the Zusaetzliche_Element_Eigenschaften_Schweiz pset


# AUFPASSEN Es gibt AllplanAttributes und Allplan Attributes psets ...
# neuer export 2x3, Allplan 2018 mit Leerzeichen, Allplan 2020 ohne Leerzeichen

# TODO: uebersicht ueber das projekt und die anzahl der element class elemente in jedem test mit ausgeben.
# zumindest im Logfile ...

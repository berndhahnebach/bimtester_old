Feature: Project setup

In order to view the BIM data
As any interested stakeholder
We need an IFC file

Feature: Project setup

In order to ensure quality of the digital built environment
As a responsible digital citizen
We expect compliant OpenBIM deliverables


Scenario: Receiving a file
# * The IFC file "{file}" is exempt from being provided
# if executed from Blender for the first time
# the full path to ifc-file must be given or
# ifc-file must be in the same directory as the feature file
# later on the ifc will be found even if the full path is not given

 * The IFC file "myifc.ifc" must be provided

 * IFC data must use the IFC2X3 schema

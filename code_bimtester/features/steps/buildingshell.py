import json
from behave import step

from utils import IfcFile


# behave needs to be started with a option to redirect prints
# see bimtesters run module
# keep in mind on a fail the output is catched and not printed
# use assert False and output inside this assert


@step("all {ifc_class} elements have an {aproperty} property in the {pset} pset")
def step_impl(context, ifc_class, aproperty, pset):
    logfile = open(context.thelogfile, "a")
    logfile.write("PropTest: {}, {}, {}\n".format(ifc_class, aproperty, pset))
    elements = IfcFile.get().by_type(ifc_class)
    false_elements_elem = []
    false_elements_guid = []
    from ifcopenshell.util.element import get_psets
    for elem in elements:
        psets = get_psets(elem)
        if not (pset in psets and aproperty in psets[pset]):
            false_elements_elem.append(str(elem))
            false_elements_guid.append(elem.GlobalId)
        logfile.write("{} --> {}\n".format(elem.id(), psets))
    logfile.write("{}\n".format(json.dumps(false_elements_elem, indent=2)))
    logfile.close()

    context.falseguids = false_elements_guid
    if len(false_elements_elem) > 0:
        assert False, (
            "Some elemets missing the pset or property: {}"
            .format(json.dumps(false_elements_elem, indent=2))
        )
        # see UUID is a IfcSpace test, there AssertionFals with smart output from utils module


# "all building elements have an {aproperty} property in the {pset} pset")
# but than the ambiguous problem, thus use different words
@step("all parts have an {attribute} attribute in the {myattributesum} attributeset")
def step_impl(context, attribute, myattributesum):
    logfile = open(context.thelogfile, "a")
    logfile.write("PropTest: {}, {}\n".format(attribute, myattributesum))
    elements = IfcFile.get().by_type("IfcBuildingElement")
    false_elements_elem = []
    false_elements_guid = []
    from ifcopenshell.util.element import get_psets
    for elem in elements:
        psets = get_psets(elem)
        if not (myattributesum in psets and attribute in psets[myattributesum]):
            false_elements_elem.append(str(elem))
            false_elements_guid.append(elem.GlobalId)
        logfile.write("{} --> {}\n".format(elem.id(), psets))
    logfile.write("{}\n".format(sorted(false_elements_elem)))
    logfile.close()

    context.falseguids = false_elements_guid
    if len(false_elements_elem) > 0:
        assert False, (
            "Some elemets missing the pset or property: {}"
            .format(json.dumps(false_elements_elem, indent=2))
        )


@step("all elements must have a shape without errors")
def step_impl(context):
    elements = IfcFile.get().by_type("IfcBuildingElement")

    import Part  # FreeCAD is needed
    # bernds geometry check is needed
    from bimstatiktools import geomchecks
    from importlib import reload
    reload(geomchecks)

    from ifcopenshell import geom as ifcgeom
    settings = ifcgeom.settings()
    settings.set(settings.USE_BREP_DATA, True)
    settings.set(settings.SEW_SHELLS, True)
    settings.set(settings.USE_WORLD_COORDS, True)

    false_elements_error = {}
    false_elements_guid = []
    for elem in elements:
        # TODO: some print and update gui and or flush, this could take time
        try:
            # TODO distinguish if there is not representation
            # or ifcos does not return a valid representation
            cr = ifcgeom.create_shape(settings, elem)
            brep = cr.geometry.brep_data
        except Exception:
            brep = None
        if brep:
            shape = Part.Shape()
            shape.importBrepFromString(brep)
            shape.scale(1000.0)  # IfcOpenShell always outputs in meters
            error = geomchecks.checkSolidGeometry(shape)
        else:
            error = "  IfcOpenShell failed to process the geometric representation."
        if error != "":
            print(error)
            Part.show(shape)
            false_elements_error[elem.id()] = error
            false_elements_guid.append(elem.GlobalId)

    context.falseguids = false_elements_guid
    if len(false_elements_error) > 0:
        assert False, (
            "Geometry elements errors: {}"
            .format(json.dumps(false_elements_error, indent=2))
        )

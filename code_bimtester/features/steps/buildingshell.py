from behave import step
from utils import IfcFile

import helpertools


# behave needs to be started with a option to redirect prints
# see fcbimtester module
# keep in mind on a fail the output is catched and not printed
# use assert False and output inside this assert


@step("all {ifc_class} elements have an {aproperty} property in the {pset} pset")
def step_impl(context, ifc_class, aproperty, pset):
    logfile = open(context.thelogfile, "a")
    logfile.write("PropTest: {}, {}, {}\n".format(ifc_class, aproperty, pset))
    elements = IfcFile.get().by_type(ifc_class)
    false_elements_id = []
    false_elements_guid = []
    from ifcopenshell.util.element import get_psets
    for element in elements:
        psets = get_psets(element)
        if not (pset in psets and aproperty in psets[pset]):
            false_elements_id.append(element.id())
            false_elements_guid.append(element.GlobalId)
        logfile.write("{} --> {}\n".format(element.id(), psets))
    logfile.write("{}\n".format(sorted(false_elements_id)))
    logfile.close()
    if len(false_elements_id) > 0:
        assert False, (
            "Some elemets missing the pset or property: {}, {}"
            .format(false_elements_id, false_elements_guid)
        )
        # see UUID is a IfcSpace test, there AssertionFals with smart output from utils module

    # Wenn ein test in einem scenario fehl schlaegt und der gleiche test nochmal kommt
    # dann kommt gelb im report "This requirement has not yet been specified."
    # normal sollten diese aber auch noch ablaufen.
    # schoen auch zu sehen an The element {uuid} is an {ifc_class}
    # der erste schlaegt fehl, der zweite "This requirement has not yet been specified."
    # https://community.osarch.org/discussion/comment/3328/#Comment_3328


# "all building elements have an {aproperty} property in the {pset} pset")
# but than the ambiguous problem, thus use different words
@step("all parts have an {attribute} attribute in the {myattributesum} attributeset")
def step_impl(context, attribute, myattributesum):
    logfile = open(context.thelogfile, "a")
    logfile.write("PropTest: {}, {}\n".format(attribute, myattributesum))
    elements = IfcFile.get().by_type("IfcBuildingElement")
    false_elements_id = []
    false_elements_guid = []
    from ifcopenshell.util.element import get_psets
    for elem in elements:
        psets = get_psets(elem)
        if not (myattributesum in psets and attribute in psets[myattributesum]):
            false_elements_id.append(elem.id())
            false_elements_guid.append(elem.GlobalId)
        logfile.write("{} --> {}\n".format(elem.id(), psets))
    logfile.write("{}\n".format(sorted(false_elements_id)))
    logfile.close()
    if len(false_elements_id) > 0:
        helpertools.append_zoom_smartview(
            context.thesmfile,
            context.scenario.name,
            false_elements_guid
        )
        assert False, (
            "Some elemets missing the pset or property: {}, {}"
            .format(false_elements_id, false_elements_guid)
        )


@step("All elements must have a shape without errors")
def step_impl(context):
    elements = IfcFile.get().by_type("IfcBuildingElement")

    import Part  # FreeCAD is needed
    # bernds geometry check is needed
    from bimstatiktools import geomchecks
    from importlib import reload
    reload(geomchecks)

    from ifcopenshell import geom as ifcgeom
    settings = ifcgeom.settings()
    settings.set(settings.USE_BREP_DATA,True)
    settings.set(settings.SEW_SHELLS,True)
    settings.set(settings.USE_WORLD_COORDS,True)

    false_elements_error = {}
    false_elements_guid = []
    for elem in elements:
        # TODO: some print and update gui and or flush, this could take time
        cr = ifcgeom.create_shape(settings, elem)
        brep = cr.geometry.brep_data
        shape = Part.Shape()
        shape.importBrepFromString(brep)
        shape.scale(1000.0)  # IfcOpenShell always outputs in meters
        error = geomchecks.checkSolidGeometry(shape)
        if error != "":
            print(error)
            Part.show(shape)
            false_elements_error[elem.id()] = error
            false_elements_guid.append(elem.GlobalId)

    if len(false_elements_error) > 0:
        helpertools.append_zoom_smartview(
            context.thesmfile,
            context.scenario.name,
            false_elements_guid
        )
        assert False, (
            "Geometry elements errors: {}"
            .format(false_elements_error)
        )

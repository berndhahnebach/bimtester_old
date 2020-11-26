from behave import step

from utils import IfcFile


# for output on a failed step: 
# use assert False and output inside this assert

# TODO: for even smarter output on a failed step:
# see UUID is a IfcSpace test in element_classes.py
# there own assert types implemented in utils


@step("all {ifc_class} elements have an {aproperty} property in the {pset} pset")
def step_impl(context, ifc_class, aproperty, pset):

    elements = IfcFile.get().by_type(ifc_class)

    context.falseelems = []
    context.falseguids = []
    context.falseprops = {}
    from ifcopenshell.util.element import get_psets
    for elem in elements:
        psets = get_psets(elem)
        if not (pset in psets and aproperty in psets[pset]):
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
        context.falseprops[elem.id()] = str(psets) 

    if len(context.falseelems) > 0:
        assert False, (
            "Some elemets missing the pset or property:\n{}"
            .format(context.falseguids)
        )


@step("all elements must have a shape without errors")
def step_impl(context):

    elements = IfcFile.get().by_type("IfcBuildingElement")

    context.falseelems = []
    context.falseguids = []
    context.falseprops = {}

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
            error = "  IfcOS failed to process the geometric representation."
        if error != "":
            # the error is printed in the geomchecks method allready
            # print(error)
            Part.show(shape)
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
            context.falseprops[elem.id()] = error

    if len(context.falseelems) > 0:
        assert False, (
            "Geometry elements errors:\n{}"
            .format(context.falseguids)
        )

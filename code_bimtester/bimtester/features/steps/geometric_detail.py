from behave import step

from utils import assert_attribute
from utils import IfcFile


@step("All elements must be under {number} polygons")
def step_impl(context, number):
    number = int(number)
    errors = []
    for element in IfcFile.get().by_type("IfcElement"):
        if not element.Representation:
            continue
        total_polygons = 0
        tree = IfcFile.get().traverse(element.Representation)
        for e in tree:
            if e.is_a("IfcFace"):
                total_polygons += 1
            elif e.is_a("IfcPolygonalFaceSet"):
                total_polygons += len(e.Faces)
            elif e.is_a("IfcTriangulatedFaceSet"):
                total_polygons += len(e.CoordIndex)
        if total_polygons > number:
            errors.append((total_polygons, element))
    if errors:
        message = (
            "The following {} elements are over 500 polygons:\n"
            .format(len(errors))
        )
        for error in errors:
            message += "Polygons: {} - {}\n".format(error[0], error[1])
        assert False, message


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

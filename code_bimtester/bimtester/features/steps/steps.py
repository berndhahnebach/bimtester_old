from behave import step

from utils import IfcFile


# for output on a failed step:
# use assert False and output inside this assert

# TODO: for even smarter output on a failed step:
# see UUID is a IfcSpace test in element_classes.py
# there own assert types implemented in utils
# or see geolocation assert_pset


@step("there are no {ifc_class} elements because {reason}")
def step_impl(context, ifc_class, reason):

    context.falseelems = []
    context.falseguids = []

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        context.falseelems.append(str(elem))
        context.falseguids.append(elem.GlobalId)

    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "All {} elements in the file are {}."
            .format(elemcount, ifc_class)
        )
    if falsecount > 0:
        assert False, (
            "{} of {} element are {} elements: {}"
            .format(falsecount, elemcount, ifc_class, context.falseelems)
        )


@step('all {ifc_class} elements have a name given')
def step_impl(context, ifc_class):

    context.falseelems = []
    context.falseguids = []

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        # print(elem.Name)
        if not elem.Name:
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
 
    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "The name of all {} {} elements is not set."
            .format(elemcount, ifc_class)
        )
    if falsecount > 0:
        assert False, (
            "The name of {} out of {} {} elements is not set."
            .format(falsecount, elemcount, ifc_class, context.falseelems)
        )


@step('all {ifc_class} elements have a description given')
def step_impl(context, ifc_class):

    context.falseelems = []
    context.falseguids = []

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        # print(elem.Description)
        if not elem.Description:
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
 
    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "The description of all {} {} elements is not set."
            .format(elemcount, ifc_class)
        )
    if falsecount > 0:
        assert False, (
            "The description of {} out of {} {} elements is not set."
            .format(falsecount, elemcount, ifc_class, context.falseelems)
        )


@step('all {ifc_class} elements class attributes have a value')
def step_impl(context, ifc_class):

    from ifcopenshell.ifcopenshell_wrapper import schema_by_name
    # schema = schema_by_name("IFC2X3")
    schema = schema_by_name(IfcFile.get().schema)
    class_attributes = []
    for cl_attrib in schema.declaration_by_name(ifc_class).all_attributes():
        class_attributes.append(cl_attrib.name())
    # print(class_attributes)

    context.falseelems = []
    context.falseguids = []
    context.falseprops = {}

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        failed_attribs = []
        elem_failed = False
        for cl_attrib in class_attributes:
            attrib_value = getattr(elem, cl_attrib)
            if not attrib_value:
               elem_failed = True
               failed_attribs.append(cl_attrib)
               # print(attrib_value)
        if elem_failed is True:
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
            context.falseprops[elem.id()] = failed_attribs

    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "For all {} {} elements at least "
            "one of these class attributes {} has no value."
            .format(elemcount, ifc_class, failed_attribs)
        )
    if falsecount > 0:
        assert False, (
            "For the following {} out of {} {} elements at least "
            "one of these class attributes {} has no value: {}"
            .format(
                falsecount,
                elemcount,
                ifc_class,
                failed_attribs,
                context.falseelems
            )
        )
    # TODO output which attributs are None


@step('all {ifc_class} elements have a name matching the pattern "{pattern}"')
def step_impl(context, ifc_class, pattern):
    import re

    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if not re.search(pattern, element.Name):
            assert False


@step("all {ifc_class} elements have an {representation_class} representation")
def step_impl(context, ifc_class, representation_class):

    def is_item_a_representation(item, representation):
        if "/" in representation:
            for cls in representation.split("/"):
                if item.is_a(cls):
                    return True
        elif item.is_a(representation):
            return True

    context.falseelems = []
    context.falseguids = []
    context.falseprops = {}
    rep = None

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        if not elem.Representation:
            continue
        has_representation = False
        for representation in elem.Representation.Representations:
            for item in representation.Items:
                if item.is_a("IfcMappedItem"):
                    # We only check one more level deep.
                    for item2 in item.MappingSource.MappedRepresentation.Items:
                        if is_item_a_representation(item2, representation_class):
                            has_representation = True
                        rep = item2
                else:
                    if is_item_a_representation(item, representation_class):
                        has_representation = True
                    rep = item
        if not has_representation:
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
            context.falseprops[elem.id()] = str(rep)

    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "All {} {} elements are not "
            "a IfcFacetedBrep representation."
            .format(elemcount, ifc_class)
        )
    if falsecount > 0:
        assert False, (
            "The following {} of {} {} elements are not  "
            "a IfcFacetedBrep representation: {}"
            .format(falsecount, elemcount, ifc_class, context.falseelems)
        )


@step("all {ifc_class} elements have an {aproperty} property in the {pset} pset")
def step_impl(context, ifc_class, aproperty, pset):

    context.falseelems = []
    context.falseguids = []
    context.falseprops = {}
    from ifcopenshell.util.element import get_psets

    elements = IfcFile.get().by_type(ifc_class)
    elemcount = len(elements)
    for elem in elements:
        psets = get_psets(elem)
        if not (pset in psets and aproperty in psets[pset]):
            context.falseelems.append(str(elem))
            context.falseguids.append(elem.GlobalId)
        context.falseprops[elem.id()] = str(psets)

    falsecount = len(context.falseelems)
    if elemcount == 0:
        assert False, (
            "There are no {} elements in the IFC file."
            .format(ifc_class)
        )
    if falsecount == elemcount:
        assert False, (
            "All {} {} elements are missing "
            "the property {} in the pset {}."
            .format(elemcount, ifc_class, aproperty, pset)
        )
    if falsecount > 0:
        assert False, (
            "The following {} of {} {} elements are missing  "
            "the property {} in the pset {}: {}"
            .format(
                falsecount,
                elemcount,
                ifc_class,
                aproperty,
                pset,
                context.falseelems
            )
        )

    if len(context.falseelems) > 0:
        assert False, (
            "Some elemets missing the pset or property:\n{}"
            .format(context.falseguids)
        )


use_step_matcher("re")


@step("all (?P<ifc_class>.*) elements have an? (?P<attribute>.*) attribute")
def step_impl(context, ifc_class, attribute):
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if not getattr(element, attribute):
            assert False


@step("all (?P<ifc_class>.*) elements have an? (?P<property_path>.*\..*) property")
def step_impl(context, ifc_class, property_path):
    pset_name, property_name = property_path.split(".")
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if not IfcFile.get_property(element, pset_name, property_name):
            assert False


@step(
    'all (?P<ifc_class>.*) elements have an? (?P<property_path>.*\..*) property value matching the pattern "(?P<pattern>.*)"'
)
def step_impl(context, ifc_class, property_path, pattern):
    import re

    pset_name, property_name = property_path.split(".")
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        prop = IfcFile.get_property(element, pset_name, property_name)
        if not prop:
            assert False
        # For now, we only check single values
        if prop.is_a("IfcPropertySingleValue"):
            if not (prop.NominalValue and re.search(pattern, prop.NominalValue.wrappedValue)):
                assert False


@step('all (?P<ifc_class>.*) elements have an? (?P<attribute>.*) matching the pattern "(?P<pattern>.*)"')
def step_impl(context, ifc_class, attribute, pattern):
    import re

    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        value = getattr(element, attribute)
        print(f'Checking value "{value}" for {element}')
        assert re.search(pattern, value)


@step('all (?P<ifc_class>.*) elements have an? (?P<attributes>.*) taken from the list in "(?P<list_file>.*)"')
def step_impl(context, ifc_class, attributes, list_file):
    import csv

    values = []
    with open(list_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            values.append(row)
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        attribute_values = []
        for attribute in attributes.split(","):
            if not hasattr(element, attribute):
                assert False, f"Failed at element {element.GlobalId}"
            attribute_values.append(getattr(element, attribute))
        if attribute_values not in values:
            assert False, f"Failed at element {element.GlobalId}"


use_step_matcher("parse")


@step("all {ifc_class} elements have a {qto_name}.{quantity_name} quantity")
def step_impl(context, ifc_class, qto_name, quantity_name):
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        is_successful = False
        if not element.IsDefinedBy:
            assert False
        for relationship in element.IsDefinedBy:
            if relationship.RelatingPropertyDefinition.Name == qto_name:
                for quantity in relationship.RelatingPropertyDefinition.Quantities:
                    if quantity.Name == quantity_name:
                        is_successful = True
        if not is_successful:
            assert False


use_step_matcher("parse")


@step('the project has a {attribute_name} attribute with a value of "{attribute_value}"')
def step_impl(context, attribute_name, attribute_value):
    project = IfcFile.get().by_type("IfcProject")[0]
    assert getattr(project, attribute_name) == attribute_value


@step('there is an {ifc_class} element with a {attribute_name} attribute with a value of "{attribute_value}"')
def step_impl(context, ifc_class, attribute_name, attribute_value):
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if hasattr(element, attribute_name) and getattr(element, attribute_name) == attribute_value:
            return
    assert False


@step("all buildings have an address")
def step_impl(context):
    for building in IfcFile.get().by_type("IfcBuilding"):
        if not building.BuildingAddress:
            assert False, f'The building "{building.Name}" has no address.'

from behave import step
from utils import IfcFile

from freecad.bimtester.tools_bimtester import get_logfile_path
mylog = get_logfile_path()

@step(u'there are no {ifc_class} elements because {reason}')
def step_impl(context, ifc_class, reason):
    assert len(IfcFile.get().by_type(ifc_class)) == 0


@step('all {ifc_class} elements have a name matching the pattern "{pattern}"')
def step_impl(context, ifc_class, pattern):
    import re
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if not re.search(pattern, element.Name):
            assert False


@step('all {ifc_class} elements have an {representation_class} representation')
def step_impl(context, ifc_class, representation_class):
    logfile = open(mylog, "a")
    logfile.write("representation test\n")
    def is_item_a_representation(item, representation):
        if '/' in representation:
            for cls in representation.split('/'):
                logfile.write("{}\n".format(cls))
                if item.is_a(cls):
                    return True
        elif item.is_a(representation):
            logfile.write("{}\n".format(item))
            return True

    elements = IfcFile.get().by_type(ifc_class)
    false_elements = {}
    for element in elements:
        logfile.write("{}\n".format(element))
        if not element.Representation:
            logfile.write("    continue{}\n")
            continue
        has_representation = False
        for representation in element.Representation.Representations:
            for item in representation.Items:
                logfile.write("    {}\n".format(item))
                if item.is_a('IfcMappedItem'):
                    # We only check one more level deep.
                    for item2 in item.MappingSource.MappedRepresentation.Items:
                        if is_item_a_representation(item2, representation_class):
                            has_representation = True
                else:
                    if is_item_a_representation(item, representation_class):
                        has_representation = True
        if not has_representation:
            false_elements[element.id()] = element.GlobalId
    logfile.write("{}\n".format(sorted(false_elements)))
    logfile.close()
    if len(false_elements) > 0:
        assert False, 'Some elemets are not a IfcFacetedBrep representation: {}'.format(false_elements)


@step('all {ifc_class} elements have an {aproperty} property in the {pset} pset')
def step_impl(context, ifc_class, aproperty, pset):
    # TODO how to redirect prints, See fcbimtester module
    print("It prints :-)")
    # TODO use some switch for me to have prints.
    # I do not need the log file, but it is cool anyway, but overhead?
    logfile = open(mylog, "a")
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
        assert False, 'Some elemets missing the pset or property: {}, {}'.format(false_elements_id, false_elements_guid)
        # siehe UUID is a IfcSpace test, dort AssertionFals mit smarter ausgabe aus utils module

    # Wenn ein test in einem scenario fehl schlaegt und der gleiche test nochmal kommt
    # dann kommt gelb im report "This requirement has not yet been specified."
    # normal sollten diese aber auch noch ablaufen.
    # schoen auch zu sehen an The element {uuid} is an {ifc_class}
    # der erste schlaegt fehl, der zweite "This requirement has not yet been specified."
    # https://community.osarch.org/discussion/comment/3328/#Comment_3328


# all building elements have an {aproperty} property in the {pset} pset')
# aber dann ambigous problem
@step('all parts have an {attribute} attribute in the {myattributesum} attributeset')
def step_impl(context, attribute, myattributesum):
    # TODO how to redirect prints !!!
    logfile = open(mylog, "a")
    logfile.write("PropTest: {}, {}\n".format(attribute, myattributesum))
    elements = IfcFile.get().by_type("IfcBuildingElement")
    false_elements_id = []
    false_elements_guid = []
    from ifcopenshell.util.element import get_psets
    for element in elements:
        psets = get_psets(element)
        if not (myattributesum in psets and attribute in psets[myattributesum]):
            false_elements_id.append(element.id())
            false_elements_guid.append(element.GlobalId)
        logfile.write("{} --> {}\n".format(element.id(), psets))
    logfile.write("{}\n".format(sorted(false_elements_id)))
    logfile.close()
    if len(false_elements_id) > 0:
        from freecad.bimtester.tools_bimtester import create_zoom_smartview
        create_zoom_smartview(false_elements_guid)
        assert False, 'Some elemets missing the pset or property: {}, {}'.format(false_elements_id, false_elements_guid)


use_step_matcher('re')
@step('all (?P<ifc_class>.*) elements have an? (?P<attribute>.*) attribute')
def step_impl(context, ifc_class, attribute):
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if not getattr(element, attribute):
            assert False


@step('all (?P<ifc_class>.*) elements have an? (?P<property_path>.*\..*) property value matching the pattern "(?P<pattern>.*)"')
def step_impl(context, ifc_class, property_path, pattern):
    import re
    pset_name, property_name = property_path.split('.')
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        prop = IfcFile.get_property(element, pset_name, property_name)
        if not prop:
            assert False
        # For now, we only check single values
        if prop.is_a('IfcPropertySingleValue'):
            if not (prop.NominalValue \
                    and re.search(pattern, prop.NominalValue.wrappedValue)):
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
        for attribute in attributes.split(','):
            if not hasattr(element, attribute):
                assert False, f'Failed at element {element.GlobalId}'
            attribute_values.append(getattr(element, attribute))
        if attribute_values not in values:
            assert False, f'Failed at element {element.GlobalId}'


use_step_matcher('parse')
@step('all {ifc_class} elements have a {qto_name}.{quantity_name} quantity')
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


use_step_matcher('parse')
@step(u'the project has a {attribute_name} attribute with a value of "{attribute_value}"')
def step_impl(context, attribute_name, attribute_value):
    project = IfcFile.get().by_type('IfcProject')[0]
    assert getattr(project, attribute_name) == attribute_value


@step(u'there is an {ifc_class} element with a {attribute_name} attribute with a value of "{attribute_value}"')
def step_impl(context, ifc_class, attribute_name, attribute_value):
    elements = IfcFile.get().by_type(ifc_class)
    for element in elements:
        if hasattr(element, attribute_name) \
                and getattr(element, attribute_name) == attribute_value:
            return
    assert False


@step(u'all buildings have an address')
def step_impl(context):
    for building in IfcFile.get().by_type('IfcBuilding'):
        if not building.BuildingAddress:
            assert False, f'The building "{building.Name}" has no address.'

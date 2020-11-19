from behave import step
from utils import IfcFile


# these modules will be copied to tmp and run from there
# print("hehe {} hehe".format(__file__))
from helpertools import get_logfile_path
mylog = get_logfile_path()


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
        from helpertools import create_zoom_smartview
        # create_zoom_smartview(false_elements_guid)
        assert False, 'Some elemets missing the pset or property: {}, {}'.format(false_elements_id, false_elements_guid)

from behave import step

from utils import assert_elements


@step("Alle {ifc_class} Bauteile müssen geometrische Repräsentationen ohne Fehler haben")
def step_impl(context, ifc_class):

    try:
        context.execute_steps(
            "* all {aifc_class} elements must have a geometric representation without errors"
            .format(aifc_class=ifc_class)
        )
    except Exception:
        assert_elements(
            ifc_class,
            context.elemcount,
            context.falsecount,
            context.falseelems
        )

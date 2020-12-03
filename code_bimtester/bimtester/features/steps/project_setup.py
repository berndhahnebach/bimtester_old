from behave import step

from utils import assert_attribute
from utils import IfcFile


@step('The IFC file "{file}" must be provided')
def step_impl(context, file):
    try:
        IfcFile.load(file)
    except:
        assert False, f"The file {file} could not be loaded"


@step("IFC data must use the {schema} schema")
def step_impl(context, schema):
    assert IfcFile.get().schema == schema, "We expected a schema of {} but instead got {}".format(
        schema, IfcFile.get().schema
    )


@step("IFC data must have a header file description of {header_file_description} such as the new Allplan IFC exporter creates it")
def step_impl(context, header_file_description):
    
    is_header_file_description = IfcFile.get().wrapped_data.header.file_description.description
    assert  str(is_header_file_description) == header_file_description , (
        "The file was not exported by the new ifc exporter in Allplan. File description header: {}"
        .format(is_header_file_description)
    )


@step("IFC data must be exported by application identifier {identifier}")
def step_impl(context, identifier):

    software_id = IfcFile.get().by_type("IfcApplication")[0].ApplicationIdentifier
    assert  software_id == identifier , (
        "The IFC file was not exported by application identifier {} "
        "instead it was exported by identifier {}"
        .format(software_id, identifier)
    )


@step("IFC data must be exported by the application version {version}")
def step_impl(context, version):

    software_version = IfcFile.get().by_type("IfcApplication")[0].Version
    assert  software_version == version , (
        "The IFC file was not exported by application version {} "
        "instead it was exported by version {}"
        .format(version, software_version)
    )


@step('The IFC file "{file}" is exempt from being provided')
def step_impl(context, file):
    pass


@step("No further requirements are specified because {reason}")
def step_impl(context, reason):
    pass


@step("The project must have an identifier of {guid}")
def step_impl(context, guid):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "GlobalId", guid)


@step('The project name, code, or short identifier must be "{value}"')
def step_impl(context, value):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "Name", value)


@step('The project must have a longer form name of "{value}"')
def step_impl(context, value):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "LongName", value)


@step('The project must be described as "{value}"')
def step_impl(context, value):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "Description", value)


@step('The project must be categorised under "{value}"')
def step_impl(context, value):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "ObjectType", value)


@step('The project must contain information about the "{value}" phase')
def step_impl(context, value):
    assert_attribute(IfcFile.get().by_type("IfcProject")[0], "Phase", value)


@step("The project must contain 3D geometry representing the shape of objects")
def step_impl(context):
    assert get_subcontext("Body", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing clearance zones")
def step_impl(context):
    assert get_subcontext("Clearance", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing the center of gravity of objects")
def step_impl(context):
    assert get_subcontext("CoG", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing the object bounding boxes")
def step_impl(context):
    assert get_subcontext("Box", "Model", "MODEL_VIEW")


def get_subcontext(identifier, type, target_view):
    project = IfcFile.get().by_type("IfcProject")[0]
    for rep_context in project.RepresentationContexts:
        for subcontext in rep_context.HasSubContexts:
            if (
                subcontext.ContextIdentifier == identifier
                and subcontext.ContextType == type
                and subcontext.TargetView == target_view
            ):
                return True
    assert False, "The subcontext with identifier {}, type {}, and target view {} could not be found".format(
        identifier, type, target_view
    )

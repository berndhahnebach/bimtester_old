from behave.model import Scenario


def before_all(context):
    userdata = context.config.userdata
    continue_after_failed = True
    Scenario.continue_after_failed_step = continue_after_failed

    # test befora_all ...
    mytestlogfile = open("/tmp/zztest", "w")
    mytestlogfile.write("myenvironmenttest")
    mytestlogfile.close()


"""
somehow the environmental seam ignored at all ...
see code about the mytestlogfile
https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
def before_step(context, step):
    print(step.name)


def before_all(context):
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini".
    context.config.setup_logging()


def after_step(context, step):
    if step.status == "failed":
        # take_the_shot(context.scenario.name + " " + step.name)
        print("BERND")
"""

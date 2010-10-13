import logging

def from_2_x_to_3_0(context):

    # run the new import step (1 -> 2)
    context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','upgrade_2_to_3')

    # log it
    log = logging.getLogger("FacultyStaffDirectory")
    log.info("Upgraded version 2 to version 3")

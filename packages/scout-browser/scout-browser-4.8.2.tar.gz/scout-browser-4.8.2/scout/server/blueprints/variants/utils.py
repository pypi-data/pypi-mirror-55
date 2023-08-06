import logging

LOG = logging.getLogger(__name__)


def get_clinical_panels(panels, hpo):
    """Create a list of what panels that should be included in the filter
    
    Args:
        panels(list(dict)): A list of gene panels in the case obj format
        hpo(bool): If the hpo panel should be included
    
    Returns:
        clinical_filter_panels(list(str)): list of panel names
    """
    clinical_filter_panels = []

    default_panels = []
    for panel in panels:
        if panel.get('is_default'):
            default_panels.append(panel['panel_name'])

    if case_obj.get('hpo_clinical_filter'):
        clinical_filter_panels = ['hpo']
    else:
        clinical_filter_panels = default_panels

    LOG.debug("Current default panels: {}".format(default_panels))
    


def build_variants_filter(case_obj, clinical_filter=False, hpo_clinical_filter=False, post=False):
    """Use the information from a request ti build a clinical filter
    
    Args:
        case_obj(scout.models.Case)
        clinical_filter(bool): If the predefined clinical filter should be built
        hpo_clinical_filter
        post(bool): If a post request has been used or not
    
    """
    clinical_panels = get_clinical_panels(case_obj.get('panels', []), hpo_clinical_filter)
    # Update filter settings if Clinical Filter was requested
    
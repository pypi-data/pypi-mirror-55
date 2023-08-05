# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GraphModuleNode(Model):
    """GraphModuleNode.

    :param id:
    :type id: str
    :param module_id:
    :type module_id: str
    :param module_type: Possible values include: 'None', 'BatchInferencing'
    :type module_type: str or ~swagger.models.enum
    :param comment:
    :type comment: str
    :param module_parameters:
    :type module_parameters: list[~swagger.models.ParameterAssignment]
    :param module_metadata_parameters:
    :type module_metadata_parameters:
     list[~swagger.models.ParameterAssignment]
    :param module_output_settings:
    :type module_output_settings: list[~swagger.models.OutputSetting]
    :param module_input_settings:
    :type module_input_settings: list[~swagger.models.InputSetting]
    :param use_graph_default_compute:
    :type use_graph_default_compute: bool
    :param runconfig:
    :type runconfig: str
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'str'},
        'module_id': {'key': 'ModuleId', 'type': 'str'},
        'module_type': {'key': 'ModuleType', 'type': 'str'},
        'comment': {'key': 'Comment', 'type': 'str'},
        'module_parameters': {'key': 'ModuleParameters', 'type': '[ParameterAssignment]'},
        'module_metadata_parameters': {'key': 'ModuleMetadataParameters', 'type': '[ParameterAssignment]'},
        'module_output_settings': {'key': 'ModuleOutputSettings', 'type': '[OutputSetting]'},
        'module_input_settings': {'key': 'ModuleInputSettings', 'type': '[InputSetting]'},
        'use_graph_default_compute': {'key': 'UseGraphDefaultCompute', 'type': 'bool'},
        'runconfig': {'key': 'Runconfig', 'type': 'str'},
    }

    def __init__(self, id=None, module_id=None, module_type=None, comment=None, module_parameters=None, module_metadata_parameters=None, module_output_settings=None, module_input_settings=None, use_graph_default_compute=None, runconfig=None):
        super(GraphModuleNode, self).__init__()
        self.id = id
        self.module_id = module_id
        self.module_type = module_type
        self.comment = comment
        self.module_parameters = module_parameters
        self.module_metadata_parameters = module_metadata_parameters
        self.module_output_settings = module_output_settings
        self.module_input_settings = module_input_settings
        self.use_graph_default_compute = use_graph_default_compute
        self.runconfig = runconfig

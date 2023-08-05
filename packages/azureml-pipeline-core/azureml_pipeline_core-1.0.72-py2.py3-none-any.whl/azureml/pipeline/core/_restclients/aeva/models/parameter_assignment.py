# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ParameterAssignment(Model):
    """ParameterAssignment.

    :param value_type: Possible values include: 'Literal',
     'GraphParameterName', 'Concatenate', 'Input'
    :type value_type: str or ~swagger.models.enum
    :param assignments_to_concatenate:
    :type assignments_to_concatenate:
     list[~swagger.models.ParameterAssignment]
    :param name:
    :type name: str
    :param value:
    :type value: str
    """

    _attribute_map = {
        'value_type': {'key': 'ValueType', 'type': 'str'},
        'assignments_to_concatenate': {'key': 'AssignmentsToConcatenate', 'type': '[ParameterAssignment]'},
        'name': {'key': 'Name', 'type': 'str'},
        'value': {'key': 'Value', 'type': 'str'},
    }

    def __init__(self, value_type=None, assignments_to_concatenate=None, name=None, value=None):
        super(ParameterAssignment, self).__init__()
        self.value_type = value_type
        self.assignments_to_concatenate = assignments_to_concatenate
        self.name = name
        self.value = value

# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ModuleCreationInfo(Model):
    """ModuleCreationInfo.

    :param name:
    :type name: str
    :param hash:
    :type hash: str
    :param description:
    :type description: str
    :param is_deterministic:
    :type is_deterministic: bool
    :param module_execution_type:
    :type module_execution_type: str
    :param identifier_hash:
    :type identifier_hash: str
    :param structured_interface:
    :type structured_interface: ~swagger.models.StructuredInterface
    :param storage_id:
    :type storage_id: str
    :param is_interface_only:
    :type is_interface_only: bool
    :param properties:
    :type properties: dict
    :param module_type:
    :type module_type: str
    :param category:
    :type category: str
    """

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str'},
        'hash': {'key': 'Hash', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'is_deterministic': {'key': 'IsDeterministic', 'type': 'bool'},
        'module_execution_type': {'key': 'ModuleExecutionType', 'type': 'str'},
        'identifier_hash': {'key': 'IdentifierHash', 'type': 'str'},
        'structured_interface': {'key': 'StructuredInterface', 'type': 'StructuredInterface'},
        'storage_id': {'key': 'StorageId', 'type': 'str'},
        'is_interface_only': {'key': 'IsInterfaceOnly', 'type': 'bool'},
        'properties': {'key': 'Properties', 'type': '{object}'},
        'module_type': {'key': 'ModuleType', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
    }

    def __init__(self, name=None, hash=None, description=None, is_deterministic=None, module_execution_type=None,
                 identifier_hash=None, structured_interface=None, storage_id=None, is_interface_only=None,
                 properties=None, module_type=None, category=None):
        super(ModuleCreationInfo, self).__init__()
        self.name = name
        self.hash = hash
        self.description = description
        self.is_deterministic = is_deterministic
        self.module_execution_type = module_execution_type
        self.identifier_hash = identifier_hash
        self.structured_interface = structured_interface
        self.storage_id = storage_id
        self.is_interface_only = is_interface_only
        self.properties = properties
        self.module_type = module_type
        self.category = category

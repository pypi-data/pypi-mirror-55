# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PortInfo(Model):
    """PortInfo.

    :param node_id:
    :type node_id: str
    :param port_name:
    :type port_name: str
    :param graph_port_name:
    :type graph_port_name: str
    """

    _attribute_map = {
        'node_id': {'key': 'NodeId', 'type': 'str'},
        'port_name': {'key': 'PortName', 'type': 'str'},
        'graph_port_name': {'key': 'GraphPortName', 'type': 'str'}
    }

    def __init__(self, node_id=None, port_name=None, graph_port_name=None):
        super(PortInfo, self).__init__()
        self.node_id = node_id
        self.port_name = port_name
        self.graph_port_name = graph_port_name

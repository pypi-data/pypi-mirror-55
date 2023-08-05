# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AzureMySql(Model):
    """AzureMySql.

    :param server_name: The Azure MySQL server name
    :type server_name: str
    :param database_name: The Azure MySQL database name
    :type database_name: str
    :param user_id: The Azure MySQL user id
    :type user_id: str
    :param user_password: The Azure MySQL user password
    :type user_password: str
    :param port_number: The Azure MySQL port number
    :type port_number: str
    :param endpoint: The Azure MySQL server host endpoint
    :type endpoint: str
    :param subscription_id: Subscription Id
    :type subscription_id: str
    :param resource_group: Resource Group Name
    :type resource_group: str
    """

    _attribute_map = {
        'server_name': {'key': 'serverName', 'type': 'str'},
        'database_name': {'key': 'databaseName', 'type': 'str'},
        'user_id': {'key': 'userId', 'type': 'str'},
        'user_password': {'key': 'userPassword', 'type': 'str'},
        'port_number': {'key': 'portNumber', 'type': 'str'},
        'endpoint': {'key': 'endpoint', 'type': 'str'},
        'subscription_id': {'key': 'subscriptionId', 'type': 'str'},
        'resource_group': {'key': 'resourceGroup', 'type': 'str'},
    }

    def __init__(self, server_name=None, database_name=None, user_id=None, user_password=None, port_number=None, endpoint=None, subscription_id=None, resource_group=None):
        super(AzureMySql, self).__init__()
        self.server_name = server_name
        self.database_name = database_name
        self.user_id = user_id
        self.user_password = user_password
        self.port_number = port_number
        self.endpoint = endpoint
        self.subscription_id = subscription_id
        self.resource_group = resource_group

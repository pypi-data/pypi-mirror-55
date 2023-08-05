# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 1.0.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UpdateDataDriftDto(Model):
    """UpdateDataDriftDto.

    :param services:
    :type services: list[str]
    :param compute_target_name:
    :type compute_target_name: str
    :param features:
    :type features: list[str]
    :param drift_threshold:
    :type drift_threshold: float
    :param alert_configuration:
    :type alert_configuration: ~_restclient.models.AlertConfiguration
    :param state: Possible values include: 'Disabled', 'Enabled', 'Disabling',
     'Enabling'
    :type state: str or ~_restclient.models.enum
    """

    _attribute_map = {
        'services': {'key': 'services', 'type': '[str]'},
        'compute_target_name': {'key': 'computeTargetName', 'type': 'str'},
        'features': {'key': 'features', 'type': '[str]'},
        'drift_threshold': {'key': 'driftThreshold', 'type': 'float'},
        'alert_configuration': {'key': 'alertConfiguration', 'type': 'AlertConfiguration'},
        'state': {'key': 'state', 'type': 'str'},
    }

    def __init__(self, *, services=None, compute_target_name: str=None, features=None, drift_threshold: float=None, alert_configuration=None, state=None, **kwargs) -> None:
        super(UpdateDataDriftDto, self).__init__(**kwargs)
        self.services = services
        self.compute_target_name = compute_target_name
        self.features = features
        self.drift_threshold = drift_threshold
        self.alert_configuration = alert_configuration
        self.state = state

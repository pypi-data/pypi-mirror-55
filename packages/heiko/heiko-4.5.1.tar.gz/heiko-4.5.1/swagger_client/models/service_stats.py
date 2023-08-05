# coding: utf-8

"""
    MaaS

    MaaS (Matomat as a Service) API definition  # noqa: E501

    OpenAPI spec version: 0.5.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.models.service_stats_items import ServiceStatsItems  # noqa: F401,E501
from swagger_client.models.service_stats_users import ServiceStatsUsers  # noqa: F401,E501


class ServiceStats(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'items': 'ServiceStatsItems',
        'users': 'ServiceStatsUsers'
    }

    attribute_map = {
        'items': 'items',
        'users': 'users'
    }

    def __init__(self, items=None, users=None):  # noqa: E501
        """ServiceStats - a model defined in Swagger"""  # noqa: E501

        self._items = None
        self._users = None
        self.discriminator = None

        if items is not None:
            self.items = items
        if users is not None:
            self.users = users

    @property
    def items(self):
        """Gets the items of this ServiceStats.  # noqa: E501


        :return: The items of this ServiceStats.  # noqa: E501
        :rtype: ServiceStatsItems
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this ServiceStats.


        :param items: The items of this ServiceStats.  # noqa: E501
        :type: ServiceStatsItems
        """

        self._items = items

    @property
    def users(self):
        """Gets the users of this ServiceStats.  # noqa: E501


        :return: The users of this ServiceStats.  # noqa: E501
        :rtype: ServiceStatsUsers
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this ServiceStats.


        :param users: The users of this ServiceStats.  # noqa: E501
        :type: ServiceStatsUsers
        """

        self._users = users

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ServiceStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

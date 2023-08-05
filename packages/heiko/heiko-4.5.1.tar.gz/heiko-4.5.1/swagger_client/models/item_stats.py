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


class ItemStats(object):
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
        'id': 'int',
        'name': 'str',
        'cost': 'int',
        'consumed': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'cost': 'cost',
        'consumed': 'consumed'
    }

    def __init__(self, id=None, name=None, cost=None, consumed=None):  # noqa: E501
        """ItemStats - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._name = None
        self._cost = None
        self._consumed = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if cost is not None:
            self.cost = cost
        if consumed is not None:
            self.consumed = consumed

    @property
    def id(self):
        """Gets the id of this ItemStats.  # noqa: E501


        :return: The id of this ItemStats.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ItemStats.


        :param id: The id of this ItemStats.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ItemStats.  # noqa: E501


        :return: The name of this ItemStats.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ItemStats.


        :param name: The name of this ItemStats.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cost(self):
        """Gets the cost of this ItemStats.  # noqa: E501


        :return: The cost of this ItemStats.  # noqa: E501
        :rtype: int
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this ItemStats.


        :param cost: The cost of this ItemStats.  # noqa: E501
        :type: int
        """

        self._cost = cost

    @property
    def consumed(self):
        """Gets the consumed of this ItemStats.  # noqa: E501


        :return: The consumed of this ItemStats.  # noqa: E501
        :rtype: int
        """
        return self._consumed

    @consumed.setter
    def consumed(self, consumed):
        """Sets the consumed of this ItemStats.


        :param consumed: The consumed of this ItemStats.  # noqa: E501
        :type: int
        """

        self._consumed = consumed

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
        if not isinstance(other, ItemStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

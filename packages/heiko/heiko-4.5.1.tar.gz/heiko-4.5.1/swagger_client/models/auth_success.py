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

from swagger_client.models.user import User  # noqa: F401,E501


class AuthSuccess(object):
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
        'token': 'str',
        'expires': 'int',
        'user': 'User'
    }

    attribute_map = {
        'token': 'token',
        'expires': 'expires',
        'user': 'user'
    }

    def __init__(self, token=None, expires=None, user=None):  # noqa: E501
        """AuthSuccess - a model defined in Swagger"""  # noqa: E501

        self._token = None
        self._expires = None
        self._user = None
        self.discriminator = None

        if token is not None:
            self.token = token
        if expires is not None:
            self.expires = expires
        if user is not None:
            self.user = user

    @property
    def token(self):
        """Gets the token of this AuthSuccess.  # noqa: E501


        :return: The token of this AuthSuccess.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this AuthSuccess.


        :param token: The token of this AuthSuccess.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def expires(self):
        """Gets the expires of this AuthSuccess.  # noqa: E501


        :return: The expires of this AuthSuccess.  # noqa: E501
        :rtype: int
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """Sets the expires of this AuthSuccess.


        :param expires: The expires of this AuthSuccess.  # noqa: E501
        :type: int
        """

        self._expires = expires

    @property
    def user(self):
        """Gets the user of this AuthSuccess.  # noqa: E501


        :return: The user of this AuthSuccess.  # noqa: E501
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this AuthSuccess.


        :param user: The user of this AuthSuccess.  # noqa: E501
        :type: User
        """

        self._user = user

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
        if not isinstance(other, AuthSuccess):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

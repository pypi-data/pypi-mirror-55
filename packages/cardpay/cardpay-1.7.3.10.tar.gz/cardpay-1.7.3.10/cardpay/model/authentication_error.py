# coding: utf-8

"""
    CardPay REST API

    Welcome to the CardPay REST API. The CardPay API uses HTTP verbs and a [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) resources endpoint structure (see more info about REST). Request and response payloads are formatted as JSON. Merchant uses API to create payments, refunds, payouts or recurrings, check or update transaction status and get information about created transactions. In API authentication process based on [OAuth 2.0](https://oauth.net/2/) standard. For recent changes see changelog section.  # noqa: E501

    OpenAPI spec version: 3.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class AuthenticationError(object):
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
    swagger_types = {"message": "str", "name": "str"}

    attribute_map = {"message": "message", "name": "name"}

    def __init__(self, message=None, name=None):  # noqa: E501
        """AuthenticationError - a model defined in Swagger"""  # noqa: E501

        self._message = None
        self._name = None
        self.discriminator = None

        self.message = message
        self.name = name

    @property
    def message(self):
        """Gets the message of this AuthenticationError.  # noqa: E501

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :return: The message of this AuthenticationError.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this AuthenticationError.

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :param message: The message of this AuthenticationError.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError(
                "Invalid value for `message`, must not be `None`"
            )  # noqa: E501

        self._message = message

    @property
    def name(self):
        """Gets the name of this AuthenticationError.  # noqa: E501

        A short, human-readable summary of the problem that *should not* change from occurrence to occurrence of the problem, except for purposes of localization.  # noqa: E501

        :return: The name of this AuthenticationError.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AuthenticationError.

        A short, human-readable summary of the problem that *should not* change from occurrence to occurrence of the problem, except for purposes of localization.  # noqa: E501

        :param name: The name of this AuthenticationError.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                if value is not None:
                    result[attr] = value
        if issubclass(AuthenticationError, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AuthenticationError):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

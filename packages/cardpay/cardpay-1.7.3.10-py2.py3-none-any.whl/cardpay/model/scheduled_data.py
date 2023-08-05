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

from cardpay.model.plan import Plan  # noqa: F401,E501


class ScheduledData(object):
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
        "dynamic_descriptor": "str",
        "generate_token": "bool",
        "initial_amount": "float",
        "initiator": "str",
        "note": "str",
        "plan": "Plan",
        "subscription_start": "datetime",
        "trans_type": "str",
    }

    attribute_map = {
        "dynamic_descriptor": "dynamic_descriptor",
        "generate_token": "generate_token",
        "initial_amount": "initial_amount",
        "initiator": "initiator",
        "note": "note",
        "plan": "plan",
        "subscription_start": "subscription_start",
        "trans_type": "trans_type",
    }

    def __init__(
        self,
        dynamic_descriptor=None,
        generate_token=None,
        initial_amount=None,
        initiator=None,
        note=None,
        plan=None,
        subscription_start=None,
        trans_type=None,
    ):  # noqa: E501
        """ScheduledData - a model defined in Swagger"""  # noqa: E501

        self._dynamic_descriptor = None
        self._generate_token = None
        self._initial_amount = None
        self._initiator = None
        self._note = None
        self._plan = None
        self._subscription_start = None
        self._trans_type = None
        self.discriminator = None

        if dynamic_descriptor is not None:
            self.dynamic_descriptor = dynamic_descriptor
        if generate_token is not None:
            self.generate_token = generate_token
        if initial_amount is not None:
            self.initial_amount = initial_amount
        self.initiator = initiator
        if note is not None:
            self.note = note
        if plan is not None:
            self.plan = plan
        if subscription_start is not None:
            self.subscription_start = subscription_start
        if trans_type is not None:
            self.trans_type = trans_type

    @property
    def dynamic_descriptor(self):
        """Gets the dynamic_descriptor of this ScheduledData.  # noqa: E501

        Short description of the service or product, must be enabled by CardPay manager to be used.  # noqa: E501

        :return: The dynamic_descriptor of this ScheduledData.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_descriptor

    @dynamic_descriptor.setter
    def dynamic_descriptor(self, dynamic_descriptor):
        """Sets the dynamic_descriptor of this ScheduledData.

        Short description of the service or product, must be enabled by CardPay manager to be used.  # noqa: E501

        :param dynamic_descriptor: The dynamic_descriptor of this ScheduledData.  # noqa: E501
        :type: str
        """
        if dynamic_descriptor is not None and len(dynamic_descriptor) > 25:
            raise ValueError(
                "Invalid value for `dynamic_descriptor`, length must be less than or equal to `25`"
            )  # noqa: E501
        if dynamic_descriptor is not None and len(dynamic_descriptor) < 0:
            raise ValueError(
                "Invalid value for `dynamic_descriptor`, length must be greater than or equal to `0`"
            )  # noqa: E501

        self._dynamic_descriptor = dynamic_descriptor

    @property
    def generate_token(self):
        """Gets the generate_token of this ScheduledData.  # noqa: E501

        This attribute can be received only in first recurring request. In all requests with recurring_id card.token can't be generated. If set to 'true', Card token will be generated and returned in GET response. Will be generated only for successful transactions (not for declined).  # noqa: E501

        :return: The generate_token of this ScheduledData.  # noqa: E501
        :rtype: bool
        """
        return self._generate_token

    @generate_token.setter
    def generate_token(self, generate_token):
        """Sets the generate_token of this ScheduledData.

        This attribute can be received only in first recurring request. In all requests with recurring_id card.token can't be generated. If set to 'true', Card token will be generated and returned in GET response. Will be generated only for successful transactions (not for declined).  # noqa: E501

        :param generate_token: The generate_token of this ScheduledData.  # noqa: E501
        :type: bool
        """

        self._generate_token = generate_token

    @property
    def initial_amount(self):
        """Gets the initial_amount of this ScheduledData.  # noqa: E501

        The amount of subscription initiated transaction in selected currency with dot as a decimal separator, must be less than 100 millions  # noqa: E501

        :return: The initial_amount of this ScheduledData.  # noqa: E501
        :rtype: float
        """
        return self._initial_amount

    @initial_amount.setter
    def initial_amount(self, initial_amount):
        """Sets the initial_amount of this ScheduledData.

        The amount of subscription initiated transaction in selected currency with dot as a decimal separator, must be less than 100 millions  # noqa: E501

        :param initial_amount: The initial_amount of this ScheduledData.  # noqa: E501
        :type: float
        """

        self._initial_amount = initial_amount

    @property
    def initiator(self):
        """Gets the initiator of this ScheduledData.  # noqa: E501

        Use `cit` for initiator attribute (cardholder initiated transaction).  # noqa: E501

        :return: The initiator of this ScheduledData.  # noqa: E501
        :rtype: str
        """
        return self._initiator

    @initiator.setter
    def initiator(self, initiator):
        """Sets the initiator of this ScheduledData.

        Use `cit` for initiator attribute (cardholder initiated transaction).  # noqa: E501

        :param initiator: The initiator of this ScheduledData.  # noqa: E501
        :type: str
        """
        if initiator is None:
            raise ValueError(
                "Invalid value for `initiator`, must not be `None`"
            )  # noqa: E501
        if initiator is not None and not re.search(r"mit|cit", initiator):  # noqa: E501
            raise ValueError(
                r"Invalid value for `initiator`, must be a follow pattern or equal to `/mit|cit/`"
            )  # noqa: E501

        self._initiator = initiator

    @property
    def note(self):
        """Gets the note of this ScheduledData.  # noqa: E501

        Note about the recurring that will not be displayed to customer.  # noqa: E501

        :return: The note of this ScheduledData.  # noqa: E501
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this ScheduledData.

        Note about the recurring that will not be displayed to customer.  # noqa: E501

        :param note: The note of this ScheduledData.  # noqa: E501
        :type: str
        """
        if note is not None and len(note) > 100:
            raise ValueError(
                "Invalid value for `note`, length must be less than or equal to `100`"
            )  # noqa: E501
        if note is not None and len(note) < 0:
            raise ValueError(
                "Invalid value for `note`, length must be greater than or equal to `0`"
            )  # noqa: E501

        self._note = note

    @property
    def plan(self):
        """Gets the plan of this ScheduledData.  # noqa: E501

        Plan data  # noqa: E501

        :return: The plan of this ScheduledData.  # noqa: E501
        :rtype: Plan
        """
        return self._plan

    @plan.setter
    def plan(self, plan):
        """Sets the plan of this ScheduledData.

        Plan data  # noqa: E501

        :param plan: The plan of this ScheduledData.  # noqa: E501
        :type: Plan
        """

        self._plan = plan

    @property
    def subscription_start(self):
        """Gets the subscription_start of this ScheduledData.  # noqa: E501

        The time in 'yyyy-MM-dd' format when subscription will actually become activated (grace period).Leave it empty to activate subscription at once without any grace period applied.  # noqa: E501

        :return: The subscription_start of this ScheduledData.  # noqa: E501
        :rtype: datetime
        """
        return self._subscription_start

    @subscription_start.setter
    def subscription_start(self, subscription_start):
        """Sets the subscription_start of this ScheduledData.

        The time in 'yyyy-MM-dd' format when subscription will actually become activated (grace period).Leave it empty to activate subscription at once without any grace period applied.  # noqa: E501

        :param subscription_start: The subscription_start of this ScheduledData.  # noqa: E501
        :type: datetime
        """

        self._subscription_start = subscription_start

    class TransType(object):
        _01 = "01"
        _03 = "03"
        _10 = "10"
        _11 = "11"
        _28 = "28"

    @property
    def trans_type(self):
        """Gets the trans_type of this ScheduledData.  # noqa: E501


        :return: The trans_type of this ScheduledData.  # noqa: E501
        :rtype: str
        """
        return self._trans_type

    @trans_type.setter
    def trans_type(self, trans_type):
        """Sets the trans_type of this ScheduledData.


        :param trans_type: The trans_type of this ScheduledData.  # noqa: E501
        :type: str
        """
        allowed_values = ["01", "03", "10", "11", "28"]  # noqa: E501
        if trans_type not in allowed_values:
            raise ValueError(
                "Invalid value for `trans_type` ({0}), must be one of {1}".format(  # noqa: E501
                    trans_type, allowed_values
                )
            )

        self._trans_type = trans_type

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
        if issubclass(ScheduledData, dict):
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
        if not isinstance(other, ScheduledData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

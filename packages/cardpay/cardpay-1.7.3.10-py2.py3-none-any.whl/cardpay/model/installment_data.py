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


class InstallmentData(object):
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
        "amount": "float",
        "currency": "str",
        "dynamic_descriptor": "str",
        "generate_token": "bool",
        "initiator": "str",
        "interval": "int",
        "note": "str",
        "payments": "int",
        "period": "str",
        "retries": "int",
        "subscription_start": "datetime",
        "trans_type": "str",
    }

    attribute_map = {
        "amount": "amount",
        "currency": "currency",
        "dynamic_descriptor": "dynamic_descriptor",
        "generate_token": "generate_token",
        "initiator": "initiator",
        "interval": "interval",
        "note": "note",
        "payments": "payments",
        "period": "period",
        "retries": "retries",
        "subscription_start": "subscription_start",
        "trans_type": "trans_type",
    }

    def __init__(
        self,
        amount=None,
        currency=None,
        dynamic_descriptor=None,
        generate_token=None,
        initiator=None,
        interval=None,
        note=None,
        payments=None,
        period=None,
        retries=None,
        subscription_start=None,
        trans_type=None,
    ):  # noqa: E501
        """InstallmentData - a model defined in Swagger"""  # noqa: E501

        self._amount = None
        self._currency = None
        self._dynamic_descriptor = None
        self._generate_token = None
        self._initiator = None
        self._interval = None
        self._note = None
        self._payments = None
        self._period = None
        self._retries = None
        self._subscription_start = None
        self._trans_type = None
        self.discriminator = None

        if amount is not None:
            self.amount = amount
        self.currency = currency
        if dynamic_descriptor is not None:
            self.dynamic_descriptor = dynamic_descriptor
        if generate_token is not None:
            self.generate_token = generate_token
        self.initiator = initiator
        if interval is not None:
            self.interval = interval
        if note is not None:
            self.note = note
        if payments is not None:
            self.payments = payments
        if period is not None:
            self.period = period
        if retries is not None:
            self.retries = retries
        if subscription_start is not None:
            self.subscription_start = subscription_start
        if trans_type is not None:
            self.trans_type = trans_type

    @property
    def amount(self):
        """Gets the amount of this InstallmentData.  # noqa: E501

        The total transaction amount in selected currency with dot as a decimal separator, must be less than 100 millions  # noqa: E501

        :return: The amount of this InstallmentData.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this InstallmentData.

        The total transaction amount in selected currency with dot as a decimal separator, must be less than 100 millions  # noqa: E501

        :param amount: The amount of this InstallmentData.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def currency(self):
        """Gets the currency of this InstallmentData.  # noqa: E501

        [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency code  # noqa: E501

        :return: The currency of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this InstallmentData.

        [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency code  # noqa: E501

        :param currency: The currency of this InstallmentData.  # noqa: E501
        :type: str
        """
        if currency is None:
            raise ValueError(
                "Invalid value for `currency`, must not be `None`"
            )  # noqa: E501

        self._currency = currency

    @property
    def dynamic_descriptor(self):
        """Gets the dynamic_descriptor of this InstallmentData.  # noqa: E501

        Short description of the service or product, must be enabled by CardPay manager to be used.  # noqa: E501

        :return: The dynamic_descriptor of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_descriptor

    @dynamic_descriptor.setter
    def dynamic_descriptor(self, dynamic_descriptor):
        """Sets the dynamic_descriptor of this InstallmentData.

        Short description of the service or product, must be enabled by CardPay manager to be used.  # noqa: E501

        :param dynamic_descriptor: The dynamic_descriptor of this InstallmentData.  # noqa: E501
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
        """Gets the generate_token of this InstallmentData.  # noqa: E501

        This attribute can be received only in first recurring request. In all requests with recurring_id card.token can't be generated. If set to 'true', Card token will be generated and returned in GET response. Will be generated only for successful transactions (not for declined).  # noqa: E501

        :return: The generate_token of this InstallmentData.  # noqa: E501
        :rtype: bool
        """
        return self._generate_token

    @generate_token.setter
    def generate_token(self, generate_token):
        """Sets the generate_token of this InstallmentData.

        This attribute can be received only in first recurring request. In all requests with recurring_id card.token can't be generated. If set to 'true', Card token will be generated and returned in GET response. Will be generated only for successful transactions (not for declined).  # noqa: E501

        :param generate_token: The generate_token of this InstallmentData.  # noqa: E501
        :type: bool
        """

        self._generate_token = generate_token

    @property
    def initiator(self):
        """Gets the initiator of this InstallmentData.  # noqa: E501

        Use `cit` for initiator attribute (cardholder initiated transaction).  # noqa: E501

        :return: The initiator of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._initiator

    @initiator.setter
    def initiator(self, initiator):
        """Sets the initiator of this InstallmentData.

        Use `cit` for initiator attribute (cardholder initiated transaction).  # noqa: E501

        :param initiator: The initiator of this InstallmentData.  # noqa: E501
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
    def interval(self):
        """Gets the interval of this InstallmentData.  # noqa: E501

        Frequency interval of period, can be 1-365 depending on selected period value. Minimum value of period + interval can be 7 days / 1 week. Maximum value of period + interval plan can be 365 days / 52 weeks / 12 months / 1 year. 1-60 minutes - for **sandbox environment** and testing purpose only.  # noqa: E501

        :return: The interval of this InstallmentData.  # noqa: E501
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this InstallmentData.

        Frequency interval of period, can be 1-365 depending on selected period value. Minimum value of period + interval can be 7 days / 1 week. Maximum value of period + interval plan can be 365 days / 52 weeks / 12 months / 1 year. 1-60 minutes - for **sandbox environment** and testing purpose only.  # noqa: E501

        :param interval: The interval of this InstallmentData.  # noqa: E501
        :type: int
        """
        if interval is not None and interval < 1:  # noqa: E501
            raise ValueError(
                "Invalid value for `interval`, must be a value greater than or equal to `1`"
            )  # noqa: E501

        self._interval = interval

    @property
    def note(self):
        """Gets the note of this InstallmentData.  # noqa: E501

        Note about the recurring that will not be displayed to customer.  # noqa: E501

        :return: The note of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this InstallmentData.

        Note about the recurring that will not be displayed to customer.  # noqa: E501

        :param note: The note of this InstallmentData.  # noqa: E501
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
    def payments(self):
        """Gets the payments of this InstallmentData.  # noqa: E501

        Number of total payments to be charged per defined interval, can be 2-200.  # noqa: E501

        :return: The payments of this InstallmentData.  # noqa: E501
        :rtype: int
        """
        return self._payments

    @payments.setter
    def payments(self, payments):
        """Sets the payments of this InstallmentData.

        Number of total payments to be charged per defined interval, can be 2-200.  # noqa: E501

        :param payments: The payments of this InstallmentData.  # noqa: E501
        :type: int
        """
        if payments is not None and payments > 200:  # noqa: E501
            raise ValueError(
                "Invalid value for `payments`, must be a value less than or equal to `200`"
            )  # noqa: E501
        if payments is not None and payments < 2:  # noqa: E501
            raise ValueError(
                "Invalid value for `payments`, must be a value greater than or equal to `2`"
            )  # noqa: E501

        self._payments = payments

    class Period(object):
        MINUTE = "minute"
        DAY = "day"
        WEEK = "week"
        MONTH = "month"
        YEAR = "year"

    @property
    def period(self):
        """Gets the period of this InstallmentData.  # noqa: E501

        Initial period of recurring, can be `day`, `week`, `month`, `year`  # noqa: E501

        :return: The period of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this InstallmentData.

        Initial period of recurring, can be `day`, `week`, `month`, `year`  # noqa: E501

        :param period: The period of this InstallmentData.  # noqa: E501
        :type: str
        """
        allowed_values = ["minute", "day", "week", "month", "year"]  # noqa: E501
        if period not in allowed_values:
            raise ValueError(
                "Invalid value for `period` ({0}), must be one of {1}".format(  # noqa: E501
                    period, allowed_values
                )
            )

        self._period = period

    @property
    def retries(self):
        """Gets the retries of this InstallmentData.  # noqa: E501

        Number of daily basis retry attempts in case of payment has not been captured successfully, from 1 to 15 attempts can be specified.  # noqa: E501

        :return: The retries of this InstallmentData.  # noqa: E501
        :rtype: int
        """
        return self._retries

    @retries.setter
    def retries(self, retries):
        """Sets the retries of this InstallmentData.

        Number of daily basis retry attempts in case of payment has not been captured successfully, from 1 to 15 attempts can be specified.  # noqa: E501

        :param retries: The retries of this InstallmentData.  # noqa: E501
        :type: int
        """
        if retries is not None and retries > 15:  # noqa: E501
            raise ValueError(
                "Invalid value for `retries`, must be a value less than or equal to `15`"
            )  # noqa: E501
        if retries is not None and retries < 1:  # noqa: E501
            raise ValueError(
                "Invalid value for `retries`, must be a value greater than or equal to `1`"
            )  # noqa: E501

        self._retries = retries

    @property
    def subscription_start(self):
        """Gets the subscription_start of this InstallmentData.  # noqa: E501

        The date in yyyy-MM-dd format when subscription will actually become activated (grace period). Auth request will be created but Customer will be charged only when subscription start date comes. Leave it empty or specify the current date to activate subscription at once without any grace period applied.  # noqa: E501

        :return: The subscription_start of this InstallmentData.  # noqa: E501
        :rtype: datetime
        """
        return self._subscription_start

    @subscription_start.setter
    def subscription_start(self, subscription_start):
        """Sets the subscription_start of this InstallmentData.

        The date in yyyy-MM-dd format when subscription will actually become activated (grace period). Auth request will be created but Customer will be charged only when subscription start date comes. Leave it empty or specify the current date to activate subscription at once without any grace period applied.  # noqa: E501

        :param subscription_start: The subscription_start of this InstallmentData.  # noqa: E501
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
        """Gets the trans_type of this InstallmentData.  # noqa: E501


        :return: The trans_type of this InstallmentData.  # noqa: E501
        :rtype: str
        """
        return self._trans_type

    @trans_type.setter
    def trans_type(self, trans_type):
        """Sets the trans_type of this InstallmentData.


        :param trans_type: The trans_type of this InstallmentData.  # noqa: E501
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
        if issubclass(InstallmentData, dict):
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
        if not isinstance(other, InstallmentData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

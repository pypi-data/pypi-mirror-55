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

from cardpay.model.payment_request_customer import (
    PaymentRequestCustomer,
)  # noqa: F401,E501
from cardpay.model.payment_response_card_account import (
    PaymentResponseCardAccount,
)  # noqa: F401,E501
from cardpay.model.payment_response_payment_data import (
    PaymentResponsePaymentData,
)  # noqa: F401,E501
from cardpay.model.transaction_response_merchant_order import (
    TransactionResponseMerchantOrder,
)  # noqa: F401,E501


class PaymentResponse(object):
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
        "customer": "PaymentRequestCustomer",
        "payment_method": "str",
        "merchant_order": "TransactionResponseMerchantOrder",
        "payment_data": "PaymentResponsePaymentData",
        "card_account": "PaymentResponseCardAccount",
    }

    attribute_map = {
        "customer": "customer",
        "payment_method": "payment_method",
        "merchant_order": "merchant_order",
        "payment_data": "payment_data",
        "card_account": "card_account",
    }

    def __init__(
        self,
        customer=None,
        payment_method=None,
        merchant_order=None,
        payment_data=None,
        card_account=None,
    ):  # noqa: E501
        """PaymentResponse - a model defined in Swagger"""  # noqa: E501

        self._customer = None
        self._payment_method = None
        self._merchant_order = None
        self._payment_data = None
        self._card_account = None
        self.discriminator = None

        if customer is not None:
            self.customer = customer
        if payment_method is not None:
            self.payment_method = payment_method
        if merchant_order is not None:
            self.merchant_order = merchant_order
        if payment_data is not None:
            self.payment_data = payment_data
        if card_account is not None:
            self.card_account = card_account

    @property
    def customer(self):
        """Gets the customer of this PaymentResponse.  # noqa: E501

        Customer data  # noqa: E501

        :return: The customer of this PaymentResponse.  # noqa: E501
        :rtype: PaymentRequestCustomer
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """Sets the customer of this PaymentResponse.

        Customer data  # noqa: E501

        :param customer: The customer of this PaymentResponse.  # noqa: E501
        :type: PaymentRequestCustomer
        """

        self._customer = customer

    @property
    def payment_method(self):
        """Gets the payment_method of this PaymentResponse.  # noqa: E501

        Payment method  # noqa: E501

        :return: The payment_method of this PaymentResponse.  # noqa: E501
        :rtype: str
        """
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        """Sets the payment_method of this PaymentResponse.

        Payment method  # noqa: E501

        :param payment_method: The payment_method of this PaymentResponse.  # noqa: E501
        :type: str
        """

        self._payment_method = payment_method

    @property
    def merchant_order(self):
        """Gets the merchant_order of this PaymentResponse.  # noqa: E501

        Merchant order data  # noqa: E501

        :return: The merchant_order of this PaymentResponse.  # noqa: E501
        :rtype: TransactionResponseMerchantOrder
        """
        return self._merchant_order

    @merchant_order.setter
    def merchant_order(self, merchant_order):
        """Sets the merchant_order of this PaymentResponse.

        Merchant order data  # noqa: E501

        :param merchant_order: The merchant_order of this PaymentResponse.  # noqa: E501
        :type: TransactionResponseMerchantOrder
        """

        self._merchant_order = merchant_order

    @property
    def payment_data(self):
        """Gets the payment_data of this PaymentResponse.  # noqa: E501

        Payment data  # noqa: E501

        :return: The payment_data of this PaymentResponse.  # noqa: E501
        :rtype: PaymentResponsePaymentData
        """
        return self._payment_data

    @payment_data.setter
    def payment_data(self, payment_data):
        """Sets the payment_data of this PaymentResponse.

        Payment data  # noqa: E501

        :param payment_data: The payment_data of this PaymentResponse.  # noqa: E501
        :type: PaymentResponsePaymentData
        """

        self._payment_data = payment_data

    @property
    def card_account(self):
        """Gets the card_account of this PaymentResponse.  # noqa: E501

        Card account data *(for BANKCARD payment method only)*  # noqa: E501

        :return: The card_account of this PaymentResponse.  # noqa: E501
        :rtype: PaymentResponseCardAccount
        """
        return self._card_account

    @card_account.setter
    def card_account(self, card_account):
        """Sets the card_account of this PaymentResponse.

        Card account data *(for BANKCARD payment method only)*  # noqa: E501

        :param card_account: The card_account of this PaymentResponse.  # noqa: E501
        :type: PaymentResponseCardAccount
        """

        self._card_account = card_account

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
        if issubclass(PaymentResponse, dict):
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
        if not isinstance(other, PaymentResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

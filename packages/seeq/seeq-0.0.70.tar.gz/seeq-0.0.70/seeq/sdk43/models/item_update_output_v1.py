# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.43.09-v201909272304
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ItemUpdateOutputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'data_id': 'str',
        'datasource_class': 'str',
        'datasource_id': 'str',
        'error_message': 'str',
        'item': 'ItemPreviewV1'
    }

    attribute_map = {
        'data_id': 'dataId',
        'datasource_class': 'datasourceClass',
        'datasource_id': 'datasourceId',
        'error_message': 'errorMessage',
        'item': 'item'
    }

    def __init__(self, data_id=None, datasource_class=None, datasource_id=None, error_message=None, item=None):
        """
        ItemUpdateOutputV1 - a model defined in Swagger
        """

        self._data_id = None
        self._datasource_class = None
        self._datasource_id = None
        self._error_message = None
        self._item = None

        if data_id is not None:
          self.data_id = data_id
        if datasource_class is not None:
          self.datasource_class = datasource_class
        if datasource_id is not None:
          self.datasource_id = datasource_id
        if error_message is not None:
          self.error_message = error_message
        if item is not None:
          self.item = item

    @property
    def data_id(self):
        """
        Gets the data_id of this ItemUpdateOutputV1.
        An ID which uniquely identifies the item within the datasource that hosts it

        :return: The data_id of this ItemUpdateOutputV1.
        :rtype: str
        """
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        """
        Sets the data_id of this ItemUpdateOutputV1.
        An ID which uniquely identifies the item within the datasource that hosts it

        :param data_id: The data_id of this ItemUpdateOutputV1.
        :type: str
        """

        self._data_id = data_id

    @property
    def datasource_class(self):
        """
        Gets the datasource_class of this ItemUpdateOutputV1.
        The class of the datasource that hosts the item

        :return: The datasource_class of this ItemUpdateOutputV1.
        :rtype: str
        """
        return self._datasource_class

    @datasource_class.setter
    def datasource_class(self, datasource_class):
        """
        Sets the datasource_class of this ItemUpdateOutputV1.
        The class of the datasource that hosts the item

        :param datasource_class: The datasource_class of this ItemUpdateOutputV1.
        :type: str
        """

        self._datasource_class = datasource_class

    @property
    def datasource_id(self):
        """
        Gets the datasource_id of this ItemUpdateOutputV1.
        The ID of the datasource that hosts the item.

        :return: The datasource_id of this ItemUpdateOutputV1.
        :rtype: str
        """
        return self._datasource_id

    @datasource_id.setter
    def datasource_id(self, datasource_id):
        """
        Sets the datasource_id of this ItemUpdateOutputV1.
        The ID of the datasource that hosts the item.

        :param datasource_id: The datasource_id of this ItemUpdateOutputV1.
        :type: str
        """

        self._datasource_id = datasource_id

    @property
    def error_message(self):
        """
        Gets the error_message of this ItemUpdateOutputV1.
        If the update failed, this field will contain an error message explaining the problem

        :return: The error_message of this ItemUpdateOutputV1.
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """
        Sets the error_message of this ItemUpdateOutputV1.
        If the update failed, this field will contain an error message explaining the problem

        :param error_message: The error_message of this ItemUpdateOutputV1.
        :type: str
        """

        self._error_message = error_message

    @property
    def item(self):
        """
        Gets the item of this ItemUpdateOutputV1.
        If the update succeeded, this field will contain a summary of the update

        :return: The item of this ItemUpdateOutputV1.
        :rtype: ItemPreviewV1
        """
        return self._item

    @item.setter
    def item(self, item):
        """
        Sets the item of this ItemUpdateOutputV1.
        If the update succeeded, this field will contain a summary of the update

        :param item: The item of this ItemUpdateOutputV1.
        :type: ItemPreviewV1
        """

        self._item = item

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ItemUpdateOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

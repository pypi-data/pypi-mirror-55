# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.44.00-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ImporterOutputV1(object):
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
        'client_file_name': 'str',
        'data_types': 'list[str]',
        'file_headers': 'list[str]',
        'server_file_name': 'str'
    }

    attribute_map = {
        'client_file_name': 'clientFileName',
        'data_types': 'dataTypes',
        'file_headers': 'fileHeaders',
        'server_file_name': 'serverFileName'
    }

    def __init__(self, client_file_name=None, data_types=None, file_headers=None, server_file_name=None):
        """
        ImporterOutputV1 - a model defined in Swagger
        """

        self._client_file_name = None
        self._data_types = None
        self._file_headers = None
        self._server_file_name = None

        if client_file_name is not None:
          self.client_file_name = client_file_name
        if data_types is not None:
          self.data_types = data_types
        if file_headers is not None:
          self.file_headers = file_headers
        if server_file_name is not None:
          self.server_file_name = server_file_name

    @property
    def client_file_name(self):
        """
        Gets the client_file_name of this ImporterOutputV1.
        The client-side name of the uploaded file

        :return: The client_file_name of this ImporterOutputV1.
        :rtype: str
        """
        return self._client_file_name

    @client_file_name.setter
    def client_file_name(self, client_file_name):
        """
        Sets the client_file_name of this ImporterOutputV1.
        The client-side name of the uploaded file

        :param client_file_name: The client_file_name of this ImporterOutputV1.
        :type: str
        """
        if client_file_name is None:
            raise ValueError("Invalid value for `client_file_name`, must not be `None`")

        self._client_file_name = client_file_name

    @property
    def data_types(self):
        """
        Gets the data_types of this ImporterOutputV1.
        The list of detected column data types in the uploaded file

        :return: The data_types of this ImporterOutputV1.
        :rtype: list[str]
        """
        return self._data_types

    @data_types.setter
    def data_types(self, data_types):
        """
        Sets the data_types of this ImporterOutputV1.
        The list of detected column data types in the uploaded file

        :param data_types: The data_types of this ImporterOutputV1.
        :type: list[str]
        """
        if data_types is None:
            raise ValueError("Invalid value for `data_types`, must not be `None`")

        self._data_types = data_types

    @property
    def file_headers(self):
        """
        Gets the file_headers of this ImporterOutputV1.
        The list of headers (first row) in the uploaded file.If a header name contains special characters or a SQL reserved word, the name will be quoted.

        :return: The file_headers of this ImporterOutputV1.
        :rtype: list[str]
        """
        return self._file_headers

    @file_headers.setter
    def file_headers(self, file_headers):
        """
        Sets the file_headers of this ImporterOutputV1.
        The list of headers (first row) in the uploaded file.If a header name contains special characters or a SQL reserved word, the name will be quoted.

        :param file_headers: The file_headers of this ImporterOutputV1.
        :type: list[str]
        """
        if file_headers is None:
            raise ValueError("Invalid value for `file_headers`, must not be `None`")

        self._file_headers = file_headers

    @property
    def server_file_name(self):
        """
        Gets the server_file_name of this ImporterOutputV1.
        The server-side name of the uploaded file

        :return: The server_file_name of this ImporterOutputV1.
        :rtype: str
        """
        return self._server_file_name

    @server_file_name.setter
    def server_file_name(self, server_file_name):
        """
        Sets the server_file_name of this ImporterOutputV1.
        The server-side name of the uploaded file

        :param server_file_name: The server_file_name of this ImporterOutputV1.
        :type: str
        """
        if server_file_name is None:
            raise ValueError("Invalid value for `server_file_name`, must not be `None`")

        self._server_file_name = server_file_name

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
        if not isinstance(other, ImporterOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

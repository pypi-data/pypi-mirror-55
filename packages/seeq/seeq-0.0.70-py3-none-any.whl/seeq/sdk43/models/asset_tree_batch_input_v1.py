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


class AssetTreeBatchInputV1(object):
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
        'child_host_id': 'str',
        'parent_host_id': 'str',
        'relationships': 'list[AssetTreeSingleInputV1]'
    }

    attribute_map = {
        'child_host_id': 'childHostId',
        'parent_host_id': 'parentHostId',
        'relationships': 'relationships'
    }

    def __init__(self, child_host_id=None, parent_host_id=None, relationships=None):
        """
        AssetTreeBatchInputV1 - a model defined in Swagger
        """

        self._child_host_id = None
        self._parent_host_id = None
        self._relationships = None

        if child_host_id is not None:
          self.child_host_id = child_host_id
        if parent_host_id is not None:
          self.parent_host_id = parent_host_id
        if relationships is not None:
          self.relationships = relationships

    @property
    def child_host_id(self):
        """
        Gets the child_host_id of this AssetTreeBatchInputV1.
        The Seeq ID of the datasource host in which the children are located.

        :return: The child_host_id of this AssetTreeBatchInputV1.
        :rtype: str
        """
        return self._child_host_id

    @child_host_id.setter
    def child_host_id(self, child_host_id):
        """
        Sets the child_host_id of this AssetTreeBatchInputV1.
        The Seeq ID of the datasource host in which the children are located.

        :param child_host_id: The child_host_id of this AssetTreeBatchInputV1.
        :type: str
        """
        if child_host_id is None:
            raise ValueError("Invalid value for `child_host_id`, must not be `None`")

        self._child_host_id = child_host_id

    @property
    def parent_host_id(self):
        """
        Gets the parent_host_id of this AssetTreeBatchInputV1.
        The Seeq ID of the datasource host in which the parents are located.

        :return: The parent_host_id of this AssetTreeBatchInputV1.
        :rtype: str
        """
        return self._parent_host_id

    @parent_host_id.setter
    def parent_host_id(self, parent_host_id):
        """
        Sets the parent_host_id of this AssetTreeBatchInputV1.
        The Seeq ID of the datasource host in which the parents are located.

        :param parent_host_id: The parent_host_id of this AssetTreeBatchInputV1.
        :type: str
        """
        if parent_host_id is None:
            raise ValueError("Invalid value for `parent_host_id`, must not be `None`")

        self._parent_host_id = parent_host_id

    @property
    def relationships(self):
        """
        Gets the relationships of this AssetTreeBatchInputV1.
        The list containing AssetTreeSingleInputV1s to create/update parent-child relationships with.

        :return: The relationships of this AssetTreeBatchInputV1.
        :rtype: list[AssetTreeSingleInputV1]
        """
        return self._relationships

    @relationships.setter
    def relationships(self, relationships):
        """
        Sets the relationships of this AssetTreeBatchInputV1.
        The list containing AssetTreeSingleInputV1s to create/update parent-child relationships with.

        :param relationships: The relationships of this AssetTreeBatchInputV1.
        :type: list[AssetTreeSingleInputV1]
        """

        self._relationships = relationships

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
        if not isinstance(other, AssetTreeBatchInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

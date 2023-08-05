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


class SyncProgress(object):
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
        'asset_count': 'int',
        'asset_progress': 'int',
        'condition_count': 'int',
        'condition_progress': 'int',
        'relationship_count': 'int',
        'relationship_progress': 'int',
        'scalar_count': 'int',
        'scalar_progress': 'int',
        'signal_count': 'int',
        'signal_progress': 'int'
    }

    attribute_map = {
        'asset_count': 'assetCount',
        'asset_progress': 'assetProgress',
        'condition_count': 'conditionCount',
        'condition_progress': 'conditionProgress',
        'relationship_count': 'relationshipCount',
        'relationship_progress': 'relationshipProgress',
        'scalar_count': 'scalarCount',
        'scalar_progress': 'scalarProgress',
        'signal_count': 'signalCount',
        'signal_progress': 'signalProgress'
    }

    def __init__(self, asset_count=None, asset_progress=None, condition_count=None, condition_progress=None, relationship_count=None, relationship_progress=None, scalar_count=None, scalar_progress=None, signal_count=None, signal_progress=None):
        """
        SyncProgress - a model defined in Swagger
        """

        self._asset_count = None
        self._asset_progress = None
        self._condition_count = None
        self._condition_progress = None
        self._relationship_count = None
        self._relationship_progress = None
        self._scalar_count = None
        self._scalar_progress = None
        self._signal_count = None
        self._signal_progress = None

        if asset_count is not None:
          self.asset_count = asset_count
        if asset_progress is not None:
          self.asset_progress = asset_progress
        if condition_count is not None:
          self.condition_count = condition_count
        if condition_progress is not None:
          self.condition_progress = condition_progress
        if relationship_count is not None:
          self.relationship_count = relationship_count
        if relationship_progress is not None:
          self.relationship_progress = relationship_progress
        if scalar_count is not None:
          self.scalar_count = scalar_count
        if scalar_progress is not None:
          self.scalar_progress = scalar_progress
        if signal_count is not None:
          self.signal_count = signal_count
        if signal_progress is not None:
          self.signal_progress = signal_progress

    @property
    def asset_count(self):
        """
        Gets the asset_count of this SyncProgress.

        :return: The asset_count of this SyncProgress.
        :rtype: int
        """
        return self._asset_count

    @asset_count.setter
    def asset_count(self, asset_count):
        """
        Sets the asset_count of this SyncProgress.

        :param asset_count: The asset_count of this SyncProgress.
        :type: int
        """

        self._asset_count = asset_count

    @property
    def asset_progress(self):
        """
        Gets the asset_progress of this SyncProgress.

        :return: The asset_progress of this SyncProgress.
        :rtype: int
        """
        return self._asset_progress

    @asset_progress.setter
    def asset_progress(self, asset_progress):
        """
        Sets the asset_progress of this SyncProgress.

        :param asset_progress: The asset_progress of this SyncProgress.
        :type: int
        """

        self._asset_progress = asset_progress

    @property
    def condition_count(self):
        """
        Gets the condition_count of this SyncProgress.

        :return: The condition_count of this SyncProgress.
        :rtype: int
        """
        return self._condition_count

    @condition_count.setter
    def condition_count(self, condition_count):
        """
        Sets the condition_count of this SyncProgress.

        :param condition_count: The condition_count of this SyncProgress.
        :type: int
        """

        self._condition_count = condition_count

    @property
    def condition_progress(self):
        """
        Gets the condition_progress of this SyncProgress.

        :return: The condition_progress of this SyncProgress.
        :rtype: int
        """
        return self._condition_progress

    @condition_progress.setter
    def condition_progress(self, condition_progress):
        """
        Sets the condition_progress of this SyncProgress.

        :param condition_progress: The condition_progress of this SyncProgress.
        :type: int
        """

        self._condition_progress = condition_progress

    @property
    def relationship_count(self):
        """
        Gets the relationship_count of this SyncProgress.

        :return: The relationship_count of this SyncProgress.
        :rtype: int
        """
        return self._relationship_count

    @relationship_count.setter
    def relationship_count(self, relationship_count):
        """
        Sets the relationship_count of this SyncProgress.

        :param relationship_count: The relationship_count of this SyncProgress.
        :type: int
        """

        self._relationship_count = relationship_count

    @property
    def relationship_progress(self):
        """
        Gets the relationship_progress of this SyncProgress.

        :return: The relationship_progress of this SyncProgress.
        :rtype: int
        """
        return self._relationship_progress

    @relationship_progress.setter
    def relationship_progress(self, relationship_progress):
        """
        Sets the relationship_progress of this SyncProgress.

        :param relationship_progress: The relationship_progress of this SyncProgress.
        :type: int
        """

        self._relationship_progress = relationship_progress

    @property
    def scalar_count(self):
        """
        Gets the scalar_count of this SyncProgress.

        :return: The scalar_count of this SyncProgress.
        :rtype: int
        """
        return self._scalar_count

    @scalar_count.setter
    def scalar_count(self, scalar_count):
        """
        Sets the scalar_count of this SyncProgress.

        :param scalar_count: The scalar_count of this SyncProgress.
        :type: int
        """

        self._scalar_count = scalar_count

    @property
    def scalar_progress(self):
        """
        Gets the scalar_progress of this SyncProgress.

        :return: The scalar_progress of this SyncProgress.
        :rtype: int
        """
        return self._scalar_progress

    @scalar_progress.setter
    def scalar_progress(self, scalar_progress):
        """
        Sets the scalar_progress of this SyncProgress.

        :param scalar_progress: The scalar_progress of this SyncProgress.
        :type: int
        """

        self._scalar_progress = scalar_progress

    @property
    def signal_count(self):
        """
        Gets the signal_count of this SyncProgress.

        :return: The signal_count of this SyncProgress.
        :rtype: int
        """
        return self._signal_count

    @signal_count.setter
    def signal_count(self, signal_count):
        """
        Sets the signal_count of this SyncProgress.

        :param signal_count: The signal_count of this SyncProgress.
        :type: int
        """

        self._signal_count = signal_count

    @property
    def signal_progress(self):
        """
        Gets the signal_progress of this SyncProgress.

        :return: The signal_progress of this SyncProgress.
        :rtype: int
        """
        return self._signal_progress

    @signal_progress.setter
    def signal_progress(self, signal_progress):
        """
        Sets the signal_progress of this SyncProgress.

        :param signal_progress: The signal_progress of this SyncProgress.
        :type: int
        """

        self._signal_progress = signal_progress

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
        if not isinstance(other, SyncProgress):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

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


class AnnotationInputV1(object):
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
        'backup_name': 'str',
        'created_by_id': 'str',
        'description': 'str',
        'discoverable': 'bool',
        'document': 'str',
        'interests': 'list[AnnotationInterestInputV1]',
        'name': 'str',
        'replies_to': 'str',
        'type': 'str'
    }

    attribute_map = {
        'backup_name': 'backupName',
        'created_by_id': 'createdById',
        'description': 'description',
        'discoverable': 'discoverable',
        'document': 'document',
        'interests': 'interests',
        'name': 'name',
        'replies_to': 'repliesTo',
        'type': 'type'
    }

    def __init__(self, backup_name=None, created_by_id=None, description=None, discoverable=None, document=None, interests=None, name=None, replies_to=None, type=None):
        """
        AnnotationInputV1 - a model defined in Swagger
        """

        self._backup_name = None
        self._created_by_id = None
        self._description = None
        self._discoverable = None
        self._document = None
        self._interests = None
        self._name = None
        self._replies_to = None
        self._type = None

        if backup_name is not None:
          self.backup_name = backup_name
        if created_by_id is not None:
          self.created_by_id = created_by_id
        if description is not None:
          self.description = description
        if discoverable is not None:
          self.discoverable = discoverable
        if document is not None:
          self.document = document
        if interests is not None:
          self.interests = interests
        if name is not None:
          self.name = name
        if replies_to is not None:
          self.replies_to = replies_to
        if type is not None:
          self.type = type

    @property
    def backup_name(self):
        """
        Gets the backup_name of this AnnotationInputV1.
        The name of a Document backup to restore, when updating an annotation.

        :return: The backup_name of this AnnotationInputV1.
        :rtype: str
        """
        return self._backup_name

    @backup_name.setter
    def backup_name(self, backup_name):
        """
        Sets the backup_name of this AnnotationInputV1.
        The name of a Document backup to restore, when updating an annotation.

        :param backup_name: The backup_name of this AnnotationInputV1.
        :type: str
        """

        self._backup_name = backup_name

    @property
    def created_by_id(self):
        """
        Gets the created_by_id of this AnnotationInputV1.
        The ID of the User that created this annotation.

        :return: The created_by_id of this AnnotationInputV1.
        :rtype: str
        """
        return self._created_by_id

    @created_by_id.setter
    def created_by_id(self, created_by_id):
        """
        Sets the created_by_id of this AnnotationInputV1.
        The ID of the User that created this annotation.

        :param created_by_id: The created_by_id of this AnnotationInputV1.
        :type: str
        """

        self._created_by_id = created_by_id

    @property
    def description(self):
        """
        Gets the description of this AnnotationInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :return: The description of this AnnotationInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AnnotationInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :param description: The description of this AnnotationInputV1.
        :type: str
        """

        self._description = description

    @property
    def discoverable(self):
        """
        Gets the discoverable of this AnnotationInputV1.
        Whether this annotation is discoverable.

        :return: The discoverable of this AnnotationInputV1.
        :rtype: bool
        """
        return self._discoverable

    @discoverable.setter
    def discoverable(self, discoverable):
        """
        Sets the discoverable of this AnnotationInputV1.
        Whether this annotation is discoverable.

        :param discoverable: The discoverable of this AnnotationInputV1.
        :type: bool
        """

        self._discoverable = discoverable

    @property
    def document(self):
        """
        Gets the document of this AnnotationInputV1.
        This annotation's document.

        :return: The document of this AnnotationInputV1.
        :rtype: str
        """
        return self._document

    @document.setter
    def document(self, document):
        """
        Sets the document of this AnnotationInputV1.
        This annotation's document.

        :param document: The document of this AnnotationInputV1.
        :type: str
        """

        self._document = document

    @property
    def interests(self):
        """
        Gets the interests of this AnnotationInputV1.
        A list of IDs representing the annotation's items of interest

        :return: The interests of this AnnotationInputV1.
        :rtype: list[AnnotationInterestInputV1]
        """
        return self._interests

    @interests.setter
    def interests(self, interests):
        """
        Sets the interests of this AnnotationInputV1.
        A list of IDs representing the annotation's items of interest

        :param interests: The interests of this AnnotationInputV1.
        :type: list[AnnotationInterestInputV1]
        """

        self._interests = interests

    @property
    def name(self):
        """
        Gets the name of this AnnotationInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :return: The name of this AnnotationInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AnnotationInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :param name: The name of this AnnotationInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def replies_to(self):
        """
        Gets the replies_to of this AnnotationInputV1.
        The ID of the Annotation that this annotation replies to.

        :return: The replies_to of this AnnotationInputV1.
        :rtype: str
        """
        return self._replies_to

    @replies_to.setter
    def replies_to(self, replies_to):
        """
        Sets the replies_to of this AnnotationInputV1.
        The ID of the Annotation that this annotation replies to.

        :param replies_to: The replies_to of this AnnotationInputV1.
        :type: str
        """

        self._replies_to = replies_to

    @property
    def type(self):
        """
        Gets the type of this AnnotationInputV1.
        This annotation's type: Report or Journal. Defaults to Journal.

        :return: The type of this AnnotationInputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AnnotationInputV1.
        This annotation's type: Report or Journal. Defaults to Journal.

        :param type: The type of this AnnotationInputV1.
        :type: str
        """

        self._type = type

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
        if not isinstance(other, AnnotationInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

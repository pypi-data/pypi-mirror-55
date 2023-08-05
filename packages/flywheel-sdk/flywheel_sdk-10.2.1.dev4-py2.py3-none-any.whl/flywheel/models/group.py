# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 10.2.1-dev.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

from flywheel.models.common_editions import CommonEditions  # noqa: F401,E501
from flywheel.models.permission import Permission  # noqa: F401,E501
from flywheel.models.provider_links import ProviderLinks  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

from .mixins import GroupMixin

class Group(GroupMixin):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'permissions': 'list[Permission]',
        'created': 'datetime',
        'modified': 'datetime',
        'tags': 'list[str]',
        'providers': 'ProviderLinks',
        'editions': 'CommonEditions'
    }

    attribute_map = {
        'id': '_id',
        'label': 'label',
        'permissions': 'permissions',
        'created': 'created',
        'modified': 'modified',
        'tags': 'tags',
        'providers': 'providers',
        'editions': 'editions'
    }

    rattribute_map = {
        '_id': 'id',
        'label': 'label',
        'permissions': 'permissions',
        'created': 'created',
        'modified': 'modified',
        'tags': 'tags',
        'providers': 'providers',
        'editions': 'editions'
    }

    def __init__(self, id=None, label=None, permissions=None, created=None, modified=None, tags=None, providers=None, editions=None):  # noqa: E501
        """Group - a model defined in Swagger"""
        super(Group, self).__init__()

        self._id = None
        self._label = None
        self._permissions = None
        self._created = None
        self._modified = None
        self._tags = None
        self._providers = None
        self._editions = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if label is not None:
            self.label = label
        if permissions is not None:
            self.permissions = permissions
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if tags is not None:
            self.tags = tags
        if providers is not None:
            self.providers = providers
        if editions is not None:
            self.editions = editions

    @property
    def id(self):
        """Gets the id of this Group.


        :return: The id of this Group.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Group.


        :param id: The id of this Group.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this Group.

        The group label

        :return: The label of this Group.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Group.

        The group label

        :param label: The label of this Group.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def permissions(self):
        """Gets the permissions of this Group.

        Array of user roles

        :return: The permissions of this Group.
        :rtype: list[Permission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this Group.

        Array of user roles

        :param permissions: The permissions of this Group.  # noqa: E501
        :type: list[Permission]
        """

        self._permissions = permissions

    @property
    def created(self):
        """Gets the created of this Group.

        Creation time (automatically set)

        :return: The created of this Group.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Group.

        Creation time (automatically set)

        :param created: The created of this Group.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this Group.

        Last modification time (automatically updated)

        :return: The modified of this Group.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Group.

        Last modification time (automatically updated)

        :param modified: The modified of this Group.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def tags(self):
        """Gets the tags of this Group.

        Array of application-specific tags

        :return: The tags of this Group.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Group.

        Array of application-specific tags

        :param tags: The tags of this Group.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def providers(self):
        """Gets the providers of this Group.


        :return: The providers of this Group.
        :rtype: ProviderLinks
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this Group.


        :param providers: The providers of this Group.  # noqa: E501
        :type: ProviderLinks
        """

        self._providers = providers

    @property
    def editions(self):
        """Gets the editions of this Group.


        :return: The editions of this Group.
        :rtype: CommonEditions
        """
        return self._editions

    @editions.setter
    def editions(self, editions):
        """Sets the editions of this Group.


        :param editions: The editions of this Group.  # noqa: E501
        :type: CommonEditions
        """

        self._editions = editions


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

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
        if not isinstance(other, Group):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result

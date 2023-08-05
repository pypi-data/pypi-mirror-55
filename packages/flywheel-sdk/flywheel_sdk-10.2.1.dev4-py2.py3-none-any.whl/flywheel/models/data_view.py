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

from flywheel.models.data_view_column_spec import DataViewColumnSpec  # noqa: F401,E501
from flywheel.models.data_view_file_spec import DataViewFileSpec  # noqa: F401,E501
from flywheel.models.origin import Origin  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class DataView(object):

    swagger_types = {
        'parent': 'str',
        'label': 'str',
        'description': 'str',
        'public': 'bool',
        'columns': 'list[DataViewColumnSpec]',
        'file_spec': 'DataViewFileSpec',
        'include_ids': 'bool',
        'include_labels': 'bool',
        'missing_data_strategy': 'str',
        'id': 'str',
        'origin': 'Origin'
    }

    attribute_map = {
        'parent': 'parent',
        'label': 'label',
        'description': 'description',
        'public': 'public',
        'columns': 'columns',
        'file_spec': 'fileSpec',
        'include_ids': 'includeIds',
        'include_labels': 'includeLabels',
        'missing_data_strategy': 'missingDataStrategy',
        'id': '_id',
        'origin': 'origin'
    }

    rattribute_map = {
        'parent': 'parent',
        'label': 'label',
        'description': 'description',
        'public': 'public',
        'columns': 'columns',
        'fileSpec': 'file_spec',
        'includeIds': 'include_ids',
        'includeLabels': 'include_labels',
        'missingDataStrategy': 'missing_data_strategy',
        '_id': 'id',
        'origin': 'origin'
    }

    def __init__(self, parent=None, label=None, description=None, public=None, columns=None, file_spec=None, include_ids=None, include_labels=None, missing_data_strategy=None, id=None, origin=None):  # noqa: E501
        """DataView - a model defined in Swagger"""
        super(DataView, self).__init__()

        self._parent = None
        self._label = None
        self._description = None
        self._public = None
        self._columns = None
        self._file_spec = None
        self._include_ids = None
        self._include_labels = None
        self._missing_data_strategy = None
        self._id = None
        self._origin = None
        self.discriminator = None
        self.alt_discriminator = None

        if parent is not None:
            self.parent = parent
        if label is not None:
            self.label = label
        if description is not None:
            self.description = description
        if public is not None:
            self.public = public
        if columns is not None:
            self.columns = columns
        if file_spec is not None:
            self.file_spec = file_spec
        if include_ids is not None:
            self.include_ids = include_ids
        if include_labels is not None:
            self.include_labels = include_labels
        if missing_data_strategy is not None:
            self.missing_data_strategy = missing_data_strategy
        if id is not None:
            self.id = id
        if origin is not None:
            self.origin = origin

    @property
    def parent(self):
        """Gets the parent of this DataView.

        The parent container id

        :return: The parent of this DataView.
        :rtype: str
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this DataView.

        The parent container id

        :param parent: The parent of this DataView.  # noqa: E501
        :type: str
        """

        self._parent = parent

    @property
    def label(self):
        """Gets the label of this DataView.

        Application-specific label

        :return: The label of this DataView.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this DataView.

        Application-specific label

        :param label: The label of this DataView.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def description(self):
        """Gets the description of this DataView.


        :return: The description of this DataView.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DataView.


        :param description: The description of this DataView.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def public(self):
        """Gets the public of this DataView.

        Indicates whether or not the view is public

        :return: The public of this DataView.
        :rtype: bool
        """
        return self._public

    @public.setter
    def public(self, public):
        """Sets the public of this DataView.

        Indicates whether or not the view is public

        :param public: The public of this DataView.  # noqa: E501
        :type: bool
        """

        self._public = public

    @property
    def columns(self):
        """Gets the columns of this DataView.


        :return: The columns of this DataView.
        :rtype: list[DataViewColumnSpec]
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """Sets the columns of this DataView.


        :param columns: The columns of this DataView.  # noqa: E501
        :type: list[DataViewColumnSpec]
        """

        self._columns = columns

    @property
    def file_spec(self):
        """Gets the file_spec of this DataView.


        :return: The file_spec of this DataView.
        :rtype: DataViewFileSpec
        """
        return self._file_spec

    @file_spec.setter
    def file_spec(self, file_spec):
        """Sets the file_spec of this DataView.


        :param file_spec: The file_spec of this DataView.  # noqa: E501
        :type: DataViewFileSpec
        """

        self._file_spec = file_spec

    @property
    def include_ids(self):
        """Gets the include_ids of this DataView.

        Whether or not to include container id fields. Default is true

        :return: The include_ids of this DataView.
        :rtype: bool
        """
        return self._include_ids

    @include_ids.setter
    def include_ids(self, include_ids):
        """Sets the include_ids of this DataView.

        Whether or not to include container id fields. Default is true

        :param include_ids: The include_ids of this DataView.  # noqa: E501
        :type: bool
        """

        self._include_ids = include_ids

    @property
    def include_labels(self):
        """Gets the include_labels of this DataView.

        Whether or not to include container label fields. Default is true

        :return: The include_labels of this DataView.
        :rtype: bool
        """
        return self._include_labels

    @include_labels.setter
    def include_labels(self, include_labels):
        """Sets the include_labels of this DataView.

        Whether or not to include container label fields. Default is true

        :param include_labels: The include_labels of this DataView.  # noqa: E501
        :type: bool
        """

        self._include_labels = include_labels

    @property
    def missing_data_strategy(self):
        """Gets the missing_data_strategy of this DataView.

        What to do if missing data are encountered. Default is none, which is to say replace with an empty or null value.

        :return: The missing_data_strategy of this DataView.
        :rtype: str
        """
        return self._missing_data_strategy

    @missing_data_strategy.setter
    def missing_data_strategy(self, missing_data_strategy):
        """Sets the missing_data_strategy of this DataView.

        What to do if missing data are encountered. Default is none, which is to say replace with an empty or null value.

        :param missing_data_strategy: The missing_data_strategy of this DataView.  # noqa: E501
        :type: str
        """

        self._missing_data_strategy = missing_data_strategy

    @property
    def id(self):
        """Gets the id of this DataView.

        Unique database ID

        :return: The id of this DataView.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DataView.

        Unique database ID

        :param id: The id of this DataView.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def origin(self):
        """Gets the origin of this DataView.


        :return: The origin of this DataView.
        :rtype: Origin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this DataView.


        :param origin: The origin of this DataView.  # noqa: E501
        :type: Origin
        """

        self._origin = origin


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
        if not isinstance(other, DataView):
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

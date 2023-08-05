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

from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.search_ml_input_file import SearchMlInputFile  # noqa: F401,E501
from flywheel.models.search_query import SearchQuery  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class SearchMlInput(object):

    swagger_types = {
        'labels': 'list[str]',
        'search_query': 'SearchQuery',
        'files': 'list[SearchMlInputFile]',
        'output': 'ContainerReference'
    }

    attribute_map = {
        'labels': 'labels',
        'search_query': 'search-query',
        'files': 'files',
        'output': 'output'
    }

    rattribute_map = {
        'labels': 'labels',
        'search-query': 'search_query',
        'files': 'files',
        'output': 'output'
    }

    def __init__(self, labels=None, search_query=None, files=None, output=None):  # noqa: E501
        """SearchMlInput - a model defined in Swagger"""
        super(SearchMlInput, self).__init__()

        self._labels = None
        self._search_query = None
        self._files = None
        self._output = None
        self.discriminator = None
        self.alt_discriminator = None

        if labels is not None:
            self.labels = labels
        if search_query is not None:
            self.search_query = search_query
        if files is not None:
            self.files = files
        if output is not None:
            self.output = output

    @property
    def labels(self):
        """Gets the labels of this SearchMlInput.


        :return: The labels of this SearchMlInput.
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this SearchMlInput.


        :param labels: The labels of this SearchMlInput.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def search_query(self):
        """Gets the search_query of this SearchMlInput.


        :return: The search_query of this SearchMlInput.
        :rtype: SearchQuery
        """
        return self._search_query

    @search_query.setter
    def search_query(self, search_query):
        """Sets the search_query of this SearchMlInput.


        :param search_query: The search_query of this SearchMlInput.  # noqa: E501
        :type: SearchQuery
        """

        self._search_query = search_query

    @property
    def files(self):
        """Gets the files of this SearchMlInput.


        :return: The files of this SearchMlInput.
        :rtype: list[SearchMlInputFile]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this SearchMlInput.


        :param files: The files of this SearchMlInput.  # noqa: E501
        :type: list[SearchMlInputFile]
        """

        self._files = files

    @property
    def output(self):
        """Gets the output of this SearchMlInput.


        :return: The output of this SearchMlInput.
        :rtype: ContainerReference
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this SearchMlInput.


        :param output: The output of this SearchMlInput.  # noqa: E501
        :type: ContainerReference
        """

        self._output = output


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
        if not isinstance(other, SearchMlInput):
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

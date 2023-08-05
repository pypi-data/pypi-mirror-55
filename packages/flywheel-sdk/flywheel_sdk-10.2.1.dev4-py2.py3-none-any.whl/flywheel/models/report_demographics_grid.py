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

from flywheel.models.report_ethnicity_grid import ReportEthnicityGrid  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class ReportDemographicsGrid(object):

    swagger_types = {
        'black_or_african_american': 'ReportEthnicityGrid',
        'unknown_or_not_reported': 'ReportEthnicityGrid',
        'american_indian_or_alaska_native': 'ReportEthnicityGrid',
        'asian': 'ReportEthnicityGrid',
        'white': 'ReportEthnicityGrid',
        'total': 'ReportEthnicityGrid',
        'native_hawaiian_or_other_pacific_islander': 'ReportEthnicityGrid',
        'more_than_one_race': 'ReportEthnicityGrid',
        'male_count': 'int',
        'group_label': 'str',
        'over_18_count': 'int',
        'under_18_count': 'int',
        'female_count': 'int',
        'subjects_count': 'int',
        'other_count': 'int',
        'name': 'str',
        'session_count': 'int',
        'admins': 'list[str]',
        'demographics_total': 'int'
    }

    attribute_map = {
        'black_or_african_american': 'Black or African American',
        'unknown_or_not_reported': 'Unknown or Not Reported',
        'american_indian_or_alaska_native': 'American Indian or Alaska Native',
        'asian': 'Asian',
        'white': 'White',
        'total': 'Total',
        'native_hawaiian_or_other_pacific_islander': 'Native Hawaiian or Other Pacific Islander',
        'more_than_one_race': 'More Than One Race',
        'male_count': 'male_count',
        'group_label': 'group_label',
        'over_18_count': 'over_18_count',
        'under_18_count': 'under_18_count',
        'female_count': 'female_count',
        'subjects_count': 'subjects_count',
        'other_count': 'other_count',
        'name': 'name',
        'session_count': 'session_count',
        'admins': 'admins',
        'demographics_total': 'demographics_total'
    }

    rattribute_map = {
        'Black or African American': 'black_or_african_american',
        'Unknown or Not Reported': 'unknown_or_not_reported',
        'American Indian or Alaska Native': 'american_indian_or_alaska_native',
        'Asian': 'asian',
        'White': 'white',
        'Total': 'total',
        'Native Hawaiian or Other Pacific Islander': 'native_hawaiian_or_other_pacific_islander',
        'More Than One Race': 'more_than_one_race',
        'male_count': 'male_count',
        'group_label': 'group_label',
        'over_18_count': 'over_18_count',
        'under_18_count': 'under_18_count',
        'female_count': 'female_count',
        'subjects_count': 'subjects_count',
        'other_count': 'other_count',
        'name': 'name',
        'session_count': 'session_count',
        'admins': 'admins',
        'demographics_total': 'demographics_total'
    }

    def __init__(self, black_or_african_american=None, unknown_or_not_reported=None, american_indian_or_alaska_native=None, asian=None, white=None, total=None, native_hawaiian_or_other_pacific_islander=None, more_than_one_race=None, male_count=None, group_label=None, over_18_count=None, under_18_count=None, female_count=None, subjects_count=None, other_count=None, name=None, session_count=None, admins=None, demographics_total=None):  # noqa: E501
        """ReportDemographicsGrid - a model defined in Swagger"""
        super(ReportDemographicsGrid, self).__init__()

        self._black_or_african_american = None
        self._unknown_or_not_reported = None
        self._american_indian_or_alaska_native = None
        self._asian = None
        self._white = None
        self._total = None
        self._native_hawaiian_or_other_pacific_islander = None
        self._more_than_one_race = None
        self._male_count = None
        self._group_label = None
        self._over_18_count = None
        self._under_18_count = None
        self._female_count = None
        self._subjects_count = None
        self._other_count = None
        self._name = None
        self._session_count = None
        self._admins = None
        self._demographics_total = None
        self.discriminator = None
        self.alt_discriminator = None

        if black_or_african_american is not None:
            self.black_or_african_american = black_or_african_american
        if unknown_or_not_reported is not None:
            self.unknown_or_not_reported = unknown_or_not_reported
        if american_indian_or_alaska_native is not None:
            self.american_indian_or_alaska_native = american_indian_or_alaska_native
        if asian is not None:
            self.asian = asian
        if white is not None:
            self.white = white
        if total is not None:
            self.total = total
        if native_hawaiian_or_other_pacific_islander is not None:
            self.native_hawaiian_or_other_pacific_islander = native_hawaiian_or_other_pacific_islander
        if more_than_one_race is not None:
            self.more_than_one_race = more_than_one_race
        if male_count is not None:
            self.male_count = male_count
        if group_label is not None:
            self.group_label = group_label
        if over_18_count is not None:
            self.over_18_count = over_18_count
        if under_18_count is not None:
            self.under_18_count = under_18_count
        if female_count is not None:
            self.female_count = female_count
        if subjects_count is not None:
            self.subjects_count = subjects_count
        if other_count is not None:
            self.other_count = other_count
        if name is not None:
            self.name = name
        if session_count is not None:
            self.session_count = session_count
        if admins is not None:
            self.admins = admins
        if demographics_total is not None:
            self.demographics_total = demographics_total

    @property
    def black_or_african_american(self):
        """Gets the black_or_african_american of this ReportDemographicsGrid.


        :return: The black_or_african_american of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._black_or_african_american

    @black_or_african_american.setter
    def black_or_african_american(self, black_or_african_american):
        """Sets the black_or_african_american of this ReportDemographicsGrid.


        :param black_or_african_american: The black_or_african_american of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._black_or_african_american = black_or_african_american

    @property
    def unknown_or_not_reported(self):
        """Gets the unknown_or_not_reported of this ReportDemographicsGrid.


        :return: The unknown_or_not_reported of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._unknown_or_not_reported

    @unknown_or_not_reported.setter
    def unknown_or_not_reported(self, unknown_or_not_reported):
        """Sets the unknown_or_not_reported of this ReportDemographicsGrid.


        :param unknown_or_not_reported: The unknown_or_not_reported of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._unknown_or_not_reported = unknown_or_not_reported

    @property
    def american_indian_or_alaska_native(self):
        """Gets the american_indian_or_alaska_native of this ReportDemographicsGrid.


        :return: The american_indian_or_alaska_native of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._american_indian_or_alaska_native

    @american_indian_or_alaska_native.setter
    def american_indian_or_alaska_native(self, american_indian_or_alaska_native):
        """Sets the american_indian_or_alaska_native of this ReportDemographicsGrid.


        :param american_indian_or_alaska_native: The american_indian_or_alaska_native of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._american_indian_or_alaska_native = american_indian_or_alaska_native

    @property
    def asian(self):
        """Gets the asian of this ReportDemographicsGrid.


        :return: The asian of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._asian

    @asian.setter
    def asian(self, asian):
        """Sets the asian of this ReportDemographicsGrid.


        :param asian: The asian of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._asian = asian

    @property
    def white(self):
        """Gets the white of this ReportDemographicsGrid.


        :return: The white of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._white

    @white.setter
    def white(self, white):
        """Sets the white of this ReportDemographicsGrid.


        :param white: The white of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._white = white

    @property
    def total(self):
        """Gets the total of this ReportDemographicsGrid.


        :return: The total of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ReportDemographicsGrid.


        :param total: The total of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._total = total

    @property
    def native_hawaiian_or_other_pacific_islander(self):
        """Gets the native_hawaiian_or_other_pacific_islander of this ReportDemographicsGrid.


        :return: The native_hawaiian_or_other_pacific_islander of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._native_hawaiian_or_other_pacific_islander

    @native_hawaiian_or_other_pacific_islander.setter
    def native_hawaiian_or_other_pacific_islander(self, native_hawaiian_or_other_pacific_islander):
        """Sets the native_hawaiian_or_other_pacific_islander of this ReportDemographicsGrid.


        :param native_hawaiian_or_other_pacific_islander: The native_hawaiian_or_other_pacific_islander of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._native_hawaiian_or_other_pacific_islander = native_hawaiian_or_other_pacific_islander

    @property
    def more_than_one_race(self):
        """Gets the more_than_one_race of this ReportDemographicsGrid.


        :return: The more_than_one_race of this ReportDemographicsGrid.
        :rtype: ReportEthnicityGrid
        """
        return self._more_than_one_race

    @more_than_one_race.setter
    def more_than_one_race(self, more_than_one_race):
        """Sets the more_than_one_race of this ReportDemographicsGrid.


        :param more_than_one_race: The more_than_one_race of this ReportDemographicsGrid.  # noqa: E501
        :type: ReportEthnicityGrid
        """

        self._more_than_one_race = more_than_one_race

    @property
    def male_count(self):
        """Gets the male_count of this ReportDemographicsGrid.


        :return: The male_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._male_count

    @male_count.setter
    def male_count(self, male_count):
        """Sets the male_count of this ReportDemographicsGrid.


        :param male_count: The male_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._male_count = male_count

    @property
    def group_label(self):
        """Gets the group_label of this ReportDemographicsGrid.

        Application-specific label

        :return: The group_label of this ReportDemographicsGrid.
        :rtype: str
        """
        return self._group_label

    @group_label.setter
    def group_label(self, group_label):
        """Sets the group_label of this ReportDemographicsGrid.

        Application-specific label

        :param group_label: The group_label of this ReportDemographicsGrid.  # noqa: E501
        :type: str
        """

        self._group_label = group_label

    @property
    def over_18_count(self):
        """Gets the over_18_count of this ReportDemographicsGrid.


        :return: The over_18_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._over_18_count

    @over_18_count.setter
    def over_18_count(self, over_18_count):
        """Sets the over_18_count of this ReportDemographicsGrid.


        :param over_18_count: The over_18_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._over_18_count = over_18_count

    @property
    def under_18_count(self):
        """Gets the under_18_count of this ReportDemographicsGrid.


        :return: The under_18_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._under_18_count

    @under_18_count.setter
    def under_18_count(self, under_18_count):
        """Sets the under_18_count of this ReportDemographicsGrid.


        :param under_18_count: The under_18_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._under_18_count = under_18_count

    @property
    def female_count(self):
        """Gets the female_count of this ReportDemographicsGrid.


        :return: The female_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._female_count

    @female_count.setter
    def female_count(self, female_count):
        """Sets the female_count of this ReportDemographicsGrid.


        :param female_count: The female_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._female_count = female_count

    @property
    def subjects_count(self):
        """Gets the subjects_count of this ReportDemographicsGrid.


        :return: The subjects_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._subjects_count

    @subjects_count.setter
    def subjects_count(self, subjects_count):
        """Sets the subjects_count of this ReportDemographicsGrid.


        :param subjects_count: The subjects_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._subjects_count = subjects_count

    @property
    def other_count(self):
        """Gets the other_count of this ReportDemographicsGrid.


        :return: The other_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._other_count

    @other_count.setter
    def other_count(self, other_count):
        """Sets the other_count of this ReportDemographicsGrid.


        :param other_count: The other_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._other_count = other_count

    @property
    def name(self):
        """Gets the name of this ReportDemographicsGrid.

        Application-specific label

        :return: The name of this ReportDemographicsGrid.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ReportDemographicsGrid.

        Application-specific label

        :param name: The name of this ReportDemographicsGrid.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def session_count(self):
        """Gets the session_count of this ReportDemographicsGrid.


        :return: The session_count of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._session_count

    @session_count.setter
    def session_count(self, session_count):
        """Sets the session_count of this ReportDemographicsGrid.


        :param session_count: The session_count of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._session_count = session_count

    @property
    def admins(self):
        """Gets the admins of this ReportDemographicsGrid.


        :return: The admins of this ReportDemographicsGrid.
        :rtype: list[str]
        """
        return self._admins

    @admins.setter
    def admins(self, admins):
        """Sets the admins of this ReportDemographicsGrid.


        :param admins: The admins of this ReportDemographicsGrid.  # noqa: E501
        :type: list[str]
        """

        self._admins = admins

    @property
    def demographics_total(self):
        """Gets the demographics_total of this ReportDemographicsGrid.


        :return: The demographics_total of this ReportDemographicsGrid.
        :rtype: int
        """
        return self._demographics_total

    @demographics_total.setter
    def demographics_total(self, demographics_total):
        """Sets the demographics_total of this ReportDemographicsGrid.


        :param demographics_total: The demographics_total of this ReportDemographicsGrid.  # noqa: E501
        :type: int
        """

        self._demographics_total = demographics_total


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
        if not isinstance(other, ReportDemographicsGrid):
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

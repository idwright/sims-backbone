
import logging

from backbone_server.controllers.base_controller import BaseController

from backbone_server.report.missing_locations import MissingLocations
from backbone_server.report.missing_taxon import MissingTaxon
from backbone_server.report.uncurated_locations import UncuratedLocations
from backbone_server.report.multiple_location_names import MultipleLocationNames
from backbone_server.report.multiple_location_gps import MultipleLocationGPS

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class ReportController(BaseController):

    def missing_locations(self, include_country, studies=None, user=None, auths=None):  # noqa: E501
        """fetches studies with sampling events with missing locations

         # noqa: E501

        :param includeCountry: include studies where only a country level location is set
        :type includeCountry: bool


        :rtype: Studies
        """
        get = MissingLocations(self.get_engine(), self.get_session())

        retcode = 200

        studies = get.get(include_country, studies)

        return studies, retcode

    def missing_taxon(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches studies with uncurated taxon

         # noqa: E501


        :rtype: Studies
        """
        get = MissingTaxon(self.get_engine(), self.get_session())

        retcode = 200

        studies = get.get(studies)

        return studies, retcode

    def multiple_location_gps(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches studies with multiple locations with the same GPS

         # noqa: E501


        :rtype: Studies
        """
        get = MultipleLocationGPS(self.get_engine(), self.get_session())

        retcode = 200

        studies = get.get(studies)

        return studies, retcode

    def multiple_location_names(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches studies with multiple locations with the same name

         # noqa: E501


        :rtype: Studies
        """
        get = MultipleLocationNames(self.get_engine(), self.get_session())

        retcode = 200

        studies = get.get(studies)

        return studies, retcode

    def uncurated_locations(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches studies with uncurated locations

         # noqa: E501


        :rtype: Studies
        """

        get = UncuratedLocations(self.get_engine(), self.get_session())

        retcode = 200

        studies = get.get(studies)

        return studies, retcode

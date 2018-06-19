import connexion
import six

from swagger_server.models.original_sample import OriginalSample  # noqa: E501
from swagger_server.models.original_samples import OriginalSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.original_sample_controller  import OriginalSampleController

original_sample_controller = OriginalSampleController()

def create_original_sample(originalSample, user=None, token_info=None):
    """
    create_original_sample
    Create a originalSample
    :param originalSample: 
    :type originalSample: dict | bytes

    :rtype: OriginalSample
    """
    if connexion.request.is_json:
        originalSample = OriginalSample.from_dict(connexion.request.get_json())

    return original_sample_controller.create_original_sample(originalSample, user,
                                                           original_sample_controller.token_info(token_info))

def delete_original_sample(originalSampleId, user=None, token_info=None):
    """
    deletes an originalSample
    
    :param originalSampleId: ID of originalSample to fetch
    :type originalSampleId: str

    :rtype: None
    """
    return original_sample_controller.delete_original_sample(originalSampleId, user,
                                                           original_sample_controller.token_info(token_info))


def download_original_sample(originalSampleId, user=None, token_info=None):
    """
    fetches an originalSample
    
    :param originalSampleId: ID of originalSample to fetch
    :type originalSampleId: str

    :rtype: OriginalSample
    """
    return original_sample_controller.download_original_sample(originalSampleId, user,
                                                             original_sample_controller.token_info(token_info))


def download_original_samples(filter=None, start=None, count=None, user=None, token_info=None):  # noqa: E501
    """fetches originalSamples

     # noqa: E501

    :param filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
    :type filter: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples(filter, start,
                                                              count, user,
                                                              original_sample_controller.token_info(token_info))

def download_original_samples_by_event_set(eventSetId, start=None, count=None, user=None, token_info=None):
    """
    fetches originalSamples in a given event set
    
    :param eventSetId: Event Set name
    :type eventSetId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_event_set(eventSetId,start,
                                                                           count, user,
                                                                       original_sample_controller.token_info(token_info))

def download_original_samples_by_attr(propName, propValue, studyName=None, user=None, token_info=None):
    """
    fetches a originalSample by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: OriginalSample
    """
    return original_sample_controller.download_original_samples_by_attr(propName, propValue,
                                                                           studyName,
                                                                           user,
                                                                           original_sample_controller.token_info(token_info))

def download_original_samples_by_location(locationId, start=None, count=None, user=None, token_info=None):
    """
    fetches originalSamples for a location
    
    :param locationId: location
    :type locationId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_location(locationId, start,
                                                                          count, user,
                                                                          original_sample_controller.token_info(token_info))

def download_original_samples_by_study(studyName, start=None, count=None, user=None, token_info=None):
    """
    fetches originalSamples for a study
    
    :param studyName: 4 digit study code
    :type studyName: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_study(studyName, start,
                                                                       count, user,
                                                                       original_sample_controller.token_info(token_info))

def download_original_samples_by_taxa(taxaId, start=None, count=None, user=None, token_info=None):
    """
    fetches originalSamples for a given taxonomy classification code
    
    :param taxaId: NCBI taxonomy code
    :type taxaId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_taxa(taxaId, start,
                                                                      count, user,
                                                                       original_sample_controller.token_info(token_info))


def update_original_sample(originalSampleId, originalSample, user=None, token_info=None):
    """
    updates an originalSample
    
    :param originalSampleId: ID of originalSample to update
    :type originalSampleId: str
    :param originalSample: 
    :type originalSample: dict | bytes

    :rtype: OriginalSample
    """
    if connexion.request.is_json:
        originalSample = OriginalSample.from_dict(connexion.request.get_json())
    return original_sample_controller.update_original_sample(originalSampleId, originalSample, user,
                                                           original_sample_controller.token_info(token_info))


import logging
from urllib import parse

import requests
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings


log = logging.getLogger(__name__)


def build_feedback_url( perceived_url, perceived_ip, email ):
    """ Builds problem/feedback url.
        Called by confirm_requeast_helper.prepare_context() """
    assert type( perceived_url ) == str
    assert type( perceived_ip ) == str
    assert type( email ) == str
    log.debug( f'perceived_url, ``{perceived_url}``' )
    encoded_perceived_url = parse.quote( perceived_url )
    log.debug( f'encoded_perceived_url, ``{encoded_perceived_url}``' )
    feedback_url = '{feedback_form_url}?formkey={feedback_form_key}&entry_1={email}&entry_2={encoded_perceived_url}&entry_3={perceived_ip}'.format(
        email=email,
        feedback_form_url=settings.FEEDBACK_FORM_URL,
        feedback_form_key=settings.FEEDBACK_FORM_KEY,
        encoded_perceived_url=encoded_perceived_url,
        perceived_ip=perceived_ip
        )
    log.debug( f'feedback_url, ``{feedback_url}``' )
    return feedback_url


def grab_pattern_header( feedback_url ) -> str:
    """ Prepares html for header.
        Called by ??? """
    assert type( feedback_url ) == str
    cache_key = 'pattern_header'
    header_html = cache.get( cache_key, None )
    if header_html:
        log.debug( 'pattern-header in cache' )
    else:
        log.debug( 'pattern-header not in cache' )
        r = requests.get( settings.PATTERNLIB_HEADER_URL )
        header_html = r.content.decode( 'utf8' )
        header_html = header_html.replace( 'DYNAMIC__FEEDBACK', feedback_url )
        cache.set( cache_key, header_html, settings.PATTERNLIB_HEADER_CACHE_TIMEOUT )
    return header_html


# def build_feedback_url( perceived_url, perceived_ip ):
#     """ Builds problem/feedback url.
#         Called by confirm_requeast_helper.prepare_context() """
#     assert type( perceived_url ) == str
#     assert type( perceived_ip ) == str
#     feedback_url = '{feedback_form_url}?formkey={feedback_form_key}&entry_2={perceived_url}&entry_3={perceived_ip}'.format(
#         feedback_form_url=settings.FEEDBACK_FORM_URL,
#         feedback_form_key=settings.FEEDBACK_FORM_KEY,
#         perceived_url=perceived_url,
#         perceived_ip=perceived_ip
#         )
#     log.debug( f'feedback_url, ``{feedback_url}``' )
#     return feedback_url

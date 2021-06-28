import logging

import requests
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings


log = logging.getLogger(__name__)


def grab_pattern_header() -> str:
    """ Prepares html for header. """
    cache_key = 'pattern_header'
    header_html = cache.get( cache_key, None )
    if header_html:
        log.debug( 'pattern-header in cache' )
    else:
        log.debug( 'pattern-header not in cache' )
        r = requests.get( settings.PATTERN_HEADER_URL )
        header_html = r.content.decode( 'utf8' )
        site_url = info_url = reverse( 'info_url' )  # this may change from site to site
        # header_html = header_html.replace( 'DYNAMIC__SITE', site_url ).replace( 'DYNAMIC__INFO', info_url )
        header_html = header_html.replace( '{% url \"info_url\" %}', info_url )
        cache.set( cache_key, header_html, settings.PATTERN_LIB_CACHE_TIMEOUT )
    return header_html


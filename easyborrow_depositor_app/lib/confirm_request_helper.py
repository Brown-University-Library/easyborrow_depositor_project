import datetime, json, logging

from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


def save_incoming_data( perceived_url ):
    """ Logs and saves perceived url.
        Called by views.confirm_request() """
    assert type(perceived_url) == str
    log.debug( f'perceived_url, ``{perceived_url}``' )
    req_data = RequestData()
    req_data.ezb_url = perceived_url
    req_data.save()

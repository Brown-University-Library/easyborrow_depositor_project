import datetime, json, logging

from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


class ConfReqHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def save_incoming_data( self, perceived_url ):
        """ Logs and saves perceived url.
            Called by views.confirm_request() """
        assert type(perceived_url) == str
        log.debug( f'perceived_url, ``{perceived_url}``' )
        self.req_data_obj = RequestData()
        self.req_data_obj.ezb_url = perceived_url
        self.req_data_obj.save()
        log.debug( f'new uu_id, ``{self.req_data_obj.uu_id}``' )
        return str( self.req_data_obj.uu_id )

    # def save_incoming_data( perceived_url ):
    #     """ Logs and saves perceived url.
    #         Called by views.confirm_request() """
    #     assert type(perceived_url) == str
    #     log.debug( f'perceived_url, ``{perceived_url}``' )
    #     req_data = RequestData()
    #     req_data.ezb_url = perceived_url
    #     req_data.save()
    #     uu_id = req_data.uu_id
    #     log.debug( f'new uu_id, ``{uu_id}``' )
    #     return uu_id

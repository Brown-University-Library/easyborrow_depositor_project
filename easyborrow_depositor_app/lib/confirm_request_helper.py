import datetime, json, logging

from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


class ConfReqHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def save_incoming_data( self, perceived_url, referrer, remote_addr ):
        """ Logs and saves perceived url.
            Called by views.confirm_request() """
        assert type(perceived_url) == str; assert type(referrer) == str; assert type(remote_addr) == str
        log.debug( f'perceived_url, ``{perceived_url}``; referrer, ``{referrer}``; remote_addr, ``{remote_addr}``' )
        self.req_data_obj = RequestData()
        self.req_data_obj.ezb_url = perceived_url
        data = {
            'referrer': referrer,
            'remote_addr': remote_addr
            }
        jsn = json.dumps( data, sort_keys=True, indent=2 )
        self.req_data_obj.referrer_url = jsn
        self.req_data_obj.save()
        log.debug( f'new uu_id, ``{self.req_data_obj.uu_id}``' )
        return str( self.req_data_obj.uu_id )

    # def save_incoming_data( self, perceived_url ):
    #     """ Logs and saves perceived url.
    #         Called by views.confirm_request() """
    #     assert type(perceived_url) == str
    #     log.debug( f'perceived_url, ``{perceived_url}``' )
    #     self.req_data_obj = RequestData()
    #     self.req_data_obj.ezb_url = perceived_url
    #     self.req_data_obj.save()
    #     log.debug( f'new uu_id, ``{self.req_data_obj.uu_id}``' )
    #     return str( self.req_data_obj.uu_id )


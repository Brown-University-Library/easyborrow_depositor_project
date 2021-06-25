import datetime, json, logging

import requests

from django.conf import settings
from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


class ConfReqHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def save_incoming_data( self, perceived_url, referrer, remote_addr ):
        """ Logs and saves perceived url.
            Called by views.confirm_request() """
        assert type(perceived_url) == str; assert type(referrer) == str; assert type(remote_addr) == str
        ( uu_id, err ) = ( None, None )
        try:
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
            uu_id = str( self.req_data_obj.uu_id )
            log.debug( f'new uu_id, ``{uu_id}``' )
        except:
            err = 'Problem saving data from easyBorrow link.'
            log.exception( err )
        return ( uu_id, err )

    def save_item_info( self, querystring ):
        """ Converts openurl data into bibjson.
            Called by views.confirm_request() """
        assert type(querystring) == str
        err = None
        try:
            params = { 'ourl': querystring }
            r = requests.get( settings.BIB_OURL_API, params=params, timeout=10, verify=True )
            log.debug( f'r-url, ``{r.url}``' )
            bib_dct = json.loads( r.content.decode('utf-8', 'replace') )
            data = { 'raw_bib_dct': bib_dct }
            jsn = json.dumps( data, sort_keys=True, indent=2 )
            self.req_data_obj.item_json = jsn
            1/0
            self.req_data_obj.save()
        except:
            err = 'Problem creating and saving item-data.'
            log.exception( err )
        return err

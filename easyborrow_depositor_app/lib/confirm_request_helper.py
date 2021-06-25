import datetime, json, logging

import requests

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
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
            self.req_data_obj.save()
        except:
            err = 'Problem creating and saving item-data.'
            log.exception( err )
        return err

    def save_patron_info( self, meta_dct ):
        """ Saves required shib-info.
            Called by views.confirm_request() """
        assert type(meta_dct) == dict
        shibber = Shibber()
        cleaned_meta_dct = shibber.prep_shib_dct( meta_dct, host )
        temp_is_member_of_str = cleaned_meta_dct.get( 'isMemberOf', '' )
        patron_dct = {
            shib_eppn: cleaned_meta_dct.get( 'Shibboleth-eppn', '' ),
            shib_name_first: cleaned_meta_dct.get( 'Shibboleth-givenName', '' ),
            shib_name_last: cleaned_meta_dct.get( 'Shibboleth-sn', '' ),
            shib_patron_barcode: cleaned_meta_dct.get( 'Shibboleth-brownBarCode', '' ),
            shib_email: cleaned_meta_dct.get( 'Shibboleth-mail', '' ),
            shib_group: cleaned_meta_dct.get( 'Shibboleth-brownType', '' ),
            shib_is_member_of_list: temp_is_member_of_str.split( ';' )
            }
        # eppn = cleaned_meta_dct.get( 'Shibboleth-eppn', '' )
        # name_first = cleaned_meta_dct.get( 'Shibboleth-givenName', '' )
        # name_last = cleaned_meta_dct.get( 'Shibboleth-sn', '' )
        # patron_barcode = cleaned_meta_dct.get( 'Shibboleth-brownBarCode', '' )
        # email = cleaned_meta_dct.get( 'Shibboleth-mail', '' )
        # group = cleaned_meta_dct.get( 'Shibboleth-brownType', '' )
        # is_member_of = temp_is_member_of_str.split( ';' )




    # def ensure_basics()
        # ensure_basics = shibber.ensure_basics( cleaned_meta_dct )

    #     - eppn
    # - name_first
    # - name_last
    # - patron_barcode
    # - patron_email
    # - patron_group ('Undergraduate Student', 'Graduate Student', etc)


    def handle_error( self, request, err ):
        assert type(err) == str
        request.session['error_message'] = err
        redirect_url = reverse( 'message_url' )
        log.debug( 'redirecting to message url' )
        rsp = HttpResponseRedirect( redirect_url )
        return rsp

    ## end class class ConfReqHlpr()


class Shibber():

    def prep_shib_dct( self, request_meta_dct, host ):
        """ Returns dct from shib-info.
            Called by ConfReqHlpr.save_patron_info() """
        log.debug( 'starting prep_shib_dct()' )
        if host == '127.0.0.1' or host == '127.0.0.1:8000' or host == 'testserver':
            cleaned_meta_dct = settings_app.DEV_META_DCT
        else:
            cleaned_meta_dct = copy.copy( request_meta_dct )
            for (key, val) in request_meta_dct.items():  # get rid of some dictionary items not serializable
                if 'passenger' in key:
                    cleaned_meta_dct.pop( key )
                elif 'wsgi.' in key:
                    cleaned_meta_dct.pop( key )
        log.debug( f'cleaned_meta_dct, ```{cleaned_meta_dct}```' )
        return cleaned_meta_dct

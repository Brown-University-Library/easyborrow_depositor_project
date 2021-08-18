import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from easyborrow_depositor_app.lib import common
from easyborrow_depositor_app.models import RequestData
from django.shortcuts import render


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
            self.req_data_obj.perceived_url = perceived_url
            data = {
                'referrer': referrer,
                'remote_addr': remote_addr
                }
            jsn = json.dumps( data, sort_keys=True, indent=2 )
            self.req_data_obj.referrer_json = jsn
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
            # bib_dct = json.loads( r.content.decode('utf-8', 'replace') )
            # data = { 'raw_bib_dct': bib_dct }
            raw_bib_dct = json.loads( r.content.decode('utf-8', 'replace') )
            data = raw_bib_dct['response']['bib']
            jsn = json.dumps( data, sort_keys=True, indent=2 )
            self.req_data_obj.item_json = jsn
            self.req_data_obj.save()
        except:
            err = 'Problem creating and saving item-data.'
            log.exception( err )
        return err

    def save_patron_info( self, meta_dct, host ):
        """ Saves required shib-info.
            Called by views.confirm_request() """
        assert type(meta_dct) == dict
        assert type(host) == str
        err = None
        try:
            shibber = Shibber()
            cleaned_meta_dct = shibber.prep_shib_dct( meta_dct, host )
            log.debug( f'cleaned_meta_dct, ``{cleaned_meta_dct}``' )
            temp_is_member_of_str = cleaned_meta_dct.get( 'isMemberOf', '' )
            temp_eppn = cleaned_meta_dct.get( 'Shibboleth-eppn', '' )
            patron_dct = {
                'shib_eppn': s.split( '@' )[0],  # just the auth_id goes into the db  :(
                'shib_name_first': cleaned_meta_dct.get( 'Shibboleth-givenName', '' ),
                'shib_name_last': cleaned_meta_dct.get( 'Shibboleth-sn', '' ),
                'shib_patron_barcode': cleaned_meta_dct.get( 'Shibboleth-brownBarCode', '' ),
                'shib_email': cleaned_meta_dct.get( 'Shibboleth-mail', '' ),
                'shib_group': cleaned_meta_dct.get( 'Shibboleth-brownType', '' ),
                'shib_is_member_of_list': temp_is_member_of_str.split( ';' )
                }
            jsn = json.dumps( patron_dct, sort_keys=True, indent=2 )
            self.req_data_obj.patron_json = jsn
            self.req_data_obj.save()
        except:
            err = 'Problem creating and saving patron-data.'
            log.exception( err )
        return err

    # def save_patron_info( self, meta_dct, host ):
    #     """ Saves required shib-info.
    #         Called by views.confirm_request() """
    #     assert type(meta_dct) == dict
    #     assert type(host) == str
    #     err = None
    #     try:
    #         shibber = Shibber()
    #         cleaned_meta_dct = shibber.prep_shib_dct( meta_dct, host )
    #         log.debug( f'cleaned_meta_dct, ``{cleaned_meta_dct}``' )
    #         temp_is_member_of_str = cleaned_meta_dct.get( 'isMemberOf', '' )
    #         patron_dct = {
    #             'shib_eppn': cleaned_meta_dct.get( 'Shibboleth-eppn', '' ),
    #             'shib_name_first': cleaned_meta_dct.get( 'Shibboleth-givenName', '' ),
    #             'shib_name_last': cleaned_meta_dct.get( 'Shibboleth-sn', '' ),
    #             'shib_patron_barcode': cleaned_meta_dct.get( 'Shibboleth-brownBarCode', '' ),
    #             'shib_email': cleaned_meta_dct.get( 'Shibboleth-mail', '' ),
    #             'shib_group': cleaned_meta_dct.get( 'Shibboleth-brownType', '' ),
    #             'shib_is_member_of_list': temp_is_member_of_str.split( ';' )
    #             }
    #         jsn = json.dumps( patron_dct, sort_keys=True, indent=2 )
    #         self.req_data_obj.patron_json = jsn
    #         self.req_data_obj.save()
    #     except:
    #         err = 'Problem creating and saving patron-data.'
    #         log.exception( err )
    #     return err

    def prepare_context( self, start_time_obj ):
        """ Preps page's data_dct.
            Called by views.confirm_request() """
        assert type(start_time_obj) == datetime.datetime
        ( context, err ) = ( None, None )
        try:
            patron_dct = json.loads( self.req_data_obj.patron_json )
            item_dct = json.loads( self.req_data_obj.item_json )
            perceived_ip = json.loads( self.req_data_obj.referrer_json )['remote_addr']
            feedback_url = common.build_feedback_url( self.req_data_obj.perceived_url, perceived_ip, patron_dct['shib_email'] )
            context = {
                'time_start': str( start_time_obj ),
                'time_elapsed': str( datetime.datetime.now() - start_time_obj ),
                'pattern_header': common.grab_pattern_header( feedback_url ),
                'welcome_name': patron_dct['shib_name_first'],
                'item_title': item_dct['title'],
                'action_url': reverse( 'confirm_handler_url' ),
            }
            log.debug( 'context, ``%s``' % pprint.pformat(context)[0:100] )
        except:
            err = 'Problem preparing "confirm-request" screen.'
            log.exception( err )
        return ( context, err )

    def prepare_response( self, request, context ):
        """ Preps response.
            Called by views.confirm_request() """
        if request.GET.get('format', '') == 'json':
            context_json = json.dumps(context, sort_keys=True, indent=2)
            resp = HttpResponse( context_json, content_type='application/javascript; charset=utf-8' )
        else:
            # resp = render( request, 'easyborrow_depositor_app_templates/confirm.html', context )
            return render( request, 'confirm.html', context )
        return resp

    ## end class class ConfReqHlpr()


class Shibber():

    def prep_shib_dct( self, request_meta_dct, host ):
        """ Returns dct from shib-info.
            Called by ConfReqHlpr.save_patron_info() """
        log.debug( 'starting prep_shib_dct()' )
        if host == '127.0.0.1' or host == '127.0.0.1:8000' or host == 'testserver':
            cleaned_meta_dct = settings.DEV_SHIB_DCT
        else:
            # cleaned_meta_dct = copy.copy( request_meta_dct )
            cleaned_meta_dct = request_meta_dct.copy()
            for (key, val) in request_meta_dct.items():  # get rid of some dictionary items not serializable
                if 'passenger' in key:
                    cleaned_meta_dct.pop( key )
                elif 'wsgi.' in key:
                    cleaned_meta_dct.pop( key )
        log.debug( f'cleaned_meta_dct, ```{cleaned_meta_dct}```' )
        return cleaned_meta_dct

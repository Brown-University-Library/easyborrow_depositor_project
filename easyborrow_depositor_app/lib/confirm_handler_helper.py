import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from easyborrow_depositor_app.lib import common
from easyborrow_depositor_app.models import RequestData
from easyborrow_depositor_app.models import RequestLegacyEntry
from django.shortcuts import render


log = logging.getLogger(__name__)


class ConfHndlrHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def load_data_obj( self, uu_id ):
        try:
            self.req_data_obj = RequestData.objects.get( uu_id=uu_id )
        except:
            err = 'Problem accessing request-data.'
            log.exception( err )
            return err

    def save_request_to_ezb_db( self ):
        try:
            ezb_db = RequestLegacyEntry()
            item_dct = json.loads( self.req_data_obj.item_json )
            ezb_db.title = item_dct.get( 'title', '' )
            ezb_db.isbn = self.process_isbn( item_dct )
            ezb_db.sfxurl = self.req_data_obj.perceived_url
            ezb_db.created = datetime.datetime.now()
            ezb_db.save( using='ezborrow_legacy' )
            log.debug( f'ezb_db.id, ``{ezb_db.id}``' )
            self.req_data_obj.ezb_db_id = ezb_db.id
            self.req_data_obj.save()
            return
        except:
            err = 'Problem saving request into easyBorrow database.'
            log.exception( err )
            return err

    def process_isbn( self, item_dct ):
        log.debug( f'item_dct, ``{pprint.pformat(item_dct)}``' )
        isbn = ''
        identifiers = item_dct.get('identifier', [])
        log.debug( f'identifiers, ``{identifiers}``' )
        for iden in identifiers:
            log.debug( f'iden, ``{iden}``' )
            assert type(iden) == dict
            assert sorted( iden.keys() ) == ['id', 'type']
            if iden['type'] == 'isbn':
                log.debug( 'type legit' )
                if len( iden['id'].strip() ) > 1:
                    log.debug( 'len id legit' )
                    isbn = iden['id']
                    break
        log.debug( f'isbn, ``{isbn}``' )
        return isbn

    ## end class ConfHndlrHlpr()

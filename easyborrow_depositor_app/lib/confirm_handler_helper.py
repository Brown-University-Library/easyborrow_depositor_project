import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
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
            ## item data --------------------------
            item_dct = json.loads( self.req_data_obj.item_json )
            ezb_db.title = item_dct.get( 'title', '' )[0:255]
            ezb_db.isbn = self.process_isbn( item_dct )[0:13]
            ezb_db.wc_accession = self.process_oclcnum( item_dct )[0:20]
            # bibno
            ezb_db.volumes = self.process_volumes( item_dct )
            ezb_db.sfxurl = self.req_data_obj.perceived_url[0:1000]

            ## patron data ------------------------
            patron_dct = json.loads( self.req_data_obj.patron_json )
            ezb_db.patronid = None
            ezb_db.eppn = patron_dct.get( 'shib_eppn', '' )
            ezb_db.name = '%s %s'.strip() % ( patron_dct.get('shib_name_first', ''), patron_dct.get('shib_name_last', '') )
            ezb_db.firstname = patron_dct.get( 'shib_name_first', '' )
            ezb_db.lastname = patron_dct.get( 'shib_name_last', '' )
            ezb_db.barcode = patron_dct.get( 'shib_patron_barcode', '' )
            ezb_db.email = patron_dct.get( 'shib_email', '' )
            ezb_db.group = patron_dct.get( 'shib_group', '' )

            ## other data -------------------------
            ezb_db.pref = 'quick'
            ezb_db.loc = 'rock'
            ezb_db.alt_edition = 'y'
            ezb_db.request_status = 'not_yet_processed'
            ezb_db.staffnote = ''
            ezb_db.created = timezone.now()

            ## save -------------------------------
            ezb_db.save( using='ezborrow_legacy' )

            ## update request-obj w/ezb-id --------
            log.debug( f'ezb_db.id, ``{ezb_db.id}``' )
            self.req_data_obj.ezb_db_id = ezb_db.id
            self.req_data_obj.save()

            return
        except:
            err = 'Problem saving request into easyBorrow database.'
            log.exception( err )
            return err

    def process_isbn( self, item_dct ):
        # log.debug( f'item_dct, ``{pprint.pformat(item_dct)}``' )
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
                    isbn = iden['id'].replace( '-', '' )
                    break
        log.debug( f'isbn, ``{isbn}``' )
        return isbn

    def process_oclcnum( self, item_dct ):
        # log.debug( f'item_dct, ``{pprint.pformat(item_dct)}``' )
        oclc = ''
        identifiers = item_dct.get('identifier', [])
        log.debug( f'identifiers, ``{identifiers}``' )
        for iden in identifiers:
            log.debug( f'iden, ``{iden}``' )
            assert type(iden) == dict
            assert sorted( iden.keys() ) == ['id', 'type']
            if iden['type'] == 'oclc':
                log.debug( 'type legit' )
                if len( iden['id'].strip() ) > 1:
                    log.debug( 'len id legit' )
                    oclc = iden['id'].replace( '-', '' )
                    break
        log.debug( f'oclc, ``{oclc}``' )
        return oclc

    def process_volumes( self, item_dct ):
        volumes = item_dct.get( 'volume', None )
        if volumes:
            volumes = volumes[0:255]
        else:
            volumes = ''
        return volumes

    ## end class ConfHndlrHlpr()

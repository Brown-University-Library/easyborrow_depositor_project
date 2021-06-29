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
        self.req_data_obj = RequestData.objects.get( uu_id=uu_id )

    def save_request_to_ezb_db( self ):
        legacy_entry = RequestLegacyEntry()
        item_dct = json.loads( self.req_data_obj.item_json )['raw_bib_dct']['response']['bib']
        legacy_entry.title = item_dct['title']
        legacy_entry.sfxurl = self.req_data_obj.perceived_url
        legacy_entry.created = datetime.datetime.now()
        legacy_entry.save( using='ezborrow_legacy' )
        log.debug( f'legacy_entry.id, ``{legacy_entry.id}``' )
        return 'foo'


    ## end class ConfHndlrHlpr()

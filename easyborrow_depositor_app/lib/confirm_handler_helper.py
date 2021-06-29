import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from easyborrow_depositor_app.lib import common
from easyborrow_depositor_app.models import RequestData
from django.shortcuts import render


log = logging.getLogger(__name__)


class ConfHndlrHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def load_data_obj( self, uu_id ):
        self.req_data_obj = RequestData.objects.get( uu_id=uu_id )

    def save_request_to_ezb_db( self ):
        return 'foo'


    ## end class ConfHndlrHlpr()

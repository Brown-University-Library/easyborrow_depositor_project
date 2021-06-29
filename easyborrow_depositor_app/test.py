# -*- coding: utf-8 -*-

import json, pprint

from django.test import TestCase
from easyborrow_depositor_app.lib import version_helper
from easyborrow_depositor_app.lib.confirm_handler_helper import ConfHndlrHlpr


# log = logging.getLogger(__name__)
TestCase.maxDiff = None


class VersionUrlTest( TestCase ):
    """ Checks version url. """

    def test_version_url(self):
        """ Checks '/version/'. """
        response = self.client.get( '/version/' )  # project root part of url is assumed
        self.assertEqual( 200, response.status_code )
        jsn_dct = json.loads( response.content )
        self.assertEqual(  dict, type(jsn_dct) )
        dct_keys = sorted( jsn_dct.keys() )
        self.assertEqual( ['request', 'response'], dct_keys )
        response_keys = sorted( jsn_dct['response'].keys() )
        self.assertEqual( ['timetaken', 'version'], response_keys )


class ParseItemDct( TestCase ):

    def test_isbn(self):
        hlpr = ConfHndlrHlpr()
        jsn = '''{
  "end_page": null,
  "identifier": [
    {
      "id": "0688084613",
      "type": "isbn"
    },
    {
      "id": ":",
      "type": "isbn"
    }
  ],
  "issue": null
}'''
        dct = json.loads( jsn )
        isbn = hlpr.process_isbn( dct )
        self.assertEqual( '0688084613', isbn )

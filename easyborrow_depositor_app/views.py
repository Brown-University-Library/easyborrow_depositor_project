import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from easyborrow_depositor_app.lib import version_helper
from easyborrow_depositor_app.lib.confirm_request_helper import ConfReqHlpr
from easyborrow_depositor_app.models import RequestData

log = logging.getLogger(__name__)


# =================================================
# primary app urls...
# =================================================

def confirm_request( request ):
    """ Validates and cleans incoming data; presents confirmation-button; triggers call to confirm_handler. """
    log.debug( '\n\nstarting views.confirm_request()' )
    log.debug( f'request.__dict__, ``{pprint.pformat(request.__dict__)}``' )
    ## setup --------------------------------------
    for key in [ 'uu_id', 'error_message' ]:
        request.session[key] = ''
    ## save incoming request ----------------------
    conf_req_hlpr = ConfReqHlpr()
    ( uu_id, err ) = conf_req_hlpr.save_incoming_data(
        request.build_absolute_uri(), request.META.get('HTTP_REFERER', ''), request.META.get('REMOTE_ADDR', '') )
    if err:
        rsp = conf_req_hlpr.handle_error( request, err )
        return rsp
    assert type(uu_id) == str
    request.session['uu_id'] = uu_id
    ## save item info -----------------------------
    err = conf_req_hlpr.save_item_info( request.META["QUERY_STRING"] )
    if err:
        rsp = conf_req_hlpr.handle_error( request, err )
        return rsp
    ## save patron info ---------------------------
    err = conf_req_hlpr.save_patron_info( request.META, request.get_host() )
    if err:
        rsp = conf_req_hlpr.handle_error( request, err )
        return rsp
    ## prep context -------------------------------
    ( context, err ) = conf_req_hlpr.prepare_context()
    if err:
        rsp = conf_req_hlpr.handle_error( request, err )
        return rsp
    ## present confirmation-button
    return HttpResponse( 'confirm_request coming ' )

def confirm_handler( request ):
    """ Deposits data to separate easyborrow db; triggers email to user; redirects to message. """
    return HttpResponse( 'confirm_handler coming ' )

def message( request ):
    """ Shows user confirmation message (or problem message). """
    log.debug( '\n\nstarting views.message()' )
    message = request.session['error_message']
    return HttpResponse( message )


# =================================================
# support urls...
# =================================================

def version( request ):
    """ Returns basic branch and commit data. """
    rq_now = datetime.datetime.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )

def error_check( request ):
    """ For checking that admins receive error-emails. """
    if settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )

def info( request ):
    """ Presents basic web-app info. """
    return HttpResponse( 'info response coming' )

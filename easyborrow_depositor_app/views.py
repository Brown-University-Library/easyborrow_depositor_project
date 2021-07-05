import datetime, json, logging, pprint

import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from easyborrow_depositor_app.lib import common
from easyborrow_depositor_app.lib import version_helper
from easyborrow_depositor_app.lib.confirm_handler_helper import ConfHndlrHlpr
from easyborrow_depositor_app.lib.confirm_request_helper import ConfReqHlpr
from easyborrow_depositor_app.lib.message_helper import MsgHlpr
from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


# =================================================
# primary app urls...
# =================================================

def confirm_request( request ):
    """ Validates and cleans incoming data; presents confirmation-button; triggers call to confirm_handler. """
    log.debug( '\n\nstarting views.confirm_request()' )
    # log.debug( f'request.__dict__, ``{pprint.pformat(request.__dict__)}``' )
    ## setup --------------------------------------
    start = datetime.datetime.now()
    for key in [ 'uu_id', 'error_message' ]:
        request.session[key] = ''
    ## save incoming request ----------------------
    conf_req_hlpr = ConfReqHlpr()
    ( uu_id, err ) = conf_req_hlpr.save_incoming_data(
        request.build_absolute_uri(), request.META.get('HTTP_REFERER', ''), request.META.get('REMOTE_ADDR', '') )
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    assert type(uu_id) == str
    request.session['uu_id'] = uu_id
    ## save item info -----------------------------
    err = conf_req_hlpr.save_item_info( request.META["QUERY_STRING"] )
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    ## save patron info ---------------------------
    err = conf_req_hlpr.save_patron_info( request.META, request.get_host() )
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    ## prep context -------------------------------
    ( context, err ) = conf_req_hlpr.prepare_context( start )
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    ## prep response ------------------------------
    resp = conf_req_hlpr.prepare_response( request, context )
    return resp


def confirm_handler( request ):
    """ Deposits data to separate easyborrow db; triggers email to user; redirects to message. """
    log.debug( '\n\nstarting views.confirm_handler()' )
    uu_id = request.session['uu_id']
    log.debug( f'uu_id, ``{uu_id}``' )
    conf_hndlr_hlpr = ConfHndlrHlpr()
    ## load data from uu_id -----------------------
    err = conf_hndlr_hlpr.load_data_obj( uu_id )
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    ## deposit request to legacy db ---------------
    err = conf_hndlr_hlpr.save_request_to_ezb_db()
    if err:
        rsp = common.handle_error( request, err )
        return rsp
    ## email user ---------------------------------
    # TODO
    ## redirect to message-view -------------------
    log.debug( 'happy-path; redirecting to message-url' )
    return HttpResponseRedirect( reverse('message_url') )


def message( request ):
    """ Shows user confirmation message (or problem message). """
    log.debug( '\n\nstarting views.message()' )
    msg_hlpr = MsgHlpr()
    error_message = request.session.get( 'error_message', '' )
    uu_id = request.session['uu_id']
    if error_message:
        log.debug( 'returning error_message' )
        # return HttpResponse( message )
        context = msg_hlpr.build_problem_context( error_message, uu_id )
        return render( request, 'easyborrow_depositor_app_templates/message.html', context )
    ## load data from uu_id -----------------------
    log.debug( f'uu_id, ``{uu_id}``' )
    err = msg_hlpr.load_data_obj( uu_id )
    if err:
        assert type(err) == str
        return HttpResponse( err )
    ## prep context -------------------------------
    ( context, err ) = msg_hlpr.prepare_context()
    log.debug( f'err, ``{err}``' )
    log.debug( f'context, ``{context}``' )
    if err:
        assert type(err) == str
        return HttpResponse( err )
    ## return request-submitted message -----------
    assert type(context) == dict
    return render( request, 'easyborrow_depositor_app_templates/message.html', context )


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











#     def build_submitted_message( self, firstname, lastname, bib_dct, ezb_db_id, email ):
#         """ Prepares submitted message
#             Called by views.process_request() """
#         if bib_dct.get( 'title', '' ) != '':
#             title = bib_dct['title']
#         else:
#             title = bib_dct['source']
#         message = '''
# Greetings {firstname} {lastname},

# We're getting the title '{title}' for you. You'll soon receive more information in an email.

# Some information for your records:

# - Title: '{title}'
# - Your easyBorrow reference number: '{ezb_reference_num}'
# - Notification of arrival will be sent to email address: <{email}>

# If you have any questions, contact the Library's Interlibrary Loan office at <interlibrary_loan@brown.edu> or call 401-863-2169.

#   '''.format(
#         firstname=firstname,
#         lastname=lastname,
#         title=title,
#         ezb_reference_num=ezb_db_id,
#         email=email )
#         log.debug( 'ezb submitted message built' )
#         return message


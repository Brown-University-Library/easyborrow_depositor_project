import datetime, json, logging, pprint

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError
from easyborrow_depositor_app.lib import version_helper
from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


## primary app urls...

def confirm_request( request ):
    """ Validates and cleans incoming data; presents confirmation-button; triggers call to confirm_handler. """
    log.debug( '\n\nstarting views.confirm_request()' )
    ## save incoming request
    """
    datestamp, referrer, full url
    """
    # log.debug( f'request.__dict__, ``{pprint.pformat(request.__dict__)}``' )
    perceived_url = request.build_absolute_uri()
    log.debug( f'perceived_url, ``{perceived_url}``' )
    req_data = RequestData()
    req_data.ezb_url = perceived_url
    req_data.save()


    ## clean params
    """
    - remove empty params
    - remove small list of end-of-line encodings
    - remove empty space
    """
    ## save patron_dct & item_dct with short_code
    """
    patron_dct:
    - eppn
    - name_first
    - name_last
    - patron_barcode
    - patron_email
    - patron_group ('Undergraduate Student', 'Graduate Student', etc)
    item_dct:
    - title
    - isbn
    - oclc accession_number
    - volumes
    - openurl
    """
    ## present confirmation-button
    return HttpResponse( 'confirm_request coming ' )

def confirm_handler( request ):
    """ Deposits data to separate easyborrow db; triggers email to user; redirects to message. """
    return HttpResponse( 'confirm_handler coming ' )

def message( request ):
    """ Shows user confirmation message (or problem message). """
    return HttpResponse( 'message coming ' )


## support urls...

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
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )

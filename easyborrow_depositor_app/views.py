from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError


def version( request ):
    return HttpResponse( 'coming' )

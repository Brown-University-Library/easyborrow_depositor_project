import uuid

from django.db import models


class RequestData( models.Model ):
    created = models.DateTimeField( auto_now_add=True )
    uu_id = models.UUIDField( default=uuid.uuid4, editable=False )
    ezb_url = models.TextField( null=True, blank=True )
    referrer_url = models.TextField( null=True, blank=True )
    item_json = models.TextField( null=True, blank=True )
    patron_json = models.TextField( null=True, blank=True )
    ezb_db_id = models.CharField( max_length=100, null=True, blank=True )

    def __str__(self):
        return str( self.uu_id )

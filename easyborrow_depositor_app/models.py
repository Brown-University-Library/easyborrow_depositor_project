import uuid

from django.db import models


class RequestData( models.Model ):
    created = models.DateTimeField( auto_now_add=True )
    uu_id = models.UUIDField( default=uuid.uuid4, editable=False )
    perceived_url = models.TextField( null=True, blank=True )
    referrer_json = models.TextField( null=True, blank=True )
    item_json = models.TextField( null=True, blank=True )
    patron_json = models.TextField( null=True, blank=True )
    ezb_db_id = models.CharField( max_length=100, null=True, blank=True )

    def __str__(self):
        return str( self.uu_id )

    class Meta:
        ordering = ['-created']
        verbose_name = "request entry"
        verbose_name_plural = "request entries"


class RequestLegacyEntry(models.Model):

    TIMEPREF_CHOICES = (
        ('quick', 'Quick'),
        ('long', 'Long'),
        ) # ('db_value', 'display_value')

    LOCATION_CHOICES = (
        ('rock', 'Rock'),
        ('sci', 'SciLi'),
        )

    YESNO_CHOICES = (
        ('y', 'Yes'),
        ('n', 'No'),
        )

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, blank=True)
    wc_accession = models.CharField(max_length=20, blank=True)
    bibno = models.CharField(max_length=10, blank=True)
    pref = models.CharField(max_length=5, choices=TIMEPREF_CHOICES, default='quick')
    loc = models.CharField(max_length=4, choices=LOCATION_CHOICES, default='rock')
    alt_edition = models.CharField(max_length=1, choices=YESNO_CHOICES, default='y')
    volumes = models.CharField(max_length=255, blank=True)
    sfxurl = models.TextField()
    patronId = models.CharField(max_length=7, blank=True)
    eppn = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=255, blank=True)
    firstname = models.CharField(max_length=120, blank=True)
    lastname = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    barcode = models.CharField(max_length=14, blank=True)
    email = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=30, blank=True)
    staffnote = models.CharField(max_length=255, blank=True)
    request_status = models.CharField(max_length=30, default='not_yet_processed')

    def __str__(self):
        # return str( self.id ) + ' ::: ' + self.title
        return self.title

    class Meta:
        managed = False
        ordering = ['-created']
        verbose_name = "deposited entry"
        verbose_name_plural = "deposited entries"
        db_table = 'requests'

    ## end RequestLegacyEntry()


# sqlite>
# sqlite> pragma table_info( requests );
# 0|id|integer|1||1
# 1|title|varchar(255)|1|''|0
# 2|isbn|varchar(13)|1|''|0
# 3|wc_accession|varchar(20)|1|'0'|0
# 4|bibno|varchar(8)|1|''|0
# 5|pref|text|1|'quick'|0
# 6|loc|text|1|'rock'|0
# 7|alt_edition|text|1|'y'|0
# 8|volumes|varchar(90)|1|''|0
# 9|sfxurl|text|1||0
# 10|patronId|integer|1|'0'|0
# 11|eppn|varchar(20)|1|'init'|0
# 12|name|varchar(255)|1|''|0
# 13|firstname|varchar(120)|1|''|0
# 14|lastname|varchar(120)|1|''|0
# 15|created|datetime|1|'1970-01-01 00:00:00'|0
# 16|barcode|varchar(14)|1|''|0
# 17|email|varchar(50)|1|''|0
# 18|group|varchar(30)|1|''|0
# 19|staffnote|varchar(255)|1|''|0
# 20|request_status|varchar(30)|1|'not_yet_processed'|0
# sqlite>

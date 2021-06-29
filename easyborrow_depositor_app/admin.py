import logging
from easyborrow_depositor_app.models import RequestData
from easyborrow_depositor_app.models import RequestLegacyEntry

from django.contrib import admin


log = logging.getLogger(__name__)


# <https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#exposing-multiple-databases-in-django-s-admin-interface>

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'ezborrow_legacy'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    ## end class MultiDBModelAdmin()


class RequestDataAdmin(admin.ModelAdmin):

    # list_display = [ 'created', 'uu_id', 'perceived_url_100', 'referrer_json', 'item_json', 'patron_json', 'ezb_db_id' ]
    list_display = [ 'created', 'uu_id', 'perceived_url_75', 'referrer_json', 'item_json_100', 'patron_json_100', 'ezb_db_id' ]

    def perceived_url_75( self, obj ):
        url = obj.perceived_url
        if len(obj.perceived_url) > 75:
            url = f'{obj.perceived_url[:72]}...'
        return url
    perceived_url_75.short_description = 'perceived url (75)'

    def item_json_100( self, obj ):
        item_str = obj.item_json
        log.debug( f'item_str after initialization, ``{item_str}``' )
        if item_str:
            assert type(item_str) == str
            if len(obj.item_json) > 100:
                item_str = f'{obj.item_json[:97]}...'
                log.debug( f'item_str after length, exceeded, ``{item_str}``' )
        return item_str
    item_json_100.short_description = 'item json (100)'

    def patron_json_100( self, obj ):
        patron_str = obj.patron_json
        log.debug( f'patron_str after initialization, ``{patron_str}``' )
        if patron_str:
            assert type(patron_str) == str
            if len(obj.patron_json) > 100:
                patron_str = f'{obj.patron_json[:97]}...'
                log.debug( f'patron_str after length, exceeded, ``{patron_str}``' )
        return patron_str
    patron_json_100.short_description = 'patron json (100)'

    readonly_fields = ( 'created', 'uu_id', 'ezb_db_id' )

    search_fields = [ 'created', 'uu_id', 'perceived_url', 'referrer_json', 'item_json', 'patron_json', 'ezb_db_id' ]

    date_hierarchy = 'created'

    save_on_top = True

    ## end class RequestDataAdmin()


class RequestLegacyEntryAdmin( MultiDBModelAdmin ):

    list_display = [ 'id', 'title', 'isbn' ]

    ## end class RequestLegacyEntryAdmin()


admin.site.register( RequestData, RequestDataAdmin )
admin.site.register( RequestLegacyEntry, RequestLegacyEntryAdmin )

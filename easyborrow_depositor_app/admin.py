import logging
from easyborrow_depositor_app.models import RequestData
from django.contrib import admin


log = logging.getLogger(__name__)


class RequestDataAdmin(admin.ModelAdmin):

    # list_display = [ 'created', 'uu_id', 'perceived_url_100', 'referrer_url', 'item_json', 'patron_json', 'ezb_db_id' ]
    list_display = [ 'created', 'uu_id', 'perceived_url_100', 'referrer_url', 'item_json_100', 'patron_json_100', 'ezb_db_id' ]

    def perceived_url_100( self, obj ):
        url = obj.perceived_url
        if len(obj.perceived_url) > 100:
            url = f'{obj.perceived_url[:97]}...'
        return url
    perceived_url_100.short_description = 'perceived url (100)'

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

    # def patron_json_100( self, obj ):
    #     patron_str = obj.patron_json
    #     if patron_str == None:
    #         patron_str = ''
    #     assert type(patron_str) == str
    #     log.debug( f'patron_str after initialization, ``{patron_str}``' )
    #     if len(obj.patron_json) > 100:
    #         patron_str = f'{obj.patron_json[:97]}...'
    #         log.debug( f'patron_str after length, exceeded, ``{patron_str}``' )
    #     return patron_str
    # patron_json_100.short_description = 'patron json (100)'

    readonly_fields = ( 'created', 'uu_id', 'ezb_db_id' )

    search_fields = [ 'created', 'uu_id', 'perceived_url', 'referrer_url', 'item_json', 'patron_json', 'ezb_db_id' ]

    date_hierarchy = 'created'

    save_on_top = True

    ## end class RequestDataAdmin()


# class RequestDataAdmin(admin.ModelAdmin):

#     list_display = [ 'project_name', 'slug', 'project_contact_email', 'score', 'modified' ]
#     list_filter = [
#         'project_contact_email',
#         'code_versioned',
#         'has_public_code_url',
#         'responsive',
#         'contains_lightweight_data_reporting',
#         'accessibility_check_run',
#         'data_discoverable',
#         'has_sitechecker_entry',
#         'framework_supported',
#         'https_enforced',
#         'admin_links_shib_protected',
#         'logs_rotated',
#         'patron_data_expiration_process',
#         'django_session_data_expired',
#         'emails_admin_on_error',
#         'vulnerabilities_fixed'
#     ]
#     ordering = [ 'project_name' ]

#     readonly_fields = ( 'created', 'modified', 'score' )

#     prepopulated_fields = { "slug": ("project_name",) }

#     fieldsets = (
#         ('Publicly Displayed', {
#             'classes': ('wide',),
#             'fields': (
#                 'project_name',
#                 'slug',
#                 'project_contact_email',
#                 'code_versioned',
#                 'has_public_code_url',
#                 'public_code_url',
#                 'responsive',
#                 'contains_lightweight_data_reporting',
#                 'accessibility_check_run',
#                 'data_discoverable',
#                 'has_sitechecker_entry',
#                 'modified',
#             )
#         }),
#         ('Non-Public Dates for above', {
#             'classes': ('wide',),
#             'fields': (
#                 'project_contact_email_CHECKED',
#                 'code_versioned_CHECKED',
#                 'has_public_code_url_CHECKED',
#                 'public_code_url_CHECKED',
#                 'responsiveness_CHECKED',
#                 'contains_lightweight_data_reporting_CHECKED',
#                 'accessibility_check_run_CHECKED',
#                 'data_discoverable_CHECKED',
#                 'has_sitechecker_entry_CHECKED',
#             ),
#         }),
#         ('Non-Public Security', {
#             'classes': ('wide',),
#             'fields': (
#                 'framework_supported',
#                 'framework_supported_CHECKED',
#                 'https_enforced',
#                 'https_enforced_CHECKED',
#                 'admin_links_shib_protected',
#                 'admin_links_shib_protected_CHECKED',
#                 'logs_rotated',
#                 'logs_rotated_CHECKED',
#                 'patron_data_expiration_process',
#                 'patron_data_expiration_process_CHECKED',
#                 'django_session_data_expired',
#                 'django_session_data_expired_CHECKED',
#                 'emails_admin_on_error',
#                 'emails_admin_on_error_CHECKED',
#                 'vulnerabilities_fixed',
#                 'vulnerabilities_fixed_CHECKED',
#             ),
#         }),
#         ('Non-Public Other', {
#             'fields': (
#                 'notes',
#                 'created',
#                 'score'
#             ),
#         }),
#     )

#     save_on_top = True

#     ## class RequestDataAdmin()


admin.site.register( RequestData, RequestDataAdmin )

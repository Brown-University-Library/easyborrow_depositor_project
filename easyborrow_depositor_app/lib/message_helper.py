import json, logging

from easyborrow_depositor_app.lib import common
from easyborrow_depositor_app.models import RequestData


log = logging.getLogger(__name__)


class MsgHlpr():

    def __init__( self ):
        self.req_data_obj = None

    def load_data_obj( self, uu_id ):
        try:
            self.req_data_obj = RequestData.objects.get( uu_id=uu_id )
            return None
        except:
            err = 'Problem accessing request-data.'
            log.exception( err )
            return err

    def build_problem_context( self, error_message, uu_id ):
        """ Preps context for problem display.
            Called by views.message() """
        assert type(error_message) == str
        assert type(uu_id) == str
        perceived_url = 'unavailable'
        perceived_ip = 'unavailable'
        patron_email = 'unavailable'
        try:
            self.load_data_obj( uu_id )
            patron_dct = json.loads( self.req_data_obj.patron_json )
            perceived_url = self.req_data_obj.perceived_url
            perceived_ip = json.loads( self.req_data_obj.referrer_json )['remote_addr']
            patron_email = patron_dct['shib_email']
        except:
            log.exception( "unable to load data-object when preparing error-context" )
        feedback_url = common.build_feedback_url( perceived_url, perceived_ip, patron_email )
        context = {
            'pattern_header': common.grab_pattern_header( feedback_url ),
            'error_message': error_message
        }
        log.debug( 'returning error context' )
        return context

    def prepare_context( self ):
        """ Preps context for request-received display.
            Called by views.message() """
        ( context, err ) = ( None, None )
        try:
            patron_dct = json.loads( self.req_data_obj.patron_json )
            item_dct = json.loads( self.req_data_obj.item_json )
            perceived_ip = json.loads( self.req_data_obj.referrer_json )['remote_addr']
            feedback_url = common.build_feedback_url( self.req_data_obj.perceived_url, perceived_ip, patron_dct['shib_email'] )
            submitted_message = {
                'firstname': patron_dct['shib_name_first'],
                'lastname': patron_dct['shib_name_last'],
                'title': item_dct['title'],
                'ezb_db_id': self.req_data_obj.ezb_db_id,
                'email': patron_dct['shib_email']
                }
            context = {
                'pattern_header': common.grab_pattern_header( feedback_url ),
                'submitted_message': submitted_message }
        except:
            err = 'Problem building submitted message.'
            log.exception( err )
        return( context, err )

    def build_submitted_message( self, firstname, lastname, title, ezb_db_id, email ):
        """ Prepares submitted message
            Called by prepare_context() """
        assert type(firstname) == str
        assert type(lastname) == str
        assert type(title) == str
        assert type(ezb_db_id) == str
        assert type(email) == str

        message = f'''
Greetings {firstname} {lastname},

We're getting the title '{title}' for you. You'll soon receive more information in an email.

Some information for your records:

- Title: '{title}'
- Your easyBorrow reference number: '{ezb_db_id}'
- Notification of arrival will be sent to email address: <{email}>

If you have any questions, contact the Library's Interlibrary Loan office at <interlibrary_loan@brown.edu> or call 401-863-2169.'''
        log.debug( 'ezb submitted message built' )
        return message

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



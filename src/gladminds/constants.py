TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
PROVIDERS = ['asc', 'dasc', 'dealer', 'helpdesk']

PROVIDER_MAPPING = {'dealer' : 'dealer/login.html',
                    'helpdesk' : 'service-desk/login.html'}

GROUP_MAPPING = {'dealers' : '/aftersell/dealer/',
                 'ascs' : '/aftersell/asc/',
                 'dascs' :'/aftersell/asc/',
                 'SDO' :'/aftersell/helpdesk/',
                 'SDM' : '/aftersell/helpdesk/'}

USER_GROUPS = ['dealers', 'ascs', 'dascs', 'SDO', 'SDM']

REDIRECT_USER = {'dealers' : '/aftersell/register/sa',
                 'ascs' : '/aftersell/register/asc',
                 'SDO' : '/aftersell/servicedesk/',
                 'SDM' : '/aftersell/servicedesk/'}

TEMPLATE_MAPPING = {'asc' :'portal/asc_registration.html',
                    'sa' :'portal/sa_registration.html',
                    'customer' : 'portal/customer_registration.html'}

ACTIVE_MENU = {'asc' : 'register_asc',
               'sa' : 'register_sa',
               'customer' : 'register_customer'}

FEEDBACK_STATUS = (('Open', 'Open'),
                   ('Closed', 'Closed'),
                   ('Resolved', 'Resolved'),
                   ('Progress', 'Progress'),
                   ('Pending', 'Pending'))

PRIORITY = (('Low', 'Low'),
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Urgent', 'Urgent'),)

FEEDBACK_TYPE = (('Problem', 'Problem'),
                 ('Question', 'Question'),
                 ('Feature', 'Feature'),
                 ('Request', 'Request'),
                 ('Suggestion', 'Suggestion'),)

USER_DESIGNATION = (('SDO', 'Owner'),
                    ('SDM', 'Manager'))

RATINGS = (('1', 'Glad'),
           ('2', 'Very Glad'),
           ('3', 'Not Glad'))

PROVIDERS = ['asc', 'dasc', 'dealer', 'desk']

PROVIDER_MAPPING = {
                             'dealer': 'dealer/login.html',
                             'desk': 'service-desk/login.html'
                             }

GROUP_MAPPING = {
                    'dealers' : '/aftersell/dealer/login',
                    'ascs' : '/aftersell/asc/login',
                    'dascs' :'/aftersell/asc/login',
                    'SDO' :'/aftersell/desk/login',
                    'SDM' : '/aftersell/desk/login'
                 }
USER_GROUPS = [ 'dealers', 'ascs', 'dascs', 'SDO', 'SDM']

REDIRECT_USER ={
                    'dealers' : '/aftersell/register/sa',
                    'ascs' : '/aftersell/register/asc',
                    'SDO' : '/aftersell/servicedesk/',
                    'SDM' : '/aftersell/servicedesk/'
                }

TEMPLATE_MAPPING = {    
                     'asc' :'portal/asc_registration.html',
                     'sa'  :'portal/sa_registration.html',
                     'customer' : 'portal/customer_registration.html'
                    }
ACTIVE_MENU ={
                'asc' : 'register_asc',
                'sa' : 'register_sa',
                'customer' : 'register_customer'
              }

FEEDBACK_STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Resolved', 'Resolved'),
        ('Progress', 'Progress'),
    )
PRIORITY = (
        ('Low', 'Low'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Urgent', 'Urgent'),
    )
FEEDBACK_TYPE = (
        ('Problem', 'Problem'),
        ('Question', 'Question'),
        ('Feature', 'Feature'),
        ('Request', 'Request'),
        ('Suggestion', 'Suggestion'),
    )

USER_DESIGNATION = (
                    ('SDO','Owner'),
                    ('SDM','Manager')
                    )
RATINGS = (
           ('1','Glad'),
           ('2','Very Glad'),
           ('3','Not Glad')
        )
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
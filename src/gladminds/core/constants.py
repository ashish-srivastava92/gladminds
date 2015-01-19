from gladminds.core.auth_helper import Roles

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_FORMAT = '%d-%m-%Y %H:%M' 

PAGINATION_LINKS = 3

RECORDS_PER_PAGE = ['5', '10', '25', '50']

BY_DEFAULT_RECORDS_PER_PAGE = RECORDS_PER_PAGE[0]

ALL = 'all'

PROVIDERS = ['asc', 'dasc', 'dealer', 'helpdesk']

PROVIDER_MAPPING = {
                    'dealer' : 'dealer/login.html',
                    'helpdesk' : 'service-desk/login.html'
                 }

GROUP_MAPPING = {
                Roles.DEALERS : '/aftersell/dealer/login',
                Roles.ASCS : '/aftersell/asc/login',
                Roles.DASCS :'/aftersell/asc/login',
                Roles.SDOWNERS :'/aftersell/helpdesk/login',
                Roles.SDMANAGERS : '/aftersell/helpdesk/login'
                }

USER_GROUPS = [ Roles.DEALERS, Roles.ASCS, Roles.DASCS, Roles.SDOWNERS, Roles.SDMANAGERS]

REDIRECT_USER ={
                 Roles.DEALERS : '/aftersell/register/asc',
                 Roles.ASCS : '/aftersell/register/sa',
                 Roles.SDOWNERS : '/aftersell/servicedesk/',
                 Roles.SDMANAGERS : '/aftersell/servicedesk/'
                }

TEMPLATE_MAPPING = {
                    'asc' :'portal/asc_registration.html',
                    'sa' :'portal/sa_registration.html',
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
        ('In Progress', 'In Progress'),
        ('Pending', 'Pending')
    )

PRIORITY = (
        ('Low', 'Low'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Urgent', 'Urgent'),
    )

FEEDBACK_TYPE = (('Problem', 'Problem'),
                 ('Question', 'Question'),
                 ('Feature Request', 'Feature Request'),
                 ('Suggestion', 'Suggestion'),)

SLA_PRIORITY = (('Low', 'Low'),
                ('Medium', 'Medium'),
                ('High', 'High'),
                ('Urgent', 'Urgent'),)

TIME_UNIT = (('mins', 'mins'),
             ('hrs', 'hrs'),
             ('days', 'days'),)

RATINGS = (
           ('1','Glad'),
           ('2','Very Glad'),
           ('3','Not Glad')
        )

ROOT_CAUSE = (('Data','Data'),
              ('Infrastructure','Infrastructure'),
              ('Bug','Bug'),
              ('New Requirement','New Requirement'),
              ('Network','Network'),
              ('Non-issue','Non-issue'),
              ('External System','External System'))

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('X', 'Other'),
)

SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)

FUEL_CHOICES = (
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('Other', 'Other'),
)

STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (
    3, 'Expired'), (4, 'In Progress'), (
       5, 'Exceeds Limit'), (6, 'Closed Old Fsc'))


COUPON_STATUS = dict((v, k) for k, v in dict(STATUS_CHOICES).items())

MAX_UCP_ALLOWED=10
MANDATORY_MECHANIC_FIELDS = ['first_name', 'date_of_birth', 'phone_number', 'shop_name', 'district', 'state', 'pincode', 'registered_by_distributor', 'image_url']

FORM_STATUS_CHOICES = (
                       ('Complete', 'Complete'),
                       ('Incomplete', 'Incomplete'),
                       )

FEED_TYPES = ['Dispatch Feed', 'Purchase Feed', 'Credit Note Feed', 'CDMS Feed']

STATUS_TO_NOTIFY = ['Approved', 'Rejected', 'Accepted', 'Shipped', 'Delivered']

REDEMPTION_STATUS = (
        ('Open', 'Open'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )

ASM_REDEMPTION_STATUS = (
        ('Open', 'Open'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

GP_REDEMPTION_STATUS = (
        ('Approved', 'Approved'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )

class FeedStatus():
    RECEIVED = 'Received'
    SENT = 'Sent'
    

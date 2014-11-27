import logging
import datetime

from gladminds.bajaj import models as models
from gladminds.core.exceptions import DataNotFoundError
from gladminds.core.utils import create_context, get_list_from_set, \
    get_start_and_end_date, set_wait_time, convert_utc_to_local_time, \
    get_time_in_seconds
from gladminds.core.managers import mail
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE, \
    TIME_FORMAT
from django.contrib.auth.models import Group, User
from gladminds.sqs_tasks import send_sms

logger = logging.getLogger('gladminds')

def get_feedbacks(user):
    group = user.groups.all()[0]
    if group.name == 'SDM':
        feedbacks = models.Feedback.objects.order_by('-created_date')
    if group.name == 'SDO':
        user_profile = models.UserProfile.objects.filter(user=user)
        servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile=user_profile[0])
        feedbacks = models.Feedback.objects.filter(
                        assignee=servicedesk_user[0]).order_by('-created_date')
    return feedbacks

def get_feedback(feedback_id, user):
    group = user.groups.all()[0]
    if group.name == 'SDO':
        user_profile = models.UserProfile.objects.filter(user=user)
        servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile=user_profile[0])
        return models.Feedback.objects.get(id=feedback_id, assignee=servicedesk_user[0])
    else:
        return models.Feedback.objects.get(id=feedback_id)

def get_servicedesk_users(designation):
    users = User.objects.filter(groups__name='sdo')
    user_list = models.UserProfile.objects.filter(user__in=users)
    servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile__in=user_list)
    return servicedesk_user

def get_comments(feedback_id):
    comments = models.Comment.objects.filter(feedback_object_id=feedback_id)
    return comments

def set_due_date(priority, feedback_obj):
    created_date = feedback_obj.created_date
    sla_obj = models.SLA.objects.get(priority=priority)
    resolution_time = sla_obj.resolution_time
    resolution_unit = sla_obj.resolution_unit
    reminder_time = sla_obj.reminder_time
    reminder_unit = sla_obj.reminder_unit
    total_seconds = get_time_in_seconds(reminder_time, reminder_unit)
    reminder_date = created_date + datetime.timedelta(seconds=total_seconds)
    total_seconds = get_time_in_seconds(resolution_time, resolution_unit)
    due_date = created_date + datetime.timedelta(seconds=total_seconds)
    reminder_date = due_date-reminder_date
    feedback_obj.reminder_date = due_date-reminder_date
    feedback_obj.save() 
    return due_date

def get_reporter_details(reporter, value="phone_number"):
    if value == "email":
        if reporter.email:
            return reporter.email
        else:
            return reporter.user_profile.user.email
    else:
        if reporter.phone_number:
            return reporter.phone_number
        else:
            return reporter.user_profile.phone_number
    
def save_update_feedback(feedback_obj, data, user, host):
    status = get_list_from_set(FEEDBACK_STATUS)
    comment_object = None
    assign_status = False
    pending_status = False
    reporter_email_id = get_reporter_details(feedback_obj.reporter,"email")
    reporter_phone_number = get_reporter_details(feedback_obj.reporter)
    #check if status is pending
    if feedback_obj.status == status[4]:
        pending_status = True
 
    if feedback_obj.assignee:
        assign_number = feedback_obj.assignee.user_profile.phone_number
    else:
        assign_number = None
    assign = feedback_obj.assignee
    if assign is None:
        assign_status = True
 
    if data['assign_to'] == '':
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
        feedback_obj.assignee = None
     
    else:
        if data['reporter_status'] == 'true':
            feedback_obj.previous_assignee = feedback_obj.assignee
            feedback_obj.assign_to_reporter = True
            feedback_obj.assignee = feedback_obj.reporter
            
        else:
            if data['assign_to'] :
                servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile__phone_number=data['assign_to'])
                feedback_obj.assignee = servicedesk_user[0]
                feedback_obj.assign_to_reporter = False
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
    #check if status is pending
    if data['status'] == status[4]:
        feedback_obj.pending_from = datetime.datetime.now()
    #check if status is progress
    if data['status'] == status[3]:
        feedback_obj.assignee = feedback_obj.previous_assignee
    #check if status is closed
    if data['status'] == status[1]:
        feedback_obj.closed_date = datetime.datetime.now()
    feedback_obj.save()
    if assign_status and feedback_obj.assignee:
        feedback_obj.assignee_created_date = datetime.datetime.now()
        feedback_obj.due_date = set_due_date(data['Priority'], feedback_obj)
        feedback_obj.save()
        context = create_context('INITIATOR_FEEDBACK_MAIL_DETAIL',
                                 feedback_obj)
        if reporter_email_id:
            mail.send_email_to_initiator_after_issue_assigned(context,
                                                         feedback_obj)
        else:
            logger.info("Reporter emailId not found.")
        send_sms('INITIATOR_FEEDBACK_DETAILS', reporter_phone_number,
                 feedback_obj)
 #check if status is resolved
    if feedback_obj.status == status[2]:
        servicedesk_obj_all = User.objects.filter(groups__name='sdm')
        feedback_obj.resolved_date = datetime.datetime.now()
        feedback_obj.resolved_date = datetime.datetime.now()
        feedback_obj.root_cause = data['rootcause']
        feedback_obj.resolution = data['resolution']
        feedback_obj.save()
        if reporter_email_id:
            context = create_context('INITIATOR_FEEDBACK_RESOLVED_MAIL_DETAIL',
                                  feedback_obj)
            mail.send_email_to_initiator_after_issue_resolved(context,
                                                          feedback_obj, host)
        else:
            logger.info("Reporter emailId not found.")
 
        context = create_context('TICKET_RESOLVED_DETAIL_TO_BAJAJ',
                                 feedback_obj)
        mail.send_email_to_bajaj_after_issue_resolved(context)
        context = create_context('TICKET_RESOLVED_DETAIL_TO_MANAGER',
                                 feedback_obj)
        mail.send_email_to_manager_after_issue_resolved(context,
                                                        servicedesk_obj_all[0])
        send_sms('INITIATOR_FEEDBACK_STATUS', reporter_phone_number,
                 feedback_obj)
  
    if pending_status:
        set_wait_time(feedback_obj)
 
    if data['comments']:
        comment_object = models.Comment(
                                        comment=data['comments'],
                                        user=user, created_date=datetime.datetime.now(),
                                        feedback_object=feedback_obj)
        comment_object.save()
 
    if feedback_obj.assignee:
        if assign_number != feedback_obj.assignee.user_profile.phone_number:
            context = create_context('ASSIGNEE_FEEDBACK_MAIL_DETAIL',
                                      feedback_obj)
            mail.send_email_to_assignee(context, feedback_obj)
            send_sms('SEND_MSG_TO_ASSIGNEE',
                     feedback_obj.assignee.user_profile.phone_number,
                     feedback_obj, comment_object)

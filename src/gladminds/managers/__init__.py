import logging
import datetime
from gladminds.aftersell.models import common as aftersell_common
from gladminds.exceptions import DataNotFoundError
from gladminds.utils import create_context, get_list_from_set,\
    get_start_and_end_date, set_wait_time, convert_utc_to_local_time
from gladminds import mail
from gladminds.sqs_tasks import send_sms
from gladminds.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    TIME_FORMAT

logger = logging.getLogger('gladminds')

def get_feedbacks(user):
    group = user.groups.all()[0]
    if group.name == 'SDM':
        feedbacks = aftersell_common.Feedback.objects.order_by('-created_date')
    if group.name == 'SDO':
        servicedesk_obj = aftersell_common.ServiceDeskUser.objects.filter(user=user)
        feedbacks = aftersell_common.Feedback.objects.filter(
                        assign_to=servicedesk_obj[0]).order_by('-created_date')
    return feedbacks


def get_feedback(feedback_id, user):
    group = user.groups.all()[0]
    if group.name == 'SDO':
        servicedesk_obj = aftersell_common.ServiceDeskUser.objects.filter(user=user)
        return aftersell_common.Feedback.objects.filter(id=feedback_id,assign_to=servicedesk_obj[0])
    else:
        return aftersell_common.Feedback.objects.filter(id=feedback_id)


def set_due_date(priority, created_date):
    sla_obj = aftersell_common.SLA.objects.get(priority=priority)
    resolution_time = sla_obj.resolution_time
    total_seconds = (resolution_time.hour * 3600) + (resolution_time.minute * 60) + (resolution_time.second)
    due_date = created_date + datetime.timedelta(seconds=total_seconds)
    return due_date

def save_update_feedback(feedback_obj, data, user,  host):
    comment_object = None
    assign_status = False
    pending_status = False
    if feedback_obj.status == 'Pending':
        pending_status = True

    if feedback_obj.assign_to:
        assign_number = feedback_obj.assign_to.phone_number
        previous_assignee = feedback_obj.assign_to
    else:
        assign_number = None
    if feedback_obj.status == 'Open':
        feedback_obj.due_date = set_due_date(data['Priority'], feedback_obj.created_date)
        feedback_obj.save()
    assign = feedback_obj.assign_to
    if assign is None:
        assign_status = True

    if data['Assign_To'] == '':
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
        feedback_obj.assign_to = None
    
    else:
        if data['reporter_status'] == 'true':
            feedback_obj.assign_to_reporter = True
            feedback_obj.assign_to = previous_assignee
        else:
            servicedesk_assign_obj = aftersell_common.ServiceDeskUser.objects.filter(
                                                            phone_number=data['Assign_To'])
            feedback_obj.assign_to = servicedesk_assign_obj[0]
            feedback_obj.assign_to_reporter = False
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
    if data['status'] == 'Pending':
        feedback_obj.pending_from = datetime.datetime.now()
    if data['status'] == 'Closed':
        feedback_obj.closed_date = datetime.datetime.now()
    feedback_obj.save()
    if assign_status and feedback_obj.assign_to:
        context = create_context('INITIATOR_FEEDBACK_MAIL_DETAIL',
                                 feedback_obj)
        if feedback_obj.reporter_email_id:
            mail.send_email_to_initiator_after_issue_assigned(context,
                                                         feedback_obj)
        else:
            logger.info("Reporter emailId not found.")
        send_sms('INITIATOR_FEEDBACK_DETAILS', feedback_obj.reporter,
                 feedback_obj)

    if feedback_obj.status == 'Resolved':
        servicedesk_obj_all = aftersell_common.ServiceDeskUser.objects.filter(
                                                    designation='SDM')
        feedback_obj.resolved_date = datetime.datetime.now()
        feedback_obj.resolved_date = datetime.datetime.now()
        feedback_obj.root_cause = data['rootcause']
        feedback_obj.resolution = data['resolution']
        feedback_obj.save()
        if feedback_obj.reporter_email_id:
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
        send_sms('INITIATOR_FEEDBACK_STATUS', feedback_obj.reporter,
                 feedback_obj)

    if pending_status:
        set_wait_time(feedback_obj)

    if data['comments']:
        comment_object = aftersell_common.Comments(
                                        comments=data['comments'],
                                        user=user, created_date=datetime.datetime.now(),
                                        feedback_object=feedback_obj)
        comment_object.save()

    if feedback_obj.assign_to:
        if assign_number != feedback_obj.assign_to.phone_number:
            context = create_context('ASSIGNEE_FEEDBACK_MAIL_DETAIL',
                                      feedback_obj)
            mail.send_email_to_assignee(context, feedback_obj)
            send_sms('SEND_MSG_TO_ASSIGNEE',
                     feedback_obj.assign_to.phone_number,
                     feedback_obj,  comment_object)

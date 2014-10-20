from datetime import datetime

from gladminds.bajaj import models as common
from gladminds.core.exceptions import DataNotFoundError
from gladminds.core.utils import create_context, get_list_from_set,\
    get_start_and_end_date, set_wait_time
from gladminds.core.managers import mail
from gladminds.core.cron_jobs.sqs_tasks import send_sms
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    TIME_FORMAT


def get_feedbacks(user):
    group = user.groups.all()[0]
    if group.name == 'SDM':
        feedbacks = common.Feedback.objects.order_by('-created_date')
    if group.name == 'SDO':
        servicedesk_obj = common.ServiceDeskUser.objects.filter(user=user)
        feedbacks = common.Feedback.objects.filter(
                        assign_to=servicedesk_obj[0]).order_by('-created_date')
    return feedbacks


def get_feedback(feedback_id):
    return common.Feedback.objects.get(id=feedback_id)


def get_servicedesk_users(**filters):
    return common.ServiceDeskUser.objects.filter(**filters)


def save_update_feedback(feedback_obj, data, user,  host):
    comment_object = None
    assign_status = False
    pending_status = False
    if feedback_obj.status == 'Pending':
        pending_status = True

    if feedback_obj.assign_to:
        assign_number = feedback_obj.assign_to.phone_number
    else:
        assign_number = None

    assign = feedback_obj.assign_to

    if assign is None:
        assign_status = True

    if data['Assign_To'] == 'None':
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
    else:
        servicedesk_assign_obj = common.ServiceDeskUser.objects.filter(
                                                            phone_number=data['Assign_To'])
        feedback_obj.assign_to = servicedesk_assign_obj[0]
        feedback_obj.status = data['status']
        feedback_obj.priority = data['Priority']
        feedback_obj.modified_date = datetime.now()
    if data['status'] == 'Pending':
        feedback_obj.pending_from = datetime.now()
    if data['status'] == 'Closed':
        feedback_obj.closed_date = datetime.now()
    feedback_obj.save()
    if assign_status and feedback_obj.assign_to:
        context = create_context('INITIATOR_FEEDBACK_MAIL_DETAIL',
                                 feedback_obj)
        mail.send_email_to_initiator_after_issue_assigned(context,
                                                         feedback_obj)
        send_sms('INITIATOR_FEEDBACK_DETAILS', feedback_obj.reporter,
                 feedback_obj)

    if feedback_obj.status == 'Resolved':
        servicedesk_obj_all = common.ServiceDeskUser.objects.filter(
                                                    designation='SDM')
        feedback_obj.resolved_date = datetime.now()
        feedback_obj.resolved_date = datetime.now()
        feedback_obj.root_cause = data['rootcause']
        feedback_obj.resolution = data['resolution']
        feedback_obj.save()
        context = create_context('INITIATOR_FEEDBACK_RESOLVED_MAIL_DETAIL',
                                  feedback_obj)
        mail.send_email_to_initiator_after_issue_resolved(context,
                                                          feedback_obj, host)
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
        comment_object = common.Comments(
                                        comments=data['comments'],
                                        user=user, created_date=datetime.now(),
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

    if feedback_obj.resolved_date:
        start_date = feedback_obj.created_date
        feedback_end_date = common.Feedback.objects.get(
                                                    id=feedback_obj.id)
        end_date = feedback_end_date.resolved_date
        start_date, end_date = get_start_and_end_date(start_date,
                                                     end_date, TIME_FORMAT)
        if start_date > end_date:
            raise ValueError('Invalid resolved date.\
             Resolved date should be after the created date')
        else:
            wait = end_date - start_date
            wait_time = float(wait.days) + float(wait.seconds) / float(86400)
            wait_final = float(wait_time) - feedback_obj.wait_time
            feedback_obj.wait_time = wait_final
            feedback_obj.save()

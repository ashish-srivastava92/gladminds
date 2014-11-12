import logging
from datetime import datetime, timedelta
from django import template
from django.conf import settings
from django.db.models import get_app, get_models
from django.http.response import HttpResponse
from gladminds.aftersell.models import logs

logger = logging.getLogger("gladminds")

def check_db_connection():
    health_status = 'success'
    reason = 'Connected to RDS'
    try:
        app_list = [get_app('gladminds'), get_app('afterbuy'), get_app('aftersell')]
        for every_app in app_list:
            for model in get_models(every_app):
                model.objects.filter()
    except Exception as ex:
        reason = "Error on RDS Connection : %s" % ex
        health_status = 'error'
    return {'health_status' : health_status, 'reason' : reason}

def check_sms_errors():
    health_status = 'success'
    reason = 'All SMS are passed'
    try:
        today = datetime.now()
        start_date = today - timedelta(hours=settings.SMS_HEALTH_CHECK_INTERVAL)
        end_date = today
        audit_logs = logs.AuditLog.objects.filter(action='failure', date__range=(start_date, end_date))
        if audit_logs:
            health_status = 'error'
            reason = 'On last {0} hours, {1} SMS Failed'.format(settings.SMS_HEALTH_CHECK_INTERVAL,
                                                                len(audit_logs))
    except Exception as ex:
        reason = "Error on SMS Health Check : %s" % ex
        health_status = 'error'
    return {'health_status' : health_status, 'reason' : reason}

def check_feed_errors():
    health_status = 'success'
    reason = 'All Feed are passed'
    try:
        today = datetime.now()
        start_date = today - timedelta(hours=settings.FEED_HEALTH_CHECK_INTERVAL)
        end_date = today
        feeds_logs = logs.DataFeedLog.objects.filter(failed_data_count__gt=0,
                                                     timestamp__range=(start_date, end_date))
        if feeds_logs:
            health_status = 'error'
            failed_data_count = 0
            for failed_feed in feeds_logs:
                failed_data_count += failed_feed.failed_data_count
            health_status = 'error'
            reason = 'On last {0} hours, {1} Feeds Failed'.format(settings.SMS_HEALTH_CHECK_INTERVAL,
                                                                  len(failed_data_count))
    except Exception as ex:
        reason = "Error on Feed Health Check : %s" % ex
        health_status = 'error'    
    return {'health_status' : health_status, 'reason' : reason}

def get_health_check_res():
    result = {}
    for fn in [check_db_connection, check_sms_errors, check_feed_errors]:
        try:
            result[fn.__name__] = fn()
        except Exception as e:
            result[fn.__name__]
            logger.info(e)
    return result
    
def gt_hlth_chk(request):
    for res_name, res_status in get_health_check_res().iteritems():
        if res_status['health_status'] == 'error':
            return HttpResponse(status=500)
    return HttpResponse(status=200)
    
def health_check_view(request):
    result = get_health_check_res()
    
    import socket
    result['machine_ip'] = socket.gethostbyname(socket.gethostname()) 
    
    html_template = open(settings.TEMPLATE_DIR + '/health-check/health-check.html')
    t = template.Template(html_template.read())
    c = template.Context(result)
    return HttpResponse(t.render(c))

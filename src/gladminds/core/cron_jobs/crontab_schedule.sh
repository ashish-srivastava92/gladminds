sudo crontab -r
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py expire_service_coupon gladminds-qa2") | sudo  crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py export_customer_reg_to_sap gladminds-qa2") | sudo  crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_report_mail_for_feed gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_reminder gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py import_data gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_schedule_reminder gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py delete_unused_otp gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_mail_for_feed_failure gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_mail_for_customer_phone_number_update gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_vin_sync_feed_details gladminds-qa2") | sudo crontab
sudo crontab -l | (cat;echo "05 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py update_coupon_history_data gladminds-qa2") | sudo crontab

sudo crontab -l | (cat;echo "00 */4 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py export_coupon_redeem_to_sap gladminds-prod2") | sudo  crontab
sudo crontab -l | (cat;echo "00 15 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py export_customer_reg_to_sap gladminds-prod2") | sudo  crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py expire_service_coupon gladminds-prod2") | sudo  crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_report_mail_for_feed gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_reminder gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py import_data gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_schedule_reminder gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py delete_unused_otp gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_mail_for_feed_failure gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_mail_for_customer_phone_number_update gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "00 19 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py send_vin_sync_feed_details gladminds-prod2") | sudo crontab
sudo crontab -l | (cat;echo "05 00 * * *  python /opt/app/gladminds/src/gladminds/core/cron_jobs/trigger_sqs_tasks.py update_coupon_history_data gladminds-prod2") | sudo crontab

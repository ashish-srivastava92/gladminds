sudo crontab -r
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py expire_service_coupon gladminds-qa") | sudo  crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py export_coupon_redeem_to_sap gladminds-qa") | sudo  crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_report_mail_for_feed gladminds-qa") | sudo crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_reminder gladminds-qa") | sudo crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  import_data gladminds-qa") | sudo crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py send_schedule_reminder gladminds-qa") | sudo crontab
sudo crontab -l | (cat;echo "00 16 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py delete_unused_otp gladminds-qa") | sudo crontab

sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py expire_service_coupon gladminds-prod") | sudo  crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py export_coupon_redeem_to_sap gladminds-prod") | sudo  crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_report_mail_for_feed gladminds-prod") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_reminder gladminds-prod") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  import_data gladminds-prod") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py send_schedule_reminder gladminds-prod") | sudo crontab
sudo crontab -l | (cat;echo "00 00 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py delete_unused_otp gladminds-prod") | sudo crontab

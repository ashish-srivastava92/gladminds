sudo crontab -r
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py expire_service_coupon") | sudo  crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py export_coupon_redeem_to_sap") | sudo  crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_report_mail_for_feed") | sudo crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  send_reminder") | sudo crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py  import_data") | sudo crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py send_schedule_reminder") | sudo crontab
sudo crontab -l | (cat;echo "0 0 * * *  python /opt/app/gladminds/src/gladminds/scheduler.py delete_unused_otp") | sudo crontab

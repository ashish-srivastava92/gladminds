chmod -R 704 /var/log/httpd/
mkdir -p  /var/log/httpd/gladminds/
echo "" >> /var/log/httpd/gladminds/sql.log
echo "" >> /var/log/httpd/gladminds/gladminds.log
echo "" >> /var/log/httpd/gladminds/afterbuy.log
echo "" >> /var/log/httpd/gladminds/test_case.log
chmod -R o+rwx /var/log/httpd/gladminds/

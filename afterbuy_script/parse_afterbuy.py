#!/usr/bin/python
import sys

form_url = sys.argv[1]
ip_address = sys.argv[1]

ip_address = 'var ipaddress = "%s";' % ip_address
form_url = 'action="%s"' % form_url


print form_url, ip_address

fp = open('afterbuy/www/index.html', 'r')
file_content = fp.read().replace('action="http://localhost:8000/gm"', form_url)
fp.close()
fp = open('afterbuy/www/index.html', 'w')
fp.write(file_content)
fp.close()

fp = open('afterbuy/www/js/inc.js', 'r')
file_content = fp.read().replace('var ipaddress = "http://localhost:8000/gm/";', ip_address)
fp.close()
fp = open('afterbuy/www/js/inc.js', 'w')
fp.write(file_content)
fp.close()

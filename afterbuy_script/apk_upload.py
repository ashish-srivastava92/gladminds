import os
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

form_url = sys.argv[1]


def upload_to_s3(app_name, app_path):
    c = S3Connection('AKIAIL7IDCSTNCG2R6JA', \
                     '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A')
    b = c.get_bucket('afterbuy')
    k = Key(b)
    k.key = app_name
    k.set_contents_from_filename(app_path, policy='public-read')


if form_url == "https://api-qa.gladmindsplatform.co/gm/":
    for file_info in [("android", 'apk'), ("ios", 'ipa')]:
        app_name = "qa_{0}_afterbuy.{1}".format(file_info[0], file_info[1])
        app_path = "afterbuy_script/{0}".format(app_name)
        upload_to_s3(app_name, app_path)
        os.remove(app_path)
else:
    for file_info in [("android", 'apk'), ("ios", 'ipa')]:
        app_name = "prod_{0}_afterbuy.{1}".format(file_info[0], file_info[1])
        app_path = "afterbuy_script/{0}".format(app_name)
        upload_to_s3(app_name, app_path)
        os.remove(app_path)

import os
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

form_url = sys.argv[1]

if form_url == "https://api-qa.gladmindsplatform.co/gm/":
    app_path = "afterbuy_script/qa_afterbuy.apk"
    app_name = "qa_afterbuy.apk"
else:
    app_path = "afterbuy_script/prod_afterbuy.apk"
    app_name = "prod_afterbuy.apk"

c = S3Connection('AKIAIL7IDCSTNCG2R6JA', \
                 '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A')
b = c.get_bucket('afterbuy')
k = Key(b)
k.key = app_name

k.set_contents_from_filename(app_path, policy='public-read')
os.remove(app_path)

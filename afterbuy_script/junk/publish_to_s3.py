from boto.s3.connection import S3Connection
from boto.s3.key import Key
c = S3Connection('AKIAIL7IDCSTNCG2R6JA', \
                 '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A')
b = c.get_bucket('afterbuy')
for i in b.list():
    print i
k = Key(b)
k.key = 'testfile21211'
k.set_contents_from_filename('test2323.txt', policy='public-read')

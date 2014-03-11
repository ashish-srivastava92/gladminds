import os
import boto
from boto.s3.key import Key
import sys
from subprocess import Popen


failed = open('failers', 'w')
machine = sys.argv[1]


def uploadResultToS3(awsid, awskey, bucket, source_folder):
    c = boto.connect_s3(awsid, awskey)
    b = c.get_bucket(bucket)
    k = Key(b)
    
    for path, dir, files in os.walk(source_folder):
        print "sending :", path, 
        print dir, files
        for upload_file in files:
            relpath = os.path.relpath(os.path.join(path, upload_file))
            if not b.get_key(relpath):
                k.key = relpath
                k.set_contents_from_filename(relpath)
                try:
                    k.set_acl('public-read')
                except:
                    failed.write(relpath + ', ')
    failed.close()

uploadResultToS3('AKIAIL7IDCSTNCG2R6JA', '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A',\
                  "afterbuy", '%s' % machine)

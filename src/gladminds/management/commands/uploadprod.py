from django.core.management.base import BaseCommand
from gladminds import settings
import MySQLdb
import boto
from boto.s3.key import Key
import csv
import os
from boto.s3.connection  import S3Connection

db = MySQLdb.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWORD,"bajajcv")
cursor = db.cursor()

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_acc_fit_data()
        
    def upload_acc_fit_data(self):

        S3_ID = settings.S3_ID
        S3_KEY = settings.S3_KEY
        connection = S3Connection(S3_ID, S3_KEY)
        AWS_STORAGE_BUCKET_NAME = 'gladminds'
        bucket = connection.get_bucket(AWS_STORAGE_BUCKET_NAME)
        k1=Key(bucket)
        k1.key = "acc_data.csv"
        
        fp = open('acc_data.csv','w')
        
        query1 = "SELECT 'Mechanic ID','Permanent ID','First Name', 'District', 'Phone Number', 'State Name','Distributer ID', 'Unique Part Code', 'Points','Date of SMSed' UNION ALL SELECT  mem.mechanic_id, mem.permanent_id, mem.first_name, mem.district, mem.phone_number, st.state_name, distr.distributor_id, spart.unique_part_code, pp.points, acre.created_date FROM gm_accumulationrequest AS acre LEFT OUTER JOIN gm_member mem ON mem.id = acre.member_id LEFT OUTER JOIN gm_distributor AS distr ON mem.registered_by_distributor_id = distr.id LEFT OUTER JOIN gm_state AS st ON mem.state_id = st.id LEFT OUTER JOIN gm_accumulationrequest_upcs AS accup ON acre.transaction_id = accup.accumulationrequest_id LEFT OUTER JOIN gm_sparepartupc AS spart ON accup.sparepartupc_id = spart.id LEFT OUTER JOIN gm_sparepartmasterdata AS mdata ON mdata.id = spart.part_number_id LEFT OUTER JOIN gm_sparepartpoint AS pp ON mdata.id = pp.part_number_id WHERE mem.form_status =  'complete' GROUP BY acre.transaction_id ";
        
        query2 = "SELECT 'Mechanic ID','Permanent ID','First Name', 'District', 'Phone Number', 'State Name','Distributer ID', 'Unique Part Code',  'Part Number', 'Description','Points','Date of SMSed' UNION ALL SELECT  mem.mechanic_id, mem.permanent_id, mem.first_name, mem.district, mem.phone_number, st.state_name, distr.distributor_id, spart.unique_part_code,mdata.part_number, mdata.description, pp.points, acre.created_date FROM gm_accumulationrequest AS acre LEFT OUTER JOIN gm_member mem ON mem.id = acre.member_id LEFT OUTER JOIN gm_distributor AS distr ON mem.registered_by_distributor_id = distr.id LEFT OUTER JOIN gm_state AS st ON mem.state_id = st.id LEFT OUTER JOIN gm_accumulationrequest_upcs AS accup ON acre.transaction_id = accup.accumulationrequest_id LEFT OUTER JOIN gm_sparepartupc AS spart ON accup.sparepartupc_id = spart.id LEFT OUTER JOIN gm_sparepartmasterdata AS mdata ON mdata.id = spart.part_number_id LEFT OUTER JOIN gm_sparepartpoint AS pp ON mdata.id = pp.part_number_id WHERE mem.form_status =  'complete' GROUP BY acre.transaction_id ";
        
        cursor.execute(query1)
        rows1 = cursor.fetchall()
        myFile = csv.writer(fp)
        
        for r in rows1:
                myFile.writerow(r)
        
        fp.close()
        
        s3_key = Key(bucket)
        
        s3_key.key = 'acc_data.csv'
        s3_key.set_contents_from_filename('acc_data.csv')
        
        s3_key.set_acl('public-read')
        path = s3_key.generate_url(expires_in=0, query_auth=False)
        
        k2= Key(bucket)
        k2.key = "fitment_data.csv"
        
        fp1 = open('fitment_data.csv','w')
        
        cursor.execute(query2)
        rows2 = cursor.fetchall()
        myFile2 = csv.writer(fp1)
        
        for r1 in rows2:
                myFile2.writerow(r1)
        
        fp1.close()
        
        s3_key = Key(bucket)
        
        s3_key.key = 'fitment_data.csv'
        s3_key.set_contents_from_filename('fitment_data.csv')
        s3_key.set_acl('public-read')
        path = s3_key.generate_url(expires_in=0, query_auth=False)
        db.close()

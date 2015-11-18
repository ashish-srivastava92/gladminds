import csv
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from gladminds.core.model_fetcher import get_model
import os
APP='bajajcv'

class Command(BaseCommand):
    
    def mobile_format(self, phone_number):
        return '+91' + phone_number[-10:]

    def handle(self, *args, **options):
#         self.upload_part_master_data()
#         self.upload_part_upc_data()
#         self.upload_part_point_data()
        self.upload_missing_upcs()

    def empty_to_none(self, value):
        if value=='':
            return None
        else:
            return int(value)

    def upload_part_master_data(self):
        '''Upload data of the part master'''
        print "Started uploading part master..."
        file_list = ['PART_MASTER_DATA.csv']
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_type = get_model('ProductType', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['desc'] = row_list[1].strip()

                    temp['type'] = row_list[2].strip()
                    temp['category']=row_list[3].strip()
                    temp['segment'] = row_list[4].strip()
                    temp['model'] = row_list[5].strip()
                    temp['supplier'] = row_list[6].strip()
                    spare_list.append(temp)
        for spare in spare_list:
            spare_object = spare_master.objects.filter(part_number=spare['part_no']).using(APP)
            if not spare_object:
                spare_type_object = spare_type.objects.filter(product_type=spare['type']).using(APP)
                if not spare_type_object:
                    spare_type_object = spare_type(product_type=spare['type'])
                    spare_type_object.save(using=APP)
                else:
                    spare_type_object = spare_type_object[0]
                spare_object = spare_master(
                                            product_type=spare_type_object,
                                            part_number = spare['part_no'],
                                            part_model = spare['model'],
                                            description = spare['desc'],
                                            category = spare['category'],
                                            segment_type = spare['segment'],
                                            supplier = spare['supplier']
                                )
                spare_object.save(using=APP)
    
    def upload_part_upc_data(self):
        '''Upload data of the part UPC'''
        print "Started uploading part upc..."
        file_list = ['PART_UPC_DATA.csv']
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_upc = get_model('SparePartUPC', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['UPC'] = (row_list[1].strip()).upper()
                    spare_list.append(temp)
        for spare in spare_list:
            spare_object = spare_upc.objects.filter(unique_part_code = spare['UPC']).using(APP)
            if not spare_object:
                spare_master_object = spare_master.objects.filter(part_number=spare['part_no']).using(APP)
                
                spare_object = spare_upc(
                                            part_number=spare_master_object[0],
                                            unique_part_code = spare['UPC'])
                spare_object.save(using=APP)

    def upload_part_point_data(self):
        '''Upload data of the part point'''
        print "Started uploading part points..."
        file_list = ['PART_POINTS_DATA.csv']
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_part = get_model('SparePartPoint', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['MRP'] = self.empty_to_none(row_list[1].strip())
                    temp['valid_from'] = datetime.datetime.strptime(row_list[2].strip(), '%d/%m/%Y')
                    temp['valid_to'] = datetime.datetime.strptime(row_list[3].strip(), '%d/%m/%Y')
                    temp['territory'] = row_list[4].strip()
                    temp['price'] = self.empty_to_none(row_list[5].strip())
                    temp['points'] = row_list[6].strip()
                    spare_list.append(temp)
        for spare in spare_list:
            spare_master_object = spare_master.objects.filter(part_number=spare['part_no']).using(APP)
            spare_object = spare_part.objects.filter(part_number=spare_master_object[0],
                                                     territory=spare['territory']).using(APP)
            if not spare_object:
                spare_object = spare_part(part_number = spare_master_object[0],
                                          points = spare['points'],
                                          price = spare['price'],
                                          MRP = spare['MRP'],
                                          valid_from = spare['valid_from'],
                                          valid_till = spare['valid_to'],
                                          territory = spare['territory'])
                spare_object.save(using=APP)


    def upload_missing_upcs(self):
            file_list = ['MISSING_UPCS_DATA.csv']
            spare_master = get_model('SparePartMasterData', APP)
            member = get_model('Member', APP)
            acc = get_model('AccumulationRequest', APP)
            spare_part_points = get_model('SparePartPoint', APP)
            spare_part_upc = get_model('SparePartUPC', APP)
            upc_part_list = []
            spare_list = []
            for i in range(0, 1):
                with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
                    upc_reader = csv.reader(csvfile, delimiter=',')
                    next(upc_reader)
                    for row_list in upc_reader:
                        temp ={}
                        temp['date'] = row_list[0].strip()
                        tokens = row_list[1].strip().split(',')#split("','")
                        temp['data'] = tokens
                        temp['phone'] = row_list[2].strip()
                        temp['phone'] = self.mobile_format(row_list[2].strip())
                        spare_list.append(temp)
            for spare in spare_list:
                points_list = []
                users_points_new = []
                users_points_old = 0
                get_member = member.objects.filter(phone_number=spare['phone']).using(APP)
                
                if get_member:    ##if len(get_member) > 0: changed to get_member
                    user_total_points  = get_member[0].total_points
                    users_points_old = ( int(user_total_points))
                        
                for data in spare['data']:
                    spare_master_object = spare_part_upc.objects.filter(unique_part_code = data, is_used=False).using(APP)
                    if spare_master_object:    #if len(spare_master_object) > 0:
                        spare_points_data = spare_part_points.objects.filter(part_number=spare_master_object[0]).using(APP)
                        if len(spare_points_data) > 0:
                            points_list.append( int (spare_points_data[0].points) )
                        else:
                            points_list.append(0)
                    
                        if get_member and spare_points_data:     #if len(get_member) > 0 and len(spare_points_data) > 0:
                            update_status = spare_part_upc.objects.filter(unique_part_code = data, is_used=False).using(APP)
                            for update in update_status:
                                update.is_used=True
                                update.save(using=APP)
                            
                        if get_member:                 #if len(get_member) > 0: changed to get_member
                            if len(spare_points_data) > 0:
                                updated_point = user_total_points+spare_points_data[0].points 
                                users_points_new.append(updated_point)
                                user_total_points = updated_point
                                
                                mechanic_id = member.objects.using(APP).get(id=get_member[0].id)
                                acc_request_update = acc( points = spare_points_data[0].points,
                                                           total_points = updated_point,
                                                           member = mechanic_id
                                                           )
                                acc_request_update.save(using=APP)
                                
                            else:
                                updated_point = user_total_points
                                users_points_new.append(updated_point)
                                user_total_points = updated_point
                            
                spare['received_points'] = points_list
                user_final_point = 0
                user_old_final_point = 0
                
                if users_points_new :    #if len(users_points_new) > 0:
                    user_final_point = users_points_new[len(users_points_new) -1]
                    mechanic_id = member.objects.using(APP).get(id=get_member[0].id)
                    mechanic_id.total_points = user_final_point
                    mechanic_id.save()
                    
                spare['total_points_new'] = user_final_point
                if users_points_old > 0:
                    user_old_final_point  = users_points_old
                spare['total_points_old'] = user_old_final_point
                        
            file_list = ['POINT_FOR_MISSING_UPCS.csv']
            with open(settings.PROJECT_DIR + '/upload_data/' +  file_list[0], 'w') as f:
                    writer = csv.writer(f)
                    header = ['date', 'phone','data','received_points', 'total_points_old', 'total_point_new']
                    writer.writerow(header)
                    for data in spare_list:
                        rows = []
                        rows.append(data['date'])
                        rows.append(data['phone'])
                        rows.append(data['data'])
                        rows.append(data['received_points'])
                        rows.append(data['total_points_old'])
                        rows.append(data['total_points_new'])
                        writer.writerow(rows)

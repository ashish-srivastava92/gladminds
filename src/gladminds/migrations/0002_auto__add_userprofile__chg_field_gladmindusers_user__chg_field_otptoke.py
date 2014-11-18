# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'gladminds_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('profile_pic', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('gladminds', ['UserProfile'])


        # Changing field 'GladMindUsers.user'
        db.alter_column(u'gladminds_gladmindusers', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gladminds.UserProfile'], unique=True, null=True))

        # Changing field 'OTPToken.user'
        db.alter_column(u'gladminds_otptoken', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gladminds.UserProfile'], null=True))

    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'gladminds_userprofile')


        # Changing field 'GladMindUsers.user'
        db.alter_column(u'gladminds_gladmindusers', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True))

        # Changing field 'OTPToken.user'
        db.alter_column(u'gladminds_otptoken', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    models = {
        'aftersell.registereddealer': {
            'Meta': {'object_name': 'RegisteredDealer'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'dependent_on': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'dealer'", 'max_length': '10'})
        },
        'aftersell.serviceadvisor': {
            'Meta': {'object_name': 'ServiceAdvisor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'service_advisor_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gladminds.branddata': {
            'Meta': {'object_name': 'BrandData'},
            'brand_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'brand_image_loc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'brand_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pk_brand_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'gladminds.coupondata': {
            'Meta': {'object_name': 'CouponData'},
            'actual_kms': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'actual_service_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'extended_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mark_expired_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sa_phone_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.ServiceAdvisor']", 'null': 'True', 'blank': 'True'}),
            'schedule_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'servicing_dealer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.RegisteredDealer']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'unique_service_coupon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '215'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'valid_kms': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'vin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.ProductData']"})
        },
        'gladminds.customertempregistration': {
            'Meta': {'object_name': 'CustomerTempRegistration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_customer_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'product_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.ProductData']", 'null': 'True', 'blank': 'True'}),
            'product_purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'sent_to_sap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tagged_sap_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'temp_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'gladminds.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'template_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'gladminds.gladmindusers': {
            'Meta': {'object_name': 'GladMindUsers'},
            'accepted_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '215'}),
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'gladmind_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 17, 0, 0)'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb_url': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gladminds.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'gladminds.messagetemplate': {
            'Meta': {'object_name': 'MessageTemplate'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'template_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'gladminds.otptoken': {
            'Meta': {'object_name': 'OTPToken'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'gladminds.productdata': {
            'Meta': {'object_name': 'ProductData'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 17, 0, 0)', 'null': 'True'}),
            'customer_phone_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.GladMindUsers']", 'null': 'True', 'blank': 'True'}),
            'customer_product_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.RegisteredDealer']", 'null': 'True', 'blank': 'True'}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_loc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'insurance_yrs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_loc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 17, 0, 0)'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'product_purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.ProductTypeData']", 'null': 'True', 'blank': 'True'}),
            'purchased_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sap_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'seller_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'seller_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'veh_reg_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'vin': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'warranty_loc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'warranty_yrs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'gladminds.productinsuranceinfo': {
            'Meta': {'object_name': 'ProductInsuranceInfo'},
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'insurance_brand_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'insurance_brand_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'insurance_email': ('django.db.models.fields.EmailField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'insurance_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'blank': 'True'}),
            'premium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.ProductData']"})
        },
        'gladminds.producttypedata': {
            'Meta': {'object_name': 'ProductTypeData'},
            'brand_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.BrandData']"}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'product_image_loc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'product_type_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'warranty_email': ('django.db.models.fields.EmailField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'warranty_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'gladminds.productwarrantyinfo': {
            'Meta': {'object_name': 'ProductWarrantyInfo'},
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'blank': 'True'}),
            'premium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.ProductData']"}),
            'warranty_brand_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'warranty_brand_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'gladminds.sasaveform': {
            'Meta': {'object_name': 'SASaveForm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'gladminds.serviceadvisorcouponrelationship': {
            'Meta': {'object_name': 'ServiceAdvisorCouponRelationship'},
            'dealer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.RegisteredDealer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_advisor_phone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.ServiceAdvisor']"}),
            'unique_service_coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.CouponData']"})
        },
        'gladminds.sparesdata': {
            'Meta': {'object_name': 'SparesData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spare_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.BrandData']"}),
            'spare_contact': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'spare_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'gladminds.uploadproductcsv': {
            'Meta': {'object_name': 'UploadProductCSV'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_brand_feed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'upload_coupon_redeem_feed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'upload_dealer_feed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'upload_product_dispatch_feed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'upload_product_purchase_feed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        'gladminds.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['gladminds']
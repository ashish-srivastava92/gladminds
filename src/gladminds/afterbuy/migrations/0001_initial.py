# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Industry'
        db.create_table(u'afterbuy_industry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['Industry'])

        # Adding model 'Brand'
        db.create_table(u'afterbuy_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Industry'])),
        ))
        db.send_create_signal('afterbuy', ['Brand'])

        # Adding model 'BrandProductCategory'
        db.create_table(u'afterbuy_brandproductcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Brand'])),
        ))
        db.send_create_signal('afterbuy', ['BrandProductCategory'])

        # Adding model 'ProductType'
        db.create_table(u'afterbuy_producttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('afterbuy', ['ProductType'])

        # Adding model 'Consumer'
        db.create_table(u'afterbuy_consumer', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('consumer_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(default='guest.png', max_length=200)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('accepted_terms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tshirt_size', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['Consumer'])

        # Adding model 'UserProduct'
        db.create_table(u'afterbuy_userproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consumer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Brand'])),
            ('nick_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.ProductType'])),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('brand_product_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['UserProduct'])

        # Adding model 'ProductSupport'
        db.create_table(u'afterbuy_productsupport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['ProductSupport'])

        # Adding model 'RegistrationCertificate'
        db.create_table(u'afterbuy_registrationcertificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('registration_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('registration_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chassis_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('engine_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('relation_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('registration_upto', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('model_year', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('fuel', self.gf('django.db.models.fields.CharField')(default='Petrol', max_length=15)),
            ('cylinder', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cc', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['RegistrationCertificate'])

        # Adding model 'ProductInsuranceInfo'
        db.create_table(u'afterbuy_productinsuranceinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('agency_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('policy_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('premium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('agency_contact', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('insurance_type', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('nominee', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('vehicle_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('is_expired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('afterbuy', ['ProductInsuranceInfo'])

        # Adding model 'ProductWarrantyInfo'
        db.create_table(u'afterbuy_productwarrantyinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('policy_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, blank=True)),
            ('premium', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['ProductWarrantyInfo'])

        # Adding model 'PollutionCertificate'
        db.create_table(u'afterbuy_pollutioncertificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('pucc_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['PollutionCertificate'])

        # Adding model 'License'
        db.create_table(u'afterbuy_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('license_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('blood_group', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['License'])

        # Adding model 'Invoice'
        db.create_table(u'afterbuy_invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dealer_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dealer_contact', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['Invoice'])

        # Adding model 'Support'
        db.create_table(u'afterbuy_support', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Brand'])),
            ('brand_product_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.BrandProductCategory'], null=True, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('toll_free', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['Support'])

        # Adding model 'OTPToken'
        db.create_table(u'afterbuy_otptoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('request_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'])),
        ))
        db.send_create_signal('afterbuy', ['OTPToken'])

        # Adding model 'UserNotification'
        db.create_table(u'afterbuy_usernotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('action', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notification_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('afterbuy', ['UserNotification'])

        # Adding model 'UserMobileInfo'
        db.create_table(u'afterbuy_usermobileinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'])),
            ('IMEI', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('ICCID', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('operating_system', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['UserMobileInfo'])

        # Adding model 'UserPreference'
        db.create_table(u'afterbuy_userpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'])),
        ))
        db.send_create_signal('afterbuy', ['UserPreference'])

        # Adding unique constraint on 'UserPreference', fields ['user', 'key']
        db.create_unique(u'afterbuy_userpreference', ['user_id', 'key'])

        # Adding model 'BrandPreference'
        db.create_table(u'afterbuy_brandpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Brand'])),
        ))
        db.send_create_signal('afterbuy', ['BrandPreference'])

        # Adding unique constraint on 'BrandPreference', fields ['brand', 'key']
        db.create_unique(u'afterbuy_brandpreference', ['brand_id', 'key'])

        # Adding model 'Interest'
        db.create_table(u'afterbuy_interest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('interest_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('afterbuy', ['Interest'])

        # Adding model 'SellInformation'
        db.create_table(u'afterbuy_sellinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_negotiable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_sold', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('afterbuy', ['SellInformation'])

        # Adding model 'UserProductImages'
        db.create_table(u'afterbuy_userproductimages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.UserProduct'])),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='primary', max_length=20)),
        ))
        db.send_create_signal('afterbuy', ['UserProductImages'])

        # Adding model 'MessageTemplate'
        db.create_table(u'afterbuy_messagetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('template_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('afterbuy', ['MessageTemplate'])

        # Adding model 'EmailTemplate'
        db.create_table(u'afterbuy_emailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('template_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('afterbuy', ['EmailTemplate'])

        # Adding model 'SMSLog'
        db.create_table(u'afterbuy_smslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('afterbuy', ['SMSLog'])

        # Adding model 'EmailLog'
        db.create_table(u'afterbuy_emaillog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('receiver', self.gf('django.db.models.fields.TextField')()),
            ('cc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['EmailLog'])

        # Adding model 'AuditLog'
        db.create_table(u'afterbuy_auditlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('urls', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['afterbuy.Consumer'], null=True, blank=True)),
        ))
        db.send_create_signal('afterbuy', ['AuditLog'])


    def backwards(self, orm):
        # Removing unique constraint on 'BrandPreference', fields ['brand', 'key']
        db.delete_unique(u'afterbuy_brandpreference', ['brand_id', 'key'])

        # Removing unique constraint on 'UserPreference', fields ['user', 'key']
        db.delete_unique(u'afterbuy_userpreference', ['user_id', 'key'])

        # Deleting model 'Industry'
        db.delete_table(u'afterbuy_industry')

        # Deleting model 'Brand'
        db.delete_table(u'afterbuy_brand')

        # Deleting model 'BrandProductCategory'
        db.delete_table(u'afterbuy_brandproductcategory')

        # Deleting model 'ProductType'
        db.delete_table(u'afterbuy_producttype')

        # Deleting model 'Consumer'
        db.delete_table(u'afterbuy_consumer')

        # Deleting model 'UserProduct'
        db.delete_table(u'afterbuy_userproduct')

        # Deleting model 'ProductSupport'
        db.delete_table(u'afterbuy_productsupport')

        # Deleting model 'RegistrationCertificate'
        db.delete_table(u'afterbuy_registrationcertificate')

        # Deleting model 'ProductInsuranceInfo'
        db.delete_table(u'afterbuy_productinsuranceinfo')

        # Deleting model 'ProductWarrantyInfo'
        db.delete_table(u'afterbuy_productwarrantyinfo')

        # Deleting model 'PollutionCertificate'
        db.delete_table(u'afterbuy_pollutioncertificate')

        # Deleting model 'License'
        db.delete_table(u'afterbuy_license')

        # Deleting model 'Invoice'
        db.delete_table(u'afterbuy_invoice')

        # Deleting model 'Support'
        db.delete_table(u'afterbuy_support')

        # Deleting model 'OTPToken'
        db.delete_table(u'afterbuy_otptoken')

        # Deleting model 'UserNotification'
        db.delete_table(u'afterbuy_usernotification')

        # Deleting model 'UserMobileInfo'
        db.delete_table(u'afterbuy_usermobileinfo')

        # Deleting model 'UserPreference'
        db.delete_table(u'afterbuy_userpreference')

        # Deleting model 'BrandPreference'
        db.delete_table(u'afterbuy_brandpreference')

        # Deleting model 'Interest'
        db.delete_table(u'afterbuy_interest')

        # Deleting model 'SellInformation'
        db.delete_table(u'afterbuy_sellinformation')

        # Deleting model 'UserProductImages'
        db.delete_table(u'afterbuy_userproductimages')

        # Deleting model 'MessageTemplate'
        db.delete_table(u'afterbuy_messagetemplate')

        # Deleting model 'EmailTemplate'
        db.delete_table(u'afterbuy_emailtemplate')

        # Deleting model 'SMSLog'
        db.delete_table(u'afterbuy_smslog')

        # Deleting model 'EmailLog'
        db.delete_table(u'afterbuy_emaillog')

        # Deleting model 'AuditLog'
        db.delete_table(u'afterbuy_auditlog')


    models = {
        'afterbuy.auditlog': {
            'Meta': {'object_name': 'AuditLog'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'urls': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']", 'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.brand': {
            'Meta': {'object_name': 'Brand'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Industry']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'afterbuy.brandpreference': {
            'Meta': {'unique_together': "(('brand', 'key'),)", 'object_name': 'BrandPreference'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Brand']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'afterbuy.brandproductcategory': {
            'Meta': {'object_name': 'BrandProductCategory'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Brand']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'afterbuy.consumer': {
            'Meta': {'object_name': 'Consumer'},
            'accepted_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consumer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'default': "'guest.png'", 'max_length': '200'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'afterbuy.emaillog': {
            'Meta': {'object_name': 'EmailLog'},
            'cc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.TextField', [], {}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'template_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'afterbuy.industry': {
            'Meta': {'object_name': 'Industry'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'afterbuy.interest': {
            'Meta': {'object_name': 'Interest'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'afterbuy.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dealer_contact': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'dealer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"})
        },
        'afterbuy.license': {
            'Meta': {'object_name': 'License'},
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"})
        },
        'afterbuy.messagetemplate': {
            'Meta': {'object_name': 'MessageTemplate'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'template_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'afterbuy.otptoken': {
            'Meta': {'object_name': 'OTPToken'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'request_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']"})
        },
        'afterbuy.pollutioncertificate': {
            'Meta': {'object_name': 'PollutionCertificate'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'pucc_number': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'afterbuy.productinsuranceinfo': {
            'Meta': {'object_name': 'ProductInsuranceInfo'},
            'agency_contact': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'agency_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'insurance_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nominee': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'premium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'vehicle_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'afterbuy.productsupport': {
            'Meta': {'object_name': 'ProductSupport'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'afterbuy.productwarrantyinfo': {
            'Meta': {'object_name': 'ProductWarrantyInfo'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'blank': 'True'}),
            'premium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"})
        },
        'afterbuy.registrationcertificate': {
            'Meta': {'object_name': 'RegistrationCertificate'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'cc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'chassis_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cylinder': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'engine_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fuel': ('django.db.models.fields.CharField', [], {'default': "'Petrol'", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'model_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'registration_upto': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relation_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'seating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'afterbuy.sellinformation': {
            'Meta': {'object_name': 'SellInformation'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_negotiable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.smslog': {
            'Meta': {'object_name': 'SMSLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'afterbuy.support': {
            'Meta': {'object_name': 'Support'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Brand']"}),
            'brand_product_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.BrandProductCategory']", 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'toll_free': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.usermobileinfo': {
            'ICCID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'IMEI': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'UserMobileInfo'},
            'capacity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'operating_system': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'afterbuy.usernotification': {
            'Meta': {'object_name': 'UserNotification'},
            'action': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notification_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']"})
        },
        'afterbuy.userpreference': {
            'Meta': {'unique_together': "(('user', 'key'),)", 'object_name': 'UserPreference'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'afterbuy.userproduct': {
            'Meta': {'object_name': 'UserProduct'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Brand']"}),
            'brand_product_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'consumer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.Consumer']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.ProductType']"}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'afterbuy.userproductimages': {
            'Meta': {'object_name': 'UserProductImages'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['afterbuy.UserProduct']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'primary'", 'max_length': '20'})
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
        }
    }

    complete_apps = ['afterbuy']
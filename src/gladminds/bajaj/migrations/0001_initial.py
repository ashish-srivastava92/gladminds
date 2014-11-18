# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BrandProductCategory'
        db.create_table(u'bajaj_brandproductcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['BrandProductCategory'])

        # Adding model 'UserProfile'
        db.create_table(u'bajaj_userprofile', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bajaj_users', unique=True, primary_key=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('bajaj', ['UserProfile'])

        # Adding model 'Dealer'
        db.create_table(u'bajaj_dealer', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('dealer_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bajaj_registered_dealer', unique=True, primary_key=True, to=orm['bajaj.UserProfile'])),
        ))
        db.send_create_signal('bajaj', ['Dealer'])

        # Adding model 'AuthorizedServiceCenter'
        db.create_table(u'bajaj_authorizedservicecenter', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('asc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bajaj_registered_asc', unique=True, primary_key=True, to=orm['bajaj.UserProfile'])),
            ('dealer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.Dealer'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['AuthorizedServiceCenter'])

        # Adding model 'ServiceAdvisor'
        db.create_table(u'bajaj_serviceadvisor', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('service_advisor_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bajaj_service_advisor', unique=True, primary_key=True, to=orm['bajaj.UserProfile'])),
            ('dealer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.Dealer'], null=True, blank=True)),
            ('asc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.AuthorizedServiceCenter'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['ServiceAdvisor'])

        # Adding model 'Feedback'
        db.create_table(u'bajaj_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporter', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reporter_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reporter_email_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='Low', max_length=12)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('resolved_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('pending_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('wait_time', self.gf('django.db.models.fields.FloatField')(default='0.0', max_length=20, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('ratings', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('root_cause', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('assign_to_reporter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assign_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.UserProfile'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['Feedback'])

        # Adding model 'Comments'
        db.create_table(u'bajaj_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('comments_str', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feedback_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.Feedback'])),
        ))
        db.send_create_signal('bajaj', ['Comments'])

        # Adding model 'ProductType'
        db.create_table(u'bajaj_producttype', (
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product_type_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('product_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('brand_product_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bajaj_product_type', null=True, to=orm['bajaj.BrandProductCategory'])),
        ))
        db.send_create_signal('bajaj', ['ProductType'])

        # Adding model 'ProductData'
        db.create_table(u'bajaj_productdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=215)),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=215, unique=True, null=True, blank=True)),
            ('customer_phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True, blank=True)),
            ('customer_name', self.gf('django.db.models.fields.CharField')(max_length=215, unique=True, null=True, blank=True)),
            ('customer_address', self.gf('django.db.models.fields.CharField')(max_length=215, unique=True, null=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('engine', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('veh_reg_no', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ProductType'], null=True, blank=True)),
            ('dealer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.Dealer'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['ProductData'])

        # Adding model 'CouponData'
        db.create_table(u'bajaj_coupondata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('unique_service_coupon', self.gf('django.db.models.fields.CharField')(unique=True, max_length=215)),
            ('valid_days', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('valid_kms', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('service_type', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, db_index=True)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('mark_expired_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('actual_service_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('actual_kms', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('last_reminder_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('schedule_reminder_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('extended_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sent_to_sap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('credit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('credit_note', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('special_case', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ProductData'])),
            ('service_advisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ServiceAdvisor'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['CouponData'])

        # Adding model 'ServiceAdvisorCouponRelationship'
        db.create_table(u'bajaj_serviceadvisorcouponrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('unique_service_coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.CouponData'])),
            ('service_advisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ServiceAdvisor'])),
        ))
        db.send_create_signal('bajaj', ['ServiceAdvisorCouponRelationship'])

        # Adding model 'UCNRecovery'
        db.create_table(u'bajaj_ucnrecovery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('file_location', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('unique_service_coupon', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bajaj_ucn_recovery', to=orm['bajaj.UserProfile'])),
        ))
        db.send_create_signal('bajaj', ['UCNRecovery'])

        # Adding model 'OldFscData'
        db.create_table(u'bajaj_oldfscdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('unique_service_coupon', self.gf('django.db.models.fields.CharField')(max_length=215, null=True)),
            ('valid_days', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True)),
            ('valid_kms', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True)),
            ('service_type', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, db_index=True)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('mark_expired_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('actual_service_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('actual_kms', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('last_reminder_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('schedule_reminder_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('extended_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sent_to_sap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('credit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('credit_note', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('special_case', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('missing_field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('missing_value', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ProductData'])),
            ('dealer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.Dealer'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['OldFscData'])

        # Adding model 'OTPToken'
        db.create_table(u'bajaj_otptoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('request_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bajaj_otp_token', null=True, to=orm['bajaj.UserProfile'])),
        ))
        db.send_create_signal('bajaj', ['OTPToken'])

        # Adding model 'MessageTemplate'
        db.create_table(u'bajaj_messagetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('template_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('bajaj', ['MessageTemplate'])

        # Adding model 'EmailTemplate'
        db.create_table(u'bajaj_emailtemplate', (
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
        db.send_create_signal('bajaj', ['EmailTemplate'])

        # Adding model 'ASCTempRegistration'
        db.create_table(u'bajaj_asctempregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('dealer_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['ASCTempRegistration'])

        # Adding model 'SATempRegistration'
        db.create_table(u'bajaj_satempregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('bajaj', ['SATempRegistration'])

        # Adding model 'CustomerTempRegistration'
        db.create_table(u'bajaj_customertempregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('new_customer_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('new_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('product_purchase_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('temp_customer_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('sent_to_sap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tagged_sap_id', self.gf('django.db.models.fields.CharField')(max_length=215, unique=True, null=True, blank=True)),
            ('product_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.ProductData'], null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['CustomerTempRegistration'])

        # Adding model 'SparesData'
        db.create_table(u'bajaj_sparesdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('spare_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('spare_contact', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['SparesData'])

        # Adding model 'UserPreferences'
        db.create_table(u'bajaj_userpreferences', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.UserProfile'])),
        ))
        db.send_create_signal('bajaj', ['UserPreferences'])

        # Adding unique constraint on 'UserPreferences', fields ['user_profile', 'key']
        db.create_unique(u'bajaj_userpreferences', ['user_profile_id', 'key'])

        # Adding model 'SMSLog'
        db.create_table(u'bajaj_smslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('bajaj', ['SMSLog'])

        # Adding model 'EmailLog'
        db.create_table(u'bajaj_emaillog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('receiver', self.gf('django.db.models.fields.TextField')()),
            ('cc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['EmailLog'])

        # Adding model 'DataFeedLog'
        db.create_table(u'bajaj_datafeedlog', (
            ('data_feed_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('total_data_count', self.gf('django.db.models.fields.IntegerField')()),
            ('failed_data_count', self.gf('django.db.models.fields.IntegerField')()),
            ('success_data_count', self.gf('django.db.models.fields.IntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.BooleanField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('file_location', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
        ))
        db.send_create_signal('bajaj', ['DataFeedLog'])

        # Adding model 'AuditLog'
        db.create_table(u'bajaj_auditlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('urls', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bajaj.UserProfile'])),
        ))
        db.send_create_signal('bajaj', ['AuditLog'])

        # Adding model 'SLA'
        db.create_table(u'bajaj_sla', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('priority', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('response_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('response_unit', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('reminder_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('reminder_unit', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('resolution_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('resolution_unit', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('bajaj', ['SLA'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserPreferences', fields ['user_profile', 'key']
        db.delete_unique(u'bajaj_userpreferences', ['user_profile_id', 'key'])

        # Deleting model 'BrandProductCategory'
        db.delete_table(u'bajaj_brandproductcategory')

        # Deleting model 'UserProfile'
        db.delete_table(u'bajaj_userprofile')

        # Deleting model 'Dealer'
        db.delete_table(u'bajaj_dealer')

        # Deleting model 'AuthorizedServiceCenter'
        db.delete_table(u'bajaj_authorizedservicecenter')

        # Deleting model 'ServiceAdvisor'
        db.delete_table(u'bajaj_serviceadvisor')

        # Deleting model 'Feedback'
        db.delete_table(u'bajaj_feedback')

        # Deleting model 'Comments'
        db.delete_table(u'bajaj_comments')

        # Deleting model 'ProductType'
        db.delete_table(u'bajaj_producttype')

        # Deleting model 'ProductData'
        db.delete_table(u'bajaj_productdata')

        # Deleting model 'CouponData'
        db.delete_table(u'bajaj_coupondata')

        # Deleting model 'ServiceAdvisorCouponRelationship'
        db.delete_table(u'bajaj_serviceadvisorcouponrelationship')

        # Deleting model 'UCNRecovery'
        db.delete_table(u'bajaj_ucnrecovery')

        # Deleting model 'OldFscData'
        db.delete_table(u'bajaj_oldfscdata')

        # Deleting model 'OTPToken'
        db.delete_table(u'bajaj_otptoken')

        # Deleting model 'MessageTemplate'
        db.delete_table(u'bajaj_messagetemplate')

        # Deleting model 'EmailTemplate'
        db.delete_table(u'bajaj_emailtemplate')

        # Deleting model 'ASCTempRegistration'
        db.delete_table(u'bajaj_asctempregistration')

        # Deleting model 'SATempRegistration'
        db.delete_table(u'bajaj_satempregistration')

        # Deleting model 'CustomerTempRegistration'
        db.delete_table(u'bajaj_customertempregistration')

        # Deleting model 'SparesData'
        db.delete_table(u'bajaj_sparesdata')

        # Deleting model 'UserPreferences'
        db.delete_table(u'bajaj_userpreferences')

        # Deleting model 'SMSLog'
        db.delete_table(u'bajaj_smslog')

        # Deleting model 'EmailLog'
        db.delete_table(u'bajaj_emaillog')

        # Deleting model 'DataFeedLog'
        db.delete_table(u'bajaj_datafeedlog')

        # Deleting model 'AuditLog'
        db.delete_table(u'bajaj_auditlog')

        # Deleting model 'SLA'
        db.delete_table(u'bajaj_sla')


    models = {
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
        'bajaj.asctempregistration': {
            'Meta': {'object_name': 'ASCTempRegistration'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'bajaj.auditlog': {
            'Meta': {'object_name': 'AuditLog'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'urls': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.UserProfile']"}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'bajaj.authorizedservicecenter': {
            'Meta': {'object_name': 'AuthorizedServiceCenter'},
            'asc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dealer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.Dealer']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bajaj_registered_asc'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['bajaj.UserProfile']"})
        },
        'bajaj.brandproductcategory': {
            'Meta': {'object_name': 'BrandProductCategory'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'bajaj.comments': {
            'Meta': {'object_name': 'Comments'},
            'comments_str': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'bajaj.coupondata': {
            'Meta': {'object_name': 'CouponData'},
            'actual_kms': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'actual_service_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_note': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'extended_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mark_expired_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ProductData']"}),
            'schedule_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_to_sap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_advisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ServiceAdvisor']", 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'special_case': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'unique_service_coupon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '215'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'valid_kms': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        'bajaj.customertempregistration': {
            'Meta': {'object_name': 'CustomerTempRegistration'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'new_customer_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'product_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ProductData']", 'null': 'True', 'blank': 'True'}),
            'product_purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'sent_to_sap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tagged_sap_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'temp_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'bajaj.datafeedlog': {
            'Meta': {'object_name': 'DataFeedLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'data_feed_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'failed_data_count': ('django.db.models.fields.IntegerField', [], {}),
            'feed_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'file_location': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {}),
            'success_data_count': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'total_data_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'bajaj.dealer': {
            'Meta': {'object_name': 'Dealer'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bajaj_registered_dealer'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['bajaj.UserProfile']"})
        },
        'bajaj.emaillog': {
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
        'bajaj.emailtemplate': {
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
        'bajaj.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'assign_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'assign_to_reporter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pending_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'Low'", 'max_length': '12'}),
            'ratings': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'reporter_email_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reporter_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'resolved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'root_cause': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'wait_time': ('django.db.models.fields.FloatField', [], {'default': "'0.0'", 'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'bajaj.messagetemplate': {
            'Meta': {'object_name': 'MessageTemplate'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'template_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'bajaj.oldfscdata': {
            'Meta': {'object_name': 'OldFscData'},
            'actual_kms': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'actual_service_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_note': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dealer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.Dealer']", 'null': 'True', 'blank': 'True'}),
            'extended_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mark_expired_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'missing_field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'missing_value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ProductData']"}),
            'schedule_reminder_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_to_sap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'special_case': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'unique_service_coupon': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'valid_kms': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'})
        },
        'bajaj.otptoken': {
            'Meta': {'object_name': 'OTPToken'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'request_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bajaj_otp_token'", 'null': 'True', 'to': "orm['bajaj.UserProfile']"})
        },
        'bajaj.productdata': {
            'Meta': {'object_name': 'ProductData'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_address': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '215', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'customer_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.Dealer']", 'null': 'True', 'blank': 'True'}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '215'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ProductType']", 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'veh_reg_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'bajaj.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'brand_product_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bajaj_product_type'", 'null': 'True', 'to': "orm['bajaj.BrandProductCategory']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'product_type_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bajaj.satempregistration': {
            'Meta': {'object_name': 'SATempRegistration'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'bajaj.serviceadvisor': {
            'Meta': {'object_name': 'ServiceAdvisor'},
            'asc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.AuthorizedServiceCenter']", 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dealer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.Dealer']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'service_advisor_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bajaj_service_advisor'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['bajaj.UserProfile']"})
        },
        'bajaj.serviceadvisorcouponrelationship': {
            'Meta': {'object_name': 'ServiceAdvisorCouponRelationship'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'service_advisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.ServiceAdvisor']"}),
            'unique_service_coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.CouponData']"})
        },
        'bajaj.sla': {
            'Meta': {'object_name': 'SLA'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'reminder_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reminder_unit': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'resolution_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'resolution_unit': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'response_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'response_unit': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'bajaj.smslog': {
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
        'bajaj.sparesdata': {
            'Meta': {'object_name': 'SparesData'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spare_contact': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'spare_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'bajaj.ucnrecovery': {
            'Meta': {'object_name': 'UCNRecovery'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'file_location': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'unique_service_coupon': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bajaj_ucn_recovery'", 'to': "orm['bajaj.UserProfile']"})
        },
        'bajaj.userpreferences': {
            'Meta': {'unique_together': "(('user_profile', 'key'),)", 'object_name': 'UserPreferences'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bajaj.UserProfile']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'bajaj.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bajaj_users'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bajaj']
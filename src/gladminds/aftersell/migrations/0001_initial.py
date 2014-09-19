# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ASCSaveForm'
        db.create_table(u'aftersell_ascsaveform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('dealer_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('aftersell', ['ASCSaveForm'])

        # Adding model 'UCNRecovery'
        db.create_table(u'aftersell_ucnrecovery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gladminds.UserProfile'])),
            ('sap_customer_id', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('file_location', self.gf('django.db.models.fields.CharField')(max_length=215, null=True, blank=True)),
            ('request_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 19, 0, 0))),
        ))
        db.send_create_signal('aftersell', ['UCNRecovery'])

        # Adding model 'RegisteredDealer'
        db.create_table(u'aftersell_registereddealer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dealer_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(default='dealer', max_length=10)),
            ('dependent_on', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('aftersell', ['RegisteredDealer'])

        # Adding model 'ServiceAdvisor'
        db.create_table(u'aftersell_serviceadvisor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_advisor_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('aftersell', ['ServiceAdvisor'])

        # Adding model 'ServiceAdvisorDealerRelationship'
        db.create_table(u'aftersell_serviceadvisordealerrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dealer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aftersell.RegisteredDealer'])),
            ('service_advisor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aftersell.ServiceAdvisor'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('aftersell', ['ServiceAdvisorDealerRelationship'])

        # Adding model 'RegisteredASC'
        db.create_table(u'aftersell_registeredasc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gladminds.UserProfile'], unique=True, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('asc_name', self.gf('django.db.models.fields.CharField')(max_length=215)),
            ('email_id', self.gf('django.db.models.fields.EmailField')(max_length=215, null=True, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 19, 0, 0))),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('img_url', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('isActive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('asc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('dealer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aftersell.RegisteredDealer'], null=True, blank=True)),
        ))
        db.send_create_signal('aftersell', ['RegisteredASC'])

        # Adding model 'ServiceDeskUser'
        db.create_table(u'aftersell_servicedeskuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gladminds.UserProfile'], unique=True, null=True, blank=True)),
            ('email_id', self.gf('django.db.models.fields.EmailField')(max_length=215, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('aftersell', ['ServiceDeskUser'])

        # Adding model 'Feedback'
        db.create_table(u'aftersell_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporter', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reporter_email_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('assign_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aftersell.ServiceDeskUser'], null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('resolved_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('pending_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('wait_time', self.gf('django.db.models.fields.FloatField')(default='0.0', max_length=20, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('ratings', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('root_cause', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('aftersell', ['Feedback'])

        # Adding model 'Comments'
        db.create_table(u'aftersell_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aftersell.Feedback'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('aftersell', ['Comments'])

        # Adding model 'AuditLog'
        db.create_table(u'aftersell_auditlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('reciever', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('aftersell', ['AuditLog'])

        # Adding model 'DataFeedLog'
        db.create_table(u'aftersell_datafeedlog', (
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
        db.send_create_signal('aftersell', ['DataFeedLog'])


    def backwards(self, orm):
        # Deleting model 'ASCSaveForm'
        db.delete_table(u'aftersell_ascsaveform')

        # Deleting model 'UCNRecovery'
        db.delete_table(u'aftersell_ucnrecovery')

        # Deleting model 'RegisteredDealer'
        db.delete_table(u'aftersell_registereddealer')

        # Deleting model 'ServiceAdvisor'
        db.delete_table(u'aftersell_serviceadvisor')

        # Deleting model 'ServiceAdvisorDealerRelationship'
        db.delete_table(u'aftersell_serviceadvisordealerrelationship')

        # Deleting model 'RegisteredASC'
        db.delete_table(u'aftersell_registeredasc')

        # Deleting model 'ServiceDeskUser'
        db.delete_table(u'aftersell_servicedeskuser')

        # Deleting model 'Feedback'
        db.delete_table(u'aftersell_feedback')

        # Deleting model 'Comments'
        db.delete_table(u'aftersell_comments')

        # Deleting model 'AuditLog'
        db.delete_table(u'aftersell_auditlog')

        # Deleting model 'DataFeedLog'
        db.delete_table(u'aftersell_datafeedlog')


    models = {
        'aftersell.ascsaveform': {
            'Meta': {'object_name': 'ASCSaveForm'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'aftersell.auditlog': {
            'Meta': {'object_name': 'AuditLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'reciever': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'aftersell.comments': {
            'Meta': {'object_name': 'Comments'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'aftersell.datafeedlog': {
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
        'aftersell.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'assign_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.ServiceDeskUser']", 'null': 'True', 'blank': 'True'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pending_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'ratings': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'reporter_email_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'resolved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'root_cause': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'wait_time': ('django.db.models.fields.FloatField', [], {'default': "'0.0'", 'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'aftersell.registeredasc': {
            'Meta': {'object_name': 'RegisteredASC'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'asc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'asc_name': ('django.db.models.fields.CharField', [], {'max_length': '215'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dealer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.RegisteredDealer']", 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 19, 0, 0)'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gladminds.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
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
        'aftersell.serviceadvisordealerrelationship': {
            'Meta': {'object_name': 'ServiceAdvisorDealerRelationship'},
            'dealer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.RegisteredDealer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_advisor_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aftersell.ServiceAdvisor']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'aftersell.servicedeskuser': {
            'Meta': {'object_name': 'ServiceDeskUser'},
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gladminds.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'aftersell.ucnrecovery': {
            'Meta': {'object_name': 'UCNRecovery'},
            'file_location': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'request_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 19, 0, 0)'}),
            'sap_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '215', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gladminds.UserProfile']"})
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
        'gladminds.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['aftersell']
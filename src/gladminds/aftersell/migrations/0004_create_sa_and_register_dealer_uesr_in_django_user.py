# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    no_dry_run = True

    def forwards(self, orm):
        for rd in orm.RegisteredDealer.objects.all():
            user_details = orm['auth.User'].objects.filter(username=rd.dealer_id)
            if not user_details:
                user_details = orm['auth.User'](username=rd.dealer_id)
                user_details.save()
                user_profile = orm['gladminds.UserProfile'](user=user_details)
                user_profile.save()
            user_profile = orm['gladminds.UserProfile'].objects.get(user=user_details)
            rd.user = user_profile
            rd.save()

        for sa in orm.ServiceAdvisor.objects.all():
            user_details = orm['auth.User'].objects.filter(username=sa.service_advisor_id)
            if not user_details:
                user_details = orm['auth.User'](username=sa.service_advisor_id)
                user_details.save()
                user_profile = orm['gladminds.UserProfile'](user=user_details)
                user_profile.save()
            user_profile = orm['gladminds.UserProfile'].objects.get(user=user_details)
            sa.user = user_profile
            sa.save()

    def backwards(self, orm):
        pass

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
            'role': ('django.db.models.fields.CharField', [], {'default': "'dealer'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gladminds.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'aftersell.serviceadvisor': {
            'Meta': {'object_name': 'ServiceAdvisor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'service_advisor_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gladminds.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
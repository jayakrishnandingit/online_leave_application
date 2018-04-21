# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LeaveType'
        db.create_table(u'leave_leavetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_leave', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('no_of_leave', self.gf('django.db.models.fields.IntegerField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_type_client', to=orm['client.Client'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_type_subscriber', to=orm['subscriber.Subscriber'])),
        ))
        db.send_create_signal(u'leave', ['LeaveType'])

        # Adding model 'Holiday'
        db.create_table(u'leave_holiday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='holiday_client', to=orm['client.Client'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='holiday_subscriber', to=orm['subscriber.Subscriber'])),
        ))
        db.send_create_signal(u'leave', ['Holiday'])

        # Adding model 'Leave'
        db.create_table(u'leave_leave', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('type_of_leave', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_leave_type', to=orm['leave.LeaveType'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_requester', to=orm['subscriber.Subscriber'])),
            ('approver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_approver', to=orm['subscriber.Subscriber'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'leave', ['Leave'])


    def backwards(self, orm):
        # Deleting model 'LeaveType'
        db.delete_table(u'leave_leavetype')

        # Deleting model 'Holiday'
        db.delete_table(u'leave_holiday')

        # Deleting model 'Leave'
        db.delete_table(u'leave_leave')


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
        u'client.client': {
            'Meta': {'object_name': 'Client'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'payment_status': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leave.holiday': {
            'Meta': {'object_name': 'Holiday'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'holiday_client'", 'to': u"orm['client.Client']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'holiday_subscriber'", 'to': u"orm['subscriber.Subscriber']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        u'leave.leave': {
            'Meta': {'object_name': 'Leave'},
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_approver'", 'to': u"orm['subscriber.Subscriber']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_requester'", 'to': u"orm['subscriber.Subscriber']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'type_of_leave': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_leave_type'", 'to': u"orm['leave.LeaveType']"})
        },
        u'leave.leavetype': {
            'Meta': {'object_name': 'LeaveType'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_type_client'", 'to': u"orm['client.Client']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_type_subscriber'", 'to': u"orm['subscriber.Subscriber']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_leave': ('django.db.models.fields.IntegerField', [], {}),
            'type_of_leave': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'subscriber.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriber_client'", 'to': u"orm['client.Client']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriber_user'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['leave']
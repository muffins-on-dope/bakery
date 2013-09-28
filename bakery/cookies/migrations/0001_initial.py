# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cookie'
        db.create_table('cookies_cookie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.BakeryUser'])),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('license', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('last_change', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_poll', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('mapping', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal('cookies', ['Cookie'])


    def backwards(self, orm):
        # Deleting model 'Cookie'
        db.delete_table('cookies_cookie')


    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'unique': 'True', 'max_length': '254', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cookies.cookie': {
            'Meta': {'object_name': 'Cookie'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'mapping': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cookies']
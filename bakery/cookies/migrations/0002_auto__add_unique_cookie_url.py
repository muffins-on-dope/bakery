# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Cookie', fields ['url']
        db.create_unique('cookies_cookie', ['url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Cookie', fields ['url']
        db.delete_unique('cookies_cookie', ['url'])


    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'email': ('django.db.models.fields.EmailField', [], {'null': 'True', 'blank': 'True', 'max_length': '254', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'cookies.cookie': {
            'Meta': {'object_name': 'Cookie'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''"}),
            'mapping': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        }
    }

    complete_apps = ['cookies']

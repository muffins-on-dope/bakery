# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cookie.owner_name'
        db.add_column('cookies_cookie', 'owner_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Cookie.backend'
        db.add_column('cookies_cookie', 'backend',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding unique constraint on 'Cookie', fields ['name', 'owner_name']
        db.create_unique('cookies_cookie', ['name', 'owner_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Cookie', fields ['name', 'owner_name']
        db.delete_unique('cookies_cookie', ['name', 'owner_name'])

        # Deleting field 'Cookie.owner_name'
        db.delete_column('cookies_cookie', 'owner_name')

        # Deleting field 'Cookie.backend'
        db.delete_column('cookies_cookie', 'backend')


    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '254', 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'cookies.cookie': {
            'Meta': {'object_name': 'Cookie', 'unique_together': "(('name', 'owner_name'),)"},
            'backend': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'mapping': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        }
    }

    complete_apps = ['cookies']
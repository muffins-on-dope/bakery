# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Cookie.participants'
        db.alter_column('cookies_cookie', 'participants', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Cookie.language'
        db.alter_column('cookies_cookie', 'language', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Cookie.homepage'
        db.alter_column('cookies_cookie', 'homepage', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Cookie.participants'
        db.alter_column('cookies_cookie', 'participants', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Cookie.language'
        db.alter_column('cookies_cookie', 'language', self.gf('django.db.models.fields.CharField')(max_length=50, default=''))

        # Changing field 'Cookie.homepage'
        db.alter_column('cookies_cookie', 'homepage', self.gf('django.db.models.fields.CharField')(max_length=255, default=''))

    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
            'clone_urls': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'mapping': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'repo_forks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_watchers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        }
    }

    complete_apps = ['cookies']
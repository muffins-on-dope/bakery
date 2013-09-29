# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Candy'
        db.create_table('socialize_candy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candy_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='candies', to=orm['auth.BakeryUser'])),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['socialize.Vote'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('socialize', ['Candy'])

        # Adding unique constraint on 'Vote', fields ['user', 'cookie']
        db.create_unique('socialize_vote', ['user_id', 'cookie_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'cookie']
        db.delete_unique('socialize_vote', ['user_id', 'cookie_id'])

        # Deleting model 'Candy'
        db.delete_table('socialize_candy')


    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cookies.cookie': {
            'Meta': {'unique_together': "(('name', 'owner_name'),)", 'object_name': 'Cookie'},
            'backend': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'clone_urls': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '50'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'mapping': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'repo_forks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_watchers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['socialize.Vote']", 'related_name': "'votes'", 'symmetrical': 'False', 'to': "orm['auth.BakeryUser']"})
        },
        'socialize.candy': {
            'Meta': {'object_name': 'Candy'},
            'candy_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'candies'", 'to': "orm['auth.BakeryUser']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['socialize.Vote']"})
        },
        'socialize.vote': {
            'Meta': {'unique_together': "(('user', 'cookie'),)", 'object_name': 'Vote'},
            'cookie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cookies.Cookie']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.BakeryUser']"})
        }
    }

    complete_apps = ['socialize']
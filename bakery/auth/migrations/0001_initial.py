# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permission'
        db.create_table('auth_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('auth', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['content_type', 'codename']
        db.create_unique('auth_permission', ['content_type_id', 'codename'])

        # Adding model 'Group'
        db.create_table('auth_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('auth', ['Group'])

        # Adding M2M table for field permissions on 'Group'
        m2m_table_name = db.shorten_name('auth_group_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['auth.group'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'permission_id'])

        # Adding model 'BakeryUser'
        db.create_table('auth_bakeryuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, null=True, blank=True, max_length=254)),
            ('name', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=100)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_organization', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_url', self.gf('django.db.models.fields.URLField')(null=True, blank=True, max_length=200)),
        ))
        db.send_create_signal('auth', ['BakeryUser'])


    def backwards(self, orm):
        # Removing unique constraint on 'Permission', fields ['content_type', 'codename']
        db.delete_unique('auth_permission', ['content_type_id', 'codename'])

        # Deleting model 'Permission'
        db.delete_table('auth_permission')

        # Deleting model 'Group'
        db.delete_table('auth_group')

        # Removing M2M table for field permissions on 'Group'
        db.delete_table(db.shorten_name('auth_group_permissions'))

        # Deleting model 'BakeryUser'
        db.delete_table('auth_bakeryuser')


    models = {
        'auth.bakeryuser': {
            'Meta': {'object_name': 'BakeryUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'null': 'True', 'blank': 'True', 'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['auth']

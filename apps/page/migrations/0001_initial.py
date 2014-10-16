# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table('page_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['team.Team'])),
            ('link', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('content', self.gf('sanitizer.models.SanitizedCharField')(max_length=50000)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages_created', to=orm['account.Account'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages_updated', to=orm['account.Account'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('page', ['Page'])

        # Adding unique constraint on 'Page', fields ['team', 'name']
        db.create_unique('page_page', ['team_id', 'name'])

        # Adding unique constraint on 'Page', fields ['team', 'link']
        db.create_unique('page_page', ['team_id', 'link'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['team', 'link']
        db.delete_unique('page_page', ['team_id', 'link'])

        # Removing unique constraint on 'Page', fields ['team', 'name']
        db.delete_unique('page_page', ['team_id', 'name'])

        # Deleting model 'Page'
        db.delete_table('page_page')


    models = {
        'account.account': {
            'Meta': {'ordering': "['user__username']", 'object_name': 'Account'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['link.Link']", 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'passport': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'OTHER'", 'max_length': '64'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'link.link': {
            'Meta': {'object_name': 'Link'},
            'confirmed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'page.page': {
            'Meta': {'ordering': "['order', 'name']", 'unique_together': "(('team', 'name'), ('team', 'link'))", 'object_name': 'Page'},
            'content': ('sanitizer.models.SanitizedCharField', [], {'max_length': '50000'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['team.Team']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'team.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application': ('django.db.models.fields.TextField', [], {}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['link.Link']", 'null': 'True', 'blank': 'True'}),
            'logo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['account.Account']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['page']
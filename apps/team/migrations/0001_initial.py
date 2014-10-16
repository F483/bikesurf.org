# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table('team_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('logo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('application', self.gf('django.db.models.fields.TextField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_created', to=orm['account.Account'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_updated', to=orm['account.Account'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('team', ['Team'])

        # Adding M2M table for field links on 'Team'
        db.create_table('team_team_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['team.team'], null=False)),
            ('link', models.ForeignKey(orm['link.link'], null=False))
        ))
        db.create_unique('team_team_links', ['team_id', 'link_id'])

        # Adding M2M table for field members on 'Team'
        db.create_table('team_team_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['team.team'], null=False)),
            ('account', models.ForeignKey(orm['account.account'], null=False))
        ))
        db.create_unique('team_team_members', ['team_id', 'account_id'])

        # Adding model 'JoinRequest'
        db.create_table('team_joinrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='join_requests', to=orm['team.Team'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='join_requests_made', to=orm['account.Account'])),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='join_requests_processed', null=True, to=orm['account.Account'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=256)),
            ('application', self.gf('django.db.models.fields.TextField')()),
            ('response', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('team', ['JoinRequest'])

        # Adding model 'RemoveRequest'
        db.create_table('team_removerequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remove_requests', to=orm['team.Team'])),
            ('concerned', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remove_requests_concerned', to=orm['account.Account'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remove_requests_made', to=orm['account.Account'])),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='remove_requests_processed', null=True, to=orm['account.Account'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=256)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('response', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('team', ['RemoveRequest'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table('team_team')

        # Removing M2M table for field links on 'Team'
        db.delete_table('team_team_links')

        # Removing M2M table for field members on 'Team'
        db.delete_table('team_team_members')

        # Deleting model 'JoinRequest'
        db.delete_table('team_joinrequest')

        # Deleting model 'RemoveRequest'
        db.delete_table('team_removerequest')


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
        'team.joinrequest': {
            'Meta': {'ordering': "['-status', 'created_on']", 'object_name': 'JoinRequest'},
            'application': ('django.db.models.fields.TextField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'join_requests_processed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'join_requests_made'", 'to': "orm['account.Account']"}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '256'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'join_requests'", 'to': "orm['team.Team']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'team.removerequest': {
            'Meta': {'ordering': "['-status', 'created_on']", 'object_name': 'RemoveRequest'},
            'concerned': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remove_requests_concerned'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'remove_requests_processed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remove_requests_made'", 'to': "orm['account.Account']"}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '256'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remove_requests'", 'to': "orm['team.Team']"}),
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

    complete_apps = ['team']
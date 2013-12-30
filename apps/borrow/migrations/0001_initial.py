# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Borrow'
        db.create_table('borrow_borrow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bike', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='borrows', null=True, to=orm['bike.Bike'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='borrows', to=orm['team.Team'])),
            ('borrower', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('finish', self.gf('django.db.models.fields.DateField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('src', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='departures', null=True, to=orm['station.Station'])),
            ('dest', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrivals', null=True, to=orm['station.Station'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('borrow', ['Borrow'])

        # Adding model 'Log'
        db.create_table('borrow_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('borrow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['borrow.Borrow'])),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'], null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('borrow', ['Log'])

        # Adding model 'Rating'
        db.create_table('borrow_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('borrow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['borrow.Borrow'])),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('originator', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('borrow', ['Rating'])

        # Adding unique constraint on 'Rating', fields ['borrow', 'account', 'originator']
        db.create_unique('borrow_rating', ['borrow_id', 'account_id', 'originator'])


    def backwards(self, orm):
        # Removing unique constraint on 'Rating', fields ['borrow', 'account', 'originator']
        db.delete_unique('borrow_rating', ['borrow_id', 'account_id', 'originator'])

        # Deleting model 'Borrow'
        db.delete_table('borrow_borrow')

        # Deleting model 'Log'
        db.delete_table('borrow_log')

        # Deleting model 'Rating'
        db.delete_table('borrow_rating')


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
        'bike.bike': {
            'Meta': {'object_name': 'Bike'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bikes_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lights': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lockcode': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'reserve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'MEDIUM'", 'max_length': '64'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bikes'", 'to': "orm['station.Station']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bikes'", 'to': "orm['team.Team']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bikes_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'borrow.borrow': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Borrow'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bike': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'borrows'", 'null': 'True', 'to': "orm['bike.Bike']"}),
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrivals'", 'null': 'True', 'to': "orm['station.Station']"}),
            'finish': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'departures'", 'null': 'True', 'to': "orm['station.Station']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'borrows'", 'to': "orm['team.Team']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'borrow.log': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Log'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'borrow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': "orm['borrow.Borrow']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']", 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'borrow.rating': {
            'Meta': {'unique_together': "(('borrow', 'account', 'originator'),)", 'object_name': 'Rating'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']"}),
            'borrow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['borrow.Borrow']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'originator': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gallery.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'galleries_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': "orm['gallery.Picture']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'galleries'", 'null': 'True', 'to': "orm['team.Team']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'galleries_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'gallery.picture': {
            'Meta': {'object_name': 'Picture'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'preview': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'thumbnail': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures_updated'", 'to': "orm['account.Account']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'station.station': {
            'Meta': {'object_name': 'Station'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stations_created'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stations'", 'to': "orm['team.Team']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stations_updated'", 'to': "orm['account.Account']"}),
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

    complete_apps = ['borrow']
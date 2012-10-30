# coding: utf8

db.define_table( # Not editable!
    'message',
    
    Field('from_organisation_id', db.organisation),
    Field('from_user_id', db.auth_user),
    Field('to_organisation_id', db.organisation),
    Field('to_user_id', db.auth_user),
    
    Field('body', 'text'),
    Field('bike_id', db.bike),
    Field('borrow_id', db.borrow),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    
    format = '%(from_user_id)s: %(body)s',
    singular = 'Message',
    plural = 'Messages',
)

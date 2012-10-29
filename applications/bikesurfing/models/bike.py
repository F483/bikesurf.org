# coding: utf8

db.define_table(
    'bike',
    Field('name', 'string'),
    Field('description', 'text'),
    Field('picture', 'upload', default=''),
    Field('available' 'boolean', default=True),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(name)s',
    singular = 'Bike',
    plural = 'Bikes',
)

db.define_table(
    'user_bike',
    Field('bike_id', db.bike),
    Field('owner_id', db.auth_user),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(bike_id)s -> %(owner_id)s',
    singular = 'UserBike',
    plural = 'UserBikes',
)

db.define_table(
    'organisation_bike',
    Field('bike_id', db.bike),
    Field('owner_id', db.organisation),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(bike_id)s -> %(owner_id)s',
    singular = 'OrganisationBike',
    plural = 'OrganisationBikes',
)

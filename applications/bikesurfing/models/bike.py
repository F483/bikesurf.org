# coding: utf8

db.define_table(
    'bike',
    Field('name', 'string'),
    Field('description', 'text'),
    Field('available' 'boolean', default=True),
    
    # common usefull properties to filter by
    Field('type', 'string'), # 'mountainbike', 'roadbike', 'fixie', etc ...
    Field('lights' 'boolean', default=False), # to cycle when dark
    Field('fenders' 'boolean', default=False), # to cycle when wet
    Field('rack' 'boolean', default=False), # to carry stuff
    Field('basket' 'boolean', default=False), # to put stuff in
    # TODO how to represent size (children, etc)
    
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
    'bike_picture',
    Field('bike_id', db.bike),
    Field('picture', 'upload', default=''),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(bike_id)s',
    singular = 'BikePicture',
    plural = 'BikePictures',
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

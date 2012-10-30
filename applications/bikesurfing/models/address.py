# coding: utf8


db.define_table(
    'address',
    
    Field('street', 'string'), # only visible if user is borrowing a bike
    Field('city' 'string'),
    Field('postalcode' 'string'),
    Field('country' 'string'),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = 'Street: %(street)s; City: %(city)s; Postalcode: %(postalcode)s; Country: %(country)s',
    singular = 'Address',
    plural = 'Addresses',
)

db.define_table( 
    'address_owner',
    
    Field('address_id', db.address),
    Field('user_id', db.auth_user),
    Field('organisation_id', db.organisation),
    Field('bike_id', db.bike),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
          
    format = '%(address_id)s:',
    singular = 'AddressOwner',
    plural = 'AddressOwners',
)

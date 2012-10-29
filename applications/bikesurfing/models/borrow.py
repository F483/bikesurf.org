# coding: utf8


# TODO list all valid borrow states!

db.define_table(
    'borrow',

    Field('bike_id', db.bike),
    Field('borrower_id', db.auth_user),
    
    Field('from','date'),
    Field('to','date'), # inclusive
    
    Field('accepted','datetime'), # owner accepted borrow request
    Field('confirmed','datetime'), # borrower confirmed
    
    # TODO how to handele stolen and bikes by borrower and 3rd party?
    
    Field('cancled_by', 'string'), # 'owner' or 'borrower' 
    Field('cancled_on','datetime'), 
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(bike_id)s -> %(borrower_id)s',
    singular = 'Borrow',
    plural = 'Borrows',
)

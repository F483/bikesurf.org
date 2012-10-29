# coding: utf8

db.define_table(
    'organisation',
    Field('name', 'string'),
    Field('description', 'text'),
    Field('logo', 'upload', default=''),
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),    
    
    format = '%(name)s',
    singular = 'Organisation',
    plural = 'Organisations',
)

db.define_table(
    'members',
    Field('organisation_id', db.organisation),
    Field('member_id', db.auth_user),
    Field('role', 'string'), # 'admin', 'mechanic' ...
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),    
    
    format = '%(member_id)s -> %(organisation_id)s Role: %(role)s',
    singular = 'Member',
    plural = 'Members',
)

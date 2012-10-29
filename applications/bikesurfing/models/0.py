from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Bikesurfing'
settings.subtitle = 'Borrow a bike for free.'
settings.author = 'Fabian Barkhau'
settings.author_email = 'fabian.barkhau@gmail.com'
settings.keywords = 'bike surfing borrow free'
settings.description = 'Borrow a bike for free.'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '32ac7285-c448-48d6-ae98-2b14778ead11'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

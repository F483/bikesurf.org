# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


ROLES = [
    'OWNER',      # can update team data and add remove users/roles
    'MANAGER',    # can lend team bikes to/from team stations
]
ROLE_CHOICES = [(role, role) for role in ROLES]


SOURCES = [
    'OTHER',
    'COUCHSURFING',
    'FACEBOOK',
    'FRIENDS',
    'GOOGLE',
    'TWITTER',
]
SOURCES_CHOICES = [(source, source) for source in SOURCES]


SITES = [ # TODO add url validation functions per site
    'COUCHSURFING',
    'FACEBOOK',
    'TWITTER',
    'GOOGLEPLUS',
    'BLOG',
    'SKYPE',
]
SITE_CHOICES = [(site, site) for site in SITES]


# TODO use local names without all caps
COUNTRIES_CHOICES = [ # ISO 3166-2
    ('AF', u'AFGHANISTAN'),
    ('AX', u'ÅLAND ISLANDS'),
    ('AL', u'ALBANIA'),
    ('DZ', u'ALGERIA'),
    ('AS', u'AMERICAN SAMOA'),
    ('AD', u'ANDORRA'),
    ('AO', u'ANGOLA'),
    ('AI', u'ANGUILLA'),
    ('AQ', u'ANTARCTICA'),
    ('AG', u'ANTIGUA AND BARBUDA'),
    ('AR', u'ARGENTINA'),
    ('AM', u'ARMENIA'),
    ('AW', u'ARUBA'),
    ('AU', u'AUSTRALIA'),
    ('AT', u'AUSTRIA'),
    ('AZ', u'AZERBAIJAN'),
    ('BS', u'BAHAMAS'),
    ('BH', u'BAHRAIN'),
    ('BD', u'BANGLADESH'),
    ('BB', u'BARBADOS'),
    ('BY', u'BELARUS'),
    ('BE', u'BELGIUM'),
    ('BZ', u'BELIZE'),
    ('BJ', u'BENIN'),
    ('BM', u'BERMUDA'),
    ('BT', u'BHUTAN'),
    ('BO', u'BOLIVIA, PLURINATIONAL STATE OF'),
    ('BQ', u'BONAIRE, SINT EUSTATIUS AND SABA'),
    ('BA', u'BOSNIA AND HERZEGOVINA'),
    ('BW', u'BOTSWANA'),
    ('BV', u'BOUVET ISLAND'),
    ('BR', u'BRAZIL'),
    ('IO', u'BRITISH INDIAN OCEAN TERRITORY'),
    ('BN', u'BRUNEI DARUSSALAM'),
    ('BG', u'BULGARIA'),
    ('BF', u'BURKINA FASO'),
    ('BI', u'BURUNDI'),
    ('KH', u'CAMBODIA'),
    ('CM', u'CAMEROON'),
    ('CA', u'CANADA'),
    ('CV', u'CAPE VERDE'),
    ('KY', u'CAYMAN ISLANDS'),
    ('CF', u'CENTRAL AFRICAN REPUBLIC'),
    ('TD', u'CHAD'),
    ('CL', u'CHILE'),
    ('CN', u'CHINA'),
    ('CX', u'CHRISTMAS ISLAND'),
    ('CC', u'COCOS (KEELING) ISLANDS'),
    ('CO', u'COLOMBIA'),
    ('KM', u'COMOROS'),
    ('CG', u'CONGO'),
    ('CD', u'CONGO, THE DEMOCRATIC REPUBLIC OF THE'),
    ('CK', u'COOK ISLANDS'),
    ('CR', u'COSTA RICA'),
    ('CI', u'CÔTE D\'IVOIRE'),
    ('HR', u'CROATIA'),
    ('CU', u'CUBA'),
    ('CW', u'CURAÇAO'),
    ('CY', u'CYPRUS'),
    ('CZ', u'CZECH REPUBLIC'),
    ('DK', u'DENMARK'),
    ('DJ', u'DJIBOUTI'),
    ('DM', u'DOMINICA'),
    ('DO', u'DOMINICAN REPUBLIC'),
    ('EC', u'ECUADOR'),
    ('EG', u'EGYPT'),
    ('SV', u'EL SALVADOR'),
    ('GQ', u'EQUATORIAL GUINEA'),
    ('ER', u'ERITREA'),
    ('EE', u'ESTONIA'),
    ('ET', u'ETHIOPIA'),
    ('FK', u'FALKLAND ISLANDS (MALVINAS)'),
    ('FO', u'FAROE ISLANDS'),
    ('FJ', u'FIJI'),
    ('FI', u'FINLAND'),
    ('FR', u'FRANCE'),
    ('GF', u'FRENCH GUIANA'),
    ('PF', u'FRENCH POLYNESIA'),
    ('TF', u'FRENCH SOUTHERN TERRITORIES'),
    ('GA', u'GABON'),
    ('GM', u'GAMBIA'),
    ('GE', u'GEORGIA'),
    ('DE', u'GERMANY'),
    ('GH', u'GHANA'),
    ('GI', u'GIBRALTAR'),
    ('GR', u'GREECE'),
    ('GL', u'GREENLAND'),
    ('GD', u'GRENADA'),
    ('GP', u'GUADELOUPE'),
    ('GU', u'GUAM'),
    ('GT', u'GUATEMALA'),
    ('GG', u'GUERNSEY'),
    ('GN', u'GUINEA'),
    ('GW', u'GUINEA-BISSAU'),
    ('GY', u'GUYANA'),
    ('HT', u'HAITI'),
    ('HM', u'HEARD ISLAND AND MCDONALD ISLANDS'),
    ('VA', u'HOLY SEE (VATICAN CITY STATE)'),
    ('HN', u'HONDURAS'),
    ('HK', u'HONG KONG'),
    ('HU', u'HUNGARY'),
    ('IS', u'ICELAND'),
    ('IN', u'INDIA'),
    ('ID', u'INDONESIA'),
    ('IR', u'IRAN, ISLAMIC REPUBLIC OF'),
    ('IQ', u'IRAQ'),
    ('IE', u'IRELAND'),
    ('IM', u'ISLE OF MAN'),
    ('IL', u'ISRAEL'),
    ('IT', u'ITALY'),
    ('JM', u'JAMAICA'),
    ('JP', u'JAPAN'),
    ('JE', u'JERSEY'),
    ('JO', u'JORDAN'),
    ('KZ', u'KAZAKHSTAN'),
    ('KE', u'KENYA'),
    ('KI', u'KIRIBATI'),
    ('KP', u'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF'),
    ('KR', u'KOREA, REPUBLIC OF'),
    ('KW', u'KUWAIT'),
    ('KG', u'KYRGYZSTAN'),
    ('LA', u'LAO PEOPLE\'S DEMOCRATIC REPUBLIC'),
    ('LV', u'LATVIA'),
    ('LB', u'LEBANON'),
    ('LS', u'LESOTHO'),
    ('LR', u'LIBERIA'),
    ('LY', u'LIBYA'),
    ('LI', u'LIECHTENSTEIN'),
    ('LT', u'LITHUANIA'),
    ('LU', u'LUXEMBOURG'),
    ('MO', u'MACAO'),
    ('MK', u'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'),
    ('MG', u'MADAGASCAR'),
    ('MW', u'MALAWI'),
    ('MY', u'MALAYSIA'),
    ('MV', u'MALDIVES'),
    ('ML', u'MALI'),
    ('MT', u'MALTA'),
    ('MH', u'MARSHALL ISLANDS'),
    ('MQ', u'MARTINIQUE'),
    ('MR', u'MAURITANIA'),
    ('MU', u'MAURITIUS'),
    ('YT', u'MAYOTTE'),
    ('MX', u'MEXICO'),
    ('FM', u'MICRONESIA, FEDERATED STATES OF'),
    ('MD', u'MOLDOVA, REPUBLIC OF'),
    ('MC', u'MONACO'),
    ('MN', u'MONGOLIA'),
    ('ME', u'MONTENEGRO'),
    ('MS', u'MONTSERRAT'),
    ('MA', u'MOROCCO'),
    ('MZ', u'MOZAMBIQUE'),
    ('MM', u'MYANMAR'),
    ('NA', u'NAMIBIA'),
    ('NR', u'NAURU'),
    ('NP', u'NEPAL'),
    ('NL', u'NETHERLANDS'),
    ('NC', u'NEW CALEDONIA'),
    ('NZ', u'NEW ZEALAND'),
    ('NI', u'NICARAGUA'),
    ('NE', u'NIGER'),
    ('NG', u'NIGERIA'),
    ('NU', u'NIUE'),
    ('NF', u'NORFOLK ISLAND'),
    ('MP', u'NORTHERN MARIANA ISLANDS'),
    ('NO', u'NORWAY'),
    ('OM', u'OMAN'),
    ('PK', u'PAKISTAN'),
    ('PW', u'PALAU'),
    ('PS', u'PALESTINIAN TERRITORY, OCCUPIED'),
    ('PA', u'PANAMA'),
    ('PG', u'PAPUA NEW GUINEA'),
    ('PY', u'PARAGUAY'),
    ('PE', u'PERU'),
    ('PH', u'PHILIPPINES'),
    ('PN', u'PITCAIRN'),
    ('PL', u'POLAND'),
    ('PT', u'PORTUGAL'),
    ('PR', u'PUERTO RICO'),
    ('QA', u'QATAR'),
    ('RE', u'RÉUNION'),
    ('RO', u'ROMANIA'),
    ('RU', u'RUSSIAN FEDERATION'),
    ('RW', u'RWANDA'),
    ('BL', u'SAINT BARTHÉLEMY'),
    ('SH', u'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA'),
    ('KN', u'SAINT KITTS AND NEVIS'),
    ('LC', u'SAINT LUCIA'),
    ('MF', u'SAINT MARTIN (FRENCH PART)'),
    ('PM', u'SAINT PIERRE AND MIQUELON'),
    ('VC', u'SAINT VINCENT AND THE GRENADINES'),
    ('WS', u'SAMOA'),
    ('SM', u'SAN MARINO'),
    ('ST', u'SAO TOME AND PRINCIPE'),
    ('SA', u'SAUDI ARABIA'),
    ('SN', u'SENEGAL'),
    ('RS', u'SERBIA'),
    ('SC', u'SEYCHELLES'),
    ('SL', u'SIERRA LEONE'),
    ('SG', u'SINGAPORE'),
    ('SX', u'SINT MAARTEN (DUTCH PART)'),
    ('SK', u'SLOVAKIA'),
    ('SI', u'SLOVENIA'),
    ('SB', u'SOLOMON ISLANDS'),
    ('SO', u'SOMALIA'),
    ('ZA', u'SOUTH AFRICA'),
    ('GS', u'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS'),
    ('SS', u'SOUTH SUDAN'),
    ('ES', u'SPAIN'),
    ('LK', u'SRI LANKA'),
    ('SD', u'SUDAN'),
    ('SR', u'SURINAME'),
    ('SJ', u'SVALBARD AND JAN MAYEN'),
    ('SZ', u'SWAZILAND'),
    ('SE', u'SWEDEN'),
    ('CH', u'SWITZERLAND'),
    ('SY', u'SYRIAN ARAB REPUBLIC'),
    ('TW', u'TAIWAN, PROVINCE OF CHINA'),
    ('TJ', u'TAJIKISTAN'),
    ('TZ', u'TANZANIA, UNITED REPUBLIC OF'),
    ('TH', u'THAILAND'),
    ('TL', u'TIMOR-LESTE'),
    ('TG', u'TOGO'),
    ('TK', u'TOKELAU'),
    ('TO', u'TONGA'),
    ('TT', u'TRINIDAD AND TOBAGO'),
    ('TN', u'TUNISIA'),
    ('TR', u'TURKEY'),
    ('TM', u'TURKMENISTAN'),
    ('TC', u'TURKS AND CAICOS ISLANDS'),
    ('TV', u'TUVALU'),
    ('UG', u'UGANDA'),
    ('UA', u'UKRAINE'),
    ('AE', u'UNITED ARAB EMIRATES'),
    ('GB', u'UNITED KINGDOM'),
    ('US', u'UNITED STATES'),
    ('UM', u'UNITED STATES MINOR OUTLYING ISLANDS'),
    ('UY', u'URUGUAY'),
    ('UZ', u'UZBEKISTAN'),
    ('VU', u'VANUATU'),
    ('VE', u'VENEZUELA, BOLIVARIAN REPUBLIC OF'),
    ('VN', u'VIET NAM'),
    ('VG', u'VIRGIN ISLANDS, BRITISH'),
    ('VI', u'VIRGIN ISLANDS, U.S.'),
    ('WF', u'WALLIS AND FUTUNA'),
    ('EH', u'WESTERN SAHARA'),
    ('YE', u'YEMEN'),
    ('ZM', u'ZAMBIA'),
    ('ZW', u'ZIMBABWE'),
]


class Cyclist(models.Model):

    # main data
    user         = models.ForeignKey('auth.User')
    is_team      = models.BooleanField(default=False)
    description  = models.TextField()
    country      = models.CharField(max_length=256, choices=COUNTRIES_CHOICES) # TODO get default according to request lang
    source       = models.CharField(max_length=256, choices=SOURCES_CHOICES, default='OTHER')
    feedback     = models.TextField()
    mobile       = models.CharField(max_length=1024)

    # meta
    created_on   = models.DateTimeField(auto_now_add=True)
    updated_on   = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_team)
        return u"id: %s; user_id: %s; is_team: %s" % args


class Profile(models.Model):

    cyclist     = models.ForeignKey('cyclist.Cyclist')
    site        = models.CharField(max_length=256, choices=SITE_CHOICES)
    link        = models.URLField()
    confirmed   = models.BooleanField(default=False) # done by bike lender

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (self.id, self.cyclist.id, self.site, self.confirmed)
        return u"id: %s; cyclist_id: %s; site: %s; confirmed: %s" % args


class Member(models.Model):

    member      = models.ForeignKey('cyclist.Cyclist', related_name='teams')
    team        = models.ForeignKey('cyclist.Cyclist', related_name='members')
    role        = models.CharField(max_length=256, choices=ROLE_CHOICES)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.member.id, self.team, self.role)
        return u"id: %s; memeber_id: %s; team_id: %s; role: %s" % args


class Picture(models.Model):

    cyclist     = models.ForeignKey('cyclist.Cyclist')
    image       = models.ImageField(upload_to='db/cyclist_images') # FIXME use hash as name to avoid collisisons
    preview     = models.BooleanField(default=False)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.cyclist.id)
        return u"id: %s; cyclist_id: %s" % args



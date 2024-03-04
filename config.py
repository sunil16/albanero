# -*- coding: utf-8 -*-

import os
try:
    import configparser
except:
    from six.moves import configparser

BRAND_NAME = "SHORT URL SERVICE"

SECRET_KEY = "df5JGZfDLMDF54RWrK_aq6Yb9HsdhdjGDDhdaPw="

APP_ENV = os.environ.get("APP_ENV") or "dev"  # or 'live' to load live
INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "./conf/{}.ini".format(APP_ENV)
)

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

POSTGRES = CONFIG["postgres"]
if APP_ENV == "dev":  # credentials not available for dev and live
    DB_CONFIG = (
        POSTGRES["user"],
        POSTGRES["password"],
        POSTGRES["host"],
        POSTGRES["database"]
    )
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s/%s?sslmode=require" % DB_CONFIG
else:
    print("Please provide production db setting")


DB_ECHO = True if CONFIG["database"]["echo"] == "yes" else False
DB_AUTOCOMMIT = True



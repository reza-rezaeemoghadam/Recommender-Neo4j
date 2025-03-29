from neomodel import config
from django.conf import settings

config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL
